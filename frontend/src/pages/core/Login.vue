<template>
  <v-app id="login" class="secondary">
    <v-content>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4 lg4>
            <v-card class="elevation-1 pa-3">
              <v-card-text>
                <div class="layout column align-center">
                  <img src="static/ktz_logo.png" width="450" height="120">
                  <!-- <h1 class="flex my-4 primary--text">RiskNET</h1> --><br><br><br><br>
                </div>
                <v-form>

                  <v-text-field
                    append-icon="person"
                    name="email"
                    label="Логин"
                    type="text"
                    v-model="email"
                    :error="error"
                    :rules="[rules.required]"/>
                  <v-text-field
                    :type="hidePassword ? 'password' : 'text'"
                    :append-icon="hidePassword ? 'visibility_off' : 'visibility'"
                    name="password"
                    label="Пароль"
                    id="password"
                    :rules="[rules.required]"
                    v-model="password"
                    :error="error"
                    @click:append="hidePassword = !hidePassword"/>
                </v-form>
              </v-card-text>
              <v-card-actions class = "d-flex justify-center">
                <v-spacer></v-spacer>
                <v-btn block color="primary" @click="register" :loading="loading">Регистрация</v-btn>
                <v-btn block color="primary" @click="submit_login ({id, email, password})" :loading="loading">
                  {{ id ? "Edit" : "Войти"}}</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
      <v-snackbar
        v-model="showResult"
        :timeout="2000"
        top>
        {{ result }}
      </v-snackbar>
    </v-content>
  </v-app>
</template>

<script>
export default {
  computed:{
    userId:{
      get(){
        return this.$store.state.user.id
      },
      // set(value){
      //   this.$store.commit("user/storeId", value)
      // }
    },
    userEmail:{
      get(){
        return this.$store.state.user.email
      },
      // set(value){
      //   this.$store.commit("user/storeEmail", value)
      // }
    },
    userPassword:{
      get(){
        return this.$store.state.user.password
      },
      // set(value){
      //   this.$store.commit("user/storePassword", value)
      // }
    }
  },

  data() {
    return {
      loading: false,
      id:0,
      email: '',
      password: '',
      hidePassword: true,
      error: false,
      showResult: false,
      result: '',
      rules: {
        required: value => !!value || 'Обязательное поле.'
      }
    }
  },

  methods: {
    async submit_login() {
      this.loading = true;
      this.error = false;
      this.result = '';

      const formData = new URLSearchParams();
      formData.append('username', this.email);
      formData.append('password', this.password);

      try {
        const response = await this.$axios.post('http://127.0.0.1:8000/login', formData);

        console.log('Login successful:', response.data);
        this.result = 'Login successful';
        this.$router.push({ name: 'Home' });

      } catch (error) {
          console.error('Login error:', error);
          this.result = 'Неверный логин или пароль';
          this.error = true;
      } finally {
          this.loading = false;
          this.showResult = true;
      }
    },



    register() {
      this.$router.push({ name: 'Register' });
    }
  }
}

</script>

<style scoped lang="css">
  #login {
    height: 50%;
    width: 100%;
    position: absolute;
    top: 0;
    left: 0;
    content: "";
    z-index: 0;
  }
</style>
