---
name: x-post
description: >
  Publish content, images, videos, quote tweets, long-form Markdown articles,
  and translated video workflows to X (Twitter) using real Chrome via Chrome
  DevTools Protocol (CDP) to bypass bot detection. Use when the user asks to
  post a tweet, publish an update to X, attach images or videos to a tweet,
  quote-tweet a link, publish a Markdown article to X Articles, or translate
  and republish a video with subtitles — even if they don't explicitly say
  "x-post" or "Twitter automation". Do NOT use for scraping tweets, reading
  feeds, or managing account settings.
---

# X Post

Automated, anti-bot-resilient publishing toolchain for X (Twitter) leveraging real Chrome instances controlled via Chrome DevTools Protocol (CDP).

## Runtime Requirements (Pre-flight)

Before executing any script, verify environment dependencies → **`references/runtime-setup.md`**.

**Essential Checklist:**
- [ ] Bun runtime installed (`bun --version`)
- [ ] Google Chrome or Chromium installed (or `X_BROWSER_CHROME_PATH` set)
- [ ] First-time run: authenticate into X in the opened Chrome window (session saved to `~/.local/share/x-browser-profile`)
- [ ] For video translation: `yt-dlp`, `ffmpeg`, and `whisper-cli` installed

**If any required tool is missing, stop and inform the user immediately.**

---

## Capabilities & Navigation Map

Choose the workflow appropriate for the publishing task:

| Content Type | Script Path | Details & Reference |
|---|---|---|
| **Text & Images** | `scripts/x-browser.ts` | Single/multi-image posts & thread chains → `references/regular-posts.md` |
| **Video Posts** | `scripts/x-video.ts` | Video uploads with transcode monitoring → `references/video-posts.md` |
| **Quote Tweets** | `scripts/x-quote.ts` | Quote existing tweets with commentary → `references/quote-tweets.md` |
| **Long-Form Articles** | `scripts/x-article.ts` | Markdown articles with inline images → `references/articles.md` |
| **Video Translation** | `scripts/x-translate-video.ts` | Subtitle extraction, translation & burning → `references/video-translation.md` |
| **Universal Distribution** | `bin/x-post.js` | Claude, Marketplace, npx, Skills.sh & all agents → `references/distribution.md` |
| **Troubleshooting** | N/A | Solutions for common errors → `references/troubleshooting.md` |

---

## 1. Regular Posts (Text, Images & Threads)

Publish standard tweets with up to 4 images and thread replies.

```bash
# Preview mode (verifies compose box and keeps window open for 30s)
bun scripts/x-browser.ts "Exploring agentic automation with Antigravity!" --image ./screenshot.png

# Publish with images and thread reply
bun scripts/x-browser.ts "Announcing our new open-source release!" \
  --image ./banner.png \
  --reply "Check out the repo here: https://github.com/org/repo" \
  --submit
```

- Details, image specs, and multi-thread chaining → **`references/regular-posts.md`**

---

## 2. Video Posts

Publish videos (MP4, MOV, WebM) with automatic upload and transcode polling.

```bash
# Preview video upload
bun scripts/x-video.ts --video ./demo.mp4 "Watch the complete architecture walkthrough"

# Publish video with source citation in reply thread
bun scripts/x-video.ts --video ./demo.mp4 \
  "Autonomous coding loop benchmark" \
  --reply "Benchmarked on SWE-bench verified dataset." \
  --submit
```

- Duration limits, formats, and upload states → **`references/video-posts.md`**

---

## 3. Quote Tweets

Quote an existing public tweet with custom commentary while preserving source attribution.

```bash
# Preview quote tweet
bun scripts/x-quote.ts https://x.com/username/status/1234567890 "Important perspective on LLM agents!"

# Publish quote tweet directly
bun scripts/x-quote.ts https://x.com/username/status/1234567890 "Strongly agree with this analysis." --submit
```

- URL normalization and menu selectors → **`references/quote-tweets.md`**

---

## 4. Long-Form X Articles (Markdown)

Convert Markdown documents with headings, lists, blockquotes, cover images, and inline images into X Articles (requires X Premium).

```bash
# Preview formatted article draft
bun scripts/x-article.ts ./article.md --cover ./cover.png

# Publish article directly
bun scripts/x-article.ts ./article.md --submit
```

- Frontmatter syntax and image placeholder mechanics → **`references/articles.md`**

---

## 5. Video Translation & Subtitle Workflow

Download foreign-language video tweets, transcribe audio via Whisper, generate editable translation files, burn styled subtitles, and publish with source attribution.

```bash
# Step 1: Ingest URL and create translation draft (/tmp/x-translate/<id>/translation.md)
bun scripts/x-translate-video.ts https://x.com/username/status/1234567890 --target-lang English

# Step 2: Edit /tmp/x-translate/<id>/translation.md with translated copy & SRT

# Step 3: Burn subtitles and preview
bun scripts/x-translate-video.ts --confirm /tmp/x-translate/<id>/translation.md

# Step 4: Burn subtitles and publish
bun scripts/x-translate-video.ts --confirm /tmp/x-translate/<id>/translation.md --submit
```

- Full pipeline and FFmpeg subtitle styling → **`references/video-translation.md`**

---

## Execution Principles & Safety

1. **Always Preview First**: Run commands without `--submit` during development or manual review.
2. **Persistent Profile**: All scripts share `~/.local/share/x-browser-profile` so authentication is required only once.
3. **Native Keystroke Dispatch**: Media assets use hardware-level paste simulation (`copy-to-clipboard.ts` + `paste-from-clipboard.ts`) to avoid CDP synthetic event blocks.
4. **Issue Resolution**: For login timeouts, clipboard permissions, or CDP connection errors → **`references/troubleshooting.md`**.
