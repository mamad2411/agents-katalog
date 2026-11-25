---
name: revenue-recognition-qa
description: Use when QAing revenue recognition schedules, deferred revenue, performance obligations, SSP assumptions, contract modifications, and close-period revenue exceptions.
source: "https://github.com/loopfour/finance-skills"
source_repository: "loopfour/finance-skills"
source_path: "skills/revenue-recognition-qa/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Revenue Recognition QA

Use this skill to review revenue recognition support and surface issues for controller review.

## Inputs

- Revenue schedule or subledger export.
- Contract/order form terms and performance obligation notes.
- Billing data, start and end dates, delivery dates, and usage data if relevant.
- Accounting policy excerpts for recognition method, SSP, materiality, and modifications.

## Workflow

1. Identify the revenue model: ratable subscription, usage-based, services, milestone, hybrid, or other.
2. Tie revenue schedule inputs back to contract and billing source data.
3. Check core fields: customer, contract ID, performance obligation, start date, end date, total consideration, deferred balance, recognized amount, and remaining obligation.
4. Review high-risk areas: nonstandard terms, discounts, credits, cancellations, upgrades, downgrades, renewals, multi-element arrangements, and services bundled with software.
5. Classify each issue as policy question, data quality issue, schedule math issue, or missing support.

## Output

Return:

- QA summary with pass, pass with notes, blocked, or controller review required.
- Exception table with issue, source evidence, financial impact, suggested owner, and recommended next step.
- Close-period risk notes.
- Questions for controller, auditor, legal, sales, or billing.

## Guardrails

- Do not provide final accounting conclusions when policy is missing or ambiguous.
- Do not cite ASC 606 or IFRS 15 as a final answer without matching the user's policy and source facts.
- Keep recommendations review-oriented: flag, reconcile, document, or escalate.
- Separate revenue recognition issues from cash collection issues.
