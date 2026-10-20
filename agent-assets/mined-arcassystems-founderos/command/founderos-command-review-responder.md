---
description: Draft replies to incoming customer messages, reviews, DMs, and inquiries. Asks whose voice to use, then drafts in that voice with channel and posture constraints applied.
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob"]
---

Read `skills/review-responder/SKILL.md` and run it.

The skill is for inbound customer messages. If the user is drafting outbound (a cold email, a new pitch), point them to `email-drafter` or `linkedin-post` instead.

If the user has not pasted the actual incoming message yet, ask for it. Do not draft from a summary.
