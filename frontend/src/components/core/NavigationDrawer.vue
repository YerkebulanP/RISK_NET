
<template>
  <v-navigation-drawer
    v-model="toggle"
    fixed app>
    <v-toolbar flat dark :color="$root.themeColor" class="toolbar">
      <router-link :to="{ name: 'Home' }">
        <img src="static/ktz_logo.png" width="250px">
      </router-link>

    </v-toolbar>
    <v-list>

      <v-list-group>
        <v-list-tile slot="activator">
          <v-list-tile-action>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><title>table-multiple</title>
            <path d="M7 2H21C22.11 2 23 2.9 23 4V16C23 17.11 22.11 18 21 18H7C5.9 18 5 17.11 5 16V4C5 2.9 5.9 2 7 2M7 6V1
            0H13V6H7M15 6V10H21V6H15M7 12V16H13V12H7M15 12V16H21V12H15M3 20V6H1V20C1 21.11 1.89 22 3 22H19V20H3Z" /></svg>
          </v-list-tile-action>

          <v-list-tile-title class="item-title">{{ ('Реестр') }}</v-list-tile-title>
        </v-list-tile>

        <v-list-tile @click="changeRoute('Table', 4)">
          <v-list-tile-action>
            <v-icon>table</v-icon>
          </v-list-tile-action>
          <v-list-tile-title :class="[{'active': selectedIndex === 4}, 'item-title' ]">{{ ('Таблица') }}</v-list-tile-title>
        </v-list-tile>
        <v-list-tile @click="changeRoute('Chart', 5)">
          <v-list-tile-action>
            <v-icon>bar_chart</v-icon>
          </v-list-tile-action>
          <v-list-tile-title :class="[{'active': selectedIndex === 5}, 'item-title' ]">{{ ('Графики') }}</v-list-tile-title>
        </v-list-tile>

    </v-list-group>

    <v-list-tile @click="changeRoute('Riskappetite', 2)">
        <v-list-tile-action>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><title>trending-down</title>
            <path d="M16,18L18.29,15.71L13.41,10.83L9.41,14.83L2,7.41L3.41,6L9.41,12L13.41,8L19.71,14.29L22,12V18H16Z" /></svg>
        </v-list-tile-action>
        <v-list-tile-title :class="[{'active': selectedIndex === 2}, 'item-title' ]"> {{ ('Риск-аппетит') }}</v-list-tile-title>
    </v-list-tile>

    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
    toggle: {
        type: Boolean,
        required: false,
        default: true
  },

  data() {
    return {
      selectedIndex: 1,
      toggle: true
      
    }
  },

  methods: {
    changeRoute(routeName, selectedIndex) {
      const vm = this;

      vm.selectedIndex = selectedIndex;

      return vm.$router.push({ name: routeName });
    }
  }
}
</script>

<style>
  .toolbar {
    font-weight: bold;
    font-size: 18px;
  }

  .toolbar .text {
    padding-left: 15px;
    color: white;
    text-decoration:none;
  }

  .item-title {
    font-size: 17px;
    font-weight: 500;
  }
  .item-sub-title {
    font-size: 15px;
    font-weight: 500;
  }

  .active {
    font-weight: bold;
  }
  svg {
    width: 27px; 
    height: 27px; 
  }
</style>
