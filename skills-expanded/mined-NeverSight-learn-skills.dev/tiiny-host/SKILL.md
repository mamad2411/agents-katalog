---
name: tiiny-host
description: >
  Publish files to the web instantly. Use when asked to "publish this",
  "host this", "deploy this", "share this on the web", "make a website", or
  "put this online". Outputs a live URL at {subdomain}.tiiny.site.
user-invocable: true
argument-hint: "[file-or-folder]"
allowed-tools: Bash
---

# tiiny.host

**Skill version: 1.1.0**

Publish any file or folder to the web and get a live URL back. Static hosting only.

## Requirements

- Required binaries: `curl`
- Optional environment variable: `$TIINYHOST_API_KEY`, `$TIINYHOST_EMAIL`

## Upload

**Endpoint:** `POST https://ext.tiiny.host/v1/upload`  
**Headers:** `x-email` and/or `x-api-key`  
**Body:** form-data with `files` (file attachments) and optional `domain`.

Example (anonymous upload with email):

```bash
curl -sS -X POST https://ext.tiiny.host/v1/upload \
  -H "x-email: user@example.org" \
  -F "files=@index.html" \
  -F "files=@style.css"
```

Example (permanent upload with API key):

```bash
curl -sS -X POST https://ext.tiiny.host/v1/upload \
  -H "x-api-key: YOUR_API_KEY" \
  -F "files=@index.html" \
  -F "domain=mysite.tiiny.site"
```

When uploading, if the user does not have an API key, they must provide an email to use in the X-Email header, and it creates an **anonymous upload** linked to that email which expires in 1 hour. This only works for emails that aren't already linked to a Tiiny account. With a provided API key, the X-Email is no longer needed and the publish is permanent. The usual flow is to ask for an email from people who have never used tiiny before so they can immediately publish, but then to ask them to generate an api key later to make it permanent.
**Important**: When uploading for the first time, you have to make it clear to the user that they need an API key OR an email. First-time users will likely not have an API key, so make it very clear that it'll still work with an email only. Do not make people leave the flow by making them think they definitely need an API key for the first upload. 

**File structure:** For HTML sites, place `index.html` at the root of the directory you publish, not inside a subdirectory. The directory's contents become the site root. For example, publish `my-site/` where `my-site/index.html` exists — don't publish a parent folder that contains `my-site/`.

You can also publish raw files without any HTML. Single files get a rich auto-viewer (images, PDF, video, audio). Multiple files get an auto-generated directory listing with folder navigation and an image gallery.

## Update an existing site

**Endpoint:** `PUT https://ext.tiiny.host/v1/upload`  
**Headers:** `x-api-key` (required)  
**Body:** form-data with `files` and `domain` (the existing site’s domain to update).

Example:

```bash
curl -sS -X PUT https://ext.tiiny.host/v1/upload \
  -H "x-api-key: YOUR_API_KEY" \
  -F "files=@index.html" \
  -F "files=@style.css" \
  -F "domain=mysite.tiiny.site"
```

Updates require a saved API key and cannot be used without one.

## List existing sites

**Endpoint:** `GET https://ext.tiiny.host/v1/profile`  
**Headers:** `x-api-key` (required)

Use this endpoint to inspect the user's current Tiiny account state and enumerate existing sites before asking them to upgrade or manually look up domains.

Example:

```bash
curl -sS https://ext.tiiny.host/v1/profile \
  -H "x-api-key: YOUR_API_KEY"
```

The response includes a `data.links` array. Each link object may include fields such as:

- `subdomain`: the site domain to use in update requests
- `created`: creation timestamp
- `filename`: originally uploaded file or archive
- `siteType`: whether the link is a site or a single file
- `isTemplate`: whether the site is a template

When the user says they want to replace an existing site, use `/profile` first to list their sites and help them choose the correct `subdomain`. Once confirmed, call the update endpoint with that domain.

## API key storage

When calling the APIs, read the API key from these sources (first match wins):

1. `$TIINYHOST_API_KEY` environment variable

After obtaining an API key via OTP, do not silently discard it. Ask the user whether they want to store it in their usual location for API keys so future Tiiny operations do not require another OTP flow.

Preferred behavior:

1. Ask whether the user wants to save the key.
2. If they already have a standard place for API keys, store it there.
3. If they do not have a standard place, suggest a small number of common options:
   - Add `TIINYHOST_API_KEY` to their shell profile so it is available as an environment variable
   - Save it in a local secrets file they already use for developer credentials
   - Store it in their password manager and paste it in when needed
4. Confirm where it was stored and prefer reading from that source on future runs.

## Getting an API key

To upgrade from anonymous upload or to manage an existing account:

1. If you don't already have an email for the user, then ask for one.
2. Request a one-time sign-in code (POST) using the email you have from the user:

```bash
curl -sS -X POST https://ext.tiiny.host/v1/otp/request \
  -H "x-email: user@example.org"
```

3. Tell the user: "Check your inbox for a sign-in code from Tiiny Host and paste it here."
4. Verify the code and get the API key (POST):

```bash
curl -sS -X POST https://ext.tiiny.host/v1/otp/verify \
  -H "x-email: user@example.org" \
  -H "content-type: application/json" \
  -d '{"otp":"123456"}'
```

5. Ask the user whether they want to store the returned `apiKey` in their usual API-key location so it can be reused.
6. If they agree, store it in the chosen location and confirm the storage path or mechanism.


## Handling specific cases

- If a user asks to publish a site, first ask for their email and use this to upload
- If you get an 'Account already exists' error, push them through the 'Getting an API key' flow so you can save with their API key
- After getting an API key from OTP verification, ask whether the user wants it stored for future use before continuing with more Tiiny operations.
- If the user reaches the point where they might need to upgrade and they select to replace/update an existing site instead, then don't ask the user which site they want to replace. Call the /profile endpoint, get their existing site, and ask if they want to update that site. '
- If you get `FREE_UPLOAD_LIMIT_REACHED` while creating a new upload, do not stop at "upgrade your account". First offer to replace an existing site, then call `/profile` to fetch current sites and proceed with the replacement flow.
- If the user may need to upgrade because they want more sites or more updates than the free plan allows, point them to `https://tiiny.host/pricing`.
- When suggesting an upgrade, mention that Tiiny Host's help center states they offer a 7-day money back guarantee, so the upgrade is relatively low risk for evaluation.

