<template>
    <div class="hello">

        <div id="basic">
            <div>
                <input v-model="query"/>
                <button v-on:click="basicSearch">Search</button>
            </div>
        </div>
        <div id="advanced">
            title:
            <input v-model="advancedQuery.title" aria-label="Title"/><br/>
            body:
            <input v-model="advancedQuery.body" aria-label="Body"/>
            <!--TODO date pickers from/to-->
            <!--TODO date pickers from/to-->
            <button v-on:click="advancedSearch">Search</button>

        </div>
        <div id="resultlist">
            <ul v-for="result in resultList">
                <li><a :href="'http://localhost:9200/reuters/_doc/' + result._source.new_id">{{ result._source.title
                    }}</a></li>
            </ul>
        </div>
    </div>


</template>

<script>
  var esb = require('elastic-builder')
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
        query: 'oil',
        advancedQuery: {
          title: null,
          body: null,
          from: null,
          to: null
        }
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
      },

      advancedSearch: () => {
        // Misschien must ipv should? (and/or)
        let query =
          esb.requestBodySearch(esb.query(
            esb.boolQuery().should([
              esb.matchQuery('title', this.$data.advancedQuery.title),
              esb.matchQuery('full_text', this.$data.advancedQuery.body)
            ])))

        client.search({
          index: 'reuters',
          body: query.toJSON()
        }).then((body) => {
            this.data.resultList = body.hits.hits
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
