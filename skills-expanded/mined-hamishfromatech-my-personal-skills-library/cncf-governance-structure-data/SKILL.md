---
name: cncf-governance-structure-data
description: Applies the CNCF Technical Oversight Committee governance guidance (blog, Aug 26, 2026) — the first data-driven open-source governance framework from 72 reviewed projects: multi-org maintainers at sandbox entry graduate 2.07× faster (59.1% vs 28.6%); org-balanced voting (per-organization vote caps, typically 1-2, applied to governance decisions) is the strongest observed predictor of sustained diversity; governance must cover WHERE THE WORK HAPPENS, not just the governance layer; three matched models (Maintainer Council / Elected Steering Committee / Federated Subproject) with size thresholds and transition signals. Use when [designing or evolving open-source project governance, choosing between maintainer councils and steering committees, preventing single-org capture, writing GOVERNANCE.md, or advising on contributor ladders and succession]. NOT for [OSS funding mechanisms (use the funding-legs stack) or sentiment surveys (use wordpress-governance-crisis-2026)].
---

# CNCF Governance Guidance: Structure as Data, Not Preference

## Overview

The CNCF Technical Oversight Committee published governance guidance (Aug 26, 2026) synthesizing patterns from governance reviews across **72 graduated, incubating, and archived projects** — moving open-source governance from opinion to evidence:

- **Multi-org maintainers at entry → 2.07× graduation rate** (59.1% vs 28.6% for single-org projects).
- **Org-balanced voting is the strongest observed predictor of sustained diversity.** Allocating governance votes per organization (typically capped at one or two, NOT six — projects with six-voter limits still concentrated) prevents any single company from dominating through maintainer headcount. Scope matters: apply to governance decisions (elections, governance changes, strategic direction) while technical decisions (code review, merge authority) stay with individual maintainers under lazy consensus.
- **Cover where the work happens, not just the governance layer.** 20% of graduated projects now show post-graduation governance concentration — all lacking org-balance mechanisms at incubation. One archived project had org-diversity rules on its governance committee but not its maintainer body: governance/code divergence creates an illusion of diversity.
- **Documentation without structural mechanisms fails.** Multiple projects with well-written governance docs still concentrated — docs without org-balance voting or steering-committee limits don't prevent concentration.
- **Contributor count alone does not predict health.** Governance structure, organizational diversity, and contributor pathways matter more.

## When to Use

- Choosing or evolving a governance model for an open-source project
- Preventing single-organization capture (or diagnosing it)
- Writing GOVERNANCE.md, contributor ladders, or maintainer-fund charters
- Advising A-Tech's own community structures (Builder's Club, A-Coder extensions)

## Core Workflow

**1. Match the model to project size (size thresholds reflect coordination costs; research on collaborative group dynamics — including Dunbar's layered model — suggests direct trust operates reliably in groups of ~5-15):**

| Project characteristic | Recommended model | Why |
|---|---|---|
| Single repo, 3–10 maintainers, 1–3 orgs | Maintainer Council | Low overhead, high trust; governance no more complex than the project |
| Single repo, 10–20 maintainers, 3–5 orgs | Maintainer Council + defined roles | SIG-like responsibility areas, documented processes; full steering committee premature |
| Multi-repo, 20+ maintainers, 5+ orgs | Elected Steering Committee or Federated Subproject | Maintainers can't all know each other's work; elections/delegation add accountability |
| Umbrella of distinct subprojects | Federated Subproject | Autonomy per subproject; steering body coordinates, not controls |
| Any project with >75% single-org contributions | Add org-balanced voting regardless of model | Without structural protections, concentration persists and deepens |

**2. Watch the transition signals** (when Maintainer Councils should evolve): decisions stall; new contributors can't find a path (build intermediate roles — reviewer, approver, SIG lead; projects with intermediate roles produce more diverse maintainer pools); a single org dominates; subprojects diverge.

**3. Document and USE the lifecycle.** Projects that never remove inactive maintainers accumulate names that no longer reflect the actual decision-making body — multiple projects listed inactive external maintainers for years, creating a false appearance of org diversity. Governance reviews check MAINTAINERS file history, not just the file.

**4. Every project, regardless of model, needs:** a documented contributor path (contributor → reviewer → approver → maintainer, with criteria linked to governance rights); documented add/remove/emeritus processes that are demonstrably practiced; vendor-neutrality documentation with current affiliations; decision documentation at every level (technical PR/merge, roadmap, leadership, governance — the most common gap in reviews is undocumented decision-making); a security response process; and a code of conduct.

**5. Avoid the five anti-patterns:** listed diversity that doesn't match contribution data; documented-but-never-used processes; governance/code divergence; no org-balance mechanism; lapsed governance (expired committee terms, overdue elections).

**6. Simplify as well as grow.** Federated structures should shrink — archive dormant SIGs and converged subprojects rather than maintaining empty shells that create the appearance of broad governance while work concentrates.

## Key Evidence

- 72-project review set: 2.07× graduation multiplier for multi-org entry; 20% post-graduation concentration rate, all without org-balance mechanisms; org-balance + contributor ladder = strongest diversity-sustaining combination.
- Size-transition data: projects below ~8 maintainers govern by consensus; above that, defined voting or role structures dominate; steering/federated transitions driven by org complexity (multiple repos, contributing companies, concentration risk), not headcount.
- The "intentional path" standard for majority-single-org projects: common and not inherently a problem for newer projects — but governance must demonstrate an intentional path toward broader participation, not just document the current state.

## Pairs with

- `oss-endowment-and-coop-funding-2026` (the funding side: co-op one-page governance, endowment board control)
- `rust-maintainers-in-residence-2026` (affiliation limits ≤1–2 per company on the Funding Team — the same org-balance principle applied to a funder)
- `omacom-patron-funding-model` (the governance-concentration opposite — this guidance supplies the structural defense)
- `wordpress-governance-crisis-2026` (what governance failure costs at sentiment scale)
- `ai-agent-open-source-governance` (agent-contribution policy — a layer above org structure)
- `nanocommunity-strategy` (small-community resilience)

## A-Tech Alignment

- **Open source:** the direct subject — A-Tech's own projects (A-Coder extensions, Builder's Club infrastructure) should adopt org-balanced voting early ("costs nothing when diversity exists; structural protection as the project evolves") and document the contributor ladder before maintainer nomination.
- **Privacy:** governance that survives corporate capture protects the neutrality of privacy-critical infrastructure (identity, encryption standards).
- **Financial freedom:** org-balance mechanisms are the structural alternative to single-patron dependency — sustainable maintainer funding needs governance that keeps the funder from owning the direction.
- **Practical:** the three-template decision table + the four anti-patterns + the "use it or lose it" lifecycle rule are a one-page governance checklist for any new project.

## Sources

- CNCF Technical Oversight Committee (Karena Angell, Chair), "Governance guidance for CNCF projects: Choosing the right structure for your project's size and stage" (cncf.io blog, Aug 26, 2026), based on governance reviews across 72 projects; three governance templates in the CNCF project template repository.
- Caveats: observational patterns from a curated foundation population (may overstate maturity vs the general OSS population); the 2.07× correlation is not causal; recommend-model thresholds are guidance, not requirements.