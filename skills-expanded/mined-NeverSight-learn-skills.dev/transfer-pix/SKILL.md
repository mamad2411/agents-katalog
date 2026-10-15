---
name: transfer-pix
description: Guide for managing Pix transfers using Kobana. Use when the user wants to create, list, get, or cancel Pix transfers, manage transfer batches, or handle financial accounts. Supports both MCP tools (preferred) and REST API.
license: Complete terms in LICENSE.txt
metadata:
  author: Kobana
  version: "1.1.0"
---

# Kobana Transfer Pix Skill

Manage Pix transfers, batches, and financial accounts via Kobana.

## How It Works

This skill supports two modes of operation:

1. **MCP (preferred)** — If the `kobana-mcp-transfer` MCP server is available, use MCP tools directly. This is simpler and recommended.
2. **REST API (fallback)** — If MCP is not available, use HTTP calls to the Kobana API.

> **Rule:** Always try MCP tools first. Only fall back to the REST API if MCP tools are not available or not configured.

---

## MCP Mode

### Available MCP Tools

#### Pix Transfers
| Tool | Description |
|------|-------------|
| `list_transfer_pix` | List all Pix transfers |
| `create_transfer_pix` | Create a new Pix transfer |
| `get_transfer_pix` | Get a specific Pix transfer |
| `cancel_transfer_pix` | Cancel a pending Pix transfer |

#### Pix Transfer Batches
| Tool | Description |
|------|-------------|
| `list_transfer_batches` | List all transfer batches |
| `create_transfer_pix_batch` | Create a Pix transfer batch |
| `get_transfer_batch` | Get a specific batch |
| `approve_transfer_batch` | Approve a batch |
| `reprove_transfer_batch` | Reprove (cancel) a batch |

#### Financial Accounts
| Tool | Description |
|------|-------------|
| `list_financial_accounts` | List all financial accounts |
| `get_financial_account` | Get a specific financial account |

### Creating a Pix Transfer (MCP)

#### Step 1: Get the Financial Account UID

```
Use tool: list_financial_accounts
```

#### Step 2: Create the Pix Transfer

**Transfer by Pix Key:**
```json
{
  "amount": 150.00,
  "financial_account_uid": "018df180-7208-727b-...",
  "type": "key",
  "key_type": "email",
  "key": "recipient@example.com",
  "beneficiary": {
    "document_number": "111.321.322-09",
    "name": "João da Silva"
  },
  "external_id": "payment_12345"
}
```

**Transfer by Bank Account:**
```json
{
  "amount": 500.00,
  "financial_account_uid": "018df180-7208-727b-...",
  "type": "bank_account",
  "beneficiary": {
    "document_number": "12.345.678/0001-90",
    "name": "Company LTDA"
  },
  "bank_account": {
    "compe_number": 341,
    "agency_number": "1234",
    "agency_digit": "5",
    "account_number": "12345",
    "account_digit": "6",
    "document_number": "12.345.678/0001-90"
  },
  "scheduled_to": "2026-02-01",
  "transfer_purpose": "20"
}
```

#### Step 3: Create a Batch to Send

After creating transfers, create a batch to send them to the bank:

```
Use tool: create_transfer_pix_batch
Parameters: {
  "financial_account_uid": "018df180-7208-727b-...",
  "transfers": [
    { "uid": "019c0cbe-f018-717e-..." }
  ]
}
```

Or create new transfers directly in the batch:
```json
{
  "financial_account_uid": "018df180-7208-727b-...",
  "transfers": [
    {
      "amount": 100.00,
      "type": "key",
      "key_type": "cpf",
      "key": "111.222.333-44",
      "beneficiary": {
        "document_number": "111.222.333-44",
        "name": "João Silva"
      }
    }
  ]
}
```

#### Step 4: Check Batch Status

```
Use tool: get_transfer_batch
Parameters: { "uid": "019c0cbe-f018-717e-..." }
```

If the batch is `awaiting_approval`, approve it:
```
Use tool: approve_transfer_batch
Parameters: { "uid": "019c0cbe-f018-717e-..." }
```

### MCP Server Setup

#### Claude Code

If you installed the `kobana-agent-skills` plugin, the MCP servers are already configured. Just set the environment variable before running Claude Code:

```bash
export KOBANA_ACCESS_TOKEN="your_access_token"
claude
```

For sandbox, also set:
```bash
export KOBANA_API_URL="https://api-sandbox.kobana.com.br"
```

Or add to `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "kobana-transfer": {
      "command": "npx",
      "args": ["-y", "kobana-mcp-transfer"],
      "env": {
        "KOBANA_ACCESS_TOKEN": "your_access_token"
      }
    }
  }
}
```

#### Claude Desktop

Add to your config file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "kobana-transfer": {
      "command": "npx",
      "args": ["-y", "kobana-mcp-transfer"],
      "env": {
        "KOBANA_ACCESS_TOKEN": "your_access_token"
      }
    }
  }
}
```

> **Important:** Replace `your_access_token` with your actual Kobana API token. Claude Desktop does not support environment variable expansion (`${VAR}`) — you must paste the real token value directly.

For sandbox, add `"KOBANA_API_URL": "https://api-sandbox.kobana.com.br"` to the `env` object.

#### Remote MCP (Hosted)

```json
{
  "mcpServers": {
    "kobana-transfer": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.kobana.com.br/transfer/mcp",
        "--header",
        "Authorization: Bearer your_access_token"
      ]
    }
  }
}
```

---

## API Mode (Fallback)

### Base URLs

```
Production: https://api.kobana.com.br
Sandbox:    https://api-sandbox.kobana.com.br
```

### Authentication

```
Authorization: Bearer {your_api_token}
```

### API Endpoints Overview

#### Pix Transfers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v2/transfer/pix` | List all Pix transfers |
| POST | `/v2/transfer/pix` | Create a new Pix transfer |
| GET | `/v2/transfer/pix/{uid}` | Get a specific Pix transfer |
| PUT | `/v2/transfer/pix/{uid}/cancel` | Cancel a Pix transfer |

#### Pix Transfer Batches
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v2/transfer/batches` | List all transfer batches |
| POST | `/v2/transfer/pix_batches` | Create a new Pix transfer batch |
| GET | `/v2/transfer/batches/{uid}` | Get a specific batch |
| PUT | `/v2/transfer/batches/{uid}/approve` | Approve a batch |
| PUT | `/v2/transfer/batches/{uid}/reprove` | Reprove a batch |

### Creating a Pix Transfer (API)

**Transfer by Pix Key (Minimum Required):**
```json
POST /v2/transfer/pix

{
  "amount": 100.50,
  "financial_account_uid": "018df180-7208-727b-...",
  "type": "key",
  "key_type": "email",
  "key": "recipient@example.com",
  "beneficiary": {
    "document_number": "12.345.678/0001-90",
    "name": "Company LTDA"
  }
}
```

**Transfer by Bank Account:**
```json
POST /v2/transfer/pix

{
  "amount": 500.00,
  "financial_account_uid": "018df180-7208-727b-...",
  "type": "bank_account",
  "beneficiary": {
    "document_number": "12.345.678/0001-90",
    "name": "Company LTDA"
  },
  "bank_account": {
    "compe_number": 341,
    "agency_number": "1234",
    "agency_digit": "5",
    "account_number": "12345",
    "account_digit": "6",
    "document_number": "12.345.678/0001-90"
  },
  "scheduled_to": "2026-02-01",
  "transfer_purpose": "98",
  "external_id": "payment_2026_001",
  "tags": ["monthly", "supplier"]
}
```

### Important: Two-Step Flow

Pix transfers require a two-step process:

1. **Create Transfer** - `POST /v2/transfer/pix` creates a pending transfer
2. **Create Batch** - `POST /v2/transfer/pix_batches` sends transfers to the bank

**Creating a Batch:**
```json
POST /v2/transfer/pix_batches

{
  "financial_account_uid": "018df180-7208-727b-...",
  "transfers": [
    { "uid": "019c0cbe-f018-717e-..." }
  ]
}
```

### Batch Approval Workflow

Some financial accounts require manual approval:

1. **Batch created** - Status: `pending` or `awaiting_approval`
2. **Approve** - `PUT /v2/transfer/batches/{uid}/approve`
3. **Or Reprove** - `PUT /v2/transfer/batches/{uid}/reprove`

### Listing and Filtering

```
GET /v2/transfer/pix?status=pending&per_page=50
```

| Parameter | Description |
|-----------|-------------|
| `status` | Filter by status (pending, confirmed, rejected) |
| `registration_status` | Filter by registration status |
| `financial_account_uid` | Filter by financial account |
| `page` / `per_page` | Pagination |

---

## Common Parameters

### Required
| Parameter | Type | Description |
|-----------|------|-------------|
| `amount` | decimal | Transfer amount in BRL |
| `financial_account_uid` | string | UUID of source financial account |
| `type` | string | `key` or `bank_account` |

### For Pix Key (`type: "key"`)
| Parameter | Type | Description |
|-----------|------|-------------|
| `key_type` | string | `cpf`, `cnpj`, `email`, `phone`, `random` |
| `key` | string | The Pix key value |

### For Bank Account (`type: "bank_account"`)
| Parameter | Type | Description |
|-----------|------|-------------|
| `bank_account.compe_number` | integer | Bank COMPE code |
| `bank_account.agency_number` | string | Agency number |
| `bank_account.account_number` | string | Account number |
| `bank_account.account_digit` | string | Account check digit |

### Beneficiary
| Parameter | Type | Description |
|-----------|------|-------------|
| `beneficiary.document_number` | string | CPF or CNPJ |
| `beneficiary.name` | string | Full name or company name |

### Optional
| Parameter | Type | Description |
|-----------|------|-------------|
| `scheduled_to` | date | Schedule date (YYYY-MM-DD) |
| `transfer_purpose` | string | Purpose code (default: "98") |
| `external_id` | string | External ID for tracking |
| `custom_data` | object | Custom metadata (JSON) |
| `tags` | array | Tags for organization |

## Transfer Purpose Codes

| Code | Description |
|------|-------------|
| `20` | Supplier Payment |
| `30` | Salary Payment |
| `32` | Fees Payment |
| `90` | Benefits Payment |
| `98` | Miscellaneous Payments (default) |

## Key Types

| Type | Description | Example |
|------|-------------|---------|
| `cpf` | CPF number | `111.222.333-44` |
| `cnpj` | CNPJ number | `11.222.333/0001-44` |
| `email` | Email address | `user@example.com` |
| `phone` | Phone number | `+5511999999999` |
| `random` | Random key (EVP) | `123e4567-e89b-12d3-...` |

## Status Reference

### Transfer Status
- `pending` - Pending (initial)
- `awaiting_approval` - Awaiting approval
- `approved` - Approved
- `confirmed` - Confirmed by bank
- `rejected` - Rejected by bank
- `reproved` - Reproved (canceled before sending)

### Registration Status
- `pending` - Waiting for registration
- `requested` - Sent to bank
- `confirmed` - Confirmed at bank
- `rejected` / `failed` - Error

### Batch Status
- `pending` - Pending (initial)
- `awaiting_approval` - Awaiting approval
- `approved` - Approved
- `confirmed` - All transfers confirmed
- `reproved` - Reproved

## Best Practices

1. **Prefer MCP when available** - Simpler and more reliable
2. **Use batches for multiple transfers** - More efficient than individual transfers
3. **Set external_id** - Track transfers in your system
4. **Schedule transfers** - Use `scheduled_to` for future-dated transfers
5. **Use X-Idempotency-Key header** - Prevent duplicates (API mode)
6. **Test in sandbox** - Before production
7. **Monitor batch status** - Poll or use webhooks for status updates

## Reference Documentation

See [references/REFERENCE.md](references/REFERENCE.md) for complete documentation including all parameters, response formats, error codes, MCP tools, and API endpoints.
