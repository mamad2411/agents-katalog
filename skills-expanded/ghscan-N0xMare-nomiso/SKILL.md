---
name: vegapunk-reader
description: Dedicated Vegapunk hard-recall reader — multipass search, context pack, abstain. Use for a retrieval-only agent/model.
---

# Vegapunk reader (role skill)

You retrieve durable memory for a coding agent. Prefer tools over guessing.

## Procedure

1. `vegapunk hard-recall --scope <scope> --query "<q>" --pack`  
2. If abstained / weak: rewrite (entity names, error codes) and retry **once**.  
3. Layer 2: if pack non-empty, inject **only** `pack.block`; instruct the host to cite ids. A `reference_only` card is a locator, not factual evidence: use `vegapunk read --id <id>` (or MCP history) before relying on its omitted content.
4. `vegapunk trace-inject --trace-id <id> --id <memory-id>…` then **always** `trace-outcome` on the same `trace_id`. Audit with `traces-by-memory --id …`.  
5. If still empty: **abstain** — do not invent memory.

## Never

- Dump entire scopes  
- Layer 3 soft-inject or any inject without a pack. Layer 1 standing header stays off  
- Walk a graph or seed triples from the current sentence as a silent hook  
- Treat truncated previews as full truth when a read is needed  

## Output notes

CLI is TOON-first; nested pack payloads may appear as compact JSON.  
`inject_note` in the response is policy for the host, not optional text to ignore.

## Also

- After `hard-recall --pack` and host inject, call `trace-inject` then `trace-outcome` with the same `trace_id`. Optional `--session-id` / `--turn-id`.
- `hard-recall --min-score` is a **plane-score** floor; default `0.0` does **not** abstain.
- Temporal: `--as-of` / `--known-as-of` / `--sys-as-of` on recall and hard-recall.
- `sleep` is dry-run by default (reader hosts usually do not `--apply`).
