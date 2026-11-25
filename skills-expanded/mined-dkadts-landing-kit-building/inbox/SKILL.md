---
name: inbox
description: Sorts client materials from inbox/. Verifies compliance with content-pipeline requirements (naming, formats, sizes). Produces a "ready / needs rework" report.
---

# /inbox

First pass over client materials. **Does not convert** (that's `/media`), **does not analyze text** (that's `/copy-analyze`) — only sorts and validates.

## When to use

- Client says "materials uploaded".
- After a new batch arrives (top-up).

## Process

**Step 1. Read `brief/08-content-pipeline.md`**
Load requirements: naming, formats, sizes.

**Step 2. Walk `inbox/` folders**

For each folder (`texts/`, `media/photos/`, `media/videos/`, `brand/logo/`, `brand/fonts/`, `notes/`):
- List files.
- Verify: naming ASCII? correct format? size within limits?
- Mark: ✅ OK / ⚠️ warning / ❌ reject.

**Step 3. Specific checks**

**texts/:**
- UTF-8?
- Section headings present (`# Hero`, `# Offer`)?

**media/photos/:**
- Min side ≥ 2400px (read via image tool or `identify`).
- sRGB (not Adobe RGB — otherwise color shift in the browser).
- ASCII filenames.
- No `IMG_1234.jpg`.

**media/videos/:**
- 1080p+.
- Bitrate ≤ 20 Mbps.
- H.264 in MP4 (not HEVC — poor browser support).

**brand/logo/:**
- SVG only.
- Text outlined (check: is there a `<text>` tag inside SVG — if yes, NOT outlined).
- No embedded raster (no `<image>` inside).

**brand/fonts/:**
- `.woff2` only.
- `LICENSE.txt` present.

**notes/:**
- List with type (audio / image / md / other).
- Transcribe voice notes (if possible).

**Step 4. Produce the report**

Create/update `inbox/inbox-report.md`:

```markdown
# Inbox report — 2026-08-08

## Overall
- Files total: N
- OK: N | Warning: N | Reject: N

## texts/
- `copy.md` — ✅ OK (UTF-8, 5 sections)
- `about.docx` — ⚠️ convert to MD

## media/photos/
- `hero-01.jpg` — ✅ 3600×2400, sRGB
- `IMG_1234.jpg` — ❌ rename to ASCII
- `founder.tif` — ⚠️ 6000×4000 > 6000px — will be cropped

## brand/logo/
- `logo.svg` — ❌ text not outlined (found <text>)

## Summary for the client
### Ready
- Texts can go to /copy-analyze
- Hero photo (after rename)

### Needs rework
- 3 photos: rename
- Logo: outline (in Illustrator: Type → Create Outlines)
- `about.docx`: convert to MD

## Next
- Wait for client rework
- OR if user says "ship with what we have" — run /media on ok-files and /copy-analyze on texts
```

**Step 5. Extract links from notes/**

If notes contain URLs — offer to move them into `references/` by aspect.

## Rules

- **Do not convert files here.** Only validate and sort.
- **Do not complain if materials are thin.** Just report "we have X, for a full landing we need Y".
- **Do not delete `reject` files.** Only mark in the report — user decides.

## Next

- `/copy-analyze` on texts.
- `/media` on photos and videos.
