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

from table import *


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

    value = person.get("courtesyName")
    if value:
        ret.append(u'字{}'.format(value[0]))

    value = person.get("alternateName")
    if value:
        #ret.append(u'别名{}'.format(value))
        # Bugged
        pass

    value = person.get("artName")
    if value:
        ret.append(u'号{}'.format(value))

    value = person.get("dynasty")
    if value:
        ret.append(u'{}人'.format(value))

    value = person.get("ancestralHome")
    if value:
        ret.append(u'祖籍{}'.format(value))

    birth_date = person.get("birthDate")
    birth_place = person.get("birthPlace")
    if birth_date and birth_place:
        ret.append(u'{}出生于{}'.format(birth_date, birth_place))
    elif birth_date:
        ret.append(u'{}出生'.format(birth_date))
    elif birth_place:
        ret.append(u'出生于{}'.format(birth_place))

    nationality = person.get("nationality")
    occupation = person.get("occupation")
    if nationality and occupation:
        ret.append(u'{}{}'.format(nationality, occupation))
    elif nationality:
        ret.append(u'{}人'.format(nationality))
    elif occupation:
        ret.append(u'{}'.format(occupation))

    value = person.get("authorOf")
    if value:
        ret.append(u'主要作品有{}'.format(value))

    value = person.get("accomplishment")
    if value and len(value) < 30:
        ret.append( u"主要成就是{}".format(value) )

    ret = u"，".join(ret)
    if ret[-1] != u'。':
        ret += u'。'

    return ret

def task_summarize_entity_person(args):
    #print "called task_test_summarize_entity_person"
    person = {
        "name": u"张三",
        "accomplishment": u"三好学生"
    }
    ret = summarize_entity_person(person)
    logging.info(ret)

def task_summarize_all_person(args):
    path2person = file2abspath('../local/person/person.json')
    person_list = (json.loads(i) for i in file2iter(path2person))

    result_person_list = []
    for person in person_list:
        ret = summarize_entity_person(person)
        if ret:
            person["shortDescription"] = ret
            result_person_list.append(person)

    logging.info( "write to JSON and excel")

    KEYS = [u"@type",u"artName",u"ethnicGroup",u"student",u"courtesyName",u"religion",u"cnProfessionalTitle",u"occupation",u"jobTitle",u"sibling",u"weight",u"nationality",u"birthPlace",u"height",u"alumniOf",u"keywords", u"schoolsOfbuddhism",u"image",u"parent",u"children",u"accomplishment",u"academicDegree",u"dharmaName",u"deathDate",u"academicMajor",u"nobleTitle",u"posthumousName",u"familyName",u"memberOfPoliticalParty",u"award",u"description", u"shortDescription", u"placeOfBurial",u"cnEducationalAttainment",u"alternateName",u"pseudonym",u"templeName",	u"birthDate",u"gender",u"worksFor",u"name",u"dynasty",u"earName",u"ancestralHome",u"birthName",u"studentOf",u"spouse",u"nobleFamily",u"authorOf",u"@id",u"colleague",u"fieldOfWork",u"mother",u"father"]

    json2excel(result_person_list, KEYS, 'person_shortDescription.xls')
    items2file(result_person_list, 'person_shortDescription.json')

if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname)s][%(asctime)s][%(module)s][%(funcName)s][%(lineno)s] %(message)s', level=logging.DEBUG)  # noqa
    logging.getLogger("requests").setLevel(logging.WARNING)

    main_subtask(__name__)

"""
    python cdata/summary.py task_summarize_entity_person
    python cdata/summary.py task_summarize_all_person

"""
