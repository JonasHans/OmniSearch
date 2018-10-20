<template>
    <div class="hello">

        <div>
            <input v-model="query"/>
            <button v-on:click="basicSearch">Search</button>
        </div>
        <ul v-for="result in resultList">
            <li>{{ result._source.title }}</li>
        </ul>

    </div>


</template>

<script>
  var elasticsearch = require('elasticsearch')
  var client = new elasticsearch.Client({
    host: 'localhost:9200',
    log: 'trace'
  })

  export default {
    name: 'HelloWorld',
    props: {
      msg: String
    },
    data: () => {
      return {
        resultList: null,
        query: 'oil'
      }
    },
    methods: {
      basicSearch: function () {
        client.search({
          index: 'reuters',
          q: this.$data.query
        }).then((body) => {
          this.$data.resultList = body.hits.hits
        })
      }
    },
    created: function () {
      this.basicSearch()
    }

  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    h3 {
        margin: 40px 0 0;
    }

    ul {
        list-style-type: none;
        padding: 0;
    }

    li {
        display: inline-block;
        margin: 0 10px;
    }

    a {
        color: #42b983;
    }
</style>
