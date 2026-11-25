---
name: repo-onboarder
description: Generate compact repo briefing documents for subagent prompt injection
version: 1.0.0
triggers:
  - "onboard repo"
  - "repo briefing"
  - "analyze repo"
inputs:
  repo: "GitHub repo (org/name or full URL)"
  force: "Regenerate even if cached (optional, default: false)"
outputs:
  briefing: "Markdown briefing file at $WORKSPACE/repo-briefings/<org>-<repo>.md (default: ~/.skills-workspace)"
tools:
  - git
  - gh
  - find
  - wc
  - sort
  - uniq
  - head
  - jq
---

WORKSPACE note: The scripts use $WORKSPACE for outputs. If unset, it defaults to `~/.skills-workspace`.

# repo-onboarder

Generates a compact (~500-1000 word) repo briefing document designed for injection into subagent prompts. Automates the "deep repo evaluation" that makes agent prompts effective — package layout, test commands, conventions, hot files.

## Usage

```bash
# Analyze a GitHub repo
bash skills/repo-onboarder/scripts/generate_briefing.sh owner/repo

# Force regeneration (skip cache)
bash skills/repo-onboarder/scripts/generate_briefing.sh owner/repo --force

# Full GitHub URL also works
bash skills/repo-onboarder/scripts/generate_briefing.sh https://github.com/owner/repo --force
```

## What it does

1. **Clone/update** — Clones to `/tmp/repo-onboarder/<org>-<repo>` or pulls if exists
2. **Detect languages** — Go (go.mod), Node (package.json), Python (pyproject.toml/setup.py), Rust (Cargo.toml)
3. **Analyze structure** — Directory layout, build system, test framework, CI config
4. **Extract conventions** — From README, CONTRIBUTING, AGENTS.md, and code patterns
5. **Find hot files** — Git log churn analysis (top 20 most-changed files)
6. **Map modules** — Language-specific package/module graph
7. **Detect release tooling** — goreleaser (.goreleaser.yml), Docker (Dockerfile), Makefile release targets, GitHub release workflows
8. **Identify tracker** — Check for Linear config, GitHub Issues usage, or project boards
9. **Output briefing** — Cached at `$WORKSPACE/repo-briefings/<org>-<repo>.md (default: ~/.skills-workspace)`

The briefing now includes a **Release & CI** section covering: release tooling, CI workflows, required checks, and deployment patterns. This prevents issues like missing ldflags or Dockerfiles when creating release-related issues.

## Output format

The briefing contains: Quick Facts, Directory Layout, Conventions, Hot Files, Key Packages/Modules, and Test Commands. Every word is chosen for density — this goes into agent context windows.

## Cache

Briefings are cached at `$WORKSPACE/repo-briefings/<org>-<repo>.md (default: ~/.skills-workspace)`. Use `--force` to regenerate. The script prints the output path on completion.
