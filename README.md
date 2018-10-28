# OmniSearch
OmniSearch is a search engine for the reuters dataset. This was the end project for the UvA course zoekmachines(2018/2019).

## Wiki
Our wiki describes the different facets of the search engine in detail. You can find it [here](/wiki).

## Installation

### Elasticsearch
A version of elastic search is necessary, running on port 9200 localhost. Development for this project was done on version "6.4.2" of elastic search. 

#### Elasticsearch config
Place elasticsearch.yml in /etc/elasticsearch/ in order to set CORS headers to "*".

### Python
Python 3, bs4 with lxml package.

### Webapp
The final production web app can be found in the /build folder. To view the web app it has to be served by an HTTP server (Apache for example). 

## Usage

1. Start your elastic search on port 9200. 
2. Run the /util/create_index.py file to create the reuters index in elastic search. 
```
python3 create_index.py
```
3. Run the /util/reuterIndex.py file to index the data folder.
```
python3 reuterIndex.py
```
4. Serve the webapp in the /build folder by an HTTP server.

## Advanced usage

In the /development the entire vue.js app can be found and run. 

Assuming you have npm and NodeJs installed, you can run the following commands to run the development version.

```
node i
npm install 
npm run sere
```
