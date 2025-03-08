<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="username">Usuário</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div class="form-group">
        <label for="password">Senha</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit" class="btn">Entrar</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
    <div class="register-link">
      <p>
        Não tem uma conta?
        <router-link to="/register">Registre-se aqui</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",
      error: null,
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post(
          "http://localhost:8000/api/auth/token",
          {
            username: this.username,
            password: this.password,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        localStorage.setItem("token", response.data.access_token);
        axios.defaults.headers.common["Authorization"] =
          "Bearer " + response.data.access_token;
        this.$router.push({ name: "payments-list" });
      } catch (err) {
        this.error = "Usuário ou senha incorretos.";
        console.error("Erro no login:", err);
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 2rem auto;
  font-family: "Poppins", sans-serif;
  padding: 2rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #fff;
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
  padding: 0.75rem 1.5rem;
  background-color: #572364;
  color: #fff;
  font-family: "Poppins", sans-serif;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #451252;
}

.error {
  color: red;
  margin-top: 1rem;
  text-align: center;
}

.register-link {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.9rem;
}

.register-link a {
  color: #572364;
  text-decoration: none;
  font-weight: bold;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>
