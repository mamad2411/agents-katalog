---
name: progress-tracker
description: "Track loop metrics, trends, improvements. Invoke: /progress-tracker."
user-invocable: true
---

# Progress Tracker

Queries: metrics, patterns, actions. Daily.

## Queries (7d)

```bash
gh issue list --label "audit" --state all --json number,title,state,createdAt,closedAt,labels --limit 100
gh issue list --label "ci-fix" --state all --json number,title,state,createdAt,closedAt,labels --limit 50
gh issue list --label "ready" --state open --json number,title
gh issue list --label "in-progress" --state open --json number,title
gh issue list --label "has-pr" --state open --json number,title
gh issue list --label "agent-failed" --state open --json number,title
gh issue list --label "agent-skip" --state open --json number,title,createdAt
gh pr list --state merged --json number,title,mergedAt,headRefName --limit 50
gh run list --branch main --limit 20 --json conclusion,createdAt
gh issue list --label "meta-improvement" --state all --json number,title,state
cat .claude/agent-spend/sessions.jsonl 2>/dev/null | tail -100
```

Per-issue attribution: `.claude/agent-spend/sessions.jsonl` = `{date,timestamp,costUsd,model,adapter,status,issueNumber?,inputTokens?,outputTokens?,numTurns?}` (single spend sink owned by agent-core's recordSpend seam; NOT total Claude spend — use ccusage for ground-truth totals). It only holds `mbe agent run`/`mbe agent eval` sessions. `/idea-to-prod:implement-queue` workers never reach `recordSpend`, so their usage is `subagent_tokens`/`cost_usd` in `metrics/queue-telemetry.jsonl` (#5885). Read both with `node -e 'import("./scripts/sensors-registry.mjs").then(({SENSORS})=>{const s=SENSORS.find(x=>x.id==="agentCost");const d=s.collect({root:process.cwd(),now:new Date()});console.log(s.format(d,"agentCost"))})'`. If queue `cost_usd` is unknown, report the tokens and say the cost is unknown. Never report it as $0.

## Metrics

| Metric        | Formula                  | Target |
| ------------- | ------------------------ | ------ |
| Created (7d)  | audit+ci-fix             | -      |
| Closed (7d)   | audit+ci-fix             | -      |
| Closure Rate  | Closed/Created           | >80%   |
| Time-to-Close | mean(closedAt-createdAt) | <24h   |
| Agent Success | has-pr/(has-pr+failed)   | >70%   |
| CI Pass       | success/total main       | >95%   |
| Queue         | count ready              | <5     |
| Stale         | ready>7d                 | 0      |
| Blocked       | agent-failed             | 0      |
| Skipped       | agent-skip               | 0      |
| Daily Spend   | Σ costUsd (attributed)   | <$10   |
| 7d Spend      | Σ costUsd (attributed)   | <$50   |
| Cost/Issue    | 7d/closed (attributed)   | <$2    |

## Analysis

1. Recurring types → systemic?
2. Agent failures → pattern?
3. CI unstable → same job?
4. Queue bottleneck?
5. Cost efficiency?

## Log

Append `.claude/improvement-loop/log.md` (then run `node scripts/cap-improvement-log.mjs` to keep only the newest 60 entries; older ones live in git history):

```markdown
## YYYY-MM-DD

### Metrics

[Table with Closed/Created/Rate/Time/Success/Pass/Queue/Stale/Skip/Spend/Cost]

### Patterns

- [Findings]

### Recommendations

- [Actions]

### Skipped Issues

[Manual review]
```

Query skipped: `gh issue list --label "agent-skip" --state open --json number,title,createdAt --jq '.[] | "  #\(.number) \(.title)"'`

Summary: "N skipped after max retries"

**Append only.**

## Persist

The append above is worthless until it is committed — cloud routines run in
ephemeral checkouts, so an uncommitted `log.md` dies with the checkout:

```bash
node scripts/persist-metrics.mjs --routine progress-tracker
```

It stages every **durable** path with a diff (never `git add -A`), commits on
a branch, and opens a PR titled `chore(metrics): progress-tracker <YYYY-MM-DD>`
labeled `has-pr` — metrics-only diffs auto-merge via the low-risk fast path.
No diff, no commit, exit 0. `.claude/improvement-loop/log.md` is already
declared `durable: true` in `scripts/metrics-store.mjs`, so it is covered
without enumerating anything by hand.

Run this even when the day's findings are unremarkable. This step is why
#4378 happened: until it existed, this skill only ever appended, and its
entries reached `main` solely because `/optimize-implement-queue` ran later in
the same checkout and swept `log.md` up in _its_ persist. When that routine
stopped producing PRs on 2026-08-16, `log.md` froze on the same date — nine
days with no entry, while the queue kept merging PRs daily. A step that
depends on a different skill happening to run afterwards is not a step.

## Improvement Issues

Pattern 3+ days consistent?

```bash
gh issue create --title "[Meta] <improvement>" --label "meta-improvement" \
  --body "## Observation
<Data>

## Recommendation
<Change>

## Impact
<Outcome>

---
*Identified: $(date +%Y-%m-%d)*"
```

## Thresholds

| Metric  | Green | Yellow   | Red   |
| ------- | ----- | -------- | ----- |
| Closure | >80%  | 50-80%   | <50%  |
| Success | >70%  | 40-70%   | <40%  |
| CI      | >95%  | 85-95%   | <85%  |
| Queue   | <5    | 5-10     | >10   |
| Time    | <24h  | 24-72h   | >72h  |
| Daily   | <$10  | $10-$20  | >$20  |
| 7d      | <$50  | $50-$100 | >$100 |
| Cost    | <$2   | $2-$5    | >$5   |

## Actions

### Pause on Failure >50% (3d)

```bash
gh issue create --title "[Alert] Queue paused — failure >50%" \
  --label "meta-improvement" \
  --body "Success <50%. Pause loop.

$(gh issue list --label agent-failed --state open --json number,title -q '.[] | "- #\(.number): \(.title)"')

Fix, improve descriptions, re-enable."
```

### Auto-retry Stale (3+ days)

Re-queue issues that have been `agent-failed` for 3+ days (excludes `agent-skip`,
caps at 2/run). Tested logic lives in `scripts/auto-retry-stale.mjs`:

```bash
node scripts/auto-retry-stale.mjs           # re-queue via @mbe/gh-client's markReady + comment
node scripts/auto-retry-stale.mjs --dry-run # report selection, mutate nothing
```

The selection rule (`selectStaleForRetry`) is a pure, unit-tested function
(`scripts/__tests__/auto-retry-stale.test.mjs`); the GitHub mutations run via
`@mbe/gh-client`'s label machine (`markReady` + `label.apply`, #2933). Max 2/run.

### Queue Adjust

Queue >10 + success >70% → `/loop 15m /idea-to-prod:implement-queue`

Queue 0 for 3d → reduce audit or expand

### Features

```bash
gh issue list --label "feature" --state all --json number,title,state,labels --limit 100
gh issue list --label "tracking" --state open --json number,title,body
```

% = closed/total in body.

### Reverts

```bash
git log --oneline --grep="Revert" --since="7 days ago" | wc -l
```

> 3/week → broken code?

## Rules

- Read-only code
- Max 2 meta/run
- Max 2 retry/run
- Append-only log
- Persist before finishing: `node scripts/persist-metrics.mjs --routine progress-tracker` (an uncommitted append is lost with the checkout)
- Per-issue attribution: `.claude/agent-spend/sessions.jsonl` (agent-core sessions, via recordSpend) + `metrics/queue-telemetry.jsonl` (queue workers), both read by the `agentCost` sensor; ccusage = ground-truth totals
- Circuit: 50% over 3+ days
