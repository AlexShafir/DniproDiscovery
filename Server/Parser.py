import sections.SectImages as SectImages
import sections.SectArticles as SectArticles
import sections.SectBlogs as SectBlogs

def parse(url):

    # Images:
    if 'https://earthobservatory.nasa.gov/images/' in url:
        parsed = SectImages.parse(url)
        ids = SectImages.process(parsed)
    if 'https://earthobservatory.nasa.gov/features/' in url:
        parsed = SectArticles.parse(url)
        ids = SectArticles.process(parsed)
    if 'https://earthobservatory.nasa.gov/blogs/' in url:
        parsed = SectBlogs.parse(url)
        ids = SectBlogs.process(parsed)

    # Convert ids to links
    out = {}

    for id in ids:
        s = f"https://search.earthdata.nasa.gov/search/granules?p={id[1]}"
        out[id[0]] = s

    return out
