---
name: leeward-concierge
description: "Handle plain-language PM and business-analysis requests with Leeward: research, PRDs, strategy, pricing, discovery, launch plans and decision analysis. Excludes software maintenance of Leeward itself."
---

Leeward root: `${CLAUDE_PLUGIN_ROOT}`. Read Leeward docs and run its helper scripts from that absolute path; it stands in for `<installed-root>` and `<absolute-shipwright-root>` below. If it still shows a variable name, locate the root from this file's path instead.

# Leeward Concierge

Locate the Leeward root from this skill's path: the ancestor containing `manifest.json` and `docs/workflow-contract.md`. In a checkout this is the repository root; in a copied install it is `.codex/`; in a plugin it is the plugin root. Read that workflow contract. Resolve referenced files and helpers from that root while keeping the working directory at the user's project.

## Routing

- A binary high-stakes question about acquisition, governance, publication, sunsetting, pivoting or a price change needs a verdict. Apply the inline decision-analysis protocol in `agents/orchestrator.md`. Do not replace the verdict with a strategy workshop or start another model CLI inside this session. A second opposing-position pass is a same-session stress test, not independent validation.
- Choose one framework first. Consult `manifest.json` and `skills-map.md` for broader work. Optional `scripts/route-request.mjs` output is a routing hint, not evidence that required inputs exist.
- For fresh web evidence, follow the research protocol in `docs/workflow-contract.md`: one primary query, `--mode auto`, facts first and then the evidence pack. A fallback pack or a missing helper or runtime permits bounded browsing.
- For a requested workflow, read `commands/<name>.md`. Reuse existing work. If delegation is unavailable, apply specialist roles sequentially in this session.

## Common mappings

| Request | Initial skill name |
|---|---|
| Market sizing or viability | market-sizing |
| Competitor research | competitive-landscape |
| Pricing and packaging | pricing-strategy |
| Build versus buy comparison | build-vs-buy-analysis |
| Discovery | opportunity-solution-tree |
| Customer feedback | feedback-triage |
| Product strategy | product-strategy-session |
| PRD | prd-development |
| Prioritization | prioritization-advisor |

Find the named skill under `skills/`; source checkouts include category directories and distribution packages use flat skill directories.

Ask at most two material clarifying questions when needed. Proceed when the request is clear. Return work inline unless a saved artifact was requested. Apply the skill's evidence bar and depth-aware readiness gate. Include the four signature elements once, with all six Decision Frame fields from `docs/output-standard.md`. Partial work remains explicitly FAIL; never invent evidence, approval, owners or dates to complete it.
