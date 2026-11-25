---
name: browser-use-cloud
description: Use Browser Use Cloud API v3 for managed AI browser automation, live browser sessions, screenshots, web research, form workflows, authentication profiles, file workspaces, and OpenClaw/Hermes browser tasks. Trigger whenever Charles asks Browser Use, cloud browser automation, web task agents, AI browser API, live browser preview, profile sync, or CDP stealth browser infrastructure.
---

# Browser Use Cloud

Use Browser Use Cloud when a task needs managed browser automation rather than local Playwright/Chrome. It can run natural-language agent tasks, return structured output, provide live browser previews, reuse sessions, use profiles/cookies, and connect through Browser Use's cloud browser infrastructure.

## What This Skill Does

This skill Use Browser Use Cloud API v3 for managed AI browser automation, live browser sessions, screenshots, web research, form workflows, authentication profiles, file workspaces, and OpenClaw/Hermes browser tasks. Trigger whenever Charles asks Browser Use, cloud browser automation, web task agents, AI browser API, live browser preview, profile sync, or CDP stealth browser infrastructure.

## First Moves

1. Read the current docs index first when exact behavior matters:
   - `https://docs.browser-use.com/cloud/llms.txt`
   - Full reference: `https://docs.browser-use.com/cloud/llms-full.txt`
2. Use API v3 only. Browser Use v2 is legacy and uses different method names.
3. Load the API key from env; never paste it into logs or prompts.
4. Send the key only to:
   - `https://api.browser-use.com`
   - `https://cloud.browser-use.com`

## Runtime Env

Hermes host:

```bash
set -a
. /root/.hermes/browser-use.env
set +a
```

OpenClaw container:

```bash
set -a
. /data/.openclaw/workspace/.secrets/browser-use.env
set +a
```

The expected variable is `BROWSER_USE_API_KEY`. Optional defaults:

```bash
export BROWSER_USE_MODEL=claude-sonnet-4.6
```

## Quick Commands

Hermes host:

```bash
/root/.hermes/skills/browser-use-cloud/scripts/browser-use-task.sh "Go to example.com and summarize the page"
```

OpenClaw container:

```bash
/data/.openclaw/workspace/skills/browser-use-cloud/scripts/browser-use-task.sh "Go to example.com and summarize the page"
```

The helper creates an API v3 session, polls until completion, and prints safe JSON containing status, output, live URL, screenshot URL, recording URLs, and cost fields. Do not paste secrets into the task text.

## API Pattern

For one-shot tasks, create a session with a task:

```bash
curl -sS -X POST https://api.browser-use.com/api/v3/sessions \
  -H "X-Browser-Use-API-Key: $BROWSER_USE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"task":"Find the top story on Hacker News","model":"claude-sonnet-4.6"}'
```

Poll:

```bash
curl -sS https://api.browser-use.com/api/v3/sessions/$SESSION_ID \
  -H "X-Browser-Use-API-Key: $BROWSER_USE_API_KEY"
```

Terminal states include `idle`, `stopped`, `error`, and `timed_out`; `output` is populated when the agent finishes.

## SDK Pattern

Python:

```python
from browser_use_sdk.v3 import AsyncBrowserUse

client = AsyncBrowserUse()
result = await client.run("List the top 20 posts on Hacker News today with their points")
print(result.output)
```

TypeScript:

```ts
import { BrowserUse } from "browser-use-sdk/v3";

const client = new BrowserUse();
const result = await client.run("List the top 20 posts on Hacker News today with their points");
console.log(result.output);
```

Install or upgrade only when needed:

```bash
pip install --upgrade browser-use-sdk
npm install browser-use-sdk@latest
```

## When To Use What

- Use `client.run()` or `/api/v3/sessions` for natural-language browser tasks.
- Reuse `session_id` for follow-up tasks that need the same browser state.
- Use profiles when login/cookies must persist.
- Use workspaces/files when the agent needs uploads or creates downloadable files.
- Use live URL/recording when Charles wants to watch or review a browser run.
- Use local Playwright/Chrome instead when the task is purely local, already authenticated in desktop Chrome, or should not spend Browser Use cloud credits.

## Safety

- Never reveal or echo `BROWSER_USE_API_KEY`.
- Do not use Browser Use for payments, irreversible account changes, sensitive credential entry, or bulk sends without explicit approval.
- Prefer a cheap smoke task before relying on a new profile/workspace.
- Stop sessions that are no longer needed.
- Keep final answers practical: include task result, public/live URL when useful, and any cost/status fields returned by the API.

See [references/browser-use-cloud.md](references/browser-use-cloud.md) for the compact reference and official docs links.
