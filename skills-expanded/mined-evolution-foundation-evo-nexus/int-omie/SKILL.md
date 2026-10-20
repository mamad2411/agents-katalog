---
name: int-omie
description: "Omie ERP integration via API. Manage clients, products, orders, invoices (NF-e), financials (accounts receivable/payable), and stock. Use when users ask about ERP data, financials, orders, invoices, stock, or clients from Omie. Also handles webhooks for real-time events."
---

# Omie ERP Skill

Integration with Omie ERP via REST API.

## Setup

Requires environment variables:
```bash
export OMIE_APP_KEY="your_app_key_here"
export OMIE_APP_SECRET="your_app_secret_here"
```

## API Client

Use the Python script for all operations:

```bash
python3 skills/omie/scripts/omie_client.py <command> [args]
```

### Available commands

#### Clients
```bash
python3 scripts/omie_client.py clientes_listar [pagina] [por_pagina]
python3 scripts/omie_client.py clientes_buscar cnpj_cpf=00.000.000/0001-00
python3 scripts/omie_client.py clientes_buscar codigo=1234567
python3 scripts/omie_client.py clientes_detalhar codigo=1234567
```

#### Products
```bash
python3 scripts/omie_client.py produtos_listar [pagina] [por_pagina]
python3 scripts/omie_client.py produtos_detalhar codigo=1234567
```

#### Sales Orders
```bash
python3 scripts/omie_client.py pedidos_listar [pagina] [por_pagina]
python3 scripts/omie_client.py pedidos_detalhar numero=1234
python3 scripts/omie_client.py pedidos_status numero=1234
```

#### Financials
```bash
python3 scripts/omie_client.py contas_receber [pagina] [por_pagina]
python3 scripts/omie_client.py contas_pagar [pagina] [por_pagina]
python3 scripts/omie_client.py resumo_financeiro
```

#### Invoices
```bash
python3 scripts/omie_client.py nfe_listar [pagina] [por_pagina]
python3 scripts/omie_client.py nfe_detalhar numero=1234
```

#### Stock
```bash
python3 scripts/omie_client.py estoque_posicao [pagina] [por_pagina]
python3 scripts/omie_client.py estoque_produto codigo=1234567
```

## Webhook

Omie can send events to an HTTP endpoint. Configure at:
Omie → Settings → Integrations → Webhooks

Supported events:
- `pedido.incluido` / `pedido.alterado`
- `nfe.emitida` / `nfe.cancelada`
- `financas.recebido` / `financas.pago`
- `cliente.incluido` / `cliente.alterado`

To start the webhook receiver:
```bash
python3 scripts/omie_webhook.py --port 8089
```

## API Limits
- **Rate limit:** 3 requests/second per app
- **Pagination:** maximum 500 records per page
- **Timeout:** 30 seconds
