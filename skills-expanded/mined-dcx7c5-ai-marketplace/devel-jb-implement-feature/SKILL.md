---
name: devel-jb-implement-feature
description: "| | `<cmd>.go` | Flag parsing + mode routing (dispatch) | `install."
domain: cybersecurity
---

|
| `<cmd>.go` | Flag parsing + mode routing (dispatch) | `install.go` |
| `_handlers.go` | Core handler logic | `install_handlers.go` |
| `_render.go` / `_audit_render.go` | Output rendering | `audit_render.go` |
| `_prompt.go` / `_prompt_tui.go` | Decision/prompt logic | `install_prompt.go` |
| `_tui.go` | Full-screen TUI (bubbletea) | `list_tui.go` |
| `_batch.go` | Batch operation orchestration | `update_batch.go` |
| `_resolve.go` | Target/skill resolution | `update_resolve.go` |
| `_context.go` | Mode-specific context struct | `install_context.go` |
| `_format.go` | Output formatting helpers | `log_format.go` |

**Principle**: dispatch file does ONLY flag parsing + mode routing. Logic goes in sub-files.

### Dual-Mode Command Pattern

Most commands support both global (`-g`) and project (`-p`) mode:

```go
func handleMyCommand(args []string) error {
    mode, rest, err := parseModeArgs(args)
    if err != nil { return err }

    switch mode {
    case modeProject:
        return handleMyCommandProject(rest)
    default:
        return handleMyCommandGlobal(rest)
    }
}
```

Create `<cmd>_project.go` for project-mode handler. Use `parseModeArgs()` from `mode.go`.

### TUI Components (bubbletea)

All interactive prompts use **bubbletea** (not survey). Key components:

- `checklist_tui.go` — shared checklist/radio picker
- `list_tui.go` — filterable list with detail panel
- `search_tui.go` — multi-select checkbox list

Color palette: cyan `Color("6")`, gray `Color("8")`, yellow `#D4D93C`.

Dispatch order: JSON output → TUI (if TTY + items + !`--no-tui`) → empty check → plain text.

### Web API Endpoint

If the feature needs a Web UI endpoint, add `internal/server/handler_<name>.go`:

```go
func (s *Server) handle<Name>(w http.ResponseWriter, r *http.Request) {
    // ...
    writeJSON(w, result)       // 200 OK with JSON
    // writeError(w, 400, msg) // for errors
}
```

Register in `server.go` route setup. Branch on `s.IsProjectMode()` for mode-specific behavior.

### Oplog Instrumentation

All mutating commands log to `operations.log` (JSONL):

```go
start := time.Now()
// ... do work ...
e := oplog.NewEntry("command-name", statusFromErr(err), time.Since(start))
e.Args = map[string]any{"key": value}
oplog.Write(configPath, oplog.OpsFile, e)
```

Security scans write to `oplog.AuditFile` instead.

### Step 6: E2E Runbook (Major Features Only)

If the feature meets **any** of these criteria, generate an E2E runbook:
- New command or subcommand
- Changes to install/uninstall/sync flow
- Security-related (audit, hash verification, rollback)
- Multi-step user workflow (init → install → sync → verify)
- Edge cases that integration tests alone can't cover (Docker, network, file permissions)

Generate `ai_docs/tests/<slug>_runbook.md` following the existing convention:

```markdown
# CLI E2E Runbook: <Title>

<One-line summary of what this validates.>

**Origin**: <version> — <why this runbook exists>

## Scope

- <bullet list of behaviors being validated>

## Environment

Run inside devcontainer with `ssenv` isolation.

## Steps

### 1. Setup: <description>

\```bash
<commands>
\```

**Expected**: <what should happen>

### 2. <Action>: <description>
...

## Pass Criteria

- All steps marked PASS
- <additional criteria>
```

Key conventions:
- YAML-free, pure Markdown
- Each step has `bash` block + `Expected` block
- `ss` = `skillshare`, `~` = ssenv-isolated HOME
- Runbook can be executed by the `cli-e2e-test` skill

If the feature does not meet the criteria above, skip this step.

### Step 7: Stage and Report

1. List all created/modified files
2. Confirm each acceptance criterion is met with test evidence
3. Remind user to run `update-docs` if the feature affects CLI flags or user-visible behavior

## Rules

- **Test-first** — always write failing test before implementation
- **Minimal code** — only write what's needed to pass tests
- **Follow patterns** — match existing code style in each package
- **3-strike rule** — if a test fails 3 times after fixes, stop and report what's blocking
- **No docs** — this skill writes code only; use `update-docs` for documentation
- **No changelog** — use `changelog` skill for release notes
- **Spec ambiguity** — ask the user rather than guessing
