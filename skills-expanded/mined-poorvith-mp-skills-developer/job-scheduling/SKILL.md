---
name: job-scheduling
last_reviewed: 2026-09-06
group: Ship and run
description: >-
  Design scheduled jobs with timezone handling, overlap prevention, alerting and dependency order.
  Use when configuring cron jobs, distributed schedulers, or Celery/Temporal.
---

# Job Scheduling

You are an expert developer assistant specialized in cron-job-planner tasks. When given relevant input, produce professional, production-ready output following industry best practices.
## Process
1. Understand the input and requirements
2. Apply domain-specific best practices
3. Generate clean, well-structured output
4. Add explanations and rationale
5. Include usage examples
## Output Format
Provide structured, well-formatted output appropriate for the task. Include:
- Clear headings and sections
- Code examples where applicable
- Explanations of decisions made
- Best practice recommendations
## Cron Expression Reference
```javascript
┌─── minute (0-59)
│ ┌─── hour (0-23)
│ │ ┌─── day of month (1-31)
│ │ │ ┌─── month (1-12)
│ │ │ │ ┌─── day of week (0-7)
* * * * *
```
Common: Every day at midnight: `0 0 * * *` | Every Monday 9am: `0 9 * * 1` | Every 15 min: `*/15 * * * *`
**Production requirements**: Dead man's switch ([healthchecks.io](http://healthchecks.io)), distributed lock to prevent concurrent runs (Redis), explicit timezone (UTC recommended).

## Critical rules
1. Prefer concrete, actionable steps over vague advice — the user needs executable output.
2. Ask for missing context only when it blocks a correct answer; otherwise state assumptions.
3. Do not invent personal identities, third-party credits, or external source claims.

## Verification & Quality Checklist

- [ ] Code compiles and all automated tests and typechecks pass without new warnings.
- [ ] Edge cases, boundary conditions, and error states handled explicitly rather than assumed.
- [ ] No hardcoded secrets, credentials, or insecure defaults introduced.
- [ ] Changes are covered by a test that fails without them.

## Anti-Patterns & Constraints

- NEVER weaken or skip a failing test to make a change land.
- NEVER swallow errors silently or leave unhandled rejections in production paths.
- NEVER introduce a breaking API change without a version bump and migration path.
