docker build -t api-pagamentos:latest .


docker run -d \
  --network minha_rede \
  -p 8000:8000 \
  -e MERCADO_PAGO_TOKEN=TEST-5053172333099584-120413-4bebf64cd9242bf4d9bd10e12f2ce517-2132155323 \
  -e DATABASE_URL="postgresql://admin:admin123@PagamentosDb:5432/pagamentosDB" \
  --name api_pagamentos \
  api-pagamentos:latest
  