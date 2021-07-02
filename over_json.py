#What this does is request data from ow api and returns it as a json dict

import requests
import json
from urllib.request import urlopen, Request

def overjson(region, platform, username):

    url = "https://ow-api.com/v1/stats/{}/{}/{}/complete".format(platform, region, username)
    stats = {}
    
    ow_r = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    with urlopen(ow_r) as page:
        stats = json.loads(page.read().decode())
    
    
    
    
    return stats
