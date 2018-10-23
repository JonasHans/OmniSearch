<template>
    <div class="hello">

        <!-- TODO als we eerst advanced search maken met alle features stiften we deze daarna door naar de simpele versie-->
        <!--<div id="basic">-->
        <!--<div>-->
        <!--<input v-model="query"/>-->
        <!--<button v-on:click="basicSearch">Search</button>-->
        <!--</div>-->
        <!--</div>-->
        <div id="advanced">
            title:
            <input v-model="advancedQuery.title" aria-label="Title"/><br/>
            body:
            <input v-model="advancedQuery.body" aria-label="Body"/>
            <input v-model="advancedQuery.from" aria-label="Body"/>
            <input v-model="advancedQuery.to" aria-label="Body"/>
            <!--TODO date pickers from/to-->
            <button v-on:click="advancedSearch">Search</button>

        </div>
        <div id="resultlist">
            <ul>
                <!-- TODO opmaak zoekresultaat, incl andere velden  -->
                <li v-for="result in resultList" v-bind:key="result._source.new_id">
                    <a :href="'http://localhost:9200/reuters/_doc/' + result._source.new_id">
                        {{ result._source.title}}
                    </a>
                </li>
            </ul>
        </div>


        <div id="topiclist">
            <ul>
                <li v-for="topic in categories.topics" v-bind:key="topic.key">
                        {{ topic.key}} {{topic.doc_count}}
                </li>
            </ul>
        </div>
    </div>


</template>

<script>
    var esb = require('elastic-builder')
    var elasticsearch = require('elasticsearch')
    var client = new elasticsearch.Client({
        host: 'localhost:9200',
        log: 'trace'
    })

    export default {
        name: 'HelloWorld',
        props: {
            msg: String
        },
        data: () => {
            return {
                resultList: null,
                query: 'oil',
                advancedQuery: {
                    title: null,
                    body: null,
                    // Deze default waarden komen overeen met dataset
                    from: "01-01-1987",
                    to: "31-12-1987"
                    // Lijsten om categorie

                },
                categories: {
                    exchanges: [],
                    orgs: [],
                    people: [],
                    places: [],
                    topics: []
                },
                selectedCategories: {
                    exchanges: [],
                    orgs: [],
                    people: [],
                    places: [],
                    topics: []
                }
            }
        },
        methods: {
            basicSearch: function () {
                client.search({
                    index: 'reuters',
                    q: this.query
                }).then((body) => {
                    this.resultList = body.hits.hits
                })
            },

            advancedSearch: function () {

                // Bool query kun je andere queries mee combineren: must, should, filter, must-not
                let boolQuery = esb.boolQuery()

                //
                if (this.advancedQuery.title) {
                    boolQuery.should(esb.matchQuery('title', this.advancedQuery.title))
                }
                if (this.advancedQuery.body) {
                    boolQuery.should(esb.matchQuery('entire_text', this.advancedQuery.body))
                }

                // Door dd-MM-yyyy aan de mapping toe te voegen kunnen we door zulke string range queries op datum doen
                if (this.advancedQuery.from || this.advancedQuery.to) {
                    let range = esb.rangeQuery('date')

                    if (this.advancedQuery.from) {
                        range.gt(this.advancedQuery.from)
                    }
                    if (this.advancedQuery.to) {
                        range.lte(this.advancedQuery.to)
                    }
                    boolQuery.filter(range)
                }

                // Histogram aggregatie
                const dateHistoAgg = esb.dateHistogramAggregation("hitsByDay").field("date").interval("day")

                // Hier aggregeren we alle categorie termen van de resultaten van de query
                const topicsAgg = esb.termsAggregation("topicsAgg", "topics").size(20)
                // const exchangesAgg = esb.termsAggregation("exchangesAgg", "exchanges").size(1000)
                // const orgsAgg = esb.termsAggregation("orgsAgg", "orgs").size(1000)
                // const peopleAgg = esb.termsAggregation("peopleAgg", "people").size(1000)
                // const placesAgg = esb.termsAggregation("placesAgg", "places").size(1000)


                // Container object voor alle aggregaties
                // const aggs = esb.aggregations(dateHistoAgg, topicsAgg, exchangesAgg, orgsAgg, peopleAgg, placesAgg)


                // TODO wordcloud aggregatie
                // Wordcloud -> https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-significanttext-aggregation.html ???

                const requestBody = esb.requestBodySearch()
                    .query(boolQuery)
                    .aggregation(dateHistoAgg)
                    .aggregation(topicsAgg)
                    // .aggregation(exchangesAgg)
                    // .aggregation(orgsAgg)
                    // .aggregation(peopleAgg)
                    // .aggregation(placesAgg)
                    // zo kan je pagineren
                    .size(10)
                    .from(0)

                client.search({
                    index: 'reuters',
                    body: requestBody.toJSON()
                }).then((body) => {
                    this.resultList = body.hits.hits
                    this.categories.topics = []
                    this.categories.topics = body.aggregations.topicsAgg.buckets


                })

            }
        },
        created: function () {
            // this.basicSearch()
            // this.advancedSearch()
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
