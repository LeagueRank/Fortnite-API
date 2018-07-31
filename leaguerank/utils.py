import json
from urllib import urlencode
import urllib2
from datetime import datetime
import sys

from settings import DEBUG


def getJSON(url, headers={}, params={}):
    if params is None:
        params = {}
    params = urlencode(params)
    if url.find('?') > 0 and len(params):
        url = url + '&' + params
    elif len(params):
        url = url + '?' + params
    try:
        request = urllib2.Request(
            url,
            headers=headers)
        response = urllib2.urlopen(request)
        return json.load(response)
    except urllib2.HTTPError, e:
        if DEBUG:
            print >> sys.stderr, url
            print >> sys.stderr, params
            print >> sys.stderr, headers
            print >> sys.stderr, e.read()
        raise e


def postJSON(url, headers={}, data={}):
    if data is None:
        data = {}
    try:
        request = urllib2.Request(url, headers=headers, data=urlencode(data))
        response = urllib2.urlopen(request)
        return json.load(response)
    except urllib2.HTTPError, e:
        if DEBUG:
            print >> sys.stderr, url
            print >> sys.stderr, data
            print >> sys.stderr, headers
            print >> sys.stderr, e.read()
        raise e


def convert_iso_time(isotime):
    """Will convert an isotime (string) to datetime.datetime"""
    return datetime.strptime(isotime, '%Y-%m-%dT%H:%M:%S.%fZ')
