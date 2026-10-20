---
name: int-bling
description: "Bling ERP integration via API v3. Manage products, sales orders, contacts, fiscal invoices (NF-e), and stock. Use when users ask about ERP data, products, orders, contacts, invoices, or inventory from Bling. Integração com ERP Bling: produtos, pedidos, contatos, NF-e, estoque."
---

# Bling ERP Skill

Integration with Bling ERP via REST API v3 (OAuth2 Bearer).

## When to use

- List or create products, services, or kits in Bling
- Create or query sales orders
- Manage contacts (customers/suppliers)
- Issue or list fiscal invoices (NF-e)
- Check or update stock levels

## Setup

This skill uses a Python client (`scripts/bling_client.py`) that handles OAuth2 Bearer auth with **automatic refresh on 401**. You do OAuth **once** via the CLI, then the skill refreshes tokens transparently forever.

### One-time OAuth setup

1. Create an app at https://developer.bling.com.br → "Meus Apps"
2. Set the app's redirect URI to: `http://localhost:8787/callback`
3. Copy the Client ID and Client Secret into `.env`:
   ```bash
   BLING_CLIENT_ID=...
   BLING_CLIENT_SECRET=...
   ```
4. Run the login helper:
   ```bash
   make bling-auth
   ```
   This opens your browser, captures the authorization code via a local callback server, exchanges it for `access_token` + `refresh_token`, and persists both to `.env`.

After this step, `.env` contains:
```bash
BLING_CLIENT_ID=...
BLING_CLIENT_SECRET=...
BLING_ACCESS_TOKEN=...
BLING_REFRESH_TOKEN=...
```

### How the auto-refresh works

`scripts/bling_client.py` is the single entry point for all API calls. On any `HTTP 401`, it:
1. Exchanges `BLING_REFRESH_TOKEN` for a new `access_token` + `refresh_token` at `https://www.bling.com.br/Api/v3/oauth/token` (Basic auth with Client ID/Secret)
2. Persists both back to `.env` and `os.environ`
3. Retries the original request once

Bling rotates the refresh token on every refresh, so **always** use this client — never call the API with raw `curl` unless you're debugging, otherwise you risk the `.env` tokens going stale.

### Calling the client

```bash
python3 .claude/skills/int-bling/scripts/bling_client.py GET /produtos --params page=1 limit=50
python3 .claude/skills/int-bling/scripts/bling_client.py POST /contatos --body '{"nome":"Acme","tipo":"J","numeroDocumento":"12345678000100"}'
python3 .claude/skills/int-bling/scripts/bling_client.py PUT /produtos/123 --body '{"preco":99.90}'
```

The client prints the JSON response to stdout and logs errors to stderr.

---

## Base URL

```
https://www.bling.com.br/Api/v3
```

---

## Products

### List products

```bash
curl -s -X GET \
  "https://www.bling.com.br/Api/v3/produtos?pagina=1&limite=100" \
  -H "Authorization: Bearer ${BLING_ACCESS_TOKEN}"
```

**Query params:**
| Param | Type | Description |
|-------|------|-------------|
| `pagina` | number | Page number (default 1) |
| `limite` | number | Items per page (default 100, max 100) |
| `nome` | string | Filter by product name |
| `codigo` | string | Filter by SKU/code |
| `tipo` | string | `P`=Product, `S`=Service, `K`=Kit |

### Create product

```bash
curl -s -X POST \
  "https://www.bling.com.br/Api/v3/produtos" \
  -H "Authorization: Bearer ${BLING_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Widget Pro",
    "codigo": "WGT-001",
    "preco": 99.90,
    "precoCusto": 45.00,
    "tipo": "P",
    "formato": "S",
    "situacao": "A",
    "unidade": "UN"
  }'
```

**Body fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `nome` | string | yes | Product name |
| `preco` | number | yes | Sale price |
| `tipo` | string | yes | `P`=Product, `S`=Service, `K`=Kit |
| `formato` | string | yes | `S`=Simple, `E`=With variations, `V`=Variation |
| `codigo` | string | no | SKU/code |
| `precoCusto` | number | no | Cost price |
| `situacao` | string | no | `A`=Active, `I`=Inactive |
| `unidade` | string | no | Unit (UN, KG, etc.) |
| `pesoLiquido` | number | no | Net weight in kg |
| `pesoBruto` | number | no | Gross weight in kg |

---

## Sales Orders

### List orders

```bash
curl -s -X GET \
  "https://www.bling.com.br/Api/v3/pedidos/vendas?pagina=1&limite=100&dataInicial=2026-01-01&dataFinal=2026-04-10" \
  -H "Authorization: Bearer ${BLING_ACCESS_TOKEN}"
```

**Query params:**
| Param | Type | Description |
|-------|------|-------------|
| `pagina` | number | Page number |
| `limite` | number | Items per page |
| `idsSituacoes[]` | number | Filter by status ID |
| `dataInicial` | string | Start date `YYYY-MM-DD` |
| `dataFinal` | string | End date `YYYY-MM-DD` |

### Create order

```bash
curl -s -X POST \
  "https://www.bling.com.br/Api/v3/pedidos/vendas" \
  -H "Authorization: Bearer ${BLING_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "contato": { "id": 123456 },
    "data": "2026-04-10",
    "observacoes": "Test order",
    "itens": [
      {
        "produto": { "id": 789 },
        "quantidade": 2,
        "valor": 99.90,
        "desconto": 0
      }
    ]
  }'
```

**Body fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `contato.id` | number | yes | Contact (customer) ID |
| `itens` | array | yes | Order line items |
| `itens[].produto.id` | number | yes | Product ID |
| `itens[].quantidade` | number | yes | Quantity |
| `itens[].valor` | number | yes | Unit price |
| `itens[].desconto` | number | no | Discount amount |
| `data` | string | no | Order date `YYYY-MM-DD` |
| `observacoes` | string | no | Notes |

---

## Contacts

### List contacts

```bash
curl -s -X GET \
  "https://www.bling.com.br/Api/v3/contatos?pagina=1&limite=100&tipoPessoa=J" \
  -H "Authorization: Bearer ${BLING_ACCESS_TOKEN}"
```

**Query params:**
| Param | Type | Description |
|-------|------|-------------|
| `pagina` | number | Page number |
| `limite` | number | Items per page |
| `nome` | string | Filter by name |
| `tipoPessoa` | string | `F`=Individual (CPF), `J`=Legal entity (CNPJ) |

### Create contact

```bash
curl -s -X POST \
  "https://www.bling.com.br/Api/v3/contatos" \
  -H "Authorization: Bearer ${BLING_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Empresa Exemplo LTDA",
    "tipo": "J",
    "numeroDocumento": "12345678000199",
    "email": "contato@empresa.com",
    "telefone": "31999990000"
  }'
```

**Body fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `nome` | string | yes | Contact name |
| `tipo` | string | yes | `F`=Individual, `J`=Legal entity |
| `numeroDocumento` | string | no | CPF or CNPJ |
| `email` | string | no | Email address |
| `telefone` | string | no | Phone number |
| `celular` | string | no | Mobile phone |

---

## Fiscal Invoices (NF-e)

### List invoices

```bash
curl -s -X GET \
  "https://www.bling.com.br/Api/v3/nfe?pagina=1&limite=100" \
  -H "Authorization: Bearer ${BLING_ACCESS_TOKEN}"
```

**Query params:**
| Param | Type | Description |
|-------|------|-------------|
| `pagina` | number | Page number |
| `limite` | number | Items per page |
| `situacao` | number | Filter by status code |

### Create invoice (from order)

```bash
curl -s -X POST \
  "https://www.bling.com.br/Api/v3/nfe" \
  -H "Authorization: Bearer ${BLING_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "pedidoVendaId": 456,
    "tipo": 1,
    "naturezaOperacao": "Venda de mercadoria"
  }'
```

**Body fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `pedidoVendaId` | number | yes | Sales order ID to generate invoice from |
| `tipo` | number | no | Invoice type: `1`=Output (Saída), `0`=Input (Entrada) |
| `naturezaOperacao` | string | no | Operation nature description |

---

## Stock

### Get stock for a product

```bash
curl -s -X GET \
  "https://www.bling.com.br/Api/v3/estoques/saldos?idsProdutos[]=789" \
  -H "Authorization: Bearer ${BLING_ACCESS_TOKEN}"
```

### Update stock

```bash
curl -s -X POST \
  "https://www.bling.com.br/Api/v3/estoques" \
  -H "Authorization: Bearer ${BLING_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "produto": { "id": 789 },
    "deposito": { "id": 1 },
    "operacao": "E",
    "quantidade": 50,
    "observacoes": "Stock received from supplier"
  }'
```

**Body fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `produto.id` | number | yes | Product ID |
| `deposito.id` | number | yes | Warehouse/deposit ID |
| `operacao` | string | yes | `B`=Balance (set), `E`=Entry (add), `S`=Exit (subtract) |
| `quantidade` | number | yes | Quantity |
| `observacoes` | string | no | Notes |

---

## Auth Model

- **Type:** OAuth2 Bearer Token
- **Header:** `Authorization: Bearer <token>`
- **Token lifetime:** short-lived; must be refreshed using the OAuth2 refresh token flow
- **Scopes:** defined per app in the Bling developer portal

## Pagination

All list endpoints use:
- `pagina` — page number (1-indexed)
- `limite` — items per page (default 100, max 100)

Date filters use `YYYY-MM-DD` format.

## Rate Limits

Bling API v3 does not publish a hard rate limit publicly. Observed safe throughput is ~10 requests/second. Back off on HTTP 429 responses. For detailed limits, see https://developer.bling.com.br.

## Notes

- This skill is based on the MCP implementation at `workspace/projects/mcp-dev-brasil/packages/erp/bling/src/index.ts` (mcp-dev-brasil project)
- For advanced endpoints not listed here (product variations, fiscal settings, categories, etc.), consult the official docs at https://developer.bling.com.br
- The OAuth2 token management (refresh flow) is not automated by this skill — ensure `BLING_ACCESS_TOKEN` is fresh before making calls
