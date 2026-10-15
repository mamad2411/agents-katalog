---
name: verasic-git-commits-audit
description: Pre-push commit history audit against the Verasic commit convention. Use when the user asks to "audit commits", "check commit messages", "clean commit history", or before push/PR to verify branch history.
disable-model-invocation: true
---

Security: see upstream [SECURITY.md](https://github.com/Milkywayrules/verasic-skills/blob/main/SECURITY.md) for trust model.

# Verasic Git Commits — Audit Orchestration

## Workflow

1. If the user passed `--help`: do not audit — print the usage table and default scope from `.cursor/skills/verasic-git-commits-convention/references/audit-protocol.md` (or `.agents/skills/verasic-git-commits-convention/references/audit-protocol.md` for cursor-hybrid installs), then stop.
2. In Cursor: launch the `verasic-git-commit-auditor` subagent (`.cursor/agents/verasic-git-commit-auditor.md`) with the repository path and any flags, in the **foreground**. Relay its report unchanged **except** strip harness paths, skill/rule names, protocol dumps, and internal config per `verasic-agent-disclosure`.
3. In any agent without subagents: read `.cursor/skills/verasic-git-commits-convention/references/audit-protocol.md` and execute the audit yourself in this conversation, following it exactly.
4. The audit is read-only. Fix mode (`--fix-trailers`) runs only in the main conversation after the user explicitly approves the audit report.

## Orchestration (Cursor)

Audit commits on the current branch against the Verasic commit convention (pre-push).

If the user passed `--help`: do not audit — print the usage table and default scope from `.cursor/skills/verasic-git-commits-convention/references/audit-protocol.md` (or `.agents/skills/verasic-git-commits-convention/references/audit-protocol.md` for cursor-hybrid installs), then stop.

Otherwise, launch the `verasic-git-commit-auditor` subagent with this prompt:

```text
Full Repository Path: <current workspace root>
Flags: <any flags I passed, e.g. --unpushed-only, --base develop, --author "Name", --include-merges; default scope otherwise>
Follow your system prompt fully: read the audit protocol, resolve scope, run every check, and report in the standard output format.
```

After the subagent returns, relay its report verbatim — do not soften tiers or drop violations. If everything passed, say so plainly.

The audit is read-only. Fix mode (`--fix-trailers` history rewrite) runs in this conversation, not the subagent, and only after the user explicitly approves the audit report — follow the fix-mode section of the audit protocol exactly.

## Source of truth

The full audit protocol lives in the **convention skill**:

- `.cursor/skills/verasic-git-commits-convention/references/audit-protocol.md` — scope, checks, report format, fix mode

The Cursor subagent is a thin pointer to it; never duplicate the spec elsewhere.

## Hard rules

- Audit is read-only; never rewrite history without explicit user approval after the report.
- For message style and hook wiring, see the sibling skill `/verasic-git-commits-convention`.
