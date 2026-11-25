---
name: safe-content-disposition-rfc5987
description: Build a Content-Disposition header that survives non-ASCII filenames on every browser using the RFC 5987 filename* encoding.
category: fastapi
version: 1.0.0
version_origin: extracted
tags: [http, headers, fastapi, i18n, downloads]
source_type: extracted-from-git
source_url: https://github.com/jamiepine/voicebox.git
source_ref: main
source_commit: 476abe07fc2c1587f4b3e3916134018ebacd143d
source_project: voicebox
confidence: high
imported_at: 2026-04-18T00:00:00Z
---

# Safe Content-Disposition RFC 5987

## When to use
Your API serves user-authored filenames (uploaded clips, generated audio, exported bundles) which may contain non-ASCII characters, emojis, spaces, or punctuation. You want every browser to download with the correct filename and stop logging header-validation warnings.

## Steps
1. Strip the "ascii-safe" fallback by keeping only alphanumerics plus a small allowlist (` `, `-`, `_`, `.`). Trim whitespace; if nothing survives, fall back to a sensible default like `"download"`. This becomes the `filename="..."` parameter.
2. Build the Unicode fallback with `urllib.parse.quote(filename, safe="")`. This percent-encodes UTF-8 bytes so the `filename*` parameter is RFC 5987 compliant (`filename*=UTF-8''<percent-encoded>`).
3. Concatenate as `"<disposition_type>; filename=\"<ascii>\"; filename*=UTF-8''<utf8>"`. Browsers that understand RFC 5987 use `filename*`; older ones fall back to `filename` and still get something reasonable.
4. Expose a single helper (e.g. `safe_content_disposition(kind, filename)`) and route every download handler through it. Do not build the header ad-hoc per endpoint.
5. When serving with FastAPI `FileResponse`, pass `filename=<bare unicode>` only when you own the filename — for user input, use your helper and set the header directly via `Response(..., headers={"content-disposition": ...})`.

## Counter / Caveats
- Quotes inside the ASCII filename will break the header. The strict `isalnum() or c in " -_."` filter eliminates them by construction — loosen that filter only if you also escape quotes.
- Don't include control characters (< 0x20) in the ASCII fallback even if your filter allowed them; they corrupt the header.
- Some older (pre-2013) browsers choke on `filename*` if `filename` is missing entirely; always emit both.
- If your framework auto-sets `Content-Disposition` from `filename=` on `FileResponse`, explicitly override the header afterwards or the framework's unsafe version may win.

Source references: `backend/app.py` (`safe_content_disposition`).
