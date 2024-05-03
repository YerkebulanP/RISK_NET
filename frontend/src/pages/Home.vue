<template>
  <v-container fluid grid-list-xl>
    <div class="center-container">
      <div class="content">
        <h1>Добро пожаловать в RiskNET!</h1>
        <p>Здесь вы можете наблюдать рисками компании АО "НК" КТЖ"</p>
      </div>
    </div>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      
    }
  }
}
</script>

<style scoped>
.center-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 220px;
  padding: auto;
}

.content {
  /* Any styles for your centered content */
  padding: 20px;
  box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}
</style>
