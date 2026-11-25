---
name: slop-gate
description: Deterministic pre-publish scan that refuses AI-slop tells in anything about to be written, published, or sent: files, artifacts, slide titles, table headers, diagram labels, chat messages, commit messages. Use before publishing or sending any deliverable, in CI, or wired as a Claude Code hook so the check runs without being remembered. The editorial counterpart is no-ai-slop, which rewrites; this one blocks.
---

Read `.claude/skills/slop-gate/SKILL.md` and execute it exactly as written; that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
