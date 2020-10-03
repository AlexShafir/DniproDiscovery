import requests
from bs4 import BeautifulSoup
import json
from types import SimpleNamespace

def parse(url):
    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'html.parser')

    ## Title
    title = soup.find("meta", attrs={"name": "DC.Title"})['content']

    ## Text
    articleP = soup.select('div.col-lg-8.col-md-8.col-sm-8.col-xs-12.col-md-right-space p')
    articleText = ""
    for p in articleP:
        articleText = articleText + "\n" + p.text

    ## Tags
    tagz = soup.select("div.panel.panel-default.panel-circle-container.hidden-xs a.btn.btn-tag.hvr-rectangle-in.btn-sm")
    tags = []
    for i in tagz:
        tags.append(i.text)

    ## R & R
    linkz = soup.select("ul.references li")
    links = []
    for i in linkz:
        links.append(i.text)

    ## Picture text
    picturr = soup.select('div.caption p')
    pictureText = []
    for i in picturr:
        pictureText.append(i.text)
    print(pictureText)

    return {
        "title": title,
        "tags": tags,
        "R&R": links,
        "pictureText": pictureText,
        "text": articleText
    }

def process(parsed):
    pass

if __name__ == '__main__':
    t = parse("https://earthobservatory.nasa.gov/features/covid-seasonality")

    print(t)