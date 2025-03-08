<template>
  <div class="register-container">
    <h2>Registro de Usuário</h2>
    <form @submit.prevent="registerUser">
      <div class="form-group">
        <label for="username">Usuário</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div class="form-group">
        <label for="password">Senha</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit" class="btn">Registrar</button>
    </form>
    <div v-if="message" :class="{'success': success, 'error': !success}" class="message">
      {{ message }}
    </div>
    <div class="login-link">
      <p>
        Não tem uma conta?
        <router-link to="/login">Login aqui</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Register',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      message: '',
      success: false,
    };
  },
  methods: {
    async registerUser() {
      try {
        const response = await axios.post('http://localhost:8000/api/auth/register', {
          username: this.username,
          email: this.email,
          password: this.password,
        });
        this.message = "Usuário registrado com sucesso!";
        this.success = true;
      } catch (error) {
        this.message = error.response?.data?.detail || "Erro no registro.";
        this.success = false;
      }
    },
  },
};
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  font-family: "Poppins", sans-serif;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
}

.form-group {
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 0.5rem;
  font-size: 1rem;
  color: #333;
  font-weight: 600;
}

input {
  padding: 0.75rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  outline: none;
  transition: border-color 0.3s;
}

input:focus {
  border-color: #572364;
}

.btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #572364;
  color: #fff;
  border: none;
  font-family: "Poppins", sans-serif;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #451252;
}

.message {
  margin-top: 1rem;
  text-align: center;
  font-size: 0.9rem;
}

.success {
  color: green;
}

.error {
  color: red;
}

.login-link {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.9rem;
}

.login-link a {
  color: #572364;
  text-decoration: none;
  font-weight: bold;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
