---
name: report
description: Generate a non-technical test coverage summary for stakeholders like PMs, CTOs, or boards. Use when the user runs /report or asks for a shareable summary of test coverage.
---

# /report — Stakeholder Coverage Summary

**Type:** Reporting
**Description:** Generates a non-technical test coverage summary for stakeholders — PMs, CTOs, or boards. Built for Persona 4.

---

## Input Format

Optional:
- A feature scope
- Allure results / latest run results (if available)

With no input, summarize the current state of the suite from the spec files.

## Output Format

A non-technical, outcome-focused summary (no code):
- **Headline** — one sentence on overall coverage and health
- **What's tested** — features covered, in plain language
- **What's not yet tested** — known gaps and risk
- **Recent results** — pass/fail trend if run data is available
- **Recommendation** — what to prioritize next

## Step-by-Step Instructions

1. Use Persona 4 tone: non-technical, outcome-focused, confident, no code.
2. Build the coverage picture from the spec files (reuse `/coverage-map` logic if needed).
3. If Allure or run results are available, fold in pass/fail and trend; otherwise state coverage only and say results aren't included.
4. Translate features into business language ("Users can log in and reset their password" — not "auth.spec.ts").
5. Be honest about gaps and frame them as risk, not blame.
6. End with a short, prioritized recommendation.

## Rules

- No code in the output unless the user explicitly asks.
- Never overstate coverage — be honest about gaps.
- Keep it shareable: clean headings, plain language, no jargon.
