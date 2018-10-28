<template>
	<div id="resultlist">
		<div class="text-left result-list">
			<div v-for="result in results" v-bind:key="result._source.new_id">
				<result :result="result"></result>
			</div>
		</div>
	</div>
</template>

<script>
	import result from './result.vue'

	export default {
		name : 'SearchResults',
		props : {
			results : Array
		},
		components : {
			result
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
