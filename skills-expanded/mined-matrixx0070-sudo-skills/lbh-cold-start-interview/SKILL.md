---
name: lbh-cold-start-interview
version: 1.0.0
description: Interview a first-time Legal Builder Hub user to turn a vague legal goal into a concrete capability, jurisdiction, and risk profile for skill discovery.
author: matrixx0070
tags: [legal, onboarding, intake, interview, requirements]
capabilities: []
---

## When to use

Use this when a user arrives with a fuzzy legal goal ("I need help with contracts") and no idea which skills exist. It runs a short structured intake so the next step — registry browsing — starts from a precise need instead of a guess.

**Not for:** users who already know the exact capability they want (go straight to `lbh-registry-browser`), or giving legal advice yourself. You gather requirements; you do not opine on the law.

## Method

1. Ask for the outcome, not the tool: "What document or decision do you need to reach?" Capture it in one sentence.
2. Pin jurisdiction. Ask country/state and whether cross-border. Jurisdiction changes everything downstream, so never assume it.
3. Classify the document type and lifecycle stage: draft, review, negotiate, or file.
4. Assess sensitivity: does the workflow touch PII, privileged material, or regulated data? This sets the security bar for later gating.
5. Establish autonomy tolerance: does the user want suggestions only, or hands-on edits to their documents?
6. Summarize back a requirements card and confirm before handing off. Ask at most five questions; infer the rest and label inferences.

## Example

User: "Help me with an employee agreement." You ask outcome (draft new), jurisdiction (US-California), stage (draft from scratch), sensitivity (contains PII, salary), autonomy (suggestions only). You produce a card: capability=employment-contract-draft, jurisdiction=US-CA, sensitivity=HIGH, and hand it to `lbh-registry-browser` with a note that HIGH sensitivity tightens the security gate.

## Pitfalls

- Assuming jurisdiction from the user's location. Where they live is not where the contract governs. Ask.
- Over-interviewing. More than five questions loses the user; infer and label instead.
- Skipping the sensitivity question, so a PII-heavy workflow later passes an unnecessarily loose security gate.
- Drifting into legal advice. Stay on requirements; recommend a human lawyer for substantive questions.

## Output format

```
# Intake Card
GOAL: <one sentence outcome>
CAPABILITY: <phrase>
JURISDICTION: <country/state> cross-border=<y/n>
DOC TYPE / STAGE: <type> / <draft|review|negotiate|file>
SENSITIVITY: <low|med|high> (PII/privileged/regulated: ...)
AUTONOMY: <suggest-only | edit>
INFERRED (unconfirmed): <...>
NEXT: lbh-registry-browser with capability + jurisdiction
```

## Reference

**Skill-vetting checklist (intake link):** the card must carry jurisdiction and sensitivity so discovery can hard-filter and QA can set the right bar.

**Security-review gate criteria:** HIGH sensitivity (PII/privileged/regulated) raises the gate — such workflows must reject any skill that fetches remotely or writes outside a sandbox.

**Versioning / rollback:** record the intake card with a timestamp so a later re-interview can diff changed requirements and justify swapping an installed skill version.
