---
name: Ship
description: Automated code shipping pipeline — validate, integrate, version, publish, verify. USE WHEN ship, ship it, deploy, push to main, merge and deploy, create PR, land this branch, release, ship dry run, rollback, init ship config, setup shipping.
---

# Ship

Automated code shipping pipeline. One command to go from feature branch to merged PR with validation, review, versioning, and changelog. Project-configurable via `.ship.json`.

Inspired by gstack's `/ship` but adapted for PAI's architecture with configurable soft constraints.

## Customization

**Before executing, check for user customizations at:**
`~/.claude/skills/PAI/USER/SKILLCUSTOMIZATIONS/Ship/`

If this directory exists, load and apply any PREFERENCES.md, configurations, or resources found there. These override default behavior. If the directory does not exist, proceed with skill defaults.

## Voice Notification

**When executing a workflow, do BOTH:**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Running the WORKFLOWNAME workflow in the Ship skill to ACTION"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **WorkflowName** workflow in the **Ship** skill to ACTION...
   ```

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **Ship** | "/ship", "ship it", "ship this", "land this branch", "deploy this" | `Workflows/Ship.md` |
| **ShipDryRun** | "/ship --dry-run", "ship dry run", "simulate ship", "what would ship do" | `Workflows/ShipDryRun.md` |
| **ShipRollback** | "rollback", "revert last ship", "undo deploy", "ship rollback" | `Workflows/ShipRollback.md` |
| **ShipInit** | "init ship", "setup ship config", "create .ship.json", "ship init" | `Workflows/ShipInit.md` |

## .ship.json Config Reference

The pipeline is configured per-project via `.ship.json` in the project root.

```jsonc
{
  // REQUIRED
  "testCommand": "bun test",              // Must exit 0 to pass

  // BUILD (optional)
  "buildCommand": null,                    // Pre-ship build step

  // VERSIONING (optional)
  "versionFile": "package.json",           // Path to version file
  "versionStrategy": "none",              // semver-patch | semver-minor | calver | none

  // CHANGELOG (optional)
  "changelogFile": null,                   // Path to CHANGELOG.md
  "changelogFormat": "none",              // keep-a-changelog | git-log | none

  // REVIEW (defaults on)
  "reviewEnabled": true,                   // Show diff summary before pushing
  "reviewMode": "full",                   // full | quick | skip

  // PR / MERGE
  "prEnabled": true,                       // Create PR (false = direct merge)
  "protectedBranches": ["main"],          // Branches that always require PR
  "autoMergeMain": true,                  // Merge main into branch before ship
  "baseBranch": "main",                   // Target branch

  // DEPLOY (optional)
  "deployCommand": null,                   // Post-merge deploy command
  "healthCheckUrl": null,                  // URL to verify after deploy (must return 2xx)
  "healthCheckTimeout": 30,              // Seconds to wait for health check

  // HOOKS (optional)
  "preShipHook": null,                     // Command before pipeline starts
  "postShipHook": null                     // Command after successful ship
}
```

**All fields except `testCommand` are optional.** Use `/ship init` to auto-generate.

## Pipeline Overview

```
PREFLIGHT → INTEGRATE → VALIDATE → REVIEW → VERSION → DOCUMENT → PUBLISH → VERIFY → [ROLLBACK]
```

- **Hard constraints** (always run): VALIDATE, INTEGRATE, VERIFY, ROLLBACK
- **Soft constraints** (configurable): REVIEW, VERSION, DOCUMENT, PR creation

## Examples

**Example 1: Ship a feature branch**
```
User: "/ship"
→ Loads .ship.json
→ Merges main, runs tests, shows diff, bumps version, creates PR
→ Reports PR URL
```

**Example 2: Check before shipping**
```
User: "/ship --dry-run"
→ Runs full pipeline in read-only mode
→ Reports what WOULD happen, surfaces blockers
```

**Example 3: Setup for a new project**
```
User: "ship init"
→ Detects project type
→ Generates .ship.json with sensible defaults
→ Asks confirmation before writing
```

**Example 4: Something went wrong**
```
User: "rollback last ship"
→ Creates revert commit
→ Pushes revert
→ Reports status
```
