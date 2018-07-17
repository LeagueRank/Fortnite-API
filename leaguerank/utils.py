import json
from urllib import urlencode
import urllib2
from datetime import datetime


def getJSON(url, headers={}, params={}):
    if params is None:
        params = {}
    params = urlencode(params)
    if url.find('?') > 0 and len(params):
        url = url + '&' + params
    elif len(params):
        url = url + '?' + params
    request = urllib2.Request(
        url, 
        headers=headers)
    response = urllib2.urlopen(request)
    return json.load(response)

def postJSON(url, headers={}, data={}):
    if data is None:
        data = {}
    request = urllib2.Request(url, headers=headers, data=urlencode(data))
    response = urllib2.urlopen(request)
    return json.load(response)

def convert_iso_time(isotime):
    """Will convert an isotime (string) to datetime.datetime"""
    return datetime.strptime(isotime, '%Y-%m-%dT%H:%M:%S.%fZ')
