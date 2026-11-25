---
name: nist-csf
description: "Covers NIST CSF 2.0: the six functions (Govern, Identify, Protect, Detect, Respond, Recover), what changed from 1.1, using it as an assessment lens with Tiers and Profiles, and its relationship to NIST 800-53. Use when the user asks about the NIST Cybersecurity Framework, a CSF assessment or current/target profile, or the new Govern function."
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# NIST Cybersecurity Framework 2.0

CSF is an **outcome-based lens**, not a control catalog. It says _what good looks like_; it points to other catalogs (800-53, CIS, ISO) for _how_. Use it to assess, communicate to execs, and structure a program, then implement controls from a catalog.

Canonical source: NIST `CSF 2.0` (Feb 2024), `nist.gov/cyberframework`. Web-fetch for current subcategory text and the Informative-Reference mappings.

## What changed in 2.0

- **New sixth function: GOVERN (GV)**: added in 2.0. Older "five functions" answers are stale.
- **Scope expanded to all organizations** (1.1 was framed for critical infrastructure); 2.0 is explicitly for any org of any size/sector.
- Now ships **Implementation Examples** and **Quick-Start Guides** + an online **Reference Tool** for mappings.

## The six functions

- **GV: Govern** (the wraparound): risk strategy, roles/responsibilities, policy, **supply-chain risk management (GV.SC)**, oversight. Informs all others.
- **ID: Identify**: asset management, risk assessment, improvement.
- **PR: Protect**: identity/access, awareness, data security, platform security, resilience.
- **DE: Detect**: continuous monitoring, adverse-event analysis.
- **RS: Respond**: incident management, analysis, mitigation, reporting/comms.
- **RC: Recover**: incident recovery execution + communications.

Hierarchy: **Functions → Categories → Subcategories** (the assessable outcome statements, e.g. `PR.AA-01`).

## Using it as an assessment lens

1. **Scope** the assessment (org / system / sector).
2. Score each **subcategory** against current state; common scale is the four **Tiers**: **1 Partial, 2 Risk Informed, 3 Repeatable, 4 Adaptive** (Tiers describe rigor/maturity of governance & risk practice, not a grade to maximize).
3. Build two **Profiles**: **Current Profile** (where you are) vs **Target Profile** (where you need to be, driven by risk/requirements). The gap between them is the roadmap.
4. Prioritize the gaps by risk; pull concrete controls from an Informative Reference to close them.

## Relationship to NIST 800-53

- **CSF = framework/outcomes; 800-53 = the control catalog** (Rev 5: control families AC, AU, SC, IR, …, with baselines low/moderate/high via 800-53B).
- CSF subcategories carry **Informative References** that map down to specific 800-53 controls (also to CIS, ISO 27001 Annex A), so you assess in CSF and implement in 800-53.
- Federal systems: 800-53 is mandated via FISMA/RMF; CSF is voluntary. Many orgs use CSF for the program and 800-53 (or CIS for smaller shops) as the control source.

## Pairs with

- Current-vs-Target profile gap work: `load_skill gap-analysis`.
- Mapping CSF subcategories to ISO/SOC 2/800-53 so one control satisfies many: `load_skill control-mapping`.
