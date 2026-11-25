---
name: frag-cost
description: Answer the load-bearing question "does clawback SESSION-KEY fragmentation actually cost Anthropic tokens?" from a finished run's per-instance turn-logs — zero new tokens. The prefix-fragmentation count (distinct SESSION KEYs per systemStableKey) tells you the cch rotation fragmented clawback's view; it does NOT tell you whether Anthropic cold-started. This does: it filters to REAL turns (mode=hash, drops keep-alive pings), partitions them into FRESH-key (sessionKey rotated vs the previous turn on the same systemStableKey stream) vs REPEAT-key, and prints mean cache_read / cache_creation / input / billable for each. If fresh-key turns read warm (read >> creation), fragmentation is NOT a valid cold-start proxy on that build and strip-ephemeral's token win is ~0 on a warm loop (the real win is eviction-regime, plus a tiny/fast clawback state file). Use after `.skills/paired` or `.skills/ab` on instance.*.ndjson; re-run on the eviction (L3 / --gap-sec 3600) arms to see where fragmentation finally bites.
---

# clawback fragmentation-cost diagnostic

`node .skills/frag-cost/scripts/frag_cost.mjs <instance.ARM.ndjson> [more.ndjson ...]`

Pass the **per-instance** turn-logs (e.g. `runs/<dir>/instance.A0.ndjson`,
`instance.A5.ndjson`), NOT the tee outputs (`A0.ndjson`/`A5.ndjson`) — only the
per-instance logs carry `systemStableKey` alongside `sessionKey` and Anthropic
`usage`. The tee body is pre-clawback and has no stable key.

## Why this exists

`.skills/bench`'s prefix-fragmentation table shows how badly the per-request
`cch` rotation split one logical context into many clawback SESSION KEYs (A0
often 100s → A5 1). That is clawback-layer fragmentation. The trap is assuming
distinct SESSION KEYs ⇒ Anthropic cold-starts. On build v2.1.145.20b they do
NOT: a fully fragmented A0 (336/336 distinct keys) still read ~92.7k tokens
**warm** on its fresh-key turns vs ~968 created (95.8×), 98.6% hit. Anthropic
serves the prefix warm despite cch rotation, so de-fragmentation buys only the
tiny creation delta (~1.8% on a tight loop), not rescued cold-starts. This skill
makes that fresh-vs-repeat cut explicit so the fragmentation count is never
mis-sold as token cost.

## Reading the output

- **fresh key (rotated)** vs **repeat key (stable)** mean usage — the decisive
  cut. `read >> creation` on fresh keys ⇒ served WARM ⇒ fragmentation is not a
  cold-start proxy on this build. `creation >> read` ⇒ fragmentation really is
  cold-starting ⇒ strip-ephemeral has token value in that regime.
- **first-in-stream** — each stream's opening turn; genuine cold-starts by
  nature (high creation), reported separately so they don't contaminate the
  fresh-vs-repeat comparison. Watch for old analyses that sampled these and
  mislabeled their natural cold-start as cch poisoning.
- **VERDICT** line states the read/create ratio and the conclusion.

## Where this sits

Static, post-hoc, zero new tokens. Run it after any `.skills/paired` or
`.skills/ab` block. Pair it with the zero-token `.skills/inspect` (static
breakpoint structure — the theoretical upper bound) to contrast prediction
(inspect) against ground truth (this).
