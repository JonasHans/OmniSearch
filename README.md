# OmniSearch
Search engine using elastic search.

## TODO

- Remove title/dateline from text to create new 'body'
- Use topic aggregation to add filter to advanced query
- Make component to show topic aggregation result list, hooking back in to filter
- Re-use said component for other category information (people, exchanges, etc) <3 vue
- Visualize date histogram for query
- Assemble wordcloud aggregation
- Optional postprocessing of wordcloud result
- Wordcloud visualization
- Spinning logo
- Styling
- Code clean up/refactor

#### Done
- Index mapping
- Index creation script
- Data indexing script using bulk API
- Sanitizing category (keyword) input
- VueJS framework setup
- Basic query (disabled)
- Advanced query (title, body, range(from, to))
- Date histogram api call
- Category aggregation call for faceted search
- Bottle of wine

# Setup

## elasticsearch
Elasticsearch "6.4.2" running on port localhost:9200.

## elasticsearch config
Place elasticsearch.yml in /etc/elasticsearch/ in order to set CORS headers to '*',
for our prototyping purposes.

## dataset
Place entire dataset, including:
- *.sgm
- all-exchanges-strings.lc.txt
- all-orgs-strings.lc.txt
- all-people-strings.lc.txt
- all-places-strings.lc.txt
- all-topics-strings.lc.txt

in ./data/ for indexing to function.

## python
Python 3, bs4 with lxml package.

## Webapp

### installation
NodeJS required, in directory: <br/>
./webApp/omnisearch/<br/>
run:<br/>
node i

### runtime
node run serve

# Reference

## elastic-builder
https://github.com/sudo-suhas/elastic-builder
