---
name: social-post
description: Post to social media platforms using a multi-provider social posting API. Use when you want to post to Twitter, LinkedIn, Instagram, Facebook, TikTok, Threads, or Bluesky. Triggers on "post to twitter", "post to instagram", "social media post", "share on linkedin", "publish to social", or any social posting request.
inputs:
  - name: content
    type: string
    required: true
    description: The text content to post
  - name: platforms
    type: list
    required: true
    description: List of platforms to post to (e.g. ["twitter", "linkedin"])
  - name: media_urls
    type: list
    required: false
    description: Optional list of media URLs to attach to the post
outputs:
  - name: post_id
    type: string
    description: The ID of the created post
  - name: provider
    type: string
    description: The provider/platform that successfully posted
  - name: success
    type: bool
    description: Whether the post was successfully published
---

# Social Posting Skill

Post to multiple social media platforms via a unified social posting API with automatic provider fallback.

---

## Setup

**Location:** `~/social-posting-api/` (configurable — point to wherever you cloned your posting API)

**Environment:**
```bash
cd ~/social-posting-api
source venv/bin/activate
```

**Required env vars in `.env`:**
- `POSTFORME_API_KEY` - Primary provider ([PostForMe](https://postforme.dev))
- `LATE_API_KEY` - Fallback provider ([LATE](https://getlate.dev))

> You only need one provider to get started. PostForMe is recommended as the primary.

---

## Quick Commands

### Check Connected Accounts
```python
from social_posting import SocialPostingClient
from dotenv import load_dotenv
load_dotenv()

client = SocialPostingClient()
print("Providers:", client.available_providers)
for acc in client.get_accounts():
    print(f"  {acc.platform}: {acc.username}")
```

### Post Text Only
```python
result = client.post(
    content="Your post content here",
    platforms=["twitter", "linkedin"]
)
print(f"Success: {result.success}, Provider: {result.provider}")
```

### Post with Images
```python
result = client.post(
    content="Check out these photos!",
    platforms=["instagram"],
    media_urls=[
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg"
    ]
)
```

### Schedule a Post
```python
from datetime import datetime

result = client.post(
    content="Scheduled post",
    platforms=["linkedin"],
    scheduled_for=datetime(2025, 1, 15, 9, 0)  # UTC
)
```

---

## Supported Platforms

| Platform | Text Only | With Media | Notes |
|----------|-----------|------------|-------|
| Twitter/X | ✅ | ✅ | 280 char limit |
| LinkedIn | ✅ | ✅ | Best for professional content |
| Instagram | ❌ | ✅ | **Requires media** |
| Facebook | ✅ | ✅ | |
| TikTok | ❌ | ✅ | Video preferred |
| Threads | ✅ | ✅ | |
| Bluesky | ✅ | ✅ | |
| Pinterest | ❌ | ✅ | Requires media |
| YouTube | ❌ | ✅ | Video only |

---

## Complete Posting Script

```python
#!/usr/bin/env python
"""Post to social media platforms."""

import sys
sys.path.insert(0, '~/social-posting-api')  # Update this path

from social_posting import SocialPostingClient
from dotenv import load_dotenv
load_dotenv('~/social-posting-api/.env')  # Update this path

def post_to_social(content: str, platforms: list, media_urls: list = None):
    """Post content to specified platforms."""
    client = SocialPostingClient()

    # Check which platforms are connected
    accounts = client.get_accounts()
    connected = [a.platform for a in accounts]

    # Filter to only connected platforms
    valid_platforms = [p for p in platforms if p in connected]

    if not valid_platforms:
        print(f"No connected accounts for: {platforms}")
        print(f"Connected: {connected}")
        return None

    # Post
    result = client.post(
        content=content,
        platforms=valid_platforms,
        media_urls=media_urls
    )

    if result.success:
        print(f"✅ Posted via {result.provider}")
        print(f"   Post ID: {result.post_id}")
    else:
        print(f"❌ Failed: {result.error}")

    return result
```

---

## Workflow for Posting

### Step 1: Check Connected Accounts

Always check what's connected first:
```bash
cd ~/social-posting-api
source venv/bin/activate && python -c "
from social_posting import SocialPostingClient
from dotenv import load_dotenv
load_dotenv()
client = SocialPostingClient()
for acc in client.get_accounts():
    print(f'{acc.platform}: {acc.username}')
"
```

### Step 2: Prepare Content

- **Twitter**: Keep under 280 chars
- **LinkedIn**: Can be longer, professional tone
- **Instagram**: Needs at least 1 image
- **Xiaohongshu**: Use `xhs-image-gen` skill for carousel content

### Step 3: Execute Post

```bash
source venv/bin/activate && python -c "
from social_posting import SocialPostingClient
from dotenv import load_dotenv
load_dotenv()

client = SocialPostingClient()
result = client.post(
    content='''Your content here''',
    platforms=['platform1', 'platform2'],
    media_urls=['https://example.com/image.jpg']  # Optional
)
print(f'Success: {result.success}')
print(f'Provider: {result.provider}')
print(f'Post ID: {result.post_id}')
"
```

---

## Connecting New Accounts

### Via PostForMe (Primary)
1. Go to https://postforme.dev/dashboard
2. Click "Connect Account"
3. Select platform and authorize

### Via LATE (Fallback)
1. Go to https://getlate.dev/dashboard
2. Connect social accounts
3. API key in `.env` will auto-detect new accounts

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "No connected accounts" | Platform not linked | Connect via provider dashboard |
| "Instagram requires media" | Text-only post | Add at least 1 image URL |
| "HTTP 401" | Invalid API key | Check `.env` file |
| "All providers failed" | Both providers down | Try again later |

---

## Cross-Posting Strategy

**For open source announcements:**
```python
result = client.post(
    content="🚀 Just open-sourced my project!\n\nGitHub: https://github.com/yourusername/your-repo",
    platforms=["twitter", "linkedin"]
)
```

**For visual content:**
```python
# Multi-image post
result = client.post(
    content="Behind the scenes 🔧",
    platforms=["instagram"],
    media_urls=[
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg",
    ]
)
```
