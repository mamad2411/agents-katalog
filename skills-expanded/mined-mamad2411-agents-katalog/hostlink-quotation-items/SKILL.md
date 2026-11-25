---
name: hostlink-quotation-items
version: 1.0.0
description: "HostLink Quotation Items: Manage line items within a quotation."
metadata:
  openclaw:
    category: "hostlink"
    requires:
      bins: ["hostlink"]
    cliHelp: "hostlink quotation-items --help"
---

# quotation-items

> **PREREQUISITE:** Run `hostlink set-token <token>` to authenticate before using any command.

Manage line items within a quotation. Each quotation can have multiple items. See [`../hostlink-quotations/SKILL.md`](../hostlink-quotations/SKILL.md) for managing quotations.

```bash
hostlink quotation-items <command> [flags]
```

## Commands

| Command | Description |
|---------|-------------|
| `hostlink quotation-items list <quotation_id>` | List all items in a quotation |
| `hostlink quotation-items get <id>` | Get a single item by ID |
| `hostlink quotation-items add` | Add a new item to a quotation |
| `hostlink quotation-items update <id>` | Update an item by ID |
| `hostlink quotation-items delete <id>` | Delete an item by ID |

## list

List all items belonging to a quotation.

```bash
hostlink quotation-items list <quotation_id> [--json]
```

```bash
hostlink quotation-items list 123
hostlink quotation-items list 123 --json
```

Output columns: `quotationitem_id`, `sequence`, `name`, `unit_quantity`, `unit_price`, `unit_month`, `discount`, `subtotal`

## get

```bash
hostlink quotation-items get <id> [--json]
```

```bash
hostlink quotation-items get 789
hostlink quotation-items get 789 --json
```

## add

```bash
hostlink quotation-items add --quotation-id <id> --name <name> [flags]
```

| Flag | Required | Description |
|------|----------|-------------|
| `-q, --quotation-id <id>` | ✅ | Quotation ID to add item to |
| `-n, --name <value>` | ✅ | Item name / description |
| `--unit-price <n>` | | Unit price |
| `--unit-month <n>` | | Number of months (default: `1`) |
| `--unit-quantity <n>` | | Quantity |
| `--discount <n>` | | Discount percentage (e.g. `10` for 10%) |
| `--remark <value>` | | Item remark |
| `--sequence <n>` | | Display order sequence |
| `--service-id <n>` | | Link to a service ID |
| `--domain-id <n>` | | Link to a domain ID |
| `--optional` | | Mark item as optional |
| `--accept` | | Mark item as accepted |
| `--hidden-price` | | Hide price on PDF |
| `--hidden-quantity` | | Hide quantity on PDF |
| `--hidden-number` | | Hide item number on PDF |
| `--page-break` | | Insert page break after this item |

```bash
# Add a hosting item for 12 months
hostlink quotation-items add --quotation-id 123 --name "Web Hosting" --unit-price 500 --unit-month 12 --unit-quantity 1

# Add an optional item with discount
hostlink quotation-items add --quotation-id 123 --name "SSL Certificate" --unit-price 800 --discount 10 --optional
```

## update

```bash
hostlink quotation-items update <id> [flags]
```

Supports all the same flags as `add` (except `--quotation-id`).

```bash
hostlink quotation-items update 789 --unit-price 600 --discount 15
hostlink quotation-items update 789 --name "Premium Web Hosting" --remark "Upgraded plan"
```

## delete

```bash
hostlink quotation-items delete <id>
```

```bash
hostlink quotation-items delete 789
```

## Typical Workflow

```bash
# 1. Create a quotation
hostlink quotations add --client-id 123 --client-name "ABC Ltd" --quotation-date "2026-03-20"
# → Created quotation [456]

# 2. Add items
hostlink quotation-items add --quotation-id 456 --name "Web Hosting" --unit-price 500 --unit-month 12
hostlink quotation-items add --quotation-id 456 --name "Domain Registration" --unit-price 200 --unit-month 12

# 3. Review items
hostlink quotation-items list 456

# 4. Download PDF
hostlink quotations pdf 456 --save
```
