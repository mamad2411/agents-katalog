---
description: Interactive or guided project setup for Claude Code token optimizer settings. Use when the user asks to install, configure, setup, enable hooks, or choose token-saving options interactively.
argument-hint: [plan|apply|options]
allowed-tools: Bash(context-guard-setup *), Bash(context-guard-diet scan *), Bash(context-guard-hooks *)
---

# ContextGuard Setup

Goal: help the user configure this plugin without memorizing helper commands.

Default flow:

1. Run a read-only health check and plan first:

```bash
context-guard-setup --verify
context-guard-setup --plan
```

2. Explain the three profiles briefly (`--profile`):
   - `minimal`: deny bulky/sensitive reads + large Read guard only,
   - `recommended` (default): adds the Bash trim/escrow + sanitizer hook and missing model/effort defaults (the statusline is deprecated and no longer part of this profile),
   - `max`: adds the failed-attempt nudge for repeated Bash failures (off by default until false-positive data exists).
   Individual `--no-*` flags remove one item from a profile.
3. If the user wants the recommended project-local setup, run:

```bash
context-guard-setup --yes
```

   For the fullest set: `context-guard-setup --profile max --yes`.

4. Treat the post-apply `context-guard-diet scan` summary emitted by setup as the default remaining-gap check; run `context-guard-diet scan .` separately only when the user wants the full report.
5. For automation that must skip the post-apply scan summary, run `context-guard-setup --no-diet-scan --yes`.
6. If they want extra token reduction beyond setup, prefer local artifact escrow, symbol reads, and semantic digests rather than external model offload.
7. If a hook misfires, turn it off for this session instead of re-running setup: `context-guard-hooks off read|bash|nudge|all [--for 2h]`, then `context-guard-hooks status` / `on`.

Safety:

- Do not modify global `~/.claude/settings.json`.
- Prefer project-local `.claude/settings.json`.
- `context-guard-setup --verify` is a local read-only health check and never applies settings.
- Setup's post-apply scan is local, read-only, and prints a summary only; it does not mutate settings.
- Setup should use packaged/check-out helper paths by default; only pass `--allow-path-helper-fallback` when the user explicitly trusts a PATH-installed ContextGuard helper set.
