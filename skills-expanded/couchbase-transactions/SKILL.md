---
name: couchbase-transactions
description: "Design and implement Couchbase distributed ACID transactions across multiple documents. Use whenever the user asks about transactions, multi-document atomicity, ACID, transaction library, TransactionAttemptContext, commit, rollback, transaction retry, Active Transaction Records (ATRs), transaction expiry, transaction lost write, transaction conflict, transaction performance, cb_transaction_run, or 'how do I atomically update multiple documents.' Distinct from couchbase-app-integration (which covers single-document KV ops, subdocument ops, and has a brief transactions overview) — this skill is for users who need the full depth: designing around transactions, understanding the two-phase commit mechanics, debugging failures, and tuning performance. Use proactively when the user has a use case requiring consistency across multiple documents."
license: MIT
---

# Couchbase Distributed Transactions

A skill for *designing and implementing* multi-document ACID transactions in Couchbase. Goes deeper than the overview in `couchbase-app-integration/references/transactions-app-side.md`.

Distinct from:
- `couchbase-app-integration` — general SDK patterns; has a transactions overview but not the depth needed for production transaction design
- `couchbase-mcp` — the `cb_transaction_run` tool for running transactions via the MCP server

## When this skill applies

- "How do I atomically update multiple documents?"
- "How do transactions work under the hood?"
- "My transaction is retrying — why?"
- "How do I handle a transaction conflict?"
- "What happens if the client crashes mid-transaction?"
- "Transactions are slow — how do I tune them?"
- "What are ATRs and why does my bucket have them?"
- "How do I model data to minimize transaction use?"

## Pick the right reference

| Question | Read |
|---|---|
| "When should I use transactions vs single-doc ops vs subdoc?" | `references/when-to-use.md` |
| "How do they work? ATRs, two-phase commit, retry, expiry" | `references/mechanics.md` |
| "Code patterns — Python, Java, Node; error handling; retry logic" | `references/patterns.md` |

## Core principle: try to design around transactions

Transactions in Couchbase are meaningfully slower than equivalent single-document KV operations — they do substantially more work (staging, two-phase commit across documents, Active Transaction Record bookkeeping, and possible retries) — and add retry complexity. Before reaching for a transaction, ask: can this be modeled as a single-document update? Often the answer is yes. See `references/when-to-use.md` for the decision framework.

When you do need transactions, they're correct and reliable — just plan for the cost.

## Quick tool map

| Task | Tool |
|---|---|
| Run a transaction via MCP | `cb_transaction_run` |
| Single-document atomic op (no transaction needed) | `cb_mutate_in` |
| Check for orphaned ATR documents | `cb_query` on `_txn:atr-*` keys |

## Related skills

- `couchbase-app-integration` — SDK setup and the single-document operations that transactions wrap
- `couchbase-data-modeling` — modeling decisions that reduce the need for transactions
- `couchbase-mcp` — `cb_transaction_run` for executing transactions via the MCP server
