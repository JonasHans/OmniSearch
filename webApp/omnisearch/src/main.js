import Vue from 'vue'
import App from './App.vue'

// Wordcloud component
// Vue.component(VueWordCloud.name, VueWordCloud);

// Bootstrap 4
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
Vue.use(BootstrapVue);

Vue.config.productionTip = false

new Vue({
  render: h => h(App)
}).$mount('#app')
