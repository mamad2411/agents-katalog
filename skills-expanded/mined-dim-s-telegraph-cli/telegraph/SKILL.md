---
name: telegraph
description: Publish or update a Markdown post on telegra.ph via the `telegraph-publish` CLI. English triggers — "publish to telegra.ph", "post on telegraph", "upload to telegra.ph", "edit telegraph page", "publish as a telegraph article", "make a telegra.ph article from this markdown". Russian triggers — «залей на телеграф», «опубликуй пост на telegra.ph», «оформи как telegra.ph-статью», «выложи на телеграф», «обнови телеграф-страницу», «загрузи картинку на telegra.ph». Also use proactively when the user asks to "publish a long text as an article" without naming a platform — telegra.ph is a sane default for public long-form markdown that needs no auth. Do NOT use for: gists, pastebin, the user's personal blog, any other publishing platform, or for sending a message into a Telegram chat — telegra.ph is a public article host, not a messenger.
---

# telegraph — publish Markdown to telegra.ph

`telegraph-publish` is a CLI that publishes (or updates) a Markdown file as a
telegra.ph article and uploads images. Stdlib-only Python 3, no runtime
dependencies. Source: <https://github.com/dim-s/telegraph-cli>.

**If the `telegraph-publish` command is not found on this machine, read
[setup.md](setup.md) and run the install command before proceeding.** It's
a one-liner via `pip` / `pipx` / `uv tool` and works on macOS, Linux, and
Windows.

The telegra.ph account is created on first run and the access token is
cached in `~/.config/telegraph/account.json` (or
`%APPDATA%\telegraph\account.json` on Windows). Keep that file —
otherwise the pages you created become unmanageable.

## Commands

| Command | Purpose |
|---|---|
| `telegraph-publish <file.md>` | Publish a markdown file, print the URL |
| `telegraph-publish <file.md> --dry-run` | Parse and print stats, do not call the API |
| `telegraph-publish <file.md> --edit <path-or-url>` | Update an existing page with new content |
| `telegraph-publish --upload-image <file>` | Upload an image, print the URL |
| `telegraph-publish <file.md> --no-image-upload` | Skip auto-uploading local `![…](…)` references |
| `telegraph-publish <file.md> --author NAME [--author-url URL]` | Override the per-page author byline (optional, default empty) |
| `telegraph-publish --help` | Full help with supported tags and env vars |

## What the parser supports

- Headings: `# Title` → page title; `##` / `###` → `<h3>`; `####` → `<h4>`.
  telegra.ph has no `<h1>` / `<h2>`, everything collapses to h3 / h4.
- Paragraphs and `---` → `<hr>`.
- Inline: `**bold**`, `*italic*`, `` `code` ``, `[text](url)`.
- Images: a standalone `![alt](src)` block becomes `<figure>` with
  `<figcaption>`. Local paths are auto-uploaded to telegra.ph and replaced
  with the absolute URL.
- Tables: each data row becomes one paragraph with column headers in
  `<strong>` joined by `·` (telegra.ph has no `<table>` — this is the
  fallback rendering).

## Limitations of telegra.ph (not bugs of the CLI)

- **No `<h1>` / `<h2>` and no `<table>`** — this is a platform limit, not
  a parser limit. The CLI collapses headings and expands tables into
  paragraphs.
- **`--upload-image` often returns `Unknown error` (HTTP 400).** telegra.ph
  has throttled its public upload endpoint for external clients since
  ~2022. When this happens, host the image on any CDN and pass an absolute
  URL in markdown. The CLI emits a clear error rather than a stack trace.
- **`--edit` only works for pages created with the same access token.** If
  `~/.config/telegraph/account.json` is deleted, previously created pages
  become read-only.

## Author byline

By default published pages carry no author. To set one, pass `--author
"NAME"` (and optionally `--author-url "URL"`) per call, or set
`TELEGRAPH_AUTHOR` / `TELEGRAPH_AUTHOR_URL` env vars as a fallback. CLI
flags override env. Empty author is valid — telegra.ph renders the page
without an author block.

## Environment variables

- `TELEGRAPH_SHORT_NAME` — short account name (only used on first run,
  baked into `account.json`).
- `TELEGRAPH_AUTHOR` — fallback author name when `--author` is omitted.
- `TELEGRAPH_AUTHOR_URL` — fallback author link when `--author-url` is omitted.

## Typical flow

```bash
# preview
telegraph-publish draft.md --dry-run

# publish
URL=$(telegraph-publish draft.md)
echo "$URL"

# edit the published page
telegraph-publish draft.md --edit "$URL"
```

## What not to do

- Don't publish without `--dry-run` if you're unsure the markdown will
  parse cleanly — telegra.ph has no "delete page" API, drafts you don't
  want pile up in the account.
- Don't `--edit` the user's published post without explicit permission —
  it's an irreversible change to a public artifact.
- Don't retry the `Unknown error` on `/upload` in a loop — it's a platform
  policy, retries don't help; use an external image host instead.
