---
description: Build an investor or sales pitch deck. Tool invocation (run /founder-os:pitch-deck). Challenges the story first, interviews one question at a time, writes a spec you own, checks every number, renders a .pptx. Needs pip install python-pptx for the render only.
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob"]
---

# Founder OS pitch-deck

Challenge the story, then build it. Never the other way round.

## Procedure

1. Read the skill at `skills/pitch-deck/SKILL.md` and execute it end to end, in order: challenge, interview, spec, claims check, render, gaps.

2. The skill owns the ten-slide structure, the interview and the checks. This command is a thin trigger.

3. If the skill file is missing, reply: `Pitch-deck skill not found at skills/pitch-deck/SKILL.md. Restarting Claude Code fixes this most of the time, because it reloads what is installed. If it happens again after a restart, say "update Founder OS".` and stop.

## Rules

- One question at a time in the interview. Never present the list.
- The markdown spec is the deliverable. The `.pptx` is a render of it.
- The render needs `pip install python-pptx`. If it is missing, say so in one line and hand over the spec. That is a working outcome, not a failure.
- Every number carries a tier tag from `rules/research-integrity.md` before the deck is rendered.
- Never invent traction, a customer, a revenue figure, or a market size. An empty proof slide that says what is being tested is more honest than a decorated one, and it is the slide an investor checks first.
- If the install is empty (no `core/identity.md`), reply: `Founder OS not set up here. Say "set up Founder OS" first.` and stop.
- No em dashes or en dashes. Hyphens only.
