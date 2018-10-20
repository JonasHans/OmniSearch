import requests, time

BASE_URL = 'http://localhost:9200/reuters/_doc'
HEADER = {'content-type': 'application/json'}

def populateIndex():
	print("Started populating reuters index")
	tic = time.time()

	with open('../JSON/reuters.json', 'rb') as fp:
		line = fp.readline()
		count = 0

		while line:
			if(count > 5000):
				print("Posted 5000 docs")
				count = 0
			# Post the JSON to elastic search
			response = requests.post(BASE_URL, data=line, headers=HEADER)

			count += 1
	print("Finished populating reuters index in : " + str(time.time()-tic))

if __name__ == "__main__":
	populateIndex()
