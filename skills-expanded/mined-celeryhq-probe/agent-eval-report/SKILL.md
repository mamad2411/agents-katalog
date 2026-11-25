---
name: agent-eval-report
description: Use when generating HTML evaluation reports for AI agent test suites — self-contained HTML with embedded screenshots, pass/fail results grouped by functional and compliance
---

# Agent Eval — Report

## Overview

Generates a single self-contained HTML report from eval results. All screenshots embedded as base64. No external dependencies.

## Input

After running all scenarios, you have:
- Suite name, date, target URL
- Per scenario: name, step screenshots, verify results (status/explanation/screenshot/category)

## Process

1. Read the report template `report-template.html` co-located in this skill's own directory (`.claude/skills/agent-eval-report/report-template.html` when running from the repo root)
2. Calculate pass/fail/warning counts and percentages
3. Build sidebar items grouped by Functional and Compliance
4. Build scenario detail sections with screenshots and verify results
5. Embed all screenshots as base64 data URIs
6. Replace `{{PLACEHOLDER}}` tokens in the template
7. Write to `eval-results/<timestamp>/report.html`

## Screenshot Embedding

```javascript
const fs = require('fs');
const base64 = fs.readFileSync(screenshotPath).toString('base64');
const dataUri = `data:image/png;base64,${base64}`;
```

## Sidebar Logic

A scenario's status dot color:
- Green: all verify checks passed
- Red: any check failed
- Yellow: any warning, no failures

A scenario appears under **Functional** if it has content/behavioral/ai-judge checks.
A scenario appears under **Compliance** if it has compliance checks.
A scenario can appear in both sections.

## AI Commentary

Generate per scenario:
- All passed: brief summary of what went well
- Any failed: explain what went wrong, potential causes
- Warnings: note what was borderline

## Output

Write report to: `<project>/eval-results/<timestamp>/report.html`
Open in browser: `open eval-results/<timestamp>/report.html`
