import sections.SectImages as SectImages

def parse(url):

    # Images:
    if 'https://earthobservatory.nasa.gov/images/' in url:
        parsed = SectImages.parse(url)
        ids = SectImages.processParsed(parsed)

    # Convert ids to links
    out = {}

    for id in ids:
        s = f"https://search.earthdata.nasa.gov/search/granules?p={id[1]}"
        out[id[0]] = s

    return out
