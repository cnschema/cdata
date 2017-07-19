#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:
# summarize a paragraph or an entity into short text description

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

from misc import main_subtask
from core import *


def summarize_paragraph_person(text):
    pass

def summarize_entity_person(person):
    """
        assume person entity using cnschma person vocabulary, http://cnschema.org/Person
    """
    ret = []

    value = person.get("name")
    if not value:
        return False
    ret.append(value)

    value = person.get("accomplishment")
    if value and len(value) < 30:
        ret.append( u"主要成就是{}".format(value) )

    return u"，".join(ret)

def task_summarize_entity_person(args):
    #print "called task_test_summarize_entity_person"
    person = {
        "name": u"张三",
        "accomplishment": u"三好学生"
    }
    ret = summarize_entity_person(person)
    logging.info(ret)

def task_summarize_all_person(args):
    person_list = []
    #TODO load person_list from json

    result_person_list = []
    for person in person_list:
        ret = summarize_entity_person(person)
        if ret:
            person["shortDescription"] = ret
            result_person_list.append(person)

    logging.info( "write to JSON and excel")

if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname)s][%(asctime)s][%(module)s][%(funcName)s][%(lineno)s] %(message)s', level=logging.DEBUG)  # noqa
    logging.getLogger("requests").setLevel(logging.WARNING)

    main_subtask(__name__)

"""
    python cdata/summary.py task_summarize_entity_person
    python cdata/summary.py task_summarize_all_person

"""
