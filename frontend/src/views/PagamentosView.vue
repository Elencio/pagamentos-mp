<template>
  <div class="payment-list-container">
    <h2>Lista de Pagamentos</h2>
    <div class="header">
      <p v-if="user">
        Você está logado como <strong>{{ user.username }}</strong>
        <span v-if="user.is_admin">(Administrador)</span>
        <span v-else>(Usuário)</span>
      </p>
      <button class="btn-logout" @click="logout">Logout</button>
    </div>

    <router-link to="/new-payment" class="btn-new">
      Novo Pagamento
    </router-link>

    <div v-if="loading" class="loading">
      Carregando...
    </div>

    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>

    <table class="payments-table" v-else-if="payments.length > 0">
      <thead>
        <tr>
          <th>ID</th>
          <th>Cliente</th>
          <th>Valor</th>
          <th>Tipo</th>
          <th>Status</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="pay in payments" :key="pay.id">
          <td>{{ pay.id }}</td>
          <td>
            {{ pay.cliente ? pay.cliente.nome + ' ' + pay.cliente.sobrenome : pay.cliente_id }}
          </td>
          <td>R$ {{ pay.valor.toFixed(2) }}</td>
          <td>{{ pay.tipo_pagamento?.nome || pay.tipo_pagamento_id }}</td>
          <td>
            <span :class="['status-badge', getStatusClass(pay.status)]">
              {{ pay.status }}
            </span>
          </td>
          <td>
            <button v-if="pay.status.toLowerCase() === 'pendente' && !user.is_admin"
                    class="btn-quitar"
                    @click="quitarPagamento(pay.id)">
              Quitar
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-else class="no-payments">Nenhum pagamento encontrado.</p>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "PaymentList",
  data() {
    return {
      payments: [],
      loading: true,
      error: null,
      user: null,
    };
  },
  methods: {
    async fetchPayments() {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          this.error = "Usuário não autenticado.";
          return;
        }
        axios.defaults.headers.common["Authorization"] = "Bearer " + token;
        this.loading = true;
        const response = await axios.get("http://localhost:8000/api/pagamentos");
        this.payments = response.data.pagamentos || [];

        const userResponse = await axios.get("http://localhost:8000/api/auth/me");
        this.user = userResponse.data;
        this.error = null;
      } catch (error) {
        console.error("Erro ao buscar dados:", error);
        this.error = "Não foi possível buscar os dados.";
      } finally {
        this.loading = false;
      }
    },
    getStatusClass(status) {
      switch (status.toLowerCase()) {
        case "pago":
          return "status-paid";
        case "pendente":
          return "status-pending";
        default:
          return "status-other";
      }
    },
    logout() {
      localStorage.removeItem("token");
      delete axios.defaults.headers.common["Authorization"];
      this.$router.push({ name: "Login" });
    },
    async quitarPagamento(pagamentoId) {
  try {

    const payment = this.payments.find(p => p.id === pagamentoId);
    if (!payment) {
      alert("Pagamento não encontrado.");
      return;
    }

    const payload = {
      transaction_amount: payment.valor
    };
    const response = await axios.put(`http://localhost:8000/api/pagamentos/${pagamentoId}/quitar`, payload);
    this.fetchPayments();
  } catch (error) {
    console.error("Erro ao quitar pagamento:", error);
    alert("Não foi possível quitar o pagamento.");
  }
},

  },
  mounted() {
    this.fetchPayments();
  },
};
</script>

<style scoped>
.payment-list-container {
  max-width: 800px;
  margin: 2rem auto;
  font-family: "Poppins", sans-serif;
  border-radius: 8px;
  padding: 2rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.btn-logout {
  background-color: #d9534f;
  color: #fff;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-family: "Poppins", sans-serif;
  transition: background-color 0.3s;
}

.btn-logout:hover {
  background-color: #c9302c;
}

.btn-new {
  display: inline-block;
  background-color: #572364;
  color: #fff;
  padding: 0.8rem 1.2rem;
  border-radius: 4px;
  text-decoration: none;
  margin-bottom: 1.5rem;
}

.payments-table {
  width: 100%;
  border-collapse: collapse;
}

.payments-table th,
.payments-table td {
  padding: 0.8rem;
  text-align: left;
  border-bottom: 1px solid #ccc;
}

.status-badge {
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  color: #fff;
}

.status-paid {
  background-color: #5cb85c;
}

.status-pending {
  background-color: #f0ad4e;
}

.status-other {
  background-color: #999;
}

.btn-quitar {
  background-color: #0275d8;
  color: #fff;
  border: none;
  font-family: "Poppins", sans-serif;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-quitar:hover {
  background-color: #025aa5;
}

.loading,
.error-message,
.no-payments {
  text-align: center;
  padding: 2rem;
}
</style>
