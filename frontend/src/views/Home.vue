<template>
  <div class="home-container">
    <h1>Pagamentos Simplificados</h1>
    <h2>Transações rápidas e seguras ao seu alcance</h2>
    <div class="buttons">
      <router-link to="/login" class="btn">Login</router-link>
      <router-link to="/register" class="btn">Register</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
};
</script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-family: "Poppins", sans-serif;
  height: 100vh;
  background-color: #f5f5f5;
  text-align: center;
  padding: 0 1rem;
}

h1 {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

h2 {
  font-size: 1.5rem;
  margin-bottom: 2rem;
  color: #555;
}

.buttons {
  display: flex;
  gap: 1rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  background-color: #572364;
  color: #fff;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #451252;
}
</style>
