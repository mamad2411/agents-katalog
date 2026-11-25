---
name: follow-tool-semgrep
description: Use Semgrep to scan code patterns and security rules that linters/ast-grep don't cover
argument-hint: "[ruleset-or-path]"
related:
  - use-astgrep
  - report
  - run-scan
---

## Goal

Use Semgrep to install and run pattern-based scanning — security rules, custom rules, and registry rulesets — when you need semantic analysis beyond plain text/AST matching

## Scope

- Use when: security scanning (`p/security-audit`, `p/owasp-top-ten`), framework-specific rules, custom org rules, taint tracking
- Comparison: `use-astgrep` suits simple structural patterns; Semgrep suits dataflow/taint and ready-made rulesets
- Scan-only in this skill — fixes via `/deep-review-codebase` or `/fix`

- Latest: `semgrep@1.177.0` (pipx/brew/mise) (verified 2026-09-13)
- References: [apis](references/apis.md) | [cli](references/cli.md) 
## Execute

### Workflows

> Goal: Dispatch to the workflow matching the topic

| Topic | Workflow |-------|----------| config | `workflows/config-rules/SKILL.md` — custom rules, registry rulesets, CI gating 
1. If the argument matches a topic → read and follow `workflows/<name>/SKILL.md` instead of the steps below
2. If not → follow the steps below normally

### 1. Ensure Semgrep Available

> Goal: Have semgrep ready to use

1. Check `semgrep --version` — if not installed: `pipx install semgrep`, `mise use -g semgrep`, or `brew install semgrep`
2. Or run via a container/CI image if you don't want to install locally

### 2. Choose Rules

> Goal: Choose the ruleset by goal

1. Registry rulesets: `p/default`, `p/security-audit`, `p/owasp-top-ten`, `p/<language>`, `p/<framework>`
2. Custom rules: `.semgrep/` or `semgrep.yml` in the repo — write YAML rules for project-specific patterns
3. Choose narrowly enough — `p/default` can be noisy; start with a specialized ruleset

### 3. Run Scan

> Goal: Scan with the right config

1. `semgrep scan --config=<ruleset> <path>` — e.g. `semgrep scan --config=p/security-audit src/` (`--config` without a subcommand still works)
2. Output options: `--json` for processing, `--sarif` for CI/GitHub code scanning
3. Use `--exclude`/`--include` to limit scope — skip tests, generated, vendored
4. `--baseline` for existing codebases — see only new findings

### 4. Triage Findings

> Goal: Handle the results

1. Group by rule severity and confidence — semgrep has false positives too
2. Use `// nosemgrep` for intentional patterns with a comment stating the reason
3. Use `/report` columns: `No.`, `Rule`, `File:Line`, `Severity`, `Confidence`, `Action`
4. Route to `/deep-review-codebase` or `/fix` for remediation

### 5. Integrate (if you want it permanent)

> Goal: Make semgrep part of the workflow

1. CI step or pre-commit hook — a repo with `.moon/workspace.yml` → moon's `vcs.hooks` (`/follow-tool-moonrepo` Step 7); other repos → `/follow-tool-hk`; use `semgrep ci` + `semgrep login` if integrating with Semgrep AppSec Platform
2. Commit custom rules in `.semgrep/` with tests (`semgrep --test`)
3. Baseline strategy for legacy code

## Rules

### 1. Right Tool For Job

- Simple structural patterns → `use-astgrep` first (faster, no install)
- Use semgrep when you need dataflow/taint or ready-made rulesets

### 2. Noise Management

- Don't dump all raw findings — triage severity/confidence first
- Baseline for legacy — don't let signal drown in noise

### 3. Versioned Config

- Custom rules must live in the repo with tests
- Pin ruleset versions in CI — ruleset change = findings change
- Use /run-scan if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- A successful scan with triaged findings
- Custom rules in `.semgrep/` if created
- CI/pre-commit integration if the user wants it
