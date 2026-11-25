---
name: technical-debt-hunter
description: Find, size, and prioritize technical debt from code, delivery, reliability, security, and developer-experience evidence. Use for repository audits, roadmap planning, slow delivery, incident follow-up, or modernization decisions.
---

# Technical Debt Hunter

Apply the shared [OutcomeLab skill standard](../../docs/SKILL-STANDARD.md) for evidence, verification, risk, benchmarking, and improvement.

Find debt that changes delivery, reliability, cost, or risk—not merely code that looks old.

## Workflow

1. Gather evidence: change frequency, defects, incidents, CI duration, dependency age, ownership gaps, duplication, complexity, and developer reports.
2. Trace debt to an observable consequence and distinguish root cause from symptom.
3. Score impact, urgency, recurrence, remediation cost, and confidence. Group repeated symptoms into debt themes.
4. Propose thin slices that create measurable improvement while protecting product delivery.
5. Define leading and lagging indicators, ownership, and a stop condition for each initiative.

## Output contract

Return a debt register with evidence, impact narrative, score, proposed intervention, estimate range, dependencies, and success metric; plus a 30/60/90-day sequence.

## Quality gates

- Do not equate style preference with debt.
- Treat low-confidence findings as investigation tasks.
- Quantify opportunity cost or risk where data permits.
- Recommend deletion or simplification before re-platforming.
