---
name: slidesfly
description: |
  Publish or share an existing local HTML deck (HTML PPT / slide file) to Slidesfly
  to get a shareable short URL. Use ONLY when (1) a .html file already exists on
  disk AND (2) user mentions "publish / share / 分享 / 发布 / 传到网上 / 给我链接 /
  put online / 上线 / make this shareable", OR wants to manage existing Slidesfly
  decks (list / delete / change visibility / versions / restore / claim / login).

  DO NOT use this skill to generate the HTML deck. If the user wants to create a
  new deck, use a slide-generation skill (e.g. anthropic/slides, codex/slides,
  marp, reveal.js) or write HTML inline FIRST, then invoke this skill to publish
  the resulting file.
version: 0.2.2
license: MIT
---

# Slidesfly Skill

Publish a local HTML deck to [Slidesfly](https://slidesfly.com) and return a shareable link on `slidesfly.xyz`.

## Trigger conditions

**Do trigger** when all of the following are true:

1. A local `.html` or `.htm` file already exists (or was just generated in this session).
2. The user wants to publish, share, or manage an existing Slidesfly deck.

Examples that **should** trigger:

- "Publish this deck and give me a link."
- "把这个 HTML 演示稿发到网上。"
- "Share the slides with my team."
- "List my Slidesfly decks."
- "Delete the deck we published yesterday."

Examples that **should not** trigger:

- "Make me a 10-slide deck about RAG." (generate HTML first, then publish)
- "Improve the typography on slide 3." (edit HTML first)
- "What is Slidesfly?" (answer directly, no CLI)
- "Convert this PDF to HTML." (different task)
- "Deploy this Next.js app." (not a single HTML deck file)

## Prerequisites

1. **HTML file on disk** — single self-contained `.html` is best for v0.
2. **Node.js 22+** — required for the bundled runner, PATH CLI, and MCP.
3. **Prefer MCP when available** — if the host has Slidesfly MCP configured (stdio `@slidesfly/mcp` or hosted `https://slidesfly.com/api/mcp`), use tools `publish` / `list` / `versions` / `restore` / `claim` / `status` (and `set_api_key` on stdio only) instead of shelling out to the CLI. Stdio shares `~/.slidesfly/config.json` with the CLI; hosted uses Bearer `sk_…`.
4. **Use the bundled runner by default** — resolve the directory containing this `SKILL.md` as
   `SKILL_DIR`, then require `$SKILL_DIR/scripts/slidesfly.mjs`. It is the complete official CLI
   built from the same source as the PATH command, not a second API implementation. It performs no
   remote code download and shares `~/.slidesfly/config.json` with the PATH CLI.

```bash
test -f "$SKILL_DIR/scripts/slidesfly.mjs"
node "$SKILL_DIR/scripts/slidesfly.mjs" --version   # expect 0.1.5+
node "$SKILL_DIR/scripts/slidesfly.mjs" publish ./deck.html --title "My Deck" --json
```

For a legacy Cursor `.mdc` installation, the installer stores the runner in the sibling
`slidesfly/scripts/slidesfly.mjs` directory. Resolve that exact path before executing it. If the
bundled runner is absent, a reviewed PATH `slidesfly` `>= 0.1.5` is a compatible fallback; do not
download and execute a replacement during the task.

5. **Install this skill locally** (optional, for persistent agent guidance and the bundled runner):

```bash
slidesfly install --target auto
# or: slidesfly install --target cursor --scope project
# guidance-only legacy mode, without the bundled runner:
slidesfly install --target auto --skill-only
```

All `slidesfly ...` examples below describe the shared command contract. Agents should invoke them
as `node "$SKILL_DIR/scripts/slidesfly.mjs" ...` unless a compatible PATH CLI was deliberately
selected.

## MCP (preferred when configured)

**Stdio** (local): `@slidesfly/mcp` — shares `~/.slidesfly/config.json` with the CLI.

```json
{
  "mcpServers": {
    "slidesfly": {
      "command": "npx",
      "args": ["-y", "@slidesfly/mcp"]
    }
  }
}
```

**Hosted** (remote Streamable HTTP): `https://slidesfly.com/api/mcp` with `Authorization: Bearer sk_…` (no `set_api_key`; publish sends `content_base64` + `filename`).

| Tool | Stdio | Hosted | Purpose |
|---|---|---|---|
| `publish` | `file_path` | `content_base64` + `filename` (+ optional `deck_id`) | Publish / update deck → `slidesfly.xyz` URL |
| `list` | owned + local anon | owned only | List decks |
| `versions` | yes | yes | Version history |
| `restore` | yes | yes | Restore prior version (creates N+1) |
| `claim` | local pending | `items[]` of deck_id + claim_token | Claim anonymous decks |
| `set_api_key` | yes | no | Save `sk_…` locally |
| `status` | yes | yes | Auth / pending state |

Rules: never paste `claim_token` into chat (stdio MCP never returns it on success). Auth via `set_api_key` / prior `slidesfly login` (stdio) or Bearer key (hosted) — no browser PKCE inside MCP. Prefer MCP `versions` / `restore` for owned deck rollback; the bundled runner or compatible PATH CLI remains the fallback for Pro controls (`expire` / `password` / `allowlist`) and skill install.

HTTP reference (no MCP): [OpenAPI](https://slidesfly.com/openapi.yaml). Publish create/update accept optional `Idempotency-Key` (CLI/MCP send a UUID automatically).

## Reader navigation (optional)

Decks can include this script so swipe and keyboard navigation from the Slidesfly reader shell (`slidesfly.xyz/d/...`) reaches in-iframe slide decks via `postMessage`:

```html
<script src="https://slidesfly.xyz/reader-host.js"></script>
```

The shell sends `{ source: 'slidesfly', action: 'next' | 'prev' | ... }`; the host script dispatches keyboard events and Reveal.js API calls when present.

## Deck runtime constraints (sandbox)

Published decks render inside a sandboxed iframe with an **opaque origin** (`allow-scripts allow-popups allow-popups-to-escape-sandbox allow-forms`, no `allow-same-origin`). When generating deck HTML, respect these constraints:

- **JS, forms, and popups work.** Inline `<script>` runs normally; keyboard/slide navigation is fine.
- **`localStorage`, `sessionStorage`, and IndexedDB THROW** (SecurityError) on access; cookies are inert — never rely on browser storage. If a library touches storage, wrap access in `try/catch` or feature-detect; do not persist viewer state.
- **CLI preflight runs before upload.** Runner/CLI 0.1.5 safely inlines eligible local classic
  `.js` files into the upload copy while leaving the source deck unchanged. It blocks remote,
  missing, oversized, module/async/defer/integrity-sensitive, `<base href>`-ambiguous, or otherwise
  unsafe script references before any network request. The server still rejects disallowed script
  sources and blocklisted domains with `MALICIOUS_CONTENT`. Behavior keywords (`eval(`,
  `document.cookie`, `javascript:`, `onerror=`, `onload=`) are accepted but logged as risk signals
  for async review; published decks are also re-scanned asynchronously (Cloudflare Security DNS by
  default; optional Google Safe Browsing) and taken down if flagged.
- **Self-contained is safest**: inline all CSS/JS/images (data URIs) in one file. Multi-file decks may reference their own relative assets only.

## Anonymous-first workflow (default)

**No login is required for the first publish.** The bundled runner posts to the anonymous API,
stores `claim_token` locally, and returns a URL on the content domain:

```bash
slidesfly publish ./deck.html --title "Q4 Plan" --json
```

Example response:

```json
{
  "ok": true,
  "data": {
    "deck_id": "v0c8Kf3sQ1MnEa7bYj9wHt",
    "url": "https://slidesfly.xyz/d/v0c8Kf3sQ1MnEa7bYj9wHt",
    "title": "Q4 Plan",
    "visibility": "unlisted",
    "size_bytes": 184320,
    "anonymous": true
  },
  "warnings": [{
    "code": "ANONYMOUS_LOCAL_ONLY",
    "message": "This deck is managed only on this machine via ~/.slidesfly/config.json. Run slidesfly login to claim it to your account."
  }]
}
```

Agent obligations after publish:

1. Show the full `https://slidesfly.xyz/d/...` URL to the user.
2. Explain visibility (`unlisted` = link-only access by default).
3. Repeat the `ANONYMOUS_LOCAL_ONLY` warning when present.
4. Never paste `claim_token` or raw `~/.slidesfly/config.json` into chat.

## Authenticated publish (when logged in)

After `slidesfly login`, the shared runner/CLI stores an API key in
`~/.slidesfly/config.json`. Subsequent `publish` calls use the owned-deck API (no local
`claim_token`, no `anon_decks` entry):

```bash
slidesfly login --json
slidesfly publish ./deck.html --title "Q4 Plan" --visibility public --json
slidesfly publish ./deck.html --id v0c8Kf3sQ1MnEa7bYj9wHt --json   # update owned deck
slidesfly delete v0c8Kf3sQ1MnEa7bYj9wHt --json
slidesfly visibility v0c8Kf3sQ1MnEa7bYj9wHt public --json
```

Owned publish supports `--visibility public|unlisted|private` (plan limits apply). Use `--id <deck_id>` to upload a new version of an existing owned deck; add `--title` to rename it in the same call. `delete`, `visibility`, `versions`, and `restore` work on owned decks by deck ID when logged in, even if the deck is not in local `anon_decks`. Restore copies a prior version into a new live version (single-file and multi-file).

### Link controls (Pro plan, owned decks)

```bash
slidesfly expire v0c8Kf3sQ1MnEa7bYj9wHt 7d --json        # link stops working in 7 days
slidesfly expire v0c8Kf3sQ1MnEa7bYj9wHt off --json       # remove expiry
slidesfly password v0c8Kf3sQ1MnEa7bYj9wHt "s3cret" --json # viewers must enter password
slidesfly password v0c8Kf3sQ1MnEa7bYj9wHt off --json      # remove password
slidesfly allowlist v0c8Kf3sQ1MnEa7bYj9wHt a@x.com b@y.com --json # email-gated access
slidesfly allowlist v0c8Kf3sQ1MnEa7bYj9wHt off --json     # remove allowlist
```

`expire` accepts durations (`7d`, `24h`, `30m`), ISO-8601 timestamps, or `off`. These commands require login and a Pro plan; on Free they fail with `FORBIDDEN` ("requires the Pro plan") — suggest upgrading at slidesfly.com/pricing instead of retrying. Never echo the password back into chat.

## Command reference

| Command | Purpose |
|---|---|
| `slidesfly publish <file.html> [--title T] [--visibility V] [--id DECK_ID] [--json]` | Publish (anonymous if logged out; owned if logged in). `--id` updates an owned deck; combine with `--title` to rename |
| `slidesfly list [--json]` | List decks stored in local config (no server call) |
| `slidesfly open <deck_id> [--json]` | Open deck URL in browser |
| `slidesfly delete <deck_id> [--json]` | Delete deck (anon: local claim_token; owned: API key) |
| `slidesfly visibility <deck_id> <public\|unlisted\|private> [--json]` | Change visibility (anon: fails with ANONYMOUS_LIMITED; owned: API key) |
| `slidesfly versions <deck_id> [--json]` | List owned deck versions (newest first; marks current) |
| `slidesfly restore <deck_id> <version> [--json]` | Restore owned deck to version N (creates N+1; single- or multi-file) |
| `slidesfly expire <deck_id> <7d\|24h\|30m\|ISO\|off> [--json]` | Set/clear link expiry (login + Pro) |
| `slidesfly password <deck_id> <password\|off> [--json]` | Set/clear viewer password (login + Pro) |
| `slidesfly allowlist <deck_id> <emails...\|off> [--json]` | Set/clear email allowlist (login + Pro) |
| `slidesfly claim [deck_id] [--json]` | Claim anonymous deck(s) to logged-in account |
| `slidesfly login [--no-claim] [--api-key KEY] [--code] [--json]` | Browser PKCE login (default); `--code` for headless/SSH; `--api-key` is fallback |
| `slidesfly logout [--json]` | Clear stored API key (keeps anon_decks) |
| `slidesfly status [--json]` | Show local config summary |
| `slidesfly install [--target auto\|claude-code\|cursor\|codex\|all] [--scope user\|project] [--force] [--from-url URL] [--json]` | Install this skill for Claude Code / Cursor / Codex |
| `slidesfly uninstall [--json]` | Remove installed skill files (does not delete config) |

Global flag: `--api-key <key>` on any command. The bundled runner and PATH CLI intentionally expose
the same command names, arguments, JSON envelope, config path, auth flows, and error codes.

Always pass `--json` when parsing stdout programmatically. Non-TTY stdout auto-emits JSON.

## Common workflows

### Publish a new deck

```bash
slidesfly publish ./deck.html --title "RAG 101" --json
```

### Update or rename a published deck

When logged in, update an owned deck in place (same URL, new content); add `--title` to rename it:

```bash
slidesfly publish ./deck.html --id v0c8Kf3sQ1MnEa7bYj9wHt --json
slidesfly publish ./deck.html --id v0c8Kf3sQ1MnEa7bYj9wHt --title "Q4 Plan (final)" --json
```

When logged out, republish creates a new anonymous deck. After `login` + `claim`, use authenticated publish/update instead.

### Restore a previous version

Owned decks keep version history (including multi-file zips after `--id` updates). List versions, then restore (creates a new live version; the share URL stays the same):

```bash
slidesfly versions v0c8Kf3sQ1MnEa7bYj9wHt --json
slidesfly restore v0c8Kf3sQ1MnEa7bYj9wHt 2 --json
```

Quarantined decks and expiry-purged content cannot be restored this way — re-publish with `--id` instead.

### Protect or expire a shared link (Pro)

```bash
slidesfly password v0c8Kf3sQ1MnEa7bYj9wHt "launch-day" --json
slidesfly expire v0c8Kf3sQ1MnEa7bYj9wHt 7d --json
```

### Manage local anonymous decks

```bash
slidesfly list --json
slidesfly delete v0c8Kf3sQ1MnEa7bYj9wHt --json
```

The shared runner/CLI reads the local `claim_token` and sends it in
`X-Slidesfly-Claim-Token`.
Never put this credential in a query string or hand-build an anonymous management URL.

### Upgrade to account (claim)

When the user needs public visibility, analytics, or cross-machine management:

```bash
slidesfly login --json          # opens browser; auto-claims local anon decks
slidesfly login --no-claim --json   # login only, skip auto-claim
slidesfly claim --json            # claim manually if needed
```

Fallback when browser/loopback login is blocked (SSH, remote devbox, no local browser):

```bash
slidesfly login --code --json
# CLI prints /cli/code URL; user opens it in any browser, copies 8-char code, pastes in terminal
slidesfly claim --json
```

Fallback when no browser access at all:

```bash
slidesfly login --api-key "$KEY" --json
slidesfly claim --json
```

## Error handling matrix

Parse `error.code` from JSON output. Follow retry rules strictly.

| Code | HTTP | Agent action | User message template |
|---|---|---|---|
| `INVALID_HTML` | 422 | Do not retry | "HTML 格式有问题：{details}。需要我重写吗？" |
| `MALICIOUS_CONTENT` | 451 | Do not retry | "Slidesfly 拒绝了该 deck（{details}）。误判可去 /report 申诉" |
| `QUOTA_EXCEEDED` | 402 | Do not retry; suggest login | "匿名配额已用完。运行 `slidesfly login` 注册后可发更多" |
| `RATE_LIMITED` | 429 | Wait 60s, retry once | 终失败："Slidesfly 限频中，请稍后再试" |
| `AUTH_REQUIRED` | 401 | Do not retry; prompt login | "需要登录。运行 `slidesfly login` 后我再试" |
| `AUTH_INVALID` | 401 | Do not retry; re-login | "Token 失效，运行 `slidesfly login` 重新授权" |
| `FORBIDDEN` | 403 | Do not retry | "无权操作该 deck。匿名 deck 可先 `slidesfly login` 再 claim" |
| `DECK_NOT_FOUND` | 404 | Do not retry | "Deck `{id}` 不存在或已删除" |
| `EXPIRED` | 410 | Do not retry | "Deck 已过期" |
| `PASSWORD_REQUIRED` | 401 | Ask user for password | "该 deck 有密码保护，请告诉我密码" |
| `ANONYMOUS_LIMITED` | 403 | Suggest login + claim | "匿名 deck 只能 unlisted。要登录认领后再改吗？" |
| `INTERNAL_ERROR` | 500 | Retry once | "Slidesfly 后端错误，稍后重试" |
| `SERVICE_UNAVAILABLE` | 503 | Wait 30s, retry once | 终失败："Slidesfly 上游不可用" |

**Network errors:** wait 5s, retry once, then stop.

**Global rules:**

- Never auto-rewrite HTML after `INVALID_HTML` or `MALICIOUS_CONTENT`.
- Do not retry other 4xx errors (except one 429 retry).
- Retry 5xx at most once.

## Output contract

Success:

```json
{ "ok": true, "data": { ... }, "warnings": [ ... ] }
```

Failure:

```json
{ "ok": false, "error": { "code": "...", "message": "...", "hint": "..." } }
```

Human TTY mode prints minimal text (usually the URL). Agents should always use `--json`.

## Sandbox notes

If the bundled runner is unavailable:

1. Check for a preinstalled `slidesfly` binary on PATH (`~/.slidesfly/bin` after website install).
2. Continue only if `slidesfly --version` is `0.1.5` or newer.
3. Otherwise stop and direct the user to the official technical quickstart. Do not download or
   execute a remote installer, ad-hoc `cli.mjs`, or unverified npm package from this Skill.
4. Do not hand-build a multipart publish request: use the bundled runner, a compatible PATH CLI, or
   configured MCP so `claim_token` stays off chat transcripts.

If loopback login is blocked, use `slidesfly login --code` (headless device flow) or `slidesfly login --api-key` with a key from the dashboard.

## Example dialogues

**Success:** User asks to publish an existing `deck.html` → run publish with `--json` → return `https://slidesfly.xyz/d/...` + anonymous warning.

**Quota exceeded:** Surface `QUOTA_EXCEEDED`, suggest `slidesfly login`, do not spam retries.

**Malicious content:** Surface `MALICIOUS_CONTENT` verbatim, do not modify HTML and retry.

**Cross-machine:** `slidesfly list` empty → explain local-only anon decks; offer `slidesfly login` + claim on original machine.

**Go public:** When logged out, `visibility public` on anon deck → `ANONYMOUS_LIMITED` → suggest `slidesfly login` + claim, or publish with `--visibility public` after login.

## Privacy & security

- Do not expose `~/.slidesfly/config.json`, API keys, or `claim_token`.
- Anonymous update/delete requests carry `claim_token` only in the
  `X-Slidesfly-Claim-Token` header; credential-bearing routes reject every query
  parameter. Account claim sends tokens only in its JSON body.
- Prefer the bundled runner. Install a PATH CLI only through the official technical quickstart or a
  reviewed binary—never ad-hoc `/tmp` + `cli.mjs`.
- Anonymous `publish --json` must not print `claim_token` (runner/CLI ≥ 0.1.3 keeps it in local
  config only).
- Default visibility is `unlisted` unless the user explicitly asks for `public`.
- Share URLs live on `slidesfly.xyz`; SaaS dashboard lives on `slidesfly.com`.

<!-- slidesfly-skill version: 0.2.2 -->
