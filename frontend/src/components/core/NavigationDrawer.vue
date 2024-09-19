
<template>
  <v-navigation-drawer
    v-model="toggle"
    fixed app>
    <v-toolbar flat dark :color="$root.themeColor" class="toolbar">
      <router-link :to="{ name: 'Home' }">
        <img src="/static/ktz_logo.png" width="250px">
      </router-link>

    </v-toolbar>
    <v-list expand>

      <v-list-group>
        <v-list-item slot="activator">
          <v-list-item-action>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><title>table-multiple</title>
            <path d="M7 2H21C22.11 2 23 2.9 23 4V16C23 17.11 22.11 18 21 18H7C5.9 18 5 17.11 5 16V4C5 2.9 5.9 2 7 2M7 6V1
            0H13V6H7M15 6V10H21V6H15M7 12V16H13V12H7M15 12V16H21V12H15M3 20V6H1V20C1 21.11 1.89 22 3 22H19V20H3Z" /></svg>
          </v-list-item-action>

          <v-list-item-title class="item-title">{{ ('Реестр') }}</v-list-item-title>
        </v-list-item>

        <v-list-group no-action>
          <v-list-item slot="activator">
            <v-list-item-action>
              <v-icon>table</v-icon>
            </v-list-item-action>
            <v-list-item-title class="item-title">{{ 'Таблица' }}</v-list-item-title>
          </v-list-item>

          <!-- Sub-items under Таблица -->
          <v-list-item @click="changeRoute('SubsidiaryTable', 1)">
            <v-list-item-title :class="[{'active': selectedIndex === 1}, 'item-title']">{{ 'Таблица по филиалам' }}</v-list-item-title>
          </v-list-item>

          <v-list-item @click="changeRoute('MainTable', 2)">
            <v-list-item-title :class="[{'active': selectedIndex === 2}, 'item-title']">{{ 'Основная таблица' }}</v-list-item-title>
          </v-list-item>

          <v-list-item @click="changeRoute('ConsolidatedTable', 3)">
            <v-list-item-title :class="[{'active': selectedIndex === 3}, 'item-title']">{{ 'Консолидированная таблица' }}</v-list-item-title>
          </v-list-item>
        </v-list-group>
       
      <v-list-item @click="changeRoute('Chart', 4)">
          <v-list-item-action>
            <v-icon>bar_chart</v-icon>
          </v-list-item-action>
          <v-list-item-title :class="[{'active': selectedIndex === 4}, 'item-title' ]">{{ ('Графики') }}</v-list-item-title>
        </v-list-item>

    </v-list-group>

      <v-list-item @click="changeRoute('Riskappetite', 5)">
          <v-list-item-action>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><title>trending-down</title>
              <path d="M16,18L18.29,15.71L13.41,10.83L9.41,14.83L2,7.41L3.41,6L9.41,12L13.41,8L19.71,14.29L22,12V18H16Z" /></svg>
          </v-list-item-action>
          <v-list-item-title :class="[{'active': selectedIndex === 5}, 'item-title' ]"> {{ ('Риск-аппетит') }}</v-list-item-title>
      </v-list-item>


    <v-list-group>
      <v-list-item slot="activator">
        <v-list-item-action>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><title>table-multiple</title>
            <path d="M7 2H21C22.11 2 23 2.9 23 4V16C23 17.11 22.11 18 21 18H7C5.9 18 5 17.11 5 16V4C5 2.9 5.9 2 7 2M7 6V1
            0H13V6H7M15 6V10H21V6H15M7 12V16H13V12H7M15 12V16H21V12H15M3 20V6H1V20C1 21.11 1.89 22 3 22H19V20H3Z" /></svg>
          </v-list-item-action>

          <v-list-item-title class="item-title">{{ ('СВК') }}</v-list-item-title>
        </v-list-item>

        <v-list-item @click="changeRoute('RankingMatrix', 6)">
          <v-list-item-action>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><title>matrix</title><path d="M2,2H6V4H4V20H6V22H2V2M20,4H18V2H22V22H18V20H20V4M9,
               5H10V10H11V11H8V10H9V6L8,6.5V5.5L9,5M15,13H16V18H17V19H14V18H15V14L14,14.5V13.5L15,13M9,13C10.1,13 11,14.34 11,16C11,17.66 10.1,19 9,19C7.9,19 7,17.66 7,
               16C7,14.34 7.9,13 9,13M9,14C8.45,14 8,14.9 8,16C8,17.1 8.45,18 9,18C9.55,18 10,17.1 10,16C10,14.9 9.55,14 9,14M15,5C16.1,5
               17,6.34 17,8C17,9.66 16.1,11 15,11C13.9,11 13,9.66 13,8C13,6.34 13.9,5 15,5M15,6C14.45,6 14,6.9 14,8C14,9.1 14.45,10 15,10C15.55,10 16,9.1 16,8C16,
               6.9 15.55,6 15,6Z" /></svg>  
          </v-list-item-action>
          <v-list-item-title :class="[{'active': selectedIndex === 6}, 'item-title' ]">{{ ('Матрица ранжирования') }}</v-list-item-title>
        </v-list-item>

        <v-list-item @click="changeRoute('BlockScheme', 7)">
          <v-list-item-action>
     
          </v-list-item-action>
          <v-list-item-title :class="[{'active': selectedIndex === 7}, 'item-title' ]">{{ ('Блок-схема') }}</v-list-item-title>
        </v-list-item>

        <v-list-item @click="changeRoute('RiskMatrix', 8)">
          <v-list-item-action>
     
         </v-list-item-action>
          <v-list-item-title :class="[{'active': selectedIndex === 8}, 'item-title' ]">{{ ('Матрица рисков и контролей') }}</v-list-item-title>
        </v-list-item>
    </v-list-group>
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
