---
name: build-borrow-buy-assessment
description: Use when an independent vibe coder (1-person team) needs to ship production-ready software with fewer unknowns by deciding what to build, what to borrow, and what to buy.
---

# Build Borrow Buy Assessment

## Overview

This skill is for turning software ideas into production systems without reinventing solved problems.
It helps prioritize custom building only where your business gains unfair advantage, while borrowing or buying commodity infrastructure.

## Default Profile

This skill is built for:
- `independent-vibe-coder` (1-person team)

Default assumptions to reduce complexity:
- Non-regulated business software (no high-compliance, no high-liability workflows)
- One production environment plus one staging/dev environment
- Low-to-moderate initial traffic
- No dedicated SRE or platform team
- Goal is first stable production launch, then hardening in follow-up sprints

## Use This Skill When

- The user is a vibe coder or founder trying to go from prototype to production.
- The user asks "can we build this ourselves?" and needs to avoid hidden production complexity.
- The decision affects delivery speed, reliability, security, compliance, or operational overhead.

## Core Principle

Build the value wedge. Borrow or buy the plumbing.

Where possible:
- `build`: domain-specific workflows, proprietary logic, and differentiated UX.
- `borrow`: extensible open source components where control matters.
- `buy`: high-complexity commodity services (auth, payments, messaging, analytics, observability, infra primitives).

## Workflow

### 1) Define the value wedge

Capture these minimum inputs:
- Product idea in one sentence
- Core customer problem and business outcome
- Success metric for the first production release
- Launch timeline and budget guardrails
- Team constraints (assume one builder unless user says otherwise)

If inputs are incomplete, make explicit assumptions and continue.

### 2) Split core vs commodity capabilities

Decompose the idea into capability blocks and tag each as:
- `Core value`: directly differentiates the business
- `Commodity`: required, but not differentiating

Use `references/production-unknowns-map.md` to find hidden commodity areas that often break first production launches.

### 3) Generate build/borrow/buy options per capability

Always include:
- One `build` baseline for the full flow
- At least 2 `borrow` options for major commodity blocks
- At least 2 `buy` options for major commodity blocks

For `borrow` discovery on GitHub:
- Use `references/query-pack.md`
- Optionally run `scripts/search_borrow_candidates.py`

### 4) Gate out production-risk options quickly

Drop options that fail hard gates:
- No clear path for auth, RBAC, and auditability
- No backup/recovery strategy for critical data
- No viable deployment/monitoring story
- No API/webhook/export path for required integrations
- Incompatible licensing or security/compliance blockers
- Obviously abandoned repos or unstable vendor signals

### 5) Score using unknown reduction + production readiness

Use `references/scoring-model.md`:
- 1-5 rating scale per criterion
- Weighted score out of 100

Do not score from marketing claims alone. Require evidence per major criterion (docs, API references, maintenance dates, implementation notes, or POC evidence).

### 6) Recommend a production path, not just a winner

Decision logic:
- Recommend the highest-scoring feasible option set.
- If scores are close (within 5 points), run a short spike focused on top unknowns.
- If all candidates are weak, narrow scope and ship a thinner first release.

Confidence levels:
- `High`: clear score lead and unknowns have mitigation paths
- `Medium`: moderate score lead with manageable unknowns
- `Low`: unknowns remain high or evidence is weak

### 7) Produce a de-risked execution plan

Use the template in `references/report-template.md`.
Always include:
- Do-not-build list for commodity components
- First 2-week unknown retirement sprint
- Integration and migration sequence
- Rollback/exit strategy for lock-in-sensitive dependencies

### 8) Run lightweight accelerator + guardrail functions

Use these optional scripts to keep execution concrete without adding heavy process:
- Implementation accelerator:
  - `python3 scripts/implementation_accelerator.py --profile independent-vibe-coder --idea "<idea>" --core "<core1,core2>" --commodity "<commodity1,commodity2>" --integrations "<int1,int2>"`
- Production guardrail check:
  - `python3 scripts/production_guardrail_check.py --profile independent-vibe-coder --fail "audit,runbook,error_budget"`

Use the accelerator output as the first delivery backlog.
Treat guardrail failures as launch blockers unless explicitly accepted as risk.

## Guardrails

- Never encourage building commodity infrastructure unless there is a defensible reason.
- Never pick a winner from stars or hype alone.
- Always separate facts from assumptions and list unknowns explicitly.
- Always include operational burden (ownership, on-call, upgrades, incident response).
- Keep recommendations practical for small teams with limited ops capacity.
- Keep recommendations optimized for a 1-person operator unless user overrides the profile.

## Output Contract

When used, return:
1. Problem framing and value wedge.
2. Capability split: core vs commodity.
3. Candidate options by `build`, `borrow`, `buy`.
4. Weighted scorecard table (0-100).
5. Recommendation with confidence level.
6. Do-not-build list for this use case.
7. Unknowns and retirement plan.
8. Phased production plan (30/60/90 or equivalent).
9. Accelerator backlog for the first sprint.
10. Guardrail pass/fail summary with blocker list.

## Resources

- `references/scoring-model.md`: weighted criteria tuned for production unknown reduction.
- `references/query-pack.md`: GitHub search patterns for borrow candidates.
- `references/production-unknowns-map.md`: checklist of production complexity areas.
- `references/report-template.md`: response template for consistent outputs.
- `references/implementation-accelerator.md`: function behavior and usage.
- `references/guardrail-gates.md`: production guardrail definitions.
- `scripts/search_borrow_candidates.py`: optional helper to gather borrow candidates quickly.
- `scripts/implementation_accelerator.py`: converts decision output into a first sprint plan.
- `scripts/production_guardrail_check.py`: checks launch readiness against non-negotiable controls.
