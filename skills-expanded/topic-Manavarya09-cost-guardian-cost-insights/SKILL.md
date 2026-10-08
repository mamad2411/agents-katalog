---
name: cost-insights
description: "Advanced cost intelligence: efficiency scoring, waste detection, ROI metrics, model savings calculator, anomaly detection, and GitHub badge generation. Use when user says 'insights', 'efficiency', 'waste', 'roi', 'savings', 'anomaly', 'badge', or '/cost-insights'."
argument-hint: "[insights|waste|roi|savings|anomaly|badge]"
allowed-tools: Bash
---

# Cost Insights

Advanced cost intelligence that goes beyond simple tracking. Shows WHERE money is wasted, WHAT you got for your spend, and HOW to spend less.

## Commands

### `/cost-insights` or `/cost-insights report` (default)
Full insights report with all metrics:
```bash
node "${CLAUDE_SKILL_DIR}/../../scripts/insights.js" insights "${CLAUDE_SESSION_ID}"
```
Display the ASCII output as-is.

### `/cost-insights waste`
Detailed waste analysis — redundant reads, failed commands, retry storms:
```bash
node "${CLAUDE_SKILL_DIR}/../../scripts/insights.js" waste "${CLAUDE_SESSION_ID}"
```
Explain each waste type and suggest how to avoid it.

### `/cost-insights roi`
Cost-per-line and cost-per-commit ROI metrics:
```bash
node "${CLAUDE_SKILL_DIR}/../../scripts/insights.js" roi "${CLAUDE_SESSION_ID}"
```
Compare to typical benchmarks ($0.02-0.05/line is good, >$0.10/line is expensive).

### `/cost-insights savings`
Model routing savings calculator — shows what you could save on cheaper models:
```bash
node "${CLAUDE_SKILL_DIR}/../../scripts/insights.js" savings "${CLAUDE_SESSION_ID}"
```
Explain which tasks could safely use Haiku vs Sonnet vs Opus.

### `/cost-insights anomaly`
Check if this session is abnormally expensive:
```bash
node "${CLAUDE_SKILL_DIR}/../../scripts/insights.js" anomaly "${CLAUDE_SESSION_ID}"
```

### `/cost-insights badge [daily|weekly|monthly]`
Generate a GitHub README badge showing AI development cost:
```bash
node "${CLAUDE_SKILL_DIR}/../../scripts/insights.js" badge monthly
```
Give the user the markdown to paste in their README.

## Response Guidelines
- Efficiency scores: 80-100 = great, 60-79 = good, 40-59 = needs work, <40 = poor
- Always suggest actionable improvements for low scores
- For waste: explain WHY each waste happens and HOW to avoid it
- For savings: be honest that model routing requires task-type awareness
- For badges: output the markdown they can paste directly
