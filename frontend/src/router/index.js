import Vue from 'vue';
import Router from 'vue-router';

import Home from '../pages/Home.vue';
import ConsolidatedTable from '../pages/RegistryConsolidatedTable.vue';
import MainTable from '../pages/RegistryMainTable.vue'
import SubsidiaryTable from '../pages/RegistrySubsidiaryTable.vue'
import Chart from '../pages/Chart.vue';
import Riskappetite from '../pages/Riskappetite.vue';

import Login from '../pages/core/Login.vue';
import Register from '../pages/core/Register.vue';

// SVK 
import RankingMatrix from '../pages/RankingMatrix.vue';
import BlockScheme from '../pages/BlockScheme.vue';
import RiskMatrix from '../pages/RiskMatrix.vue';

Vue.use(Router);

export default new Router({
  mode: "history",
  routes: [
    {
      path: '/home',
      name: 'Home',
      component: Home,
    },
// internal system control
    {
      path: '/isc/ranking_matrix',
      name: 'RankingMatrix',
      component: RankingMatrix,
      meta: {
        breadcrumb: [
          {name : 'СВК'},
          {name: 'Матрица ранжирования'}
        ]
      }
    },
    {
      path: '/isc/block_scheme',
      name: 'BlockScheme',
      component: BlockScheme,
      meta: {
        breadcrumb: [
          {name : 'СВК'},
          {name: 'Блок-схема'}
        ]
      }
    },
    {
      path: '/isc/risk_matrix',
      name: 'RiskMatrix',
      component: RiskMatrix,
      meta: {
        breadcrumb: [
          {name : 'СВК'},
          {name: 'Матрица рисков и контроля'}
        ]
      }
    },
    
// reestr 
    {
      path: '/reestr/table/subsidiary',
      name: 'SubsidiaryTable',
      component: SubsidiaryTable,
      meta: {
        breadcrumb: [
          { name: 'Реестр'},
          { name: 'Таблицы'},
          { name: 'Таблица по филиалам'}
        ]
      }
    },
    {
      path: '/reestr/table/main-table',
      name: 'MainTable',
      component: MainTable,
      meta: {
        breadcrumb: [
          { name: 'Реестр'},
          { name: 'Таблицы'},
          { name: 'Основная таблица'}
        ]
      }
    },   
    {
      path: '/reestr/table/subsidiary',
      name: 'ConsolidatedTable',
      component: ConsolidatedTable,
      meta: {
        breadcrumb: [
          { name: 'Реестр'},
          { name: 'Таблицы'},
          { name: 'Консолидированная таблица'}
        ]
      }
    },
    {
      path: '/reestr/chart',
      name: 'Chart',
      component: Chart,
      meta: {
        breadcrumb: [
          { name: 'Реестр'},
          { name: 'Графики' }
        ]
      }
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
      meta: {
        allowAnonymous: true
      }
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: {
        allowAnonymous: true
      }
    },
    {
      path: '/riskappetite',
      name: 'Riskappetite',
      component: Riskappetite,
      meta: {
        breadcrumb: [
          { name: 'Риск-аппетит'}
        ],
      }
    },
    
  ]
});
