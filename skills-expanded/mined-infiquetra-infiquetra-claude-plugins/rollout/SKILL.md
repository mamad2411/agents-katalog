---
name: rollout
description: |
  Track and drive SDLC rollout across Infiquetra organization repositories. Provides rollout
  status dashboards, gap analysis per repo, and label and template deployment.
  Uses GitHub repos, issue templates, labels, project mapping, and rollout-status tracking.
when_to_use: |
  Use this skill when the user wants to:

  Rollout status and progress:
  - "which repos have SDLC set up", "rollout status", "how's the SDLC rollout going"
  - "show me rollout progress", "what's the overall status", "rollout dashboard"
  - "which repos still need setup", "how many repos are complete"

  Gap analysis:
  - "check if infiquetra-core is SDLC-ready", "what's missing from this repo"
  - "gap analysis for infiquetra-auth", "run a gap check", "is this repo compliant"
  - "verify this repo's SDLC setup", "what does this repo still need"

  Label deployment:
  - "deploy labels to infiquetra-core", "push SDLC labels to this repo"
  - "set up labels on infiquetra-auth", "create SDLC labels"

  Template deployment:
  - "copy issue templates to this repo", "does this repo have our issue templates"
  - "deploy templates to infiquetra-core", "push issue templates", "set up templates"

  Full deployment (labels + templates):
  - "set up SDLC on this repo", "deploy all SDLC config to infiquetra-core"
  - "push the SDLC config", "deploy labels and templates", "full SDLC setup"
---

# SDLC Rollout

Track and drive SDLC rollout across Infiquetra organization repositories. Check rollout status,
run gap analysis, and deploy labels and templates.

## Script Location

```
$INFIQUETRA_SDLC_PATH/../infiquetra-claude-plugins/plugins/mission-control/scripts/sdlc_manager.py
```

> If `$INFIQUETRA_SDLC_PATH` is unset, use `~/workspace/infiquetra/infiquetra-sdlc` as the default base path.

**IMPORTANT**: Always use `python3` (not `python`) to run the script.

## Rollout Status Overview

Rollout status is tracked in `$INFIQUETRA_SDLC_PATH/config/rollout-status.json`.

### Repo Tiers

| Tier | Priority | Description | Templates |
|------|----------|-------------|-----------|
| Tier 1 | High | Core service repos — full SDLC | All 6 templates |
| Tier 2 | Medium | Infrastructure/shared repos — full SDLC | All 6 templates |
| Tier 3 | Minimal | Claude tool repos — minimal SDLC only | defect + enhancement only |

### Team

| Team | Project | Description |
|------|---------|-------------|
| Mount Olympus | mount-olympus | All Infiquetra org repos |

**Note**: Tier 3 repos (Claude tooling) are excluded from project board automation.

## Rollout Tracking Fields

Each repo tracks four fields in `rollout-status.json`:

| Field | Description | Complete when... |
|-------|-------------|-----------------|
| `labels` | SDLC labels deployed | All 40+ SDLC labels present in the repo |
| `templates` | Issue templates deployed | All required templates present (6 for Tier 1/2, 2 for Tier 3) |
| `claude_md` | CLAUDE.md has SDLC guidance section | CLAUDE.md exists with SDLC workflow guidance |
| `project` | Repo added to project board | Repo is linked to mount-olympus GitHub Project |

Status values: `pending`, `complete`, `n/a` (for Tier 3 repos where project board is excluded)

## Coordination

Rollout work is tracked through GitHub issues, project fields, and `rollout-status.json`.

## Core Operations

### Rollout Status

```bash
# Status for all repos
python3 sdlc_manager.py rollout status
```

Output shows a table: repo, tier, and status of each tracking field.

### Gap Analysis

```bash
# Check what a specific repo is missing
python3 sdlc_manager.py rollout gap-analysis --repo infiquetra-core
python3 sdlc_manager.py rollout gap-analysis --repo infiquetra-auth
```

Gap analysis checks:
1. **Labels**: Are all 40+ SDLC labels present? Lists any missing.
2. **Templates**: Are all required issue templates present? Lists missing template files.
3. **Project**: Is the repo linked to its project board?
4. **CLAUDE.md**: Does CLAUDE.md exist with an SDLC guidance section?

### Deploy Labels

```bash
# Deploy (or update) all SDLC labels to a repo
python3 sdlc_manager.py rollout deploy-labels --repo infiquetra-core
```

Uses `gh label create --force` — creates new labels and updates existing ones.
Safe to run multiple times (idempotent).

### Deploy Templates

```bash
# Deploy all required issue templates to a repo
python3 sdlc_manager.py rollout deploy-templates --repo infiquetra-core

# Tier 3 repos get minimal templates (defect + enhancement only)
python3 sdlc_manager.py rollout deploy-templates --repo infiquetra-claude-plugins
```

Copies templates from `infiquetra-sdlc` checkout into `.github/ISSUE_TEMPLATE/` in the
target repo via GitHub API. Creates or updates template files.

### Deploy All (Labels + Templates)

```bash
# Deploy labels and templates in one operation + show gap report
python3 sdlc_manager.py rollout deploy-all --repo infiquetra-core
```

Runs `deploy-labels` and `deploy-templates` in sequence, then produces a gap report
showing what still needs attention (claude_md, project board mapping).

## Natural Language Examples

**"How's the SDLC rollout going?"**
-> `rollout status`

**"Which repos still need setup?"**
-> `rollout status` — look for any field that is not `complete`

**"What's missing from infiquetra-auth?"**
-> `rollout gap-analysis --repo infiquetra-auth`

**"Set up SDLC on infiquetra-core"**
-> `rollout deploy-all --repo infiquetra-core`

**"Deploy labels to all Infiquetra repos"**
-> Run `rollout deploy-labels` for each repo

**"Is infiquetra-core compliant?"**
-> `rollout gap-analysis --repo infiquetra-core`

## Deployment Workflow

### Full Setup for a New Repo

```bash
# 1. Check current state
python3 sdlc_manager.py rollout gap-analysis --repo infiquetra-core

# 2. Deploy labels and templates
python3 sdlc_manager.py rollout deploy-all --repo infiquetra-core

# 3. Remaining steps (manual or via other commands):
#    - Add SDLC guidance section to CLAUDE.md
#    - Confirm repo is linked to project board
```

### Bulk Rollout

```bash
# Check status first
python3 sdlc_manager.py rollout status

# For each pending repo, run gap analysis then deploy
python3 sdlc_manager.py rollout gap-analysis --repo infiquetra-auth
python3 sdlc_manager.py rollout deploy-all --repo infiquetra-auth
# ... repeat for each repo
```

### Verifying Existing Setup

```bash
# Run gap analysis to confirm all fields are present
python3 sdlc_manager.py rollout gap-analysis --repo infiquetra-core

# Check if rollout status reflects current state
python3 sdlc_manager.py rollout status
```

## Special Cases

### Tier 3 Repos (Claude Tooling)

- Deploy only defect and enhancement templates (not capability, objective, exploration, context-update)
- `project` field is `n/a` — these repos are excluded from project board automation
- Labels still apply (useful for tracking issues even without project board)

## Reference Documents

- `references/work-hierarchy.md` — Initiative, Objective, Capability hierarchy reference
- `$INFIQUETRA_SDLC_PATH/config/rollout-status.json` — Live rollout tracking data
- `$INFIQUETRA_SDLC_PATH/config/project-mappings.json` — Repo-to-project mappings
