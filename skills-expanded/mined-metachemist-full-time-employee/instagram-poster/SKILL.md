---
name: instagram-poster
description: |
  Create and publish photo posts with captions to Instagram using the official
  Content Publishing API (no browser required). Use when asked to post on Instagram,
  or when processing an approved APPROVAL_SEND_INSTAGRAM_POST_*.md file from vault/Approved/.
  Always draft first and require human approval before posting.
  NOTE: Instagram requires a publicly accessible HTTPS image URL — local file paths are not supported by the API.
---

# Instagram Poster

Publish photo posts to Instagram using the official Content Publishing API (no Playwright required).

## When to Use

- Processing an `APPROVAL_SEND_INSTAGRAM_POST_*.md` file from `vault/Approved/`
- Creating a new post when explicitly instructed by the user

**Never post directly** — always route through `vault/Pending_Approval/` first.

## Important: Public HTTPS Image URL Required

The Instagram Content Publishing API does **not accept local file paths**. The image must be at a publicly accessible HTTPS URL (e.g., hosted on S3, Cloudflare Images, Imgur, or any CDN).

- Upload your image to a public host first
- Paste the URL into the approval file `Target:` field

## One-Time Setup

### 1. Requirements

- An **Instagram Business** or **Creator** account linked to a Facebook Page
- A Facebook Developer App with these permissions approved:
  - `pages_show_list` — to auto-derive the page access token
  - `pages_manage_posts` — for page token validity
  - `instagram_basic` — to look up the IG Business Account ID from the page
  - `instagram_content_publish` — to create and publish posts

### 2. Add credentials to `.env`

```
FACEBOOK_APP_ID=xxxxx
FACEBOOK_APP_SECRET=xxxxx
FACEBOOK_ACCESS_TOKEN=EAAxxxxx    # user token with instagram_content_publish scope
FACEBOOK_PAGE_ID=123456789        # your Facebook Page ID
```

The script **auto-detects** `INSTAGRAM_USER_ID` from your page on first run.

To pin it (faster, avoids one API call):
```
INSTAGRAM_USER_ID=123456789
INSTAGRAM_ACCESS_TOKEN=EAAxxxxx   # defaults to FACEBOOK_PAGE_ACCESS_TOKEN if absent
```

### 3. Find your Instagram User ID (optional)

```bash
curl "https://graph.facebook.com/v21.0/{PAGE_ID}?fields=instagram_business_account&access_token={TOKEN}"
# Returns: {"instagram_business_account": {"id": "YOUR_IG_USER_ID"}, ...}
```

## Approval File Format

```markdown
---
type: approval_request
action: send_instagram_post
status: approved
---

# What will happen after approval?

The following post will be published to Instagram.

# Payload

- **Target:** https://yourdomain.com/images/post.jpg

## Message / Content

  Your Instagram caption here (max 2,200 chars).

  #hashtag1 #hashtag2 #hashtag3
```

`Target:` = public HTTPS image URL
`## Message / Content` = caption text

Save to `vault/Approved/APPROVAL_SEND_INSTAGRAM_POST_<topic>_<YYYY-MM-DD>.md`

## Dry-Run Mode

```bash
python .claude/skills/instagram-poster/scripts/create_post.py \
  --caption "Caption text..." \
  --image-url "https://example.com/image.jpg" \
  --dry-run
```

Expected output:
```json
{"status": "dry_run", "caption_len": 42, "image_url": "https://...", "preview": "...", "timestamp": "..."}
```

## Live Post

```bash
python .claude/skills/instagram-poster/scripts/create_post.py \
  --caption "Caption text..." \
  --image-url "https://example.com/image.jpg"
```

Expected output:
```json
{"status": "posted", "post_id": "...", "url": "https://www.instagram.com/p/.../", "timestamp": "..."}
```

## Caption Best Practices

- First line is the hook (shows before "more" cutoff)
- 3–10 hashtags on the last line
- Max 2,200 characters
- Emojis encouraged for engagement

## API Flow (internal)

1. `POST /{ig-user-id}/media` — creates a media container with `image_url` + `caption`
2. Poll `GET /{creation_id}?fields=status_code` until `FINISHED` (up to 90s)
3. `POST /{ig-user-id}/media_publish` — publishes the container

## Rules

- **Never** post without a file in `vault/Approved/`
- **Image URL must be public HTTPS** — local paths are rejected by the API
- **Always** log every post attempt to `vault/Logs/`
- **Max 3 posts per day** to avoid spam flags
