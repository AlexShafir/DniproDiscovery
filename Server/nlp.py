
# Done: standart name for platforms and instruments
# Done: add date search (done, we return only years)
# Done: add text main tags (word cloud)

import requests

# # NLTK part
# import nltk
#
# # todo: run only once:
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
#
# from nltk.tokenize import word_tokenize
# from nltk.tag import pos_tag
NLTK_interesting_tags = []

# spaCy part
import spacy
from spacy import displacy
from collections import Counter
# import en_core_web_sm
nlp = spacy.load("en_core_web_sm")

spaCy_interesting_tags = ["PERSON","NORP","FAC","ORG","GPE","LOC","PRODUCT"]
spaCy_location_tags = ["FAC","GPE","LOC",]

from collections import Counter
from string import punctuation


# Google API part
GOOGLE_API_KEY = 'AIzaSyDwzuxWz43qlgfwkUuP4s1rbJJI8jy1iYs'

# Constants
import nlp_constants
from nlp_constants import title, text, args

import re

def extract_lat_long_via_address(address_or_zipcode):
    lat, lng = None, None
    api_key = GOOGLE_API_KEY
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?address={address_or_zipcode}&key={api_key}"
    # see how our endpoint includes our API key? Yes this is yet another reason to restrict the key
    r = requests.get(endpoint)
    if r.status_code not in range(200, 299):
        return None, None
    try:
        '''
        This try block incase any of our inputs are invalid. This is done instead
        of actually writing out handlers for all kinds of responses.
        '''
        results = r.json()['results'][0]
        lat = results['geometry']['location']['lat']
        lng = results['geometry']['location']['lng']
    except:
        pass
    return lat, lng

class TextAnalysis:
    def __init__(self, title: str, text: str, args: dict):
        self.title = title # heading of the article
        self.text = text # text of the article
        self.args = args # additional arguments: (Table of contents, References & Resources, etc)

    # # todo: delete
    # def preprocess(self, text):
    #     data = nltk.word_tokenize(text)
    #     data = nltk.pos_tag(data)
    #     return data
    #
    # # todo: delete
    # def NLTK_tags(self, text):
    #     res = self.preprocess(text)
    #     return res

    def spaCy_tags(self, text):
        # nlp = en_core_web_sm.load()
        doc = nlp(text)
        res = [(X.text, X.label_) for X in doc.ents]
        return res

    def instruments_extraction(self, pairs):
        """
        :param pairs: pairs of words and tags  ('More than a week', 'DATE') or ('good', 'JJ')
        :return: pairs that can be instrument
        """

        instruments_candidates = [pair[0] for pair in pairs if pair[1] in spaCy_interesting_tags ]
        text_instruments = set()
        for instr in instruments_candidates:
            if instr.lower() in nlp_constants.all_instruments.keys():
                text_instruments.add(nlp_constants.all_instruments[instr.lower()])
        return text_instruments

    def platforms__extraction(self, pairs):
        """
        :param pairs: pairs of words and tags  ('More than a week', 'DATE') or ('good', 'JJ')
        :return: pairs that can be platform
        """
        platforms_candidates = [pair[0] for pair in pairs if pair[1] in spaCy_interesting_tags]
        text_platforms = set()
        for pltfrm in platforms_candidates:
            if pltfrm.lower() in nlp_constants.all_platforms.keys():
                text_platforms.add(nlp_constants.all_platforms[pltfrm.lower()])

        return text_platforms

    def locations_extraction(self, pairs):
        """
        :param pairs: pairs of words and tags  ('More than a week', 'DATE') or ('good', 'JJ')
        :return: coordinates of suiting locations
        """
        locations = [pair for pair in pairs if pair[1] in spaCy_location_tags]

        locations = [loc[0] for loc in locations if( len(loc[0]) > 3  and
                                                  loc[0]!='Earth')]

        res = {}
        for loc in locations:
            if(loc.lower() in res.keys()):
                res[loc.lower()][2] += 1
            else:
                res[loc.lower()] = [loc,[],1]

        for loc in res.keys():
            lat_long = extract_lat_long_via_address(loc)
            if(lat_long[0]!=None):
                res[loc][1] = lat_long

        locations = []
        for key in res.keys():
            if(len(res[key][1])!=0):
                locations.append(res[key])

        locations.sort(key = lambda x: x[2], reverse=True)
        print(f"from text locations: {locations}")
        best_locations = [loc[1] for loc in locations if loc[2]>3]
        return best_locations

    def dates_extraction(self, pairs):
        """

        :param pairs: pairs of words and tags  ('More than a week', 'DATE') or ('good', 'JJ')
        :return: suiting dates (currently only returns years, since we don't need month and day)
        """
        dates = set([pair[0] for pair in pairs if pair[1] in ['DATE']])
        res = []
        for date in dates:
            match = re.match(r'.*([1-2][0-9]{3})', date)
            if match is not None:
                # Then it found a match!
                #res.append(date)                    # We can return full date
                res.append(int(match.group(1)))      # We can return only year

        return res

    def keywords_extraction(self, text, num=10):
        """
        Returns most popular words from the text
        :param text:
        :param num: number of most popular words
        :return:
        """
        # nlp = en_core_web_sm.load()

        def get_hotwords(text):
            result = []
            pos_tag = ['PROPN', 'ADJ', 'NOUN',]  # 1
            doc = nlp(text.lower())  # 2
            for token in doc:
                # 3
                if (token.text in nlp.Defaults.stop_words or token.text in punctuation):

                    continue
                # 4
                if (token.pos_ in pos_tag):
                    result.append(token.text)
            return result  # 5

        output = get_hotwords(text)
        most_popular = [x[0].lower() for x in Counter(output).most_common(10)]
        return most_popular

def main(title, text, args):
    tA = TextAnalysis(title, text, args)

    # nltk_tags = tA.NLTK_tags(tA.text)
    # print(f"NLTK tags: {nltk_tags}")

    print("\n TEXT INFO: ")
    text_tags = tA.spaCy_tags(tA.text)
    print(f"spaCy text tags: {text_tags}")

    # print(f"In text instruments:{tA.instruments_extraction(text_tags)}")
    # print(f"In text platforms:{tA.platforms__extraction(text_tags)}")
    # print(f"In text locations:{tA.locations_extraction(text_tags)}")
    # print(f"In text dates:{tA.dates_extraction(text_tags)}")
    # print(f"In text keywords:{tA.keywords_extraction(tA.text)}")

    print("\n TITLE INFO: ")
    title_tags = tA.spaCy_tags(tA.title)
    print(f"spaCy title tags: {title_tags}")
    #
    # print(f"In title instruments:{tA.instruments_extraction(title_tags)}")
    # print(f"In title platforms:{tA.platforms__extraction(title_tags)}")
    # print(f"In title locations:{tA.locations_extraction(title_tags)}")
    # print(f"In title years:{tA.dates_extraction(title_tags)}")



if __name__ == '__main__':
    main(nlp_constants.title, nlp_constants.text, nlp_constants.args)
