---
name: engineering
description: >
  Engineering guidance and best practices for software engineers. Use this skill whenever
  the user is doing engineering work: writing code, designing systems, reviewing PRs,
  debugging issues, deploying software, handling incidents, writing docs, managing
  tech debt, designing tests, or doing standups. Load this skill even if the request
  seems simple — it routes to the right reference material so you give grounded,
  practical advice rather than generic answers.
---

# Engineering

This skill routes engineering requests to the right reference material. Your job is to
identify what kind of engineering task the user is doing, read the relevant reference
file(s), then help them using that guidance.

## Reference files

Load only the files relevant to the current task. Don't load everything upfront.

| File                              | Covers                                                 | Load when user is...                                                         |
| --------------------------------- | ------------------------------------------------------ | ---------------------------------------------------------------------------- |
| `references/architecture.md`      | ADRs, design proposals, architectural trade-offs       | Making architecture decisions, evaluating design options, writing ADRs       |
| `references/code-review.md`       | Code review for security, performance, correctness     | Reviewing a PR, asking for feedback on code, checking a diff                 |
| `references/debug.md`             | Structured debugging from reproduction to fix          | Stuck on a bug, asking how to diagnose an issue, tracing unexpected behavior |
| `references/deploy-checklist.md`  | Pre-deploy verification, rollback readiness            | About to deploy, asking what to check before shipping                        |
| `references/documentation.md`     | API docs, runbooks, READMEs                            | Writing or improving docs, generating a README, creating a runbook           |
| `references/incident-response.md` | Incident triage, comms, blameless postmortems          | In an incident, writing a postmortem, on-call response                       |
| `references/standup.md`           | Daily standup updates from git/PR activity             | Writing a standup update, summarizing recent work                            |
| `references/system-design.md`     | Systems, APIs, data models, service boundaries         | Designing a new system or feature, thinking through API shape, scaling       |
| `references/tech-debt.md`         | Identifying, categorizing, prioritizing tech debt      | Asking about tech debt, refactor planning, what to clean up                  |
| `references/testing-strategy.md`  | Test strategies balancing coverage, speed, maintenance | Designing tests, asking what/how to test, test pyramid questions             |

## How to use this skill

1. Read the user's message and identify which engineering domain(s) it falls into.
2. Load the relevant reference file(s).
3. Apply the guidance from those references to the user's specific situation.
4. If the task spans multiple domains (e.g., designing a system and then reviewing the code),
   load both relevant files and synthesize the guidance.

When in doubt about which reference applies, briefly explain which one you're consulting
and why — this helps the user understand the reasoning and correct you if you picked wrong.
