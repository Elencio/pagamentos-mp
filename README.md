# Projeto de Pagamentos com Mercado Pago

Este projeto demonstra uma aplicação Fullstack utilizando **FastAPI** (backend), **Vue.js** (frontend) e a API do **Mercado Pago** para realizar pagamentos via PIX e Boleto.

## Pré-requisitos

- Docker e Docker Compose (opcional, se utilizar containers)
- Python 3.10+ (para rodar o backend localmente)
- Node.js 16+ e npm (para rodar o frontend localmente)
- Conta de desenvolvedor no [Mercado Pago](https://www.mercadopago.com.br/developers/pt/guides/) para obter a chave de acesso (Access Token)


## Configuração do Backend

1. **Variáveis de Ambiente**  
   Crie um arquivo `.env` na pasta `backend/` com:
   ```
   MERCADO_PAGO_TOKEN=<SUA_ACCESS_TOKEN_DO_MERCADO_PAGO>
   DATABASE_URL=postgresql://usuario:senha@host:porta/nome_do_banco
   ```
2. **Instale as Dependências**  
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. **Execute o Backend**  
   ```bash
   docker build -t api-pagamentos:latest .
   ```
    ```bash
   
docker run -d \
  --network minha_rede \
  -p 8000:8000 \
  -e MERCADO_PAGO_TOKEN="" \
  -e DATABASE_URL="" \
  --name api_pagamentos \
  api-pagamentos:latest
   ```

   A API estará disponível em [http://localhost:8000](http://localhost:8000).

### Endpoints Principais

- **POST /api/pagamentos** – Cria um novo pagamento (PIX ou Boleto).  
- **GET /api/pagamentos** – Lista todos os pagamentos.  
- **GET /api/pagamentos/{id}** – Retorna detalhes de um pagamento específico.

## Configuração do Frontend

1. **Instale as Dependências**  
   ```bash
   cd frontend
   npm install
   ```

2. **Execute o Frontend**  

   ```bash
   npm run dev
   ```
   O frontend estará disponível em [http://localhost:5173](http://localhost:5173).

### Telas Principais

- **PaymentFormView.vue** – Formulário para criação do pagamento.
- **PaymentDetail.vue** – Tela de visualização dos detalhes do pagamento (exibe QR code para PIX ou linha digitável/links para boleto).





  