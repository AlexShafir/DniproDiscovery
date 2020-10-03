import sections.SectImages as SectImages
import sections.SectArticles as SectArticles
import sections.SectBlogs as SectBlogs

def parse(url):

    # Images:
    if 'https://earthobservatory.nasa.gov/images/' in url:
        parsed = SectImages.parse(url)
        # print(f"parsed: {parsed}")
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


if __name__ == '__main__':
    # image example
    # res = parse("https://earthobservatory.nasa.gov/images/147342/superior-fall-colors")
    res = parse("https://earthobservatory.nasa.gov/images/147350/spalte-splits")
    for i, el in enumerate(res):
        print(f"{i} : {el}")
    """
    
    
    # article example
    # res = parse("https://earthobservatory.nasa.gov/features/covid-seasonality")

    # blog example
    # res = parse("https://earthobservatory.nasa.gov/blogs/earthmatters/category/reader-mail/")
    # print(f'res: {res}')
    """
