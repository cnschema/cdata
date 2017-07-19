#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Path hack
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from cdata.summary import *  # noqa

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class SummaryTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_misc(self):
        person = {
            "name": u"张三",
            "accomplishment": u"三好学生"
        }
        ret = summarize_entity_person(person)
        assert u"张三，主要成就是三好学生。" == ret

if __name__ == '__main__':
    unittest.main()
