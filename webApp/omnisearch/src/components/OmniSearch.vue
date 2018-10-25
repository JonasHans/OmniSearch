<template>
    <b-container fluid>
        <!-- TODO als we eerst advanced search maken met alle features stiften we deze daarna door naar de simpele versie-->

		<b-row class="justify-content-md-center my-1">
			<b-col lg="5">
				<b-form-input v-model="advancedQuery.query" id="query"></b-form-input>
			</b-col>
			<b-button @click="search">Search</b-button>
		</b-row>

		<a href="#" v-b-toggle.accordion1 @click="toggleAccordion">Advanced search</a>

		<b-row class="justify-content-md-center">
			<b-col lg="6">
				<b-collapse id="accordion1" :v-model="accordionVisible" accordion="my-accordion" role="tabpanel">
					<b-card-body>
						<b-row class="justify-content-md-center my-1">
							<b-col lg="3">
								<label for="title">Title</label>
							</b-col>
							<b-col lg="8">
								<b-form-input v-model="advancedQuery.title" id="title"></b-form-input>
							</b-col>
						</b-row>

						<b-row class="justify-content-md-center my-1">
							<b-col lg="3">
								<label for="body">Body</label>
							</b-col>
							<b-col lg="8">
								<b-form-input v-model="advancedQuery.body" id="body"></b-form-input>
							</b-col>
						</b-row>

						<b-row class="justify-content-md-center my-1">
							<b-col lg="3">
								<label for="date-from">Date range</label>
							</b-col>
							<b-col lg="3">
								<b-form-input v-model="advancedQuery.from" id="date-from"></b-form-input>
							</b-col>
							<b-col lg="2">
							-
							</b-col>
							<b-col lg="3">
								<b-form-input v-model="advancedQuery.to" id="date-to"></b-form-input>
							</b-col>
						</b-row>
					</b-card-body>
				</b-collapse>
			</b-col>
		</b-row>

		<SearchResults :categories="categories" :results="resultList"></SearchResults>

    </b-container>


</template>

<script>
	import SearchResults from './../components/SearchResults.vue'

    var esb = require('elastic-builder')
    var elasticsearch = require('elasticsearch')
    var client = new elasticsearch.Client({
        host: 'localhost:9200',
        log: 'trace'
    })

    export default {
        name: 'OmniSearch',
		components: {
			SearchResults
		},
        data: () => {
            return {
                resultList: null,
                query: '',
				accordionVisible : false,
                advancedQuery: {
					query: null,
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
                },
				dateHistory : {}
            }
        },
        methods: {
			search: function () {
				if (this.accordionVisible) {
					this.advancedSearch()
				} else {
					this.basicSearch()
				}
			},

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
                // const exchangesAgg = esb.termsAggregation("exchangesAgg", "exchanges").size(20)
                // const orgsAgg = esb.termsAggregation("orgsAgg", "orgs").size(20)
                // const peopleAgg = esb.termsAggregation("peopleAgg", "people").size(20)
                // const placesAgg = esb.termsAggregation("placesAgg", "places").size(20)

                // TODO wordcloud aggregatie
				const textAgg = esb.significantTextAggregation("wordCloud", "title")
                // Wordcloud -> https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-significanttext-aggregation.html ???

                const requestBody = esb.requestBodySearch()
                    .query(boolQuery)
                    .aggregation(dateHistoAgg)
                    .aggregation(topicsAgg)
					.aggregation(textAgg)
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
					this.dateHistory = body.aggregations.wordCloud.buckets
                })
            },
			toggleAccordion: function(){
				this.accordionVisible = !this.accordionVisible
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
