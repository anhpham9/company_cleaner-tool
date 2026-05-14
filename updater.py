import requests
import os

VERSION = "1.0"

def check_update():
    try:
        url = "https://raw.githubusercontent.com/anhpham9/company_cleaner-tool/master/version/version.txt"
        latest = requests.get(url).text.strip()

        return latest != VERSION
    except:
        return False
