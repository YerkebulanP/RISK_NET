<template>
    <v-card style="max-width: 155%;">
      <v-toolbar flat>
        <v-toolbar-title>
            План-график 
        </v-toolbar-title>

        <v-spacer></v-spacer>
     
  
        <vue-json-to-csv
          :json-data="plan_schedule"
          :csv-title="'Календарный план-график работ по разработке и/или актуализации блок-схем, матриц рисков и контролей АО «НК ҚТЖ» на 20__ год'"
          >
          <v-btn small icon class="icon-button">
            <v-icon left>mdi-download</v-icon>
          </v-btn>
        </vue-json-to-csv>
        
        <v-card-title>
  
  
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Поиск"
            single-line
            hide-details
          ></v-text-field>
        </v-card-title>
  
   
  
        <v-btn @click="openAddDialog">Добавить новый план-график</v-btn>
  
      </v-toolbar>
  
      <v-data-table   
         class="table"
        :headers="headers"
        :items="plan_schedule"
        :search="search"
        :rows-per-page-items="[5, 10, 20, 50, 100, 200, 1000]">
  
  
      <template v-slot:items="{ item }">
            <td>{{ item.owner }}</td>
            <td>{{ item.business_process_1_name }}</td>
            <td>{{ item.business_process_2_name }}</td>
            <td>{{ item.block_scheme_update_period_start}} : {{ item.block_scheme_update_period_end }}</td>
            <td>{{ item.control_matrix_update_period_start }} - {{ item.control_matrix_update_period_end }}</td> 
            <td>{{ item.control_procedure_assessment_period_start}} - {{ item.control_procedure_assessment_period_end }}</td>
            
          <td><v-btn small icon @click="openDeleteDialog(item)"><v-icon>mdi-delete</v-icon></v-btn></td>
          <td><v-btn small icon @click="editItem(plan_schedule)" class="icon-button"><v-icon>mdi-pencil</v-icon></v-btn></td>
        </template>
    </v-data-table>

    
        
    <v-dialog v-model="pg_dialog" max-width="600px">
      <v-card>
        <v-card-title style="text-align: center"><span>{{ formTitle }}</span></v-card-title>
        
        <v-card-text>
          <v-select
            v-model="editedItem.business_process_1_id" 
            :items="BusinessProcess1" 
            label="Выберите бизнесс-процесс 1-го уровня" required 
            class="mb-5"
            item-text="business_process_1_name" 
            item-value = "business_process_1_id"
          ></v-select>

          <v-select
            v-if="editedItem.business_process_1_id"
            v-model="editedItem.business_process_2_id" 
            :items="BusinessProcess2" 
            label="Выберите бизнесс-процесс 2-го уровня" required 
            class="mb-5"
            item-text="business_process_2_name" 
            item-value = "business_process_2_id"
            @change="handleBusinessProcess2Select"
          ></v-select>

          <v-text v-if="editedItem.business_process_2_id"> 
            <div style="text-align: center;">Календарный план-график работ по разработке и/или актуализации блок-схем, матриц рисков и контролей АО «НК ҚТЖ»</div>


      <v-expansion-panels multiple>
        <v-expansion-panel>
          <v-expansion-panel-content>
            <div slot="header">Период разработки и/или актуализации блок-схем</div>
                <v-text-field
                  v-model="editedItem.block_scheme_update_period_start"
                  label="Начало"
                  prepend-icon="mdi-calendar"
                  @click = "openStartDateMenu('block_scheme')"
                ></v-text-field>
                <v-menu
                  v-model="menus.block_scheme_start"
                  :close-on-content-click="false"
                  transition="scale-transition"
                  offset-y
                  min-width="290px"
                >
                  <v-date-picker
                    v-model="editedItem.block_scheme_update_period_start"
                    @input="menus.block_scheme_start = false"
                  ></v-date-picker>
                </v-menu>

                <v-text-field
                  v-model="editedItem.block_scheme_update_period_end"
                  label="Конец"
                  prepend-icon="mdi-calendar"
                  @click ="openEndDateMenu('block_scheme')"
                  readonly
                ></v-text-field>
                <v-menu
                  v-model="menus.block_scheme_end"
                  :close-on-content-click="false"
                  transition="scale-transition"
                  offset-y
                  min-width="290px"
                >
                  <v-date-picker
                    v-model="editedItem.block_scheme_update_period_end"
                    @input="menus.block_scheme_end = false"
                  ></v-date-picker>
                </v-menu>

          </v-expansion-panel-content>
        </v-expansion-panel>

        <v-expansion-panel>
          <v-expansion-panel-content>
            <div slot="header">Период разработки и/или актуализации матриц рисков и контролей</div>
            <v-card>
            </v-card>
                <v-text-field
                  v-model="editedItem.control_matrix_update_period_start"
                  label="Начало"
                  prepend-icon="mdi-calendar"
                  @click ="openStartDateMenu('control_matrix')"
                  readonly
                ></v-text-field>
                <v-menu
                  v-model="menus.control_matrix_start"
                  :close-on-content-click="false"
                  transition="scale-transition"
                  offset-y
                  min-width="290px"
                >
                  <v-date-picker
                    v-model="editedItem.control_matrix_update_period_start"
                    @input="menus.control_matrix_start = false"
                  ></v-date-picker>
                </v-menu>

                <v-text-field
                  v-model="editedItem.control_matrix_update_period_end"
                  label="Конец"
                  prepend-icon="mdi-calendar"
                  @click ="openEndDateMenu('control_matrix')"
                  readonly
                ></v-text-field>
                <v-menu
                  v-model="menus.control_matrix_end"
                  :close-on-content-click="false"
                  transition="scale-transition"
                  offset-y
                  min-width="290px"
                >
                  <v-date-picker
                    v-model="editedItem.control_matrix_update_period_end"
                    @input="menus.control_matrix_end = false"
                  ></v-date-picker>
                </v-menu>

          </v-expansion-panel-content>
        </v-expansion-panel>

        <v-expansion-panel>
          
          <v-expansion-panel-content>
            <div slot="header">Период оценки эффективности дизайна контрольных процедур</div>
                <v-text-field
                      v-model="editedItem.control_procedure_assessment_period_start"
                      label="Начало"
                      prepend-icon="mdi-calendar"
                      @click ="openStartDateMenu('control_procedure')"
                      readonly
                ></v-text-field>
                <v-menu
                  v-model="menus.control_procedure_start"
                  :close-on-content-click="false"
                  transition="scale-transition"
                  offset-y
                  min-width="290px"
                >
                  <v-date-picker
                    v-model="editedItem.control_procedure_assessment_period_start"
                    @input="menus.control_procedure_start = false"
                  ></v-date-picker>
                </v-menu>

                <v-text-field
                  v-model="editedItem.control_procedure_assessment_period_end"
                  label="Конец"
                  prepend-icon="mdi-calendar"
                  @click="openEndDateMenu('control_procedure')"
                  readonly
                ></v-text-field>
                <v-menu
                  v-model="menus.control_procedure_end"
                  :close-on-content-click="false"
                  transition="scale-transition"
                  offset-y
                  min-width="290px"
                >
                  <v-date-picker
                    v-model="editedItem.control_procedure_assessment_period_end"
                    @input="menus.control_procedure_end = false"
                  ></v-date-picker>
                </v-menu>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
             
            <v-card-actions>
              <v-btn @click="closeDialog" class = "ml-auto">Отменить</v-btn>
              <v-btn @click="saveOrUpdate" class = "ml-auto">Сохранить</v-btn>
            </v-card-actions>
          </v-text>
        </v-card-text>

        <v-dialog v-model="deleteDialog" max-width="500px">
            <v-card>
                <v-card-title class="text-xs-title">Вы уверены что хотите удалить данную строку?</v-card-title>
                <v-card-actions><v-spacer></v-spacer>
                <v-btn color="blue-darken-1" variant="text" @click="closeDeleteDialog">Отменить</v-btn>
                <v-btn color="blue-darken-1" variant="text" @click="deleteItemConfirm">Удалить</v-btn>
                <v-spacer></v-spacer>
                </v-card-actions>
            </v-card>
        </v-dialog>

      </v-card>
    </v-dialog>
   </v-card>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      search: '',
      pg_dialog: false,
      deleteDialog: false,
      headers: [
        { value: 'owner', text: 'Владелец бизнес-процесса' },
        { value: 'business_process_1_name', text: 'Бизнес-процесс 1-го уровня'}, 
        { value: 'business_process_2_name', text: 'Бизнес-процесс 2-го уровня' },
        { value: 'block_scheme_update_period', text: 'Период разработки и/или актуализации блок-схем' },
        { value: 'control_matrix_update_period', text: 'Период разработки и/или актуализации матриц рисков и контролей' },
        { value: 'control_procedure_assessment_period', text: 'Период оценки эффективности дизайна контрольных процедур' },
        { value: 'delete', text: 'Удалить'},
        { value: 'edit', text: 'Изменить'}
     ],
     editedItem: {
        business_process_1_id: '',
        business_process_2_id: '',
        business_process_1_name: '',
        business_process_2_name: '',
        block_scheme_update_period_start: null,
        block_scheme_update_period_end: null,
        control_matrix_update_period_start: null,
        control_matrix_update_period_end: null,
        control_procedure_assessment_period_start: null,
        control_procedure_assessment_period_end: null,
     },
     menus: {
        block_scheme_start: null,
        block_scheme_end: null,
        control_matrix_start: null,
        control_matrix_end: null,
        control_procedure_start: null,
        control_procedure_end: null,
      },
     editedItemId: null,
     selectedProcess1: null,
     selectedProcess2: null,
     plan_schedule: [],
     showBusinessProcess1Input: false,
     BusinessProcess1: [],
     BusinessProcess2: []
    };
  },

  computed: {
    computed_plan_schedule(){
        return this.search ? this.filtered_plan_schedule : this.plan_schedule;
    },
    formTitle(){
        return this.editedItemId ? 'Добавить новый план-график' : 'Добавить новый план-график';
    }
  },

methods: {

  // Открыть календарь план-графика 
    openStartDateMenu(type) {
        this.$set(this.menus, `${type}_start`, true);
      },
    openEndDateMenu(type) {
        this.$set(this.menus, `${type}_end`, true);
      },
    
  // HANDLES FOR BUSINESS PROCESSESS    
    handleBusinessProcess1Select() {
        if (this.editedItem.business_process_1_id) {
            this.fetchExactBusinessProcess_2(); // Fetch level 2 items based on level 1 selection
        }
    },

    handleBusinessProcess2Select() {
        const selectedLevel2 = this.BusinessProcess2.find(bp2 => bp2.business_process_2_id === this.editedItem.business_process_2_id);
        if (selectedLevel2) {
            this.editedItem.business_process_2_id = selectedLevel2.business_process_2_id;
            console.log('Selected Level 2:', selectedLevel2);
        } else {
            console.error('Selected Business Process 2 not found');
        }
    },

    // Показать в таблице данные с бэкенда план-график
    async fetch_plan_schedule() {
        try {
            const response = await axios.get("http://localhost:8000/internal_system_control/get/plan_schedule/");
            console.log('API response plan_schedule: ', response.data);
            this.plan_schedule = response.data;
        } 
        catch(error){
            console.error("Error fetching plan_schedule:", error);
        }
    },    

    async fetchBusinessProcess1(){
        try {
            const response = await axios.get("http://localhost:8000/internal_system_control/business_process_1/");
            console.log('API response Business Process 1', response.data);
            this.BusinessProcess1 = response.data;
        }
        catch(error){
            console.error("Error fetching Business Process 1:", error);
        }
    },

 
    async fetchExactBusinessProcess_2() {
      try {
            const response = await axios.get(`http://localhost:8000/internal_system_control/business_process_2/${this.editedItem.business_process_1_id}`);
            console.log('API response Business Process 2 Descriptions', response.data);
            this.BusinessProcess2 = response.data;
        } catch (error) {
            console.error("Error fetching Business Process 2:", error);
        }
    },


     // POST METHOD
    async saveOrUpdate(){
        const post_plan_schedule = {
            business_process_1_id: this.editedItem.business_process_1_id,
            business_process_2_id: this.editedItem.business_process_2_id,
            block_scheme_update_period_start: this.editedItem.block_scheme_update_period_start,
            block_scheme_update_period_end: this.editedItem.block_scheme_update_period_end,
            control_matrix_update_period_start: this.editedItem.control_matrix_update_period_start,
            control_matrix_update_period_end: this.editedItem.control_matrix_update_period_end,
            control_procedure_assessment_period_start: this.editedItem.control_procedure_assessment_period_start,
            control_procedure_assessment_period_end: this.editedItem.control_procedure_assessment_period_end,
        };
        console.log('POST data for Plan Schedule:', post_plan_schedule);

        try {
            const response = await axios.post("http://localhost:8000/internal_system_control/post/plan_schedule/", post_plan_schedule);
            console.log('Plan schedule response from backend:', response.data);
        }
        catch(error){
            console.error('Error saving data:', error);
        }
    },

    // DELETE ITEM
    async deleteItemConfirm() {
      try {
        await axios.delete(`http://localhost:8000/reestr/${this.editedItemId}`);
        this.fetchReestr();
        this.closeDeleteDialog();
      } catch (error) {
        console.error("Ошибка при удалении строки:", error);
      }
    },

    openAddDialog() {
        this.editedItem = {
           business_process_2_id: null,
            business_process_2_id: null,
            business_process_1_name: '',
            business_process_2_name: '',
            block_scheme_period: '',
            control_matrix_period: '',
            control_procedure: ''            
        };
        this.pg_dialog = true;
    },

// need to change EDIT , change this.dialog into new dialog for editting

    editItem(plan_schedule) {
      this.editedItemId = plan_schedule.id;
      this.editedItem = { ...plan_schedule };
      this.pg_dialog = true;
    },
    
    openDeleteDialog(item) {
      this.editedItemId = item.id;
      this.deleteDialog = true;
    },

    closeDialog() {
      this.pg_dialog = false;
      this.editedItem = {};
      this.editedItemId = null;
    },

    closeDeleteDialog() {
      this.deleteDialog = false;
      this.editedItemId = null;
    },
},

mounted(){
    this.fetch_plan_schedule();
    this.fetchBusinessProcess1();
    this.fetchExactBusinessProcess_2();

},
watch:{
  'editedItem.business_process_1_id':'handleBusinessProcess1Select'
}

};
</script>

<style>
    .table {
        border-radius: 3px;
        background-clip: border-box;
        border: 1px solid rgba(0, 0, 0, 0.125);
        box-shadow: 1px 1px 1px 1px rgba(0, 0, 0, 0.21);
        background-color: transparent;
    }
    .ml-auto {
        float: right;
    }
    .icon-button{
        padding-top: 15px;
        padding-right: 15px;
    }
</style>



