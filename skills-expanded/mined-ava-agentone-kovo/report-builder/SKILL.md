---
name: report-builder
description: Generate beautiful, modern HTML reports for any purpose — system health, project status, analytics, weekly summaries, incident reports, or any structured data. Produces a self-contained single-file HTML with dark/light mode toggle, animated charts, responsive cards, and email-ready output.
tools: [shell]
trigger: report, dashboard, health report, status page, weekly report, generate report, build report, system report, morning briefing report, email report
---

# Report Builder

## Purpose

Generate stunning, single-file HTML reports from any structured data. The output is self-contained (inline CSS/JS, no external dependencies except Google Fonts) and can be:

- Served on the Kovo dashboard at port 8080
- Attached to emails via Gmail
- Sent as a file via Telegram
- Opened directly in any browser
- Printed to PDF from the browser

## When to Use

Trigger this skill when asked to:
- Create/generate/build any kind of report
- Make a dashboard or status page
- Visualize metrics, KPIs, or structured data
- Produce a summary report (weekly, monthly, project, incident, etc.)
- Generate something to send via email as an HTML attachment
- Generate a morning briefing as a visual report

Report types: system health, morning briefings, storage reports, project status, weekly digests, incident reports, analytics dashboards.

## Architecture

Single self-contained HTML file with:
- Inline CSS using custom properties for theming
- Inline SVG icons (no icon libraries)
- Vanilla JS for theme toggle only
- CSS animations (no JS animation libraries)
- Google Fonts link (Outfit + JetBrains Mono) — gracefully degrades to system fonts if offline

## Report Skeleton

Every report follows this structure — pick the components you need:

Header (always) → Hero with Score Ring + Stat Cards (optional) → Sections with any mix of: Info Grid, Metric Cards, Data Tables, List Rows, Item Cards, Score Breakdown Cards, Timeline, Tag Cards, Recommendations → Footer (always)

## Available Components (13 total)

1. **Header** — title, subtitle, status badge (green/warning/critical/info)
2. **Score Ring** — circular gauge, animated fill. Offset = 439.82 - (439.82 × pct / 100)
3. **Stat Cards** — KPI cards with colored left accent (cyan/green/purple/orange)
4. **Info Grid** — key-value pairs, 2-4 column grid
5. **Metric Cards with Progress** — percentage bar + detail rows
6. **Data Table** — header row + data rows with status pills
7. **List Rows** — grid items with status badges
8. **Item Cards** — dot + label + badge (for software, tools, tags)
9. **Score Breakdown** — accent bar, score badge, progress, sparkline
10. **Timeline** — vertical dots with dashed connectors
11. **Tag Cards** — small centered cards with top accent
12. **Numbered Recommendations** — ordered items with colored number badges
13. **Section Divider** — labeled horizontal line

## Color System

| Token | Use For |
|-------|---------|
| cyan | Primary metrics, default accent |
| green | Success, healthy, complete |
| yellow | Warning, needs attention |
| red | Error, critical, failed |
| purple | Secondary, informational |
| orange | Tertiary, in-progress |

Percentage metrics (lower=better): 0-30% green, 31-60% cyan, 61-80% yellow, 81-100% red
Score metrics (higher=better): 90-100 green, 70-89 cyan, 50-69 yellow, 0-49 red

## Report Type → Components

| Type | Use |
|------|-----|
| System Health | Score Ring + Stat Cards + Metric Cards + Score Breakdown + Recommendations |
| Morning Briefing | Stat Cards + List Rows + Timeline + Recommendations |
| Storage Report | Metric Cards + Score Breakdown + Recommendations |
| Weekly Digest | Stat Cards + List Rows + Timeline + Tag Cards + Recommendations |
| Incident Report | Info Grid + Timeline + List Rows + Recommendations |

## How to Build a Report

1. Read templates/report-template.html as your base
2. Set header: title, subtitle, status badge
3. Choose components based on the report type
4. Remove unused sections
5. Inject live data from shell commands (df, free, systemctl, etc.)
6. Calculate derived values: score ring offsets, color assignments
7. Set footer date
8. Save to /opt/kovo/data/documents/Report_Name_YYYYMMDD.html

## Template Location

/opt/kovo/workspace/skills/report-builder/templates/report-template.html
