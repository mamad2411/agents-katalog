---
name: ig-research-report
version: 1.0.0
description: |
  Report state — generates a beautiful HTML report from scraped data.
  Platform-agnostic: works with raw-posts.json from any platform.
  Reads transcripts, hook screenshots, engagement data, and produces
  a dark-themed report with post cards, pattern analysis, and findings.

allowed-tools:
  - Bash
  - Read
---

# Social Research — Report State

Generates a styled HTML report from scraped data, transcripts, and screenshots.

## Run

```bash
node "$CLAUDE_SKILL_ROOT/scripts/report-html.js" <project-name> [sessionId]  # resolves latest if no session
```

## What it generates

The report includes:
- **Hero section**: Project name, niche, search terms, scan date
- **Stats bar**: Total posts, reel %, transcribed count, visual hooks, top likes
- **Top 6 post cards**: Rank, author, engagement, hook screenshots (0s/1s/2s), visual hook description, spoken hook quote, "why it worked" analysis, full transcript (scrollable), caption preview
- **Winning patterns**: Format breakdown, comment CTA usage, hook analysis, content themes

### "Why it worked" detection

Automatically checks for:
- Comment-bait CTAs
- Specific numbers in hooks (anchoring)
- Named frameworks (authority)
- Short punchy hooks (≤8 words)
- Question format (curiosity gap)
- Comparison format (contrast)
- Time promises (loss aversion)

### Visual hook inference

Infers from caption/transcript: split screen, whiteboard, screen recording, talking head, before/after, etc.

## Output

```
.ig-research/projects/<project-name>/report.html
```
