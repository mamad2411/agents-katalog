---
name: mymind
description: Use the local mymind CLI to initialize auth, refresh bookmark cache from access.mymind.com/cards, search bookmarks by text or regex, query tags, and shape JSON output with jq. Trigger when a user mentions "mymind", asks to find bookmarks, list tag counts, troubleshoot mymind CLI fetch errors (including CloudFront 403), or operate local cache/config files in ~/.mymind.
---

# mymind

Use this skill to run and troubleshoot the local `mymind` binary.

## Verify availability

1. Prefer `mymind` from PATH.
2. If missing, build from repo root:
   `go build -o /opt/homebrew/bin/mymind ./cmd/mymind`
3. Confirm:
   `which mymind`
   `mymind -h`

## Initialize auth

1. Run `mymind init` interactively, or:
   `mymind init --cookie '<full Cookie header>' --token '<x-authenticity-token>'`
2. Require the full request `Cookie` header from browser Network tab, not `document.cookie`.
3. Store config in `~/.mymind/config.json`.

## Refresh cache

1. Run `mymind update` to fetch `/cards` and rewrite cache.
2. Read cache from `~/.mymind/bookmarks.json`.
3. Read last fetch from `~/.mymind/version.json`.

## Search workflows

1. Full-text search:
   `mymind search articles`
2. Regex search:
   `mymind search '/(?i)(shadcn|component)/'`
3. Tag-only search:
   `mymind tags components`
4. List tag counts:
   `mymind list tags`

## jq filtering patterns

1. Name/title only:
   `mymind search articles | jq '.[] | {title}'`
2. Name/title and source URL:
   `mymind search articles | jq '.[] | {title, source_url: .source.url}'`
3. Top tags in plain lines:
   `mymind list tags | jq -r '.[0:10][] | "\(.tag) \(.count)"'`

## 403 troubleshooting

1. Detect CloudFront 403 in command output.
2. Re-copy cookie + token from browser request headers.
3. Re-run `mymind init --cookie ... --token ...`.
4. Re-run `mymind update` before search commands.
5. If still blocked, treat as upstream/WAF policy issue and keep existing cache if present.

## Command behavior expectations

1. `mymind search` and `mymind tags` return JSON arrays of matching cards.
2. `mymind list tags` returns JSON array objects: `{"tag":"...","count":N}`.
3. `mymind version` returns JSON with `cli_version` and `last_cache_fetch`.
