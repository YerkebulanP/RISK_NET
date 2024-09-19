<template>
    <v-card style="max-width: 155%;">
      <v-toolbar flat>
        <v-toolbar-title>
            Матрица 
        </v-toolbar-title>

        <v-spacer></v-spacer>
     
        <!-- <v-btn small icon @click="editItem(isc)" class="icon-button"><v-icon>mdi-pencil</v-icon></v-btn> -->
  
        <vue-json-to-csv
          :json-data="isc"
          :csv-title="'Матрица ранжирования'"
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
  
   
  
        <v-btn @click="openAddDialog">Добавить новый бизнес процесс</v-btn>
  
      </v-toolbar>
  
      <v-data-table   
         class="table"
        :headers="headers"
        :items="isc"
        :search="search"
        :rows-per-page-items="[5, 10, 20, 50, 100, 200, 1000]">
  
  
      <template v-slot:items="{ item }">
            <td>{{ item.owner }}</td>
            <td>{{ item.business_process_1_name }}</td>
            <td>{{ item.business_process_2_name }}</td>
            <td>{{ item.effect_econ }}</td>
            <td>{{ item.effect_operational }}</td>
            <td>{{ item.effect_law }}</td>
            <td>{{ item.assessment }}</td>
            <td>{{ item.average_assessment }}</td>
            <td>{{ item.notes }}</td>
  
  
                  
          <td><v-btn small icon @click="openDeleteDialog(item)"><v-icon>mdi-delete</v-icon></v-btn></td>
          <td><v-btn small icon @click="editItem(isc)" class="icon-button"><v-icon>mdi-pencil</v-icon></v-btn></td>
        </template>
    </v-data-table>

    
        
    <v-dialog v-model="bp_dialog" max-width="600px">
      <v-card>
        <v-card-title style="text-align: center"><span>{{ formTitle }}</span></v-card-title>
        
        <v-card-text>
          <v-select
            v-model="editedItem.business_process_1_name" 
            :items="BusinessProcess1" 
            label="Выберите бизнесс-процесс 1-го уровня" required 
            class="mb-5"
            item-text="business_process_1_name" 
            @change="handleBusinessProcess1Select"
          ></v-select>

          <v-row v-if="!showBusinessProcess1Input && editedItem.business_process_1_name"> 
            <div style="text-align: center;">Бизнес процесс 2-го уровня</div>
              <v-text-field v-if="editedItem.business_process_1_name" v-model="editedItem.business_process_2_name" label="Наименование бизнес-процесса 2-го уровня" required></v-text-field>
              <v-text>Влияние бизнес-процесса 2-го уровня на подготовку достоверной внутренней и внешней финансовой и нефинансовой отчетности Компании</v-text>
              <v-slider v-if="editedItem.business_process_1_name" v-model="editedItem.effect_econ" label="" tick-size="2" thumb-label ticks="always" min="0" max="5"></v-slider>
              <v-text>Влияние бизнес-процесса 2-го уровня на повышение эффективности операционной деятельности Компании</v-text>
              <v-slider v-if="editedItem.business_process_1_name" v-model="editedItem.effect_operational" label="" tick-size="2" thumb-label ticks="always" min="0" max="5"></v-slider>
              <v-text>Влияние бизнес-процесса 2-го уровня на соблюдение требований законодательства Республики Казахстан и внутренних документов Компании</v-text>
              <v-slider v-if="editedItem.business_process_1_name" v-model="editedItem.effect_law" label="" tick-size="2" thumb-label ticks="always" min="0" max="5"></v-slider>
              <v-text>Оценка на основании карты рисков</v-text>
              <v-slider v-if="editedItem.business_process_1_name" v-model="editedItem.assessment" label="" tick-size="2" thumb-label ticks="always" min="0" max="5"></v-slider>
              <v-text-field v-if="editedItem.business_process_1_name" v-model="editedItem.notes" label="Примечание" required></v-text-field>
              
              <v-btn @click="closeDialog" class = "ml-auto">Отменить</v-btn>
              <v-btn @click="saveOrUpdate" class = "ml-auto">Сохранить</v-btn>
          </v-row>
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
      bp_dialog: false,
      deleteDialog: false,
      headers: [
        { value: 'owner', text: 'Владелец бизнес-процесса' },
        { value: 'business_process_1_name', text: 'Бизнес-процесс 1-го уровня'}, 
        { value: 'business_process_2_name', text: 'Бизнес-процесс 2-го уровня' },
        { value: 'effect_econ', text: 'Влияние бизнес-процесса 2-го уровня на подготовку достоверной внутренней и внешней финансовой и нефинансовой отчетности Компании' },
        { value: 'effect_operational', text: 'Влияние бизнес-процесса 2-го уровня на повышение эффективности операционной деятельности Компании' },
        { value: 'effect_law', text: 'Влияние бизнес-процесса 2-го уровня на соблюдение требований законодательства Республики Казахстан и внутренних документов Компании' },
        { value: 'assessment', text: 'Оценка на основании карты рисков' },
        { value: 'average_assessment', text: 'Итоговая средневзвешанная оценка бизнес-процесса 2-го уровня' },
        { value: 'notes', text: 'Примечание' },
        { value: 'delete', text: 'Удалить'},
        { value: 'edit', text: 'Изменить'}
     ],
     editedItem: {
        business_process_1_id: '',
        business_process_2_id: '',
        business_process_1_name: '',
        business_process_2_name: '',
        owner: '',
        effect_econ: '',
        effect_law: '',
        effect_operational: '',
        assessment: '',
        notes: ''
     },
     editedItemId: null,
     selectedProcess1: null,
     isc: [],
     showBusinessProcess1Input: false,
     BusinessProcess1: []
    };
  },

  computed: {
    computedISC(){
        return this.search ? this.filteredISC : this.isc;
    },
    formTitle(){
        return this.editedItemId ? 'Добавить новый бизнес-процесс' : 'Добавить новый бизнес-процесс';
    }
  },

methods: {
    async fetchISC() {
        try {
            const response = await axios.get("http://localhost:8000/internal_system_control/business_process_2");
            console.log('API response ISC: ', response.data);
            this.isc = response.data;
        } 
        catch(error){
            console.error("Error fetching internal system control:", error);
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

    handleBusinessProcess1Select() {
        if (this.editedItem.business_process_1_name) {
            this.selectedProcess1 = this.BusinessProcess1.find(bp1 => bp1.business_process_1_name === this.editedItem.business_process_1_name);
            if (this.selectedProcess1) {
                this.editedItem.business_process_1_id = this.selectedProcess1.business_process_1_id;
            }
        }
    },


    async saveOrUpdate(){
        const business2level = {
            business_process_2_name: this.editedItem.business_process_2_name,
            effect_econ: this.editedItem.effect_econ,      
            effect_operational: this.editedItem.effect_operational,
            effect_law: this.editedItem.effect_law,
            assessment: this.editedItem.assessment,
            notes: this.editedItem.notes,
            business_process_1_id: this.selectedProcess1.business_process_1_id
        };
        console.log('Payload:', business2level);

        try {
            const response = await axios.post("http://localhost:8000/internal_system_control/post/business_process_2/", business2level);
            console.log('Business process 2 level response from backend:', response.data);
        }
        catch(error){
            console.error('Error saving data:', error);
        }
    },


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
            business_process_1_id: '',
            business_process_2_id: '',
            business_process_1_name: '',
            business_process_2_name: '',
            owner: '',
            effect_econ: '',
            effect_law: '',
            effect_operational: '',
            assessment: '',
            notes: ''            
        };
        this.bp_dialog = true;
    },

// need to change EDIT , change this.dialog into new dialog for editting

    editItem(isc) {
      this.editedItemId = isc.id;
      this.editedItem = { ...isc };
      this.bp_dialog = true;
    },
    
    openDeleteDialog(item) {
      this.editedItemId = item.id;
      this.deleteDialog = true;
    },

    closeDialog() {
      this.bp_dialog = false;
      this.editedItem = {};
      this.editedItemId = null;
    },

    closeDeleteDialog() {
      this.deleteDialog = false;
      this.editedItemId = null;
    },
},

mounted(){
    this.fetchISC();
    this.fetchBusinessProcess1();
},


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



