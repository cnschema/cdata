#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Path hack
import os
import sys
import logging
sys.path.insert(0, os.path.abspath('..'))

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from cdata.wikify import wikidata_search, wikidata_get  # noqa


class WikifyTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_wikidata(self):
        query = u"居里夫人"
        ret = wikidata_search(query, lang="zh")
        #logging.info(ret)
        nodeid = ret["itemList"][0]["identifier"]
        assert nodeid == "Q7186"
        ret = wikidata_get(nodeid)
        lable_zh = ret["entities"][nodeid]["labels"]["zh"]["value"]
        assert lable_zh == u"玛丽·居里"

        query = u"AutoDealer"
        ret = wikidata_search(query)
        logging.info(ret)
        assert 0 == len(ret["itemList"])

        query = u"Campsite"
        ret = wikidata_search(query)
        logging.info(ret)
        nodeid = ret["itemList"][0]["identifier"]
        assert nodeid == "Q832778"
        ret = wikidata_get(nodeid)
        lable_zh = ret["entities"][nodeid]["labels"]["zh"]["value"]
        logging.info(lable_zh)
        assert lable_zh == u"露營場"

        query = "birthplace"
        ret = wikidata_search(query, searchtype="property")
        #logging.info(ret)
        nodeid = ret["itemList"][0]["identifier"]
        assert nodeid == "P19"
        ret = wikidata_get(nodeid)
        lable_zh = ret["entities"][nodeid]["labels"]["zh"]["value"]
        logging.info(lable_zh)
        assert lable_zh == u"出生地"




if __name__ == '__main__':
    unittest.main()
