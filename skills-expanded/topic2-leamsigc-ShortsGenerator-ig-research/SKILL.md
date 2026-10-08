---
name: ig-research
version: 1.0.0
description: |
  Social media content research tool — scrape, transcribe, analyze top-performing
  content across platforms (Instagram, Facebook, LinkedIn, X, YouTube).
  Main orchestrator skill. Delegates to state sub-skills for each phase.

allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Question

states:
  - ig-research-setup    — Prerequisites, directory, config
  - ig-research-scrape   — Scrape posts via Chrome DevTools
  - ig-research-transcribe — Transcribe audio via Whisper
  - ig-research-report   — Generate HTML report
  - ig-research-analyze  — Content psychology analysis
---

# Social Research Tool — Main Skill

Full workflow: Setup → Scrape → Transcribe → Report → Analyze

## Architecture

```
skills/ig-research/            # Skill (bundled, global-installable via ~/.claude/skills/)
├── SKILL.md
└── scripts/                   # Bundled — no external .ig-research/scripts needed
    ├── package.json
    ├── scrape.js
    ├── transcribe.sh
    └── report-html.js

.ig-research/                  # Tool data directory (project root, auto-resolved)
└── projects/<name>/
    ├── config.json            # Global per-project config
    ├── latest.json            # -> <YYYY-MM-DD_HHMMSS>
    └── <YYYY-MM-DD_HHMMSS>/   # One folder per run (dated)
        ├── raw-posts.json
        ├── transcripts/
        ├── hook-screenshots/
        └── report.html
```

## Platform Extensibility

Each platform has its own scraper. The config schema includes a `platform` field:

| Platform    | Scraper location                  | Config `platform` |
|-------------|-----------------------------------|-------------------|
| Instagram   | `scripts/scrape.js` (default)     | `instagram`       |
| Facebook    | `platforms/facebook/scrape.js`    | `facebook`        |
| LinkedIn    | `platforms/linkedin/scrape.js`    | `linkedin`        |
| X           | `platforms/x/scrape.js`           | `x`               |
| YouTube     | `platforms/youtube/scrape.js`     | `youtube`         |

To add a new platform: create a scraper script in `skills/ig-research/platforms/<name>/scrape.js` (or external platforms/<name>/scrape.js with --data-root) that outputs `raw-posts.json` with the same schema (posts array with `postId`, `type`, `likes`, `caption`, `author`, `platform`, `hasScreenshots`, `hasAudio`). The transcribe and report steps work with any platform's output.

## Workflow

Load the full workflow with: `skill ig-research`

Each state can be run independently with: `skill ig-research-<state>`

```bash
# Run full pipeline for a project
skill ig-research-setup     # Step 1: Setup (prerequisites + config)
skill ig-research-scrape    # Step 2: Scrape Instagram
skill ig-research-transcribe # Step 3: Transcribe audio
skill ig-research-report    # Step 4: Generate HTML report
skill ig-research-analyze   # Step 5: Content psychology analysis
```
