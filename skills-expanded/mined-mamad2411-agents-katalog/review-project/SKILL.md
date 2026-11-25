---
name: review-project
description: Review completed tasks for quality, completeness, and integration; update _OVERVIEW with findings. Use when work packages are done and you want a quality pass.
---

# Review project

Post-WP QA: **`npm run build`**, best-effort tests, integrate findings into **`_OVERVIEW`**.

**Context:** **`project-workflow.mdc`**, **`workpkg-hygiene.mdc`**.

---

## Input

Path to **`docs/implementation/<name>/_OVERVIEW.md`** (or folder).

## Flow

1. **Compile signal** — `npm run build`; knock down trivial breakage; tabulate lingering failures.
2. **Task audit** — each ✅ package: acceptance coverage, risky shortcuts (swallowed errors, `any`, missing UX affordances vs **user-goals**).
3. **_OVERVIEW** — refresh completion % , review stamp, 2–3 bullet synthesis; offload novellas elsewhere.
4. **User recap** — shippable? deferred risks? automation gaps?

## Output guarantees

Green build **or** explicit exemption list with owners; `_OVERVIEW` mentions review date + key risks; conversational summary distinguishes fixed vs documented debt.
