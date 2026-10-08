---
name: heic-to-jpeg-bundle
description: Convert a folder of iPhone HEIC photos to JPEG and package them for sharing — a browsable thumbnail gallery plus an optional password-protected ZIP sized to fit a static host's per-file cap. Uses macOS sips (zero install). Use when someone can't open HEIC (Windows, appraisal/CRM software, older tools), when you need to hand a non-technical recipient a JPEG photo set, or when prepping images for a static-hosted gallery. TRIGGERS - heic to jpeg, convert heic, jpeg bundle, photo gallery zip, heic wont open, share photos as jpeg, password protected photo zip.
allowed-tools: Bash, Read, AskUserQuestion
argument-hint: "[source folder of HEIC images]"
---

# heic-to-jpeg-bundle

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

Turn a folder of HEIC (or any `sips`-readable) images into a share-ready JPEG bundle:
a self-contained gallery page plus an optional password-protected ZIP. Everything runs
through macOS `sips` and `zip` — **no Homebrew, no Python, no ImageMagick.**

## Why this exists

iPhones shoot **HEIC** by default. HEIC is poorly supported on Windows and in a lot of
appraisal / CRM / dealer / insurance software, so recipients hit a wall: they can see the
file but can't open or import it, and free online converters are flaky. Re-encoding to
JPEG once, locally, removes that wall for everyone downstream.

## When to use

- A recipient says they "can't open" / "can't convert" your photos (HEIC → JPEG).
- You're handing a photo set to a non-technical person or to software that wants JPEG.
- You're prepping images to drop on a static host (see the companion
  `cloudflare-workers-publish` skill) and want a gallery + a bulk-download ZIP.

For the **full end-to-end playbook** (pull from a cloud album → bundle → host unlisted →
share via a gist gateway), see the `photo-gallery-delivery` skill, which orchestrates this one.

## Quick start

```bash
SKILL_DIR="$(dirname "$(find ~/.claude ~/eon -path '*/heic-to-jpeg-bundle/scripts/make-bundle.sh' 2>/dev/null | head -1)")"

# Gallery + password-protected ZIP that fits the Cloudflare Workers 25 MiB cap:
bash "$SKILL_DIR/make-bundle.sh" \
  --src ~/Pictures/my-photos \
  --title "2023 Corolla Cross — trade-in photos" \
  --zip --password "CorollaCross2023" --zip-cap-mib 25

# Also emit a full-resolution JPEG tier (host its ZIP off a large-file host, not Workers):
bash "$SKILL_DIR/make-bundle.sh" --src ~/Pictures/my-photos --full --zip
```

Output:

```
<src>/_bundle/site/index.html        # gallery: thumbnails -> full "view" JPEGs
<src>/_bundle/site/photos/photo-NNN.jpg
<src>/_bundle/site/thumbs/photo-NNN.jpg
<src>/_bundle/site/bundle.zip        # when --zip and it fits the cap
<src>/_bundle/full/photo-NNN.jpg     # when --full (full-res tier)
```

Deploy the `site/` directory to any static host. Tap-through opens the 2048px "view"
JPEG, so close-up detail (VIN stickers, odometer, damage) stays legible even if the ZIP
tier was downscaled to fit a size cap.

## Options

| Flag             | Default         | Meaning                                                  |
| ---------------- | --------------- | -------------------------------------------------------- |
| `--src DIR`      | (required)      | Source folder of `.heic/.jpg/.png/.tiff` (non-recursive) |
| `--out DIR`      | `<src>/_bundle` | Output root                                              |
| `--title "TEXT"` | `Photos`        | Gallery heading + `<title>`                              |
| `--view-edge PX` | `2048`          | Long edge of the per-photo "view" JPEGs                  |
| `--view-quality` | `82`            | JPEG quality (1–100) for the view tier                   |
| `--full`         | off             | Also emit a full-resolution JPEG tier (no resize)        |
| `--zip`          | off             | Build a ZIP of the view tier                             |
| `--zip-cap-mib`  | `25`            | Auto-downscale the ZIP tier until it lands under N MiB   |
| `--password PW`  | none            | Encrypt the ZIP (ZipCrypto)                              |
| `--jobs N`       | `6`             | Parallel `sips` workers                                  |

## Key facts and gotchas

- **`sips` honors EXIF orientation** when it resamples (`-Z`), so portrait shots come out
  upright. It ships on every macOS — never reach for ImageMagick/`magick` for this.
- **Static hosts cap file size.** Cloudflare Workers Static Assets reject any single file
  **> 25 MiB** (hard error: `Asset too large`). A ZIP of ~120 full-res iPhone JPEGs is
  ~100–500 MB and will **not** fit — hence `--zip-cap-mib`, which downscales the ZIP tier
  (not the gallery) until it fits. For a true full-resolution bulk download, host that ZIP
  on a large-file host (R2, a GitHub Release, your own server), not on Workers.
- **ZipCrypto, on purpose.** `--password` uses classic ZipCrypto (`zip -e`), which Windows
  Explorer, 7-Zip, and macOS Archive Utility all open natively with the password. AES-256
  zips are stronger but need 7-Zip on the recipient's end — more friction for a
  non-technical recipient, so ZipCrypto is the pragmatic default. It's a light access gate,
  not strong cryptography.
- **Password-on-the-gateway model.** The gallery page never prints the ZIP password. Put
  the password only on whatever gateway you share (a gist, an email, a message). Then
  finding the bare ZIP URL alone won't open it — the gateway is required. See
  `cloudflare-workers-publish` for the hosting side.
- **JPEGs are already compressed**, so the ZIP uses store (`-0`), not deflate — zipping
  doesn't shrink them and `-0` is faster.
- **Filenames with spaces/parentheses** (Amazon/iCloud exports) are handled — the script
  reads sources null-safely and renames outputs to stable `photo-NNN.jpg`.
- **The gallery is emitted as pure ASCII** (every non-ASCII char — em-dash, middot, arrows,
  emoji, and anything in your `--title` — is folded to a numeric HTML entity like `&#8212;`).
  ASCII is byte-identical under UTF-8 / Latin-1 / Windows-1252, so the page **cannot mojibake**
  even if a host serves `text/html` with no `charset` (Cloudflare Workers does exactly that).
  A build-time guard (`iconv -f ASCII`) fails the run if any non-ASCII byte survives.
  - **Hazard this prevents:** never run an in-place `perl -pe` / `sed -i` edit that _inserts_
    non-ASCII (e.g. `\x{2014}`, `\x{2B07}`, an emoji) over a UTF-8 file **without the `-CSD`
    layer** — perl will read the existing multibyte bytes as Latin-1 and re-emit them as UTF-8,
    silently corrupting them (the tell-tale `Wide character in print` warning). Each pass
    re-encodes again. If you must post-edit generated HTML, edit ASCII entities, or use
    `perl -CSD`. This skill avoids the pattern entirely by folding to entities once.

## Preflight

`sips` and `zip` are macOS built-ins; the script fails fast if either is missing. No other
dependencies.

## Post-Execution Reflection

After running, before closing:

1. **Did conversion or the ZIP fail?** Fix the step in `make-bundle.sh` that caused it.
2. **Did a host reject a file for size?** Confirm `--zip-cap-mib` matches that host's real
   cap, and record the cap if it differs from 25 MiB.
3. **Did a recipient still struggle to open the ZIP?** Note their tool; if AES was needed,
   document it. Update this SKILL.md only for real, reproduced issues.
