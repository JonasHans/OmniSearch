<template>
    <div>
        <b-card no-body>
            <b-card-header v-on:click="toggleOpen">
				{{name}}
                <!-- <b-button v-on:click="toggleOpen">{{ name }}</b-button> -->
                <!--<b-button :v-b-toggle="'\'' + name +'\''">{{ name }}</b-button>-->
            </b-card-header>
            <b-collapse v-bind:visible="open" id="Topic" accordeon="accordeon1">
                <b-card-header>
                    <b-list-group>
                        <b-list-group-item
                                href="#"
                                v-for="cat in categories"
                                v-bind:key="cat.key"
                                v-bind:active="isSelected(cat.key)"
                                v-on:click="$emit('select', selectedCategories, cat.key)"
                        >
                            {{ cat.key }}
                            <b-badge>{{ cat.doc_count }}</b-badge>
                        </b-list-group-item>
                    </b-list-group>
                </b-card-header>
            </b-collapse>
        </b-card>
    </div>

</template>

<script>
    export default {
        name: "Facet",
        props: {
            name: String,
            categories: Array,
            selectedCategories: Array
        },
        data: function () {
            return {
                open: false
            }
        },
        methods: {
            isSelected: function (key) {
                return this.selectedCategories.includes(key)
            },
            toggleOpen: function () {
                this.open = !this.open
            }
        }
    }
</script>

<style scoped>

</style>
