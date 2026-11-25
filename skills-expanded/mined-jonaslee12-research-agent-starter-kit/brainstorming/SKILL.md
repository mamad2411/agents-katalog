---
name: brainstorming
description: Use for structured research project or agent-system ideation when the user's idea is still unclear, high-impact, or needs route comparison before drafting, implementation, or skill changes.
---

# Brainstorming

Use this skill to turn a rough idea into a usable decision, design route, or next-step plan.

## Use When

- the user is exploring a research route, research gap, method choice, concept card, or supervisor question;
- the user wants to change the agent system but the exact workflow is unclear;
- multiple options exist and choosing the wrong one would cause rework;
- the next action may affect skills, rules, knowledge-base structure, proposal logic, or ethics materials.

## Default Pattern

1. Restate the decision to be made in one sentence.
2. Ask only the minimum necessary questions. Prefer 1-3 focused questions.
3. Offer one recommended route first.
4. Give 2-4 reasons.
5. Name alternatives only when they change the decision.
6. End with a concrete next action or `待确认`.

## Dissertation-Specific Rules

- For proposal, methodology, ethics, or supervisor discussion, connect the idea to the current project spine:
  - active learning implementation;
  - AI-agent support;
  - university teachers' perceptions;
  - concerns, risks, trust, autonomy, workload, and pedagogic identity;
  - adoption conditions and design boundaries.
- For formal drafting, hand off to `dissertation-source-first-gate` before writing.
- For major proposal or chapter structure, hand off to `dissertation-argument-spine`.
- For system changes, hand off to `dissertation-agent-architecture-audit` and `dissertation-skill-stocktake`.

## Stop Conditions

Stop and ask the user when:

- the decision depends on a missing supervisor requirement;
- the decision depends on an official Canvas/rubric rule not locally confirmed;
- the choice would alter ethics-facing or participant-facing materials;
- the user must choose between different study scopes.

## Output Shape

```text
结论：
...

依据：
1. ...
2. ...
3. ...

待确认：
- ...

下一步：
- ...
```

