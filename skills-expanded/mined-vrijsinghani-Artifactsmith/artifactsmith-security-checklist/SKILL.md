---
name: artifactsmith-security-checklist
description: >-
  Project-specific security checklist for ArtifactSmith. Covers HTML/CSS
  sanitization of model output, spreadsheet formula injection, concurrent job
  races, resource limits, secrets in metadata, and private-host links. Use when
  reviewing ArtifactSmith changes, auditing output safety, or verifying that a
  previously fixed bug class has not returned.
---

# ArtifactSmith security checklist

Model output is untrusted. Hosted preview adds CSP; downloaded / standalone HTML does not. Stored bytes must be safe without CSP.

Do not mark an item pass from reading tests alone. Reproduce it.

## 1. HTML and CSS sanitization

Target: `src/artifactsmith/renderers/html_sanitize.py`, then `builder.sanitize_html` / `run_build`.

Run each payload through `sanitize_html_document` and, for XSS claims, open the standalone export in headless Chromium with **no CSP**.

| Payload class | Example | Fail if |
|---|---|---|
| Style-block breakout | `<style>p{}</style><script>alert(1)</script>` or `</style>` inside CSS | Script or raw `</style>` survives into the stored document |
| Entity-encoded closer | `<style>p{color:red}&lt;/style&gt;<script>alert(1)</script>` | Unescape-then-parse turns entities into a real close tag |
| CSS `url()` / escapes | `background:u\72l(https://evil)` or `url(//evil)` | Any fetch-capable function remains after tinycss2 resolution |
| `@import` / `@\69mport` | `@\69mport url(https://evil)` | At-rule or escaped at-rule fetches |
| `image-set` / `-webkit-image-set` | `background:image-set(url(https://evil) 1x)` | Function kept |
| `@font-face` | `@font-face{src:url(https://evil)}` | Font fetch remains |
| Backslash hrefs | `href="javascript:\\nalert(1)"`, `href="/\\evil.example/"`, `href="\\evil"` | Browser would treat `\` as `/` and navigate or run JS |
| `javascript:` / `data:` | `href="javascript:alert(1)"`, `href="data:text/html,..."` | Attribute kept |
| Protocol-relative `//host` | `href="//example.com"`, `href="//127.0.0.1/"` | Public host is not upgraded to `https://`; private host is kept or upgraded |
| Inline `style=` url | `style="background:url(https://evil)"` | Fetch-capable value kept |

Also confirm `<img src>`, `cite`, and rebuilt `<title>` cannot smuggle markup.

## 2. Spreadsheet formula injection

Target: `src/artifactsmith/renderers/xlsx.py`.

Round-trip through `XlsxRenderer.render` and open with openpyxl (data_only=False).

| Check | Fail if |
|---|---|
| Cell starts with `=`, `+`, `-`, `@` | Cell is a formula (`data_type` is `f`) rather than a string |
| Leading tab/space before `=` | Excel still evaluates it as a formula |
| Numeric-looking text (`"007"`, `"1e2"`) | Stored as a number (loses leading zeros / becomes scientific) |
| Title, notes, headings, list items | Any of those sheets write unquoted formula text |

Ints, decimals, currency, and percents in table cells are stored as numbers with Excel formats. IDs with leading zeros and scientific-looking tokens stay text. Formula-like values (`=`, `@`) stay strings.

## 3. Concurrent jobs

Target: `src/artifactsmith/service.py`, `db.py`, worker claim SQL.

Use threads/asyncio plus a barrier or `BEGIN IMMEDIATE` contention. Fail if any of these succeed:

1. **Delete vs edit**: delete confirm races an in-flight edit/upload and leaves object-store bytes or a live share for a deleted id.
2. **Delete vs upload**: worker writes files after `delete` purged the row.
3. **Duplicate claim at startup**: two workers (or restart + live worker) claim the same `queued`/`building` job.
4. **Thread-unsafe enqueue**: `create`/`edit` from a non-loop thread drops or double-enqueues a job (`asyncio.Queue` is not thread-safe for `put_nowait`).
5. **Idempotency**: same `idempotency_key` with a different fingerprint is accepted as the first result, or the same fingerprint creates two artifacts.

## 4. Resource limits

Confirm each bound is enforced in code, not only documented.

| Limit | Where to check | Fail if |
|---|---|---|
| Render deadline | `AM_RENDER_TIMEOUT`, `subprocess_render.render_killable` for PDF/DOCX/XLSX. HTML and Markdown use `render_inprocess` (capped text encode, no child). | A PDF/DOCX/XLSX renderer ignores timeout or leaves the child alive |
| Build deadline | `AM_BUILD_TIMEOUT` | Job can run past the cap |
| Memory / output size | `AM_MAX_OUTPUT_BYTES` | Oversize HTML/PDF/XLSX is stored |
| Input size | `SOURCE_CAP_BYTES`, `VERBATIM_CAP_CHARS` | Caps are bypassed via `source_files` split or edit reuse |
| Model output size | `check_content(..., max_chars=)` | Multi-megabyte model text is parsed/rendered unbounded |
| Concurrency / quota | `AM_MAX_BUILDS`, `AM_BUILDS_PER_HOUR` | Extra workers start, or quota is per-process not per-token |

## 5. Secrets in titles, summaries, assumptions

Target: `check_fields` in `safety.py`, called from `run_build` **before** cards are stored.

1. Put a `sk-` / `ghp_` / PEM / `AKIA` / Slack / Bearer string in `display_name`, `===SUMMARY===`, and an assumption line.
2. Fail if the build succeeds and the secret appears in `inspect`, list cards, or share metadata.
3. Fail if only the HTML/Markdown body is scanned.
4. Record that detection is heuristic; note any realistic secret shape that is not in `SECRET_PATTERNS`.

## 6. Links must never point at private hosts

Target: `find_private_links`, `AM_BLOCK_PRIVATE_LINKS` (default true), `AM_ALLOWED_LINK_DOMAINS`.

Reject (or strip, then still fail closed) all of:

- `http://127.0.0.1`, `http://localhost`, `http://[::1]`
- RFC1918 (`10.`, `172.16–31.`, `192.168.`)
- Link-local, metadata (`169.254.169.254`, `metadata.google.internal`)
- `*.local`, `*.internal`, `*.localhost`, `*.lan`, `*.corp`, `*.home.arpa`, bare single-label hosts
- Decimal/hex IP forms if a browser would still hit a private address
- Known wildcard-DNS suffixes that alias loopback (`nip.io`, `sslip.io`, …)

Also fail if:

- An entity-like query name (`https://example.com/?a=1&section=2`) is rewritten on emit (HTML-unescape or percent-decode of the destination)
- Host-reading disagrees across de-obfuscated, urllib, and WHATWG-style parses (backslash, userinfo, hidden whitespace) and the link is still kept
- A Markdown escape round-trip or linkify pass relinks a destination that the first pass neutralized
- `AM_BLOCK_PRIVATE_LINKS=false` is the documented default, or empty `AM_ALLOWED_LINK_DOMAINS` silently allows every public host while private-link blocking is off

Standalone exports and Markdown/PDF/DOCX/XLSX bodies are in scope, not only hosted preview. Public `http(s)` citations to global hosts may stay.

Also open the stored Markdown in at least one outside renderer (pandoc
`--from gfm` / `--to html`, or GitHub-flavored Markdown preview). Fail if
that renderer linkifies or restores a destination this repo's parser
neutralized. Do not pass the item from this repo's markdown-it path alone.

## How to record a result

For each item: payload or race setup, file:line of the sink, whether the control held, and one concrete fix if it failed.