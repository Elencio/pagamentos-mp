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

    <!-- Mensagens de loading ou erro -->
    <div v-if="loading" class="loading">Carregando detalhes do pagamento...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <!-- Se os dados foram carregados com sucesso -->
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

      <!-- Se for PIX, exibe a seção PIX -->
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
        <button class="btn-copy" @click="copiarQRCode">
          Copiar Código Pix
        </button>
      </div>

      <!-- Se for Boleto, exibe a nova seção editada -->
      <div v-else-if="payment.tipo_pagamento === 'Boleto'" class="boleto-section">
        <!-- “Linha Digitável” simulada ou obtida do back -->
        <div class="linha-digitavel">
          <!-- Se você tiver o valor real no backend, exiba com {{ boletoCode }} -->
          <p>{{ boletoCode || "12345.67891 12345.123456" }}</p>
          <p>{{ boletoCode ? boletoCode : "12345.123456 1234567891234" }}</p>
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
    // Busca os dados do pagamento ao montar o componente
    async fetchPayment() {
      this.loading = true;
      this.error = null;
      const id = this.$route.params.id;
      try {
        const response = await axios.get(`http://localhost:8000/api/pagamentos/${id}`);
        this.payment = response.data;

        // Exemplo: extrair dados de metadados
        const meta = this.payment.metadados || {};

        // Se PIX, extrair base64 do QR Code
        this.qrCodeBase64 = meta.point_of_interaction?.transaction_data?.qr_code_base64 || null;

        // Se Boleto, extrair a “linha digitável” ou outro campo
        // Aqui, supomos que viria em meta.barcode ou algo similar
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
      // Se você tiver a linha digitável real em `boletoCode`, copie-a
      const codigo = this.boletoCode || "12345.67891 12345.123456 12345.123456 1234567891234";
      navigator.clipboard.writeText(codigo);
      alert("Código de barras copiado!");
    },
    baixarBoleto() {
      // Se o backend retorna link_pagamento com a URL do boleto, abra em nova aba
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
  background: linear-gradient(135deg, #fff5ff, #fce4ff);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-family: "Poppins", sans-serif;
  color: #572364;
  text-align: center;
}

.header {
  margin-bottom: 1.5rem;
}

.success-title {
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
}

.emoji {
  font-size: 1.2rem;
}

.alert {
  font-size: 0.9rem;
  margin: 0.5rem 0;
  color: #009045;
}

.loading,
.error {
  font-size: 1rem;
  margin: 1rem 0;
  color: #f00;
}

.payment-card {
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.price-section {
  margin-bottom: 1rem;
}

.valor-original {
  font-size: 0.9rem;
  text-decoration: line-through;
  color: #999;
  margin-bottom: 0.3rem;
}

.desconto {
  color: #ff2d55;
  font-weight: bold;
  margin-left: 0.4rem;
}

.valor-final {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.tipo-pagamento {
  margin-bottom: 1rem;
}

.tipo {
  color: #009045;
  font-weight: 600;
}

.pix-section,
.boleto-section {
  margin-top: 1rem;
}

.pix-info,
.boleto-info {
  font-size: 0.95rem;
  margin-bottom: 0.6rem;
}

.qr-code-img {
  width: 160px;
  height: 160px;
  border: 1px solid #ccc;
  border-radius: 8px;
  margin-bottom: 0.8rem;
}

.linha-digitavel {
  background-color: #fff;
  border: 1px solid #eee;
  border-radius: 4px;
  padding: 0.8rem;
  font-size: 0.95rem;
  color: #444;
  margin-bottom: 1rem;
}

.button-group,
.boleto-buttons {
  display: flex;
  justify-content: space-between;
  gap: 0.5rem;
}

.btn-copy,
.btn-action {
  background-color: #572364;
  color: #ffffff;
  font-weight: 600;
  border: none;
  border-radius: 4px;
  padding: 0.65rem 1rem;
  cursor: pointer;
  font-family: "Poppins", sans-serif;
  width: 100%;
  transition: background-color 0.3s ease;
}
.btn-copy:hover,
.btn-action:hover {
  background-color: #3f1d4b;
}
</style>
