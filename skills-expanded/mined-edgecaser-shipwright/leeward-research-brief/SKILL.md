---
name: leeward-research-brief
description: "Produce an evidence-backed market, competitor, pricing or business-attractiveness brief. Use Leeward's installed collector when available, with bounded browsing for gaps."
---

Leeward root: `${CLAUDE_PLUGIN_ROOT}`. Read Leeward docs and run its helper scripts from that absolute path; it stands in for `<installed-root>` and `<absolute-shipwright-root>` below. If it still shows a variable name, locate the root from this file's path instead.

# Leeward Research Brief

Locate the Leeward root from this skill's path: the ancestor containing `manifest.json` and `docs/workflow-contract.md`. In a checkout this is the repository root; in a copied install it is `.codex/`; in a plugin it is the plugin root. Read that workflow contract. Resolve referenced files and helpers from that root while keeping the working directory at the user's project.

## Retrieve once

1. Reuse adequate current evidence. When fresh web evidence is needed, run the installed `scripts/collect-research.mjs` with one primary query and `--mode auto`.
2. A fallback pack, missing Node or helper, or collector failure permits available browsing tools. If browsing is unavailable too, name the gap and produce a limited draft.
3. Read `facts.json` when present, then `evidence.md` or `evidence.json`. Extraction confidence describes parsing, not source truth. Verify material facts against cited entries even at high confidence. Medium or missing confidence is provisional; low confidence is a lead only.
4. Name material gaps before targeted follow-up searches. A usable pack should not trigger a second broad pass.

The collector already classifies the query. `format-facts.mjs` and `pricing-diff.mjs` are optional conveniences. Compare only the intended packs and check currency, billing period, unit and retrieval date before treating prices as comparable.

## Synthesize

Choose the smallest fitting framework from `manifest.json`: competitive-landscape, market-sizing or pricing-strategy. Combine only when needed. Keep one primary deliverable and separate facts, assumptions and inferences. Cite material claims and state evidence limitations.

Return findings inline unless a saved artifact was requested. Mention use of the local evidence pack when applicable. A substantial brief includes an executive recommendation, evidence, tradeoffs and risks, plus Decision Frame; Unknowns & Evidence Gaps; Pass/Fail Readiness; Recommended Next Artifact. Use all six Decision Frame fields from `docs/output-standard.md`.
