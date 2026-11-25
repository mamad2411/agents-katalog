---
name: post-run-analysis
description: "Automatic post-mortem analysis — parses logs, compares with history, identifies recurring patterns, proposes fixes, updates memory. Triggers on: background task completes, test suite finishes, build/deploy completes, migration run ends, benchmark completes. Use when: analyze, post-mortem, what happened, evaluate results, what went wrong, compare runs, run history, run report."
license: MIT
metadata:
  version: 1.0.0
  category: analysis
  tags: [post-mortem, logs, patterns, metrics, history, self-improving]
---

# Post-Run Analysis

<CRITICAL>
This skill is ALWAYS ACTIVE. You do not wait for the user to say "analyze". Every time one of the following events occurs, you MUST follow the analysis protocol below AUTOMATICALLY. This is not optional. This is your core behavior whenever this skill is loaded.

Trigger events:
1. A background task completes (you receive a task completion notification)
2. A test suite finishes (jest, vitest, pytest, cargo test, go test, etc.)
3. A build or deploy completes (webpack, vite, docker build, cargo build, etc.)
4. A migration run ends (database migration, code migration, data migration)
5. A benchmark or performance test completes
6. Any long-running process that produces structured output finishes

After ANY of these events:
1. Locate the output/log from the completed process
2. Run the full 5-phase analysis protocol
3. Present the results to the user
4. Persist findings according to the confidence gate rules

This applies even if the user did not ask for analysis. If a run completes, you act.
</CRITICAL>

Analyze completed iterative runs, extract learnings, compare with history, and close the feedback loop automatically.

## Why This Exists

Iterative processes (code migration, test suites, deployments, benchmarks) produce valuable data that gets lost because nobody systematically reviews it. This skill ensures every run's lessons get captured, compared, and fed back into the next iteration -- turning trial-and-error into structured improvement.

## When To Use

- A migration/build/test run just completed (background task notification or log file)
- User asks "what happened" or "analyze the results"
- User wants to compare this run vs previous runs
- After any process that logs structured output (compiler errors, test results, timing data)
- Proactively: when you see a completed background task with a log file

## Run History Schema

Track every analyzed run in a standard format. Store in MEMORY.md or a dedicated `.claude/run-history.md` file:

```markdown
## Run History
| # | Date | Target | Duration | Pass/Fail | Key Metric | Delta |
|---|------|--------|----------|-----------|------------|-------|
| 7 | 2026-03-17 | test-suite | 42s | PASS | 98% coverage | +2% |
| 6 | 2026-03-16 | test-suite | 51s | FAIL | 96% coverage | -1% |
| 5 | 2026-03-15 | migration | 3m12s | PASS | 847/900 files | +23 |
```

### Schema Rules
- **#**: Auto-incrementing run number, scoped per target
- **Date**: ISO date (YYYY-MM-DD)
- **Target**: Short identifier for what ran (test-suite, migration, build, deploy, benchmark-name)
- **Duration**: Wall-clock time
- **Pass/Fail**: Binary outcome based on exit code or threshold
- **Key Metric**: The single most important number for this run type
- **Delta**: Change from previous run of the same target (use `--` for first run)

## The Analysis Protocol

### Phase 1: Gather Data

1. **Find the log**: Look for the most recent log file (run output, build log, test results). Common locations:
   - `run*-output.log` in project root
   - Background task output files
   - Project artifact directories (`.artifacts/`, `build/`, `output/`, `dist/`, etc.)
   - CI/CD output
   - stdout/stderr from the just-completed process

2. **Extract key metrics** from the log:
   - Duration / timing
   - Success/failure counts
   - Error categories and counts
   - Resource usage (API calls, tokens, cost)
   - Any scores or quality metrics

3. **Find artifacts**: Intermediate outputs, best versions, manifests

### Phase 2: Compare With History

1. **Load run history** from project memory (MEMORY.md, `.claude/run-history.md`, or equivalent)
2. **Build comparison table**: This run vs previous runs on same target
3. **Identify trends**: Improving? Regressing? Stalled?
4. **Flag anomalies**: Unexpectedly good/bad results vs baseline

### Phase 3: Error Pattern Analysis

1. **Categorize errors** by type (group by error code, message pattern)
2. **Identify recurring errors** that appear across multiple runs
3. **For each recurring error**: Is there an existing fix? Was it supposed to be fixed? Did the fix regress?
4. **Distinguish root causes from symptoms**: Syntax errors can mask semantic errors. Count errors AFTER fixing syntax first.

### Phase 4: Actionable Recommendations

Classify each finding as one of:

- **FIXED**: Already have a fix/rule for this -- verify it is working
- **FIXABLE**: Clear pattern that can be automated (new rule, prompt change, config tweak)
- **NEEDS_INVESTIGATION**: Unclear root cause, needs deeper analysis
- **ACCEPTED**: Known limitation, not worth fixing now

For FIXABLE items, propose specific changes:
- Which file to modify
- What the fix looks like
- Expected impact

#### Confidence Gate for Persistence

Not every finding should be persisted to memory. Apply this filter:

- **FIXABLE**: Persist to memory. These are actionable and should be tracked.
- **NEEDS_INVESTIGATION**: Persist to memory. These need follow-up and should not be forgotten.
- **FIXED**: Note in the run report only. Do not persist -- the fix already exists.
- **ACCEPTED**: Note in the run report only. Do not persist -- consciously accepted trade-offs do not need tracking.

This keeps memory lean. Only items that require future action get stored.

### Phase 4.5: Secret Sanitization

**Before writing ANY content to memory, run history, or persistent files, scan every field for secrets and redact them.** This is non-negotiable. Run reports and history files may be committed to version control.

#### Patterns to detect and redact:

| Pattern | Example | Replacement |
|---------|---------|-------------|
| API keys | `sk-proj-abc123...`, `sk-ant-...` | `<REDACTED_API_KEY>` |
| GitHub tokens | `ghp_xxxx`, `github_pat_xxxx` | `<REDACTED_GITHUB_TOKEN>` |
| AWS keys | `AKIA...`, `aws_secret_access_key=...` | `<REDACTED_AWS_KEY>` |
| Bearer tokens | `Bearer eyJhb...` | `Bearer <REDACTED_TOKEN>` |
| Generic tokens | `token: abc123...`, `token=abc123...` | `token: <REDACTED>` |
| Passwords | `password=secret123` | `password=<REDACTED>` |
| Connection strings | `postgres://user:pass@host/db` | `<REDACTED_CONNECTION_STRING>` |
| MongoDB URIs | `mongodb://user:pass@...` | `<REDACTED_CONNECTION_STRING>` |
| Redis URIs | `redis://:pass@host` | `<REDACTED_CONNECTION_STRING>` |
| Absolute home paths | `/home/username/...`, `/Users/name/...` | `<PROJECT_PATH>/...` |
| Email addresses | `user@domain.com` | `<REDACTED_EMAIL>` |
| Internal IP addresses | `192.168.x.x`, `10.x.x.x` | `<REDACTED_IP>` |
| Private keys | `-----BEGIN RSA PRIVATE KEY-----` | `<REDACTED_PRIVATE_KEY>` |
| JWT tokens | `eyJhbG...` (3-part base64) | `<REDACTED_JWT>` |
| High-entropy strings | Base64 blobs, hex strings > 20 chars | `<REDACTED_SECRET>` |

#### If uncertain whether something is a secret:
- Default to redacting. False positives are harmless; leaked secrets are not.
- When in doubt, ask the user before persisting.

### Phase 5: Update Memory & Artifacts

1. **Update project memory** with run results (add to MEMORY.md or equivalent)
2. **Update run history** table (append new row to the run history schema)
3. **Save new learnings** as memory files if they are novel -- only FIXABLE and NEEDS_INVESTIGATION findings
4. **Update warm-start/artifacts** if this run produced better intermediate results
5. **Update skill files** if learnings affect project conventions

## Output Format

Present the analysis as:

```
## Run [N] Analysis: [target name]

### Metrics
| Metric | This Run | Previous Best | Delta |
|--------|----------|---------------|-------|
| ...    | ...      | ...           | ...   |

### Error Breakdown
| Error Type | Count | Recurring? | Status |
|------------|-------|------------|--------|
| ...        | ...   | ...        | FIXED/FIXABLE/... |

### Recommendations
1. [FIXABLE] Description -- File: path, Change: what
2. [NEEDS_INVESTIGATION] Description -- Why unclear
3. ...

### Memory Updates
- [x] Run history updated (#N)
- [x] New finding persisted: description
- [ ] Warm-start updated (if better than previous)

### Ready for Next Run?
[Yes/No] -- [what needs to change first]
```

## Adapting to Different Project Types

This skill is generic. Adapt the metrics and error analysis to the project:

- **Code migration**: errors = compiler errors, metrics = LOC/score/unsafe count
- **Test suites**: errors = test failures, metrics = pass rate/coverage/timing
- **Deployments**: errors = deploy failures, metrics = uptime/latency/rollback count
- **Benchmarks**: errors = N/A, metrics = performance numbers/regression detection
- **Build pipelines**: errors = build failures, metrics = build time/artifact size/warnings

The key principle is the same: **extract -> compare -> categorize -> recommend -> persist**.

## Anti-Patterns

- Do not just list errors -- categorize them and check if they are recurring
- Do not skip the comparison with previous runs -- trends matter more than snapshots
- Do not update memory with every small detail -- only FIXABLE and NEEDS_INVESTIGATION findings
- Do not recommend changes without checking if a fix already exists
- Do not claim improvement without verifying (syntax errors can mask real error counts)
- Do not persist FIXED or ACCEPTED findings to memory -- they belong in the run report only
- Do not write secrets, tokens, or absolute paths to persistent files -- sanitize first

## Slash Commands Reference

| Command | Action |
|---------|--------|
| `/analyze` | Force analysis of the most recent run |
| `/runs` | Browse run history, show trends and comparisons |
| `/compare <run1> <run2>` | Compare two specific runs side by side |

## Integration Notes

### With version control
- Run history files should be committed to the repository so analysis persists across sessions.
- Sanitization ensures no secrets leak into committed files.

### With learn-by-mistake
- Post-run-analysis identifies error patterns; learn-by-mistake captures the lessons.
- When a FIXABLE finding is also a recurring error, suggest creating a lesson via `/learn`.
- Run history provides the data that proves whether a lesson's fix actually worked.

### With other skills
- This skill is reactive -- it activates on run completion events, not on explicit invocation (though `/analyze` forces it).
- It cooperates with any build, test, or deployment workflow.
- It does not interfere with process output or runners.
