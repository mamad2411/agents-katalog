# hooks/

Claude Code plugin hooks shipped with `faion-network`.

## Registration

Only `hooks.json` is loaded by the runtime. It registers four `UserPromptSubmit` commands, each `python3 ${CLAUDE_PLUGIN_ROOT}/hooks/<file>` with `timeout: 5`. A file present here but absent from `hooks.json` does not run. Workspace-specific hooks (e.g. the NERO statusline's wakeup tracker) live in `~/.claude/hooks/`, not in this repo — the plugin ships only universal session-discipline hooks.

| File | Effect |
|------|--------|
| `context-compact-gate.py` | ctx >40% blocks the prompt unless it starts with `compact` or contains `КРИТИЧНО`; 30-40% injects a soft warning; <=30% silent |
| `stop-improver-check.py` | Injects an improver suggestion once the transcript passes ~25% context |
| `quota-guard.py` | Parks work at 5h quota >=95%, resumes below 90% |
| `peer-nick-check.py` | Flags a peer message whose signature nick is not in `KNOWN`; warns, never blocks |

## Conventions

- stdout is contract, not logging. Emit either nothing or one JSON object with `hookSpecificOutput.additionalContext`; any stray `print()` lands in the model's context.
- Exit 0 to allow, exit 2 to block. `quota-guard.py` uses exit 2.
- Stay well under the 5s timeout. Read pre-computed state from `/tmp/claude-*.json` written by the statusline; never call a network or `op`.
- Never crash a session: wrap all I/O so a missing state file degrades to a silent pass-through.
- Hooks read machine-local paths (`/tmp/claude-session-state.json`, `~/.claude/parked-*.json`). They are NERO-runtime specific and are not portable to a customer install.

## Gotchas

- `quota-guard.py`'s docstring says "PreToolUse hook" while `hooks.json` registers it under `UserPromptSubmit`. The registration wins; treat the docstring as stale.
- `__pycache__/` is checked into the working tree here. Do not import from it.
- `peer-nick-check.py`'s `KNOWN` set is NERO-specific, unlike the other three hooks' machine-local paths. It degrades to silence rather than to noise on a customer install: a prompt with no `[nick/project]` signature returns before the set is consulted, so an install with no peer traffic never sees it fire.
