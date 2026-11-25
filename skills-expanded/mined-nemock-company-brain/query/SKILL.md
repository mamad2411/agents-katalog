---
name: query
description: Answer questions against a company-brain vault using staged retrieval, auto-injected pillars, typed edge traversal, and node-id citations. Profile-aware. Cites the graph as the source of truth; flags contradictions, staleness, and confidence.
---

# query

This skill answers questions by reading the typed graph in a company-brain vault. You are the retrieval analyst; the vault is the source of truth.

The pattern follows the Infinite Brain retrieval analyst convention, adapted for a multi-product, multi-stakeholder company graph:

1. Auto-inject the relevant pillars before reasoning about the user's question.
2. Select candidate nodes by summary relevance, type, confidence, recency.
3. Expand the candidate set by walking typed edges.
4. Answer with node-id citations. Every claim names the node it comes from.
5. Flag staleness, contradictions, and low confidence explicitly.

You do not invent facts. If the vault does not contain the answer, say so — and offer to capture the gap with the `intake` skill rather than guessing.

## Before any question

Do these first when the skill is invoked:

1. **Confirm the vault path.** Default: current working directory. Resolve to absolute. Refuse if the path has no `_system/PROFILE.md`.
2. **Load the active schema.** Run:
   ```
   cb describe-profile --path <vault>
   ```
   The returned JSON tells you the active profile, controlled-document-footer policy, and the full list of `active_node_types`. The profile decides which node folders even exist.
3. **Load the pillar set.** Run:
   ```
   cb list-nodes --path <vault> --auto-inject-only
   ```
   This returns every pillar with `auto_inject: true` plus its `applicable_when` string. These are the governing principles of the company. Skim them up front. They will shape your answer even when the user's question is narrow.

## Staged retrieval

### Stage A — auto-inject relevant pillars

Each pillar carries an `applicable_when` field listing the topics it governs (e.g. `"pricing, business model, pad, disposable, recurring revenue"`). Match the user's question against `applicable_when` strings; load the body of any pillar that matches. These pillars are *facts about how this company thinks* — they govern the answer even when not explicitly cited by the user.

Non-goal pillars matter as much as positive ones. If the user asks "should we consider X?", a non-goal pillar that forbids X is the answer.

### Stage B — candidate node selection

Run a focused `cb list-nodes` per the question's shape:

```bash
# Topic-specific entities
cb list-nodes --path <vault> --type competitor
cb list-nodes --path <vault> --type decision --namespace product-strategy
cb list-nodes --path <vault> --type indication-for-use   # medical-device profile
cb list-nodes --path <vault> --type requirement
cb list-nodes --path <vault> --type fact

# Sources by kind
cb list-nodes --path <vault> --type source --source-kind customer-interview
cb list-nodes --path <vault> --type source --source-kind fda-510k-summary
```

From the returned summaries, pick the candidates that match the question. Be conservative — better to fetch 5 nodes that matter than 50 that mostly don't.

Selection criteria, in roughly this priority order:
- **Summary relevance.** The `summary` field is one line and tells you whether to load the full body.
- **Type fit.** A "what are our pricing principles" question wants pillars and decisions, not facts.
- **Confidence.** Below ~0.5 should be flagged as low-confidence in the answer; below 0.3 is usually not worth loading unless the user asked specifically about that node.
- **Recency.** `verified_at` matters for time-sensitive types (metrics' fact snapshots, competitor IFUs, regulatory clearances).
- **Staleness signal.** If `staleness_signal` is set and the described condition has plausibly occurred, flag it.

### Stage C — fetch full nodes

For each selected candidate, load the full node:

```
cb get-node <id> --path <vault>
```

This returns the full frontmatter, the body, the outbound edges, and crucially the *inbound* edges other nodes point at it. Inbound edges are what make graph walks cheap.

### Stage D — typed edge walk

Walk one hop at a time. The typed edges tell you which direction to walk for which question:

- `derived_from` — "where does this claim come from?" Walk to the source. The source's `source_kind` is the credibility label.
- `supports` — "what is this node arguing for / against?"
- `contradicts` — surface both sides if you find one; never silently pick a side.
- `preceded_by` / `followed_by` — IFU history chains and 510(k) predicate chains. Walk the chain to answer "how did this evolve" or "what is the substantial-equivalence path."
- `depends_on`, `part_of` — structural relationships; useful for impact-of-change questions.
- `related_to` — weakly typed; treat as a hint, not a load-bearing claim.

Stop walking when you have enough to answer cleanly. Two hops is usually enough; three hops is a sign the question is broader than you thought.

### Stage E — write the answer

Format the answer with **inline node-id citations** in square brackets:

> Our pricing is monthly because the disposable pad is the recurring-revenue engine [pillar-disposable-pad-business-model], which depends on a 7-day wear cycle [decision-003-7-day-wear-not-14-day]. This is a strategy-level commitment, not a price experiment.

Citation rules:
- Every load-bearing claim names the node it comes from. Uncited prose is editorializing; use it sparingly and mark it as your inference.
- Source-derived claims should also note the `source_kind` in parentheses when it changes the credibility of the claim — e.g. "(founder-vision)" vs "(fda-510k-summary)" vs "(customer-interview)".
- If a claim is vision-driven (`derived_from` a `founder-vision` / `strategic-thesis` / `domain-expertise` source), flag it: this is a bet the company is making, not a measured fact.
- If a claim is evidence-driven (`market-data`, `internal-data`, `customer-interview`, `fda-510k-summary`), it's grounded in something checkable.

This distinction matters more than the binary "we know X." A vision-driven claim acted on too late is failure; an evidence-driven claim treated as faith is also failure.

## What to flag explicitly

- **Low confidence.** `confidence < 0.5` → say so. Don't quietly average.
- **Stale.** `verified_at` more than a year old on a `medium`/`high`-volatility-class metric snapshot → flag. Same for any node whose `staleness_signal` condition plausibly holds.
- **Contradictions.** If two nodes contradict (either via explicit `contradicts` edges or by your reading), surface both with their citations. Don't pick a winner.
- **Profile-restricted answers.** If the user asks about an IFU and the active profile isn't medical-device, the vault has no IFU nodes — explain the profile gap, don't invent.
- **Missing answer.** If no nodes match the question well, say so. Offer to capture the gap via `intake` (e.g. a fresh `question` node, a `customer-interview` source, a missing `competitor`).

## Auto-injection details

Pillars are *governing principles*. Auto-injection means: load them into your reasoning context even when the user did not name them. Two patterns:

1. **Topic-driven injection.** Match the user's question against each pillar's `applicable_when` string. If any token matches, inject that pillar.
2. **Negative-space injection.** Always check non-goal pillars even when the user's question is positive. A user asking "what's our pediatric plan?" deserves to know if `pillar-no-pediatric-use` exists.

A pillar that fires should appear in the answer's citations.

## Multi-question sessions

The user may ask several questions in one session. Reuse the loaded pillar set and node summaries — don't re-run `describe-profile` and `list-nodes` per question. Re-run only when the user moves into a new topic area that wasn't in your original candidate set.

## What this skill does NOT do

- Does not write to the vault. For capturing answers, use `intake`. For ingesting source documents, use `atomize`. For generating planning documents, use `doc-generate`.
- Does not modify `_system/*.md`.
- Does not bypass the controlled-document boundary. If asked to draft a controlled record, refuse and explain — company-brain produces planning artifacts only.

## What to do when something goes wrong

- **`cb list-nodes` returns very few results.** The vault may be sparse, the filter may be too tight, or the namespace may not exist. List without filters and re-pick.
- **An edge target does not resolve.** The validator catches this; you can ignore the broken edge in your answer but flag it to the user so they know the vault needs repair (`cb validate` will list it).
- **The user asks for a node type the profile does not enable.** Explain which profile would activate it; don't invent the node.
- **The user disagrees with your answer.** Re-read the cited nodes. Often the answer is right but the citations need to be expanded. Sometimes the vault contradicts the user's expectation — say so plainly and let them decide whether to update the vault.
