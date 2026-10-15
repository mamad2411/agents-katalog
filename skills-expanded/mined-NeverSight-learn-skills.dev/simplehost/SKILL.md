---
name: simplehost
description: Publish any file or folder to the web instantly via simplehost.dev. Use when the user wants to publish, deploy, host, or share HTML/CSS/JS files, static sites, images, PDFs, or any files as a live website. Also triggers on "make this live", "give me a URL", "host this", "deploy this", "add a domain", "claim a handle", "check my account", "password protect", "set up a link", or "manage subscription".
argument-hint: "[directory-or-file]"
allowed-tools: Read, Glob, Grep, Bash, Write
---

# SimpleHost — Instant Web Publishing

Publish any file or folder to a live URL at `<slug>.simplehost.dev`. Everything works from the terminal.

Base URL: `https://simplehost.dev`
Auth header (when needed): `Authorization: Bearer $SIMPLEHOST_API_KEY`

---

## Publish a Site

**Just publish. Don't ask questions first.** Get the site live, then offer options.

### Step 1: Find what to publish

- Use `$ARGUMENTS` if provided
- Otherwise look for: `dist/`, `build/`, `out/`, `public/`, `.next/out/`
- If nothing found, ask the user
- Single files work too — publish a single image, PDF, video, or any file and SimpleHost auto-generates a viewer page

### Step 2: Download the publish script

```bash
curl -fsSL https://simplehost.dev/publish.sh -o /tmp/simplehost-publish.sh && chmod +x /tmp/simplehost-publish.sh
```

### Step 3: Publish

```bash
# If SIMPLEHOST_API_KEY is set, it publishes permanently. If not, it publishes temporarily.
/tmp/simplehost-publish.sh <directory>

# To update an existing site
/tmp/simplehost-publish.sh <directory> <existing-slug>
```

### Step 4: After publishing, show the result

Show the live URL prominently: `https://<slug>.simplehost.dev/`

**If the publish was anonymous** (no API key), the response includes a `claimToken`. Save it. Tell the user:
> "Your site is live! This link expires in 24 hours. Want me to make it permanent? It's free — I just need your email and it takes 30 seconds."

If they say yes, run the Sign Up flow below, then claim the site with:
```bash
curl -s -X POST https://simplehost.dev/api/v1/publish/<slug>/claim \
  -H "Authorization: Bearer $SIMPLEHOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"claimToken": "TOKEN_FROM_PUBLISH_RESPONSE"}'
```

---

## Sign Up / Login

Only do this when the user wants to make a site permanent or explicitly asks to sign up. Never ask for this upfront.

```bash
# 1. Send verification code
curl -s -X POST https://simplehost.dev/api/auth/agent/request-code \
  -H "Content-Type: application/json" \
  -d '{"email": "USER_EMAIL"}'

# 2. User checks email, gives you the XXXX-XXXX code

# 3. Verify and get API key
curl -s -X POST https://simplehost.dev/api/auth/agent/verify-code \
  -H "Content-Type: application/json" \
  -d '{"email": "USER_EMAIL", "code": "XXXX-XXXX"}'
```

Response gives `apiKey`. Tell the user to add it to their shell profile so it works forever:
```bash
export SIMPLEHOST_API_KEY="sh_live_..."
```

---

## Check Account

```bash
curl -s https://simplehost.dev/api/v1/account \
  -H "Authorization: Bearer $SIMPLEHOST_API_KEY"
```

Returns: plan, usage (sites, storage, domains), limits, email, handle.

---

## Manage Sites

```bash
# List all sites
curl -s https://simplehost.dev/api/v1/publishes \
  -H "Authorization: Bearer $SIMPLEHOST_API_KEY"

# Get site details
curl -s https://simplehost.dev/api/v1/publish/<slug> \
  -H "Authorization: Bearer $SIMPLEHOST_API_KEY"

# Delete a site
curl -s -X DELETE https://simplehost.dev/api/v1/publish/<slug> \
  -H "Authorization: Bearer $SIMPLEHOST_API_KEY"

# Duplicate a site
curl -s -X POST https://simplehost.dev/api/v1/publish/<slug>/duplicate \
  -H "Authorization: Bearer $SIMPLEHOST_API_KEY"
```

---

## Update Site Metadata

Use `PATCH /api/v1/publish/<slug>/metadata` to update any of these fields:

```bash
# Update title and description (for SEO / social previews)
curl -s -X PATCH https://simplehost.dev/api/v1/publish/<slug>/metadata \
  -H "Authorization: Bearer $SIMPLEHOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Site", "description": "A cool project"}'

# Set OG image for social media previews (path relative to site root)
curl -s -X PATCH https://simplehost.dev/api/v1/publish/<slug>/metadata \
  -H "Authorization: Bearer $SIMPLEHOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ogImagePath": "images/preview.png"}'

# Password protect a site
curl -s -X PATCH https://simplehost.dev/api/v1/publish/<slug>/metadata \
  -H "Authorization: Bearer $SIMPLEHOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"password": "secret123"}'

# Remove password protection
curl -s -X PATCH https://simplehost.dev/api/v1/publish/<slug>/metadata \
  -H "Authorization: Bearer $SIMPLEHOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"password": null}'

# Set auto-expiry (Hobby plan only) — site deletes itself after N seconds
curl -s -X PATCH https://simplehost.dev/api/v1/publish/<slug>/metadata \
  -H "Authorization: Bearer $SIMPLEHOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ttlSeconds": 86400}'

# Remove auto-expiry
curl -s -X PATCH https://simplehost.dev/api/v1/publish/<slug>/metadata \
  -H "Authorization: Bearer $SIMPLEHOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ttlSeconds": null}'
```

---

## Links (Path Routing)

Route paths on your handle or custom domain to specific sites. For example, `yourname.simplehost.dev/docs` can point to a different published site.

Requires a handle or custom domain.

```bash
# List all links
curl -s https://simplehost.dev/api/v1/links \
  -H "Authorization: Bearer $SIMPLEHOST_API_KEY"

# Create a link on your handle subdomain
# yourname.simplehost.dev/docs → points to site with slug "bright-canvas-a7k2"
curl -s -X POST https://simplehost.dev/api/v1/links \
  -H "Authorization: Bearer $SIMPLEHOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"location": "docs", "targetSlug": "bright-canvas-a7k2"}'

# Create a link on a custom domain
# example.com/blog → points to site with slug "my-blog-x9f3"
curl -s -X POST https://simplehost.dev/api/v1/links \
  -H "Authorization: Bearer $SIMPLEHOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"location": "blog", "targetSlug": "my-blog-x9f3", "domain": "example.com"}'

# Delete a link
curl -s -X DELETE https://simplehost.dev/api/v1/links/<link-id> \
  -H "Authorization: Bearer $SIMPLEHOST_API_KEY"
```

---

## Custom Domains

Only when the user asks to connect a domain.

```bash
# Add domain
curl -s -X POST https://simplehost.dev/api/v1/domains \
  -H "Authorization: Bearer $SIMPLEHOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'

# Verify after DNS setup
curl -s -X POST https://simplehost.dev/api/v1/domains/example.com/verify \
  -H "Authorization: Bearer $SIMPLEHOST_API_KEY"

# List domains
curl -s https://simplehost.dev/api/v1/domains \
  -H "Authorization: Bearer $SIMPLEHOST_API_KEY"

# Remove domain
curl -s -X DELETE https://simplehost.dev/api/v1/domains/example.com \
  -H "Authorization: Bearer $SIMPLEHOST_API_KEY"
```

---

## Custom Handle

A vanity URL like `yourname.simplehost.dev`. Requires Hobby plan ($5/mo).

```bash
# Claim
curl -s -X PUT https://simplehost.dev/api/v1/handle \
  -H "Authorization: Bearer $SIMPLEHOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"handle": "yourname"}'

# Check current
curl -s https://simplehost.dev/api/v1/handle \
  -H "Authorization: Bearer $SIMPLEHOST_API_KEY"

# Release
curl -s -X DELETE https://simplehost.dev/api/v1/handle \
  -H "Authorization: Bearer $SIMPLEHOST_API_KEY"
```

---

## Billing & Upgrade

```bash
# Get a checkout link to upgrade to Hobby ($5/mo)
curl -s -X POST https://simplehost.dev/api/billing/checkout \
  -H "Authorization: Bearer $SIMPLEHOST_API_KEY"
# Returns {"checkoutUrl": "https://..."} — tell user to open it in browser

# Manage subscription (cancel, update payment method)
curl -s -X POST https://simplehost.dev/api/billing/portal \
  -H "Authorization: Bearer $SIMPLEHOST_API_KEY"
# Returns {"portalUrl": "https://...", "status": "active", "currentEnd": "..."}
```

When API errors include an `upgrade` object, show the user `upgrade.message` and offer to get a checkout link.

---

## Quick Facts

- **Static files only**: HTML, CSS, JS, images, fonts, PDFs, videos, audio, text, JSON — any file works
- **Single-file publishing**: Upload one image/PDF/video and SimpleHost auto-generates a viewer page
- **No index.html needed**: If missing, SimpleHost shows a browsable file listing
- **No server-side code**: No Node.js, Python, PHP, etc.
- **Max 1,000 files** per site

### Plan Limits

| | Free | Hobby ($5/mo) |
|---|---|---|
| Sites | 500 | Unlimited |
| Storage | 10 GB | 100 GB |
| Max file size | 250 MB | 5 GB |
| Domains | 1 | 5 |
| Handle | — | ✓ |
| Password protection | ✓ | ✓ |
| Auto-expiry (TTL) | — | ✓ |
| API rate limit | 60/hour | 200/hour |
