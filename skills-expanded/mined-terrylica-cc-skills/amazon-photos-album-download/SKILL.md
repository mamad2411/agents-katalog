---
name: amazon-photos-album-download
description: Download the original photo and video files from a public Amazon Photos shared album (an amazon.com/amazon.ca /photos/share/<id> link) via Amazon Drive's own JSON API, no login required. Drives headless Chrome with Playwright, lists the album nodes, and pulls size-verified originals. Use when you need a local copy of every file in a shared Amazon Photos album, to re-process or re-host them (e.g. convert HEIC to JPEG, build a gallery). TRIGGERS - amazon photos download, download shared album, amazon photos share link, pull amazon album, amazon drive share, save amazon photos.
allowed-tools: Bash, Read, AskUserQuestion
argument-hint: "[Amazon Photos share URL]"
---

# amazon-photos-album-download

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

Download every **original** file from a **public Amazon Photos shared album** —
the kind of link you get from "Share → Copy link", e.g.
`https://www.amazon.ca/photos/share/qGAyl…`. No Amazon login is needed for a
public share; the album authorizes anonymously via its `shareId`.

## When to use

- You shared an album with someone and need the originals back locally to
  re-process them (the #1 case: **convert iPhone HEIC originals to JPEG** for a
  recipient who can't open HEIC — then see the `heic-to-jpeg-bundle` skill).
- You want to re-host an album's photos yourself (a static gallery, a ZIP).
- You need a verified, complete local backup of a share you (or someone) sent.

## How it works

Amazon Photos is a React app over **Amazon Drive's `/drive/v1/` JSON API**. A
public share exposes, with just the `shareId` as auth:

1. `GET /drive/v1/shares/<shareId>` → the root `SHARED_COLLECTION` node id.
2. `GET /drive/v1/nodes/<root>/children?limit=1…` → the album **folder** node id.
3. `GET /drive/v1/nodes/<album>/children?filters=…image*+OR+video*…&limit=200…`
   → the list of asset nodes (name, `contentProperties.contentType`, `size`).
4. per node: `GET /drive/v1/nodes/<id>/contentRedirection?download=true&shareId=…`
   → the original bytes.

The script runs the JSON calls **inside a headless Chrome page** (via Playwright)
so they carry the exact cookies/headers the web app uses, then writes each file
under its real name and **verifies the byte size** against `contentProperties.size`.
A `manifest.json` records every node id, name, type, and size.

## Prerequisites

- `bun`, `playwright-core`, and **Google Chrome** installed.
- The album link must be **public** (open it once in a logged-out browser to
  confirm it doesn't redirect to a sign-in wall).

```bash
# one-time, in the dir you'll run from (or any scratch dir):
mkdir -p ~/scratch/amazon-album && cd ~/scratch/amazon-album
bun add playwright-core
```

## Quick start

```bash
SKILL_DIR="$(dirname "$(find ~/.claude ~/eon -path '*/amazon-photos-album-download/scripts/download-album.ts' 2>/dev/null | head -1)")"

ALBUM_URL="https://www.amazon.ca/photos/share/REPLACE_WITH_SHARE_ID" \
ALBUM_OUT="$HOME/Pictures/my-album-originals" \
bun "$SKILL_DIR/download-album.ts"
```

Then convert + bundle for sharing:

```bash
BUNDLE="$(dirname "$(find ~/.claude ~/eon -path '*/heic-to-jpeg-bundle/scripts/make-bundle.sh' 2>/dev/null | head -1)")"
bash "$BUNDLE/make-bundle.sh" --src "$HOME/Pictures/my-album-originals" --zip --zip-cap-mib 25
```

## Options (env vars)

| Env                    | Default                        | Meaning                             |
| ---------------------- | ------------------------------ | ----------------------------------- |
| `ALBUM_URL`            | (required)                     | The `/photos/share/<id>` URL        |
| `ALBUM_OUT`            | `./album-originals`            | Output directory                    |
| `ALBUM_INCLUDE`        | `image`                        | `image`, `image,video`, or `all`    |
| `ALBUM_PROFILE_DIR`    | `~/.cache/amazon-album/chrome` | Persistent Chrome profile dir       |
| `ALBUM_CHROME_CHANNEL` | `chrome`                       | Playwright Chrome channel           |
| `ALBUM_PAUSE_MS`       | `800`                          | Delay between downloads (be gentle) |

## Key facts and gotchas

- **The album may hold more than you think.** A "~40 photo" album can list 100+
  asset nodes once you count Live-Photo stills and videos. The default
  `ALBUM_INCLUDE=image` keeps just still images; widen it if you want videos.
- **`contentRedirection?download=true` returns the original**, not a thumbnail.
  The album-listing `tempLink`s can be downsized (the app requests
  `lowResThumbnail=true`); always pull originals via `contentRedirection`.
- **Run the JSON calls in-page.** Calling `/drive/v1/` from plain `curl` fails —
  the share auth rides on the browser context. The script uses `page.evaluate`
  (JSON) + `context.request` (binaries), both inside the loaded album context.
- **Size-verify.** Each file is checked against `contentProperties.size` (±2%);
  the `manifest.json` `verified` count should equal `selected`.
- **Undocumented API.** This is Amazon's internal Drive API. It works today; if
  it breaks, load the album in a **headed** browser and re-watch the `/drive/v1/`
  requests to re-derive the endpoints.
- **Privacy.** Originals often carry GPS EXIF, license plates, VIN/odometer, and
  home surroundings. Store them outside any git repo and don't re-host them
  publicly without thought (an unlisted host + the `heic-to-jpeg-bundle` password
  ZIP is the cautious default).

## Post-Execution Reflection

After running, before closing:

1. **Did `verified` < `selected`?** Investigate the failed nodes (rate limiting,
   a node type without `contentRedirection`); note the fix.
2. **Did an API call 4xx/5xx?** Amazon may have changed an endpoint — re-derive
   from a headed browser and update `download-album.ts` + the steps above.
3. Only update this SKILL.md for real, reproduced changes.
