---
name: ez-github
description: Discover trending GitHub repositories, view repo details and releases, search repos. Find popular new projects by language and time period. Use for any GitHub trending/discovery queries.
---

# ez-github - GitHub Trending CLI

Simple typer CLI for discovering trending GitHub repos. No authentication required (60 requests/hour unauthenticated).

## Usage

Run `uv run skills/ez-github/scripts/gh_trending.py <command>`. All commands support `--json` for raw JSON output.

### Trending Repos

```bash
uv run skills/ez-github/scripts/gh_trending.py trending                         # weekly trending (default)
uv run skills/ez-github/scripts/gh_trending.py trending --period daily           # today's trending
uv run skills/ez-github/scripts/gh_trending.py trending --period monthly         # this month
uv run skills/ez-github/scripts/gh_trending.py trending --lang python            # Python repos only
uv run skills/ez-github/scripts/gh_trending.py trending --lang rust --limit 20   # top 20 Rust repos
```

### Popular Repos with Recent Activity

```bash
uv run skills/ez-github/scripts/gh_trending.py stars                    # popular repos active this week
uv run skills/ez-github/scripts/gh_trending.py stars --lang typescript  # TypeScript only
```

### Repo Details and Releases

```bash
uv run skills/ez-github/scripts/gh_trending.py repo astral-sh/uv
uv run skills/ez-github/scripts/gh_trending.py releases astral-sh/uv
uv run skills/ez-github/scripts/gh_trending.py releases astral-sh/uv --limit 10
```

### Search

```bash
uv run skills/ez-github/scripts/gh_trending.py search "LLM framework"
uv run skills/ez-github/scripts/gh_trending.py search "web framework" --lang rust --sort stars
```

## Common Workflows

| User asks | Command |
|---|---|
| "What's trending on GitHub?" | `gh_trending.py trending` |
| "Trending Rust repos this week" | `gh_trending.py trending --lang rust` |
| "Tell me about repo X" | `gh_trending.py repo owner/X` |
| "Latest releases for uv" | `gh_trending.py releases astral-sh/uv` |
| "Search GitHub for LLM tools" | `gh_trending.py search "LLM tools"` |
