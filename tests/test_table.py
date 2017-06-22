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

from cdata.core import file2abspath  # noqa
from cdata.table import *  # noqa


class TableTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_excel2json(self):
        filename = "ex2.xls"
        filename = file2abspath(filename, __file__)

        if not os.path.exists(filename):
            # init_excel():
            input_data = [{
                "name": u"张三",
                u"年龄": 18
            },
                {
                "name": u"李四",
                "notes": u"this is li si",
                u"年龄": 18
            }]
            json2excel(input_data, ["name", u"年龄", "notes"], filename)

        output_data = excel2json(filename)
        assert len(output_data) == 2
        assert len(output_data["data"]) == 1
        assert len(output_data["data"].values()[0]) == 2
        assert output_data["fields"].values()[0] == ["name", u"年龄", "notes"]


if __name__ == '__main__':
    unittest.main()
