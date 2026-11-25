---
name: skill-to-web-app
description: Wrap an existing Hermes skill as a public-facing website deployed on Vercel
---

# Skill-to-Web-App

**Take an existing AI skill (triggered by voice/text in Telegram) and wrap it as a public website on Vercel.**

## What This Skill Does

This skill Wrap an existing Hermes skill as a public-facing website deployed on Vercel.

## When to Use
- User wants to expose an existing skill to the public via a web interface
- The skill involves image upload, form input, and report generation
- Need a self-contained, no-login, instant-value web app

## Architecture
Single Next.js app with:
- **Frontend**: React page with image upload + form inputs → submits to API route
- **API Route** (`/app/api/xxx/route.js`): Edge runtime, handles all skill logic serverlessly
- **Results page**: Inline component that displays the generated report
- **Deploy**: Vercel (default hosting)

## File Structure
```
my-web-app/
├── package.json          # next, react, react-dom
├── app/
│   ├── layout.js         # Minimal layout with metadata
│   ├── page.js           # Main UI (form + results as inline component)
│   └── api/xxx/
│       └── route.js      # Edge runtime handler for skill logic
```

## Step-by-Step

### 1. Create project
```bash
mkdir -p my-web-app/app/api/xxx
```

### 2. package.json
```json
{
  "name": "my-web-app",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "^15.1.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0"
  }
}
```

### 3. Build all files BEFORE npm install
Write all source files first, then run `npm install`. This avoids editing node_modules.

### 4. API route pattern (edge runtime)
```js
export const runtime = 'edge'

export async function POST(request) {
  // 1. Parse FormData from client
  const formData = await request.formData()
  const image = formData.get('image')
  // 2. Convert image to base64 for AI analysis
  const bytes = await image.arrayBuffer()
  const base64 = Buffer.from(bytes).toString('base64')
  // 3. Call AI (OpenRouter/Gemini) for analysis
  // 4. Call external APIs (SerpApi, etc.) for data
  // 5. Calculate and return JSON
}
```

### 5. Frontend pattern
- Single page with form (image upload + inputs)
- On submit: POST FormData to API route
- Show loading state during API call
- On success: swap to Results component (all inline, no navigation)

### 6. Deploy to Vercel
```bash
cd my-web-app
npm install

# Deploy (token in .secrets/vercel.env)
VERCEL_TOKEN=$(grep VERCEL_TOKEN /path/to/vercel.env | cut -d= -f2-)
vercel --token "$VERCEL_TOKEN" --name my-web-app --confirm

# Set env vars in Vercel dashboard:
# https://vercel.com/<org>/<project>/settings/environment-variables
```

## API Key Strategy
- **DO NOT** hardcode API keys in the app
- Use Vercel environment variables (`process.env.XXX`)
- The app should gracefully handle missing keys with clear error messages
- Required env vars: document which ones the user needs to set

## Pitfalls

### DO NOT over-investigate before building
When the user says "build this", start building. Check the existing skill, create the project scaffold, and write all files. Only investigate API keys that are strictly necessary — and even then, design the app to read them from env vars. You will waste turns searching for keys that may not exist or may be deleted.

### Terminal REDACTS secret values in output
The terminal tool replaces sensitive values (API keys, tokens) with `***` in stdout. If you `grep` or `cat` a secret and try to use it in a Python string or curl command constructed from that output, you'll get `***` instead of the real value. **Solution**: Write a Python script to a temp file that reads the secret directly from the source files internally — never pass secrets through terminal string interpolation. Use `write_file()` to create `/tmp/script.py`, then `terminal("python3 /tmp/script.py")`.

### Edge runtime limitations
OpenRouter returns a **404** (not a graceful error) for model IDs that don't exist. Always verify the model exists.

**Verified working models (as of April 2026):**
- `google/gemini-2.0-flash-001` — Vision API + fast, free tier available
- `google/gemini-2.0-flash-lite-001` — Cheaper, no vision
- `anthropic/claude-sonnet-4-6-20250514` — High quality

**Avoid non-existent models:** `google/gemini-2.5-flash:free` does NOT exist on OpenRouter. The `:free` suffix is only used in Hermes's internal routing config, NOT in actual OpenRouter model IDs. For free models on OpenRouter, use the base ID — OpenRouter handles the free tier internally.

### Edge runtime limitations
`export const runtime = 'edge'` means:
- No Node.js-only modules (fs, path, etc.)
- No `require()` — use dynamic imports or ESM only
- Use `Buffer.from()` for encoding (available in edge)
- No large dependencies — keep it lean

### FormData handling
- Client: `const formData = new FormData(); formData.append('image', file)`
- Server: `const formData = await request.formData()`
- File: `await file.arrayBuffer()` then `Buffer.from(bytes).toString('base64')`

### Terminal redacts env var values — DO NOT pass secrets via shell commands
The terminal tool REDACTS sensitive values in OUTPUT, replacing them with `***`. If you grep a key from a `.env` file and try to use it in a `curl` or `python3 -c` command, the shell sees the real value but your Python/shell script may receive garbage if you constructed it from terminal output.

**Solution**: Write a Python script to a file that reads the secret directly from the source `.env` file and makes the API call internally — never pass the secret through terminal command output or string interpolation in a shell command. Use `write_file()` to create the script, then `terminal()` to `python3 script.py`.

### Setting env vars on Vercel via API (avoids interactive CLI)
Use the Vercel REST API to set env vars programmatically. This avoids interactive prompts and works cleanly with token auth.

**Delete existing env var first** (create will fail with `ENV_CONFLICT` if one already exists):
1. List env vars: `GET https://api.vercel.com/v9/projects/{project}/env/` — find the env var ID
2. Delete: `DELETE https://api.vercel.com/v9/projects/{project}/env/{id}`
3. Create: `POST https://api.vercel.com/v10/projects/{project}/env` with JSON body:
   ```json
   {"key":"NAME","value":"secret","target":["production","preview","development"],"type":"encrypted"}
   ```

**Python script template** (saves to `/tmp/set_env.py`, reads keys from files, calls Vercel API):
```python
import json, urllib.request
key = [l.split("=",1)[1].strip() for l in open("/root/.hermes/.env") if l.startswith("OPENROUTER_API_KEY=")][0]
token = [l.split("=",1)[1].strip() for l in open("/path/to/vercel.env") if "VERCEL_TOKEN=" in l][0]

# Delete existing
resp = json.loads(urllib.request.urlopen(urllib.request.Request(
    "https://api.vercel.com/v9/projects/{project}/env/",
    headers={"Authorization": f"Bearer {token}"}
)).read())
for env in resp.get("envs", []):
    if env["key"] == "OPENROUTER_API_KEY":
        urllib.request.urlopen(urllib.request.Request(
            f"https://api.vercel.com/v9/projects/{project}/env/{env['id']}",
            method="DELETE", headers={"Authorization": f"Bearer {token}"}
        ))

# Create new
data = json.dumps({"key":"OPENROUTER_API_KEY","value":key,"target":["production","preview","development"],"type":"encrypted"}).encode()
urllib.request.urlopen(urllib.request.Request(
    "https://api.vercel.com/v10/projects/{project}/env",
    data=data, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
)).read()
print("SUCCESS")
```

### Vercel project naming
- `vercel deploy` will prompt for org/team if not specified
- Team ID from memory: `team_RI521BtIL6MYYsZZaNfI1oQo`
- The `--confirm` flag skips interactive prompts
- After setting env vars via API, you MUST redeploy (`vercel --prod`) for the new env values to take effect in the serverless functions
