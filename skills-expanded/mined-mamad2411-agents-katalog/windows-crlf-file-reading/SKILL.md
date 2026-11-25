---
name: windows-crlf-file-reading
description: Use when read_file flags CRLF/emoji files as binary.
version: 1.0.0
author: Hermes Agent (curator)
metadata:
  hermes:
    tags: [windows, crlf, read_file, binary, utf8, markdown, reports, cat-v]
    triggers:
    - read_file binary
    - binary file cannot display as text
    - CRLF
    - is_binary true
    - daily brief unreadable
    - cat -v
    - grep -a
    related_skills: [windows-cross-platform-debugging, recurring-status-checks, discord-report-format]
---

# Windows CRLF File Reading

On this Windows host, report files written with CRLF line endings + emoji/em-dash characters (daily briefs, council reports, digests — e.g. `_project/06-reports/**`, `daily-digest/**`) are valid UTF-8 text but Hermes file tools misdetect them as binary.

## The Trap

`read_file` returns `{"content": "", "is_binary": true}` with "Binary file - cannot display as text" for these files. Plain `grep`/`rg` also silently skips them (same binary misdetection) unless `-a` is passed. The file is NOT actually binary — `file` reports `Unicode text, UTF-8 text, with CRLF line terminators`.

## Diagnosis

```bash
file "path/to/report.md"     # → Unicode text, UTF-8 text, with CRLF line terminators
```

If `file` says Unicode/UTF-8 text, the content is readable — just not by `read_file`.

## Fix Pattern — Read via Terminal

```bash
head -c 2000 "path/to/report.md" | cat -v
```

`cat -v` renders em-dashes as `M-bM-^@M-^` and emoji as `M-x...` sequences — decodable enough to extract content. Plain `cat` also works; terminal tools don't apply the binary misdetection. For a full file, use `cat` piped to `sed`/`grep -a` as needed.

## Write / Append Safely

- **Never** `write_file` after a partial `read_file` (empty content) — you'd truncate the file to nothing. Read the full content via terminal first, or use the dedicated append script (`scripts/append-digest.py`) for digest-style logs.
- For byte-exact edits, use Python `pathlib` with `read_bytes()`/`write_bytes()` (preserves CRLF); text mode normalizes line endings.
- Verify with `grep -a pattern file.md`, not plain `grep`.

## Pitfalls

- Don't conclude the file is corrupt or empty from `read_file` alone — check `file` first.
- Don't rewrite CRLF files as LF unless that's intended — `write_file` normalizes line endings and can churn git diffs on CRLF-tracked repos.
- This is a tool misdetection, not a broken file — the same class as `grep` needing `-a`.

## Related

- `windows-cross-platform-debugging` — broader Windows/MSYS path + CRLF quirk catalog (user-owned; `hermes curator adopt` to make editable).
- `recurring-status-checks` — daily-brief reconstruction workflow that reads these report files (user-owned).
