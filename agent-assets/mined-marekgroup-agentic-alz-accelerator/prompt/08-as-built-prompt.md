---
agent: documentation
description: "Generate post-deployment Enterprise Landing Zone as-built documentation"
---

# Step 7: As-built documentation

Act as the Chronicler (📚). Generate comprehensive post-deployment documentation
for the Enterprise Landing Zone estate.

## Process

1. Read session state: `alz-recall show {customer} --json`
2. Read all approved predecessor artifacts (00 through 06) — use compression tiers if context is high
3. Use `06-deployment-summary.md` and any deployment-generated outputs as the source of truth for deployed state
4. Use Steps 1, 2, 3.5, 4, and 5 as artifact-derived context for rationale, intended configuration, governance, and operations
5. If Step 3 artifacts are present, reference them for diagrams and design details
6. If Step 3 artifacts are absent, say so explicitly: "Step 3 was skipped." Do not reference missing diagrams. Instead, generate an inline Mermaid diagram in the TDD from `02-architecture-assessment.md` plus `06-deployment-summary.md`
7. Document each platform Landing Zone with deployed resources, management group hierarchy, and network topology using only approved artifacts and deployed-state evidence
8. Make evidence gaps explicit. If a detail comes only from predecessor artifacts and is not evidenced in Step 6 outputs, label it as artifact-derived instead of independently verified live state
9. Generate the canonical Step 7 deliverables in the shared `deliverables/` path
10. Record completion: `alz-recall complete-step {customer} 7 --json`

## Canonical output contract

Produce in `agent-output/{customer}/deliverables/`:

- `07-technical-design-document.md` — Canonical Step 7 design document with architecture overview, design decisions, inline Step 3 fallback if needed, and deployed-state narrative
- `07-operational-runbook.md` — Day-2 operations procedures
- `07-resource-inventory.md` — Resource-by-resource deployed inventory
- `07-compliance-summary.md` — Security posture, policy, tag, identity, and governance summary
- `07-cost-baseline.md` — Budget configuration, thresholds, and deployed cost baseline

Do not create deprecated parallel outputs such as `07-design-document.md` or
`07-security-posture.md`. For Step 7, `07-technical-design-document.md` is the
canonical design document.

## Data-source contract

- **Deployed-state evidence:** Step 6 outputs, especially `06-deployment-summary.md`, plus deployment-generated inventories or logs
- **Artifact-derived context:** Approved artifacts from earlier steps that explain intent, rationale, and operating model
- **Not in scope for Step 7:** Independent live Azure discovery beyond the evidence already captured in workflow artifacts

## Skills to reference

- `.github/skills/docs-writer/SKILL.md` — Documentation conventions
- `.github/skills/azure-diagnostics/SKILL.md` — Monitoring patterns
- `.github/skills/mermaid/SKILL.md` — Inline fallback diagrams
