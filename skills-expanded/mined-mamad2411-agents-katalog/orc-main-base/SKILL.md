---
name: orc-main-base
description: "Coordinate ORC work: clarify outcomes, choose the development/review flow, track progress and preserve project knowledge."
---

# Coordinate ORC development

Call context first. Inspect active tasks and relevant memories/KB guidance before
creating work so you do not duplicate it. Explore the code or ask a focused question
when needed to turn intent into checkable acceptance criteria.

Use the smallest workflow that completes the request:
- orc-default: development with independent agent review (unless review is opted out).
- orc-human-review: the same development/review lifecycle with human sign-off.
- orc-review-only: review existing work without an implementation node.

Assign orc-coder for development, or a relevant specialized skill when needed.
Features, bugs and refactors are playbooks within development. Choose backends by
available capabilities; do not assume hook enforcement is identical across clients.

Decompose only when separate work units are useful. Use existing task dependencies
and flow capacity limits. Delegate when authorized and useful; otherwise execute
the clear task yourself. Do not hand execution back to the human.

Monitor the task/flow ledger. Surface actionable blockers, completed milestones
and required human decisions. Keep progress in tasks/sessions, reusable discoveries
in memory, and verified procedures in knowledge bases. Follow orc-memory-review before
ending a meaningful work unit. Do not silently rewrite shared skills from one result.

User/project flow overrides remain supported. Prefer extending one existing template
for a real need to adding overlapping global choices. Publishing and deployment
require the authorization defined by the task/user, not this coordinator skill.
