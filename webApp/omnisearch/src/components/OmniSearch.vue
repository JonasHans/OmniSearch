<template>
	<div id="main">
		<img id="main-image" src="./../assets/omni.png">
		<b-input-group>
			<b-form-input v-model="searchInput"
				type="text"
				placeholder="Search reuters...">
			</b-form-input>
			<b-button id="search-button" variant="success">Search</b-button>
		</b-input-group>
	</div>
</template>

<script>
export default {
	name: 'OmniSearch',
	data () {
		return {
			searchInput : ''
		}
	}
}
</script>

<style scoped>
#main {
	width:800px;
	margin:0 auto
}
#main-image {
	margin: 0 auto;
}
#search-button {
	float: right;
}
</style>
