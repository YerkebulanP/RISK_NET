
import Toolbar from '../components/core/Toolbar.vue';
import Navigation from '../components/core/NavigationDrawer.vue';
import Breadcrumbs from '../components/core/Breadcrumbs.vue';
import RegistryDataTable from '../components/RegistryDataTable.vue';
import RankingMatrixDataTable from '../components/RankingMatrixDataTable.vue';
import BlockSchemeDataTable from '../components/BlockSchemeDataTable.vue';
import RiskMatrixDataTable from '../components/RiskMatrixDataTable.vue';

function setupComponents(Vue){

  Vue.component('toolbar', Toolbar);
  Vue.component('navigation', Navigation);
  Vue.component('breadcrumbs', Breadcrumbs);
  Vue.component('registry-data-table', RegistryDataTable);
  Vue.component('ranking-matrix-data-table', RankingMatrixDataTable);
  Vue.component('block-scheme-data-table', BlockSchemeDataTable);
  Vue.component('risk-matrix-data-table', RiskMatrixDataTable)

}


export {
  setupComponents
}
