<template>
  <v-app-bar
    dark
    app
    :color="$root.themeColor"
  >
    <v-spacer></v-spacer>

    <v-dialog
      v-model="dialogSettings"
      width="700"
    >
      <v-card>
        <v-card-title
          class="headline"
          style="justify-content: center;"
          primary-title
        >
          Настройки
        </v-card-title>

        <v-card-text class="text-center" style="justify-content: center;">
          Изменение персональных данных </v-card-text>
          <v-form>
            <v-container>
              <v-row>
                <v-col cols="12" xs12 sm6 md11>
                  <v-text-field
                    v-model="password"
                    :append-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                    :type="showPassword ? 'text' : 'password'"
                    label="Новый пароль"
                    :error="error"
                    @click:append="showPassword = !showPassword"
                  />
                </v-col>

                <v-col cols="12" xs12 sm6 md11>
                  <v-text-field
                    v-model="passwordConfirm"
                    :append-icon="showPasswordConfirm ? 'mdi-eye-off' : 'mdi-eye'"
                    :type="showPasswordConfirm ? 'text' : 'password'"
                    label="Подтвердите пароль"
                    :error="error"
                    @click:append="showPasswordConfirm = !showPasswordConfirm"
                  />
                </v-col>
              </v-row>

              <v-row justify="center">
                <v-col cols="auto">
                  <v-btn>
                    Сохранить
                  </v-btn>
                </v-col>
              </v-row>
            </v-container>
          </v-form>
        <!-- </v-card-text> -->
      </v-card>
    </v-dialog>

    <v-menu
      class="toolbar-menu-item"
      offset-y
      origin="center center"
      :nudge-bottom="10"
      transition="scale-transition"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn v-bind="attrs" v-on="on" icon large text :ripple="false">
          <v-avatar size="42px">
            <img src="https://avataaars.io/?avatarStyle=Circle&topType=ShortHairShortFlat&accessoriesType=Sunglasses&hairColor=Black&facialHairType=Blank&clotheType=CollarSweater&clotheColor=Black&eyeType=Default&eyebrowType=Default&mouthType=Smile&skinColor=Light"/>
          </v-avatar>
        </v-btn>
      </template>
      <v-list>
        <v-list-item
          v-for="(item, index) in items"
          :key="index"
          :to="!item.href ? { name: item.name } : null"
          :href="item.href"
          :disabled="item.disabled"
          :target="item.target"
          @click="item.click"
        >
          <v-list-item-action v-if="item.icon">
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app-bar>
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
          icon: 'mdi-settings',
          href: '',
          title: 'Настройки',
          click: () => {
            this.dialogSettings = true;
          }
        },
        {
          icon: 'mdi-exit-to-app',
          href: '#',
          title: 'Выйти',
          click: () => {
            this.$router.push({ name: 'Login' });
          }
        }
      ]
    };
  },
  methods: {
    toggleNavigationBar() {
      this.$root.$emit('toggleNavigationBar');
    }
  }
};
</script>

<style>
.toolbar-menu-item {
  padding-left: 5px;
}
</style>
