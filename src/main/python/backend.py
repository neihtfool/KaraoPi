import os
import sys
import requests


URL = "https://www.youtube.com/results?search_query="


if __name__ == '__main__':
    obj = requests.get(URL + "540+kick")