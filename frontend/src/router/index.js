import Vue from 'vue';
import Router from 'vue-router';

import Home from '../pages/Home.vue';
import Table from '../pages/Table.vue';
import Chart from '../pages/Chart.vue';
import Riskappetite from '../pages/Riskappetite.vue';

import Login from '../pages/core/Login.vue';
import Register from '../pages/core/Register.vue';


Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/home',
      name: 'Home',
      component: Home,
    },
    {
      path: '/table',
      name: 'Table',
      component: Table,
      meta: {
        breadcrumb: [
          { name: 'Реестр'},
          { name: 'Таблицы' }
        ]
      }
    },
  
    {
      path: '/chart',
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
        allowAnonymous: true
      }
    },
    
  ]
});
