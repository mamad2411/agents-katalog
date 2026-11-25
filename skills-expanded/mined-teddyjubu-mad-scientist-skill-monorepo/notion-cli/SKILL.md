---

name: notion-cli
description: notion-cli lets the user create, read, update, and manage pages, databases, comments, files, and Workers in Notion through the command line, which is useful when they want to save AI outputs, build internal knowledge bases, create structured documents, or automate Notion workflows without clicking through the UI.

---
Use `ntn` as the first-choice Notion control surface on this VPS. It is already installed and authenticated by environment token, so do not run `ntn login` unless Charles explicitly asks to replace credentials.

## What This Skill Does

This skill notion-cli lets the user create, read, update, and manage pages, databases, comments, files, and Workers in Notion through the command line, which is useful when they want to save AI outputs, build internal knowledge bases, create structured documents, or automate Notion workflows without clicking through the UI.

## Runtime Setup

Hermes host:

```bash
set -a
. /root/.hermes/notion.env
set +a
unset NOTION_KEYRING
export NOTION_HOME=/root/.config/notion
ntn api v1/users/me
```

OpenClaw container:

```bash
set -a
. /data/.openclaw/workspace/.secrets/notion.env
set +a
unset NOTION_KEYRING
export NOTION_HOME=/data/.config/notion
/data/.npm-global/bin/ntn api v1/users/me
```

Default workspace is `Charles Blair’s Space`. The migrated Hermes root is:

```text
36325ada250d8192af71ec68617029d3
```

Migration folder/root page:

```text
36325ada250d81b08171fa8170e25c82
```

Do not print tokens. The token lives in the env files above and is also exposed to the active Hermes systemd services and OpenClaw container env.

## What Is Verified

As of 2026-05-17, both Hermes host and OpenClaw container can:

- Read the current bot/user via `v1/users/me`.
- Retrieve known users by ID.
- Retrieve pages and block children.
- Create pages under the Hermes page.
- Append and update page blocks.
- Insert comments on pages.
- Upload files and attach uploaded files to pages.
- Create databases and data sources.
- Create rows/pages inside data sources and query them.
- Create, get, list, and delete Notion Workers.

Worker availability must be checked with `ntn workers list/deploy` on the active workspace before hosted Worker use. Local Worker execution is available.

Known Notion/PAT limitation: `v1/users` full user listing returns `403 restricted_resource` for personal access tokens. Use `v1/users/me`, retrieve known user IDs directly, or ask Charles to use the UI if a full people directory is required.

`ntn doctor` may still warn that Workers are not enabled even when `ntn workers create/list/delete` works. Treat successful worker commands as authoritative.

## Common Commands

```bash
ntn api ls --json
ntn api v1/pages/<page_id>
ntn api v1/blocks/<page_id>/children
ntn pages create --parent page:<page_id> --content '# Title\n\nBody'
ntn pages trash <page_id> --yes
ntn files create --filename report.txt --content-type text/plain < report.txt
ntn workers list --json
ntn workers create --name <temporary-or-real-name> --json
ntn workers delete <worker_id> --yes
```

Use `:=` for JSON values in `ntn api` inline arguments and `=` for strings. Body input defaults to POST, so add `-X PATCH`, `-X DELETE`, or `-X GET` when needed.

## Safety Rules

- Never reveal or paste Notion tokens.
- Prefer temporary smoke pages under the migrated Hermes page, then trash them when testing.
- Ask before archiving/deleting real user pages, changing existing database schemas, bulk-editing more than about 20 pages, or changing billing/trial settings.
- For Workers, delete smoke workers after verification unless Charles asks to keep them.
- Treat webhook URLs and worker secrets as secrets.

## Block Writing — Use Direct API, Not `ntn api`

`ntn api` PATCH to the blocks endpoint (append children) silently returns exit 0 with no errors — but writes zero blocks. This has been confirmed across multiple runs. **For any block creation or bulk append, use direct Notion API calls via Python `urllib.request` or `curl` instead of `ntn api`.**

Correct pattern (Python):

```python
import urllib.request, json, subprocess, os

# Read token at runtime from env
token = subprocess.check_output(
    "grep NOTION_TOKEN /root/.hermes/notion.env | cut -d= -f2",
    shell=True
).decode().strip()

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def append_blocks(page_id, blocks):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    payload = json.dumps({"children": blocks}).encode()
    req = urllib.request.Request(url, data=payload, headers=headers, method="PATCH")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

# Append in batches of 50 (Notion limit per request)
for i in range(0, len(all_blocks), 50):
    batch = all_blocks[i:i+50]
    result = append_blocks(page_id, batch)
```

## Block Payload Rules

- **Never set `icon: null`** in any block payload. Notion API 2022-06-28 rejects null icon fields with a 400 validation error (`validation_error` code, `path failed validation`). **Omit the `icon` field entirely** when there is no icon — do not set it to `None`, `null`, or `{}`.
- **Callout blocks do not support `icon`** — attempting to set `icon: {"type": "emoji", "emoji": "💡"}` on a callout causes a 400 "embed should be defined" validation error. To add visual interest to callouts, use `color` only; omit the icon field entirely.
- Same rule applies to `cover` fields on page objects.
- **Only set `icon` as a dict** with `type` + the appropriate value key (e.g., `{"type": "emoji", "emoji": "🚀"}`).
- `type` and content keys are required on every block object; missing `type` causes a 400.

### `rich_text` Array Rules

- **No mixed annotation states within one `rich_text` array.** If you pass two entries (e.g., `[plain_text, {"text": ..., "annotations": {"bold": true}}]`) the API returns 400 "annotations should be not present." Each distinct annotation state must be its own separate block.
- **Correct pattern:** Use separate `bulleted_list_item` blocks for each annotation variation, or use a helper that produces one `rich_text` dict at a time with consistent structure.
- Helper pattern (Python):
  ```python
  def t(text):
      return {"text": {"content": text}}
  def ta(text, bold=False, italic=False):
      ann = {}
      if bold: ann["bold"] = True
      if italic: ann["italic"] = True
      return {"text": {"content": text}, "annotations": ann} if ann else {"text": {"content": text}}
  ```

### Unsupported Block Types (2022-06-28 API)

| Block Type | Status | Workaround |
|---|---|---|
| `table` / `table_row` | **Not supported** — causes 400 validation error | Use bulleted list with pipe-separated columns, or a pre-formatted grid layout |
| `callout` with `icon` field | Not supported | Omit `icon`; use `color` only |

## Page Title Update

`ntn pages create` sets the page title, but if you need to update the title after creation use a direct PATCH to `https://api.notion.com/v1/pages/{page_id}` with `{"properties": {"title": {"title": [{"text": {"content": "New Title"}}]}}`.

## `ntn` CLI Limitations

- `ntn pages` has no `delete` subcommand. To remove a page, PATCH it with `{"archived": true}` via direct API.
- `ntn api` PATCH to blocks endpoint silently fails; use direct API for all block writes.
- `ntn doctor` may warn Workers are unavailable even when worker commands (`create`, `list`, `delete`) work correctly — treat successful command output as authoritative.

<!-- notion-beautiful-systems-pairing -->
## Beautiful Systems Pairing

Before using `ntn` to create or update any substantial Notion deliverable, load `notion-beautiful-systems`. Create the page/system skeleton first, then fill content, then run Publisher Agent validation when the result is meant to be shared or published.

