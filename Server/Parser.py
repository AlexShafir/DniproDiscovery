import sections.SectImages as SectImages
import sections.SectArticles as SectArticles
import sections.SectBlogs as SectBlogs

def parse(url):

    # Images:
    if 'https://earthobservatory.nasa.gov/images/' in url:
        parsed = SectImages.parse(url)
        print(f"parsed: {parsed}")
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



    """
    # image example
    res = parse("https://earthobservatory.nasa.gov/images/147342/superior-fall-colors")
    
    # article example
    # res = parse("https://earthobservatory.nasa.gov/features/covid-seasonality")

    # blog example
    # res = parse("https://earthobservatory.nasa.gov/blogs/earthmatters/category/reader-mail/")
    # print(f'res: {res}')
    """

    parsed = {
        "title":"California’s Nightmare Fire Season Continues",
        "text":"""After a brief lull, a late-September heat wave reinvigorated California’s already brutal 2020 fire season.

The Visible Infrared Imaging Radiometer Suite (VIIRS) on the NOAA-20 satellite captured this natural-color image of the state on October 1, 2020. The volume of smoke coming from the fires has been high in recent days and has spread across much of the state.

On the same day, the Environmental Protection Agency’s Airnow system reported that many sensors across the state had measured unhealthy (between 150-200 on the air quality index) and hazardous (above 300 AQI) conditions in recent days. In a few cases, especially close to the fires, sensors recorded AQI values that exceeded 1000.

According to Cal Fire, fires have charred more than 3.7 million acres in California since the beginning of the year. Blazes have destroyed more than 8,000 structures and taken at least 31 lives. As of October 2, more than 50,000 people faced evacuation orders.

Several fires are contributing to the layer of smoke currently hanging over the state. Some of the most active and least controlled included the Glass Fire (6 percent contained), the Red Salmon Complex (31 percent), the Creek (45 percent), the Slater (50 percent), August Complex (51 percent), the SQF Complex (61 percent), and the North Complex (79 percent).

The August Complex, the largest fire by area on record in California, had burned nearly 1 million acres by October 2. The North Complex Fire, having destroyed more than 2,315 structures, was the fifth most destructive on record. The Glass Fire, currently the least controlled of California's fires, has devastated several vineyards and smothered the Bay Area with smoke.

Wildfire smoke contains a potent mixture of particles and gases that can pose a serious health hazard. According to one recent analysis from researchers with Stanford’s Center on Food Security and the Environment, poor air quality from fires in August and September 2020 likely contributed to more than 1,200 excess deaths and 4,800 additional hospital visits in California.

NASA Earth Observatory images by Joshua Stevens, using VIIRS data from NASA EOSDIS/LANCE and GIBS/Worldview and the Joint Polar Satellite System (JPSS). Story by Adam Voiland.""",
        "tags":["Image of the day","Atmosphere", "Heat", "Land","Fires","Human Presence",],
        "dates":[2020],
        "R&R":"""Deryugina, T. et al. (2019) The Mortality and Medical Costs of Air Pollution: Evidence from Changes in Wind Direction. American Economic Review, 109 (12), 4178-4219.
G-Feed (2020, September 11) Indirect mortality from recent wildfires in CA. Accessed October 2, 2020.
Los Angeles Times (2020, October 1) Fall heat wave breaks records, prompts statewide flex alert to conserve energy. Accessed October 2, 2020.
NASA Earth Observatory (2020) 2020 Fire Season in the Western U.S.
NASA Earth Science Disasters Program (2020) NASA Products for the California Fires August 2020. Accessed October 2, 2020.
The Sacramento Bee (2020, September 23) ‘These are hidden deaths’ Over 1,000 likely died early due to California’s wildfire smoke. Accessed October 2, 2020.
The Washington Post (2020, October 1) California wildfires prompt new warnings amid record heat, erratic winds. Accessed October 2, 2020.""",
        "platInstr": [['NOAA-20', 'VIIRS']],
        "coord": ['46.866880494515', '-89.99947993713'],
    }
    ids = SectImages.process(parsed)


