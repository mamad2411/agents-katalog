---
name: agent-progress
description: "Sub-phase progress tracking protocol for all agents. Enables debugging pipeline execution by writing structured status files at every step transition. Injected into every agent to provide observability into internal workflows."
---

# Agent Progress Tracking Protocol

## Overview

Every agent MUST write a progress status file at each step transition. This enables debugging stalled pipelines, understanding agent behavior, and resuming from failures.

## File Location

```
.claude/specs/[feature]/agent-status/[agent-name].md
```

Example: `.claude/specs/water-delivery/agent-status/product-manager.md`

Create the `agent-status/` directory if it doesn't exist.

## When to Update

Write or update the status file at these moments:

1. **Agent start** — write initial file with all steps PENDING
2. **Step transition** — mark previous step COMPLETE, current step IN_PROGRESS
3. **Step skip** — mark as SKIPPED with reason
4. **Error** — mark as FAILED with error details
5. **Agent complete** — mark final step COMPLETE, set overall status to DONE
6. **Agent blocked** — mark current step as BLOCKED with blocker description

## Status Values

| Status | Meaning |
|--------|---------|
| `PENDING` | Not yet started |
| `IN_PROGRESS` | Currently executing |
| `COMPLETE` | Successfully finished |
| `SKIPPED` | Intentionally skipped (reason required) |
| `FAILED` | Error occurred (error details required) |
| `BLOCKED` | Waiting on external dependency |
| `RETRYING` | Failed once, retrying |

## File Format

```markdown
# Agent Status — [agent-name]

## Summary
- **Agent:** [agent-name]
- **Phase:** [pipeline phase number]
- **Feature:** [feature-name]
- **Status:** IN_PROGRESS / DONE / FAILED / BLOCKED
- **Started:** [ISO timestamp]
- **Last Updated:** [ISO timestamp]
- **Duration:** [elapsed time]

## Steps
| # | Step ID | Name | Status | Started | Completed | Notes |
|---|---------|------|--------|---------|-----------|-------|
| 1 | read-context | Read project config | COMPLETE | 14:30:01 | 14:30:05 | Found NestJS + React stack |
| 2 | assess-requirements | Requirements clarity check | COMPLETE | 14:30:05 | 14:30:08 | Requirements are vague — full discovery needed |
| 3 | tier-1-discovery | Core questions (Tier 1) | IN_PROGRESS | 14:30:08 | — | Q3 of 6 asked |
| 4 | tier-2-discovery | Domain-adaptive questions | PENDING | — | — | |
| 5 | scope-discipline | MVP scope framing | PENDING | — | — | |
| 6 | write-prd | Write PRD (10 sections) | PENDING | — | — | |
| 7 | gap-analysis | Specification gap analysis | PENDING | — | — | |
| 8 | approval-gate | Request user approval | PENDING | — | — | |

## Sub-Step Detail
[For steps with internal progression, track granularity here]

### Step 3 — tier-1-discovery
| Sub-step | Status | Detail |
|----------|--------|--------|
| Q1 — Core purpose | COMPLETE | User described: "task management for remote teams" |
| Q2 — Target users | COMPLETE | B2B — team managers and employees |
| Q3 — Platforms | IN_PROGRESS | Waiting for user response |
| Q4 — Scope approach | PENDING | |
| Q5 — Core features | PENDING | |
| Q6 — Out of scope | PENDING | |

## Output Files
| File | Status | Detail |
|------|--------|--------|
| requirements.md | NOT_STARTED | |
| feature_list.json | NOT_STARTED | |

## Errors
[Log any errors encountered during execution]

| Timestamp | Step | Error | Recovery |
|-----------|------|-------|----------|
| — | — | — | — |

## Decision Log
[Record key decisions made during execution]

| Timestamp | Decision | Reasoning |
|-----------|----------|-----------|
| 14:30:08 | Full discovery needed | Requirements vague — no specific acceptance criteria provided |
```

## Update Protocol

### On Agent Start

```
1. Read your step table from the ## Progress Steps section in your agent definition
2. Create the status file with all steps set to PENDING
3. Set overall Status to IN_PROGRESS
4. Set Started timestamp
```

### On Step Transition

```
1. Mark previous step as COMPLETE with Completed timestamp
2. Mark new step as IN_PROGRESS with Started timestamp
3. Update Last Updated timestamp
4. Add any Notes for completed step (brief: what was found/decided)
```

### On Sub-Step Progress

For steps with internal iterations (e.g., asking multiple questions, processing multiple files):
```
1. Add a Sub-Step Detail section under ## Sub-Step Detail
2. Track each iteration with its own status
3. Update the parent step's Notes with progress count (e.g., "Q3 of 6 asked")
```

### On Error

```
1. Mark current step as FAILED
2. Add entry to ## Errors table with timestamp, step, error description, and recovery action
3. If retrying, mark step as RETRYING
4. If unrecoverable, set overall Status to FAILED
```

### On Skip

```
1. Mark step as SKIPPED
2. Add reason in Notes column (e.g., "SMALL task — skipped", "Already in project-config.md")
```

### On Output File Creation

```
1. Update ## Output Files table when a file is written
2. Status values: NOT_STARTED, PARTIAL (with detail), COMPLETE
3. For partial writes, note which sections are done (e.g., "Sections 1-5 of 10")
```

### On Key Decision

```
1. Add entry to ## Decision Log when making a non-trivial choice
2. Include reasoning so debugging can understand WHY a path was taken
```

### On Agent Complete

```
1. Mark final step as COMPLETE
2. Set overall Status to DONE
3. Update Duration
4. Ensure all Output Files are marked COMPLETE or explain why not
```

## Performance Rules

- **Write frequency:** Update the file at every step transition. For long steps with sub-steps, update at sub-step transitions too.
- **Keep it brief:** Notes should be 1 line. Don't write paragraphs.
- **Timestamps:** Use `HH:MM:SS` format (time only, not full ISO — saves space).
- **Don't block on writes:** If the Write tool fails, continue execution. Progress tracking should never block the actual work.
- **Incremental updates:** Use the Edit tool to update specific rows, not rewrite the entire file each time.

## Reading Agent Status (for commands and debugging)

To check agent status:
```
Glob(".claude/specs/*/agent-status/*.md")
Read(".claude/specs/[feature]/agent-status/[agent-name].md")
```

To find stalled agents:
```
Grep("IN_PROGRESS", ".claude/specs/*/agent-status/", glob="*.md")
```

To find failures:
```
Grep("FAILED", ".claude/specs/*/agent-status/", glob="*.md")
```

## Anti-Patterns

- **No status updates** — running an agent without writing progress files; the orchestrator has no visibility into what's happening
- **Stale IN_PROGRESS** — leaving a status file at IN_PROGRESS after the agent has finished or failed; clean up on exit
- **Progress without timestamps** — status files missing timestamps make it impossible to detect stalls
- **Overwriting instead of appending** — replacing the entire status file on each update instead of appending sub-steps; history is lost
- **No failure details** — writing FAILED without an error message or context; debugging becomes impossible

## Checklist

- [ ] Status file created at agent start with IN_PROGRESS
- [ ] Sub-step transitions logged with timestamps
- [ ] Status updated to COMPLETED or FAILED on exit
- [ ] Error details included in FAILED status
- [ ] Status files queryable via Grep for debugging
