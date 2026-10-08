---
name: retro
description: Run a sprint/session retrospective to capture what worked, what didn't, and what to improve.
---

# Retrospective Skill

Run a sprint/session retrospective to capture what worked, what didn't, and what to improve.

## When to Use
- After completing a major feature or task
- After a debugging session
- At the end of a development sprint
- After a production incident

## Process

1. **Gather Data**: Review what happened in this session/sprint
   - Read recent git log: `git log --oneline -20`
   - Check files changed: `git diff --stat HEAD~N` — clamp N to the available history first so this doesn't fail on repos with fewer than N commits: `N=$(( $(git rev-list --count HEAD) - 1 )); [ $N -gt 5 ] && N=5`; if `N` is 0 (single commit), fall back to `git log --oneline` / `git show --stat`.
   - Review any error logs or failed attempts

2. **Classify Events**: Sort into categories

   ### What Went Well (Keep)
   - Approaches that worked efficiently
   - Good architectural decisions
   - Tools/commands that saved time

   ### What Didn't Go Well (Stop)
   - Wasted time on wrong approaches
   - Bugs introduced by oversight
   - Communication gaps or unclear requirements

   ### What To Try Next Time (Start)
   - New tools or approaches to try
   - Process improvements
   - Better testing strategies

3. **Extract Action Items**: Concrete, actionable improvements

4. **Identify Patterns**: Look for recurring themes across retros

## Output Format

```
## Retrospective: [date or sprint name]

### Summary
- Duration: [time spent]
- Commits: [count]
- Files changed: [count]
- Lines: +[added] / -[removed]

### 🟢 Keep (What Went Well)
- [item 1]
- [item 2]

### 🔴 Stop (What Didn't Go Well)
- [item 1] → Root cause: [why]
- [item 2] → Root cause: [why]

### 🔵 Start (Try Next Time)
- [item 1] — Expected benefit: [what it improves]
- [item 2] — Expected benefit: [what it improves]

### Action Items
- [ ] [concrete action 1]
- [ ] [concrete action 2]

### Metrics
| Metric | This Sprint | Trend |
|--------|-------------|-------|
| Bugs found in review | N | ↑↓→ |
| Build failures | N | ↑↓→ |
| Test coverage | N% | ↑↓→ |
```

## Rules
- Be honest — the point is improvement, not blame
- Focus on process, not people
- Every "Stop" item needs a root cause
- Every "Start" item needs an expected benefit
- Action items must be specific and achievable (not "be better at X")
- If this is a recurring retro, compare with previous ones to track progress
