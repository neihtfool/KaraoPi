from selenium import webdriver
from googleapiclient.discovery import build
import os
import sys
import requests
import html
import urllib

TOKEN = os.environ['YT_TOKEN']

def search(query, max=5):
    youtube = build('youtube', 'v3', developerKey=TOKEN)
    req = youtube.search().list(q=query, part='snippet', maxResults=max, type='video') 
    res = req.execute() # search results
    search_results = res['items']
    return search_results


def get_title(item):
    return html.unescape(item['snippet']['title'])


def get_id(item):
    return item['id']['videoId']


def get_thumbnail_medium(item):
    url = item['snippet']['thumbnails']['default']['url']
    data = urllib.request.urlopen(url).read()
    return data
