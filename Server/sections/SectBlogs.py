import requests
from bs4 import BeautifulSoup
import json
from types import SimpleNamespace
import sys
sys.path.append("..")
import nlp, nlp_constants
import re


def tags_fusion(parced_tags, from_text_tags, tags_max=20):
    final_tags = []  # fusion of text tags and predefined tags
    for tag in from_text_tags:
        if (tag in parced_tags):
            final_tags.append(tag)

    for tag in parced_tags:
        if (tag not in final_tags):
            final_tags.append(tag)

    for tag in from_text_tags:
        if (tag not in final_tags):
            final_tags.append(tag)

    final_tags = final_tags[:tags_max]
    return final_tags

def generate_all_pairs(platforms, instruments):
    res = []
    if (len(platforms) == 0 and len(instruments) == 0):
        pass
    elif (len(platforms) > 0 and len(instruments) == 0):
        res = [[plt, None] for plt in platforms]
    elif (len(platforms) == 0 and len(instruments) > 0):
        res = [[None, instr] for instr in instruments]
    for plt in platforms:
        for instr in instruments:
            res.append([plt, instr])
    return res

def generate_search_url(plat,instruments, lat_long):

    base_part = f"https://cmr.earthdata.nasa.gov/search/collections.json?"

    # platform search
    plat_part = ""
    if(plat!=None):
        plat_part = f"platform={plat}"

    # instruments search
    instr_part = ""
    for instr in instruments:
        instr_part += f"instrument={instr}&"

    # location search
    loc_part = ""
    lat, lon = lat_long
    loc_part = ""
    if(lat!=None):
        loc_part = f"point={lon},{lat}&"

    end_part = "has_granules=true&pretty=true"

    search_url = base_part +  plat_part + instr_part + loc_part + end_part
    return search_url

def generate_tags_search_url(tags):

    base_part = f"https://cmr.earthdata.nasa.gov/search/collections.json?"

    keyword_part = f"keyword ="
    for tag in tags:
        keyword_part+=tag + "%20"

    end_part = "has_granules=true&pretty=true"

    search_url = base_part +  keyword_part + end_part
    return search_url

def sort_by_keywords(colIds, final_tags):
    res = []
    for title in colIds.keys():
        dataset_score = 10* colIds[title][3]
        text = colIds[title][0].lower() + colIds[title][2].lower()
        for i, keyword in enumerate(final_tags):
            dataset_score += (25 - i) * text.count(keyword)
        res.append([colIds[title][0], colIds[title][1], dataset_score])
    res.sort(key=lambda x: x[2], reverse=True)
    print(f'SORTED results:')
    for el in res:
        print(el)
    print('=====')
    res = [[el[0], el[1]] for el in res]
    return res

def colIds_from_url(colIds, url, lat_long):
    res = requests.get(url)
    items = json.loads(res.text, object_hook=lambda d: SimpleNamespace(**d))
    for e in items.feed.entry:
        if (lat_long == [[None,None]]):
            if (e.title not in colIds.keys()):
                colIds[e.title] = [e.title, e.id, e.summary, 0]
            else:
                pass
        else: # Check granules by location
            collection_url = f"https://cmr.earthdata.nasa.gov/search/granules.json?collection_concept_id={e.id}&point={lon},{lat}&pretty=true"
            res = requests.get(collection_url)
            granules = json.loads(res.text, object_hook=lambda d: SimpleNamespace(**d))

            if len(granules.feed.entry) == 0:
                continue
            else:
                if (e.title not in colIds.keys()):
                    colIds[e.title] = [e.title, e.id, e.summary, 1]
                else:
                    pass

    return colIds

def parse(url):
    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'html.parser')

    ## Title
    title = soup.find("meta", attrs={"name": "DC.Title"})['content']

    ## Publish Year
    t = soup.find("meta", attrs={"name": "DC.Date"})['content']
    match = re.match(r'.*([1-2][0-9]{3})', t)
    if match is not None:
        publishYear = int(match.group(1))

    ## Text
    articleP = soup.select('div.col-lg-8.col-md-8.col-sm-8.col-xs-12.col-md-right-space p')
    articleText = ""
    for p in articleP:
        articleText = articleText + "\n" + p.text

    ## Picture text
    picturr = soup.select('figcaption')
    pictureText = []
    for i in picturr:
        pictureText.append(i.text)

    ## Tags
    tagz = soup.find_all('a', attrs={'rel':'tag'})
    tags = []
    for i in tagz:
        tags.append(i.text)

    return {
        "title": title,
        "publishYear": publishYear,
        "tags": tags,
        "pictureText": pictureText,
        "text": articleText,
    }

def process(parsed):
    """

    :param parsed:
        "title": title,
        "publishYear": publishYear,
        "tags": tags,
        "pictureText": pictureText,
        "text": articleText,
    :type parsed: dict

    :return: list of ids
    :rtype: list

    """

    ### ================================ P A R S E D    D A T A ===========================
    title = parsed["title"]
    text = parsed["text"]
    parced_tags = parsed["tags"]
    publishYear = parsed["publishYear"]
    pictureText = parsed["pictureText"]

    ### ================================ T E X T    D A T A ==============================

    args = {}
    tA = nlp.TextAnalysis(title=title, text=text, args=args)
    text_tags = tA.spaCy_tags(tA.text)

    from_text_instruments = tA.instruments_extraction(text_tags)
    from_text_platforms = tA.platforms__extraction(text_tags)
    from_text_locations = tA.locations_extraction(text_tags)
    from_text_dates = tA.dates_extraction(text_tags)
    from_text_tags = tA.keywords_extraction(tA.text, 10)

    # Tags processing

    # location processing:
    # print(f'best locations: {from_text_locations[:10]}')

    ### ================================ P R O C E S S I N G =============================

    # tags creation
    final_tags = tags_fusion(parced_tags, from_text_tags, 20)

    colIds = {}

    if(len(from_text_platforms)==0 and len(from_text_locations) == 0 and len(from_text_instruments) == 0):
        print("No important infro, search by tags")
        search_url = generate_tags_search_url(final_tags)
        colIds = colIds_from_url(colIds, search_url, [None, None])
    else:
        if(len(from_text_platforms)==0):
            from_text_platforms = [None]
        if(len(from_text_locations)==0):
            from_text_locations = [[None,None]]

        # search by platform, all instruments and concrete location
        for plat in from_text_platforms:
            for lat_long in from_text_locations:
                search_url = generate_search_url(plat, from_text_instruments, lat_long)
                colIds = colIds_from_url(colIds, search_url, lat_long)

        # If we don't have enought results, we drop search by location
        if (len(colIds.keys()) < 10 and from_text_locations!=[[None,None]]):
            for plat in from_text_platforms:
                search_url = generate_search_url(plat, from_text_instruments, [None,None])
                colIds = colIds_from_url(colIds, search_url, [None,None])

    Ordered_colIds = sort_by_keywords(colIds, final_tags)

    # print(f'Ordered result: {Ordered_colIds}')
    return Ordered_colIds[:10]

if __name__ == '__main__':
    t = parse("https://earthobservatory.nasa.gov/blogs/earthmatters/2020/06/29/nasa-esa-and-jaxa-provide-global-observations-of-covid-19-impacts/")

    print(t)