<template>
  <div class="payment-form-container">
    <h2 class="title">Fazer Pagamento</h2>
    <form @submit.prevent="submitPayment">
      <div class="form-group">
        <label for="cliente_id">Cliente ID</label>
        <input
          type="number"
          id="cliente_id"
          v-model="clienteId"
          placeholder="Digite o ID do cliente"
          required
        />
      </div>

      <div class="form-group">
        <label for="valor">Valor (R$)</label>
        <input
          type="number"
          id="valor"
          v-model="valor"
          placeholder="Ex: 1250.88"
          min="0.01"
          step="0.01"
          required
        />
      </div>

      <div class="form-group">
        <label for="tipo_pagamento">Tipo de Pagamento</label>
        <select id="tipo_pagamento" v-model="tipoPagamento" required>
          <option value="PIX">PIX</option>
          <option value="Boleto">Boleto</option>
        </select>
      </div>

      <button type="submit" class="btn-submit">Criar Pagamento</button>
    </form>
  </div>
</template>
<script>
import axios from "axios";

export default {
  name: "PaymentForm",
  data() {
    return {
      clienteId: 1,
      valor: 100.0,
      tipoPagamento: "Boleto",
    };
  },
  methods: {
    async submitPayment() {
      try {
        const response = await axios.post(
          "http://localhost:8000/api/pagamentos",
          null,
          {
            params: {
              cliente_id: this.clienteId,
              valor: this.valor,
              tipo_pagamento: this.tipoPagamento,
            },
          }
        );

        const pagamentoCriado = response.data.pagamento;
        alert("Pagamento criado com sucesso!");
        console.log("Resposta do backend:", pagamentoCriado);

        this.$router.push({
          name: "PaymentDetail",
          params: { id: pagamentoCriado.id },
        });
      } catch (error) {
        console.error("Erro:", error.response?.data || error.message);
        alert("Ocorreu um erro ao criar o pagamento.");
      }
    },
  },
};
</script>

<style scoped>
.payment-form-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 1.5rem;
  background-color: #fce4ff;
  border: 2px solid #e5c1f6;
  border-radius: 8px;
  font-family: "Poppins", serif;
  color: #572364;
}

.title {
  text-align: center;
  margin-bottom: 1rem;
  color: #572364;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
}

.form-group label {
  margin-bottom: 0.3rem;
  font-weight: 600;
}

.form-group input,
.form-group select {
  padding: 0.5rem;
  border: 1px solid #c8a2e4;
  border-radius: 4px;
}

.btn-submit {
  background-color: #572364;
  color: #ffffff;
  font-weight: 600;
  border: none;
  border-radius: 4px;
  padding: 0.7rem 1rem;
  cursor: pointer;
  font-family: "Poppins", serif;
}
.btn-submit:hover {
  background-color: #3f1d4b;
}
</style>
