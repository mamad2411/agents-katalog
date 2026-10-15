---
name: mlwcli
description: >
  Unified command-line interface for managing feeds (Miniflux), links
  (Linkding), and pages (Wallabag). Use when the user wants to: save a URL as a
  bookmark, add or browse RSS/Atom feeds, read or search unread feed entries,
  save an article to Wallabag, manage tags on links or pages, or authenticate
  with Miniflux/Linkding/Wallabag.
---

# mlwcli

A unified CLI for managing feeds (Miniflux), links (Linkding), and pages (Wallabag).

## Command Reference

```bash
# Authentication (interactive TUI)
mlwcli auth login        # Login to linkding, miniflux, or wallabag
mlwcli auth logout       # Logout from a service

# Linkding (Links)
mlwcli link add <url>    # Add link
mlwcli link list         # List links

# Miniflux (Feeds)
mlwcli feed add <url>    # Add feed
mlwcli feed list         # List feeds
mlwcli entry list        # List feed entries
mlwcli entry save <id>   # Save entry to third-party service

# Wallabag (Pages)
mlwcli page add <url>    # Add page
mlwcli page list         # List pages
```

Use `--help` on any command for options.

## Critical Guidelines

1. **Authentication requires user action**:
   - `auth login` and `auth logout` use an interactive TUI that requires a TTY — do not run them yourself
   - If a command fails due to missing credentials, tell the user to run `mlwcli auth login` in their terminal
   - Config stored at `~/.config/mlwcli/auth.toml`

2. **Pagination**: All `list` commands return `{total, items}`.
   - `link list`, `entry list`: `--limit` / `--offset` (default: limit=10, offset=0)
   - `page list`: `--page` / `--per-page` (default: page=1, per-page=10)
   - `feed list`: no pagination parameters (returns all)
   - **Always check `total` vs items returned** before assuming you have all results.

3. **Output Filtering**:
   - `--jq=expression` — inline jq filter (automatically enables JSON output)
   - `--json=field1,field2` — select specific fields (comma-separated, no spaces)
   - Without these flags, output is human-readable table format

4. **Search and Filtering**:
   - `link list`: `--search`, `--limit`, `--offset`
   - `entry list`: `--search`, `--status` (read/unread/removed, default: unread), `--starred`, `--feed-id`, `--limit`, `--offset`
   - `page list`: `--archive`, `--starred`, `--tags`, `--domain`, `--page`, `--per-page`

5. **Quote Handling**:
   - Values with double quotes: wrap in single quotes: `--notes 'Title: "Example"'`
   - Tags are space-separated within a quoted string: `--tags "tag1 tag2"`

## Examples

### Authentication

Authentication requires an interactive TTY — ask the user to run these commands themselves:

```bash
mlwcli auth login   # interactive TUI: select service, enter endpoint + credentials
mlwcli auth logout  # interactive TUI: only shows signed-in services
```

### Check pagination before processing

```bash
mlwcli entry list --status=unread --jq='{total: .total, returned: (.items | length)}'
```

If `total > returned`, increase `--limit` or paginate:

```bash
mlwcli entry list --status=unread --limit=100
# or iterate with --offset=0, --offset=10, etc.
```

### List unread entries

```bash
mlwcli entry list --status=unread --jq='.items[] | { id, url, title, published_at, status, feed_id: .feed.id, feed_title: .feed.title }'
```

### List entries by feed

```bash
# Find feed ID
mlwcli feed list --jq='.items[] | { id, title, site_url }'

# Fetch entries from that feed
mlwcli entry list --feed-id=42 --limit=20 --jq='.items[] | { id, url, title, published_at }'
```

### Find starred/read entries by date

```bash
mlwcli entry list --starred --status=read --limit=100 --json=id,url,title,changed_at,starred | jq '.items[] | select(.changed_at >= "2025-12-26")'
```

Note: `changed_at` reflects when the entry was last modified (starred/read status changed), not publication date.

### Save an entry to a third-party service

```bash
mlwcli entry save 42
```

Saves to Miniflux's configured third-party integration (e.g. Wallabag, Pocket).

### Add a feed (with optional category)

```bash
mlwcli feed add <url>
mlwcli feed add <url> --category-id=<id>   # defaults to 1 (All) if omitted
```

To find category IDs:
```bash
mlwcli feed list --jq='.items[] | { id, title, category_id: .category.id, category_title: .category.title }'
```

### Add a link

```bash
mlwcli link add <url>
mlwcli link add <url> --notes='Title: "Some Title"' --tags="tag1 tag2"
```

### Add a page

```bash
mlwcli page add <url>
mlwcli page add <url> --tags="tag1 tag2" --archive
```

### List pages

```bash
mlwcli page list --starred --per-page=20 --jq='.items[] | { id, url, title, domain_name }'
mlwcli page list --domain=example.com
mlwcli page list --tags="tech news"
```
