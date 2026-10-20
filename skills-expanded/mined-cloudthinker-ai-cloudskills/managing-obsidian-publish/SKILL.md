---
name: managing-obsidian-publish
description: |
  Use when working with Obsidian Publish — obsidian Publish site management
  covering published pages, site configuration, navigation, and content health.
  Use when auditing an Obsidian Publish site, checking published content status,
  reviewing site navigation structure, or analyzing content coverage and
  freshness.
connection_type: obsidian-publish
preload: false
---

# Managing Obsidian Publish

Obsidian Publish site management and content health analysis via the Obsidian Publish API.

## Discovery Phase

```bash
#!/bin/bash
SITE_ID="${1:?Site ID/slug required}"
PUBLISH_BASE="https://publish-01.obsidian.md"

echo "=== Site Configuration ==="
curl -s -X POST "$PUBLISH_BASE/cache/$SITE_ID" \
  -H "Content-Type: application/json" \
  -d '{}' | jq '{
    siteId: .id,
    name: .name,
    theme: .theme,
    totalFiles: (.files | length),
    customDomain: .customDomain
  }'

echo ""
echo "=== Published Pages ==="
curl -s -X POST "$PUBLISH_BASE/cache/$SITE_ID" \
  -H "Content-Type: application/json" \
  -d '{}' | jq -r '.files[] | "\(.path)\t\(.size)b"' \
  | sort | head -30

echo ""
echo "=== Navigation Structure ==="
curl -s -X POST "$PUBLISH_BASE/cache/$SITE_ID" \
  -H "Content-Type: application/json" \
  -d '{}' | jq '{
    total_files: (.files | length),
    folders: [.files[].path | split("/")[0:-1] | join("/")] | unique | map(select(. != "")) | sort,
    top_level_pages: [.files[] | select(.path | contains("/") | not) | .path]
  }'

echo ""
echo "=== Site Metadata ==="
curl -s "https://$SITE_ID.obsidian.md/" -o /dev/null -w "HTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

## Analysis Phase

```bash
#!/bin/bash
SITE_ID="${1:?Site ID required}"
PUBLISH_BASE="https://publish-01.obsidian.md"

echo "=== Content Health ==="
curl -s -X POST "$PUBLISH_BASE/cache/$SITE_ID" \
  -H "Content-Type: application/json" \
  -d '{}' | jq '{
    total_pages: (.files | length),
    by_extension: (.files | group_by(.path | split(".")[-1]) | map({ext: .[0].path | split(".")[-1], count: length})),
    avg_size: (.files | map(.size) | add / length | round),
    largest_pages: [.files | sort_by(-.size)[:5][] | {path, size}]
  }'

echo ""
echo "=== Folder Distribution ==="
curl -s -X POST "$PUBLISH_BASE/cache/$SITE_ID" \
  -H "Content-Type: application/json" \
  -d '{}' | jq -r '
    [.files[].path | split("/")[0]] | group_by(.) | map({folder: .[0], count: length}) | sort_by(-.count)[] |
    "\(.folder)\t\(.count) pages"
  ' | column -t | head -15
```

## Output Format

```
OBSIDIAN PUBLISH SITE HEALTH
Site:           [name] ([site_id].obsidian.md)
Total Pages:    [count]
Total Folders:  [count]

CONTENT DISTRIBUTION
Folder               Pages
[folder]             [count]
[folder]             [count]

CONTENT HEALTH
Avg Page Size:   [size]
Largest Pages:   [list]
Orphan Pages:    [count] (no backlinks)
```

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

