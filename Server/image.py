import requests
from bs4 import BeautifulSoup
import json
from types import SimpleNamespace
from datetime import datetime

def parse(url):

    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'html.parser')

    # In "images" we can extract: point coordinate, instrument, platform, provider, dates from images

    ## Coordinate
    coord = soup.select_one('p.text-center.map-link > a')['href'].split('/')
    lat, lon = coord[2], coord[3]

    ## Instrument
    instrDd = soup.select('dl.instruments > dd')
    platInstr = []
    for i in instrDd:
        t = i.text.split(' — ')

        res = requests.get(f"https://cmr.earthdata.nasa.gov/search/autocomplete?q={t[0]}&pretty=true")
        items = json.loads(res.text, object_hook=lambda d: SimpleNamespace(**d))
        for e in items.feed.entry:
            if e.type == 'platform':
                plat = e.value
                break

        res = requests.get(f"https://cmr.earthdata.nasa.gov/search/autocomplete?q={t[1]}&pretty=true")
        items = json.loads(res.text, object_hook=lambda d: SimpleNamespace(**d))
        for e in items.feed.entry:
            if e.type == 'instrument':
                instr = e.value
                break

        platInstr.append([plat, instr])
        # Substitute platform, instrument to autocomplete

    #print(platInstr)


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
        t = datetime.strptime(t, '%B %d, %Y')
        dates.append(t)

    dates = list(set(dates))

    ## todo: Provider


    # Now we have everything from article and can filter results
    colIds = []

    for item in platInstr:
        plat, instr = item
        res = requests.get(f"https://cmr.earthdata.nasa.gov/search/collections.json?point={lon},{lat}&platform={plat}&instrument={instr}&has_granules=true&pretty=true")
        items = json.loads(res.text, object_hook=lambda d: SimpleNamespace(**d))

        # Iterate collections

        for e in items.feed.entry:

            # Filter by granules
            res = requests.get(f"https://cmr.earthdata.nasa.gov/search/granules.json?collection_concept_id={e.id}&point={lon},{lat}&pretty=true")
            granules = json.loads(res.text, object_hook=lambda d: SimpleNamespace(**d))

            if len(granules.feed.entry) == 0: continue

            colIds.append([e.title, e.id])

            """
    
            if hasattr(e, 'time_end'):
                dateEnd = datetime.strptime(e.time_start, '%Y-%m-%dT%H:%M:%S.%fZ')
                atleastEnd = False
                for date in dates:
                    if dateEnd > date:
                        atleastEnd = True
                        break
    
                if not atleastEnd: continue
    
            atleastStart = False
            dateStart = datetime.strptime(e.time_start, '%Y-%m-%dT%H:%M:%S.%fZ')
            for date in dates:
                if dateStart < date:
                    atleastStart = True
                    break
    
            if not atleastStart: continue
            """


        #print(res.text)

    return colIds
    # First execute search using location