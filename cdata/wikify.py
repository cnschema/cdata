#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Li Ding

# wikification apis

import os
import sys
import json
import logging
import datetime
import logging
import time
import urllib
import re

import requests

from misc import main_subtask
from core import *


def task_compare(args):
    queries = [
        "autodealer",
        "birthplace",
        u"居里夫人",
        u"爱因斯坦",
    ]
    for query  in queries:
        args ={"query": query}
        logging.info(u"-----{}------".format(query))
        task_wikipedia_test(args)

        task_wikidata_test(args)

def task_wikipedia_test(args):
    ret = wikipedia_search(args["query"])
    logging.info(json.dumps(ret, ensure_ascii=False, sort_keys=True, indent=4))
    # ret = wikipedia_search_slow(query)
    # logging.info(json.dumps(ret, ensure_ascii=False, sort_keys=True, indent=4))

def task_wikidata_test(args):
    ret = wikidata_search(args["query"])
    logging.info(json.dumps(ret, ensure_ascii=False, sort_keys=True, indent=4))
    if ret["itemList"]:
        nodeid = ret["itemList"][0]["identifier"]
        ret = wikidata_get(nodeid)
        logging.info(json.dumps(ret["entities"][nodeid]["labels"]["zh"]["value"], ensure_ascii=False, sort_keys=True, indent=4))

def wikidata_get(identifier):
    """
        https://www.wikidata.org/wiki/Special:EntityData/P248.json
    """
    url = 'https://www.wikidata.org/wiki/Special:EntityData/{}.json'.format(identifier)
    #logging.info(url)
    return json.loads(requests.get(url).content)

def wikidata_search(query, lang="zh", output_lang="en",  searchtype="item",  max_result=1):
    """
        wikification: search wikipedia pages for the given query
        https://www.wikidata.org/w/api.php?action=help&modules=wbsearchentities

        result format
        {
            searchinfo: - {
            search: "birthday"
            },
            search: - [
            - {
                repository: "",
                id: "P3150",
                concepturi: "http://www.wikidata.org/entity/P3150",
                url: "//www.wikidata.org/wiki/Property:P3150",
                title: "Property:P3150",
                pageid: 28754653,
                datatype: "wikibase-item",
                label: "birthday",
                description: "item for day and month on which the subject was born. Used when full "date of birth" (P569) isn't known.",
                match: - {
                type: "label",
                language: "en",
                text: "birthday"
            }
        }
    """
    query = any2unicode(query)
    params = {
        "action":"wbsearchentities",
        "search": query,
        "format":"json",
        "language":lang,
        "uselang":output_lang,
        "type":searchtype
    }
    urlBase = "https://www.wikidata.org/w/api.php?"
    url = urlBase + urllib.urlencode(any2utf8(params))
    #logging.info(url)
    r = requests.get(url)
    results = json.loads(r.content).get("search",[])
    #logging.info(items)

    property_list = [
        {"name":"name", "alternateName":["label"]},
        {"name":"url", "alternateName":["concepturi"]},
        {"name":"identifier", "alternateName":["id"]},
        {"name":"description"},
    ]
    items = []
    ret = {"query": query, "itemList":items}
    for result in results[0:max_result]:
        #logging.info(result)
        item = json_dict_copy(result, property_list)
        items.append(item)
    return ret

def wikipedia_search_slow(query, lang="en", max_result=1):
    import wikipedia
    #wikification
    query = any2unicode(query)
    items = []
    ret = {"query":query, "itemList":items}
    wikipedia.set_lang(lang)
    wikiterm = wikipedia.search(query)
    #logging.info(wikiterm)
    for idx, term in enumerate(wikiterm[0:max_result]):
        wikipage = wikipedia.page(term)
        item = {
            "name": wikipage.title,
            "description": wikipedia.summary(term, sentences=1),
            "url": wikipage.url,
        }
        items.append(item)

    return ret

def wikipedia_search(query, lang="en", max_result=1):
    """
        https://www.mediawiki.org/wiki/API:Opensearch
    """
    query = any2unicode(query)
    params = {
        "action":"opensearch",
        "search": query,
        "format":"json",
        #"formatversion":2,
        #"namespace":0,
        "suggest":"true",
        "limit": 10
    }
    urlBase = "https://{}.wikipedia.org/w/api.php?".format(lang)
    url = urlBase + urllib.urlencode(any2utf8(params))
    #logging.info(url)
    r = requests.get(url)
    jsonData = json.loads(r.content)
    #logging.info(jsonData)

    items = []
    ret = {"query":query, "itemList":items}
    for idx, label in enumerate(jsonData[1][0:max_result]):
        description = jsonData[2][idx]
        url = jsonData[3][idx]

        item = {
            "name": label,
            "description":description,
            "url": url,
        }
        items.append(item)

    return ret

if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname)s][%(asctime)s][%(module)s][%(funcName)s][%(lineno)s] %(message)s', level=logging.INFO)
    logging.getLogger("requests").setLevel(logging.WARNING)

    optional_params = {
        '--query': 'query'
    }
    main_subtask(__name__, optional_params=optional_params)

"""
    python cdata/wikify.py task_wikipedia_test --query="birth place"
    python cdata/wikify.py task_wikidata_test --query="birth place"
    python cdata/wikify.py task_wikidata_test --query="birthplace"
    python cdata/wikify.py task_wikidata_test --query=居里夫人

    python cdata/wikify.py task_compare

"""
