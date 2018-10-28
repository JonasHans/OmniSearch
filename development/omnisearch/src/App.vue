<template>
	<div id="app">
		<h1>OmniSearch</h1>
		<img class="image" alt="Omnisearch logo" src="./assets/omni.png">
		<br /><br /><br /><br />
		<OmniSearch></OmniSearch>
	</div>
</template>

<script>
import OmniSearch from './components/OmniSearch.vue'

export default {
  name: 'app',
  components: {
    OmniSearch
  }
}
</script>

<style>

#app {
	font-family: 'Avenir', Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	text-align: center;
	color: #2c3e50;
	margin-top: 60px;
}
 /*
 CSS used from this stackoverflow for rotating image

 https://stackoverflow.com/questions/16771225/css3-rotate-animation
 */
.image {
	mix-blend-mode: multiply;
    width: 250px;
    height: 200px;
    -webkit-animation:spin 4s linear infinite;
    -moz-animation:spin 4s linear infinite;
    animation:spin 4s linear infinite;
}
@-moz-keyframes spin { 100% { -moz-transform: rotate(360deg); } }
@-webkit-keyframes spin { 100% { -webkit-transform: rotate(360deg); } }
@keyframes spin { 100% { -webkit-transform: rotate(360deg); transform:rotate(360deg); } }
</style>
