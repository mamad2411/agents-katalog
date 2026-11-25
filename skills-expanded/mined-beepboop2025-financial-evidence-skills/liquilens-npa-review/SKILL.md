---
name: liquilens-npa-review
description: Review a covered Indian bank's disclosed NPAs, capital ratios and NPA stock movements with LiquiLens. Use for bank filing research, including Cosmos Co-operative Bank.
---

Use LiquiLens at `https://api.liquilens.in/mcp`; public research requires no account or API key. Discover covered slugs with `banking_specialisation_coverage` before choosing an unfamiliar bank. Registry presence alone is not evidence coverage.

For the Cosmos demo call `bank_asset_quality_review` with `{"slug":"cosmos-ucb","include_history":true}`. For other banks, use an exact covered slug. Preserve `status`, `period_end`, `available_at`, filing URLs, PDF pages, units, comparability notes and unavailable metrics.

Explain GNPA/NNPA changes in percentage points. For NPA movements keep cash recoveries, write-offs and upgrades separate. A reconciled stock identity verifies arithmetic against the supplied statement; it does not authenticate the filing or prove that all reductions were cash recoveries. Retain PCR's stated definition rather than comparing unlike bases.

The result is filing research. Historical, stale or unavailable evidence must remain labelled. It does not establish deposit safety or authorize credit. If no matching covered institution exists, report that coverage gap instead of inventing a dossier.

Starter question: “What changed in Cosmos Bank's NPAs? Separate cash recoveries, write-offs and upgrades, and cite the filing pages.”

[Browser demo](https://liquilens.in/start/?task=bank) · [Coverage and setup](https://liquilens.in/developers/institutions/)
