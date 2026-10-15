---
name: x2c-socialposter
description: "Social media publishing and engagement management via X2C Open API. Use when the user needs to publish posts to social media, check linked accounts, manage comments, or upload media. Use cases: (1) Publish text/media posts to TikTok, Instagram, Facebook, YouTube, LinkedIn, Twitter, etc. (2) Schedule posts for future publishing. (3) Manage comments and replies on posts. (4) Upload media files (up to 5GB) and get CDN links. (5) View post history and linked account status. Triggers: post to social media, publish post, social media, schedule post, social publish, upload media, social accounts, comment on post."
version: "0.1.0"
license: MIT
author: storyclaw-official
homepage: https://github.com/storyclaw-official/skills
repository: https://github.com/storyclaw-official/skills
requires:
  bins: [python3]
  env: [X2C_API_KEY]
  pip: [requests]
metadata:
  {
    "openclaw": {
      "emoji": "📱",
      "requires": {
        "bins": ["python3"],
        "env": ["X2C_API_KEY"],
        "pip": ["requests"]
      },
      "primaryEnv": "X2C_API_KEY",
      "installSpec": {
        "bins": ["python3"],
        "env": ["X2C_API_KEY"],
        "pip": ["requests"]
      }
    }
  }
---

[简体中文](./SKILL.zh-CN.md) | English

# X2C Social Poster

**Source**: [storyclaw-official/skills](https://github.com/storyclaw-official/skills) · Dashboard: [x2creel.ai](https://www.x2creel.ai/)

Publish posts, manage comments, and upload media to 13+ social platforms via X2C Open API. Features smart upload (auto-selects pre-signed URL for large files), per-platform validation, and one-step publish with local files.

---

## Installation Requirements

| Requirement | Value |
|-------------|-------|
| **Binary** | `python3` |
| **Environment** | `X2C_API_KEY` (required; obtain from [X2C Dashboard](https://www.x2creel.ai/)) |
| **Pip** | `requests` |

Set `X2C_API_KEY` before use. The script will prompt if not configured.

---

## First-Time Setup Guide

**When the user invokes this skill for the first time, follow these onboarding steps IN ORDER:**

### Step 0: Check API Key

```bash
python3 scripts/x2c_social.py --action check-key
```

- If the key is set → proceed to Step 1.
- If the key is NOT set → guide the user:

```
🔑 X2C API Key is not configured yet. Let's set it up:

1. Go to https://www.x2creel.ai/social-accounts and sign up / log in
2. Click "Link Account" to connect your social media accounts (TikTok, Instagram, etc.)
3. On the same page, scroll down to "Developer API Key" section and click "Get API Key"
4. Copy your X2C Open API Key and paste it here

Once you provide the key, I'll save it for you.
```

### Step 1: Verify Linked Accounts

```bash
python3 scripts/x2c_social.py --action status
```

Display the linked platforms. If none are linked:

```
⚠️ No social accounts linked yet.
Please visit https://www.x2creel.ai/social-accounts to link your accounts.
```

---

## Platform Requirements Quick Reference

**Before publishing, always check the target platform's requirements and guide the user accordingly.**

| Platform | ID | Media Required | Text Limit | Max Media | Supported Types | Key Constraints |
|----------|-----|:---:|---:|:---:|---|---|
| YouTube | `youtube` | ✅ (video) | title:100 desc:5,000 | 1 video | MP4, MOV, AVI, WMV | `--title` required (auto-gen if missing, max 100 chars). Default visibility = public. |
| Instagram | `instagram` | ✅ | 2,200 | 10 (carousel) | JPEG, PNG, MP4 | Must be Business/Creator. No text-only. Max 5 hashtags, 3 @mentions. |
| TikTok | `tiktok` | ✅ | 2,200 | 1 video or 35 images | MP4, JPG, JPEG, WEBP | Images & video can't mix. **No PNG**. No `\n` in text. AI content must mark `--ai-generated`. |
| X (Twitter) | `twitter` | ❌ | 280 | 4 images or 1 video | JPEG, PNG, GIF, MP4 | Images and videos can't mix. BYO API keys required. Use `longPost` for >280 chars. |
| Facebook | `facebook` | ❌ | 63,206 | 10+ | JPEG, PNG, MP4 | Must be a Page (not personal). |
| LinkedIn | `linkedin` | ❌ | 3,000 | 9 | JPEG, PNG, GIF, MP4 | Personal or Company page. |
| Pinterest | `pinterest` | ✅ | 500 | 5 (carousel) | JPEG, PNG | Image required. Video requires `--thumbnail`. |
| Reddit | `reddit` | ❌ | title:300 post:40,000 | 1 | JPEG, PNG, GIF, MP4 | `--title` required. `--subreddit` required. |
| GMB | `gmb` | ❌ | 1,500 | 1 | JPEG, PNG, MP4 | Verified business. No phone numbers in text. |
| Bluesky | `bluesky` | ❌ | 300 | 4 | JPEG, PNG, MP4 | 300 chars including links. |
| Threads | `threads` | ❌ | 500 | 10 (carousel) | JPEG, PNG, MP4 | Linked to Instagram account. |
| Snapchat | `snapchat` | ✅ | 160 | 1 | JPEG, PNG, MP4 | Exactly 1 media item. |
| Telegram | `telegram` | ❌ | 4,096 | 1 | JPEG, PNG, GIF, MP4 | Bot + Channel/Group. |

### ⚠️ Multi-Platform Posting Caveat

When posting to multiple platforms simultaneously, content guards apply sequentially — the **shortest character limit wins** and will truncate for all platforms. If you need different text per platform, make **separate publish calls**.

### Platform-Specific Parameters

When publishing to these platforms, the script **automatically validates and builds platform options**:

| Parameter | Platforms | Description |
|-----------|-----------|-------------|
| `--title` | YouTube, Reddit | Post/video title (required). YouTube auto-generates from post text if missing (max 100 chars). |
| `--subreddit` | Reddit | Target subreddit without `r/` (required) |
| `--visibility` | YouTube, TikTok | `public`/`unlisted`/`private` (YT), `PUBLIC_TO_EVERYONE`/`SELF_ONLY` etc. (TT) |
| `--thumbnail` | Pinterest | Thumbnail URL for video pins (required for video) |
| `--ai-generated` | TikTok | Mark content as AI-generated (recommended for AI content) |

---

## Media Upload

The script uses **smart upload** — automatically selects the best method based on file size:

| Method | File Size | Limit | How It Works |
|--------|-----------|-------|-------------|
| **Direct upload** | ≤ 50MB | ~50MB | One-step multipart upload |
| **Pre-signed URL** | > 50MB | **5GB** | Gets S3 pre-signed URL → PUT directly to S3 |

This is handled automatically — the user just provides a file path and the script picks the right method.

### Standalone Upload

```bash
# Small file → direct upload
python3 scripts/x2c_social.py --action upload --file /path/to/image.jpg

# Large file → auto pre-signed upload
python3 scripts/x2c_social.py --action upload --file /path/to/large_video.mp4 --folder videos
```

### One-Step Publish with Local Files

When publishing, local files are **auto-uploaded** before publishing — no separate upload step needed:

```bash
# 75MB video → auto pre-signed upload → publish
python3 scripts/x2c_social.py --action publish \
  --platforms tiktok instagram \
  --post "Check this out! 🎬" \
  --media-files /path/to/large_video.mp4
```

Output flow:
```json
{"status": "uploading", "file": "large_video.mp4", "size_mb": 75.2, "method": "presigned", "message": "..."}
{"status": "uploaded", "file": "large_video.mp4", "url": "https://v.arkfs.co/.../large_video.mp4", "method": "presigned"}
{"success": true, "data": {"id": "post_abc123", "postIds": [...]}}
```

---

## Commands

### 1. Check Linked Accounts

```bash
python3 scripts/x2c_social.py --action status
```

### 2. Publish Post

```bash
# Text-only (works for: twitter, facebook, linkedin, reddit, gmb, bluesky, threads, telegram)
python3 scripts/x2c_social.py --action publish \
  --platforms twitter facebook \
  --post "Hello world! 🚀"

# With local file — auto-uploaded (any size up to 5GB)
python3 scripts/x2c_social.py --action publish \
  --platforms tiktok instagram \
  --post "Watch this! 🎬" \
  --media-files /path/to/video.mp4

# With remote URL
python3 scripts/x2c_social.py --action publish \
  --platforms tiktok instagram \
  --post "Watch this! 🎬" \
  --media-urls "https://example.com/video.mp4"

# Mix local + remote
python3 scripts/x2c_social.py --action publish \
  --platforms facebook \
  --post "Double media! 🎬" \
  --media-files /local/video.mp4 \
  --media-urls "https://cdn.example.com/image.jpg"

# YouTube — title required
python3 scripts/x2c_social.py --action publish \
  --platforms youtube \
  --post "Video description here" \
  --title "My YouTube Video" \
  --visibility public \
  --media-files /path/to/video.mp4

# Reddit — title + subreddit required
python3 scripts/x2c_social.py --action publish \
  --platforms reddit \
  --post "Post body text" \
  --title "Discussion: AI in 2026" \
  --subreddit technology

# TikTok — mark AI content
python3 scripts/x2c_social.py --action publish \
  --platforms tiktok \
  --post "AI generated content" \
  --ai-generated \
  --media-files /path/to/ai_video.mp4

# Scheduled post
python3 scripts/x2c_social.py --action publish \
  --platforms tiktok instagram \
  --post "Coming soon! ⏰" \
  --media-files /path/to/video.mp4 \
  --schedule "2026-04-01T12:00:00Z"

# Shorten links
python3 scripts/x2c_social.py --action publish \
  --platforms twitter linkedin \
  --post "Read our blog: https://example.com/very-long-url" \
  --shorten-links
```

### 3. Get Post History

```bash
python3 scripts/x2c_social.py --action posts
python3 scripts/x2c_social.py --action posts --platform tiktok
```

### 4. Delete Post

```bash
python3 scripts/x2c_social.py --action delete-post --post-id post_abc123
python3 scripts/x2c_social.py --action delete-post --post-id post_abc123 --bulk
```

### 5. Post Comment

```bash
python3 scripts/x2c_social.py --action comment \
  --post-id post_abc123 --platforms tiktok --comment "Great! 🔥"
```

### 6. Get Comments

```bash
python3 scripts/x2c_social.py --action comments --post-id post_abc123 --platform tiktok
```

### 7. Reply to Comment

```bash
python3 scripts/x2c_social.py --action reply \
  --comment-id comment_xyz --platforms tiktok --comment "Thanks!"
```

### 8. Delete Comment

```bash
python3 scripts/x2c_social.py --action delete-comment --comment-id comment_xyz
```

### 9. Upload Media (standalone)

```bash
python3 scripts/x2c_social.py --action upload --file /path/to/file.mp4 --folder videos
```

---

## Parameter Reference

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--action` | ✅ | Action to perform |
| `--post` | for publish | Post text content |
| `--platforms` | for publish | Space-separated target platforms |
| `--platform` | for filtering | Single platform filter |
| `--media-urls` | ❌ | Remote URLs or local paths (auto-uploaded) |
| `--media-files` | ❌ | Local file paths to auto-upload and attach |
| `--schedule` | ❌ | ISO 8601 date for scheduled posting |
| `--shorten-links` | ❌ | Shorten URLs in post text |
| `--title` | YouTube, Reddit | Post/video title |
| `--subreddit` | Reddit | Target subreddit (without `r/`) |
| `--visibility` | YouTube, TikTok | Post visibility setting |
| `--thumbnail` | Pinterest | Video thumbnail URL |
| `--ai-generated` | TikTok | Mark as AI-generated content |
| `--post-id` | for post ops | Ayrshare post ID |
| `--comment-id` | for comment ops | Comment ID |
| `--comment` | for comment/reply | Comment or reply text |
| `--bulk` | ❌ | Delete from all platforms |
| `--file` | for upload | Local file path to upload |
| `--folder` | ❌ | Upload subfolder (default: `uploads`) |

---

## Interaction Guide

**When the user request is vague, guide per the steps below. If the user has provided enough info, run the command directly.**

### Step 1: Onboarding Check

Always run the First-Time Setup Guide first. Verify API key and linked accounts.

### Step 2: Determine Intent

```
What would you like to do?
Options:
  📝 Publish a post
  📊 View post history
  💬 Manage comments
  📤 Upload media
  🔗 Check linked accounts
```

### Step 3: For Publishing — Platform-Aware Guidance

1. **Ask which platforms** → show only linked platforms from `status` check.

2. **Check platform requirements** and proactively ask for required fields:
   - YouTube → ask for `--title` and `--visibility`
   - Reddit → ask for `--title` and `--subreddit`
   - Instagram/TikTok/Pinterest/Snapchat → remind media is required
   - TikTok with AI content → suggest `--ai-generated`

3. **Ask for post content** → check text length against platform limits.

4. **Ask about media** → accept local files or remote URLs. Local files auto-upload (any size).

5. **Ask about scheduling** → publish now or schedule for later.

### Step 4: Execute and Display

Run the command. The script will:
1. Auto-upload local files (smart method selection)
2. Validate against platform requirements
3. Build platform-specific options
4. Publish and return per-platform results

Display results clearly, highlighting any per-platform success/failure.

---

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| 400 | Missing/invalid parameters | Check platform requirements and fix |
| 401 | Invalid API key | Guide user to verify/reset key |
| 500 | Server error | Retry or inform user |

The script also performs **client-side validation** before calling the API:
- Text length per platform
- Media required check
- Required fields (title, subreddit)
- Media count limits (Snapchat = 1)

Fatal validation errors block the publish. Warnings are displayed but don't block.
