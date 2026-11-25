---
name: image-search
description: Search a local or uploaded image with Google Lens, inspect visual matches, and extract ordered unique result URLs. Use for reverse image search, search by image, Google Lens, or top-N URLs from an image.

Before the first step that uses the built-in browser or browser pane, read built-in-browser.
Before the first step that uses Chrome extension, read chrome-browser.
Before the first step that uses computer use, read computer-use.
Before the first step that uses docs, read docs.
compatibility: Linux with Chromium, Python 3, Playwright, and BeautifulSoup installed.
allowed-tools: bash read write browser
metadata:
  hermes:
    tags: [image, reverse-search, google-lens, visual-search, urls]
---

# Image Search

Use this skill for image-based web search. Do not claim that a result is an exact match unless Google Lens labels it as such; distinguish visual matches, similar content, and ordinary web results.

## Local image workflow

For a local image, run the helper from this skill directory:

```bash
python3 ~/.hermes/skills/image-search/scripts/google_lens_search.py \
  /absolute/path/to/image.jpeg \
  --limit 20 \
  --lang zh-TW \
  --output-dir /tmp/image-search
```

The command:

1. Opens Google Lens through Chromium.
2. Clicks Google's semantic “Search by image” control.
3. Uploads the local image without copying it to a public host.
4. Waits for the rendered result page.
5. Extracts ordered, unique external URLs and writes `results.json`, `urls.txt`, and `search-url.txt`.

Read `results.json` and `urls.txt` after completion. Return the requested number of URLs in the user's language, preserving their order. Include titles when useful, but do not invent titles or URLs. The result page may contain fewer than the requested number of visual matches; state that clearly instead of silently padding the list with unrelated web results.

## Browser-first interaction

When the user asks only to open/search the image, use the `browser` tool and leave Google Lens open:

1. `open https://lens.google.com/`.
2. Run `snapshot -i` before using any `@ref`.
3. If Lens shows a marketing page on mobile, open `https://www.google.com/?olud`, use the visible semantic `Search by image` / `以圖搜尋` control, then `upload` the image file.
4. Inspect the loaded result page with `get text` or a screenshot.

For bulk URL extraction, prefer the helper because the browser tool exposes only a subset of anchors in its interactive snapshot. The helper uses a desktop-like Chromium context because the mobile Lens landing page can redirect to the app promotion instead of exposing a web upload control.

## Verification and failure handling

- Verify the input path exists before starting.
- Treat Google `/sorry/` pages as anti-bot verification, not as an empty result. Rerun with `--headed` and complete verification manually if appropriate:

```bash
python3 ~/.hermes/skills/image-search/scripts/google_lens_search.py \
  /absolute/path/to/image.jpeg --headed --limit 20
```

- Deduplicate URLs while preserving first-seen order.
- Exclude Google navigation and redirect URLs; unwrap Google redirect links to their direct destination.
- Never expose cookies, session identifiers, or the full Lens query URL unless the user asks for it.
- If Lens returns no matches, report that explicitly and do not infer a source from the image.

## Tests

The parser tests use the Python standard library and need no network access:

```bash
python3 -m unittest discover \
  -s ~/.hermes/skills/image-search/tests \
  -p 'test_*.py' -v
```
