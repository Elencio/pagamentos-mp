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

      <button type="submit" class="btn-submit" :disabled="isSubmitting">
        {{ isSubmitting ? 'Processando...' : 'Criar Pagamento' }}
      </button>
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
      isSubmitting: false,
    };
  },
  methods: {
    async submitPayment() {
      if (this.isSubmitting) return;

      this.isSubmitting = true;
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
      } finally {
        this.isSubmitting = false;
      }
    },
  },
};
</script>

<style scoped>
.payment-form-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #ffffff;
  border: 2px solid #e5c1f6;
  border-radius: 12px;
  font-family: "Poppins", sans-serif;
  color: #572364;
  box-shadow: 0 4px 10px rgba(87, 35, 100, 0.1);
}

.title {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #572364;
  font-size: 1.8rem;
  font-weight: 600;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.2rem;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #572364;
}

.form-group input,
.form-group select {
  padding: 0.7rem;
  border: 1px solid #c8a2e4;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #572364;
  box-shadow: 0 0 0 3px rgba(87, 35, 100, 0.1);
}

.btn-submit {
  width: 100%;
  background-color: #572364;
  color: #ffffff;
  font-weight: 600;
  border: none;
  border-radius: 6px;
  padding: 0.9rem 1rem;
  cursor: pointer;
  font-family: "Poppins", sans-serif;
  font-size: 1rem;
  transition: background-color 0.3s ease, transform 0.1s ease;
  margin-top: 0.5rem;
}

.btn-submit:hover {
  background-color: #3f1d4b;
}

.btn-submit:active {
  transform: translateY(1px);
}

.btn-submit:disabled {
  background-color: #a78eb4;
  cursor: not-allowed;
}

@media (max-width: 480px) {
  .payment-form-container {
    padding: 1.5rem;
    margin: 1rem;
  }

  .title {
    font-size: 1.5rem;
  }

  .form-group input,
  .form-group select,
  .btn-submit {
    font-size: 0.9rem;
  }
}
</style>

