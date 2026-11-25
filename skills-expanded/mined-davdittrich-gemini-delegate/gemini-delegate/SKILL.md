---
name: gemini-delegate
description: Use when [large codebase >200 lines], [web search current info], [adversarial review/critique].
metadata:
  triggers: web search, adversarial review, code analysis, plan critique, large file analysis
---

# Gemini Delegate (ACP)

Delegate tasks to Gemini via ACP bridge. Verification MANDATORY.

## Bridge Mandates
- **MANDATORY**: `scripts/gemini_bridge.py` only. NEVER call `gemini` directly.
- **Safe I/O**: Use `--prompt-stdin` to prevent deadlocks.
- **Persistence**: Use `--output-file AUTO` for unique result files.
- **Sessions**: Capture/reuse `SESSION_ID` from JSON for follow-ups.
- **Timeout**: Total 600s (10m). First chunk 300s.

## Grounding & Web Search
- **Prefix**: Queries MUST start with `WebSearch:` (e.g., `WebSearch: API news 2026`).
- **Grounding**: Prefix forces web grounding. No prefix = fabrication risk.
- **Fallback**: If bridge fails (timeout/crash), use built-in `WebSearch`. Report in one line.

## Routing & Tasking
| Task | Model | Template |
|---|---|---|
| Review (<200 lines) | `gemini-3-flash-preview` | Focused review |
| Bug/Arch (>3 files) | `gemini-3.1-pro-preview` | Tool-assisted |
| Search/Info | `gemini-3-flash-preview` | Web search |
| Adversarial/Plan | `gemini-3.1-pro-preview` | Critique |

## CLI Flags
| Flag | Description | Default |
|---|---|---|
| `--prompt` | Prompt text | |
| `--prompt-file` | Read prompt from file | |
| `--prompt-stdin` | Read from stdin (MANDATORY for automation) | |
| `--session-id` | Resume specific session | |
| `--new-session` | Force fresh session | |
| `--sessions-dir` | Override session storage dir | |
| `--cd` | Workspace root directory | `.` |
| `--timeout` | Total max wall-clock seconds | 600 |
| `--idle-timeout` | Max seconds between chunks | 120 |
| `--first-chunk-timeout` | Max seconds for first chunk | 300 |
| `--verbose` | Print heartbeat markers to stderr | |
| `--output-file` | Write JSON to file (`AUTO` for unique temp) | |
| `--approve-edits` | Allow file writes within `--cd` scope | |
| `--cache` | Content-addressed git-based caching | off |
| `--cache-ttl` | Cache TTL in seconds (1-2592000) | 86400 |
| `--clear-cache` | Clear result cache and exit | |
| `--parallel-models` | Comma-separated models for parallel runs | |
| `--log-feedback` | Append feedback entry `VERDICT|TASK|TOKENS|NOTE` | |
| `--model` | Gemini model to use | |

## Output Schema
```json
{
  "success": true,
  "SESSION_ID": "...",
  "agent_messages": "...",
  "read_file_count": N,
  "fallback_occurred": boolean,
  "requested_model": "...",
  "actual_model_selection": "specified"|"automatic",
  "tool_calls": [...],
  "token_estimate": { "estimated_cost_usd": 0.00 }
}
```

## STOP & VERIFY (Red Flags)
**Violating the letter of these rules violates the spirit. STOP if**:
- `read_file_count` is 0 for code analysis (Gemini is guessing).
- Response contains functions not present in source files.
- Web search response lacks specific source URLs.
- Requested Pro failed (`fallback_occurred: true`). Alert user immediately.
- Calling `gemini` directly. Revert and use bridge.
- Omitted `WebSearch:` prefix. Re-run with prefix.

## Rationalization Table
| Excuse | Reality |
|---|---|
| "I know this code already." | Code changes. RE-VERIFY key logic via `read_file`. |
| "File names explain it." | Guessing = fabrication. READ content. |
| "I'll skip WebSearch: prefix." | Internal 2026 knowledge is fabrication. GROUND every claim. |
| "Pro failed, Flash is fine." | pro-preview is the tier for logic. Fallback must be reported. |

## Permissions & Logs
- **Write**: `--approve-edits` required for file writes.
- **Feedback**: Log outcome via `--log-feedback` after every task.
- **Escalation**: Rejection rate >50% -> escalate model tier.

## References
- `assets/prompt-template.md`: Task templates.
- `assets/reference.md`: Logs, parallel runs, capsules.
