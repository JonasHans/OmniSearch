from bs4 import BeautifulSoup
import glob
import os
import time
import requests
import json

DEBUG = False
DATA_PATH = '../data'
INDEX_NAME = 'reuters'
BULK_URL = 'http://localhost:9200/_bulk'
BASE_URL = 'http://localhost:9200/' + INDEX_NAME + '/_doc'
BULK_HEADER = {'content-type': 'application/x-ndjson'}
HEADER = {'content-type': 'application/json'}
BULK_INDEX_COMMAND = "{\"index\" : {\"_index\": \"" + \
                     INDEX_NAME + "\", \"_type\": \"_doc\"}}\n"

EXCHANGES_FILE = 'all-exchanges-strings.lc.txt'
ORGS_FILE = 'all-orgs-strings.lc.txt'
PEOPLE_FILE = 'all-people-strings.lc.txt'
PLACES_FILE = 'all-places-strings.lc.txt'
TOPICS_FILE = 'all-topics-strings.lc.txt'


# Returns list of new line seperated strings from file
def _get_cats_from_file(filename):
    with open(DATA_PATH + '/' + filename) as f:
        return f.read().splitlines(keepends=False)


# Returns list of strings in list if string as substring in file
def _parse_cats_to_list(list, text):
    return [s for s in list if s in text]


def indexReuters():
    # Get all .sgm files
    os.chdir(DATA_PATH)
    totalTimeStart = time.time()
    totalDocuments = 0

    print("Indexing documents...")

    # Load categories from files
    exchanges_list = _get_cats_from_file(EXCHANGES_FILE)
    org_list = _get_cats_from_file(ORGS_FILE)
    people_list = _get_cats_from_file(PEOPLE_FILE)
    places_list = _get_cats_from_file(PLACES_FILE)
    topics_list = _get_cats_from_file(TOPICS_FILE)

    for sgmFile in glob.glob("*.sgm"):
        startTime = time.time()

        # Open file
        reuterFile = open(sgmFile, 'r', encoding="utf8", errors='ignore')
        reuterData = reuterFile.read()

        # Format reuters data using BeautifulSoup
        formattedReuter = BeautifulSoup(reuterData, features='lxml')

        # Get all docs in the reuters
        allDocs = formattedReuter.find_all('reuters')
        bulkPayloadList = list()
        for i, doc in enumerate(allDocs):
            # Guaranteed tags
            document = {
                "topic_flag": doc["topics"],
                "lewis_split": doc["lewissplit"],
                "cgi_split": doc["cgisplit"],
                "old_id": doc["oldid"],
                "new_id": doc["newid"],
                "date": doc.date.get_text().lstrip(),  # remove leading spaces
                "topics": _parse_cats_to_list(topics_list, doc.topics.get_text()),
                "places": _parse_cats_to_list(places_list, doc.places.get_text()),
                "people": _parse_cats_to_list(people_list, doc.people.get_text()),
                "orgs": _parse_cats_to_list(org_list, doc.orgs.get_text()),
                "exchanges": _parse_cats_to_list(exchanges_list, doc.exchanges.get_text()),
                # Text is build in function so find is needed
                "entire_text": doc.find("text").get_text()
            }

            # Optional Tags
            if doc.find('text').title:
                document['title'] = doc.find('text').title.get_text()
            if doc.find('text').dateline:
                document['date_line'] = doc.find('text').dateline.get_text()
            if doc.find('text').body:
                document['body'] = doc.find('text').body.get_text()

            # TODO: remove dateline and tile from entire text if applicable, use that as body instead

            # Bulk index are in the form of:
            # {index: { <meta data> }}
            # {<source>}
            # Using newline delimited JSON, elasticsearch document id conforms to new_id tag parameter
            bulkPayloadList.append("{\"index\" : {\"_index\": \"" + \
                                   INDEX_NAME + "\", \"_type\": \"_doc\", \"_id\": \"" + document['new_id'] + "\" }}\n")
            bulkPayloadList.append(json.dumps(document) + "\n")

            # every 1000 documents or last document we will perform a bulk update
            if i > 0 and (i % 1000 == 0 or i == (len(allDocs) - 1)):
                totalDocuments += len(bulkPayloadList)

                # Concatenating bulk index commands and documents to single string
                bulkPayload = ''.join(bulkPayloadList)
                response = requests.post(BULK_URL, data=bulkPayload, headers=BULK_HEADER)

                # Error handling in case of failed bulk index
                if response.status_code is not 200:
                    raise Exception('Indexing error', response.content)
                else:
                    if DEBUG:
                        print('succesfully posted, i', i)

                bulkPayloadList.clear()

        # Print passed time
        if DEBUG:
            print("File: " + sgmFile + ", time to read: " + str(time.time() - startTime))

    print(totalDocuments, "documents successfully indexed, total time was", str(time.time() - totalTimeStart),
          "seconds.")


if __name__ == "__main__":
    indexReuters()
