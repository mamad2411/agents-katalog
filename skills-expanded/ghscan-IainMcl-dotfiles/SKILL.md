---
name: setup-project-update
description: Set up a project update config for the current repo, so that running project-update requires no setup questions. Use when asked to "set up project updates", "configure project update", "initialise project update", or "create a project update config". Run this once per project repo.
---

# Setup Project Update

Create a `.claude/project-update.json` config file in the current repo so that the `project-update` skill can run without asking setup questions each time.

## Step 1 — Ask for project config

Ask all of these in a single message:

1. **Project name** — what's this project called?
2. **Audience & Slack channel** — who receives the update and where does it get posted? (e.g. "PM lead Sarah, #product-updates")
3. **Sources** — which of these apply? For each relevant one, ask for the detail needed:
   - *Git* — just confirm yes/no (uses the current repo automatically)
   - *Jira* — what's the project key? (e.g. `PAY`, `AUTH`, `TK-APP`)
   - *Slack* — which channel to read? (e.g. `#payments-eng`)
   - *Notion* — page URL or search term?
   - *docs/* — any specific path, or just `docs/`?
4. **Standing highlights** — anything to always mention or emphasise? (optional)
5. **Standing exclusions** — anything to always leave out? (optional)

## Step 2 — Write the config file

Create `.claude/project-update.json` at the root of the current working directory.

```json
{
  "project": "<project name>",
  "audience": "<audience description>",
  "channel": "<slack channel>",
  "sources": {
    "git": true,
    "jira": "<project key or null>",
    "slack": "<channel name or null>",
    "notion": "<url or search term or null>",
    "docs": "<path or null>"
  },
  "highlights": "<standing things to emphasise, or null>",
  "exclusions": "<standing things to omit, or null>"
}
```

Omit any source key where the value would be null — keep the file clean.

## Step 3 — Confirm

Tell the user:
- The config has been written to `.claude/project-update.json`
- They can now run `project-update` (or say "write a project update") and it will skip the setup questions — only asking for the time period
- They can edit the file directly anytime to change config
- Commit the file to the repo so the whole team benefits
