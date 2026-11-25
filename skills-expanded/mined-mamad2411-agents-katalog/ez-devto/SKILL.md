---
name: ez-devto
description: Browse and search DEV.to articles. Fetch top, latest, rising, and tag-filtered articles. View article details and comments. List popular tags. Use for any DEV.to-related queries.
---

# ez-devto - DEV.to CLI

Simple typer CLI for browsing DEV.to. No authentication required.

## Usage

Run `uv run skills/ez-devto/scripts/devto.py <command>`. All commands support `--json` for raw JSON output.

### Browse Articles

```bash
uv run skills/ez-devto/scripts/devto.py top                    # top articles this week
uv run skills/ez-devto/scripts/devto.py top --limit 20          # more results
uv run skills/ez-devto/scripts/devto.py latest                  # newest articles
uv run skills/ez-devto/scripts/devto.py rising                  # rising today
uv run skills/ez-devto/scripts/devto.py tag python              # by tag
uv run skills/ez-devto/scripts/devto.py tag webdev              # webdev articles
```

### View Article Details and Comments

```bash
uv run skills/ez-devto/scripts/devto.py article 12345
uv run skills/ez-devto/scripts/devto.py comments 12345
```

### Search and Tags

```bash
uv run skills/ez-devto/scripts/devto.py search "react hooks"
uv run skills/ez-devto/scripts/devto.py tags                   # popular tags
```

## Common Workflows

| User asks | Command |
|---|---|
| "What's popular on DEV.to?" | `devto.py top` |
| "Latest DEV.to articles" | `devto.py latest` |
| "DEV.to posts about Python" | `devto.py tag python` |
| "Search DEV.to for X" | `devto.py search "X"` |
| "Show comments on article Y" | `devto.py comments Y` |
| "What tags are popular on DEV.to?" | `devto.py tags` |
