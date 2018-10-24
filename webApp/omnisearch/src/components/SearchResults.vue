<template>
	<div id="resultlist">
		<div class="text-left result-list">
			<b-card class="result-card" v-for="result in results" v-bind:key="result._source.new_id"
				:header="result._source.title"
				border-variant="secondary"
	            header-bg-variant="secondary"
	            header-text-variant="white">

			<p class="card-text">
			{{result}}
			</p>

			<div slot="footer">
				<small class="text-muted">Timestamp: {{result._source.date}}</small>
			</div>
			</b-card>
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
	export default {
		name : 'SearchResults',
		props : {
			results : Array,
			categories : Object
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
</style>
