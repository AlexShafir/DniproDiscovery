import requests
from bs4 import BeautifulSoup
import json
from types import SimpleNamespace
from datetime import datetime

def parse(url):
    return {
        "title":"",
        "text":"",
        "tags":"",
        "R&R":"",
    }

def process(parsed):
    pass