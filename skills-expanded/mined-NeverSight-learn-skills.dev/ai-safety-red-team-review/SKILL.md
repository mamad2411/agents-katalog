---
name: ai-safety-red-team-review
description: Plan and audit AI safety red-team reviews for prompt injection, jailbreaks, data exfiltration, tool misuse, unsafe autonomy, hallucinated actions, privacy leakage, harmful content, policy bypass, model routing fallback, eval coverage, mitigations, release gates, and incident response. Use when an AI feature needs adversarial testing before or after launch.
---

# AI Safety Red Team Review

Use this skill to convert AI safety red-team, prompt injection, jailbreak, privacy, tool-use, eval, mitigation, and release-gate questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify AI feature scope, users, data classes, tools/actions, autonomy level, model routes, policy boundaries, known harms, release stage, and incident history.
2. Read `references/ai-safety-red-team-patterns.md`.
3. Classify tests as prompt injection, jailbreak, data leakage, tool misuse, unsafe action, hallucination, bias/fairness, harmful content, fallback regression, or monitoring gap.
4. Define attack scenarios, fixtures, success criteria, mitigations, severity, owners, release gates, regression evals, and incident response triggers.
5. Produce red-team plan, state machine, decision table, event schema, test matrix, and mitigation backlog.

## Guardrails

- Do not provide exploit instructions beyond what is necessary to define safe internal test scenarios and mitigations.
- Do not treat generic content-policy testing as sufficient for tool-using or data-accessing agents.
- Do not ship high-risk autonomy without recovery, audit logs, user confirmation, and kill switches.
- Do not close red-team findings without regression tests or measurable mitigation evidence.

## Output format

```text
AI safety context:
Audience / source of truth / risk boundary:

Red-team plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Attack classes, mitigations, and release gates:
- <trigger> -> <policy, metric, edge case, support note>
```
