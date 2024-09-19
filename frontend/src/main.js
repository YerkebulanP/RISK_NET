import Vue from 'vue';
import Vuex from 'vuex'
import Vuetify from 'vuetify';
import VueChartkick from 'vue-chartkick';
import VueJsonToCsv from 'vue-json-to-csv';
import App from './App';
import axios from 'axios'
import router from './router';
import Chart from 'chart.js';


import swatches from 'vue-swatches';
import { setupComponents } from './config/setup-components';

import 'vuetify/dist/vuetify.min.css';
import "vue-swatches/dist/vue-swatches.min.css"
import 'font-awesome/css/font-awesome.css';
import '@mdi/font/css/materialdesignicons.min.css';
import 'material-design-icons-iconfont/dist/material-design-icons.css';
import './styles/global.css';


Vue.prototype.$axios = axios;
const token = localStorage.getItem('token');
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

Vue.use(VueChartkick, { adapter: Chart });
Vue.use(Vuetify);
Vue.use(Vuex)
Vue.component('swatches', swatches);
Vue.component('vue-json-to-csv', VueJsonToCsv);

setupComponents(Vue);

Vue.config.productionTip = false

const vuetify = new Vuetify({
  theme: {
    primary: "#1D2939"
  }
})
new Vue({
  // el: '#app',
  router,
  // components: { App },
  template: '<App/>',
  vuetify,
  render: h => h(App),
}).$mount('#app');
