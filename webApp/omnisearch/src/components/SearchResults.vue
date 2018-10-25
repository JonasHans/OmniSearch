<template>
	<div id="resultlist">

		<div class="text-left result-list">
				<wordcloud
					:data="wordcloud"
					nameKey="key"
					valueKey="score">
				</wordcloud>
			<div class="card result-card" v-for="result in results" v-bind:key="result._source.new_id">
				<div class="card-header bg-secondary text-white">
					{{result._source.title}}

					<b-button @click="wordCloud" variant='warning' class="button-right">Word cloud</b-button>
				</div>

				<div class="card-body">
					<div v-if="wordCloudVis">
					</div>
					<div v-else>
						{{result}}
					</div>
				</div>

				<div class="card-footer">
					<small class="text-muted">Timestamp: {{result._source.date}}</small>
				</div>
			</div>
		</div>

		<ul>
			<!-- TODO opmaak zoekresultaat, incl andere velden  -->
			<li v-for="result in results" v-bind:key="result._source.new_id">
				<a :href="'http://localhost:9200/reuters/_doc/' + result._source.new_id">
					{{ result._source.title}}
				</a>
			</li>
		</ul>

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
	import wordcloud from 'vue-wordcloud'

	export default {
		name : 'SearchResults',
		props : {
			results : Array,
			categories : Object,
			wordcloud: Array
		},
		components : {
			wordcloud
		},
		data: () => {
			return {
				wordCloudVis : false,
				words: [{
				"name": "Cat",
				"value": 26
				},
				{
				"name": "fish",
				"value": 19
				},
				{
				"name": "things",
				"value": 18
				},
				{
				"name": "look",
				"value": 16
				},
				{
				"name": "two",
				"value": 15
				},
				{
				"name": "fun",
				"value": 9
				},
				{
				"name": "know",
				"value": 9
				},
				{
				"name": "good",
				"value": 9
				},
				{
				"name": "play",
				"value": 6
				}
				]
			}
		},
		methods : {
			wordCloud: function() {
				this.wordCloudVis = !this.wordCloudVis
			}
		}
	}
</script>

<style>
.result-card {
	margin-bottom: 25px;
}
.result-list {
	padding: 25px;
}
.button-right {
	float: right;
}
</style>
