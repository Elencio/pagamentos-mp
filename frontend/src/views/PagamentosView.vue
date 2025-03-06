<template>
  <div class="payment-list-container">
    <h2>Lista de Pagamentos</h2>

    <router-link to="/payment-form" class="btn-new">
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
        </tr>
      </thead>
      <tbody>
        <tr v-for="pay in payments" :key="pay.id">
          <td>{{ pay.id }}</td>
          <td>{{ pay.cliente_id }}</td>
          <td>R$ {{ pay.valor.toFixed(2) }}</td>
          <td>{{ pay.tipo_pagamento?.nome || pay.tipo_pagamento_id }}</td>
          <td>
            <span :class="['status-badge', getStatusClass(pay.status)]">
              {{ pay.status }}
            </span>
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
    };
  },
  methods: {
    async fetchPayments() {
      try {
        this.loading = true;
        const response = await axios.get("http://localhost:8000/api/pagamentos");
        this.payments = response.data.pagamentos || [];
        this.error = null;
      } catch (error) {
        console.error("Erro ao buscar pagamentos:", error);
        this.error = "Não foi possível buscar a lista de pagamentos.";
      } finally {
        this.loading = false;
      }
    },
    getStatusClass(status) {
      switch (status.toLowerCase()) {
        case 'pago':
          return 'status-approved';
        case 'pendente':
          return 'status-pending';
        default:
          return 'status-other';
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

h2 {
  color: #572364;
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  text-align: center;
}

.btn-new {
  display: inline-block;
  background-color: #572364;
  color: #fff;
  border: none;
  padding: 0.8rem 1.2rem;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 1.5rem;
  font-family: "Poppins", sans-serif;
  text-decoration: none;
  transition: background-color 0.3s ease;
}

.btn-new:hover {
  background-color: #3f1d4b;
}

.payments-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.payments-table th,
.payments-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
}

.payments-table th {
  background-color: #fce4ff;
  color: #572364;
  font-weight: 600;
}

.payments-table tr:last-child td {
  border-bottom: none;
}

.payments-table tr:nth-child(even) {
  background-color: #f9f2fc;
}

.payments-table tr:hover {
  background-color: #f0e0f5;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-paid {
  background-color: #d1fae5;
  color: #065f46;
}

.status-pending {
  background-color: #fef3c7;
  color: #92400e;
}

.status-other {
  background-color: #fee2e2;
  color: #991b1b;
}

.loading, .error-message, .no-payments {
  text-align: center;
  padding: 2rem;
  background-color: #f9f2fc;
  border-radius: 4px;
  color: #572364;
}

.error-message {
  color: #991b1b;
  background-color: #fee2e2;
}

@media (max-width: 768px) {
  .payment-list-container {
    padding: 1rem;
  }

  .payments-table th,
  .payments-table td {
    padding: 0.75rem 0.5rem;
  }

  .btn-new {
    width: 100%;
    text-align: center;
  }
}
</style>

