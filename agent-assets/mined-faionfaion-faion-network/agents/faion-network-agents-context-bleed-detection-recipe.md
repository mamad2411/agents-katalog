# Context Bleed Detection Recipe

## Summary

**One-sentence:** Produces a runnable detection recipe (canary probe + embedding-distance check + tag-based audit) for context bleed across multi-tenant LLM sessions, plus a tagged incident record for each hit.

**Ефективно для:** Production LLM systems that serve multiple tenants from the same model deployment where a user can ask a benign question and recover snippets from a prior user's session, OR where stale tool output from turn N-1 silently feeds into turn N.

**One-paragraph:** Pins the recurring "is this LLM bleeding context between sessions" investigation into a deterministic recipe. The recipe injects per-session canary tokens, snapshots system-prompt + tool-call state, and runs a post-hoc embedding-distance check between adjacent sessions. Output is a tagged incident record naming (a) the bleed type (cross-tenant / prior-turn / system-drift), (b) the probe that fired, (c) the affected session ids, and (d) the recommended kill switch (session-id reset, fresh worker, prompt-cache invalidate).

## Applies If (ALL must hold)

- LLM serves at least two distinct tenants OR sessions from the same model deployment.
- A bleed-like complaint or audit finding has been opened in the last 30 days.
- The operator has session logs + system-prompt history available.
- Tier == geek or higher.
- A single accountable on-call owner can be named.

## Skip If (ANY kills it)

- Single-tenant / single-session deployment with no carry-over surface.
- Bleed already root-caused and patched — use a regression test, not this recipe.
- Provider-managed deployment where session isolation is delegated (e.g., managed agent runtime) — open vendor ticket instead.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| 24h of session logs with timestamps + session_id | jsonl | log store |
| Current system-prompt snapshot | text | prompt repo |
| List of tools the agent can call | yaml | tool registry |
| Tenant - session_id mapping | csv | auth / billing service |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `geek/ai/data-exfiltration-canary-tokens` | the canary mechanism this recipe leans on |
| `geek/ai/llm-integration` | parent operating context |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 rules: r1-canary-per-session, r2-snapshot-before-probe, r3-distance-threshold, r4-named-incident, r5-no-blast-radius-fix | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema for incident record + examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: false-positive-from-paraphrase / canary-leak / snapshot-stale / tenant-id-misjoin / overfire-killswitch | ~900 |
| `content/04-procedure.xml` | essential | 5-step probe to measure to score to classify to emit recipe | ~1000 |
| `content/06-decision-tree.xml` | essential | Bleed-type classifier branching on probe + distance + system-drift | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `inject_canary_and_snapshot` | haiku | Mechanical insertion |
| `score_embedding_distance` | sonnet | Bounded distance compute + threshold pick |
| `classify_bleed_type` | opus | Multi-signal synthesis, high consequence |

## Templates

| File | Purpose |
|---|---|
| `templates/context-bleed-detection-recipe.json` | JSON schema for the incident record output |
| `templates/context-bleed-detection-recipe.md.j2` | Markdown skeleton for the incident record |
| `templates/context-bleed-detection-recipe.md` | Markdown skeleton for the incident record Generated from `templates/context-bleed-detection-recipe.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-context-bleed-detection-recipe.py` | Enforce incident-record contract | After detector returns, before paging on-call |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[data-exfiltration-canary-tokens]] — upstream primitive.
- [[hallucination-detection-online]] — adjacent online monitor.
- Upstream playbook: `p3-llm-integration/Detect cross-session context bleed`.

## Decision tree

Lives at `content/06-decision-tree.xml`. Three-question tree: (1) preconditions present? - no = skip; yes (2) canary appeared in foreign session? - yes = cross-tenant bleed; no (3) embedding-distance between turn N and N-1 across sessions exceeds threshold? - yes = prior-turn carry-over; no = clean. Terminal branches reference rules in `content/01-core-rules.xml`.
