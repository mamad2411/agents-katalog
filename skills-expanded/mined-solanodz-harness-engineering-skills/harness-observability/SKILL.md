---
name: harness-observability
description: >-
  See what the agent actually did — captured logs, health checks, and debug
  commands. Use when the agent says it worked but you can't tell why, or when
  failures are hard to diagnose.
---

# Harness Observability

## What this does for you

- **Evidence you can read** — test output and logs saved, not lost in the terminal
- **Health before smoke tests** — know the app is up before declaring success
- **Faster debugging** — documented commands instead of guessing what ran

If you cannot see what the agent did, you cannot fix what it broke (Lesson 11). Observability belongs **inside** the harness, not as an afterthought.

## What to make observable

| Signal | Purpose | Where |
|--------|---------|-------|
| Structured logs | What ran, what failed | stdout, files in `logs/` |
| Service state | Is app running? DB up? | health endpoints, status bar |
| Verification results | Pass/fail evidence | progress.md, feature_list evidence |
| Change diff | What the agent modified | git diff, git log |
| Runtime errors | Post-implementation bugs | console, test output |

## Practical patterns

### 1. Verification with captured output

```bash
npm test 2>&1 | tee .harness/last-test-run.log
echo "Exit: $?" >> .harness/last-test-run.log
```

The agent (and you) can read the log afterward.

### 2. Visible status in the app

For apps with UI (like the course capstone project):

- Status bar: indexed docs, last sync, errors
- On-screen health indicators
- Agent can verify state without guessing

### 3. `.harness/` directory (optional)

```
.harness/
├── last-init.log
├── last-test-run.log
├── session-metrics.json
└── README.md  # what each file contains
```

Add `.harness/*.log` to `.gitignore` if ephemeral; commit metrics if they are evidence.

### 4. Documented debug commands

In AGENTS.md or session-handoff:

```markdown
## Debug
- View logs: `tail -50 logs/app.log`
- Health check: `curl localhost:3000/health`
- DB status: `npm run db:status`
```

## Integration with verification

Observability + verification = complete evidence:

```json
{
  "evidence": [{
    "date": "2026-06-16",
    "commands": ["./init.sh", "npm run test:e2e"],
    "result": "pass",
    "artifacts": [".harness/last-test-run.log"],
    "observations": "Status bar shows 42 docs indexed"
  }]
}
```

## Agent failure diagnosis

When the agent fails repeatedly:

1. Can it **execute** the command? (Gulf of Execution)
2. Can it **interpret** the output? (Gulf of Evaluation)
3. Is the output **visible** in its context?
4. Is there a **feedback loop** to correct?

Close the gap with harness, not longer prompts.

## Ablation study (Project 06)

For the capstone, remove subsystems one at a time and measure:

```
Baseline (full harness)     → success rate X%
Without observability       → success rate Y%
Without verification      → success rate Z%
...
```

Document results in progress.md.

## Anti-patterns

- Agent declares done without verification logs
- Errors only in ephemeral terminal (not captured)
- No health check before smoke tests
- Observability only in production, not in dev harness

## Course reference

- Lesson 11: Why observability belongs in the harness
- Project 06: Full harness with observability and debugging
- [references/course/gotchas.md](../../references/course/gotchas.md)

## Related skills

- `harness-verification` — pass/fail evidence
- `harness-evaluator` — sprint contracts and rubrics (process observability)
- `harness-lifecycle` — session logs in progress/handoff
- `harness-audit` — detect observability gaps
- `harness-e2e` — runtime signals from smoke/E2E runs
