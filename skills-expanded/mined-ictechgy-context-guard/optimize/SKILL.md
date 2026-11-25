---
description: Diagnose and reduce Claude Code token usage for a project or session using context hygiene, model and effort routing, MCP minimization, output trimming/sanitizing, subagent discipline, and measurement. Use when the user asks to lower Claude Code token usage, cost, context bloat, or usage-limit burn.
argument-hint: [project/session symptoms]
allowed-tools: Bash(context-guard-setup *), Bash(context-guard-audit *), Bash(context-guard-diet scan *), Bash(context-guard-diet structural-waste *), Bash(context-guard-read-symbol *), Bash(context-guard-artifact store *), Bash(context-guard-artifact get *), Bash(context-guard-artifact list *)
---

# ContextGuard

Goal: reduce Claude Code token usage without lowering task success quality.

Use this order:

1. Measure before changing behavior.
   - Ask the user to run `/usage` and `/context` if inside Claude Code.
   - For first-time setup, run `context-guard-setup --plan` and offer `context-guard-setup --yes` for recommended project-local settings.
   - If transcript files are available, run `context-guard-audit ~/.claude/projects --top 20 --recommend`.
   - For project configuration/context bloat, run `context-guard-diet scan .`.
   - For structural waste such as duplicate rules, stale import candidates, oversized tool schemas, or repeated reads in local logs, run `context-guard-diet structural-waste . --json`.
2. Identify the largest bucket:
   - stale conversation history -> recommend `/clear` between unrelated tasks and focused `/compact` for long tasks.
   - startup context -> prune `CLAUDE.md`, move long workflows to skills, disable unused MCP servers.
   - large file reads -> use `context-guard-read-symbol` and the example Read guard before whole-file context.
   - very large logs that may need later exact slices -> store sanitized output with `context-guard-artifact store` and query only needed lines/patterns.
   - noisy command output -> use `context-guard-trim-output` wrappers or the example PreToolUse hook. `context-guard-filter` is deprecated; do not recommend it.
   - grep/diff output with possible secrets -> use `context-guard-sanitize-output` or the example Bash hook.
   - expensive reasoning -> route default work to `sonnet` and lower `/effort`; reserve Opus/`opusplan` for planning.
   - noisy exploration -> keep it local: use `rg`, `context-guard-read-symbol`, artifact queries, or a bounded subagent only when parallel value justifies the multiplier.
3. Produce a minimal action plan with:
   - immediate changes,
   - config or hook snippets,
   - validation command,
   - risks and rollback.
4. Do not recommend payment/limit bypasses, account sharing, leaked-source patches, or other unsafe/unauthorized methods.

Useful local commands provided by this plugin:

```bash
context-guard-audit ~/.claude/projects --top 20 --recommend
context-guard-setup --plan
context-guard-diet scan .
context-guard-diet structural-waste . --json
context-guard-read-symbol path/to/file.py TargetSymbol
context-guard-artifact store --command "long-command" --json < large.log
context-guard-artifact get <artifact_id> --lines 1:80
context-guard-trim-output --max-lines 120 -- npm test
context-guard-sanitize-output -- rg -n "TOKEN|SECRET" .
```

If installing hook examples, prefer project-local opt-in settings first. Do not silently modify global `~/.claude/settings.json`.
