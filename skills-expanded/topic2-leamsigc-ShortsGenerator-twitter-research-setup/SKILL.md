---
name: twitter-research-setup
version: 2.0.0
description: |
  Setup state for Twitter/X research tool. Checks prerequisites, creates
  directory structure, creates config.json with the research topic,
  target audience keywords, and optional seed accounts, sets up Chrome
  for X/Twitter access. Call this before any other twitter-research state.

allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Question
  - ChromeDevTools
---

# Twitter/X Research — Setup State (v2)

Run this first. Configures the research topic, audience keywords, and output structure.

## Steps

### 1. Gather Parameters

Ask the user:

1. **What topic do you want to research?** (e.g., `social media scheduling tools`, `Liga MX transfers`, `AI in content creation`) — this is the search query that drives the whole research.
2. **How many posts minimum do you want to explore?** (default: `10`, recommend `10-15` for good coverage)
3. **What optional seed accounts should bootstrap the search?** (comma-separated X handles, e.g., `@buffer, @hootsuite` — leave empty to rely purely on X search)
4. **What target audience keywords define the ideal customer?** (comma-separated, e.g., `social media manager, content creator, agency owner, freelancer`)
5. **What content format do you want generated?** (options: `social media post`, `video script`, `both`)
6. **What language?** (default: `en`)
7. **What's the user's product/service in one sentence?** (e.g., "A social media scheduling tool for agencies")

### 2. Create Output Directory

```bash
mkdir -p ".twitter-research/$(date +%Y-%m-%d_%H%M%S)"
```

Store the timestamp for later use.

### 3. Create config.json

```json
{
  "timestamp": "<YYYY-MM-DD_HHMMSS>",
  "topic": "<research topic / search query>",
  "topicKeywords": ["<keyword1>", "<keyword2>"],
  "minPosts": 10,
  "productDescription": "<user's product in one sentence>",
  "targetAudienceKeywords": ["<keyword1>", "<keyword2>", "<keyword3>"],
  "accounts": [
    {
      "handle": "@handle",
      "url": "https://x.com/handle",
      "name": "Account Name",
      "isSeed": true
    }
  ],
  "contentFormat": "both",
  "language": "en",
  "createdAt": "<YYYY-MM-DD HH:MM:SS>"
}
```

### 4. Install Node dependencies

```bash
npm install --prefix "$CLAUDE_SKILL_ROOT/scripts"  # ~/.claude/skills/twitter-research/scripts
# fallback: npm install --prefix ./skills/twitter-research/scripts
```

Installs `chrome-remote-interface` for the scrape/report scripts.

### 5. Ensure Chrome Has X/Twitter Access

Check if Chrome is accessible:

```bash
chrome-devtools list_pages
```

If Chrome is not running or accessible, start it:

```bash
google-chrome --remote-debugging-port=9222 --no-first-run --no-default-browser-check --user-data-dir=/tmp/chrome-twitter-research &
```

Wait 3 seconds for Chrome to start.

### 6. Verify X/Twitter Access

Navigate to X to check if the user is logged in:

```bash
chrome-devtools navigate_page --url "https://x.com/home"
```

Wait 5 seconds, then check if the login state is visible:

```javascript
async () => {
  await new Promise(r => setTimeout(r, 3000));
  const loginButton = document.querySelector('a[href="/login"], a[href="/i/flow/login"]');
  const isLoggedIn = !loginButton && document.body.innerText.length > 100;
  return JSON.stringify({
    loggedIn: isLoggedIn,
    url: window.location.href,
    title: document.title
  });
}
```

If not logged in, guide the user through one of:

**Option A — Import cookies** (recommended):
```
/setup-browser-cookies
```
Select `x.com` and `twitter.com` domains.

**Option B — Manual login**:
```
The browser is now open at x.com. Please log in to your X/Twitter account in the browser and type "done" when you're ready.
```

### 7. Validate Optional Seed Accounts

Only if the user provided seed accounts. For each account URL in the config, verify it resolves:

```bash
chrome-devtools navigate_page --url "https://x.com/<handle>"
```

Wait 3 seconds, then check:

```javascript
async () => {
  await new Promise(r => setTimeout(r, 3000));
  const errorText = document.body.innerText;
  const isError = errorText.includes("This account doesn't exist") || errorText.includes("No results");
  const profileName = document.querySelector('div[data-testid="UserName"]')?.innerText || '';
  return JSON.stringify({
    exists: !isError,
    profileName: profileName?.substring(0, 100) || '',
    url: window.location.href
  });
}
```

Remove any invalid accounts from the config.

### 7. Report Completion

```
✅ Twitter/X Research Setup Complete!

Project: .twitter-research/<timestamp>/
Research topic: <topic>
Minimum posts to explore: <N>
Seed accounts: <N> (<@handle1>, <@handle2>) — or none (pure topic search)
Target audience keywords: <keyword1>, <keyword2>, <keyword3>
Content format: <format>
Language: <language>
Chrome: ✅ ready
X login: ✅ logged in

Next step: skill twitter-research-scrape
```
