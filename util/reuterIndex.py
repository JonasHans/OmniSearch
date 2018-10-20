from bs4 import BeautifulSoup,SoupStrainer
import glob, os, time, json, sys

DATA_PATH = '../data'

def indexReuters():
	# Get all .sgm files
	os.chdir(DATA_PATH)

	# create the json file
	jsonFile = open("../JSON/reuters.json", "w")

	for sgmFile in glob.glob("*.sgm"):
		startTime = time.time()

		# Open file
		reuterFile= open(sgmFile, 'r')
		try:
			reuterData= reuterFile.read()

			# Format reuters data using BeautifulSoup
			formattedReuter = BeautifulSoup(reuterData, features='lxml')

			# Get all docs in the reuters
			allDocs = formattedReuter.find_all('reuters')
			for doc in allDocs:
				# Guaranteed tags
				payload = {
					"topic_flag": doc["topics"],
					"lewis_split": doc["lewissplit"],
					"cgi_split": doc["cgisplit"],
					"old_id": doc["oldid"],
					"new_id": doc["newid"],
					"date": doc.date.get_text().lstrip(), # remove leading spaces
					"topics": doc.topics.get_text(),
					"places": doc.places.get_text(),
					"people": doc.people.get_text(),
					"orgs": doc.orgs.get_text(),
					"exchanges": doc.exchanges.get_text(),
					"entire_text": doc.find("text").get_text() # Text is build in function so find is needed
				}

				# Optional Tags
				if doc.find('text').title:
					payload['title'] = doc.find('text').title.get_text()
				if doc.find('text').dateline:
					payload['date_line'] = doc.find('text').dateline.get_text(),
				if doc.find('text').body:
					payload['body'] = doc.find('text').body.get_text(),

				# Write created json to file
				jsonFile.write(json.dumps(payload)+'\n')

		except:
			print("File did not read")

		# Print passed time
		print("File: "+sgmFile+", time to read: "+str(time.time()-startTime))

if __name__ == "__main__":
    indexReuters()
