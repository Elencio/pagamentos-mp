<template>
  <div class="payment-list-container">
    <h2>Lista de Pagamentos</h2>


    <RouterLink to="/about">
      <button class="btn-new" @click="goToNewPayment">
        Novo Pagamento
      </button>
    </RouterLink>

    <table class="payments-table" v-if="payments.length > 0">
      <thead>
        <tr>
          <th>ID</th>
          <th>Cliente</th>
          <th>Valor</th>
          <th>Tipo</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="pay in payments" :key="pay.id">
          <td>{{ pay.id }}</td>
          <td>{{ pay.cliente_id }}</td>
          <td>R$ {{ pay.valor.toFixed(2) }}</td>
          <td>{{ pay.tipo_pagamento?.nome || pay.tipo_pagamento_id }}</td>
          <td>{{ pay.status }}</td>
        </tr>
      </tbody>
    </table>

    <p v-else>Nenhum pagamento encontrado.</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "PaymentList",
  data() {
    return {
      payments: [],
    };
  },
  methods: {
    async fetchPayments() {
      try {
        const response = await axios.get("http://localhost:8000/api/pagamentos");
        this.payments = response.data.pagamentos || [];
      } catch (error) {
        console.error("Erro ao buscar pagamentos:", error);
        alert("Não foi possível buscar a lista de pagamentos.");
      }
    },
    goToNewPayment() {
      this.$router.push({ name: "PaymentForm" });
    },
  },
  mounted() {
    this.fetchPayments();
  },
};
</script>

<style scoped>
.payment-list-container {
  max-width: 600px;
  margin: 2rem auto;
  font-family: "Poppins", serif;
}

.btn-new {
  background-color: #572364;
  color: #fff;
  border: none;
  padding: 0.6rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 1rem;
  font-family: "Poppins", serif;
}

.btn-new:hover {
  background-color: #3f1d4b;
}

.payments-table {
  width: 100%;
  border-collapse: collapse;
}

.payments-table th,
.payments-table td {
  border: 1px solid #ccc;
  padding: 0.5rem;
  text-align: left;
}

.payments-table th {
  background-color: #fce4ff;
  color: #572364;
}
</style>
