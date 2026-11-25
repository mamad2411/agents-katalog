---
name: devel-jb-managing-youtrack
description: "- Comment: `$YOUTRACK_URL/issue/<idReadable>#focus=Comments-<COMMENT_ID>` - Drafts have no web URL."
domain: cybersecurity
---

# YouTrack REST API

## Setup (minimal)
- NEVER use pipes after curl commands to parse the output, do that in a separate tool call.
- Always pass the auth header via `"${YOUTRACK_TOKEN}"`. Always include `Accept: application/json`; add `Content-Type: application/json` for write calls.
- For queries containing spaces or symbols, use `curl -G --data-urlencode "query=..."` instead of embedding the query string.
- Request only needed fields via the `fields` parameter; default minimal issue fields: `idReadable,summary`.

## Navigation
- Issues, drafts, comments → [reference/issues.md](reference/issues.md)
- Tags, links, work items → [reference/metadata.md](reference/metadata.md)
- Fields, saved searches, users, groups → [reference/admin.md](reference/admin.md)
- Field presets and `$type` values → [reference/fields.md](reference/fields.md)

## Output requirement
After create/update/delete, print a link to the affected item:
- Issue: `$YOUTRACK_URL/issue/<idReadable>`
- Comment: `$YOUTRACK_URL/issue/<idReadable>#focus=Comments-<COMMENT_ID>`
- Drafts have no web URL.
