#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Path hack
import os, sys
sys.path.insert(0, os.path.abspath('..'))

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import cdata
from cdata.core import *


class CoreTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_file2abspath(self):
        the_input = "test.json"
        the_output = file2abspath(the_input, __file__)
        logging.info(" {} => {}".format(the_input, the_output))
        assert the_output.endswith(u"tests/"+the_input), the_output

        the_input = "../test.json"
        the_output = file2abspath(the_input)
        logging.info(" {} => {}".format(the_input, the_output))
        assert the_output.endswith(u"cdata/"+os.path.basename(the_input)), the_output

    def test_file2json(self):
        filename = "ex1.json"
        filename = file2abspath(filename, __file__)
        ret = file2json(filename)
        assert len(ret) == 3

    def test_file2iter(self):
        filename = "ex1.json"
        filename = file2abspath(filename, __file__)
        str_iter = file2iter(filename)
        assert len(list(str_iter)) == 5

    def test_json_get(self):

        json_data = {"a":{"b":1},"c":["d"],"e":"f"}
        assert type(json_get(json_data, ["a"])) == dict
        assert json_get(json_data,["k"]) == None
        assert json_get(json_data,["k"], 10) == 10
        assert json_get(json_data,["a","b"], 10) == 1
        assert json_get(json_data,["a","k"], 10) == 10
        assert json_get(json_data,["c","d"], 10) == None
        assert json_get(json_data,["e","k"], 10) == None
        assert type(json_get(json_data, ["c"])) == list

        json_data = {
            "father": {"name":"john"},
            "birthPlace": "Beijing"
        }

        assert json_get(json_data, ["father","name"]) == "john"
        assert json_get(json_data, ["father","image"],default="n/a") == "n/a"
        assert json_get(json_data, ["father","father"]) == None
        assert json_get(json_data, ["birthPlace"]) == "Beijing"
        assert json_get(json_data, ["birthPlace","name"], default="n/a") == None

    def test_json_get_list(self):

        json_data = {
            "name":"john",
            "birthPlace": ["Beijing"]
        }
        assert json_get_list(json_data, "name") == ["john"]
        assert json_get_list(json_data, "birthPlace") == ["Beijing"]


    def test_any2utf8(self):
        the_input = "你好世界"
        the_output = any2utf8(the_input)
        logging.info(" {} => {}".format(the_input, the_output))

        the_input = u"你好世界"
        the_output = any2utf8(the_input)
        logging.info((the_input, the_output))

        the_input = "hello world"
        the_output = any2utf8(the_input)
        logging.info((the_input, the_output))

        the_input = ["hello", "世界"]
        the_output = any2utf8(the_input)
        logging.info((the_input, the_output))

        the_input = {"hello": u"世界"}
        the_output = any2utf8(the_input)
        logging.info((the_input, the_output))

    def test_any2unicode(self):
        the_input = "你好世界"
        the_output = any2unicode(the_input)
        logging.info((the_input, the_output))

        the_input = u"你好世界"
        the_output = any2unicode(the_input)
        logging.info((the_input, the_output))

        the_input = "hello world"
        the_output = any2unicode(the_input)
        logging.info((the_input, the_output))

        the_input = ["hello", "世界"]
        the_output = any2unicode(the_input)
        logging.info((the_input, the_output))

        the_input = {"hello": u"世界"}
        the_output = any2unicode(the_input)
        logging.info((the_input, the_output))


    def test_any2sha1(self):
        the_input = "你好世界"
        the_output = any2sha1(the_input)
        assert "dabaa5fe7c47fb21be902480a13013f16a1ab6eb" == the_output, the_output

        the_input = u"你好世界"
        the_output = any2sha1(the_input)
        assert "dabaa5fe7c47fb21be902480a13013f16a1ab6eb" == the_output, the_output

        the_input = "hello world"
        the_output = any2sha1(the_input)
        assert "2aae6c35c94fcfb415dbe95f408b9ce91ee846ed" == the_output, the_output

        the_input = ["hello", "world"]
        the_output = any2sha1(the_input)
        assert "238d2b0d23b6b4fb22934792bec13448d12df3cf" == the_output, the_output

        the_input = {"hello": "world"}
        the_output = any2sha1(the_input)
        assert "d3b09abe30cfe2edff4ee9e0a141c93bf5b3af87" == the_output, the_output

if __name__ == '__main__':
    unittest.main()
