---
name: pp-e-boekhouden
description: "Balance, profit & loss, and journal entries from your terminal — with local financial reports and write-safety guards the API doesn't give you. Trigger phrases: `check my e-boekhouden balance`, `book a mutation in e-boekhouden`, `e-boekhouden profit and loss`, `which invoices are still outstanding in e-boekhouden`, `use e-boekhouden`, `run e-boekhouden`."
author: "markvandeven"
license: "Apache-2.0"
argument-hint: "<command> [args] | install cli|mcp"
allowed-tools: "Read Bash"
metadata:
  openclaw:
    requires:
      bins:
        - e-boekhouden-pp-cli
---

# e-Boekhouden — Printing Press CLI

## Prerequisites: Install the CLI

This skill drives the `e-boekhouden-pp-cli` binary. **You must verify the CLI is installed before invoking any command from this skill.** If it is missing, install it first:

1. Install via the Printing Press installer. It defaults binaries to `$HOME/.local/bin` on macOS/Linux and `%LOCALAPPDATA%\Programs\PrintingPress\bin` on Windows:
   ```bash
   npx -y @mvanhorn/printing-press-library install e-boekhouden --cli-only
   ```
2. Verify: `e-boekhouden-pp-cli --version`
3. Ensure the reported install directory is on `$PATH` for the agent/runtime that will invoke this skill.

If the `npx` install fails before this CLI has a public-library category, install Node or use the category-specific Go fallback after publish.

If `--version` reports "command not found" after install, the runtime cannot see the binary directory on `$PATH`. Do not proceed with skill commands until verification succeeds.

e-Boekhouden's v1 REST API has no CLI today, only library wrappers in PHP, Rust, Node, and Python. This CLI absorbs every endpoint (all 24) and adds local financial reporting (trial balance, P&L, balance sheet, VAT summary, AR/AP aging) computed offline from your synced ledgers and mutations, plus reconciliation and safety-gated writes for a service where every mutation is a real accounting entry.

## When to Use This CLI

Use this CLI for day-to-day bookkeeping tasks against e-Boekhouden: checking balances and P&L, searching mutations and invoices, chasing overdue payments, and booking new journal entries with safety guards. It is well-suited to bookkeepers doing weekly reconciliation, accountants managing multiple client administrations, and agents automating recurring accounting checks.

**Do not use this CLI for:**
- Attaching or uploading files/receipts to invoices or mutations — no endpoint in the e-Boekhouden v1 API supports attachments; this is a real API limitation, not a missing CLI feature.
- Managing more than one administration's data in a single session — each API token is scoped to exactly one administration, so cross-administration writes require switching `EBOEKHOUDEN_API_TOKEN` between calls (see `administration overview`'s honest scoping note).
- Legally-authoritative financial reporting without review — `report profit-loss`, `report balance-sheet`, and `report vat-summary` are locally computed convenience views for day-to-day work, not a substitute for your accountant's official figures or VAT filing.

## Unique Capabilities

These capabilities aren't available in any other tool for this API.

### Safety-gated writes
- **`mutation create`** — Refuses to actually write a mutation or invoice without --confirm, and blocks an ambiguous write across multiple linked administrations unless --company names the exact target.

  _Use --dry-run to preview any mutation/invoice write, and add --confirm only once you're sure — add --company on accounts linked to more than one administration to avoid silently booking an entry into the wrong client's books._

  ```bash
  e-boekhouden-pp-cli mutation create --date 2026-01-15 --ledger-id 1300 --type 7 --description "Office supplies" --rows '[{"ledgerId":4200,"vatCode":"HOOG_INK_21","amount":25.50}]' --dry-run
  ```

### Local state that compounds
- **`invoice reconcile`** — Lists invoices with no matching payment mutation, and mutations that reference an invoice number the CLI doesn't recognize.

  _Reach for this when chasing overdue invoices — it tells you which ones genuinely have no recorded payment, not just which the UI marks outstanding._

  ```bash
  e-boekhouden-pp-cli invoice reconcile --json --select unmatchedInvoices.number,unmatchedInvoices.relationName
  ```
- **`mutation suggest`** — Suggests the ledger and VAT code most often used for past mutations with a similar description.

  _Use before booking a recurring but not-identical transaction to avoid re-deriving the right ledger/VAT code from memory every time._

  ```bash
  e-boekhouden-pp-cli mutation suggest "Office supplies - Staples" --json
  ```
- **`administration overview`** — Lists every administration linked to this API token, alongside ledger balances and outstanding invoices for the one administration this session is actually authenticated against.

  _Use this to see every administration linked to an API token plus that token's own balance/outstanding figures, instead of two separate calls._

  ```bash
  e-boekhouden-pp-cli administration overview --json
  ```
- **`relation statement`** — Full chronological history of invoices and mutations for one relation, with a computed running balance.

  _Use this to answer "has this customer actually paid what they owe" in one call instead of cross-referencing two separate lists._

  ```bash
  e-boekhouden-pp-cli relation statement 789012 --json
  ```
- **`ledger history`** — Itemized chronological mutation rows for one ledger account with a computed running balance.

  _Use this when you need to see how a specific ledger account arrived at its current balance, not just what the balance is today._

  ```bash
  e-boekhouden-pp-cli ledger history 1300 --json --select rows.date,rows.description,rows.runningBalance
  ```

## Command Reference

**administration** — Manage administration

- `e-boekhouden-pp-cli administration get` — Get all administrations managed by the authorized accountant.
- `e-boekhouden-pp-cli administration get-linked` — Get all administrations that are linked to the authorized administration.

**costcenter** — Manage costcenter

- `e-boekhouden-pp-cli costcenter create-cost-center` — Create a new cost center.
- `e-boekhouden-pp-cli costcenter delete-cost-center` — Delete a cost center.
- `e-boekhouden-pp-cli costcenter get-cost-center` — Get a cost center.
- `e-boekhouden-pp-cli costcenter get-cost-centers` — Get all cost centers.
- `e-boekhouden-pp-cli costcenter update-cost-center` — Update a cost center.

**emailtemplate** — Manage emailtemplate

- `e-boekhouden-pp-cli emailtemplate` — Get all email templates.

**invoice** — Manage invoice

- `e-boekhouden-pp-cli invoice create` — Create a new invoice.
- `e-boekhouden-pp-cli invoice get` — Search for invoices.
- `e-boekhouden-pp-cli invoice get-id` — Get an invoice.

**invoicetemplate** — Manage invoicetemplate

- `e-boekhouden-pp-cli invoicetemplate` — Get all invoice templates.

**ledger** — Manage ledger

- `e-boekhouden-pp-cli ledger create` — Create a new ledger.
- `e-boekhouden-pp-cli ledger get` — Get all ledgers.
- `e-boekhouden-pp-cli ledger get-balances` — Get the balances on all ledgers with optional filters.
- `e-boekhouden-pp-cli ledger get-id` — Get a ledger.
- `e-boekhouden-pp-cli ledger update` — Update a ledger.

**member** — Manage member

- `e-boekhouden-pp-cli member create` — Create a new member (only available to clubs or associations).
- `e-boekhouden-pp-cli member get` — Get all members (only available to clubs or associations).
- `e-boekhouden-pp-cli member get-id` — Get a member (only available to clubs or associations).
- `e-boekhouden-pp-cli member update` — Update an existing member (only available to clubs or associations).

**mutation** — Manage mutation

- `e-boekhouden-pp-cli mutation create` — Create a new mutation.
- `e-boekhouden-pp-cli mutation get` — Get all mutations.
- `e-boekhouden-pp-cli mutation get-id` — Get a mutation by id.
- `e-boekhouden-pp-cli mutation get-outstanding-invoices` — Get all outstanding invoices.

**product** — Manage product

- `e-boekhouden-pp-cli product create` — Create a new product.
- `e-boekhouden-pp-cli product delete` — Delete a product.
- `e-boekhouden-pp-cli product get` — Get all products.
- `e-boekhouden-pp-cli product get-group` — Get all product groups.
- `e-boekhouden-pp-cli product get-id` — Get a product.
- `e-boekhouden-pp-cli product update` — Update a product.

**relation** — Manage relation

- `e-boekhouden-pp-cli relation create` — Create a new relation.
- `e-boekhouden-pp-cli relation get` — Get all relations.
- `e-boekhouden-pp-cli relation get-id` — Get a relation.
- `e-boekhouden-pp-cli relation update` — Update an existing relation.

**session** — Manage session

- `e-boekhouden-pp-cli session end` — Revokes the session token.
- `e-boekhouden-pp-cli session start` — Start a new session. The response session token can be used as the `Authorization` header.

**swagger** — Manage swagger

- `e-boekhouden-pp-cli swagger get` — Get
- `e-boekhouden-pp-cli swagger list` — List

**unit** — Manage unit

- `e-boekhouden-pp-cli unit` — Get all units.


### Finding the right command

When you know what you want to do but not which command does it, ask the CLI directly:

```bash
e-boekhouden-pp-cli which "<capability in your own words>"
```

`which` resolves a natural-language capability query to the best matching command from this CLI's curated feature index. Exit code `0` means at least one match; exit code `2` means no confident match — fall back to `--help` or use a narrower query.

## Recipes

### Monday portfolio round across all clients

```bash
e-boekhouden-pp-cli administration overview --json
```

One call replaces switching between every managed administration to check balance and outstanding invoices.

### Chase real unpaid invoices, not just UI-flagged ones

```bash
e-boekhouden-pp-cli invoice reconcile --agent --select unmatchedInvoices.number,unmatchedInvoices.relationName,unmatchedInvoices.amount
```

Narrows the reconciliation report to just the fields needed to act, since invoice/mutation payloads are large.

### Suggest a ledger/VAT code for a recurring expense

```bash
e-boekhouden-pp-cli mutation suggest "Office supplies - Staples"
```

Surfaces the ledger + VAT code you've used most often for similar descriptions before you book the entry.

### Full customer payment history in one call

```bash
e-boekhouden-pp-cli relation statement 789012
```

Joins invoices and mutations for one relation with a running balance instead of cross-referencing two lists.

### See how a ledger account reached its current balance

```bash
e-boekhouden-pp-cli ledger history 1300
```

Itemized mutation history with a running balance, not just the point-in-time total the API's balance endpoint returns.

## Auth Setup

Auth is a two-step handshake: create a long-lived API token once in your e-Boekhouden account settings, then the CLI exchanges it for a short-lived session token automatically on every run — you never handle the session token yourself, and it never touches disk as a long-lived credential.

Run `e-boekhouden-pp-cli doctor` to verify setup.

## Agent Mode

Add `--agent` to any command. Expands to: `--json --compact --no-input --no-color --yes`.

- **Pipeable** — JSON on stdout, errors on stderr
- **Filterable** — `--select` keeps a subset of fields. Dotted paths descend into nested structures; arrays traverse element-wise. Critical for keeping context small on verbose APIs:

  ```bash
  e-boekhouden-pp-cli administration get --agent --select id,name,status
  ```
- **Previewable** — `--dry-run` shows the request without sending
- **Offline-friendly** — sync/search commands can use the local SQLite store when available
- **Non-interactive** — never prompts, every input is a flag
- **Explicit retries** — use `--idempotent` only when an already-existing create should count as success, and `--ignore-missing` only when a missing delete target should count as success

### Response envelope

Commands that read from the local store or the API wrap output in a provenance envelope:

```json
{
  "meta": {"source": "live" | "local", "synced_at": "...", "reason": "..."},
  "results": <data>
}
```

Parse `.results` for data and `.meta.source` to know whether it's live or local. A human-readable `N results (live)` summary is printed to stderr only when stdout is a terminal AND no machine-format flag (`--json`, `--csv`, `--compact`, `--quiet`, `--plain`, `--select`) is set — piped/agent consumers and explicit-format runs get pure JSON on stdout.

## Agent Feedback

When you (or the agent) notice something off about this CLI, record it:

```
e-boekhouden-pp-cli feedback "the --since flag is inclusive but docs say exclusive"
e-boekhouden-pp-cli feedback --stdin < notes.txt
e-boekhouden-pp-cli feedback list --json --limit 10
```

Entries are stored locally at `~/.local/share/e-boekhouden-pp-cli/feedback.jsonl`. They are never POSTed unless `E_BOEKHOUDEN_FEEDBACK_ENDPOINT` is set AND either `--send` is passed or `E_BOEKHOUDEN_FEEDBACK_AUTO_SEND=true`. Default behavior is local-only.

Write what *surprised* you, not a bug report. Short, specific, one line: that is the part that compounds.

## Output Delivery

Every command accepts `--deliver <sink>`. The output goes to the named sink in addition to (or instead of) stdout, so agents can route command results without hand-piping. Three sinks are supported:

| Sink | Effect |
|------|--------|
| `stdout` | Default; write to stdout only |
| `file:<path>` | Atomically write output to `<path>` (tmp + rename) |
| `webhook:<url>` | POST the output body to the URL (`application/json` or `application/x-ndjson` when `--compact`) |

Unknown schemes are refused with a structured error naming the supported set. Webhook failures return non-zero and log the URL + HTTP status on stderr.

## Named Profiles

A profile is a saved set of flag values, reused across invocations. Use it when a scheduled agent calls the same command every run with the same configuration - HeyGen's "Beacon" pattern.

```
e-boekhouden-pp-cli profile save briefing --json
e-boekhouden-pp-cli --profile briefing administration get
e-boekhouden-pp-cli profile list --json
e-boekhouden-pp-cli profile show briefing
e-boekhouden-pp-cli profile delete briefing --yes
```

Explicit flags always win over profile values; profile values win over defaults. `agent-context` lists all available profiles under `available_profiles` so introspecting agents discover them at runtime.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 2 | Usage error (wrong arguments) |
| 3 | Resource not found |
| 4 | Authentication required |
| 5 | API error (upstream issue) |
| 7 | Rate limited (wait and retry) |
| 10 | Config error |

## Argument Parsing

Parse `$ARGUMENTS`:

1. **Empty, `help`, or `--help`** → show `e-boekhouden-pp-cli --help` output
2. **Starts with `install`** → ends with `mcp` → MCP installation; otherwise → see Prerequisites above
3. **Anything else** → Direct Use (execute as CLI command with `--agent`)

## MCP Server Installation

Install the MCP binary from this CLI's published public-library entry or pre-built release, then register it:

```bash
claude mcp add e-boekhouden-pp-mcp -- e-boekhouden-pp-mcp
```

Verify: `claude mcp list`

## Direct Use

1. Check if installed: `which e-boekhouden-pp-cli`
   If not found, offer to install (see Prerequisites at the top of this skill).
2. Match the user query to the best command from the Unique Capabilities and Command Reference above.
3. Execute with the `--agent` flag:
   ```bash
   e-boekhouden-pp-cli <command> [subcommand] [args] --agent
   ```
4. If ambiguous, drill into subcommand help: `e-boekhouden-pp-cli <command> --help`.
