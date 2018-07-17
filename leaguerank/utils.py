import json
from urllib import urlencode
import urllib2
from time import strptime


def getJSON(url, headers={}, params={}):
    request = urllib2.Request(
        url + '?' + urlencode(params), 
        headers=headers)
    response = urllib2.urlopen(request)
    return json.load(response)

def postJSON(url, headers={}, data={}):
    if data is None:
        data = {}
    request = urllib2.Request(url, headers=headers, data=data)
    response = urllib2.urlopen(request)
    return json.load(response)

def convert_iso_time(isotime):
    """Will convert an isotime (string) to datetime.datetime"""
    return strptime(isotime, '%Y-%m-%dT%H:%M:%S.%fZ')
