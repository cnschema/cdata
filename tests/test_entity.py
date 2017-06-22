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
from cdata.entity import SimpleEntity

class EntityTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_ner_utf8(self):
        entity_list = [{"@id":"1","name":"张三"},{"@id":"2","name":"李四"}]
        ner = SimpleEntity(entity_list)
        sentence = "张三给了李四一个苹果"
        ret = ner.ner(sentence)
        #logging.info(json.dumps(ret, ensure_ascii=False, indent=4))
        assert len(ret) == 2


    def test_ner(self):
        entity_list = [{"@id":"1","name":u"张三"},{"@id":"2","name":u"李四"}]
        ner = SimpleEntity(entity_list)
        sentence = u"张三给了李四一个苹果"
        ret = ner.ner(sentence)
        #logging.info(json.dumps(ret, ensure_ascii=False, indent=4))
        assert len(ret) == 2

        #张三丰 不会识别成 张三 丰
        sentence = u"张三丰给了李四一个苹果"
        ret = ner.ner(sentence)
        #logging.info(json.dumps(ret, ensure_ascii=False, indent=4))
        assert len(ret) == 1


if __name__ == '__main__':
    unittest.main()
