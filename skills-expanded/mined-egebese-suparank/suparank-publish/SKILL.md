---
name: suparank/publish
description: Publishing phase - publish articles to WordPress, Ghost, generate images, and send webhooks.
user_invocable: true
---

# Suparank Publishing Phase

You handle publishing content to CMS platforms, generating images, and sending webhooks. All publishing uses `curl` commands via the Bash tool.

## Before Starting

1. Read credentials from `~/.claude/suparank-credentials.json`
2. If it doesn't exist, check the legacy path `~/.suparank/credentials.json` as fallback
3. If neither exists, tell the user:
   - "No publishing credentials found. Run `/suparank/setup` to configure WordPress, Ghost, or image generation."
   - They can still save content locally without credentials.
4. Read the project config from `.claude/suparank.json` for site context

## Detect Publishing Action

### Publish to WordPress
**Triggers:** "publish to WordPress", "post to WordPress", "send to WordPress"

**Requirements:** `~/.claude/suparank-credentials.json` must have a `wordpress` section with:
- `site_url`: WordPress site URL
- `username`: WordPress username
- `app_password`: WordPress application password

**Steps:**

1. Get the article to publish:
   - Read from `.claude/suparank-session.json` for the latest saved article
   - Or let the user specify which article (by number or title)
   - Read the article content from `.claude/suparank-content/[folder]/article.md`
   - Read metadata from `metadata.json`

2. Convert markdown content to HTML:
   - Convert the markdown article to clean HTML
   - Preserve heading hierarchy (h1, h2, h3)
   - Convert lists, bold, italic, links, code blocks
   - Convert images to `<img>` tags

3. Publish via WordPress REST API using curl:

```bash
curl -s -X POST "${site_url}/wp-json/wp/v2/posts" \
  -H "Authorization: Basic $(echo -n '${username}:${app_password}' | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Article Title",
    "content": "<html content>",
    "status": "draft",
    "excerpt": "Meta description"
  }'
```

4. Parse the response to get:
   - Post ID
   - Post URL
   - Edit URL

5. If a featured image URL is available (from image generation), set it:
   - First, upload the image via media endpoint
   - Then set as featured_media on the post

6. Report success:
   - "Published to WordPress as draft!"
   - "Title: [title]"
   - "URL: [url]"
   - "Edit: [edit_url]"

7. Update session: mark article as published_to: ["wordpress"]

**Status options:** Ask the user: "Publish as draft (default) or live?"
- `draft` (default, safer)
- `publish` (immediately live)

### Publish to Ghost
**Triggers:** "publish to Ghost", "post to Ghost", "send to Ghost"

**Requirements:** `~/.claude/suparank-credentials.json` must have a `ghost` section with:
- `api_url`: Ghost site API URL
- `admin_api_key`: Ghost Admin API key (format: `id:secret`)

**Steps:**

1. Get the article (same as WordPress flow above)

2. Convert markdown to HTML

3. Generate a Ghost Admin API JWT token using a Node.js one-liner:

```bash
TOKEN=$(node -e "
const c = require('crypto');
const [id, secret] = '${admin_api_key}'.split(':');
const h = Buffer.from(JSON.stringify({alg:'HS256',typ:'JWT',kid:id})).toString('base64url');
const now = Math.floor(Date.now()/1000);
const p = Buffer.from(JSON.stringify({iat:now,exp:now+300,aud:'/admin/'})).toString('base64url');
const sig = c.createHmac('sha256', Buffer.from(secret,'hex')).update(h+'.'+p).digest('base64url');
console.log(h+'.'+p+'.'+sig);
")
```

4. Create the Ghost mobiledoc payload:

```json
{
  "posts": [{
    "title": "Article Title",
    "mobiledoc": "{\"version\":\"0.3.1\",\"atoms\":[],\"cards\":[[\"html\",{\"html\":\"<html content>\"}]],\"markups\":[],\"sections\":[[10,0]]}",
    "status": "draft",
    "tags": [{"name": "keyword1"}, {"name": "keyword2"}],
    "feature_image": "image_url_if_available"
  }]
}
```

5. Publish via Ghost Admin API:

```bash
curl -s -X POST "${api_url}/ghost/api/admin/posts/" \
  -H "Authorization: Ghost ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '${post_data}'
```

6. Parse response and report success
7. Update session: mark article as published_to: ["ghost"]

### Generate Images
**Triggers:** "generate images", "create images", "generate hero image", "make images for article"

**Requirements:** `~/.claude/suparank-credentials.json` must have image provider config:
- `image_provider`: "fal" (currently the only supported provider)
- `fal.api_key`: fal.ai API key

**If `image_provider` is missing or set to an unsupported value** (anything other than "fal"):
- Skip image generation with message: "Skipped images (unsupported provider '[value]', only 'fal' is currently supported)"
- Do NOT block the rest of publishing

**Steps:**

1. Read the article from session to understand content
2. Read image prompt template from `~/.claude/skills/suparank/templates/image-prompt-designer.md`
3. Generate image prompts based on article content and visual style from config
4. For each image, call fal.ai via curl:

```bash
curl -s -X POST "https://fal.run/fal-ai/flux/schnell" \
  -H "Authorization: Key ${fal_api_key}" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "detailed image prompt here",
    "image_size": "landscape_16_9",
    "num_images": 1
  }'
```

5. Parse response to get image URL from `result.images[0].url`
6. Store image URLs in session metadata
7. Report: "Generated [N] images. Cover: [url]. Ready to publish."

**Image count calculation:**
- 1 cover/hero image (always)
- 1 inline image per 300 words of content (if config.content.include_images is true)

### Send Webhook
**Triggers:** "send webhook", "notify Slack", "send to Make", "trigger webhook"

**Requirements:** `~/.claude/suparank-credentials.json` must have `webhooks` section

**Steps:**

1. Determine webhook type: slack / make / n8n / zapier / default
2. Build the payload:

For Slack:
```bash
curl -s -X POST "${slack_url}" \
  -H "Content-Type: application/json" \
  -d '{"text": "New article published: [title]\n[url]"}'
```

For Make/n8n/Zapier:
```bash
curl -s -X POST "${webhook_url}" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "suparank",
    "timestamp": "2026-02-23T10:30:00Z",
    "title": "Article Title",
    "url": "https://...",
    "keywords": ["keyword1", "keyword2"]
  }'
```

3. Report success: "Webhook sent to [type]!"

## Batch Publishing

When publishing multiple articles (from multi-article pipeline):

1. Read all articles from session
2. Publish each one sequentially
3. Track progress: "Publishing article 1 of 3..."
4. Report summary: "Published 3 articles to WordPress as drafts."

## When Called from Pipeline

When invoked by the pipeline orchestrator:
- Generate images first (if enabled and credentials available)
- Then publish to all configured platforms
- Use draft status by default
- Report results but don't ask questions - the pipeline is automated

## Graceful Degradation

If credentials are missing for a specific platform:
- Skip that platform silently
- Report which platforms were skipped and why
- Never fail the entire publish phase because one platform is missing

Example: "Published to WordPress. Skipped Ghost (not configured). Skipped images (no fal.ai key)."

## Image Generation Error Handling

If image generation fails, handle gracefully:

1. **Timeout (>60s):** "Image generation timed out. Publishing without images."
2. **Rate limiting:** "Image provider rate limited. You can retry with `/suparank/publish` later."
3. **Invalid prompt:** Try a simplified prompt. If it still fails, skip that image.
4. **API key invalid:** "fal.ai API key is invalid. Update with `/suparank/setup`."

Never block the entire publishing phase because image generation failed.

## Security Notes

- Credentials are read from `~/.claude/suparank-credentials.json` (or legacy `~/.suparank/credentials.json`)
- NEVER log or display full API keys, passwords, or tokens in output
- When showing curl commands to the user, ALWAYS mask sensitive values:
  - API keys: show first 4 chars only → `sk_l****`
  - Passwords: replace entirely → `****`
  - Tokens: show first 10 chars → `eyJhbGci...`
  - Example: `Authorization: Basic ****` (never the actual base64 string)
- Application passwords are safer than regular WordPress passwords
- If an error message contains credentials, sanitize before displaying
