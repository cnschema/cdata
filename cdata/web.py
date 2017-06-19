#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Li Ding

# utility stuff

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

####################################
# url data manipulation
def url2domain(url):
    parsed_uri = urlparse.urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    domain = re.sub("^.+@","",domain)
    domain = re.sub(":.+$","",domain)
    return domain
