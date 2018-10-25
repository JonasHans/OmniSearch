<template>
	<div id="resultlist">

		<column-chart v-if="histogram.length !== 0" :data="chartData"></column-chart>

		<div class="text-left result-list">
				<wordcloud
					:data="wordcloud"
					nameKey="key"
					valueKey="score">
				</wordcloud>
			<div v-for="result in results" v-bind:key="result._source.new_id">
				<result :result="result"></result>
			</div>
		</div>
	</div>
</template>

<script>
	import wordcloud from 'vue-wordcloud'
	import result from './result.vue'

	export default {
		name : 'SearchResults',
		props : {
			results : Array,
			histogram: Array,
			wordcloud: Array
		},
		components : {
			wordcloud,
			result
		},
		computed : {
			chartData: function() {
				let data = {}
				for (let i = 0; i < this.histogram.length; i++) {
					let hitDate = this.histogram[i]['key_as_string'].split(" ")[0]
					let hitCount = this.histogram[i]['doc_count']
					data[hitDate] = hitCount
				}

				return data
			}
		},
		data: () => {
			return {
				wordCloudVis : false,
				words: []
			}
		},
		methods : {
			wordCloud: function() {
				this.wordCloudVis = !this.wordCloudVis
			},
			summary: function(all){
				let text = all.split(" ")
				let sum = ""

				for (let x in text.slice(0, 100)){
					sum += " " + text.slice(0, 100)[x]
				}

				return sum + "..."
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
