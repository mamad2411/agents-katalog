---
name: facebook-research-setup
version: 2.0.0
description: |
  Setup state for Facebook research tool. Checks prerequisites, creates project
  directory structure, creates config.json (including competitor pages), sets up
  Chrome with Facebook login, and initializes history tracking files.
  Call this before any other facebook-research state.

allowed-tools:
  - Bash
  - Read
  - Write
  - Question
---

# Facebook Research — Setup State (v2)

Run this first. It checks prerequisites, creates the project, and sets up Chrome.

## Steps

### 1. Gather Parameters

Ask the user:
1. "What's the Facebook page name or URL to analyze?" (e.g., `ESPN`, `https://www.facebook.com/ESPN`)
2. "Give it a short project name (e.g., `espn-sports`)" — this becomes the directory name
3. "What's the page's niche/industry?" (e.g., sports, news, fitness, entertainment)
4. "What competitor pages should we analyze? (comma-separated URLs or names, e.g., `BleacherReport, SportsCenter`)" — leave empty if none
5. "Any specific keywords/topics this page targets?" (comma-separated, e.g., `soccer, NBA, highlights`)
6. "What topics are YOU creating content about? (for replication scripts)" (comma-separated)
7. "How many top posts to analyze?" (default: `10`)
8. "Date range for analytics?" (default: `last 28 days`)
9. "Is this a first-time analysis or a repeat?" (if repeat, existing history will be loaded)

### 2. Create Project Directory Structure

```bash
SESSION=$(date +%Y-%m-%d_%H%M%S)
mkdir -p ".fb-research/projects/<project-name>/$SESSION"
mkdir -p ".fb-research/projects/<project-name>/$SESSION/screenshots"
mkdir -p ".fb-research/projects/<project-name>/$SESSION/screenshots-competitors"
mkdir -p ".fb-research/projects/<project-name>/$SESSION/replication-scripts"
mkdir -p ".fb-research/projects/<project-name>/$SESSION/competitors"
# legacy dirs for back-compat (also create at project root)
mkdir -p ".fb-research/projects/<project-name>/screenshots"
mkdir -p ".fb-research/projects/<project-name>/competitors"
```

For each competitor, create a subdirectory:

```bash
mkdir -p ".fb-research/projects/<project-name>/$SESSION/competitors/<competitor-name>"
mkdir -p ".fb-research/projects/<project-name>/competitors/<competitor-name>"
```

### 3. Create config.json

```json
{
  "name": "<project-name>",
  "pageUrl": "<facebook_page_url>",
  "pageName": "<page name>",
  "niche": "<niche>",
  "competitors": [
    {"name": "<competitor-1>", "url": "<competitor_url>"},
    {"name": "<competitor-2>", "url": "<competitor_url>"}
  ],
  "targetKeywords": ["<keyword1>", "<keyword2>"],
  "yourTopics": ["<your_topic1>", "<your_topic2>"],
  "maxPosts": 10,
  "dateRange": "last_28_days",
  "analysisRound": 1,
  "createdAt": "<YYYY-MM-DD HH:MM:SS>",
  "updatedAt": "<YYYY-MM-DD HH:MM:SS>"
}
```

If this is a repeat analysis, increment `analysisRound` from the existing config.

### 4. Initialize or Load History Files

Check if history files exist:

```bash
cat .fb-research/projects/<project-name>/page-analytics-history.json  # global history, not per-session 2>/dev/null || echo '{"snapshots": []}'
cat .fb-research/projects/<project-name>/report-history.json 2>/dev/null || echo '{"reports": []}'
cat .fb-research/projects/<project-name>/replication-history.json 2>/dev/null || echo '{"scripts": []}'
```

If any are missing, initialize them with empty arrays. If they exist, load them — they'll be used by the scrape and report phases for trend comparison.

### 5. Install Node dependencies

```bash
# scripts are now bundled inside the skill — install there (global-safe):
npm install --prefix "$CLAUDE_SKILL_ROOT/scripts"  # e.g. ~/.claude/skills/facebook-research-setup/scripts
# fallback for local dev without global install:
npm install --prefix ./skills/facebook-research/scripts
```

Installs `chrome-remote-interface` for the scrape/report/download scripts.

### 6. Set Up Chrome with Facebook Access

Facebook requires authentication. Two options:

**Option A — Import cookies via setup-browser-cookies skill** (recommended):

```
/setup-browser-cookies
```

When the picker opens, select Facebook/Meta domains (facebook.com, fb.com, etc.).

**Option B — Manual login**:

Tell the user:
> "Open Chrome DevTools on a new page and navigate to `https://www.facebook.com/`. Log into Facebook manually, then come back and tell me 'ready'."

Wait for the user to confirm they're logged in.

### 7. Verify Access

```bash
chrome-devtools navigate_page --url "https://www.facebook.com/"
chrome-devtools take_snapshot
```

Check if the page shows the logged-in Facebook feed (look for the Facebook logo, stories, or news feed elements — not the login screen).

If login screen shows, return to step 6.

### 8. Confirm Setup Complete

```markdown
✅ Facebook Research Setup Complete!

Project: .fb-research/projects/<project-name>/
Config: config.json
Page: <page_name> (<page_url>)
Competitors: <N> configured (<list_names>)
Analysis Round: <round_number>

History loaded:
  - Page analytics snapshots: <N> previous
  - Reports: <N> previous
  - Replication scripts: <N> previous

Next step: skill facebook-research-scrape
```
