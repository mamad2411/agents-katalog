---
name: research-weave
description: Find and prioritize research papers for a concrete research question; reconstruct intellectual lineages, connect claims into an evidence network, and investigate conflicting findings. Use when a researcher needs to decide what to read, what prior work actually establishes, or where their project sits among competing explanations. Not for a bare bibliography, a single-paper summary, or a definitive novelty audit.
license: MIT
metadata:
  version: "1.1"
---

# Research Weave

Help the researcher decide which papers deserve attention and which research judgments they can change. Preserve scope, main conclusions, source dependence and counterevidence; do not turn fluent summaries into equally positive recommendations.

## Set the decision and effort

Extract the question, decision, target conditions and reading constraints from the request. State a working interpretation and proceed; ask only when different interpretations would materially change retrieval. Keep unknown model/task/budget assumptions explicit.

Start with **Scout** for orientation or a small reading decision. Use **Map** for a requested reusable evidence network, and **Update** for an existing map. Attention budgets follow the user's constraint, not a paper-count quota. A source-limited run can finish without live retrieval; name its missing branches.

## Discover and inspect

Search the problem and historical aliases, current mechanisms/evaluation, contrary or null findings, and relevant neighboring fields. Follow references and later challenges where accessible. Treat recall and reviews as leads; verify consequential claims in primary text. If a known seed is missed, repair the query/source/filter that missed it. This workflow does not establish comprehensive recall.

For each inspected key paper, **capture its main claim, its decisive result/proof locations, and whether that main evidence enters the ledger before selecting secondary observations**. If access or relevance prevents this, record `main_claim_omission`. Inspect both favorable and unfavorable conditions in the relevant result block. Do not replace the central result with an easier-to-quote ancillary table. Abstract-only candidates remain provisional.

A useful evidence card records the scoped claim, source/version/locator, actual result and comparator, validity limitation, and its use for this decision. Separate observation, author interpretation and analyst inference whenever making those layers of claim. Numbers need their task, metric, denominator, uncertainty and resource conditions; mark unreported details.

For deeper discovery, domain-specific validity checks or reading tradeoffs, consult [evidence-method.md](references/evidence-method.md) as needed. Scout does not require loading all references.

## Compare evidence

Use claims as analytical nodes and papers as provenance. Relationships include support, contradiction, boundary, dependency, transfer and replacement. An analyst comparison is labeled `hypothesis`; a `source_supported` edge also records the primary location supporting the relationship itself. Endpoint citations alone do not establish that relationship. They are not automatically circular reasoning either.

For each consequential proposition, align its scope and quantifier with the evidence. Keep direct support/counterevidence separate from inspected but uninformative results, context/analogy, and unverified leads. A local negative effect does not prove universal failure; a wide interval is evidence about precision, not merely a retrieval lead.

More credible, independent, applicable evidence can strengthen support. Count papers, originating result families, and independent contributions separately. Check versions, shared authors/data/code and reused results before declaring convergence; different family labels do not prove independence. Preserve possible inherited validity threats without treating them as confirmed defects.

Compare opposing findings only after aligning definitions, tasks, models, feedback access, comparators, cost, selection and uncertainty. Use `comparable_conflict`, `scope_mismatch`, `inconclusive` or `not_opposed`; do not infer conflict from noisy point estimates. For consequential unresolved questions, consult [contradictions.md](references/contradictions.md) and give alternatives, controls, distinct predictions and an outcome that would remove the motivation. No contradiction is a valid finding.

## Decide, stop and update

Return a short ordered queue with `deep_read`, `targeted_read`, `verify_access`, `defer` or `exclude`. Each item names the exact focus and the decision it could change. Spend limited deep reads on distinct consequential uncertainties, including inconvenient counterevidence.

Locate the project: inherited assumptions → established findings → unsupported step → closest competing explanation → next useful observation. Keep historical results bounded to their tested models and conditions. A gap or diagnostic experiment is not a novelty verdict.

Stop at the budget, exhausted corpus, or recorded lack of further decision change. For a live saturation claim, log `round` and changed IDs in searches; only claim two unchanged expansions when actually performed and recorded. Do not manufacture rounds for offline packets.

On updates, retain old IDs, versions and observations. Mark superseded/withdrawn claims and remove them from current direct support; a historically useful paper need not be excluded wholesale. Trace which downstream propositions and priorities change.

## Deliver proportionately

For Scout, lead with the decision and queue in a concise report. If saving a ledger, use `schema_version: 2`, `profile: scout` and only `context`, `papers`, `claims`, `reading_queue` by default. Optional propositions/edges/tensions/searches earn their place by changing the decision. Do not generate a full network to fill slots.

For a saved Scout ledger, read only [scout-format.md](references/scout-format.md) for exact field names, enums and a complete small example. The full references are for a requested Map/Update or a specific unresolved analytical question; a compact record needs no invented graph or proposition slots.

For Map/Update or rich proposition/relationship records, read [output-contract.md](references/output-contract.md). Match the user's language. Keep saved runs outside the installed skill and preserve prior runs. A small request may remain inline.

Run saved ledgers through:

```bash
python3 <skill-dir>/scripts/check_evidence.py <output-dir>/evidence.json
```

Resolve structural errors and inspect cautions. The checker validates declared data, not source meaning, logical entailment, actual independence or coverage. Reopen primary locations behind the main conclusion, top reading priorities and claimed conflicts; check at least one deferred near-match. Report unresolved semantic questions rather than forcing a zero-caution badge.
