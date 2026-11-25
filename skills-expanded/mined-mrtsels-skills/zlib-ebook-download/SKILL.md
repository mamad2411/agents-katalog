---
name: zlib-ebook-download
title: zlib-ebook-download
description: Search and download ebooks from Z-Library via the `zlib` CLI (brew-installed). Covers search, domain config, TTY workaround for non-interactive environments, and format handling.
tags: [zlib, zlibrary, ebook, download, book-search]
---

# zlib-ebook-download

## When to use

User asks to search for or download a book from Z-Library (z-lib, zlibrary, singlelogin).

## CLI tool

`zlib` — installed via `brew install zlib` (Go-based CLI for Z-Library).

Binary at `/opt/homebrew/bin/zlib`.

## Config

Config file: `~/.config/zlib/session.json`

```json
{
  "cookies": { ... },
  "domain": "https://z-library.im"
}
```

**Domain changes frequently.** When search/download fails with `failed to parse page: searchResultBox not found` or network timeout, the domain is likely hijacked. Update the `domain` field in session.json to the current working Z-Library domain.

Known good domains (subject to change):
- `https://z-library.im` (current)
- `https://z-lib.sk` (may work with cookies)

Verify a domain responds correctly: `curl -sL -o /dev/null -w "%{http_code}" --connect-timeout 8 "https://<domain>/"`

## Search

```bash
zlib search "<query>"
```

Output shows: ID, Title, Authors, Year, Format, Size, Rating.
The format column determines the download format (EPUB, TXT, PDF, etc.).

## Download

The `zlib download` command requires a TTY (it uses terminal prompt libraries). In non-interactive environments (Hermes terminal tool, scripts), use `script -q` as a workaround:

```bash
script -q /dev/null zlib download <book-id> -d <dir> < /dev/null
```

**Parameters:**
- `<book-id>` — the ID from search results (e.g. `Wkmo1oqlZj`)
- `-d <dir>` — destination directory (default: current dir)

The downloaded format matches what was shown in search results.

## Pitfalls

- **Domain hijacking**: Z-Library domains get seized/hijacked frequently. A hijacked domain returns 200 but serves a parked page or porn site. Always verify the actual page content if search fails.
- **TTY requirement**: `zlib download` opens `/dev/tty` for confirmation prompts. `script -q /dev/null ... < /dev/null` is the workaround — plain pipe (`echo y | ...`) does NOT work.
- **Cookie expiry**: Session cookies expire. If auth fails, re-login via `zlib login` (interactive, needs real TTY).
- **No format override**: The CLI doesn't support `--format` flag. Download format is determined by which result you select.
