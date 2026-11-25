---
name: customer-feedback-scan
description: Scan Slack channels and other sources for customer feedback patterns
alwaysApply: false
---

# Customer Feedback Scan

Scans registered Slack channels (and optionally call transcripts) for customer feedback signal. Produces a dated analysis with themes, severity, and actionable patterns.

## Trigger

"scan for customer feedback" or "run feedback scan"

## Pre-Run

1. Read `.claude/skills/customer-feedback-scan/gotchas.md` (if it exists)
2. Read `customer-intelligence/README.md` for the channel registry and source list

## Execution

### Phase 1: Setup
- Load the channel list from `customer-intelligence/README.md`
- Determine scan window (default: last 7 days, or since last scan per `runs.log`)

### Phase 2: Slack Scan
For each registered channel:
1. Read messages in the scan window
2. Filter for product-relevant signal (not general chatter, not bot messages)
3. Classify each signal:
   - **Bug report** — something is broken
   - **Feature request** — customer wants something new
   - **Confusion** — customer doesn't understand how something works
   - **Churn risk** — customer expressing frustration or intent to leave
   - **Positive signal** — customer expressing satisfaction or success

### Phase 3: Synthesis
- Group signals by theme (not by channel)
- For each theme: count, severity, example quotes, affected customer segments
- Identify co-occurring patterns (e.g., confusion + churn risk on the same feature)

### Phase 4: Output
Write to `customer-intelligence/slack-scans/YYYY-MM-DD-scan.md`:

```markdown
# Slack Feedback Scan — YYYY-MM-DD
**Window:** [start] to [end]
**Channels scanned:** [list]

## Top Themes
1. [Theme] — [count] signals, [severity]
   - Example: "[quote]" — [channel, date]
   - Affected: [customer segment]

## Co-occurring Patterns
- [Pattern description]

## Proposed Actions
- [ ] [Action — owner suggestion, project link if relevant]
```

### Phase 5: Cross-Reference
- If any theme maps to an active project, note it in the scan output
- If any theme challenges or confirms a belief, flag it for `strategy/beliefs.md` update

## Post-Run

Append to `.claude/skills/customer-feedback-scan/runs.log`:
```
[date] | [channels scanned] | [signals found] | [themes identified]
```
