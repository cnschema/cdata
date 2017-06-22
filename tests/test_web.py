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

from cdata.web import url2domain  # noqa


class WebTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_url2domain(self):
        the_input = "http://www.sge.com.cn/sjzx/mrhqsj/540603"
        the_output = url2domain(the_input)
        assert the_output == "www.sge.com.cn", the_output


if __name__ == '__main__':
    unittest.main()
