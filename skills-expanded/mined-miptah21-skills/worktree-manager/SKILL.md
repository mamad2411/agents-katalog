---
name: worktree-manager
description: Create, manage, and cleanup git worktrees with Claude Code agents across all projects. USE THIS SKILL when user says "create worktree", "spin up worktrees", "new worktree for X", "worktree status", "cleanup worktrees", "sync worktrees", or wants parallel development branches. Also use when creating PRs from a worktree branch (to update registry with PR number). Handles worktree creation, dependency installation, validation, agent launching in Ghostty, and global registry management.
---

# Global Worktree Manager

Manage parallel development across ALL projects using git worktrees with Claude Code agents. Each worktree is an isolated copy of the repo on a different branch, stored centrally at `~/tmp/worktrees/`.

**IMPORTANT**: You (Claude) can perform ALL operations manually using standard tools (jq, git, bash). Scripts are helpers, not requirements. If a script fails, fall back to manual operations.

## When This Skill Activates

**Trigger phrases:**
- "spin up worktrees for X, Y, Z"
- "create 3 worktrees for features A, B, C"
- "new worktree for feature/auth"
- "what's the status of my worktrees?"
- "clean up merged worktrees"
- "launch agent in worktree X"
- "sync worktrees"
- "create PR" (when in a worktree — updates registry with PR number)

---

## File Locations

| File | Purpose |
|------|---------|
| `%USERPROFILE%\.gemini\antigravity\worktree-registry.json` | **Global registry** — tracks all worktrees |
| `.agents/skills/worktree-manager/config.json` | **Skill config** — terminal, shell, port range |
| `.agents/skills/worktree-manager/scripts/` | **Helper scripts** — optional |
| `~/tmp/worktrees/` | **Worktree storage** — all worktrees live here |

---

## Core Concepts

### Centralized Worktree Storage
All worktrees live in `~/tmp/worktrees/<project-name>/<branch-slug>/`

### Branch Slug Convention
Branch names slugified: `feature/auth` → `feature-auth` (`tr '/' '-'`)

### Port Allocation
- **Global pool**: 8100-8199 (100 ports)
- **Per worktree**: 2 ports (API + frontend)
- **Globally unique**: tracked in registry

---

## What You Do vs What Scripts Do

| Task | Script | Manual Fallback |
|------|--------|-----------------|
| Create git worktree | No | `git worktree add <path> -b <branch>` |
| Copy .agents/ | No | `cp -r .agents <worktree-path>/` |
| Install dependencies | No | Detect lockfile, run install |
| Allocate ports | `scripts/allocate-ports.ps1` | Find unused ports manually |
| Register worktree | `scripts/register.ps1` | Update JSON with jq |
| Launch agent | `scripts/launch-agent.ps1` | Open terminal manually |
| Cleanup | `scripts/cleanup.ps1` | Kill ports, remove worktree, update registry |

---

## Workflows

### 1. Create Worktrees with Agents

```
For EACH branch (can run in parallel):

1. SETUP — get project name, repo root, slugify branch, determine path
2. ALLOCATE PORTS — 2 per worktree
3. CREATE WORKTREE — git worktree add
4. COPY RESOURCES — .agents, .env.example
5. INSTALL DEPS — detect package manager
6. VALIDATE — start server, health check, stop
7. REGISTER — add to global registry
8. LAUNCH AGENT — open terminal with claude

AFTER ALL: Report summary table, note failures
```

### 2. Check Status

```bash
cat ~/.gemini/antigravity/worktree-registry.json | jq -r '.worktrees[] | "\(.project)\t\(.branch)\t\(.ports | join(","))\t\(.status)"'
```

### 3. Cleanup Worktree

```bash
# 1. Kill processes on ports
# 2. git worktree remove <path> --force
# 3. git worktree prune
# 4. Remove from registry
# 5. Release ports
# 6. Optionally delete branch
```

### 4. Create PR from Worktree

After `gh pr create`, update registry with PR number:
```bash
PR_NUM=$(gh pr view --json number -q '.number')
jq "(.worktrees[] | select(.branch == \"$BRANCH\")).prNumber = $PR_NUM" \
  ~/.gemini/antigravity/worktree-registry.json > "$TMP" && mv "$TMP" ~/.gemini/antigravity/worktree-registry.json
```

---

## Package Manager Detection

| File | Manager | Install |
|------|---------|---------|
| `bun.lockb` | bun | `bun install` |
| `pnpm-lock.yaml` | pnpm | `pnpm install` |
| `yarn.lock` | yarn | `yarn install` |
| `package-lock.json` | npm | `npm install` |
| `uv.lock` | uv | `uv sync` |
| `requirements.txt` | pip | `pip install -r requirements.txt` |
| `go.mod` | go | `go mod download` |
| `Cargo.toml` | cargo | `cargo build` |

---

## Safety Guidelines

1. Before cleanup: check PR status (merged → safe; open → warn; no PR → warn)
2. Before deleting branches: confirm unsubmitted work
3. Port conflicts: pick different port if in use
4. Max ~50 concurrent worktrees (100 ports / 2)

## Common Issues

| Issue | Fix |
|-------|-----|
| "Worktree already exists" | `git worktree list`, then `remove --force` + `prune` |
| "Branch already exists" | Use existing branch (omit `-b` flag) |
| "Port already in use" | `lsof -i :<port>`, kill or pick different |
| Registry out of sync | Compare registry vs `find ~/tmp/worktrees` |

---

## References

> For registry schema, manual jq operations, script reference, and config format, see:
> `references/registry-operations.md`
