#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Li Ding
# JSON data manipulation

#base packages
import os
import sys
import json
import logging
import codecs
import hashlib
import datetime
import logging
import time
import argparse
import urlparse
import re
import collections

# global constants
VERSION = 'v20170619'
CONTEXTS = [os.path.basename(__file__), VERSION ]

####################################
# file path
def file2abspath(filename, this_file=__file__):
    """
        generate absolute path for the given file and base dir
    """
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(this_file)), filename))


####################################
# read from file

def file2json(filename, encoding ='utf-8'):
    """
        save a line
    """
    with codecs.open(filename, "r", encoding=encoding) as f:
        return json.load(f)

def file2iter(filename, encoding='utf-8', comment_prefix="#", skip_empty_line = True):
    """
        json stream parsing or line parsing
    """
    ret = list()
    visited = set()
    with codecs.open(filename,  encoding=encoding) as f:
        for line in f:
            line = line.strip()
            #skip empty line
            if skip_empty_line and len(line)==0:
                continue

            #skip comment line
            if comment_prefix and line.startswith(comment_prefix):
                continue

            yield line


####################################
# write to file

def json2file(data, filename,encoding ='utf-8'):
    """
        write json in canonical json format
    """
    with codecs.open(filename, "w", encoding=encoding) as f:
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)


def lines2file(lines, filename, encoding='utf-8'):
    """
        write json stream, write lines too
    """
    with codecs.open(filename, "w", encoding=encoding) as f:
        for line in lines:
            f.write(line)
            f.write("\n")

def items2file(items, filename,encoding ='utf-8', modifier='w'):
    """
        json array to file, canonical json format
    """
    with codecs.open(filename, modifier, encoding=encoding) as f:
        for item in items:
            f.write(u"{}\n".format(json.dumps(item, ensure_ascii=False, sort_keys=True)))



####################################
# json data access

def json_get(json_object, property_path, default=None):
    """
        get value of the property path from a json object, e.g. person.father.name
        * invalid path return None
        * valid path (the -1 on path is an object), use default
    """
    temp = json_object
    for field in property_path[:-1]:
        if not type(temp) == dict:
            return None
        temp = temp.get(field,{})
    if not type(temp) == dict:
        return None
    return temp.get(property_path[-1], default)


def json_get_list(json_object, p):
    v = json_object.get(p,[])
    if type(v) == list:
        return v
    else:
        return [v]

####################################
# data conversion

def any2utf8(data):
    """
        rewrite json object values (unicode) into utf-8 encoded string
    """
    if type(data) == dict:
        ret = {}
        for k,v in data.items():
            k = any2utf8(k)
            ret[k]= any2utf8(v)
        return ret
    elif type(data) == list:
        return [any2utf8(x) for x in data]
    elif type(data) == unicode:
        return data.encode("utf-8")
    elif type(data) in [str, basestring]:
        return data
    else:
        logging.error("unexpected {} {}".format(type(data), data))
        return data

def any2unicode(data):
    """
        rewrite json object values (assum utf-8) into unicode
    """
    if type(data) == dict:
        ret = {}
        for k,v in data.items():
            k = any2unicode(k)
            ret[k]= any2unicode(v)
        return ret
    elif type(data) == list:
        return [any2unicode(x) for x in data]
    elif type(data) == unicode:
        return data
    elif type(data) in [str, basestring]:
        return data.decode("utf-8")
    else:
        logging.error("unexpected {} {}".format(type(data), data))
        return data

def any2sha1(text):
    """
        convert a string into sha1hash. For json object/array, first convert
        it into canonical json string.
    """
    #canonicalize json object or json array
    if type(text) in [dict, list]:
        text = json.dumps(text, sort_keys=True)

    #assert question as utf8
    if isinstance(text, unicode):
        text = text.encode('utf-8')

    return hashlib.sha1(text).hexdigest()


####################################
# file statistics

def stat(items, unique_fields, value_fields=[], printCounter=True):
    counter = collections.Counter()
    unique_counter = collections.defaultdict(list)

    for item in items:
        counter["all"] +=1
        for field in unique_fields:
            if item.get(field):
                unique_counter[field].append(item[field])
        for field in value_fields:
            value = item.get(field)
            if value:
                counter[u"{}_{}".format(field,value)] +=1

    for field in unique_fields:
        counter[u"{}_unique".format(field)] = len(set(unique_counter[field]))
        counter[u"{}_nonempty".format(field)] = len(unique_counter[field])

    if printCounter:
        logging.info( json.dumps(counter, ensure_ascii=False, indent=4, sort_keys=True) )

    return counter
