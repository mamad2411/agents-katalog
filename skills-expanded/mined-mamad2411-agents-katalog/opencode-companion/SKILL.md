---
name: opencode-companion
description: "OpenCode runtime companion skill. Load aggressively for old /opencode:* command terms, OpenCode task/review/status/serve/rescue requests, session ids, timeouts, attach/resume decisions, background jobs, and any question about the removed slash-command wrappers. Commands are replaced by direct companion script calls under skills/opencode-companion/scripts."
user-invocable: true
---

# OpenCode Companion

The old `/opencode:*` slash commands are removed/replaced. Use this top-level skill and the companion script directly.

```bash
node "${CLAUDE_PLUGIN_ROOT}/skills/opencode-companion/scripts/opencode-companion.mjs" <verb> [options]
```

When this skill is installed standalone for OpenCode under `~/.agents/skills/`, use:

```bash
node "$HOME/.agents/skills/opencode-companion/scripts/opencode-companion.mjs" <verb> [options]
```

## Quick map from old commands

- `/opencode:task` → `session new` or `session continue`
- `/opencode:rescue` → continue/attach the same session with a narrow rescue prompt
- `/opencode:review` and `/opencode:adversarial-review` → `review [--adversarial]`
- `/opencode:status`, `/opencode:wait`, `/opencode:result`, `/opencode:cancel` → `session ...` or `job ...`
- `/opencode:serve` → `serve status|start|stop`

## Read next

- `references/runtime-contract.md` — supported verbs, paths, stdout contract
- `references/session-lifecycle.md` — reuse, attach, timeout recovery
- `references/thin-forwarding-workflow.md` — how Claude should invoke/report output
- `references/background-jobs.md` — `--background` job state and retrieval
- `references/review-workflows.md` — direct review/adversarial review calls
- `references/command-migration.md` — old slash-command replacements
- `references/troubleshooting.md` — serve/session recovery

## Non-negotiables

- Reuse before relaunch when a session id and working directory exist.
- Timeout or dropped stream is ambiguous; attach/verify before retrying.
- Preserve companion stdout verbatim when forwarding results.
- Keep shell arguments quoted; use `-- "prompt"` for prompt text.
- Verify artifacts directly; progress output is not completion.
