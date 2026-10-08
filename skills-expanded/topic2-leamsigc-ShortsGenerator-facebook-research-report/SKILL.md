---
name: facebook-research-report
version: 3.0.0
description: |
  Report state — synthesizes all phase outputs into a comprehensive final
  report. Generates a self-contained HTML report (REPORT.html) plus a markdown
  backup (report.md). Includes performance summary, history trend comparison,
  top 5 deconstruction recap, video structure analysis, competitor deep-dive,
  replication scripts, keyword strategy, and engagement opportunities.

allowed-tools:
  - Bash
  - Read
  - Write
  - ChromeDevTools
  - WebSearch
---

# Facebook Research — Report State (v3)

Generates the final report. The HTML shell is produced by a script; the analytical
sections are authored from the scraped data.

## Preconditions

- Config: `.fb-research/projects/<project-name>/config.json`
- Analysis: `.fb-research/projects/<project-name>/top5-analysis.md`
- Analytics: `.fb-research/projects/<project-name>/page-analytics.json` + `page-analytics-history.json`
- Competitors: `.fb-research/projects/<project-name>/competitors/`
- Optional video template data: `video-template/VIDEO-TEMPLATE.md`, `video-analysis.json`, `transcripts/`

## Steps

### 1. Load all data + compute history trends

Read all JSON/markdown files. Compute trend direction per metric (followers, avg views,
avg likes, top post views) across snapshots — improving / declining / stable.

### 2. Discover real competitors via Facebook search

```bash
chrome-devtools navigate_page --url "https://www.facebook.com/search/pages/?q=<URL_ENCODED_NICHE>"
```

Scroll, extract page results, filter to the top 5 most relevant, save to `discovered-competitors.json`. Benchmark each competitor's positioning relative to the target page.

### 3. Generate 5 replication script templates

Mix at least 3 from the page's top 5 + up to 2 from competitor patterns. Each script:
original source, core pattern, why it works, adapted topic script (hook/body/CTA), caption
template, production notes, performance prediction, post-publication tracking checklist.

Save each to `replication-scripts/001-<slug>.md` and update `replication-history.json`.

### 4. Keyword research + competitor deep-dive

- WebSearch the niche for trending topics/audience interests
- Extract keywords from top posts + competitors → keyword clusters by content type
- Visit competitor pages via Chrome DevTools, extract recent posts + video URLs

### 5. Generate the HTML report + markdown backup

The HTML shell is rendered from the structured data:

```bash
node "$CLAUDE_SKILL_ROOT/scripts/report-html.js" <project-name> [sessionId] --session $SESSION
# fallback: node ./skills/facebook-research/scripts/report-html.js <project-name> --session $SESSION
```

Then **augment REPORT.html** with the analytical sections authored above (executive
summary, top-5 deep dive, video structure analysis, replication scripts, keyword strategy,
engagement strategy, feedback for page manager, 30-day action plan). Keep `REPORT.html`
as the primary deliverable and write `report.md` as the markdown backup. Append a snapshot
to `report-history.json`.

## Report Completion

```
✅ Facebook Research Report Complete!
Project: .fb-research/projects/<project-name>/
📊 REPORT.html (primary) · 📄 report.md (backup) · 📈 trend-report.md (round 2+)
Replication scripts: <N> · Competitors analyzed: <N>
Next step: skill facebook-research-engage (recommended for growth)
```
