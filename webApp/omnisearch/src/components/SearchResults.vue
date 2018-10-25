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
				wordCloudVis : false
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
