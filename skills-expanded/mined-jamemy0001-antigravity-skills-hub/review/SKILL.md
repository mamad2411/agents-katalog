---
name: review
description: Review code changes for bugs, defects, and security issues.
disable-model-invocation: true
aliases:
  - review
category: "05 - Security & Code Quality"
tags:
  - agent-skill
  - quality-security
  - stage-5
---

# Review

> [!NOTE] Single-Agent Mode (Default)
> If autonomous subagents are disabled, perform the review directly within the current session.

Ask the user which review to run with the AskQuestion tool. If the AskQuestion tool is not available, ask the user directly. Provide exactly one single-select question with two options:

- `bugbot`: Bugbot (`/review-bugbot`)
- `security`: Security Review (`/review-security`)

After the user chooses, run the matching review once:

- Bugbot: follow the `/review-bugbot` instructions.
- Security Review: follow the `/review-security` instructions.

---

## 🔗 Connected Skills
- [[Skills/review-security/SKILL|review-security]]
- [[Skills/review-bugbot/SKILL|review-bugbot]]
- [[Skills/autopilot/SKILL|autopilot]]

<!-- v1.1.0 synchronized: 2026-09-29 -->
