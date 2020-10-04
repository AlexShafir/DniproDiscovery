import sections.SectImages as SectImages
import sections.SectArticles as SectArticles
import sections.SectBlogs as SectBlogs
import time
def parse(url, results_num = 10):
    # Images:
    if 'https://earthobservatory.nasa.gov/images/' in url:
        parsed = SectImages.parse(url)
        ids = SectImages.process(parsed, results_num = 10)
    if 'https://earthobservatory.nasa.gov/features/' in url:
        parsed = SectArticles.parse(url)

        ids = SectArticles.process(parsed, results_num = 10)
    if 'https://earthobservatory.nasa.gov/blogs/' in url:
        parsed = SectBlogs.parse(url)
        ids = SectBlogs.process(parsed, results_num = 10)
    # Convert ids to links
    out = {}

    for id in ids:
        s = f"https://search.earthdata.nasa.gov/search/granules?p={id[1]}"
        out[id[0]] = s

    return out


if __name__ == '__main__':
    results_num = 10
    timer_start = time.time()
    # image examples
    # res = parse("https://earthobservatory.nasa.gov/images/147342/superior-fall-colors", results_num)
    # res = parse("https://earthobservatory.nasa.gov/images/147350/spalte-splits", results_num)
    # res = parse("https://earthobservatory.nasa.gov/images/147355/coloring-the-great-salt-lake", results_num)
    res = parse("https://earthobservatory.nasa.gov/images/147261/a-wall-of-smoke-on-the-us-west-coast", results_num)

    # article examples
    # res = parse("https://earthobservatory.nasa.gov/features/disease-vector", results_num)
    # res = parse("https://earthobservatory.nasa.gov/features/covid-seasonality", results_num)
    # res = parse("https://earthobservatory.nasa.gov/features/pine-island", results_num)

    # blog example
    # res = parse("https://earthobservatory.nasa.gov/blogs/earthmatters/2016/08/17/perseids-or-sporadic-meteors-maybe-both/", results_num)
    # res = parse("https://earthobservatory.nasa.gov/blogs/fromthefield/2020/09/23/polarstern-at-the-north-pole/", results_num)


    for i, el in enumerate(res):
        print(f"{i} : {el}")

    print(f"\nTime spent on processing: {time.time() - timer_start}")