---
name: hostlink-invoice-items
version: 1.0.0
description: "HostLink Invoice Items: Manage invoice line items (API resource: PaymentPeriod)."
metadata:
  openclaw:
    category: "hostlink"
    requires:
      bins: ["hostlink"]
    cliHelp: "hostlink invoice-items --help"
---

# invoice-items

> **PREREQUISITE:** Run `hostlink set-token <token>` to authenticate before using any command.

Manage line items (PaymentPeriod records) within an invoice.

> **API Note:** The CLI command is `invoice-items`, but the underlying GraphQL API resource is called `PaymentPeriod`.  
> Queries/mutations used: `listPaymentPeriod`, `addPaymentPeriod`, `updatePaymentPeriod`, `deletePaymentPeriod`.

```bash
hostlink invoice-items <command> [flags]
```

## Commands

| Command | Description |
|---------|-------------|
| `hostlink invoice-items list <invoice_id>` | List all items in an invoice |
| `hostlink invoice-items get <id>` | Get an item by ID |
| `hostlink invoice-items add` | Add an item to an invoice |
| `hostlink invoice-items update <id>` | Update an item by ID |
| `hostlink invoice-items delete <id>` | Delete an item by ID |

---

## list

```bash
hostlink invoice-items list <invoice_id> [--json]
```

```bash
hostlink invoice-items list 101
hostlink invoice-items list 101 --json
```

### Sample output

```
[55] #1 Web Hosting | qty:1 x $500 | discount:0% | total:$500
[56] #2 Domain Renewal | qty:1 x $200 | discount:10% | total:$180 | annual renewal
```

---

## get

```bash
hostlink invoice-items get <id> [--json]
```

Returns full item details including service period and linked IDs.

```bash
hostlink invoice-items get 55
hostlink invoice-items get 55 --json
```

---

## add

```bash
hostlink invoice-items add --invoice-id <id> [flags]
```

| Flag | Description |
|------|-------------|
| `-i, --invoice-id <id>` | Invoice ID *(required)* |
| `--unit-price <n>` | Unit price |
| `--qty <n>` | Quantity |
| `--unit-month <n>` | Number of months (default: 1) |
| `--free-month <n>` | Free months |
| `--discount <n>` | Discount percentage |
| `--subtotal <n>` | Subtotal (override) |
| `--remark <value>` | Remark |
| `--sequence <n>` | Display sequence order |
| `--period-from <date>` | Service period start (YYYY-MM-DD) |
| `--period-to <date>` | Service period end (YYYY-MM-DD) |
| `--clientservice-id <n>` | Client service ID |
| `--quotation-id <n>` | Linked quotation ID |

```bash
hostlink invoice-items add --invoice-id 101 --unit-price 500 --qty 1 --remark "Web Hosting"
hostlink invoice-items add --invoice-id 101 --unit-price 200 --qty 1 --discount 10 --period-from "2026-04-01" --period-to "2027-03-31"
```

Returns the new item ID on success.

---

## update

```bash
hostlink invoice-items update <id> [flags]
```

Supports all the same flags as `add` (all optional). At least one flag must be provided.

```bash
hostlink invoice-items update 55 --unit-price 600 --discount 5
hostlink invoice-items update 55 --period-from "2026-05-01" --period-to "2027-04-30"
```

---

## delete

```bash
hostlink invoice-items delete <id>
```

```bash
hostlink invoice-items delete 55
```

---

## Output Fields

| Field | Description |
|-------|-------------|
| `paymentperiod_id` | Item ID |
| `invoice_id` | Parent invoice ID |
| `sequence` | Display order |
| `description` | Item description (computed from clientService) |
| `unit_price` | Unit price |
| `qty` | Quantity |
| `free_month` | Free months |
| `discount` | Discount percentage |
| `subtotal` | Subtotal before discount |
| `total` | Final total |
| `period_from` / `period_to` | Service period |
| `remark` | Remark |
| `clientservice_id` | Linked client service ID |
| `quotation_id` | Linked quotation ID |

> **Note:** The `list` command returns `free_month`. Use the `get` command to retrieve both `unit_month` and `free_month`.
