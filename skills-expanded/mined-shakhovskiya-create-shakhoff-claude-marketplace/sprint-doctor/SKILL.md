---
name: sprint-doctor
description: Preflight diagnostic for ai-scrum. Reports hook health, strictness, tracker MCPs, Codex/DeepSeek availability, LSP fallback, test runner, scribe directories. Use before /sprint:start to surface missing tooling and silent fallbacks.
---

# sprint-doctor

Цель — за один pass сообщить "готов ли проект к sprint discipline" и почему нет.

## Checks (mandatory)

| Check | How | Pass criterion |
|-------|-----|----------------|
| **Hooks installed** | `ls $CLAUDE_PLUGIN_ROOT/hooks/*.sh` | All 4 ai-scrum hooks present, executable |
| **Hooks valid schema** | `jq` on `hooks/hooks.json` против `schemas/plugin-hooks.schema.json` | Top-level `hooks` is object с PreToolUse/PostToolUse/Stop |
| **Strictness** | `.sprints/config.yaml` → `strictness:` | One of strict\|lenient\|permissive |
| **Sprint dirs** | `.sprints/active`, `.sprints/archive` | Created or creatable |
| **State file** | `.sprints/active/_state.json` parseable | If exists, `jq empty` passes |
| **Test runner** | Detect from project (pytest, vitest, jest, go test, cargo test) | At least one detected |
| **LSP availability** | Use `ai-scrum:lsp-bridge` skill | At least one LSP MCP or CLI fallback |
| **Tracker MCP** | Detect Jira/Linear/GitHub Issues MCP | Optional — note presence |
| **Codex CLI** | `command -v codex` | Note availability |
| **DeepSeek fallback** | env `OPENROUTER_API_KEY` or saved credential | Note availability |
| **HANDOFF.md** | repo root | Note presence (DoD requirement) |
| **Engram** | `mem_search` tool present | Note availability |
| **portable date** | `date -d` OR BSD `date -jf` OR `python3` | At least one available (for hooks epoch parsing) |

## Output format

```
ai-scrum sprint:doctor
======================

GREEN  hooks installed (4/4 executable, schema valid)
GREEN  strictness=strict (default)
GREEN  test runner: pytest (auto-detected)
YELLOW LSP: typescript-language-server-mcp not found, falling back to tsc CLI
GREEN  tracker MCP: github-issues
YELLOW Codex CLI not on PATH; external review will degrade
GREEN  DeepSeek fallback configured (OPENROUTER_API_KEY present)
GREEN  Engram memory available
GREEN  HANDOFF.md present

Verdict: GREEN — ready for /sprint:start.
        2 yellow notes — sprint will run with degraded external review.
```

## With `--fix`

- Run `chmod +x $CLAUDE_PLUGIN_ROOT/hooks/*.sh` if needed.
- `mkdir -p .sprints/active .sprints/archive` if missing.
- Write minimal `.sprints/config.yaml` with `strictness: strict` if absent.
- Skip everything else (require user opt-in for installations).

## Output schema (machine-readable)

When called with `--json`, emit:
```json
{
  "verdict": "green|yellow|red",
  "checks": [{"name":"...","status":"green|yellow|red","detail":"..."}],
  "fixable": ["..."]
}
```

## When to invoke

- Manually before `/sprint:start`.
- Auto-invoked by `sprint-orchestrator` if `.sprints/config.yaml::auto_doctor: true`.
