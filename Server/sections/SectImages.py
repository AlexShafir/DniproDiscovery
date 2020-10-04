import requests
from bs4 import BeautifulSoup
import json
from types import SimpleNamespace
import sys
sys.path.append("..")
import nlp, nlp_constants
import re


def parse(url):

    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'html.parser')

    # In "images" we can extract: point coordinate, instrument, platform, provider, dates from images

    ## Title
    title = soup.find("meta", attrs={"name":"DC.Title"})['content']

    ## Publish Year
    t = soup.find("meta", attrs={"name": "DC.Date"})['content']
    match = re.match(r'.*([1-2][0-9]{3})', t)
    if match is not None:
        publishYear = int(match.group(1))

    ## Tags
    tagz = soup.select("a.btn.btn-tag.hvr-rectangle-in.btn-sm")
    tags = []
    not_informative_tags = ['Image of the Day', 'Human Presence']
    for i in tagz:
        if not (i.text in not_informative_tags):
            tags.append(i.text.lower())

    ## R & R
    linkz = soup.select("div.col-xs-12.references-content li")
    links = []
    for i in linkz:
        links.append(i.text)

    ## Coordinate
    coord = soup.select_one('p.text-center.map-link > a')['href'].split('/')
    lat, lon = coord[2], coord[3]

    ## Instrument
    instrDd = soup.select('dl.instruments > dd')
    platInstr = []
    for i in instrDd:
        t = i.text.split(' — ')

        if t[0].lower() in nlp_constants.all_platforms.keys():
            plat = nlp_constants.all_platforms[t[0].lower()]

        if t[1].lower() in nlp_constants.all_instruments.keys():
            instr = nlp_constants.all_instruments[t[1].lower()]

        platInstr.append([plat, instr])
        # Substitute platform, instrument to autocomplete

    ## Article text w/o dates
    articleP = soup.select('div.col-lg-8.col-md-8.col-sm-8.col-xs-12.col-md-right-space.col-md-bottom-space > p')
    articleText = ""
    for p in articleP:
        articleText = articleText + "\n" + p.text

    ## Dates from images

    dateP = soup.select('div.panel-footer > p')
    dates = []
    for p in dateP:
        t = p.contents[0]
        if '-' in t: continue
        match = re.match(r'.*([1-2][0-9]{3})', t)
        if match is not None:
            dates.append(int(match.group(1)))

    dates = list(set(dates))


    return {
        "platInstr": platInstr,
        "coord": [lat, lon],
        "title": title,
        "publishYear": publishYear,
        "tags": tags,
        "dates": dates,
        "R&R": links,
        "text": articleText
    }

def process(parsed):
    """

    :param parsed:
        "platInstr": platInstr,
        "coord": [lat, lon],
        "title": title,
        "publishYear": publishYear,
        "tags": tags,
        "dates": dates,
        "R&R": links,
        "text": articleText
    :type parsed: dict

    :return: list of ids
    :rtype: list

    """

    title = parsed["title"]
    text = parsed["text"]
    tags = parsed["tags"]
    dates = parsed["dates"]
    R_and_R = parsed["R&R"]
    lat, lon = parsed["coord"]
    platInstr = parsed["platInstr"]

    ### TEXT INFO :
    args = {"R&R":parsed["R&R"]}
    tA = nlp.TextAnalysis(title=title, text=text, args=args )
    text_tags = tA.spaCy_tags(tA.text)

    from_text_instruments = tA.instruments_extraction(text_tags)
    from_text_platforms = tA.platforms__extraction(text_tags)
    from_text_locations = tA.locations_extraction(text_tags)
    from_text_dates = tA.dates_extraction(text_tags)
    from_text_tags = tA.keywords_extraction(tA.text, 10)


    # Tags processing
    # print(f'tags: {tags}')
    # print(f'from_text_tags: {from_text_tags}')
    final_tags = [] # fusion of text tags and predefined tags
    for tag in from_text_tags:
        if(tag in tags):
            final_tags.append(tag)

    for tag in tags:
        if(tag not in final_tags):
            final_tags.append(tag)

    for tag in from_text_tags:
        if(tag not in final_tags):
            final_tags.append(tag)

    final_tags = final_tags[:20]
    # print(f'best tags: {final_tags[:20]}')
    # location processing:
    # print(f'best locations: {from_text_locations[:10]}')


    ### PROCESSING :

    # Now we have everything from article and can filter results
    colIds = []
    if(len(platInstr)==0):
        def generate_all_pairs(platforms, instruments):
            res = []
            if(len(platforms) == 0 and len(instruments) == 0):
                pass
            elif(len(platforms) > 0 and len(instruments) == 0):
                res = [[plt, None] for plt in platforms]
            elif(len(platforms) == 0 and len(instruments) > 0):
                res = [[None, instr] for instr in instruments]
            for plt in platforms:
                for instr in instruments:
                    res.append([plt,instr])
            return res
        platInstr = generate_all_pairs(from_text_platforms, from_text_instruments)
    if (len(platInstr) == 0):
        platInstr = [[None, None]]
    for item in platInstr:

        plat, instr = item
        if(plat==None and instr == None):
            search_url = f"https://cmr.earthdata.nasa.gov/search/collections.json?point={lon},{lat}&has_granules=true&pretty=true"
        elif(plat!=None and instr == None):
            search_url = f"https://cmr.earthdata.nasa.gov/search/collections.json?point={lon},{lat}&platform={plat}&has_granules=true&pretty=true"
        elif(plat==None and instr != None):
            search_url = f"https://cmr.earthdata.nasa.gov/search/collections.json?point={lon},{lat}&instrument={instr}&has_granules=true&pretty=true"
        else:
            search_url = f"https://cmr.earthdata.nasa.gov/search/collections.json?point={lon},{lat}&platform={plat}&instrument={instr}&has_granules=true&pretty=true"
        res = requests.get(search_url)
        items = json.loads(res.text, object_hook=lambda d: SimpleNamespace(**d))

        # Iterate collections

        for e in items.feed.entry:

            # Filter by granules
            collection_url = f"https://cmr.earthdata.nasa.gov/search/granules.json?collection_concept_id={e.id}&point={lon},{lat}&pretty=true"
            res = requests.get(collection_url)
            granules = json.loads(res.text, object_hook=lambda d: SimpleNamespace(**d))

            if len(granules.feed.entry) == 0: continue

            colIds.append([e.title, e.id, e.summary])
            
    # print(f'Results: {colIds}')

    Ordered_colIds = []
    def sort_by_keywords():
        res = []
        for el in colIds:
            el_count = 0
            text = el[0].lower() + el[2].lower()
            for i, keyword in enumerate(final_tags):
                el_count += (25-i) * text.count(keyword)
            res.append([el[0],el[1], el_count])
        res.sort(key = lambda x: x[2], reverse=True)
        res = [[el[0],el[1]] for el in res]
        return res

    Ordered_colIds = sort_by_keywords()

    #print(f'Ordered result: {Ordered_colIds}')
    return Ordered_colIds[:10]

if __name__ == '__main__':
    t = parse("https://earthobservatory.nasa.gov/images/147350/spalte-splits")
    print(t)
    print()

