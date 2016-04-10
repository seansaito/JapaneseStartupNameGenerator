"""
English to Japanese Translator Module for JapaneseStartupNameGenerator
This module uses beautiful soup to scrape English to Japanese translations
in both Hiragana and Romaji

Author  Sean Saito
"""

from bs4 import BeautifulSoup
from global_vars import *
from multiprocessing import Pool
import os, json, requests

class Translator(object):

    def __init__(self):
        self.root_url = "http://romajidesu.com/dictionary/meaning-of-{phrase}.html"
        self.cache_uri = os.path.join(script_dir, "app/static/json/translation_cache.json")
        self.cache = self.load_cache()

    def load_cache(self):
        with open(self.cache_uri, "r") as fp:
            store = json.load(fp)
            fp.close()
            return store
        return {}

    def get_translations_aux(self, word):
        """ For a single word/phrase """
        full_url = self.root_url.format(phrase=word)
        print "Making request to %s" % full_url
        response = requests.get(full_url)
        soup = BeautifulSoup(response.text, "html.parser")
        return [a for a in soup.find_all("rt")]

    def get_translations(self, words):
        """
        Gets translations for an array of words.
        Args:
            words (list)    : list of words
        Examples:
            Translator.get_translations(["dog", "pet", "hospitality", "cute"])

        """
        pool = Pool(len(words))
        results = pool.map(self.get_translations_aux, words)
        return results
