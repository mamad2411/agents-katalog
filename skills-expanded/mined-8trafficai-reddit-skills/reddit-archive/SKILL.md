---
name: reddit-archive
description: >
  Download and archive a Reddit post with everything attached to it — full text, the whole comment
  tree, images, galleries, and v.redd.it video with the audio actually merged back in. Use whenever
  someone wants to save, download, archive, back up, or scrape a Reddit post or thread; download a
  Reddit video or gallery; capture a thread before it is deleted; or build a dataset from Reddit
  content. Also use when a downloaded Reddit video has no sound, which is the usual symptom of
  taking `fallback_url` instead of merging the DASH streams, or when a gallery download returns
  403. Produces a self-contained directory with a manifest, so the capture is reproducible and
  auditable. Not for posting to Reddit.
---

# Archiving a Reddit post with its media

Reddit stores a post's media in four different shapes, and a naive download gets three of them
wrong. This skill handles all four, verified against live posts of each type.

```bash
node scripts/rdtx.mjs archive <permalink> --out ./archive --comments 200
```

## Verify the installed runtime without Reddit

Run `node scripts/verify-synthetic.mjs` with no arguments. It uses fabricated local fixtures to
exercise production media planning—including galleries, video audio metadata, and crosspost-parent
resolution—plus the shared runtime contracts. It makes no Reddit request or download and removes
its temporary state. A pass proves installation and planning behavior only; it does not prove a
live post can be fetched or that media bytes can be downloaded.
Overall `passed` is the AND of all five shared checks; inspect `functional.reddit_archive` for this
skill's evidence.

An independent tester can submit the exact named verifier result through the
[structured installed-run report](https://github.com/L4A-ai/reddit-skills/issues/new?template=reddit-skill-installed-run.yml).
Select the `reddit-archive` zero-input synthetic option only after running the installed copy. This
proves installation and media-planning contracts, not a live fetch or downloaded media bytes.

## What you get

```
archive/aww_1varxvd/
├── post.json        raw API response, unmodified
├── post.md          readable: title, author, age in years, body, nested comments
├── comments.json    the full tree
├── media/           image.jpeg | gallery_01..NN.jpeg | video.mp4
└── manifest.json    files, sizes, sha256 prefixes, source URLs, media_kind
```

`post.md` reports the post's **age in years**, which is what you want when hunting for old threads.
`manifest.json` makes the capture reproducible — it records where every byte came from.

## The four media shapes, and the trap in each

| type | where the URL lives | the trap |
|---|---|---|
| image | `url` (`i.redd.it/…`) | none — public, no cookies needed |
| gallery | `media_metadata[id].s.u` | the signed `s=` param must be passed **whole**; truncating it returns 403 |
| **video** | `secure_media.reddit_video` | `fallback_url` is **video-only** — taking it silently gives you a clip with no sound |
| crosspost | `crosspost_parent_list[0]` | the crosspost itself carries no media; you must follow to the parent |

**The video case is the one that bites.** Reddit serves v.redd.it as DASH with separate video and
audio streams. `archive` runs `yt-dlp` against the permalink and lets ffmpeg merge them, producing
a real `h264 + aac` file. Verified with `ffprobe`:

```
stream: video  (h264)
stream: audio  (aac)
```

yt-dlp also refuses Reddit without credentials ("Account authentication is required"), and reading
Chrome's cookie database fails while Chrome holds it open. `archive` exports a Netscape
`cookies.txt` from the live browser session instead, which works regardless of locks or keychain.

## Requirements

- `node` ≥ 18 and [`agent-browser`](https://github.com/vercel-labs/agent-browser)
- `yt-dlp` and `ffmpeg` — needed only for video; images and galleries work without them
- a logged-in Chrome session: `rdtx launch` → `rdtx login` → `rdtx doctor`

## Options

| flag | effect |
|---|---|
| `--out <dir>` | archive root (default `./archive`) |
| `--comments <n>` | how many comments to fetch (default 200) |
| `--no-media` | metadata and text only |

## Verifying a capture

`manifest.json` records `media_kind` and a per-file result. A partial capture is visible rather
than silent:

```json
{ "media_kind": "gallery", "comments_captured": 41,
  "media": [{ "type": "gallery", "file": "media/gallery_01.jpeg", "bytes": 231460, "ok": true }],
  "crossposted_from": null }
```

If `ok` is false on any entry, that file did not download — the manifest tells you which and why
instead of leaving a gap you discover later.

## Scope and courtesy

This archives **public** posts through your own logged-in session, at human pace (a jittered wait
between requests). It is not a bulk scraper and deliberately has no crawl mode: fetching whole
subreddits is what gets IPs and accounts blocked, and Reddit's terms cover bulk collection. For
large-scale historical data, use Reddit's own data API or an existing archive dump rather than
driving a browser at it.

## Related

- `reddit-post` — write posts and comments
- `reddit-seo` — check whether a post is indexable
