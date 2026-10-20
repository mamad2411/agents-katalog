---
name: social-instagram-report
description: "Instagram analytics report — queries profile stats, recent posts, engagement rates, insights for all connected accounts. Generates HTML report. Use when user says 'instagram report', 'instagram metrics', or any reference to Instagram performance analysis."
---

# Instagram Report — Profile Analytics

Routine that pulls data from Instagram via `/int-instagram` and generates an HTML performance report.

**Always respond in English.**

## Workflow

### Step 1 — Collect data from all accounts

Para cada conta Instagram configurada:

```bash
python3 {project-root}/.claude/skills/int-instagram/scripts/instagram_client.py summary
python3 {project-root}/.claude/skills/int-instagram/scripts/instagram_client.py recent_posts [account] 20
python3 {project-root}/.claude/skills/int-instagram/scripts/instagram_client.py account_insights [account]
```

### Step 2 — Compare with previous period

Read previous report from `workspace/social/reports/instagram/` if it exists. Calculate deltas de seguidores, engagement, impressões.

### Step 3 — Analyze

Per account:
1. **KPIs:** followers, media count, average engagement rate
2. **Period posts:** published, likes, comments, engagement
3. **Top post:** best performance
4. **Content type:** Reels vs Image vs Carousel — which performs better
5. **Account insights:** impressions, reach, profile views (if available)

### Step 4 — Generate HTML

Use template `.claude/templates/html/custom/social-analytics-report.html` with `{{REPORT_TYPE}}` = "Instagram".

### Step 5 — Save

```
workspace/social/reports/instagram/[C] YYYY-MM-DD-instagram-report.html
```

### Step 6 — Telegram

Notify: followers per account + average engagement + best post
