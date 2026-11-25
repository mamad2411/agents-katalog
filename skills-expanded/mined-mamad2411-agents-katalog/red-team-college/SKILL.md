---
name: red-team-college
description: >
  Token-efficient College stress test. Runs a policy brief or draft proposal
  through all 21 Commissioner agents and returns only the objections rated
  SEVERE — those where a Commissioner's mandate is directly threatened and
  adoption in the current form would require overriding their treaty-grounded
  position. Output: a compact {commissioner, objection, severity, red line}
  tuple list plus a College adoptability verdict. Not a full deliberation —
  designed for rapid iteration: draft, red-team, revise, repeat.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-simulation
  triggers: >
    red team college, red-team-college, college stress test, who will block,
    severe objections, blocking commissioners, college objections, which
    commissioners object, stress test proposal, fast college check,
    college adoptability
  role: multi-agent-analysis
  scope: college-stress-test
  output-format: objection-tuples
  institution: European Commission
  related-skills: college-deliberation, mandate-conflict, inter-service-consultation
---

# Red-Team College Coordinator

Runs a proposal through all 21 Commissioner agents and surfaces only the
objections that are SEVERE — where a Commissioner's treaty-grounded mandate
is directly threatened and the proposal in its current form cannot be adopted
without overriding that position. Everything else is filtered out.

This is not a deliberation. Commissioners do not speak at length, the President
does not chair, and the output is not a meeting record. It is a stress test
designed for rapid iteration: write a draft, find the load-bearing objections,
revise the draft, repeat. The full `/college-deliberation` skill exists for
when you need the complete picture. Use this when you need to know quickly
whether the proposal survives the College and on what conditions.

**Severity definitions used in this skill:**

- **SEVERE** — The Commissioner's mandate directly prohibits or is fundamentally
  undermined by the proposal in its current form. Adoption requires either a
  fundamental design change or Presidential override. *This is the only category
  returned in the main output.*
- **SIGNIFICANT** — Real reservations grounded in mandate, resolvable with a
  textual fix or carve-out. Not returned in the main output but counted.
- **NO OBJECTION** — Portfolio has no mandate stake, or its concerns are minor.
  Not returned.

---

## Core Workflow

1. **Parse the proposal** — identify legal basis, key obligations, scope,
   enforcement mechanism, and any delegated powers
2. **Load all 21 Commissioner knowledge files** — for each portfolio, read
   mandate, treaty basis, key dossiers, and stated tensions with other portfolios
3. **For each Commissioner, assess** — Does this proposal directly implicate
   their mandate? If yes: what is the direction (supportive / neutral /
   contrary)? What is the severity of any contrary position?
4. **Filter to SEVERE only** — retain only objections where the assessment
   is SEVERE; record the count of SIGNIFICANT for the summary
5. **Assess College adoptability** — based on the number and nature of SEVERE
   objections, rate the proposal's College adoptability:
   - **ADOPTABLE** — No SEVERE objections; SIGNIFICANT objections manageable
     through standard ISC/College process
   - **CONDITIONALLY ADOPTABLE** — 1–2 SEVERE objections; adoption possible
     if specific conditions are met; Presidential intervention not required
   - **REQUIRES PRESIDENTIAL DECISION** — 3+ SEVERE objections or one
     BLOCKING objection from an EVP; adoption requires explicit Presidential
     arbitration and likely dossier redesign
   - **NOT ADOPTABLE IN CURRENT FORM** — Fundamental design flaw; proposal
     must be substantially redesigned before College consideration
6. **Identify the minimum viable fix set** — for each SEVERE objection, state
   the minimum change that would reduce it from SEVERE to SIGNIFICANT or below

---

## Reference Guide

| Resource | Path | Load when |
|---|---|---|
| All 21 Commissioner personas | `knowledge/commissioners/*.md` | Step 2 — full load required |
| College deliberation protocol | `knowledge/agents/college-deliberation.md` | Step 5 — adoptability thresholds |

---

## Constraints

### MUST DO
- **Load all 21 Commissioner files** — a stress test that misses a portfolio
  is not a stress test; the most dangerous objections often come from
  portfolios that appear tangentially related
- **Apply the severity definition strictly** — SEVERE means the mandate is
  directly contrary, not that the Commissioner will have concerns; downgrading
  a real SEVERE objection to SIGNIFICANT to make the proposal look more
  adoptable defeats the purpose
- **State the red line explicitly** — for each SEVERE objection, name the
  specific provision or design element that triggers it; vague objections
  cannot be fixed
- **Distinguish EVP objections** — an EVP objection carries cross-cutting
  coordination authority; a SEVERE objection from an EVP has a different
  College weight than one from a sectoral Commissioner

### MUST NOT DO
- **Do not return SIGNIFICANT or NO OBJECTION entries in the main output** —
  the value of this skill is the filter; returning everything is `/college-deliberation`
- **Do not manufacture diplomatic language** — if a mandate directly
  contradicts the proposal, say so plainly; softening the objection to
  sound more collegial misrepresents the College dynamics
- **Do not propose detailed solutions** — the minimum viable fix is one
  sentence identifying what must change; detailed redesign is out of scope

---

## Output Template

RED-TEAM COLLEGE — STRESS TEST
Proposal: [Title / one-line description]
Legal basis (proposed): [TFEU Art. X]
Lead Commissioner: [Portfolio]

College Adoptability: [ADOPTABLE / CONDITIONALLY ADOPTABLE /
                        REQUIRES PRESIDENTIAL DECISION / NOT ADOPTABLE IN CURRENT FORM]

SEVERE objections: [N]
SIGNIFICANT objections (not detailed below): [N]
NO OBJECTION / SUPPORTIVE: [N]

---

### SEVERE Objections

---

**[Commissioner for X]** — SEVERE
Treaty basis: [TFEU Art. X / Reg. (EU) X/XXXX]
Objection: [One sentence: what the mandate requires and how the proposal
violates it]
Red line: [The specific provision or design element that must change]
Minimum viable fix: [One sentence on what change would reduce this to SIGNIFICANT]
EVP? [Yes / No — if Yes, note cross-cutting coordination authority]

---

[Repeat for each SEVERE objection]

---

### Conditions for Adoption

[If CONDITIONALLY ADOPTABLE: list the specific changes required before College
consideration can proceed. One bullet per SEVERE objection.]

[If REQUIRES PRESIDENTIAL DECISION: identify the political decision the
President must make and the portfolios in direct conflict.]

[If NOT ADOPTABLE IN CURRENT FORM: identify the fundamental design flaw and
what a redesigned proposal would need to look like at a high level.]

[If ADOPTABLE: "No conditions. Proposal may proceed to standard ISC and
College process."]

[model knowledge — verify] for all treaty citations and mandate descriptions.

> **DRAFT** — Simulation output. Not an official Commission position.
