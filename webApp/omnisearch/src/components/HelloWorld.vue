<template>
    <div class="hello">

        <div id="basic">
            <div>
                <input v-model="query"/>
                <button v-on:click="basicSearch">Search</button>
            </div>
        </div>
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
            <ul v-for="result in resultList" v-bind:key="result._source.new_id">
                <li><a :href="'http://localhost:9200/reuters/_doc/'
                 + result._source.new_id">{{ result._source.title}}</a></li>
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
                    from: "01-01-1987",
                    to: "31-12-1987"
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
                const agg = esb.dateHistogramAggregation("hitsByDay").field("date").interval("day")
                // Wordcloud -> https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-significanttext-aggregation.html ???

                const requestBody = esb.requestBodySearch().query(
                    boolQuery
                ).aggregation(agg)
                // zo kan je pagineren
                    .size(10).from(0)

                client.search({
                    index: 'reuters',
                    body: requestBody.toJSON()
                }).then((body) => {
                    this.resultList = body.hits.hits
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
    h3 {
        margin: 40px 0 0;
    }

    ul {
        list-style-type: none;
        padding: 0;
    }

    li {
        display: inline-block;
        margin: 0 10px;
    }

    a {
        color: #42b983;
    }
</style>
