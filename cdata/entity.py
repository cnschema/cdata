#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Li Ding

# utility stuff

# base packages
import os
import sys
import json
import logging
import codecs
import hashlib
import datetime
import logging
import time
import re
import collections

import jieba
from core import any2unicode, stat
from misc import main_subtask


class SimpleEntity():
    def __init__(self, entity_list):
        """
            [{"@id":"1","name":"张三"},{"@id":"2","name":"李四"}]
            all input text are assumed (or will be converted into) unicode
        """
        # init entity index
        self.entities = collections.defaultdict(list)
        entity_list_unicode = []
        for entity in entity_list:
            entity_list_unicode.append(any2unicode(entity))

        for entity in entity_list_unicode:
            name = entity["name"]
            self.entities[name].append(entity)

        for entity in entity_list_unicode:
            for name in entity.get("alternateName", []):
                self.entities[name].append(entity)

        stat(entity_list_unicode, ["name"])

        # init jieba
        self.tokenizer = jieba.Tokenizer()
        for name in self.entities:
            self.tokenizer.add_word(name)

    def ner(self, sentence):
        # normalize to unicode
        sentence = any2unicode(sentence)

        # split
        segments = self.tokenizer.cut(sentence, HMM=False)

        # generate output
        word_index = 0
        ret = []
        for segment in segments:
            logging.debug(segment)

            matched_entities = self.entities.get(unicode(segment))
            if matched_entities:
                temp = {"text": segment,
                        "index": word_index,
                        "entities": matched_entities}
                ret.append(temp)
            word_index += len(segment)
        return ret

    
    def get_primary_entity(self,sentence_list,threshold=0.24):
        if not sentence_list:
            return []

        #计算各个词在每个句子中出现的频率
        counter_list = []
        for sentence in sentence_list:
            ret = self.ner(sentence)
            if ret:
                counter = collections.defaultdict(float)
                length = len(ret)
                for entity in ret:
                    counter[entity["text"]] += 1
                for name in counter:
                    counter[name] = counter[name]*1.0/length
                counter_list.append(counter)

        #频率相加，归一化处理
        sum_counter = collections.defaultdict(float)
        for counter in counter_list:
            for text in counter:
                sum_counter[text] += counter[text]

        for text in sum_counter:
            sum_counter[text] = sum_counter[text]/len(sentence_list)

        result_entity_list = []
        sorted_counter = sorted(sum_counter.items(),lambda x,y:cmp(y[1],x[1]))   #按照分数从大到小排序
        for text,score in sorted_counter:
            if score>=threshold:
                tmp = {
                    "text":text,
                    "score":score,
                    "entity":self.entities[text]
                }
                result_entity_list.append(tmp)
            else:
                break
        return  result_entity_list


def task_ner_test(args=None):
    entity_list = [{"@id": "1", "name": "张三"}, {"@id": "2", "name": "李四"}]
    ner = SimpleEntity(entity_list)
    sentence = "张三给了李四一个苹果"
    ret = ner.ner(sentence)
    logging.info(json.dumps(ret, ensure_ascii=False, indent=4))

    sentence = "张三丰给了李四一个苹果"
    ret = ner.ner(sentence)
    logging.info(json.dumps(ret, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname)s][%(asctime)s][%(module)s][%(funcName)s][%(lineno)s] %(message)s', level=logging.DEBUG)  # noqa

    main_subtask(__name__)

"""
    python cdata/entity.py task_ner_test
"""
