---
name: social-linkedin-report
description: "LinkedIn analytics report — profile data, posts (when available), org stats. Use when user says 'linkedin report', 'linkedin analytics', or any reference to LinkedIn performance."
---

# LinkedIn Report — Analytics

Routine that pulls data from LinkedIn via `/int-linkedin` and generates a report.

**Always respond in English.**

## Workflow

### Step 1 — Collect data

```bash
python3 {project-root}/.claude/skills/int-linkedin/scripts/linkedin_client.py summary
python3 {project-root}/.claude/skills/int-linkedin/scripts/linkedin_client.py my_posts 1 10
```

If `my_posts` returns a permission error, inform that approval is needed and use available data.

### Step 2 — Generate report

Use template `.claude/templates/html/custom/social-analytics-report.html` with available data. Mark sections without data as "Pending — requires LinkedIn Advertising API approval".

### Step 3 — Save

```
workspace/social/reports/linkedin/[C] YYYY-MM-DD-linkedin-report.html
```

### Step 4 — Telegram

Notify with available data.
