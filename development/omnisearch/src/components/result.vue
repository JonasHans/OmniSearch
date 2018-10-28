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
				let stopWords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", 'now']
				let cloud = []
				let text = this.result._source.entire_text.split(" ")
				let found = false

				for (let t in text) {

					if (!stopWords.includes(text[t].toLowerCase())){
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
				}

				return cloud.slice(0,15)
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
