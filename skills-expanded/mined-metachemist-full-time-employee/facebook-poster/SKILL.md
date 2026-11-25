---
name: facebook-poster
description: |
  Create and publish text posts to a Facebook Page using the official Graph API.
  Use when asked to post on Facebook, or when processing an approved
  APPROVAL_SEND_FACEBOOK_POST_*.md file from vault/Approved/.
  Always draft first and require human approval before posting.
---

# Facebook Poster

Publish posts to a Facebook Page using the Graph API (no browser required).

## When to Use

- Processing an `APPROVAL_SEND_FACEBOOK_POST_*.md` file from `vault/Approved/`
- Creating a new post when explicitly instructed by the user
- Drafting post content for human review (no approval needed for drafts)

**Never post directly** — always route through `vault/Pending_Approval/` first.

## One-Time Setup

### 1. Create a Facebook App

1. Go to https://developers.facebook.com → **My Apps** → **Create App**
2. Choose **Business** type, fill in the name, click **Create**
3. Add products: **Facebook Login** and **Pages API**

### 2. Get a Page Access Token

In Graph API Explorer (https://developers.facebook.com/tools/explorer/):

1. Select your App from the dropdown
2. Click **Generate Access Token** → grant these scopes:
   - `pages_show_list` — required for `/me/accounts` (auto-derive page token)
   - `pages_manage_posts` — required to post
   - `pages_read_engagement` — read page metrics
3. Call `GET /me/accounts` — find your Page in the response
4. Copy the `access_token` value for your Page (this is the Page Access Token)
5. Copy the `id` value (this is your Page ID)

To convert to a long-lived token (~60 days):
```
GET https://graph.facebook.com/v21.0/oauth/access_token
    ?grant_type=fb_exchange_token
    &client_id={APP_ID}
    &client_secret={APP_SECRET}
    &fb_exchange_token={SHORT_LIVED_TOKEN}
```

### 3. Add to `.env`

```
FACEBOOK_PAGE_ID=123456789
FACEBOOK_PAGE_ACCESS_TOKEN=EAAxxxxx...
```

## Approval File Format

```markdown
---
type: approval_request
action: send_facebook_post
status: approved
---

# What will happen after approval?

The following post will be published to the Facebook Page.

## Message / Content

  Your Facebook post text here.

  Can be multiple paragraphs. Facebook supports up to 63,206 characters.
```

Save to `vault/Approved/APPROVAL_SEND_FACEBOOK_POST_<topic>_<YYYY-MM-DD>.md`

## Dry-Run Mode

```bash
python .claude/skills/facebook-poster/scripts/create_post.py \
  --content "Post text..." --dry-run
```

Expected output:
```json
{"status": "dry_run", "content_len": 42, "preview": "Post text...", "timestamp": "..."}
```

## Live Post

```bash
python .claude/skills/facebook-poster/scripts/create_post.py \
  --content "Post text..."
```

Expected output:
```json
{"status": "posted", "post_id": "123456789_987654321", "url": "https://www.facebook.com/...", "timestamp": "..."}
```

## Token Expiry

Page access tokens last ~60 days. When expired, the script returns:
```
"error": "... — Page access token has expired. Refresh via: GET /me/accounts?access_token=<USER_TOKEN>"
```

Refresh by generating a new User Token in Graph API Explorer and calling `/me/accounts` again.

## Rules

- **Never** post without a file in `vault/Approved/`
- **Always** log every post attempt to `vault/Logs/`
- **Max 3 posts per day** to avoid spam flags
