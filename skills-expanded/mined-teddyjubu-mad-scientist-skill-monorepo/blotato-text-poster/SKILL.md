---

name: blotato-text-poster
description: blotato-text-poster lets the user publish text-based social content through Blotato, making it useful for pushing written posts, captions, short updates, promotional copy, or repurposed text assets out to connected social channels without having to manually open each platform and post them one by one.
category: social-media

---
Post text-only content to Blotato-connected social accounts (Twitter/X, LinkedIn, etc.) via the v2 API.

## What This Skill Does

This skill blotato-text-poster lets the user publish text-based social content through Blotato, making it useful for pushing written posts, captions, short updates, promotional copy, or repurposed text assets out to connected social channels without having to manually open each platform and post them one by one.

## API Details

```
Endpoint: POST https://backend.blotato.com/v2/posts
Auth Header: blotato-api-key: {key}
Content-Type: application/json
API Key: blt_C4H/l9gOlOm/+pt4wXQqWiJ9VBMl3n/FEW17OKovrtw=
```

## Account IDs

| Platform | Account ID | targetType |
|----------|-----------|------------|
| Twitter/X | 10251 | twitter |
| Facebook | 15082 | facebook |
| Instagram | 24117 | instagram |
| TikTok | 23181 | tiktok |
| YouTube | 21244 | youtube |

## Payload Format

**CRITICAL: `mediaUrls` is REQUIRED even for text-only posts — use empty array `[]`**
**CRITICAL: `targetType` must match platform name exactly — "twitter" NOT "tweet"**

```json
{
  "post": {
    "accountId": "10251",
    "content": {
      "text": "Your post text here",
      "mediaUrls": [],
      "platform": "twitter"
    },
    "target": {
      "targetType": "twitter"
    }
  }
}
```

## Posting an X Thread

Loop through tweets, posting each one individually:

```python
import requests
import json

API_KEY = "blt_C4H/l9gOlOm/+pt4wXQqWiJ9VBMl3n/FEW17OKovrtw="
BASE_URL = "https://backend.blotato.com/v2/posts"

def post_tweet(text):
    payload = {
        "post": {
            "accountId": "10251",
            "content": {
                "text": text,
                "mediaUrls": [],
                "platform": "twitter"
            },
            "target": {
                "targetType": "twitter"
            }
        }
    }
    resp = requests.post(BASE_URL,
        headers={"blotato-api-key": API_KEY, "Content-Type": "application/json"},
        json=payload)
    return resp.json()

# Post each tweet in the thread
tweets = ["tweet 1 text...", "tweet 2 text...", ...]
for t in tweets:
    result = post_tweet(t)
    print(result)  # Returns {"postSubmissionId": "..."}
```

## Posting to LinkedIn

Same format, just change accountId and targetType:

```json
{
  "post": {
    "accountId": "9668",
    "content": {
      "text": "Your LinkedIn post...",
      "mediaUrls": [],
      "platform": "linkedin"
    },
    "target": {
      "targetType": "linkedin"
    }
  }
}
```

## Pitfalls

- **DO NOT use `targetType: "tweet"`** — must be `"twitter"`
- **DO NOT omit `mediaUrls`** — it is required, use `[]` for text-only
- **Endpoint is `backend.blotato.com/v2`** NOT `api.blotato.com` (that domain does not resolve)
- Auth header is `blotato-api-key:` NOT `Authorization: Bearer`
- X threads are posted as individual posts, not auto-threaded by Blotato. Each tweet is a separate submission.
