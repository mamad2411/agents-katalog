---
name: install-agent
description: When the user pastes a GitHub URL, clone or pull the repo locally so it can be read and analyzed. Use when a GitHub repo link appears in conversation and the user wants to explore, review, or understand its contents.
user-invocable: true
---

# Install Agent — Fetch GitHub Repo for Analysis

When the user pastes a GitHub URL, pull the repo locally so you can read and analyze its contents.

$ARGUMENTS

## Process

### Step 1: Parse the URL

Accept these formats:
- `https://github.com/user/repo`
- `https://github.com/user/repo.git`
- `git@github.com:user/repo.git`
- `user/repo` (expand to `https://github.com/user/repo`)

Extract the repo name from the URL.

### Step 2: Clone or Pull

Target directory: `/tmp/repos/<repo-name>`

- **If the directory doesn't exist:** `git clone <url> /tmp/repos/<repo-name>`
- **If it already exists:** `cd /tmp/repos/<repo-name> && git pull`

### Step 3: Analyze

Once cloned, explore the repo:

1. Show the directory structure (`ls` or `find` top-level)
2. Read key files: README, config files, entry points
3. Summarize what the repo is and what it does
4. Answer whatever the user asked about it

## Notes

- This is a lightweight fetch — just clone to `/tmp` for reading, not a permanent install
- If the clone fails (private repo, bad URL), tell the user and suggest fixes
- If the user wants to install the repo as a Talon agent, use `/create-agent` or `/compose-agent` after analysis
