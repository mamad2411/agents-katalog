---
name: ez-hn
description: Browse and search Hacker News. Fetch top, new, best, Ask HN, Show HN stories and job postings. View item details, comments, and user profiles. Search stories via Algolia. Find "Who is hiring?" threads. Use for any HN-related queries.
---

# ez-hn - Hacker News CLI

Simple typer CLI for browsing Hacker News. No authentication required.

## Usage

Run `uv run skills/ez-hn/scripts/hn.py <command>`. All commands support `--json` for raw JSON output.

### Browse Stories

```bash
uv run skills/ez-hn/scripts/hn.py top              # top/trending (default 10)
uv run skills/ez-hn/scripts/hn.py top --limit 20    # more results
uv run skills/ez-hn/scripts/hn.py new               # newest
uv run skills/ez-hn/scripts/hn.py best              # highest rated
uv run skills/ez-hn/scripts/hn.py ask               # Ask HN
uv run skills/ez-hn/scripts/hn.py show              # Show HN
uv run skills/ez-hn/scripts/hn.py jobs              # job postings
```

### View Item Details and Comments

```bash
uv run skills/ez-hn/scripts/hn.py item 12345678
uv run skills/ez-hn/scripts/hn.py comments 12345678
uv run skills/ez-hn/scripts/hn.py comments 12345678 --limit 10 --depth 2
```

### User Profiles

```bash
uv run skills/ez-hn/scripts/hn.py user dang
```

### Search

```bash
uv run skills/ez-hn/scripts/hn.py search "rust programming"
uv run skills/ez-hn/scripts/hn.py search "LLM" --type story --sort date --period week --limit 5
```

### Who is Hiring

```bash
uv run skills/ez-hn/scripts/hn.py whoishiring
uv run skills/ez-hn/scripts/hn.py whoishiring --limit 20
```

## Common Workflows

| User asks | Command |
|---|---|
| "What's trending on HN?" | `hn.py top` |
| "Latest Ask HN posts" | `hn.py ask` |
| "Search HN for X" | `hn.py search "X"` |
| "Show comments on story Y" | `hn.py comments Y` |
| "Who is hiring?" | `hn.py whoishiring` |
| "Tell me about HN user Z" | `hn.py user Z` |
