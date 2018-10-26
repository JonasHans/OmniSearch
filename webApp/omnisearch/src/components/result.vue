<template>
		<div class="card result-card">
			<div class="card-header bg-secondary text-white">
				{{result._source.title}}

				<b-button @click="wordCloud" variant='warning' class="button-right">Word cloud</b-button>
			</div>

			<div class="card-body">
				<div v-if="wordCloudVis">
					<wordcloud
						:data="words"
						nameKey="name"
						valueKey="value">
					</wordcloud>
				</div>
				<div v-else>
					{{summary(result._source.entire_text)}}
				</div>
			</div>

			<div class="card-footer">
				<small class="text-muted">Timestamp: {{result._source.date}}</small>
			</div>
		</div>

</template>
<script>
	import wordcloud from 'vue-wordcloud'

	export default {
		name : 'result',
		props : {
			result : Object
		},
		data: () => {
			return {
				wordCloudVis : false
			}
		},
		computed : {
			words: function() {
				let cloud = []
				let text = this.result._source.entire_text.split(" ")
				let found = false

				for (let t in text) {
					for (let pair in cloud){
						if (cloud[pair].name == text[t]) {
							cloud[pair].value += 1
							found = true
						}
					}

					if(!found) {
						cloud.push({
							'name': text[t],
							'value': 1
						})
					}else {
						found = false
					}
				}

				return cloud
			}
		},
		components : {
			wordcloud
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
<style></style>
