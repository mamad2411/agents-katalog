---
description: Use whenever the user's message contains a URL, OR the user asks about content, docs, APIs, libraries, prices, dates, versions, or behavior that lives on the public web. Prevents stale-training-data answers by routing through specialized MCPs → WebFetch → Chrome MCP → Playwright, with a refusal-with-install-help fallback if no fetcher is available. Skip only when the URL is clearly incidental — the user is sharing a link to act on via another tool (gh CLI, linear MCP, etc.) rather than asking about its content.
---

# fresh-fetch

Stop answering web-content questions from stale training data. Always go to the source.

## When this skill applies

**Fire on:**
- Any URL in the user's message that they appear to be asking *about* (not just sharing)
- Any question about content, docs, APIs, libraries, prices, dates, versions, or behavior that lives on the public web — even with no URL in the message

**Skip on:**
- URL in a code block / fenced sample (it's code, not a question)
- URL is `localhost`, `127.0.0.1`, or a private IP — note "looks local, no fetch attempted" and continue
- User wants you to *act on* the URL via another tool (`open this PR`, `git push to <url>`, `query this linear ticket`) — use the action tool, not the fetcher
- URL was produced by *you* in a prior turn — don't infinite-loop on links you just printed

## The procedure

Run this top to bottom. Stop at the first step that succeeds.

### 1. In-session cache check

If you've already fetched this URL in the current session within the last 15 minutes (WebFetch's built-in cache window), reuse it.

Status line: `[fresh-fetch] <url> — cached Nm ago`

### 2. Specialized MCP

Scan the available tools list for an MCP that natively serves the URL's host. Match on capability suffix, **never** on the per-user server UUID prefix.

| URL host | Look for a tool matching |
|----------|--------------------------|
| `github.com` / `*.github.com` | `mcp__*github*` |
| `linear.app` | linear issue/doc tools (`mcp__*__get_issue`, `*__list_issues`, etc.) |
| `supabase.com/docs` | `*search_docs*` on a supabase server |
| `vercel.com/docs` | `*search_vercel_documentation*` |
| `render.com` | `mcp__*render*` |
| `slack.com` / `*.slack.com` | `mcp__*slack*` |
| (others) | grep for the host's brand name in the tool list |

If you find a match, use it. Status line: `[fresh-fetch] <url> — source: <mcp-server-name>`

If no specialized MCP matches, continue to step 3.

### 3. WebFetch

Call `WebFetch` with the URL and a prompt that extracts what the user actually needs.

- **Success** → Status line: `[fresh-fetch] <url> — source: WebFetch (fresh, Ts)`
- **Failure** (robots.txt, 403/4xx, "javascript required", auth wall) → continue to step 4

### 4. Chrome MCP

Check whether the Chrome MCP is installed. Use ToolSearch with query `claude-in-chrome` (or similar). If tools matching `mcp__*claude-in-chrome*` appear, load them, navigate to the URL, and extract the page content.

Status line: `[fresh-fetch] <url> — WebFetch failed (<reason>) → Chrome MCP`

If Chrome MCP is not available, continue to step 5.

### 5. Playwright

Check whether Playwright is installed *and* the chromium binary exists:

```bash
npx -y playwright --version 2>&1 | head -1
test -d "$(npx -y playwright install --dry-run chromium 2>&1 | grep -oE '/[^ ]+chromium[^ ]*' | head -1)" && echo "chromium present" || echo "chromium missing"
```

If both succeed, run a small inline extract script:

```bash
node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(process.argv[1], { waitUntil: 'networkidle', timeout: 30000 });
  console.log(await page.evaluate(() => document.body.innerText));
  await browser.close();
})();
" "<URL>"
```

Status line: `[fresh-fetch] <url> — source: Playwright`

If Playwright is not installed or chromium binary is missing, continue to step 6.

### 6. Refuse and offer install

Do **not** guess from training data. Print exactly:

```
[fresh-fetch] Could not fetch <url>.

WebFetch:    <actual reason: blocked by robots.txt | 403 | JS-only | timeout>
Chrome MCP:  not connected
Playwright:  not installed

I won't guess from training data — too high a chance of being wrong.

Options:

1. Chrome MCP — recommended; uses your existing Chrome session, handles
   auth/cookies/JS automatically.
   Install: visit https://claude.ai/chrome and follow the prompts to install
   the official Claude for Chrome extension (requires Pro/Team/Enterprise plan).

2. Playwright — headless, no auth state, works in CI.
   Install: npm install -g playwright && npx playwright install chromium

Reply "chrome" (after installing the extension, I'll wait for confirmation)
or "playwright" (I'll run the install for you with your OK).
```

Then wait.

- **"chrome"** → wait for the user to confirm the extension is installed, then restart this procedure from step 2.
- **"playwright"** → confirm before running (this is a risky action — global npm install + browser download). On user OK, run:
  ```bash
  npm install -g playwright && npx playwright install chromium
  ```
  Then restart this procedure from step 5.
- **"neither" / something else** → stop. Tell the user you can't proceed without a fetcher.

## Edge cases

| Case | Behavior |
|------|----------|
| Multiple URLs in one message | Run the procedure for each URL in parallel; one status line per URL |
| Auth-walled URL (Notion, Linear with no MCP, Figma, internal company tools) | WebFetch will fail with 401/403 — jump straight to Chrome MCP since only it has the user's session |
| PDF, image, or other non-HTML | Try WebFetch once. On failure, hand the URL back to the user with a note ("PDF — Chrome/Playwright won't help extract this; consider downloading it locally"). Do **not** escalate to browser fetchers for binary content. |
| URL produced by you in a prior turn | Skip — assume the user is referencing it, not asking about it |

## Status line format

Always one short line, then the answer. Never more, never less.

```
[fresh-fetch] react.dev/learn — source: WebFetch (fresh, 1.2s)
[fresh-fetch] github.com/foo/bar — source: github MCP
[fresh-fetch] notion.so/abc — WebFetch failed (auth wall) → Chrome MCP
[fresh-fetch] linear.app/team/X/issue/1 — cached 4m ago
```

The status line is required even when the fetch is trivial. It's how the user knows what just happened and gives them a chance to redirect.

## What this skill is not

- Not a screenshot tool — only text/markdown content extraction.
- Not a persistent cross-session cache — relies on WebFetch's existing 15-minute in-session cache.
- Not a replacement for action tools — if the user wants to push code, open a PR, or run a query through a connected MCP, use that tool instead of fetching the URL.
