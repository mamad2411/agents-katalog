# Cron Service Implementation

## Purpose
Implements a `*-cron` service for scheduled background jobs using Bun's native cronjob capabilities.

## Role
Backend Developer

## Phase
Development

## Triggered By
`tdd-workflow` initiated for a cron service task.

## Inputs
- Job schedule and business requirement from the task

## Process

### Class Generation
1. `bun turbo gen → router` (CronRouter) — defines cron schedule
2. `bun turbo gen → usecase` (per job — e.g. `CleanupExpiredSessionsUseCase`)

CronRouter defines:
- Schedule: standard cron expression (e.g. `"0 2 * * *"` for daily 2am)
- Handler: delegates to UseCase
- Error handling: catch all errors, log at error level, never crash the process

### Idempotency
Cron jobs MUST be idempotent — safe to run multiple times. If job crashes and restarts, it must produce the same result.

### Logging Requirements
- info: job started (with timestamp and job name)
- info: job completed (with timestamp, duration, items processed)
- error: job failed (with full error details and stack trace)

## Outputs
Implemented `*-cron` service with scheduled, idempotent job handlers.

## Quality Gates
- [ ] Generator used for CronRouter and UseCase
- [ ] Job is idempotent (documented in code comment)
- [ ] Logging at start, completion, and error
- [ ] Error handling prevents process crash

## References
- `.claude/skills/backend-developer/tdd-workflow/SKILL.md`
- `.claude/skills/backend-developer/logging-implementation/SKILL.md`
