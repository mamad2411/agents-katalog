---
name: hyperliquid-review
description: "Journal and review Hyperliquid orders, fills, positions, funding, fees, incidents, and trading process from the exchange record. Use when an action or trade has completed, for a daily or weekly review, or when the user asks what execution cost, outcome, or control failure occurred. Read-only; not for market research, planning, or execution."
license: MIT
compatibility: "Requires read-only account history and the relevant ticket or intent record. The bundled review script needs Node.js 20 or newer."
metadata:
  version: "0.4.2"
  protocol: "hyperliquid"
---

# Hyperliquid review

Reconstruct what happened from exchange records, then grade process separately from outcome.

## Tools and resources

Read [the tool contract](references/official-tools.md) only when selecting or verifying a capability. Resolve scripts and references from this skill's directory. Related skills are optional handoffs; their absence is not permission to invent state or bypass a prerequisite.

## Task

Reconstruct one completed trade from fills, fees and funding; use the bundled arithmetic script on explicit inputs and mark any missing exchange evidence.

## Task handling

Use the existing ticket and conversation to scope the review. Ask only for missing identity or history that affects the result; complete supported accounting while marking gaps unknown. Lead with the process finding and evidence. A follow-up question does not reset the review or authorize an exchange action.

Keep the user's strategy ID/revision and separate historical simulation, forward paper records and verified live fills in summaries. Do not mix their performance series. Reuse the requested base currency and review window, explaining valuation sources. If the original risk budget is unknown, report R as unknown while completing supported cash accounting; a zero gross PnL denominator makes cost ratios undefined, not zero.

## Workflow

1. Bind the network, user account, market and DEX, review window, ticket ID, account mode, and known client order IDs.
2. Gather [review evidence](references/review-evidence.md): ticket, approvals, order status, historical and detailed open orders, fills, funding, ledger changes, positions, portfolio samples, and incident records.
3. Deduplicate fills by trade ID. Preserve maker or taker status, fee token, signed funding, partial fills, and position before each fill.
4. Compute gross PnL, fees, funding, net PnL, slippage against the ticket, holding time, protection gaps, and result in the ticket's original risk unit. Use `node scripts/review.mjs --help` for simple round-trip arithmetic.
5. Grade [process and incidents](references/process-review.md) before reading the profit or loss verdict.
6. Append facts to [the journal contract](references/journal-contract.md). Corrections are new entries, never rewrites.
7. Deliver one repeatable finding with an owner or next test. Do not produce a list nobody will act on.

## Evidence rules

- Chat shows intent. Orders and fills show exchange activity. Current account state shows what remains.
- Portfolio graphs are sampled and are not precise trade accounting.
- A missing client order ID weakens reconciliation and is itself a process finding.
- Funding is signed from the account's perspective. Do not reverse it twice.
- Mark unrealized PnL separately from realized PnL.
- Unknown or unavailable history stays unknown. Do not fill gaps from screenshots or memory.

## Process grade

Use `clean`, `minor break`, or `major break`. Major breaks include an unapproved write, material ticket drift, duplicate send on an unknown result, exposure above limits, or an unprotected position. A profitable major break remains a major break.

## Boundary

Do not recommend a new trade, modify controls to excuse an outcome, or perform any exchange write. Route new research to `hyperliquid-analyze` and any new action through a fresh plan.
