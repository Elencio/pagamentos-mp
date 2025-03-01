<template>
  <div class="payment-detail-container">
    <header class="header">
      <h2 v-if="paymentOk" class="success-title">
        Parabéns! <span class="emoji">👏👏</span><br />
        Você tem um acordo
      </h2>
      <p v-if="paymentOk" class="alert">
        Fique ligado! Seu acordo vence dia 14/12/2020. Programe-se para garantir essa conquista!
      </p>
    </header>

    <div v-if="loading" class="loading">Carregando detalhes do pagamento...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="payment && !loading && !error" class="payment-card">
      <div class="price-section">
        <p class="valor-original">
          R$ 1.756,23 <span class="desconto">-88%</span>
        </p>
        <p class="valor-final">
          À vista por <strong>R$ {{ payment.valor.toFixed(2) }}</strong>
        </p>
      </div>

      <div class="tipo-pagamento">
        <p>Pagamento via <span class="tipo">{{ payment.tipo_pagamento }}</span></p>
      </div>

      <div v-if="payment.tipo_pagamento === 'PIX'" class="pix-section">
        <p class="pix-info">
          Escaneie o QR Code ou copie o código para pagar:
        </p>
        <img
          v-if="qrCodeBase64"
          :src="`data:image/png;base64,${qrCodeBase64}`"
          alt="QR Code"
          class="qr-code-img"
        />
        <button class="btn-action" @click="copiarQRCode">
          Copiar Código Pix
        </button>
      </div>

      <div v-else-if="payment.tipo_pagamento === 'Boleto'" class="boleto-section">
        <div class="linha-digitavel">
          <p>{{ boletoCode.content }}</p>
        </div>

        <div class="button-group">
          <button class="btn-action" @click="copiarCodigoBoleto">
            COPIAR CÓDIGO
          </button>
          <button class="btn-action" @click="baixarBoleto">
            BAIXAR BOLETO
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "PaymentDetail",
  data() {
    return {
      payment: null,
      loading: false,
      error: null,
      qrCodeBase64: null,
      boletoCode: null,
    };
  },
  computed: {
    paymentOk() {
      return this.payment && !this.loading && !this.error;
    },
  },
  methods: {
    async fetchPayment() {
      this.loading = true;
      this.error = null;
      const id = this.$route.params.id;
      try {
        const response = await axios.get(`http://localhost:8000/api/pagamentos/${id}`);
        this.payment = response.data;

        const meta = this.payment.metadados || {};

        this.qrCodeBase64 = meta.point_of_interaction?.transaction_data?.qr_code_base64 || null;
        this.boletoCode = meta.barcode || null;
      } catch (err) {
        this.error = "Não foi possível carregar os detalhes do pagamento.";
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    copiarQRCode() {
      if (this.qrCodeBase64) {
        navigator.clipboard.writeText(this.qrCodeBase64);
        alert("Código Pix copiado!");
      }
    },
    copiarCodigoBoleto() {
      const codigo = this.boletoCode.content || "12345.67891 12345.123456 12345.123456 1234567891234";
      navigator.clipboard.writeText(codigo);
      alert("Código de barras copiado!");
    },
    baixarBoleto() {
      if (this.payment.link_pagamento) {
        window.open(this.payment.link_pagamento, "_blank");
      } else {
        alert("Link do boleto não disponível.");
      }
    },
  },
  mounted() {
    this.fetchPayment();
  },
};
</script>

<style scoped>
.payment-detail-container {
  max-width: 420px;
  margin: 2rem auto;
  padding: 1.5rem;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  font-family: "Poppins", sans-serif;
  color: #333333;
}

.header {
  margin-bottom: 2rem;
  text-align: center;
}

.logos {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.price-section {
  text-align: center;
  margin-bottom: 1.5rem;
}

.valor-original {
  font-size: 1.1rem;
  color: #666;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.desconto {
  background: #FFE8EC;
  color: #FF2D55;
  font-weight: 600;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.9rem;
}

.valor-final {
  color: #9B2AAF;
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

.valor-final strong {
  font-size: 1.8rem;
  display: block;
  margin-top: 0.2rem;
}

.tipo-pagamento {
  display: flex;
  flex-direction: row;
  align-items: center;
  background: #F0FFF4;
  color: #009045;
  padding: 0.5rem;
  border-radius: 8px;
  margin: 1rem 0;
  font-size: 0.9rem;
  font-weight: 500;
}

.linha-digitavel {
  background: #F8F9FA;
  border: 1px solid #E9ECEF;
  border-radius: 8px;
  padding: 1rem;
  margin: 1rem 0;
  font-size: 0.9rem;
  color: #495057;
  word-break: break-all;
  text-align: center;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  margin-top: 1.5rem;
}

.btn-action {
  width: 100%;
  padding: 1rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-action:first-child {
  background: #F8F9FA;
  color: #9B2AAF;
  border: 2px solid #9B2AAF;
}

.btn-action:last-child {
  background: #9B2AAF;
  color: white;
}

.btn-action:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(155, 42, 175, 0.2);
}

.social-share {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #E9ECEF;
}

.social-share a {
  color: #6C757D;
  transition: color 0.2s ease;
}

.social-share a:hover {
  color: #9B2AAF;
}

/* QR Code specific styles */
.qr-code-img {
  width: 200px;
  height: 200px;
  margin: 1.5rem auto;
  display: block;
  padding: 1rem;
  background: white;
  border: 1px solid #E9ECEF;
  border-radius: 12px;
}

.pix-info {
  text-align: center;
  color: #495057;
  font-size: 0.9rem;
  margin: 1rem 0;
}

/* Loading and error states */
.loading,
.error {
  text-align: center;
  padding: 2rem;
  color: #6C757D;
}

.error {
  color: #DC3545;
}

@media (max-width: 480px) {
  .payment-detail-container {
    margin: 1rem;
    padding: 1rem;
  }

  .valor-final strong {
    font-size: 1.5rem;
  }
}
</style>

