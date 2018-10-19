#!/usr/bin/env python3

import os
import requests

headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
BASE_URL = 'http://localhost:9200/'

# delete existing index
requests.delete(BASE_URL+'reuters')

# read mapping as json
with open('mapping.json', 'r') as f:
    payload = f.read()

# PUT new index with specified mapping
r = requests.put(BASE_URL+'reuters', headers=headers, data=payload)
print(r.content)