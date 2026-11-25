---
name: open-weight-role-drift-governance-artifacts
description: Applies Oliveira, Conte, Gerosa & Steinmacher (CHASE'26, April 2026, arXiv:2603.24879) — the first systematic cross-project study of how OSS projects codify roles in GOVERNANCE.md files (8,000 license-stratified repos; 54 governance files with content; Institutional Grammar decomposition of 133 roles into scope/privileges/obligations/promotion criteria) — showing ROLE DRIFT (identical titles carry different responsibilities; different labels describe similar functions), the MAINTAINER PARADOX (the role meant to distribute power centralizes it: 50 of 133 roles are composite maintainers spanning technical + managerial + interpersonal skills), and the two-layer organizational/operational governance structure. Use when [writing GOVERNANCE.md or role definitions, diagnosing maintainer-overload and governance concentration, designing role clarity for open-source projects, or briefing on governance-as-documented-artifact]. NOT for [funding structures (use the OSS-funding stack) or CNCF structural guidance (use cncf-governance-structure-data)].
---

# Role Drift and the Maintainer Paradox: What GOVERNANCE.md Files Actually Say

## Overview

Open-source sustainability depends on governance that defines who decides, who acts, and how responsibility is distributed — but the empirical evidence of how projects actually codify this was missing. This study (CHASE'26, Rio de Janeiro; NSF-funded) analyzed governance artifacts from **8,000 license-stratified GitHub repositories** (top-1,000 by stars per license type), finding governance files in only **72 projects (0.9%)**, with usable content in **54** — governance is documented in less than 1% of high-visibility OSS projects.

Applying Institutional Grammar to decompose 133 roles into scope, privileges, obligations, and promotion/demotion criteria, then mapping each to a 45-skill catalog:

- **Role drift** — the same title ("maintainer," "owner," "core developer") carries different responsibilities across projects; different labels ("owner," "project lead," "core developers") describe near-identical functions. Terminology misalignment is the norm, not the exception.
- **The Maintainer Paradox** — governance artifacts centralize power in those meant to distribute it. Maintainers are the most multidimensional role (50 of 133 roles): programming + engineering + version control + documentation skills, PLUS management (community, project, planning) and interpersonal skills (communication, collaboration). The composite role couples organizational and operational authority in a small group — embedding dependency, burnout, and turnover risk into the governance itself.
- **Two-layer structure** — organizational roles (Owners, Steering, BDFL: strategic, management, external-relations skills; almost no technical skills) vs operational roles (Contributors, Reviewers, Triagers; technical, narrow). Maintainers are the connective tissue between layers.
- **Role specialization vs hybridization** — some projects split reviewer/triager/release-manager; others merge everything into one maintainer. Neither is inherently better, but composite roles hide workload.
- **Symbolic roles matter** — Community Advocates (almost exclusively communication/external-relations skills), Emeritus Maintainers (no measurable skills — purely institutionalized recognition), Users (the "silent majority" whose presence justifies the project).

## When to Use

- Writing or auditing a GOVERNANCE.md file
- Designing role definitions that won't drift
- Diagnosing maintainer overload in a project (or defending against it structurally)
- Advising on whether to document roles that are informally practiced

## Core Workflow

1. **Decompose every role into four dimensions** (Institutional Grammar operationalization): scope of responsibility (what domain it governs), privileges (merge/commit/voting rights), responsibilities/obligations (review, mentoring, decision participation), and promotion/demotion criteria (nomination, election, activity thresholds, resignation). If a dimension isn't stated, mark it absent — do not infer.
2. **Name roles by function, not tradition.** Two "maintainers" can differ as much as a reviewer and a release manager. Compare roles by their skill bundle, not their title; identical titles across projects are NOT equivalent.
3. **Document composite responsibilities visibly.** Where one person holds triage + review + merge + community duties, write the overlap down — hidden dependencies are the burnout mechanism.
4. **Make promotion criteria explicit and public.** Promotion/demotion is the most commonly absent dimension in governance files; undocumented advancement is where authority boundaries blur.
5. **Distribute what maintainers accumulate.** Splitting composite roles (triage out of maintainership; review ladders; release rotation) is the structural defense against the paradox — governance designed to distribute power shouldn't concentrate it in one role.

## Key Evidence

- Method: Institutional Grammar decomposition (Crawford & Ostrom) adapted to four role dimensions; license-stratified sampling across 11 licenses; skill mapping via the Liang et al. (2022) open-source skills catalog (45 skills, binary matrix).
- Manual interpretive clustering (three coders, unanimous agreement) produced 12 clusters: Core Maintainer (50), Contributor (29), Steering (20), User (12), Project-Specific (9), Owner (8), Advocacy (4), Emeritus (4), Triage (3), Reviewer (2), Committer (1).
- Skill-profile findings: Contributors carry the broadest technical-interpersonal mix; Committers/Reviewers are narrow gatekeepers (merge rights / LGTM votes); Steering and Owner roles concentrate management + external-relations skills with technical skills largely absent; the Emeritus role institutionalizes memory.
- Methodological honesty: governance-as-written ≠ governance-as-enacted; star-ranked sampling over-represents prominent projects; composite roles destabilized automatic clustering (a finding in itself); replication package (Zenodo 17430401) published.

## Pairs with

- `cncf-governance-structure-data` (the structural-layer companion — same week, complementary: CNCF supplies the models and thresholds; this study supplies the role-drift diagnosis that tells you WHY your documented model isn't preventing concentration)
- `wordpress-governance-crisis-2026` (the cost of governance failure at sentiment scale)
- `oss-endowment-and-coop-funding-2026` (co-op one-page charters — the antidote to role drift in small teams)
- `rust-maintainers-in-residence-2026` (funded maintainer roles — the employment fix for the Maintainer Paradox's overload side)
- `agentic-oss-economics-2026` (the maintainer-economics pressure that makes role clarity urgent)

## A-Tech Alignment

- **Open source:** direct infrastructure — every A-Tech open-source project ships a GOVERNANCE.md with four-dimension role definitions, explicit promotion criteria, and named intermediate roles; role clarity is the cheapest governance investment with the longest payoff.
- **Privacy:** documented role boundaries are the accountability layer for privacy-sensitive projects (who reviews, who can approve sensitive changes).
- **Financial freedom:** the Maintainer Paradox quantifies why funding matters — composite maintainer roles are both the bottleneck and the burnout source; splitting roles + funding them (Rust-MiR pattern) distributes rather than concentrates.
- **Practical:** the four-dimension template (scope/privileges/obligations/promotion) is a fill-in-the-blanks GOVERNANCE.md skeleton; the skill-bundle distance test (do two same-named roles actually differ?) is a portable audit.

## Sources

- Oliveira, P., Conte, T., Gerosa, M. & Steinmacher, I. (2026). "Governance in Practice: How Open Source Projects Define and Document Roles." CHASE'26, arXiv:2603.24879 (CC-BY; replication Zenodo 17430401).
- Companion case study: Oliveira et al., "Governance Matters: Lessons from Restructuring the data.table OSS Project" (ICSME 2025) — governance reform produced 200% new-contributor growth, PR resolution from 700+ days to under a week, 3× contributor retention.