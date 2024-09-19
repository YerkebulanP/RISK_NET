<template>
    <v-card style="max-width: 155%;">
      <v-toolbar flat>
        <v-toolbar-title>
            Матрицы рисков и контролей
        </v-toolbar-title>

        <v-spacer></v-spacer>
     
  
        <vue-json-to-csv
          :json-data="risk_matrix"
          :csv-title="'Матриц рисков и контролей АО «НК ҚТЖ» на 20__ год'"
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
  
   
  
        <v-btn @click="openAddDialog">Добавить новую матрицу рисков и контролей</v-btn>
  
      </v-toolbar>
  
      <v-data-table   
         class="table"
        :headers="headers"
        :items="risk_matrix"
        :search="search"
        :rows-per-page-items="[5, 10, 20, 50, 100, 200, 1000]">
  
  
      <template v-slot:items="{ item }">
            <td>{{ item.business_process_1_name }}</td>
            <td>{{ item.owner }}</td>
            <td>{{ item.business_process_2_name }}</td>
            <td>{{ item.step_business_process_2_level }}</td>
            <td>{{ item.step_description }}</td>
            <td>{{ item.step_performer }}</td>
            <td>{{ item.risk_code }}</td>
            <td>{{ item.risk_name }}</td>
            <td>{{ item.risk_description }}</td>
            <td>{{ item.control_procedure_code }}</td>
            <td>{{ item.control_procedure_name }}</td>
            <td>{{ item.control_procedure_owner }}</td>
            <td>{{ item.control_procedure_description }}</td>
            <td>{{ item.control_procedure_inner_outer_document }}</td>
            <td>{{ item.control_procedure_frequency }}</td>
            <td>{{ item.control_procedure_type }}</td>
            <td>{{ item.control_procedure_category }}</td>
            <td>{{ item.effectivity_assessment }}</td>
            <td>{{ item.basis_of_assessment }}</td>

          <td><v-btn small icon @click="openDeleteDialog(item)"><v-icon>mdi-delete</v-icon></v-btn></td>
          <td><v-btn small icon @click="editItem(risk_matrix)" class="icon-button"><v-icon>mdi-pencil</v-icon></v-btn></td>
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
            :items="businessProcess2Level" 
            label="Выберите бизнесс-процесс 2-го уровня" required 
            class="mb-5"
            item-text="business_process_2_name" 
            item-value = "business_process_2_id"
            @change="handleBusinessProcess2Select"
          ></v-select>

          <v-text v-if="editedItem.business_process_2_id"> 
            <!-- <div style="text-align: center;">Календарный план-график работ по разработке и/или актуализации блок-схем, матриц рисков и контролей АО «НК ҚТЖ»</div> -->

            <div style="text-align: center;">Детализация бизнес процесса</div>

              <v-text-field v-model="editedItem.step_business_process_2_level" label="Шаг бизнес процесса 2-го уровня " required></v-text-field> 
              <v-text-field v-model="editedItem.step_description" label="Описание шага" required></v-text-field> 
              <v-text-field v-model="editedItem.step_performer" label="Исполнитель шага" required></v-text-field> 
             
            <div style="text-align: center;">Детализация риска</div>

              <v-text-field v-model="editedItem.risk_code" label="Код риска" required></v-text-field> 
              <v-text-field v-model="editedItem.risk_name" label="Наименование риска" required></v-text-field> 
              <v-text-field v-model="editedItem.risk_description" label="Описание риска" required></v-text-field> 

            <div style="text-align: center;">Детализация контрольной процедуры</div>
              
              <v-text-field v-model="editedItem.control_procedure_code"   label="Код контрольной процедуры" required></v-text-field> 
              <v-text-field v-model="editedItem.control_procedure_name" label="Наименование контрольной процедуры" required></v-text-field> 
              <v-text-field v-model="editedItem.control_procedure_owner" label="Владелец контрольной процедуры" required></v-text-field> 
              <v-text-field v-model="editedItem.control_procedure_description" label="Детальное описание контрольной процедуры" required></v-text-field> 
              <v-text-field v-model="editedItem.control_procedure_inner_outer_document" label="Внутренний и/или внешний регламентирующий документ, на основании которого исполняется контрольная процедура" required></v-text-field> 
              <v-text-field v-model="editedItem.control_procedure_frequency" label="Частота контрольной процедуры" required></v-text-field> 
              <v-text-field v-model="editedItem.control_procedure_type" label="Тип контрольной процедуры" required></v-text-field> 
              <v-text-field v-model="editedItem.control_procedure_category" label="Категория контрольной процедуры" required></v-text-field> 
            
            <div style="text-align: center;">Детализация оценки эффективности дизайна контрольной процедуры</div>
              <v-text-field  v-model="editedItem.effectivity_assessment" label="Оценка эффективности дизайна контрольной процедуры" required></v-text-field> 
              <v-text-field  v-model="editedItem.basis_of_assessment" label="Основание для оценки эффективности контрольной процедуры" required></v-text-field>            
            
            <v-card-actions>
              <v-btn @click="closeDialog" class = "ml-auto">Отменить</v-btn>
              <v-btn @click="saveOrUpdate" class = "ml-auto">Сохранить</v-btn>
            </v-card-actions>
          </v-text>
        </v-card-text>

        <v-dialog v-model="deleteDialog" max-width="500px">
            <v-card>
                <v-card-title class="text-xs-title">Вы уверены что хотите удалить данную строку?</v-card-title>
                    <v-card-actions>
                        <v-spacer></v-spacer>
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
        { value: 'business_process_1_name', text: 'Бизнес-процесс 1-го уровня'}, 
        { value: 'owner', text: 'Владелец бизнес-процесса' },
        { value: 'business_process_2_name', text: 'Бизнес-процесс 2-го уровня' },
        { value: 'step_business_process_2_level', text: 'Шаг бизнес процесса 2-го уровня' },
        { value: 'step_description', text: 'Описание шага' },
        { value: 'step_performer', text: 'Исполнитель шага' },
        { value: 'risk_code', text: 'Код риска' },
        { value: 'risk_name', text: 'Наименование риска '},
        { value: 'risk_description', text: 'Описание риска' },
        { value: 'control_procedure_code', text: 'Код контрольной процедуры' },
        { value: 'control_procedure_name', text: 'Наименование контрольной процедуры' },
        { value: 'control_procedure_owner', text: 'Владелец контрольной процедуры' },
        { value: 'control_procedure_description', text: 'Детальное описание контрольной процедуры' },
        { value: 'control_procedure_inner_outer_document', text: 'Внутренний и/или внешний регламентирующий документ, на основании которого исполняется контрольная процедура' },
        { value: 'control_procedure_frequency', text: 'Частота контрольной процедуры' },
        { value: 'control_procedure_type', text: 'Тип контрольной процедуры' },
        { value: 'control_procedure_category', text: 'Категория контрольной процедуры' },
        { value: 'effectivity_assessment', text: 'Оценка эффективности дизайна контрольной процедуры' },
        { value: 'basis_of_assessment', text: 'Основание для оценки эффективности контрольной процедуры' },

        { value: 'delete', text: 'Удалить'},
        { value: 'edit', text: 'Изменить'}
     ],

     editedItem: {
        business_process_1_id: '',
        business_process_2_id: '',
        business_process_1_name: '',
        business_process_2_name: '',
        step_business_process_2_level: '',
        step_description: '',
        step_performer: '',
        risk_code: '',
        risk_name: '',
        risk_description: '',
        control_procedure_code: '',
        control_procedure_name: '',
        control_procedure_owner: '',
        control_procedure_description: '',
        control_procedure_inner_outer_document: '',
        control_procedure_frequency: '',
        control_procedure_type: '',
        control_procedure_category: '',
        effectivity_assessment: '',
        basis_of_assessment: '',
     },

     editedItemId: null,
     selectedProcess1: null,
     selectedProcess2: null,
     risk_matrix: [],
     showBusinessProcess1Input: false,
     BusinessProcess1: [],
    //  BusinessProcess2: [],
     businessProcess2Level: []
    };
  },

  computed: {
    computed_risk_matrix(){
        return this.search ? this.filtered_risk_matrix : this.risk_matrix;
    },
    formTitle(){
        return this.editedItemId ? 'Добавить новую матрицу рисков' : 'Добавить новую матрицу рисков';
    }
  },

methods: {

    // HANDLES 
    handleBusinessProcess1Select() {
        if (this.editedItem.business_process_1_id) {
            this.fetchExactBusinessProcess_2(); 
        }
    },

    handleBusinessProcess2Select() {
        const selectedLevel2 = this.businessProcess2Level.find(bp2 => bp2.business_process_2_id === this.editedItem.business_process_2_id);
        if (selectedLevel2) {
            this.editedItem.business_process_2_id = selectedLevel2.business_process_2_id;
            console.log('Selected Level 2:', selectedLevel2);
        } else {
            console.error('Selected Business Process 2 not found');
        }
    },
    

    // Показать в таблице данные с бэкенда 
    async fetch_risk_matrix() {
        try {
            const response = await axios.get("http://localhost:8000/internal_system_control/get/risk_matrix/");
            console.log('API response risk_matrix: ', response.data);
            this.risk_matrix = response.data;
        } 
        catch(error){
            console.error("Error fetching risk_matrix:", error);
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

    // async fetchBusinessProcess2(){
    //     try {
    //         const response = await axios.get("http://localhost:8000/internal_system_control/business_process_2/");
    //         console.log('API response Business Process 2', response.data);
    //         this.BusinessProcess2 = response.data;
    //     }
    //     catch(error){
    //         console.error("Error fetching Business Process 2:", error);
    //     }
    // },

    async fetchExactBusinessProcess_2() {
      try {
            const response = await axios.get(`http://localhost:8000/internal_system_control/business_process_2/${this.editedItem.business_process_1_id}`);
            console.log('API response Business Process 2 Descriptions', response.data);
            this.businessProcess2Level = response.data;
        } catch (error) {
            console.error("Error fetching Business Process 2:", error);
        }
    },


    async saveOrUpdate(){
        const post_risk_matrix = {
            business_process_1_id: this.editedItem.business_process_1_id,
            business_process_2_id: this.editedItem.business_process_2_id,
            step_business_process_2_level: this.editedItem.step_business_process_2_level,
            step_description: this.editedItem.step_description,
            step_performer: this.editedItem.step_performer,
            risk_code: this.editedItem.risk_code,
            risk_name: this.editedItem.risk_name,
            risk_description: this.editedItem.risk_description,
            control_procedure_code: this.editedItem.control_procedure_code,
            control_procedure_name: this.editedItem.control_procedure_name,
            control_procedure_owner: this.editedItem.control_procedure_owner,
            control_procedure_description: this.editedItem.control_procedure_description,
            control_procedure_inner_outer_document: this.editedItem.control_procedure_inner_outer_document,
            control_procedure_frequency: this.editedItem.control_procedure_frequency,
            control_procedure_type: this.editedItem.control_procedure_type,
            control_procedure_category: this.editedItem.control_procedure_category,
            effectivity_assessment: this.editedItem.effectivity_assessment,
            basis_of_assessment: this.editedItem.basis_of_assessment,


        };
        console.log('POST data for Risk Matrix:', post_risk_matrix);

        try {
            const response = await axios.post("http://localhost:8000/internal_system_control/post/risk_matrix/", post_risk_matrix);
            console.log('Risk matrix response from backend:', response.data);
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
            business_process_2_id: null,
            business_process_2_id: null,
            business_process_1_name: '',
            business_process_2_name: '',
            step_business_process_2_level: '',
            step_description: '',
            step_performer: '',
            risk_code: '',
            risk_description: '',
            control_procedure_code: '',
            control_procedure_name: '',
            control_procedure_owner: '',
            control_procedure_description: '',
            control_procedure_inner_outer_document: '',
            control_procedure_frequency: '',
            control_procedure_type: '',
            control_procedure_category: '',
            effectivity_assessment: '',
            basis_of_assessment: '',         
        };
        this.pg_dialog = true;
    },

// need to change EDIT , change this.dialog into new dialog for editting

    editItem(risk_matrix) {
      this.editedItemId = risk_matrix.id;
      this.editedItem = { ...risk_matrix };
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
    this.fetch_risk_matrix();
    this.fetchBusinessProcess1();
    this.fetchBusinessProcess2();
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



