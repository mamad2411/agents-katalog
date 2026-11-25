---
name: storyclaw-autoposter
description: "Supports publishing, scheduling, querying, managing, and analyzing posts across 13 social platforms via StoryClaw. Use when the user wants to post to TikTok, Instagram, Facebook, X/Twitter, YouTube, LinkedIn, Threads, Pinterest, Reddit, Bluesky, Telegram, Snapchat, or Google Business Profile. Use cases: (1) Publish or schedule a post with optional media, (2) Query post history or view post details, (3) View post or account analytics (likes, views, followers, reach), (4) Delete a post. Triggers: 帮我发帖, 自动发帖, 定时发帖, 查看帖子, 帖子数据, 观看量, 粉丝数, 账号分析, post to social media, schedule post, social media analytics."
version: "1.0.0"
license: MIT
author: storyclaw-official
homepage: https://storyclaw.com
repository: https://github.com/storyclaw-official/skills
requires:
  bins: [python3]
  env: [STORYCLAW_API_KEY]
  pip: [requests]
metadata:
  {
    "openclaw": {
      "emoji": "📱",
      "requires": {
        "bins": ["python3"],
        "env": ["STORYCLAW_API_KEY"],
        "pip": ["requests"]
      },
      "primaryEnv": "STORYCLAW_API_KEY",
      "installSpec": {
        "bins": ["python3"],
        "env": ["STORYCLAW_API_KEY"],
        "pip": ["requests"]
      }
    }
  }
---

# StoryClaw Auto-Post Skill

Supports full social media post management and analytics across 13 platforms.

**Supported Platforms:** TikTok, Instagram, Facebook, X/Twitter, YouTube, LinkedIn, Threads, Pinterest, Reddit, Bluesky, Telegram, Snapchat, Google Business Profile

**API Endpoint:** `POST https://aipuejhjwmabtobjrqdz.supabase.co/functions/v1/storyclaw-api`

---

## Phase 1: API Key Check & Account Binding Confirmation

### Step 1: Check API Key

First, check if `STORYCLAW_API_KEY` is available in the environment variable.

- **Available** → Use it directly, proceed to Step 2
- **Not available** → Ask the user:
  > "To get started, I need your StoryClaw API Key. Please go to **https://storyclaw.com/profile** → **StoryClaw API Key**, copy it and paste it here."

Once the key is obtained (from env or user input), call `get_social_status` to verify:

```json
{ "storyclaw_api_key": "<STORYCLAW_API_KEY>", "action": "get_social_status" }
```

- 401 Invalid API key → Tell the user:
  > "Your API Key appears to be invalid. Please go to **https://storyclaw.com/profile** → **StoryClaw API Key** to check and recopy it."
- Success → Record connected platforms, proceed to Step 2

### Step 2: Confirm Social Account Binding

Show the user their connected platforms returned by `get_social_status`.

If no platforms are connected, or the user asks how to link social accounts, guide them:
> "Please go to **https://storyclaw.com/profile** → **Social Account Binding**, and follow the instructions to link your TikTok, Instagram, or other accounts. Come back once done."

If at least one platform is connected → proceed to Phase 2.

**Only connected platforms appear as options throughout all operations.**

---

## Phase 2: Select Feature

Ask what the user needs:

| Feature | Description |
|---------|-------------|
| 📝 Publish Post | Publish immediately or schedule |
| 🔍 Query Post List | View post history for a platform |
| 📄 View Post Details | View full details of a specific post |
| 📊 Post Analytics | Likes, views, comments, shares, reach |
| 👥 Account Analytics | Followers, following, impressions |
| 🗑️ Delete Post | Delete a specific post |

---

## Feature 1: Publish Post

### Collect Content
Ask what the user wants to post. If they provide a draft or idea, enter the content optimization flow.

### Content Optimization (if needed)
Ask preferences:
- **Platform style**: Adapt per platform (TikTok: energetic short sentences, LinkedIn: professional, X: concise, etc.)
- **Tone**: Professional / Casual & Humorous / Inspirational / Educational
- **Hashtags**: Yes / No / Auto-recommend
- **Language**: Chinese / English / Other

Show optimized content for user confirmation before proceeding.

### Select Platforms
Show only connected platforms from `get_social_status` (multi-select):

```
Your connected platforms:
- TikTok ✅
- Instagram ✅
- Facebook ✅
...
Which platforms would you like to post to?
```

**Restriction:** If no video content → remove TikTok from options:
> "TikTok requires video content. Since no video is included, TikTok has been removed from the options."

### Media Attachments (Optional)
Ask if the user has images or videos to attach. `publish_post` only accepts HTTPS URLs — no local files.

**If user has a local file → must upload first:**

```bash
curl -X POST https://aipuejhjwmabtobjrqdz.supabase.co/functions/v1/storyclaw-api \
  -F "action=upload_file" \
  -F "storyclaw_api_key=<key>" \
  -F "file=@/path/to/photo.jpg" \
  -F "folder=my-media"
```

Upload returns an S3 HTTPS URL → use as `mediaUrls`.

**Flow:** Local file → `upload_file` → S3 URL → `mediaUrls` → `publish_post`

### ⚠️ Pre-Post Media Validation (MANDATORY)

Before calling the API, check every target platform against the limits below:

| Check | Detail |
|-------|--------|
| File format | Must be in platform's supported list |
| File size | Must not exceed platform max |
| Video duration | Must be within min/max range |
| Resolution / aspect ratio | Must meet requirements |
| Media count | Must not exceed platform max per post |
| Video URL | Must end in known extension (.mp4/.mov) |
| Reddit + video | Reddit does NOT support video — block if selected |
| TikTok + PNG | TikTok does NOT support PNG — block if detected |
| HTTPS | All URLs must start with https:// |

**If any violation found → BLOCK and notify:**
> "⚠️ Cannot post: [Platform] requires [requirement], but your [media] [issue]. Please fix and retry."

Examples:
- "⚠️ Cannot post: TikTok does not support PNG images. Please convert to JPG or WebP."
- "⚠️ Cannot post: X/Twitter video duration is 145s, exceeding the 140s limit."
- "⚠️ Cannot post: Reddit does not support video. Please remove the video or deselect Reddit."
- "⚠️ Cannot post: Telegram image size is 8MB, exceeding the 5MB limit."

Files over 50MB → suggest using `scheduleDate` for async processing.

### Platform Media Limits Reference

**TikTok**
- Images: JPG/JPEG/WebP only (NO PNG), max 35 images; recommended 1080×1920
- Video: MP4/MOV/WebM, max 1GB, 3s–600s, resolution 360–4096px, 23–60 FPS, max 1 video

**Instagram**
- Images: JPG/GIF/PNG, max 8MB, width 320–1440px, ratio 4:5~1.91:1, max 10 images, 50 posts/day
- Video (Feed/Reels): MP4/MOV, max 300MB, 3s–15min, 23–60 FPS, max 1 video
- Stories video: max 100MB, 3–60s

**Facebook Pages**
- Images: JPEG/BMP/PNG/GIF/TIFF, max 10MB, max 2048×2048px, max 10 images
- Video: max 2GB, max 1 video

**LinkedIn**
- Images: JPG/GIF/PNG, max 5MB, recommended 1200×627px, max 9 images, 150 posts/day
- Documents: PPT/PPTX/DOC/DOCX/PDF, max 100MB, max 300 pages
- Video: MP4, max 500MB, 3s–30min, ratio 1:2.4~2.4:1, max 1 video

**X / Twitter**
- Images: JPG/PNG/GIF/WebP, max 5MB, max 4 images
- Video: MP4/MOV, max 1280×1024px, 0.5s–140s (longVideo for 10+ min), ≤60FPS, ratio 1:3~3:1, audio mono/stereo, max 4 videos; avoid Dropbox/S3 signed URLs

**Bluesky**
- Images: JPG/GIF/PNG, max 1MB, max 4 images; animated GIF → treated as 1 video
- Video: MP4, max 1GB, 1s–3min, ratio 1:3~3:1, max 1 video

**Pinterest**
- Images: BMP/JPEG/PNG/TIFF/GIF/WebP, max 20MB, recommended 1000×1500 (2:3), max 1 image (carousel up to 5, same size)
- Video: MP4/MOV/M4V, max 1GB, 4s–15min, max 1 video

**Reddit**
- Images: JPG/PNG/GIF/WebP, max 10MB, max 1 image
- Video: ❌ NOT SUPPORTED

**Snapchat**
- Story/Spotlight images: JPEG/PNG, max 20MB, recommended 1080×1920
- Story/Spotlight video: MP4, max 500MB, 5–60s, recommended 540×960, 9:16, max 1 video

**Telegram**
- Images: JPG/PNG/GIF/WebP, max 5MB, width+height ≤10,000, ratio ≤20:1, max 1 image; text ≤1,024 chars
- Video: max 20MB, text ≤1,024 chars, max 1 video

**Threads**
- Up to 20 images/videos mixed; video URL must end in known extension or use isVideo param
- ⚠️ Threads does not support post deletion via API (must delete manually in app)

**YouTube**
- Video: MP4/MOV, max 4GB, recommended 16:9, H.264+AAC, frame rates: 24/25/30/48/50/60 FPS, max 1 video

**Google Business Profile**
- Images: max 1 image

**Universal Rules**
- All media URLs must start with https://
- Video URLs must end in a known extension (.mp4, .mov); otherwise add `isVideo: true`
- Files >50MB: use `scheduleDate` for async processing
- Max 1 video per post per platform (except X which supports 4)

### Schedule Settings
Ask: publish now or schedule? If scheduling, suggest optimal times:

| Platform | Recommended Times |
|----------|-------------------|
| TikTok | Weekdays 7–9am, 12–3pm, 7–9pm |
| Instagram | Tue–Fri 9–11am, 1–3pm |
| Facebook | Wed 11am–1pm, Thu 1–3pm |
| LinkedIn | Tue–Thu 8–10am, 12pm |
| X/Twitter | Mon–Fri 8am, 12pm, 5pm |
| YouTube | Fri–Sun 2–4pm |

Offer 2–3 specific options. User makes final decision. Convert to ISO 8601.

### Final Confirmation

**Must show full summary and wait for explicit confirmation before calling API:**

```
📋 Post Confirmation
─────────────────
Content: [final content]
Platforms: [selected platforms]
Media: [yes/no]
Post time: [now / specific time]
─────────────────
Confirm posting?
```

Call `publish_post` after confirmation:

```json
{
  "storyclaw_api_key": "<key>",
  "action": "publish_post",
  "post": "<content>",
  "platforms": ["tiktok", "instagram"],
  "mediaUrls": ["<url>"],
  "scheduleDate": "<ISO8601, omit for immediate>"
}
```

---

## Feature 2: Query Post List

Ask which platform (from connected list):

```json
{ "storyclaw_api_key": "<key>", "action": "get_posts", "platform": "<platform>" }
```

Display results:
```
📋 [Platform] Post List:
1. "[content first 40 chars...]" — 2025-01-10
2. "[content first 40 chars...]" — 2025-01-08
```

---

## Feature 3: View Post Details

If user doesn't know post_id, show list from `get_posts` first.

```json
{ "storyclaw_api_key": "<key>", "action": "get_post", "post_id": "<post_id>" }
```

---

## Feature 4: Post Analytics

**Method A — StoryClaw Post ID:**
```json
{ "storyclaw_api_key": "<key>", "action": "get_analytics_post", "post_id": "<id>", "platforms": ["tiktok"] }
```

**Method B — Platform native ID:**
```json
{ "storyclaw_api_key": "<key>", "action": "get_analytics_post_by_social_id", "social_post_id": "<id>", "platforms": ["instagram"] }
```

Display grouped by platform with likes, views, comments, shares, impressions, reach.

---

## Feature 5: Account Analytics

```json
{ "storyclaw_api_key": "<key>", "action": "get_analytics_social", "platforms": ["instagram", "tiktok"] }
```

Display followers, following, post count, impressions per platform.

---

## Feature 6: Delete Post

Show post list first. After user selects, confirm:
```
⚠️ Confirm deletion?
"[post content first 40 chars]" will be permanently deleted from all platforms.
Reply "confirm delete" to proceed.
```

```json
{ "storyclaw_api_key": "<key>", "action": "delete_post", "post_id": "<post_id>" }
```

---

## Error Handling

| Error | Message |
|-------|---------|
| 401 Invalid API key | "API Key is invalid. Please copy it again from your profile." |
| 400 No social profile | "No social account linked. Please link one at StoryClaw.com." |
| 500 Internal server error | "Service temporarily unavailable. Please try again later." |

---

## Key Rules

- **Never call publish or delete APIs without explicit user confirmation**
- Mask API Key in display (`sk_****...`)
- Always base platform options on live `get_social_status` response
- User can go back and change any setting at any time
