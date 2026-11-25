---
name: hq-feature
description: "Manage cross-repo feature branches via ClaudeHQ. Start, commit, push, PR, merge, or abandon features spanning multiple repos. Triggers: hq feature, cross-repo feature, feature branch, hq-feature."
argument-hint: "<subcommand> <feature-name> [options]"
---

# /hq-feature — Cross-Repo Feature Manager

Manages feature branches that span multiple repositories using the `hq feature` CLI in `~/Projects/ClaudeHQ/scripts/hq`.

## Usage

```
/hq-feature start <name> [--repos=A,B,C]
/hq-feature status <name>
/hq-feature commit <name> -m "message"
/hq-feature push <name>
/hq-feature pr <name> [--title "..."] [--body "..."]
/hq-feature merge <name> [--auto]
/hq-feature abandon <name>
```

## Examples

```
/hq-feature start gpt-models-integration --repos=claude-config,GptModels
/hq-feature status gpt-models-integration
/hq-feature commit gpt-models-integration -m "add execution-backends"
/hq-feature push gpt-models-integration
/hq-feature pr gpt-models-integration --title "feat: GPT models integration"
/hq-feature merge gpt-models-integration
/hq-feature abandon gpt-models-integration
```

## Execution Steps

### 1. Resolve CLI path

Check that the `hq` CLI exists:
```bash
ls ~/Projects/ClaudeHQ/scripts/hq
```

If missing, report: "ClaudeHQ not found at ~/Projects/ClaudeHQ/scripts/hq. Clone the repo first."

### 2. Parse arguments

Extract from the invocation:
- `subcommand` — one of: `start`, `status`, `commit`, `push`, `pr`, `merge`, `abandon`
- `feature-name` — positional arg after subcommand
- remaining flags — pass through verbatim (e.g. `--repos=...`, `-m "..."`, `--title "..."`, `--auto`)

If no subcommand or feature-name is provided, show the usage block above and stop.

### 3. Run the command

```bash
~/Projects/ClaudeHQ/scripts/hq feature <subcommand> <feature-name> [flags...]
```

Capture both stdout and stderr. Do not modify or filter the output.

### 4. Report output

Print the full output from the command to the user. If the exit code is non-zero, highlight the error clearly and suggest a fix if obvious (e.g. wrong repo name, missing feature state file).

## Subcommand Reference

| Subcommand | Args | What it does |
|------------|------|--------------|
| `start` | `<name> [--repos=A,B,C]` | Creates `feature/<name>` branch in each listed repo. If `--repos` omitted, uses all registered projects. |
| `status` | `<name>` | Shows branch status, divergence, and dirty files across all repos in the feature. |
| `commit` | `<name> -m "msg"` | Stages and commits changes in all repos that have modifications on the feature branch. |
| `push` | `<name>` | Pushes `feature/<name>` to remote in all repos. |
| `pr` | `<name> [--title "..."] [--body "..."]` | Opens pull requests in all repos. Title defaults to feature name if omitted. |
| `merge` | `<name> [--auto]` | Merges the feature PRs. `--auto` enables auto-merge when checks pass. |
| `abandon` | `<name>` | Deletes the feature branch locally and remotely in all repos, removes state file. |

## Rules

- NEVER edit the `hq` script — only invoke it
- Pass flags through verbatim; do not rewrite or reorder them
- If commit message contains spaces, ensure it is quoted properly when building the command string
- For `pr` subcommand: if `--title` is not in the invocation, do NOT invent one — let `hq` use its default

## Error Handling

- CLI not found → stop, report path and suggest cloning ClaudeHQ
- Feature state file not found → report the exact error from `hq`, suggest running `start` first
- Non-zero exit on `commit` with no changes → inform user there was nothing to commit (not an error)
- 3 consecutive failures → stop and report blocker

## When NOT to Use

- Single-repo operations — use standard git/gh commands instead
- If the user only wants to inspect code without touching branches

## Verification

- [ ] Command ran without error
- [ ] Output reported back in full
- [ ] No flags were silently dropped or modified
