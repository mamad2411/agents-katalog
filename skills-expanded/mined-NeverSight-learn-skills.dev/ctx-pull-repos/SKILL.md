---
name: ctx-pull-repos
description: Clone all repos from config.json into the workspace root. Skips repos that already exist locally. Use to sync your workspace with the configured repo list.
metadata:
  author: nicolasse
  version: "2.0.0"
---

# Pull Repos

Reads the repo list from `context/config.json` at the workspace root and clones any missing repos into the workspace root.

## Workflow

### 1. Read config

Read `context/config.json`. Parse the `repos` array. Each entry has:
- `name` — directory name at the workspace root
- `url` — git clone URL

If `context/config.json` doesn't exist or has no `repos` key, tell the user and stop.

If the `repos` array is empty, tell the user there are no repos configured and suggest they run `/ctx-export` or add entries to `context/config.json` manually.

### 2. Clone missing repos

For each repo in the array:

- Check if `{name}` already exists at the workspace root
- If it exists, mark as **skipped**
- If it doesn't exist, run `git clone {url} {name}` and mark as **cloned**

If a clone fails, report the error but continue with the remaining repos.

### 3. Report

Print a summary:

- **Cloned**: list of repos that were cloned
- **Skipped** (already existed): list of repos that were skipped
- **Failed**: list of repos that failed to clone, with error details

If everything was skipped, say all repos are already present.
