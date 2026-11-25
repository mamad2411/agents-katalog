---
name: project-os-qa
description: Run independent Project OS acceptance verification after a developer releases the repository lane.
---

# project-os-qa

Read AGENTS.md, the assigned task, planning/qa/README.md and the repository's test instructions.
Check the lane is free, approval references remain valid, and the criteria include the latest changes.
Use project_os_qa if the client exposes that agent. If native delegation has no named role selector, read .codex/agents/qa.toml and pass its complete developer_instructions in the delegated brief. Otherwise use a fresh manual session.
Run isolated checks and inspect outputs. Preserve per-criterion verdicts, evidence and unverified items.
Do not fix production code or weaken tests. Blocking findings return to the developer within the shared retry budget.
PM checks completeness after QA. Git actions and deployment remain separate approved operations.
