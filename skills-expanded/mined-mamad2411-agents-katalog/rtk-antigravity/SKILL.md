---
name: rtk-antigravity
description: >
  RTK (Rust Token Killer) usage rules for Antigravity. Always prefix terminal
  commands with rtk to reduce token consumption by 60–99%. RTK is a transparent
  proxy — if it has a dedicated filter it uses it; if not, it passes through
  unchanged. Always safe to use.
---

# RTK — Token-Optimized Commands (Antigravity)

## Golden Rule

**Always prefix commands with `rtk`** — every single command, in every chain.

```bash
# ✅ Correct
rtk git add -A && rtk git commit -m "msg" && rtk git push origin <branch>

# ❌ Wrong
git add -A && git commit -m "msg" && git push origin <branch>
```

## Mandatory prefixes for this project

```bash
# Tests
rtk go test ./...
rtk go test -race -coverprofile=coverage.out ./...

# Build / lint
rtk go build ./...
rtk go vet ./...

# Git
rtk git status
rtk git add .
rtk git commit -m "..."
rtk git push origin <branch>
rtk git log --oneline
rtk git diff

# GitHub CLI
rtk gh run list
rtk gh run view <id>
rtk gh pr create ...
rtk gh pr view <num>

# File ops
rtk grep <pattern> <path>
rtk find <path> ...
```

## Token savings reference

| Category | Typical savings |
|---|---|
| Tests (`go test`) | 90% |
| Git operations | 59–80% |
| GitHub CLI | 26–87% |
| File search | 60–75% |

## Meta commands

```bash
rtk gain           # Show total token savings
rtk gain --history # Per-command history
```
