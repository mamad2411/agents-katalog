---
name: confluence
description: This skill should be used when the user asks to manage Confluence Cloud content from the command line — list/search Confluence spaces, list/create/update/delete Confluence pages, **download existing pages locally** (JSONL + optional markdown) for offline reference or edit-and-reupload, upload attachments, configure Confluence authentication, store API tokens securely, switch between Confluence profiles, or publish a richdoc-generated Confluence bundle. Triggers include "publish to Confluence", "update Confluence page", "download Confluence page", "pull Confluence content", "export Confluence page to markdown", "list Confluence spaces", "Confluence auth", "Confluence login", "store Confluence token", "publish-bundle", or "send this to Confluence". For authoring polished HTML documents that will eventually be published to Confluence, use the `richdoc` skill first (`richdoc export confluence`) and then use this skill to publish the resulting bundle.
---

# confluence

CLI for managing Confluence Cloud content and publishing storage
bundles produced by other tools (notably `richdoc`). JSON output, no
interactive prompts.

## When to use confluence

- Browsing or searching Confluence spaces / pages.
- **Downloading existing pages locally** — a single page, a subtree,
  or a whole space — into JSONL (lossless, default) and optionally
  best-effort markdown for human reading. This is the read side of
  the edit-and-reupload loop.
- Creating, updating, or deleting Confluence pages from storage-format
  XML files.
- Uploading attachments to a page.
- Managing the auth profile(s) the agent uses to talk to Confluence.
- Publishing a `richdoc.confluence.bundle.v1` directory to a Confluence
  space (one-shot, idempotent, two-pass).

For authoring rich documents, use the `richdoc` skill. The two skills
share a documented on-disk bundle format and are deliberately
decoupled: `confluence` never imports richdoc code, and `richdoc` never
opens a Confluence connection.

## CLI Discovery

The CLI is located at `./confluence-cli/` relative to this SKILL.md.
Requires [`uv`](https://docs.astral.sh/uv/); the first call provisions
the Python environment.

| Platform         | Script                                              |
| ---------------- | --------------------------------------------------- |
| Unix/Linux/macOS | `confluence`                                        |
| Windows          | `confluence.cmd` (`confluence.ps1` also available)  |

| Command | Description |
| --- | --- |
| `confluence auth init --profile NAME [--site URL] [--email EMAIL] [--space-key KEY] [--token-env NAME]` | Write a profile entry to the user config file with a `<your-token-here>` placeholder. Returns `next_steps` for the human user. |
| `confluence auth profiles` | List profiles from project and user config. Token values never appear. |
| `confluence auth use PROFILE` | Set the user-config default profile. |
| `confluence auth logout --profile NAME [--keep-config]` | Forget a profile (removes the entry or just the token field). |
| `confluence auth status [--profile NAME] [--strict] [--no-verify]` | Resolve credentials, report `tokenSource` / `tokenLocation` / `secure`, and ping Confluence. |
| `confluence spaces [-q TEXT] [--limit N]` | List spaces visible to the token. |
| `confluence pages [--space-key KEY] [-q TEXT] [--parent-id ID] [--limit N]` | List pages in a space. |
| `confluence page-by-id PAGE_ID_OR_URL` | Resolve a page id (or full Confluence URL) to `{id, title, parentId, spaceId, version, url}`. |
| `confluence page get PAGE_ID_OR_URL [--body]` | Fetch one page's metadata. With `--body`, also returns the storage-format XML body (lossless; suitable for editing then re-uploading). |
| `confluence page create --space-key KEY [--parent-id ID] --title TEXT --body-file FILE` | Create a page from a storage-format XML file. |
| `confluence page update PAGE_ID_OR_URL [--title TEXT] --body-file FILE [--comment TEXT]` | Update an existing page. |
| `confluence download PAGE_ID_OR_URL [--recurse] [--depth N] [--markdown] [--attachments] -o DIR` | Download one page / subtree to a local directory as JSONL (always) + optional markdown + optional attachment bytes. With `--space-key KEY` alone, downloads every page in the space (capped by `--limit`, default 200). |
| `confluence publish-bundle BUNDLE [...]` | Publish a `richdoc.confluence.bundle.v1` directory. |

All three of `page-by-id`, `page get`, `page update`, and
`download` accept either a numeric page id **or** a full Confluence
page URL (e.g.
`https://acme.atlassian.net/wiki/spaces/DEV/pages/123456/Title`).
TinyLinks (`/wiki/x/…`) need to be expanded in a browser first.

## Authentication — the AI agent workflow

The CLI never accepts an API token as a flag, on stdin, or through any
other channel the AI agent can supply. The token MUST be entered by
the human user. The agent's job is to template the config file and
forward instructions.

**Standard recipe (do this exact sequence):**

1. Call `confluence auth init --profile NAME [--site URL] [--email EMAIL] [--space-key KEY]`.
2. Read the `next_steps` array from the JSON envelope. Forward those
   instructions to the user verbatim. Do not try to fill in the token
   yourself.
3. Wait for the user to confirm they've saved the file.
4. Call `confluence auth status --profile NAME` to verify.

For CI / headless contexts, prefer the env-var path — no `auth init`
needed:

```bash
export CONFLUENCE_SITE=https://acme.atlassian.net
export CONFLUENCE_EMAIL=me@acme.com
export CONFLUENCE_TOKEN=...     # CI secret
export CONFLUENCE_SPACE_KEY=DEV
confluence spaces
```

See [references/auth.md](references/auth.md) for the threat model, full
resolution precedence, and the advanced OS-keyring path.

## Downloading existing pages (read side)

The agent workflow for editing a page that already lives in
Confluence:

1. Get a page reference from the human — a numeric id, a page URL,
   or a title within a space.
2. Download the page (and optionally its subtree) locally:
   ```bash
   # Single page from a URL the user pasted:
   confluence download "https://acme.atlassian.net/wiki/spaces/DEV/pages/123456/How+to+deploy" \
       -o ./pulled --markdown --attachments

   # A page and all its descendants:
   confluence download 123456 -o ./pulled --recurse --depth 3
   ```
3. Inspect `./pulled/manifest.json` for the page tree, then read
   `./pulled/pages.jsonl`. Each row is a complete page record with
   the **storage-format XML body** under `body.value`. This is the
   lossless, edit-friendly representation.
4. To edit a page: extract `body.value`, modify the storage XML
   (LLMs handle XHTML + `ac:*`/`ri:*` macros fine), write it to a
   file, then push it back with:
   ```bash
   confluence page update 123456 --body-file edited.storage.xml
   ```
5. The download envelope already suggests this `nextStep` argv so the
   agent has a known-good path forward.

**Important: markdown is read-only.** When `--markdown` is passed,
each page also gets a best-effort `.md` sidecar so a human can skim
it. The conversion is intentionally lossy — info/warning callouts,
code blocks, page links, attachments, expand sections, and task lists
are handled; everything else degrades to HTML comments or plain text.
**Never** re-upload from markdown. Always edit the storage XML in
`pages.jsonl` and push via `page update`.

See [references/download.md](references/download.md) for the full
JSONL/manifest schema, markdown caveats, and worked examples.

## Publishing a richdoc bundle

Always a two-step flow. The agent should pipe `nextStep.argv` from the
richdoc envelope directly into the next command — don't reconstruct
the bundle path by hand.

```bash
# 1. In the richdoc skill: build the bundle (no credentials needed).
richdoc export confluence docs/ -o build/confluence-docs
# Envelope contains: "nextStep": {"argv": ["confluence", "publish-bundle", "<path>"], ...}

# 2. Here: publish it.
confluence publish-bundle build/confluence-docs --profile work --parent-id 12345
```

The publisher is idempotent: re-running updates existing pages in
place (matched by `(space, parent, title)`) and re-uploads only
changed attachments. Cross-page links and attachment references are
resolved post-creation. See
[references/richdoc-bundles.md](references/richdoc-bundles.md).

### Common agent mistakes

- **Do not** pass a `.html` file or a richdoc source directory to
  `confluence publish-bundle`. It will fail with `code: NOT_A_BUNDLE`
  and a hint pointing at `richdoc export confluence`. Always build a
  bundle first.
- **Do not** attempt to run `auth login` — the command no longer
  exists. Use `auth init` to template a config file, then ask the user
  to fill in the token.
- **Do not** echo, log, or include `CONFLUENCE_TOKEN` or any literal
  token value in commands you suggest to the user. Reference env vars
  by name only.

## Output

Every command writes a single-line JSON envelope to stdout. On
success: `{"ok": true, ...}`. On failure: `{"ok": false, "code": "...",
"error": "...", "hint": "..."}`. Exit code matches.

## Limits and trust

- **Confluence Cloud only.** The v2 REST API the client targets does
  not exist on Data Center.
- **Pages and attachments only.** Whiteboards, databases, blog posts,
  comments, and labels are not managed by this CLI yet.
- **Read side is JSONL + storage XML.** `confluence download` pulls
  pages locally losslessly. Markdown is opt-in, best-effort, and
  read-only — re-uploads always go through storage XML.
- **No mirror sync.** Re-downloading does not delete local files;
  uploading does not delete Confluence pages. Stale dumps must be
  pruned manually.
- **Destructive operations require confirmation.** `page delete` (when
  implemented) takes `--confirm`; without it the call errors with
  `CONFIRMATION_REQUIRED`.

## See also

- [references/auth.md](references/auth.md) — profile / env / keyring precedence; corporate-proxy TLS / CA-bundle env vars.
- [references/download.md](references/download.md) — JSONL / manifest schema for `confluence download`, markdown caveats, edit-and-reupload recipe.
- [references/richdoc-bundles.md](references/richdoc-bundles.md) — bundle schema and publish algorithm.
- `richdoc/SKILL.md` — authoring polished HTML documents and producing Confluence bundles.
