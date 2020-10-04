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
    # image examples
    # res = parse("https://earthobservatory.nasa.gov/images/147342/superior-fall-colors")
    # res = parse("https://earthobservatory.nasa.gov/images/147350/spalte-splits")

    # article examples
    # res = parse("https://earthobservatory.nasa.gov/features/disease-vector")
    # res = parse("https://earthobservatory.nasa.gov/features/covid-seasonality")
    # res = parse("https://earthobservatory.nasa.gov/features/pine-island")

    # blog example
    # res = parse("https://earthobservatory.nasa.gov/blogs/earthmatters/2016/08/17/perseids-or-sporadic-meteors-maybe-both/")
    res = parse("https://earthobservatory.nasa.gov/blogs/fromthefield/2020/09/23/polarstern-at-the-north-pole/")


    for i, el in enumerate(res):
        print(f"{i} : {el}")

