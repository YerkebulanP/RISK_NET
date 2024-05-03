  <template>
    <v-toolbar
      dark
      app
      :color="$root.themeColor">
      <v-spacer></v-spacer>


      <v-dialog
        v-model="dialogSettings"
        width="700">
        <v-card>
          <v-card-title class = "headline" style="justify-content: center;"
            primary-title>
            Настройки
          </v-card-title>

          <v-card-text class="text-xs-center">
              Изменение персональных данных 
          <v-form>
              <v-container>
                <v-layout row wrap>

                 
                  <v-flex xs12 sm6 md11>
                    <v-text-field
                      v-model="password"
                      :append-icon="showPassword ? 'visibility_off' : 'visibility'"
                      :type="showPassword ? 'text' : 'password'"
                      label="Новый пароль"
                      :error="error"
                      @click:append="showPassword = !showPassword" />
                  </v-flex>


                  <v-flex xs12 sm6 md11>
                    <v-text-field
                      v-model="passwordConfirm"
                      :append-icon="showPasswordConfirm ? 'visibility_off' : 'visibility'"
                      :type="showPasswordConfirm ? 'text' : 'password'"
                      label="Подтвердите пароль"
                      :error="error"
                      @click:append="showPasswordConfirm = !showPasswordConfirm" />
                  </v-flex>


                </v-layout>
              </v-container>
            </v-form>
          </v-card-text>


          <v-card-actions class="justify-center">
            <!-- <v-btn @click="changePassword">Сохранить</v-btn> -->
          </v-card-actions>
        </v-card>
      </v-dialog>


      <v-menu class="toolbar-menu-item" offset-y origin="center center" :nudge-bottom="10" transition="scale-transition">
        <v-btn icon large flat slot="activator" :ripple="false">
          <v-avatar size="42px">
            <img src="https://avataaars.io/?avatarStyle=Circle&topType=ShortHairShortFlat&accessoriesType=Sunglasses&hairColor=Black&facialHairType=Blank&clotheType=CollarSweater&clotheColor=Black&eyeType=Default&eyebrowType=Default&mouthType=Smile&skinColor=Light"/>
          </v-avatar>
        </v-btn>
        <v-list>
          <v-list-tile
            v-for="(item,index) in items"
            :key="index"
            :to="!item.href ? { name: item.name } : null"
            :href="item.href"
            ripple="ripple"
            :disabled="item.disabled"
            :target="item.target"
            @click="item.click">
            <v-list-tile-action v-if="item.icon">
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>{{ item.title }}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-menu>
    </v-toolbar>
  </template>
  <script>

  export default {
    data() {
      return {
        dialog: false,
        dialogSettings: false,
        showPassword: null,
        showPasswordConfirm: null,
        userEmail: null,
        password: null,
        passwordConfirm: null,
        error: false,
        showResult: false,
        result: '',
        items: [
          {
            icon: 'settings',
            href: '#',
            title: 'Настройки',
            click: () => {
              const vm = this;

              vm.dialogSettings = true;
            }
          },
          {
            icon: 'exit_to_app',
            href: '#',
            title: 'Выйти',
            click: () => {
              const vm = this;

              vm.$router.push({ name: 'Login' });
            }
          }
        ],
      
        
    methods: {
      toggleNavigationBar() {
        this.$root.$emit('toggleNavigationBar');
      },

      async changePassword() {
        if (this.password === this.passwordConfirm) {
          try {
            const response = await this.$axios.post('http://localhost:8000/change-password', {
              oldPassword: this.oldPassword,
              newPassword: this.password
            });

            console.log('Пароль успешно изменён');
          } catch (error) {
            console.error('Ошибка при изменении пароля:', error);
          }
        } else {
          this.error = true;
          console.error('Пароли не совпадают');
        }
      }

    }
  };
    } }

  </script>
  <style>
    .toolbar-menu-item {
      padding-left: 5px;
    }

    
    
  </style>