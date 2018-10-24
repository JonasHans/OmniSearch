#!/usr/bin/env python3

import requests

HEADERS = {'Content-type': 'application/json', 'Accept': 'application/json'}
BASE_URL = 'http://localhost:9200/'
INDEX_NAME = 'reuters'


def main():
    # delete existing index
    requests.delete(BASE_URL + 'reuters')

    # read mapping as json
    with open('mapping.json', 'r') as f:
        payload = f.read()

    # PUT new index with specified mapping
    r = requests.put(BASE_URL + INDEX_NAME, headers=HEADERS, data=payload)

    if r.status_code is not 200:
        raise Exception("Index creation error", r.content)
    # Print response for validation
    print(r.content)


if __name__ == '__main__':
    main()
