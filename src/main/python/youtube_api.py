from selenium import webdriver
from googleapiclient.discovery import build
from youtube_search import YoutubeSearch
import os
import sys
import requests
import html
import urllib

TOKEN = os.environ['YT_TOKEN']

def search(term, max=10):
    results = YoutubeSearch(search_terms=term, max_results=int(max)).to_dict()
    return results


def get_title(item):
    return item['title']


def get_id(item):
    return item['id']


def get_thumbnail(item):
    url = item['thumbnails'][0]
    data = urllib.request.urlopen(url).read()
    return data
