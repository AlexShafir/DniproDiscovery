import image

def parse(url):
    ids = []
    if 'image' in url:
        ids = image.parse(url)

    # Convert ids to links
    out = {}

    for id in ids:
        s = f"https://search.earthdata.nasa.gov/search/granules?p={id[1]}"
        out[id[0]] = s

    return out
