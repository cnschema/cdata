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


####################################################
def main_subtask(module_name, method_name_prefixs=["task_"], optional_params={}):
    #  http://stackoverflow.com/questions/3217673/why-use-argparse-rather-than-optparse
    #  As of 2.7, optparse is deprecated, and will hopefully go away in the future
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('method_name', help='')
    for optional_param_key, optional_param_help  in optional_params.items():
        parser.add_argument(optional_param_key, required=False, help= optional_param_help)
        #parser.add_argument('--reset_cache', required=False, help='')
    args = parser.parse_args()

    for prefix in method_name_prefixs:
        if args.method_name.startswith(prefix):
            if prefix == "test_":
                # Remove all handlers associated with the root logger object.
                for handler in logging.root.handlers[:]:
                    logging.root.removeHandler(handler)

                # Reconfigure logging again, this time with a file.
                logging.basicConfig(format='[%(levelname)s][%(asctime)s][%(module)s][%(funcName)s][%(lineno)s] %(message)s', level=logging.DEBUG)

            # http://stackoverflow.com/questions/17734618/dynamic-method-call-in-python-2-7-using-strings-of-method-names
            the_method =  getattr(sys.modules[module_name], args.method_name)
            if the_method:
                the_method(args=vars(args))

                logging.info("done")
                return
            else:
                break

    logging.info("unsupported")


def task_subtask(args):
    print "called task_subtask"

if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname)s][%(asctime)s][%(module)s][%(funcName)s][%(lineno)s] %(message)s', level=logging.INFO)
    logging.getLogger("requests").setLevel(logging.WARNING)

    main_subtask(__name__)


"""
    python misc.py task_subtask

"""
