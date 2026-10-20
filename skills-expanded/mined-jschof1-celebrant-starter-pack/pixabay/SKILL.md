---
name: pixabay
description: Use Pixabay to search and download royalty-free images or videos. Trigger this whenever the user asks for stock photos, royalty-free images, free images of something, "grab some pics of X", "find me a photo of Y", "need an image of Z", wants Pixabay-sourced imagery, or asks to search/download from Pixabay — even if they don't name the site. Use it for videos too: "find a stock video of waves", "get a clip of X from Pixabay", "need B-roll of Y". Prefer this skill over hand-rolling a curl request to pixabay.com/api/ — it handles the API key, safe defaults, file naming, and output folder. Do NOT use it for AI-generated imagery (use gpt-image-2-webp or seo-image-gen) or for already-sourced client assets.
---

# pixabay

Search Pixabay's royalty-free library and auto-download the top results to disk so the agent (or Jack) can use them right away. Reads `PIXABAY_API_KEY` from `~/.env` (sourced automatically by the wrapper script).

## When to use

Reach for this skill whenever a task wants **stock, royalty-free, real-world** imagery or video:

- "Get me 5 photos of mountains for the site hero."
- "Find a stock video of ocean waves for the homepage."
- "Need some royalty-free pictures of weddings for a celebrant page."
- "Pull a clip from Pixabay of someone pouring coffee."
- "Search Pixabay for background images of London."

Don't reach for it when the user wants AI-generated imagery (use `gpt-image-2-webp` or `seo-image-gen`), when they have their own client assets, or when the brief specifically excludes stock libraries.

## How it works (one-shot)

The skill is exposed as a single CLI: `pixabay "<query>" [--flags...]`.

It does three things in one invocation:
1. Hits the Pixabay `/api/` (images) or `/api/videos/` (videos) endpoint with safe defaults.
2. Downloads the top N results into a query-specific folder.
3. Prints a JSON line to **stdout** describing every file (local path, source URL, tags, dimensions, attribution) and a human-readable summary to **stderr**.

That's it — no multi-step prompts, no candidate review. The user said "get some images", they get images.

## Default invocation

```bash
pixabay "mountain sunset" --count 5
```

This writes to `<cwd>/assets/pixabay-images/mountain-sunset/` with tag-based filenames like `mountain-sunset-sky-clouds.jpg`. Five files, safesearch on, photo type, all orientations, popular order.

## Output location

Priority order:
1. `--output-dir <path>` if given (full override).
2. `./assets/` if it exists in CWD (most common for project work — Fiona, a celebrant repo, etc.).
3. CWD as a last resort.

Within that base, files land in:
- `assets/pixabay-images/<query-slug>/` for images
- `assets/pixabay-videos/<query-slug>/` for videos

Filenames come from the result's tags (slugified, max 3 words) and get `-01`, `-02` suffixes on collision. So running the same query twice doesn't overwrite.

## Reading the JSON

The stdout JSON is one line per invocation. The shape:

```json
{
  "ok": true,
  "query": "mountain sunset",
  "type": "images",
  "requested": 5,
  "downloaded_count": 5,
  "total": 80037,
  "total_hits": 500,
  "output_dir": "/path/to/assets/pixabay-images/mountain-sunset",
  "downloaded": [
    {
      "id": 862870,
      "type": "image",
      "tags": "mountains, snow, sunset, dusk, twilight, peak, summit, ...",
      "local_path": "/path/to/assets/pixabay-images/mountain-sunset/mountains-snow-sunset.jpg",
      "source_url": "https://pixabay.com/get/g..._1280.jpg",
      "preview_url": "https://cdn.pixabay.com/.../_150.jpg",
      "page_url": "https://pixabay.com/photos/mountains-snow-sunset-dusk-862870/",
      "width": 6000,
      "height": 3376,
      "size_bytes": 201453,
      "user": "klausdie"
    }
  ],
  "pixabay_attribution": "Images and videos via Pixabay (https://pixabay.com)."
}
```

The `local_path` is what to use for downstream work (embed in HTML, copy into a site build, pass to another tool). The `page_url` is the Pixabay credit URL — link to it where the image appears per their license.

`ok: false` with `reason: "no_results"` is a clean no-hit. Treat that as "try a different query" rather than an error.

## Common flags

| Flag | Default | Notes |
| --- | --- | --- |
| `--count N` | 5 | 3–200 (Pixabay API limit). |
| `--type {images,videos}` | images | |
| `--orientation {all,horizontal,vertical}` | all | images only |
| `--image-type {all,photo,illustration,vector}` | photo | images only |
| `--category <name>` | none | backgrounds, nature, business, etc. |
| `--color red,blue` | none | images only, comma list |
| `--min-width N` / `--min-height N` | 0 | quality floor |
| `--order {popular,latest}` | popular | |
| `--video-size {tiny,small,medium,large}` | medium | videos only |
| `--video-type {all,film,animation}` | all | videos only |
| `--no-safesearch` | off | safesearch on by default |
| `--editors-choice` | off | filter to Pixabay editor picks |
| `--output-dir <path>` | auto | see Output location above |
| `--lang <iso-639-1>` | en | |
| `--page N` | 1 | for paginated fetches |
| `--check` | — | verify CLI + API key, exit |

## Practical recipes

Hero image for a project site:

```bash
pixabay "english countryside" --count 3 --orientation horizontal --min-width 1920
```

Celebrant background:

```bash
pixabay "wedding ceremony candles" --count 4 --category backgrounds
```

Stock B-roll for a video reel:

```bash
pixabay "drone aerial coastline" --type videos --count 2 --video-size medium
```

Stricter safety + smaller files:

```bash
pixabay "office team" --count 5 --image-type photo --orientation horizontal --min-width 1280
```

## Verification before reporting done

After running the CLI, **always confirm files actually landed on disk** before reporting success to the user. The stdout JSON claims a `downloaded_count`, but trust but verify:

```bash
test -d "<output_dir from JSON>"
ls "<output_dir from JSON>"
```

If `downloaded_count` is 0 or the path doesn't exist, the search returned no usable results. Try a broader query (drop `--image-type photo` → `all`, drop `--orientation`, broaden the wording) before giving up.

## Pitfalls

- **Per-page minimum is 3.** Pixabay rejects `--count 1` and `--count 2` with HTTP 400. The CLI guards against this; use 3+.
- **Videos can be huge.** A single medium-rendition `ocean waves` clip is 77 MB. Three at that size is 200 MB+ on disk. Mention this to the user if they ask for many videos, or drop to `--video-size small` (~1–3 MB).
- **Hotlinking is forbidden.** Don't use the `source_url` from the JSON directly in `<img src>` on a live site. Always copy the file to your own assets first — which is exactly what this CLI does.
- **Attribution.** Pixabay's free license requires a visible credit where the image appears (a link back to the `page_url` is the standard form). When you embed these in a website, include that link in the caption or footer.
- **Rate limit.** 100 requests per 60 s. The skill sleeps briefly between downloads to stay polite; don't loop it thousands of times.
- **Cache-bust the API key.** If `PIXABAY_API_KEY` ever rotates, just update `~/.env`. The wrapper re-sources it on every invocation.
- **Empty `assets/` folder.** If you create `assets/` mid-session, the next invocation will use it. If `assets/` is removed, the skill falls back to CWD without warning — be explicit with `--output-dir` if that's risky.

## If the CLI is broken

```bash
command -v pixabay       # should print /Users/jack/.local/bin/pixabay
pixabay --check          # should print "PIXABAY_API_KEY is set"
```

Repair the symlink:

```bash
ln -sf /Users/jack/.agents/skills/pixabay/scripts/pixabay /Users/jack/.local/bin/pixabay
```

Re-run `--check`. If the API key check fails:

```bash
secret PIXABAY_API_KEY   # confirm the key exists in ~/.env
```

## Reference

The full Pixabay API docs (parameters, response shape) are at https://pixabay.com/api/docs/ — the script mirrors those parameters 1:1, so anything in the docs is also a flag on this CLI.