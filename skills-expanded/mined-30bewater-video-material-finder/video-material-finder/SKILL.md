---
name: video-material-finder
description: Find a specific online video from text, screenshots, clips, quotes, or other clues, or discover reusable stock footage with verified source pages, resolution, licensing, attribution, and direct download links. Use when users ask to 找视频、找原视频、全网搜视频、找高清视频、找 4K 素材、找免版权视频素材、查视频出处、根据截图或片段反查视频、compare footage sources, or download clearly licensed/public-domain footage. Supports zero-key public catalogs plus optional Brave, Pexels, and Pixabay APIs. Never use it to bypass DRM, paywalls, authentication, or copyright restrictions.
---

# Video Material Finder

Find videos by evidence, not by guesswork. Default to Chinese interaction; switch to English when the user writes in English or requests it.

## Choose the workflow

- Use **Specific video** when the user wants a known work, upload, music video, interview, scene, original source, or higher-resolution copy.
- Use **Reusable footage** when the user wants stock footage, B-roll, public-domain media, Creative Commons media, or material safe to download and edit.
- Run both workflows when the request is ambiguous, then label the two result groups separately.

Before searching, extract the strongest clues: exact title, people, lyrics or dialogue, creator, platform, approximate year, duration, visual landmarks, language, and desired resolution. Generate a compact original-language query and, when useful, one English or Chinese alternate query.

## Specific video workflow

1. Search authoritative or original sources first: creator/label/studio accounts, official archives, publisher pages, then reputable platform uploads.
2. Run `scripts/search_specific_video.py` for YouTube, Bilibili, and optional Brave Video Search. If platform-specific search tools already exist in the environment, use them as additional evidence.
3. If the user supplied a local clip they own or are authorized to analyze, inspect metadata and extract a few keyframes with FFmpeg. Do not upload private media to third-party reverse-search services without permission.
4. Compare title, creator, duration, upload date, frame content, audio clues, and resolution. Do not call a candidate a match from title similarity alone.
5. Return the best match, 2-4 alternatives, why each matches, maximum verified resolution, and a source page link.
6. A viewable video is not automatically downloadable. Offer a direct file only for user-owned, public-domain, or explicitly licensed material. Never bypass DRM, login, geographic restrictions, expiring authorization, or paid access.

Read `references/specific-video.md` when the evidence is incomplete, multiple copies disagree, or the user asks for downloading.

## Reusable footage workflow

1. Search with `scripts/search_stock_video.py`. Start with Wikimedia Commons; add NASA and Library of Congress for archival material. Enable Pexels/Pixabay when their API keys exist.
2. Prefer exact licensing metadata over site reputation. Keep the provider page together with every file URL.
3. Apply the status gate:
   - `reusable`: explicit compatible license or public-domain dedication; direct download may be offered.
   - `review`: rights vary, third-party credits may apply, or the catalog only provides a rights statement; show the link but require human review before publication.
   - `blocked`: all-rights-reserved, missing source, or incompatible/unknown license; do not present as downloadable stock.
4. Check format, dimensions, orientation, duration, file size, attribution, model/property/trademark restrictions, and commercial-use constraints.
5. Return a short ranked list. Include `source_page`, `direct_download`, resolution, license name/link, attribution, usage status, and restrictions.

Read `references/providers.md` for setup and API behavior, `references/licensing.md` before making reuse claims, and `references/output-format.md` for the response schema.

## Commands

Probe the local environment without exposing secrets:

```bash
python scripts/probe_sources.py
```

Search reusable footage with zero-key providers:

```bash
python scripts/search_stock_video.py "ocean waves" --providers commons,nasa,loc --limit 5 --format markdown
```

Add commercial stock APIs when configured:

```bash
python scripts/search_stock_video.py "城市夜景" --alt-query "city night aerial" --providers all --min-width 1920 --format markdown
```

Search for a specific video without downloading it:

```bash
python scripts/search_specific_video.py "Frank Ocean Endless visual album" --providers youtube,bilibili,brave --limit 5 --format markdown
```

API keys are optional environment variables: `BRAVE_SEARCH_API_KEY`, `PEXELS_API_KEY`, and `PIXABAY_API_KEY`. Never print or commit their values.

## Non-negotiable rules

- Distinguish `free to view`, `free to download`, `royalty-free`, Creative Commons, and public domain. They are not synonyms.
- Treat every direct file URL as coupled to its source page and license evidence.
- Do not scrape sites whose terms prohibit it; use documented APIs or manual links.
- Do not mass-download, mirror, or redistribute stock libraries.
- Do not claim legal certainty. State what the provider says and flag jurisdiction, people, logos, music, artworks, and property as separate rights.
- Ask before downloading a large file when size or destination is unclear.
- Prefer stable provider pages over temporary CDN links in long-lived reports.
