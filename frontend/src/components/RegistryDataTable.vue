<template>
  <v-card style="max-width: 155%;">
    <v-toolbar flat>
      <v-toolbar-title>Реестр</v-toolbar-title>
      
      <v-btn style="margin-left: 50px;" v-if="isCentralApparatus && tableType === 'main_table'" color="primary" @click="consolidateRisks"> Консолидировать </v-btn>

      <v-spacer></v-spacer>
   
      <!-- <v-btn small icon @click="editItem(reestr)" class="icon-button"><v-icon>mdi-pencil</v-icon></v-btn> -->
      <vue-json-to-csv
        :json-data="reestr"
        :csv-title="'Реестр'"
        :fields="{
          risk_category_name: 'КАТЕГОРИЯ РИСКА',
          risk_code: 'КОД РИСКА'
        }"
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

 
      <v-btn style="margin-right: 10px;" @click="openAddDialog">Добавить новый риск</v-btn>
      <v-btn @click="openAddEventDialog">Добавить мерпориятия</v-btn>

    </v-toolbar>

    <v-data-table   
       class="elevation-1"
       item-key="level_1_id"
      :headers="headers"
      :items="reestr"
      :search="search"
      :rows-per-page-items="[5, 10, 20, 50, 100, 200, 1000]"
      >

    <template v-slot:items="{ item }">

          <td>{{ item.risk_category_name }}</td>
          <td>{{ item.level_1_id }}</td>
          <td>{{ item.owner }}</td>
          <td>{{ item.control_sp }}</td>
          <td>{{ item.description_1 }}</td>
          <td>{{ item.description_2 }}</td>
          <td>{{ item.description_3 }}</td>
          <td>{{ item.description_4 }}</td>
          <td>{{ item.swot }}</td>
          <td>{{ item.prob_1 }}</td>
          <td>{{ item.effect_1 }}</td>
          <td>{{ item.loss_1 }}</td>
          <td>{{ item.event_name }}</td>
          <td>{{ item.responsible_sp }}</td>
          <td>{{ item.event_effectiveness }}</td>
          <td>{{ item.residual_loss }}</td>


        
        <td><v-btn small icon @click="openDeleteDialog(item)"><v-icon>mdi-delete</v-icon></v-btn></td>
        <td><v-btn small icon @click="editItem(reestr)"><v-icon>mdi-pencil</v-icon></v-btn></td>
      </template>
  </v-data-table>


  <v-dialog v-model="eventDialog" max-width="650px" maxHeight="700px">
      <v-card>
        <v-card-title style="text-align: center">
          <span>{{ formEvent }}</span>
        </v-card-title>

        <v-card-text>
          <v-select
            v-if="showRiskCategoryInput"
            v-model="editedItem.risk_category_name"
            :items="riskCategories"
            label="Выберите категорию риска"
            required
            class="mb-5"
            item-text="risk_category_name"
            item-value="risk_category_name"
            @change="handleCategorySelect"
          ></v-select>

          <v-select v-if="editedItem.risk_category_name" v-model="editedItem.level_1_id"  item-text ='description_1' item-value='level_1_id' @change="handleLevel1Select"
              :items="riskFactor1Description"  label="ВЫБЕРИТЕ ФАКТОР РИСКА УРОВЕНЬ 1"
              ></v-select>

          <v-select
            v-if="editedItem.level_1_id"
            v-model="editedItem.level_2_id"
            :items="riskFactor2Description"
            label="Выберите риск фактор уровня 2"
            required
            class="mb-5"
            item-text="description_2"
            item-value="level_2_id"
            @change="handleLevel2Select"
          ></v-select>
          <v-row v-if="editedItem.level_2_id" justify="center" >
            <div style="height: 300px; text-align: center;">ОПИСАНИЕ МЕРОПРИЯТИИ
            <v-text-field v-if="editedItem.level_2_id" v-model="editedItem.event_name" label="НАИМЕНОВАНИЕ МЕРОПРИЯТИЯ ПО СНИЖЕНИЮ РИСКА" required></v-text-field>
            <v-text-field v-if="editedItem.level_2_id" v-model="editedItem.responsible_sp" label="ОТВЕТСТВЕННОЕ СП" required></v-text-field>
            <v-select v-if="editedItem.level_2_id" v-model="editedItem.event_effectiveness" :items="['высокий','средний','низкий', 'Очистить']" label="ЭФФЕКТИВНОСТЬ" @input="handleSelect" required></v-select>
            <v-btn @click="closeDialog" class = "ml-auto">Отменить</v-btn>
            <v-btn @click="saveEvents" class = "ml-auto">Сохранить</v-btn>  
          </div>

          </v-row>

        </v-card-text>
      </v-card>
  </v-dialog>

    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title style="text-align: center">
          <span>{{ formTitle }}</span>
        </v-card-title>

        <!-- ADD THE NEW RECORD -->
        <v-card-text>
            
          <v-select
            v-if="showRiskCategoryInput" v-model="editedItem.risk_category_name" :items="riskCategories" label="Выберите категорию риска" required 
            class="mb-5"item-text="risk_category_name" item-value="risk_category_name" @change="handleCategorySelect"
          ></v-select>
        
        <v-row>
          <v-col v-if="!showLevel2Inputs && editedItem.risk_category_name"> 
            <div style="text-align: center;">ОПИСАНИЯ РИСК ФАКТОРА УРОВНЯ 1</div>
              <v-text-field v-if="editedItem.risk_category_name" v-model="editedItem.description_1" label="ФАКТОРЫ РИСКА УРОВЕНЬ 1 (описание)" required></v-text-field>
              <v-text-field v-if="editedItem.risk_category_name" v-model="editedItem.owner" label="ВЛАДЕЛЕЦ РИСКА" required></v-text-field>
              <v-text-field v-if="editedItem.risk_category_name" v-model="editedItem.control_sp" label="КОНТРОЛИРУЮЩЕЕ СП" required></v-text-field>
              <v-select v-if="editedItem.risk_category_name" :items="['высокий','средний','низкий', 'Очистить']" v-model="editedItem.priority" label="ПРИОРИТЕТ" required @input="handleSelect"></v-select>
              
              <v-btn icon @click="saveIntermediateData_1"><v-icon>mdi-plus</v-icon></v-btn>
              <v-btn @click="showLevel2Inputs = true; showRiskCategoryInput = false;" class="ml-auto" >Далее</v-btn>
          </v-col>
        </v-row>
        
        <v-row>
          <v-col v-if="showLevel2Inputs" justify="center">
              <div style="text-align: center;">ОПИСАНИЯ РИСК ФАКТОРА УРОВНЯ 2</div>
              <v-select v-if="showLevel2Inputs" v-model="editedItem.level_1_id"  item-text ='description_1' item-value='level_1_id' @change="handleLevel1Select" :items="riskFactor1Description"  label="ВЫБЕРИТЕ ФАКТОР РИСКА УРОВЕНЬ 1"></v-select>
              <v-text-field v-if="showLevel2Inputs" v-model="editedItem.description_2" label="ФАКТОР РИСКА УРОВЕНЬ 2(описание)" required></v-text-field>
              <v-select v-if="showLevel2Inputs" :items="['КОЛИЧЕСТВЕННЫЕ','КАЧЕСТВЕННЫЕ']" v-model="editedItem.data_type" label="ТИП ДАННЫХ" required></v-select>
              <v-text-field v-if="showLevel2Inputs && editedItem.data_type === 'КОЛИЧЕСТВЕННЫЕ'" v-model="editedItem.prob_2" label="ВЕРОЯТНОСТЬ" required></v-text-field>
              <v-text-field v-if="showLevel2Inputs && editedItem.data_type === 'КОЛИЧЕСТВЕННЫЕ'" v-model="editedItem.effect_2" label="ЭФФЕКТИВНОСТЬ" required></v-text-field>
              <v-slider v-if="showLevel2Inputs && editedItem.data_type === 'КАЧЕСТВЕННЫЕ'" v-model="editedItem.prob_2" label="БАЛЛ ВЕРОЯТНОСТЬ" tick-size="2" thumb-label ticks="always" min="0" max="10"></v-slider>
              <v-slider v-if="showLevel2Inputs && editedItem.data_type === 'КАЧЕСТВЕННЫЕ'" v-model="editedItem.effect_2" label="БАЛЛ ЭФФЕКТИВНОСТЬ" tick-size="2" thumb-label ticks="always" min="0" max="10"></v-slider>
              <v-select v-if="showLevel3Inputs" :items="['Сильные стороны','Слабые стороны','Возможности','Угрозы','Очистить']" v-model="editedItem.swot" label="SWOT" required @input="handleSelect"></v-select>
              <v-text-field v-if="showLevel2Inputs" v-model="editedItem.comments_2" label="КОММЕНТАРИЙ"></v-text-field>

              <v-btn @click="showLevel2Inputs = false; showRiskCategoryInput = true">Назад</v-btn>
              <v-btn icon @click="saveIntermediateData_2"><v-icon>mdi-plus</v-icon></v-btn>
              <v-btn @click="showLevel3Inputs = true; showLevel2Inputs = false;  editedItem.risk_category_name = false; showRiskCategoryInput = false" class="ml-auto">Далее</v-btn>
          </v-col>
        </v-row>
          
        <v-row>
          <v-col v-if="showLevel3Inputs" justify="center" class="mb-3">
              <div style="text-align: center;">ОПИСАНИЯ РИСК ФАКТОРА УРОВНЯ 3</div>
              <v-select v-if="showLevel3Inputs" v-model="editedItem.level_2_id" item-text="description_2" item-value="level_2_id" @change="handleLevel2Select" :items="riskFactor2Description" label="ВЫБЕРИТЕ ФАКТОР РИСКА УРОВЕНЬ 2"></v-select>
              <v-text-field v-if="showLevel3Inputs" v-model="editedItem.description_3" label="ФАКТОР РИСКА УРОВЕНЬ 3(описание)" required></v-text-field>
              <v-select v-if="showLevel3Inputs" :items="['КОЛИЧЕСТВЕННЫЕ','КАЧЕСТВЕННЫЕ', 'Очистить']" v-model="editedItem.data_type" label="ТИП ДАННЫХ" required @input="handleSelect"></v-select>
              <v-text-field v-if="showLevel3Inputs && editedItem.data_type === 'КОЛИЧЕСТВЕННЫЕ'" v-model="editedItem.prob_3" label="ВЕРОЯТНОСТЬ" required></v-text-field>
              <v-text-field v-if="showLevel3Inputs && editedItem.data_type === 'КОЛИЧЕСТВЕННЫЕ'" v-model="editedItem.effect_3" label="ЭФФЕКТИВНОСТЬ" required></v-text-field>
              <v-slider v-if="showLevel3Inputs && editedItem.data_type === 'КАЧЕСТВЕННЫЕ'" v-model="editedItem.prob_3" label="БАЛЛ ВЕРОЯТНОСТЬ" tick-size="2" thumb-label ticks="always" min="0" max="10"></v-slider>
              <v-slider v-if="showLevel3Inputs && editedItem.data_type === 'КАЧЕСТВЕННЫЕ'" v-model="editedItem.effect_3" label="БАЛЛ ЭФФЕКТИВНОСТЬ" tick-size="2" thumb-label ticks="always" min="0" max="10"></v-slider>
              <v-text-field v-if="showLevel3Inputs" v-model="editedItem.comments_3" label="КОММЕНТАРИЙ"></v-text-field>

              <v-btn @click="showLevel3Inputs = false; showLevel2Inputs = true">Назад</v-btn>
              <v-btn icon @click="saveIntermediateData_3"><v-icon>mdi-plus</v-icon></v-btn>
              <v-btn @click="showLevel4Inputs = true; showLevel3Inputs = false; showRiskCategoryInput = false"  class="ml-auto">Далее</v-btn>
          </v-col>
        </v-row>

        <v-row>
          <v-col v-if="showLevel4Inputs" justify="center" class="mb-3">
              <div style="text-align: center;">ОПИСАНИЯ РИСК ФАКТОРА УРОВНЯ 4</div>
              <v-select v-if="showLevel4Inputs" v-model="editedItem.level_3_id" item-text="description_3" item-value="level_3_id" @change = "handleLevel3Select" :items="riskFactor3Description" label="ВЫБЕРИТЕ ФАКТОР РИСКА УРОВЕНЬ 3"></v-select>
              <v-text-field v-if="showLevel4Inputs" v-model="editedItem.description_4" label="ФАКТОР РИСКА УРОВЕНЬ 4(описание)" required></v-text-field>      
              <v-select v-if="showLevel4Inputs" :items="['КОЛИЧЕСТВЕННЫЕ','КАЧЕСТВЕННЫЕ', 'Очистить']" v-model="editedItem.data_type" label="ТИП ДАННЫХ" required @input="handleSelect"></v-select>
              <v-text-field v-if="showLevel4Inputs && editedItem.data_type === 'КОЛИЧЕСТВЕННЫЕ'" v-model="editedItem.prob_4" label="ВЕРОЯТНОСТЬ" required></v-text-field>
              <v-text-field v-if="showLevel4Inputs && editedItem.data_type === 'КОЛИЧЕСТВЕННЫЕ'" v-model="editedItem.effect_4" label="ЭФФЕКТИВНОСТЬ" required></v-text-field>              
              <v-slider v-if="showLevel4Inputs && editedItem.data_type === 'КАЧЕСТВЕННЫЕ'" v-model="editedItem.prob_4" label="БАЛЛ ВЕРОЯТНОСТЬ" tick-size="2" thumb-label ticks="always" min="0" max="10"></v-slider>
              <v-slider v-if="showLevel4Inputs && editedItem.data_type === 'КАЧЕСТВЕННЫЕ'" v-model="editedItem.effect_4" label="БАЛЛ ЭФФЕКТИВНОСТЬ" tick-size="2" thumb-label ticks="always" min="0" max="10"></v-slider>             
              <v-text-field v-if="showLevel4Inputs" v-model="editedItem.comments_4" label="КОММЕНТАРИЙ"></v-text-field>

              <v-btn @click="showLevel4Inputs = false; showLevel3Inputs = true">Назад</v-btn>
              <v-btn icon @click="saveIntermediateData_4"><v-icon>mdi-plus</v-icon></v-btn>
              <v-btn @click="saveOrUpdate" class = "ml-auto">Сохранить</v-btn>
          </v-col>
        </v-row>
          
        </v-card-text>

        <!-- <v-card-actions class="justify-center"></v-card-actions>
        <v-card-actions class="justify-center"></v-card-actions> -->

      </v-card>
    </v-dialog>

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
</template>

<script>
import axios from 'axios';
import { jwtDecode } from "jwt-decode";

export default {
  props: {
    tableType: {
      type: String,
      required: true
    }
  },

  data() { 
    return {
      selected: [],
      selectedRisk: [],
      search: '',
      dialog: false,
      eventDialog: false,
      deleteDialog: false,
      headers: [
        // { value: '', text:''},
        { value: 'risk_category_name', text: 'КАТЕГОРИЯ РИСКА'}, // RISK CATEGORY
        { value: 'level_1_id', text: 'КОД РИСКА'}, // РИСК ФАКТОР 1
        { value: 'owner', text: 'ВЛАДЕЛЕЦ РИСКА'}, // RISK FACTOR 1
        { value: 'control_sp', text: 'КОНТРОЛИРУЮЩЕЕ СП'}, // RISK FACTOR 1 
        { value: 'description_1', text: 'ФАКТОРЫ РИСКА УРОВЕНЬ 1'}, // RISK FACTOR 1
        { value: 'description_2', text: 'ФАКТОРЫ РИСКА УРОВЕНЬ 2'},
        { value: 'description_3', text: 'ФАКТОРЫ РИСКА УРОВЕНЬ 3' },
        { value: 'description_4', text: 'ФАКТОРЫ РИСКА УРОВЕНЬ 4' },
        { value: 'swot', text: 'SWOT' },
        { value: 'prob_1', text: 'ВЕРОЯТНОСТЬ 1 ФАКТОРА' },
        { value: 'effect_1', text: 'ЭФФЕКТИВНОСТЬ 1 ФАКТОРА' },
        { value: 'loss_1', text: 'ОЖИДАЕМЫЕ ПОТЕРИ 1 ФАКТОРА' },
        { value: 'event_name', text: 'НАИМЕНОВАНИЕ МЕРОПРИЯТИЯ ПО СНИЖЕНИЮ РИСКА' },
        { value: 'responsible_sp', text: 'ОТВЕТСТВЕННОЕ СП' },
        { value: 'event_effectiveness', text: 'ЭФФЕКТИВНОСТЬ МЕРОПРИЯТИЯ'},
        { value: 'residual_loss', text: 'ОЖИДАЕМЫЕ ПОТЕРИ/ПРИБЫЛЬ(ОСТАТОЧНЫЙ)'},
        { value: 'delete', text: 'УДАЛИТЬ' },
        { value: 'edit', text: 'ИЗМЕНИТЬ' },

      ],
      editedItem: {
        risk_category_name: '',
        level_1_id: '',
        level_2_id: '',
        level_3_id: '',
        level_4_id: '',
        owner: '',
        control_sp: '',
        priority: '',
        description_1: '',
        description_2: '',
        description_3: '',
        description_4: '',
        swot: '',
        prob_1: '',
        effect_1:'',
        loss_1:'',
        prob_2: '',
        effect_2:'',
        comments_2: '',
        prob_3: '',
        effect_3:'',
        comments_3:'',
        prob_4: '',
        effect_4:'',
        comments_4: '',
        event_name: '',
        responsible_sp: '',
        event_effectiveness: '',
        residual_loss: '',
      },
      editedItemId: null,
      reestr: [],
      showRiskCategoryInput: true,
      showLevel2Inputs: false,
      showLevel3Inputs: false,
      showLevel4Inputs: false,
      showEventInputs: false,
      selectedCategory: null,
      riskCategories:[],
      riskFactor1Description:[],
      riskFactor2Description:[],
      riskFactor3Description:[],
      riskFactor4Description:[],
      riskFactor2DescriptionForEvent: [],
    };
  },

  computed: {
    computedReestr() {
      return this.search ? this.filteredReestr : this.reestr;
    },
    formTitle() {
      return this.editedItemId ? 'Edit Item' : 'Добавить новый риск';
    },
    formEvent(){
      return this.editedItemId ? 'Добавление мероприятия' : "Добавить мероприятия";
    },
    isCentralApparatus() {
      const token = localStorage.getItem('access_token');

      const decodedToken = jwtDecode(token);
      console.log('Decoded token:', decodedToken);
      return decodedToken.workplace === 11 && decodedToken.department === 'ЦУР';  // Проверяем должность пользователя
      // НУЖНО ДЛЯ ОТОБРАЖЕНИЯ КНОПКИ КОНСОЛИДИРОВАТЬ
    },
  },

  methods: {


    // ASYNC GET METHODS

    async fetchReestr() {
      try {
        const token = localStorage.getItem('access_token');
        let endpoint = '';
        if (this.tableType === 'structure_divisions') {
            endpoint = 'structure_divisions_table';
          } 
        else if (this.tableType === 'main_table') {
            endpoint = 'main_table';
          } 
        else if (this.tableType === 'consolidated') {
            endpoint = 'consolidated';
          }
        const response = await axios.get(`http://localhost:8000/reestr/${endpoint}`, 
            { headers: 
              {'Authorization': `Bearer ${token}`}
            }
          );
            
        this.reestr = response.data;
        console.log('API Response:', response.data);
        console.log('responseXML:: ', await response); //Show list of things
      } 
        catch (error) {
          console.error("Error fetching reestr:", error);
        }
    },
   
    async fetchRiskCategories() {
      try {
        const response = await axios.get("http://localhost:8000/reestr/risk_category_name/");

        console.log('API response:: ', response.data); //Show list of things
        this.riskCategories = response.data;
      } catch (error) {
        console.error("Error fetching reestr category:", error);
      }
    },
    
    async fetchRiskCode() {
      if (this.editedItem.risk_category_name) {
        this.selectedCategory = this.riskCategories.find(category => category.risk_category_name === this.editedItem.risk_category_name);
      }
    },

    async fetchDescriptions() {
      try {
        if (!this.editedItem || !this.editedItem.risk_category_name) {
            return;
        }

        const response = await axios.get(`http://localhost:8000/reestr/description_1/${this.editedItem.risk_category_name}`);
        if (response.status !== 200) {
            console.error('Ошибка при получении описаний:', response.statusText);
            return;
        }
        console.log('API response123:: ', response.data); //Show list of things

        this.riskFactor1Description = response.data;
      } 
      catch (error) {
        console.error('Ошибка при получении описаний:', error);
      }
    },

    async fetchDescriptions_2() {
      try {
        if (!this.editedItem.level_1_id) {
            return;
        }
        const response = await axios.get(`http://localhost:8000/reestr/description_2/${this.editedItem.level_1_id}`);

        if (response.status !== 200) {
            console.error('Ошибка при получении описаний:', response.statusText);
            return;
        }
        console.log('API response for description2:: ', response.data); //Show list of things
        
        this.riskFactor2Description = response.data;
      } 
      catch (error) {
        console.error('Ошибка при получении описаний:', error);
      }
    },

    async fetchDescriptions_3() {
      try {
        if (!this.editedItem.level_2_id) {
            return;
        }
        const response = await axios.get(`http://localhost:8000/reestr/description_3/${this.editedItem.level_2_id}`);

        if (response.status !== 200) {
            console.error('Ошибка при получении описаний:', response.statusText);
            return;
        }
        console.log('API response for description3:: ', response.data); //Show list of things
        
        this.riskFactor3Description = response.data;
      } 
      catch (error) {
        console.error('Ошибка при получении описаний:', error);
      }
    },








//  HANDLES 

    handleSelect(value) {
      if (value === 'Очистить') {
        this.editedItem.priority = null; 
        this.editedItem.event_effectiveness = null;
        this.editedItem.data_type = '';
      }
    },
   
    handleCategorySelect() {
      if (this.editedItem.risk_category_name) {
              this.selectedCategory = this.riskCategories.find(category => category.risk_category_name === this.editedItem.risk_category_name);
              this.showRiskCategoryInput = false;
              this.fetchDescriptions();
        }
    },
    
    handleLevel1Select() {

      if (this.editedItem.level_1_id) {
        console.log('Выбранный level_1_id:', this.editedItem.level_1_id);
        
          const selectedLevel1 = this.riskFactor1Description.find(level1 => level1.level_1_id === this.editedItem.level_1_id);
          if (selectedLevel1) {
              this.editedItem.level_1_id = selectedLevel1.level_1_id;
              this.fetchDescriptions_2();
          } else {
              console.error('Выбранный элемент не найден в riskFactor1Description');
          }
      } else {
          console.error('Выбранный элемент не содержит level_1_id');
      }
    },
    handleLevel2Select() {

      if (this.editedItem.level_2_id) {
        console.log('Выбранный level_2_id:', this.editedItem.level_2_id);

          const selectedLevel2 = this.riskFactor2Description.find(level2 => level2.level_2_id === this.editedItem.level_2_id);
          if (selectedLevel2) {
              this.editedItem.level_2_id = selectedLevel2.level_2_id;
              this.fetchDescriptions_3();
          } else {
              console.error('Выбранный элемент не найден в riskFactor2Description');
          }
      } else {
          console.error('Выбранный элемент не содержит level_2_id');
      }
    },
    handleLevel3Select() {

    if (this.editedItem.level_3_id) {
      console.log('Выбранный level_3_id:', this.editedItem.level_3_id);

        const selectedLevel3 = this.riskFactor3Description.find(level3 => level3.level_3_id === this.editedItem.level_3_id);
        if (selectedLevel3) {
            this.editedItem.level_3_id = selectedLevel3.level_3_id;
            console.log('asd', this.editedItem.level_3_id)
            // this.fetchDescriptions_4();
        } else {
            console.error('Выбранный элемент не найден в riskFactor3Description');
        }
    } else {
        console.error('Выбранный элемент не содержит level_3_id');
    }
    },



// ASYNC POST DATA

    async saveIntermediateData_1() {
      const riskFactor1Data = {
        description_1: this.editedItem.description_1,
        owner: this.editedItem.owner,
        control_sp: this.editedItem.control_sp,
        priority: this.editedItem.priority,
        risk_code: this.selectedCategory.risk_code,
      };

      try {
        const response = await axios.post("http://localhost:8000/reestr/risk_factor_1/", riskFactor1Data);
        console.log('Response from backend:', response.data); 
      } 
        catch (error) {
        console.error("Error saving data:", error);
      }
    },

    async saveIntermediateData_2(){
      const riskFactor2Data = {
        description_2: this.editedItem.description_2,
        datatype: this.editedItem.data_type,
        prob: this.editedItem.prob_2,
        effect: this.editedItem.effect_2,
        swot: this.editedItem.swot,
        comments: this.editedItem.comments_2,
        level_1_id: this.editedItem.level_1_id
      }

      try {
        const response = await axios.post("http://localhost:8000/reestr/risk_factor_2/", riskFactor2Data);
        console.log('Response from backend:', response.data); 
      } 
        catch (error) {
        console.error("Error saving data:", error);
      }
    },
    
    async saveIntermediateData_3(){
      const riskFactor3Data = {
        description_3: this.editedItem.description_3,
        datatype: this.editedItem.data_type,
        prob: this.editedItem.prob_3,
        effect: this.editedItem.effect_3,
        comments: this.editedItem.comments_3,
        level_2_id: this.editedItem.level_2_id
      }

      try {
        const response = await axios.post("http://localhost:8000/reestr/risk_factor_3/", riskFactor3Data);
        console.log('Response from backend:', response.data); 
      } 
        catch (error) {
        console.error("Error saving data:", error);
      }
    },

    async saveIntermediateData_4(){
      const riskFactor4Data = {
        description_4: this.editedItem.description_4,
        datatype: this.editedItem.data_type,
        prob: this.editedItem.prob_4,
        effect: this.editedItem.effect_4,
        comments: this.editedItem.comments_4,
        level_3_id: this.editedItem.level_3_id
      }

      try {
        const response = await axios.post("http://localhost:8000/reestr/risk_factor_4/", riskFactor4Data);
        console.log('Response from backend:', response.data); 
      } 
        catch (error) {
        console.error("Error saving data:", error);
      }
    },

    async saveOrUpdate() {
          if (this.editedItemId) {
            // Update existing reestr
            await axios.put(`http://localhost:8000/reestr/${this.editedItemId}`, this.editedItem);
          } else {
            // Add new reestr
            await axios.post("http://localhost:8000", this.editedItem);
          }
          this.fetchReestr();
          this.closeDialog();
    },


    async saveEvents(){
      const riskEvents = {
        event_name: this.editedItem.event_name,
        responsible_sp: this.editedItem.responsible_sp,
        event_effectiveness: this.editedItem.event_effectiveness,
        level_2_id: this.editedItem.level_2_id
      }

      try {
        const response = await axios.post(`http://localhost:8000/reestr/risk_factor_2/${this.editedItem.level_2_id}/events`, riskEvents);
        console.log('Response from backend:', response.data); 
      } 
        catch (error) {
        console.error("Error saving data:", error);
      }
    },



    openAddDialog() {
      this.editedItem = {
        risk_category_name: '',
        level_1_id: '',
        level_2_id:'',
        level_3_id:'',
        level_4_id:'',
        owner: '',
        control_sp: '',
        description_1: '',
        description_2: '',
        description_3: '',
        description_4: '',
        swot:'',
        prob_1: '',
        effect_1:'',
        loss_1:'',
      };
      this.dialog = true;
    },
    openAddEventDialog(){
      this.editedItem = {
        event_name:'',
        responsible_sp:'',
        event_effectiveness:''
      };
      this.eventDialog = true;
    },

    editItem(reestr) {
      this.editedItemId = reestr.id;
      this.editedItem = { ...reestr };
      this.dialog = true;
    },

    
    openDeleteDialog(item) {
      this.editedItemId = item.id;
      this.deleteDialog = true;
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

    closeDialog() {
      this.dialog = false;
      this.eventDialog = false;
      this.editedItem = {};
      this.editedItemId = null;
    },

    closeDeleteDialog() {
      this.deleteDialog = false;
      this.editedItemId = null;
    },
  },

  mounted() {
    this.fetchReestr();
    this.fetchRiskCategories();
    this.fetchDescriptions();
    this.fetchDescriptions_2();
    this.fetchDescriptions_3();
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
