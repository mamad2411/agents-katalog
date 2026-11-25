---
name: github
description: Fetch and digest GitHub activity from specified repositories. Use when user asks for GitHub updates, repository activity, or /github.
---

# GitHub Digest Skill

Fetches recent activity (issues, PRs, releases) from GitHub repositories and creates an AI-curated digest.

## Usage

```bash
python3 _scripts/github_digest.py
```

With custom repos:
```bash
python3 _scripts/github_digest.py --repos microsoft/vscode facebook/react golang/go
```

## Configuration

`.env` — Optional `GITHUB_TOKEN` for higher rate limits

## Default Repos

microsoft/vscode, facebook/react, golang/go, rust-lang/rust

## Output

`Sources/GitHub Digest - YYYY-MM-DD.md` (activity summary with AI analysis)
