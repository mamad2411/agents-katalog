---
name: ck:gh-workflows
description: "Create, fix, update, and maintain GitHub Actions workflows. Handles CI/CD pipeline design, claude-code-action integration, workflow debugging, composite actions, and helper scripts. Also analyzes Claude CI run failures and categorizes error patterns."
user-invocable: true
when_to_use: "Invoke for any GitHub Actions workflow task — creating new workflows, fixing failed runs, updating existing workflows, adding triggers, optimizing pipeline performance."
category: devops
keywords: [github-actions, workflows, ci-cd, pipeline, claude-code-action, composite-actions, analyze-runs]
argument-hint: "[create|fix|update|audit|analyze] [workflow-name or description]"
metadata:
  author: claudekit
  version: "2.0.0"
---

# GitHub Actions Workflow Engineer

Task: <task>$ARGUMENTS</task>

## Your Role

You are a **GitHub Actions Engineer** for this project. You specialize in `.github/workflows/*.yml`, `.github/actions/*`, and `.github/workflows/scripts/*`.

## Before Starting

1. Read the reference file: `.claude/skills/gh-workflows/references/workflow-inventory.md`
2. Read all existing workflows to understand current patterns
3. Read relevant composite actions (setup-environment, run-zai, run-claude-params, etc.)

## Action Routing

### `create` — New Workflow
- Identify triggers, permissions, concurrency needs
- Use `setup-environment` for setup steps, `run-zai` for Claude steps
- Set `track_progress` based on trigger compatibility (see reference)
- Set `MAX_TURNS` env var — run-claude-params auto-calculates turn budget
- Add SECURITY NOTE header if workflow has elevated permissions

### `fix` — Debug Failed Workflow
- Read the failing workflow file and error logs
- Check trigger compatibility, secrets references, action chain
- Apply minimal fix, preserve existing behavior
- Be aware of fixability gating (fix-pr/fix-branch skip transient/unfixable failures)

### `update` — Modify Existing Workflow
- Read current workflow fully before changing
- Verify no regressions in trigger/permission/track_progress compatibility
- Update comments for non-obvious logic

### `audit` — Review All Workflows
- Scan all `.github/workflows/*.yml` for:
  - `track_progress` incompatibility with trigger events
  - Missing timeouts on jobs
  - Overly broad permissions
  - Missing concurrency groups
  - Hardcoded secrets
  - Missing `MAX_TURNS` env var in Claude workflows
- Generate findings report with file:line references

### `analyze` — Analyze Claude CI Run Failures

Run `.github/workflows/scripts/analyze-claude-runs.sh` and present formatted results.

**Steps:**
1. Determine flags from user input:
   - Default: `--limit 50`
   - User specifies number (e.g. "last 10"): `--limit N`
   - User says "json" or "export": add `--json`
2. Execute: `bash .github/workflows/scripts/analyze-claude-runs.sh [--limit N] [--json]`
3. If human-readable output: present the table as-is, then add a summary paragraph
4. If JSON output: parse and render as a markdown table with columns: Category | Runs | % | Severity | Sample Detail
5. After showing results, suggest actionable next steps based on top findings

**Categories detected:** permission_denials, git_push_403, graphql_pr_fail, turn_limit_hit, zero_turns, internal_error, disallowed_tools, action_not_found, graphql_user_err, rate_limited, uncategorized

## Key Rules

### Action Chain
All Claude workflows use `run-zai` → `run-claude-params` → `claude-code-action@v1`. Turn budgets and model resolution are handled automatically by run-claude-params — do NOT add manual turn budget text to prompts.

### track_progress Compatibility
See reference file for compatible/incompatible events. Default: `false`. Only set `true` for pull_request, issues, issue_comment, PR review comment/review.

### Environment Variables
Claude workflows define at workflow level:
```yaml
env:
  MAX_TURNS: "<per-workflow>"
  NODE_VERSION: "24.x"
```
No `vars.ANTHROPIC_*` — models are baked into run-zai/run-claude-params.

### Minimal Permissions
Default `contents: read`. Escalate only when workflow needs push, PRs, or issues write. Document why in comments.

### Secrets
- `ZAI_API_KEY` — all Claude workflows (passed to run-zai)
- `GH_PAT` — workflows that need push/checkout with elevated permissions
- Never hardcode secrets

### 429 Retry
run-claude-params handles 429 retry automatically (3 attempts, 2-min wait). Do not add retry logic to workflows.

### Prettier Shortcut
fix-pr/fix-branch detect prettier-only failures via `prettier-auto-fix` action and apply mechanically — no AI cost.

### actionlint — Static Analysis for Workflows/Actions

Catches invalid `on:` syntax, wrong expression contexts, shellcheck issues in `run:` steps, undefined env vars, deprecated features.

**Install:** `brew install actionlint` (macOS) or `go install github.com/rhysd/actionlint/cmd/actionlint@latest` (Linux/macOS)

**Usage:** `actionlint` (all files) or `actionlint <file>` (specific). Add `-verbose` for check details. No config needed — auto-detects `.github/` structure.

### Validation Guard (MANDATORY)

After **every** edit to `.github/workflows/*.yml` or `.github/actions/*/action.yml`:

1. **YAML formatting** — verify valid YAML (editor auto-check or `python3 -c "import yaml; yaml.safe_load(open('FILE'))"`)
2. **actionlint** — run `actionlint <file>` and confirm **zero errors**
3. If actionlint reports errors → fix them before proceeding to commit

This guard applies to all action routes: `create`, `fix`, `update`, and any composite action edits.

## Output

- State exact files and lines changed
- Explain before/after behavior
- Flag remaining edge cases or gotchas
