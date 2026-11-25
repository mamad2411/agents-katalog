---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
allowed-tools: Read, Grep, Glob, Bash
metadata:
  phase: planner
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time.

If a question can be answered by exploring the codebase, explore the codebase instead.

As each branch resolves, record it — after the decision, never in place of it: `sh scripts/trace.sh emit kind=grill.decision [subject=<prd:#N, ticket:#N or branch:x, when the plan has one>] outcome=accepted|overridden data.recommended='<your recommended answer>' data.answer='<the answer taken>' reason='<why they chose it, one line>' || :`. `accepted` is your recommendation taken, `overridden` is theirs instead. The trace is written here and never read (the kit's ADR-0008); unconfigured, the call is a silent no-op.

---

*Adapted from `productivity/grill-me` in [mattpocock/skills](https://github.com/mattpocock/skills) — MIT, see `.agents/skills/LICENSE-mattpocock-skills.md`. Use `/grill-with-docs` instead when the project has a glossary and decision records worth challenging the plan against.*
