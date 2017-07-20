#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Path hack
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from cdata.core import *  # noqa


class CoreTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_file2abspath(self):
        tin = "test.json"
        tout = file2abspath(tin, __file__)
        logging.info(" {} => {}".format(tin, tout))
        assert tout.endswith(u"tests/" + tin), tout

        tin = "../test.json"
        tout = file2abspath(tin)
        logging.info(" {} => {}".format(tin, tout))
        assert tout.endswith(
            u"cdata/" + os.path.basename(tin)), tout

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

        json_data = {"a": {"b": 1}, "c": ["d"], "e": "f"}
        assert type(json_get(json_data, ["a"])) == dict
        assert json_get(json_data, ["k"]) is None
        assert json_get(json_data, ["k"], 10) == 10
        assert json_get(json_data, ["a", "b"], 10) == 1
        assert json_get(json_data, ["a", "k"], 10) == 10
        assert json_get(json_data, ["c", "d"], 10) is None
        assert json_get(json_data, ["e", "k"], 10) is None
        assert type(json_get(json_data, ["c"])) == list

        json_data = {
            "father": {"name": "john"},
            "birthPlace": "Beijing"
        }

        assert json_get(json_data, ["father", "name"]) == "john"
        assert json_get(json_data, ["father", "image"], default="n/a") == "n/a"
        assert json_get(json_data, ["father", "father"]) is None
        assert json_get(json_data, ["birthPlace"]) == "Beijing"
        assert json_get(
            json_data, ["birthPlace", "name"], default="n/a") is None

    def test_json_get_list(self):

        json_data = {
            "name": "john",
            "birthPlace": ["Beijing"]
        }
        assert json_get_list(json_data, "name") == ["john"]
        assert json_get_list(json_data, "birthPlace") == ["Beijing"]

    def test_json_get_first_item(self):

        json_data = {
            "name": "john",
            "birthPlace": ["Beijing"],
            "interests": []
        }
        assert json_get_first_item(json_data, "name") == "john"
        assert json_get_first_item(json_data, "birthPlace") == "Beijing"
        assert json_get_first_item(json_data, "birthDate") is None
        assert json_get_first_item(json_data, "interests") is None

    def test_any2utf8(self):
        tin = "你好世界"
        tout = any2utf8(tin)
        logging.info(" {} => {}".format(tin, tout))

        tin = u"你好世界"
        tout = any2utf8(tin)
        logging.info((tin, tout))

        tin = "hello world"
        tout = any2utf8(tin)
        logging.info((tin, tout))

        tin = ["hello", "世界"]
        tout = any2utf8(tin)
        logging.info((tin, tout))

        tin = {"hello": u"世界"}
        tout = any2utf8(tin)
        logging.info((tin, tout))

        tin = {"hello": u"世界", "number": 90}
        tout = any2utf8(tin)
        logging.info((tin, tout))

    def test_any2unicode(self):
        tin = "你好世界"
        tout = any2unicode(tin)
        logging.info((tin, tout))

        tin = u"你好世界"
        tout = any2unicode(tin)
        logging.info((tin, tout))

        tin = "hello world"
        tout = any2unicode(tin)
        logging.info((tin, tout))

        tin = ["hello", "世界"]
        tout = any2unicode(tin)
        logging.info((tin, tout))

        tin = {"hello": u"世界"}
        tout = any2unicode(tin)
        logging.info((tin, tout))

    def test_any2sha1(self):
        tin = "你好世界"
        tout = any2sha1(tin)
        assert "dabaa5fe7c47fb21be902480a13013f16a1ab6eb" == tout, tout

        tin = u"你好世界"
        tout = any2sha1(tin)
        assert "dabaa5fe7c47fb21be902480a13013f16a1ab6eb" == tout, tout

        tin = "hello world"
        tout = any2sha1(tin)
        assert "2aae6c35c94fcfb415dbe95f408b9ce91ee846ed" == tout, tout

        tin = ["hello", "world"]
        tout = any2sha1(tin)
        assert "238d2b0d23b6b4fb22934792bec13448d12df3cf" == tout, tout

        tin = {"hello": "world"}
        tout = any2sha1(tin)
        assert "d3b09abe30cfe2edff4ee9e0a141c93bf5b3af87" == tout, tout

    def test_json_dict_copy(self):
        property_list = [
            { "name":"name", "alternateName": ["name","title"]},
            { "name":"birthDate", "alternateName": ["dob","dateOfBirth"] },
            { "name":"description" }
        ]
        json_object = {"dob":"2010-01-01","title":"John","interests":"data","description":"a person"}
        ret = json_dict_copy(json_object, property_list)
        assert json_object["title"] == ret["name"]
        assert json_object["dob"] == ret["birthDate"]
        assert json_object["description"] == ret["description"]
        assert ret.get("interests") is None

if __name__ == '__main__':
    unittest.main()
