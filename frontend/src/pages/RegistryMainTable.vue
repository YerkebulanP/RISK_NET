<template>
    <v-container grid-list-xl fluid>
        <v-layout row wrap>
          <v-flex d-flex lg8 sm6 xs12>
            <registry-data-table :tableType = "'main_table'"/>
          </v-flex>
        </v-layout>
      </v-container>
</template>

<script>

export default {
  data () {
    return {
      
    }
  }
}
</script>

<style>

</style>
