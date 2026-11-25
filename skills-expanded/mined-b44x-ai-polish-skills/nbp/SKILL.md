---
name: nbp
display_name: Narodowy Bank Polski (NBP)
version: 1.0.0
description: >-
  Fetch official exchange rates, calculate tax conversions for foreign currency invoices,
  and check gold prices from Narodowy Bank Polski (NBP). Get current or historical average
  rates (Table A & B) for EUR, USD, GBP, CHF, etc. Calculate foreign currency invoices in
  PLN according to Polish tax law (Art. 31a ustawy o VAT / Art. 11a ustawy o PIT) by
  automatically looking up the official NBP rate from the last business day preceding the
  invoice date. Convert between any currency pairs. Get official gold prices per gram and
  troy ounce. Use whenever the user asks about "kurs euro", "kurs dolara", "tabela NBP",
  "kurs do faktury", "przelicz walutę NBP", "cena złota NBP", or foreign invoice conversion.
category: finance
language: pl
country: PL
license: MIT
author: Michell Hoduń (https://github.com/b44x)
repository: https://github.com/b44x/ai-polish-skills
network: true
authentication: none
source: Narodowy Bank Polski
source_type: official_api
official: true
homepage: https://nbp.pl
documentation: https://api.nbp.pl/
rate_limit: fair use
last_verified: 2026-09-28
tags:
  - nbp
  - waluty
  - kursy-walut
  - euro
  - dolar
  - podatki
  - vat
  - zloto
  - faktury
compatibility: Python 3.8+ (standard library only); network access to api.nbp.pl.
---

# Narodowy Bank Polski (NBP)

Fetches official currency exchange rates and gold prices from Narodowy Bank Polski using
`scripts/nbp.py`. Always outputs structured JSON.

## Running the script

Run from this skill's directory (or use relative path from repo root):

| OS | Command |
|---|---|
| Linux / macOS | `python3 scripts/nbp.py <command> …` |
| Windows | `py scripts/nbp.py <command> …` (or `python`) |

Zero external dependencies required (standard library only).

## Workflow

1. **Foreign Currency Invoices (Tax conversion):**
   - Whenever the user asks to convert an invoice or calculate VAT/income tax for a foreign currency:
     `python3 scripts/nbp.py invoice <amount> <currency> <invoice_date>`
     *Example:* `python3 scripts/nbp.py invoice 1500 EUR 2026-09-28`
   - The script automatically locates the official NBP table published on the **last business day preceding the invoice date** (skipping weekends and holidays) in accordance with Art. 31a ust. 1 Ustawy o VAT.
   - Always report the `tableNumber`, `taxEffectiveDate`, `exchangeRate`, and `amountPln`.

2. **Single Currency Rate:**
   - User asks for the current or historical rate of a currency (e.g. "ile kosztuje euro dzisiaj?"):
     `python3 scripts/nbp.py rate EUR`
     `python3 scripts/nbp.py rate USD --date 2026-09-15`

3. **General Currency Conversion:**
   - Convert arbitrary amounts between currencies:
     `python3 scripts/nbp.py convert 250 USD EUR`

4. **Gold Price:**
   - User asks for gold prices:
     `python3 scripts/nbp.py gold`
   - Returns official NBP price per 1 gram and calculated per troy ounce (oz) in PLN.

5. **Full Tables:**
   - List all rates from Table A (major) or B (exotic):
     `python3 scripts/nbp.py table A`

## Commands

| Command | Description | Returns |
|---|---|---|
| `invoice <amount> <currency> <date>` | Convert invoice to PLN according to Polish tax law (preceding business day) | `invoiceDate`, `taxEffectiveDate`, `tableNumber`, `exchangeRate`, `amountPln`, `legalBasis` |
| `rate <currency> [--date D]` | Get mid exchange rate for currency (Table A or B) | `currency`, `mid`, `tableNumber`, `effectiveDate` |
| `convert <amount> <from> <to> [--date D]` | Convert between any two currencies | `amount`, `convertedAmount`, `effectiveRate`, `date` |
| `table [A\|B\|C] [--date D]` | Fetch complete exchange rates table | `tableNumber`, `effectiveDate`, `rates` list |
| `gold [--date D]` | Get official gold price in PLN (per gram and troy ounce) | `pricePerGramPln`, `pricePerTroyOuncePln`, `priceFormatted` |

Field reference and statutory tax rules: [references/output.md](references/output.md).

## Exit codes

JSON goes to stdout; errors go to stderr as `{"error": "...", "type": "..."}`.

| Code | Meaning | What to do |
|---|---|---|
| `0` | Success | Use the JSON output |
| `2` | Not found | Invalid currency code or date out of range / holiday |
| `64` | Bad usage / validation | Invalid date format (expected YYYY-MM-DD) or missing arguments |
| `69` | Network / NBP server error | Retry once; check internet connection |

## Rules

- For tax and invoicing questions, always use `invoice` rather than `rate` — Polish tax law strictly forbids using the rate from the same day as the invoice.
- Cite the official `tableNumber` (e.g. `187/A/NBP/2026`) in your answer to ensure full legal audit compliance.
