---
name: fizko
description: |
  Use this skill whenever the user asks about tax documents, accounting data, bank movements, reconciliation, IVA, F29, facturas, compras, ventas, honorarios, obligaciones, asientos contables, or any financial/accounting data for their Chilean business. Also use it when the user asks to classify a bank movement, reconcile a movement with a document, create a journal entry, or perform any accounting action. This skill controls the `fizko` CLI (npm package) to query and act on data from the Fizko API. Use it even if the user doesn't mention "fizko" explicitly — if they're asking about their empresa's financial data or want to do something with a bank movement or tax document, this skill applies.
---

# Fizko CLI Skill

You have access to the `fizko` CLI, which communicates with the Fizko API for Chilean tax and accounting data.

## Setup check

Before running any command, verify the CLI is ready:

```bash
fizko status
```

If the output says "No autenticado", tell the user to run `fizko login` and wait for them. If `fizko` is not found, tell them to run `npm install -g fizko-cli`.

The status output also shows the active company. If it says "Sin empresa activa", handle it as described below.

## Active company

Almost every command needs a company context. The CLI resolves it automatically in this order:

1. `--company <uuid>` flag (explicit override for this command only)
2. Saved active company (`fizko companies use <uuid>` sets this persistently)
3. Auto-activate if the user has exactly 1 company

If none of the above apply, the command fails with an error asking to run `fizko companies use <uuid>`.

**When there's no active company** and the user has multiple companies:
```bash
fizko companies list          # show available companies
fizko companies use <uuid>    # activate one persistently
```

Once activated, all subsequent commands work without `--company`. You don't need to ask again during the conversation.

**To check or change the active company:**
```bash
fizko companies active        # show current active company
fizko companies use <uuid>    # switch to a different company
```

## Command reference

### Companies
```bash
fizko companies list
fizko companies get <uuid>
fizko companies use <uuid>    # activate as default
fizko companies active        # show current active company
```

### Tax documents
```bash
# Lists (paginated) — --company optional if active company is set
fizko tax purchases [--period-year 2026] [--period-month 1] [--document-type 33]
fizko tax sales [--period-year 2026] [--period-month 1] [--document-type 33]
fizko tax honorarios [--period-year 2026] [--period-month 1]
fizko tax documents [--period 2026-01] [--start-date 2026-01-01] [--end-date 2026-01-31]
fizko tax documents-summary              # count by type, last 3 months
fizko tax contacts                       # suppliers and clients

# Individual records
fizko tax purchase <uuid>
fizko tax sale <uuid>
fizko tax document <uuid>

# F29 and tax forms
fizko tax f29 [--year 2026]
fizko tax f29-codes --period 2026-01
fizko tax f29-export --code <code> --period 2026-01
fizko tax summary --period 2026-01
fizko tax iva --period 2026-01
fizko tax timeline
fizko tax ddjj [--year 2025]

# Checkers (discrepancy analysis)
fizko tax checker-tributario --period 2026-01   # SII book vs Fizko
fizko tax checker-impuestos --period 2026-01    # F29 declared vs Fizko
```

### Accounting
```bash
# Plan de cuentas y asientos — --company opcional si hay empresa activa
fizko accounting accounts [--tree]
fizko accounting journal-entries [--period 2026-01]
fizko accounting journal-entry <uuid>
fizko accounting progress [--period 2026-01]

# Reportes financieros
fizko accounting balance-report --period-from 2026-01 --period-to 2026-12 [--cost-center-id <uuid>]
fizko accounting income-statement --period-from 2026-01 --period-to 2026-12 [--cost-center-id <uuid>]
fizko accounting general-journal --period 2026-01 [--page <n>] [--page-size <n>]
fizko accounting general-ledger --period-from 2026-01 --period-to 2026-12 [--account-id <uuid>]
fizko accounting classified-balance [--period 2026-12] [--period-from 2026-01 --period-to 2026-12]
fizko accounting rli-balance --period-from 2026-01 --period-to 2026-12

# Centros de costo
fizko accounting cost-centers

# Obligaciones (cuentas por pagar/cobrar)
# --status: pending, partial, paid, overdue
# --obligation-type: payable, receivable
# --source-document-type: sales_document, purchase_document, honorarios_receipt, payroll_period, form29
fizko accounting obligations [--status pending] [--obligation-type payable] [--source-document-type purchase_document] [--search texto] [--from 2026-01-01] [--to 2026-01-31] [--conciliado true|false] [--contabilizado true|false]
fizko accounting obligation <uuid>

fizko accounting suggest-lines <uuid>            # sugerencia de líneas de asiento
fizko accounting contabilizar <uuid> [--lines '[{"account_code":"5101","debit":1000,"credit":0}]'] [--account-code 5101] [--description "texto"]
fizko accounting update-journal <uuid> --lines '[...]' [--description "texto"]
fizko accounting descontabilizar <uuid>

fizko accounting abonar <uuid> --amount 50000 --payment-type cash [--notes "texto"] [--no-contabilizar]
  # payment-type: cash, check, third_party, international, factoring, bad_debt
fizko accounting payments <uuid>                 # listar abonos de una obligación
fizko accounting reverse-payment <uuid> --payment-id <uuid>

fizko accounting set-cost-center <uuid> --cost-center <uuid>
fizko accounting sync [--period 2026-01] [--obligation-type payable] [--force]
```

### Banking (movimientos bancarios)
```bash
# Read — --company opcional si hay empresa activa
# --status: pending, reconciled, matched, split
# --classification-status: classified | unclassified
fizko banking movements [--status pending] [--classification-status unclassified] [--type abonos|cargos] [--search texto] [--from 2026-01-01] [--to 2026-01-31] [--period 2026-01] [--bank-account <uuid>]
fizko banking movement <uuid>
fizko banking list-reconciliations [--period 2026-01]
fizko banking suggestions --movement-id <uuid>
fizko banking status [--period 2026-01]

# Clasificación
fizko banking classify <uuid> --classification 'Gasto Operacional' [--document-type 'Factura'] [--contact-id <uuid>] [--comment "texto"]
fizko banking update <uuid> [--category texto] [--comment texto] [--cost-center <uuid>] [--pin true|false]
fizko banking bulk-classify --movement-ids UUID1,UUID2 --classification 'Gasto Operacional'

# Splits
fizko banking split <uuid> --splits '[{"amount":1000,"description":"texto"},...]'

# Contabilización
fizko banking contabilizar <uuid> --account-code 5101 [--description "texto"]
fizko banking contabilizar-reconciliaciones <uuid> --entries '[{"reconciliation_id":"UUID","lines":[{"account_code":"5101","debit":1000,"credit":0}]}]'
fizko banking update-journal <uuid> --lines '[...]' [--description "texto"]
fizko banking descontabilizar <uuid>

# Conciliación
fizko banking reconcile --movement-id <uuid> --obligation-id <uuid> [--amount 50000] [--notes "texto"]
fizko banking reconcile-multi --movement-id <uuid> --obligation-ids UUID1,UUID2
fizko banking unmatch <reconciliation-uuid>
fizko banking obligation-from-movement <uuid> [--classification 'Gasto Operacional'] [--obligation-type payable]
```

## Handling output

All commands return JSON. When presenting results to the user:

- **Lists**: Show a summary table with the most relevant fields, not the raw JSON dump. For bank movements show date, description, amount, status.
- **Single records**: Show the key fields the user likely cares about, and mention there's more detail available if they want.
- **Errors**: If a command exits with an error (stderr), explain what went wrong in plain language and suggest the fix.
- **Pagination**: If results show a `count` much larger than `results`, let the user know there are more pages and offer to fetch them with `--offset`.

## Common workflows

### "¿Cuánto IVA debo este mes?"
1. `fizko tax iva --period YYYY-MM`
2. Show debito, credito, and balance clearly.

### "Muéstrame los movimientos bancarios pendientes"
1. `fizko banking movements --status pending`
2. Show a table with date, description, amount. Offer to classify or reconcile any of them.

### "Concilia este movimiento con su factura"
1. If user gives movement ID and obligation ID: `fizko banking reconcile --movement-id <uuid> --obligation-id <uuid>`
2. If user only gives movement ID: `fizko banking suggestions --movement-id <uuid>` to show candidates, then reconcile after confirmation.
3. If no matching obligation exists: `fizko banking obligation-from-movement <uuid>`

### "Contabiliza este movimiento"
1. `fizko accounting accounts` if user doesn't know the account code.
2. `fizko banking contabilizar <uuid> --account-code <code>`

### "Contabiliza las reconciliaciones de este movimiento"
1. `fizko banking movement <uuid>` to see the reconciliations and their IDs.
2. `fizko banking contabilizar-reconciliaciones <uuid> --entries '[{"reconciliation_id":"UUID","lines":[...]}]'`

### "Contabiliza esta obligación"
1. `fizko accounting suggest-lines <uuid>` to get the suggested account lines.
2. `fizko accounting contabilizar <uuid> --lines '<suggested lines>'`

### "¿Cómo vamos con la contabilidad de enero?"
1. `fizko accounting progress --period YYYY-MM`
2. Show booked vs pending counts.

### "Sincronizar obligaciones"
1. `fizko accounting sync [--period YYYY-MM]`

## Tips

- Use `--compact` flag when you need to parse the output programmatically (no indentation).
- Period format is always `YYYY-MM` (e.g., `2026-01`).
- When the user says "este mes" or "el mes pasado", calculate the actual period before running the command.
- UUIDs: if the user pastes a partial UUID or a name instead of UUID, run `companies list` or the relevant list command to find the right ID.
- `fizko accounting contabilizar` without `--lines` auto-generates the journal entry; use `suggest-lines` first to see what lines the system recommends.
- `fizko accounting cost-centers` lists the available cost centers (needed before using `--cost-center-id`).
