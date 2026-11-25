---
name: chrome-extension
description: |
  Drive the Claude Chrome extension from the CLI via Puppeteer and Chrome DevTools Protocol.
  Gives Claude Code browser agent capabilities — browse the web, check social media,
  fill forms, read pages, anything the Chrome extension can do, triggered from the terminal.
  Requires one-time setup: bind mount + Chrome with remote debugging.
allowed-tools:
  - Bash
  - Read
  - Write
---

# Chrome Extension Browser Agent

Drive the Claude Chrome extension from Claude Code to perform browser tasks.
Use when you need to browse the web, check social media, fill forms, read pages,
or do anything that requires a real browser session with the user's logged-in accounts.

## One-time setup

Requires `puppeteer-core`:

```bash
cd /tmp && npm install puppeteer-core
```

Chrome needs to run with remote debugging enabled on your real profile. A bind mount
is required because Chrome refuses to enable debugging on the default profile path:

```bash
mkdir -p /tmp/chrome-bind-profile
sudo mount --bind ~/.config/google-chrome /tmp/chrome-bind-profile
```

Then close Chrome and relaunch:

```bash
pkill -f google-chrome; sleep 2
rm -f /tmp/chrome-bind-profile/SingletonLock /tmp/chrome-bind-profile/SingletonSocket /tmp/chrome-bind-profile/SingletonCookie
google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-bind-profile --restore-last-session &
```

Verify it's working:

```bash
curl -s http://localhost:9222/json/version | head -1
```

## Usage

Check if Chrome is ready before running:

```bash
curl -s http://localhost:9222/json/version | head -1
```

If it's not running, tell the user to run the setup commands above.

### Send a task to the Chrome extension

```javascript
const puppeteer = require('puppeteer-core');
const EXT_ID = 'fcoeoabgfenejglbffodgkkbkcdhcgfn';

const browser = await puppeteer.connect({ browserURL: 'http://localhost:9222', defaultViewport: null });

// Get a valid tabId (required for API communication)
const sw = (await browser.targets()).find(t => t.url().includes(EXT_ID) && t.type() === 'service_worker');
const worker = await sw.worker();
const tabs = await worker.evaluate(async () => {
  const all = await chrome.tabs.query({});
  return all.map(t => ({ id: t.id, url: t.url }));
});
const tabId = tabs.find(t => !t.url.includes('sidepanel'))?.id;

// Open side panel (or reuse existing)
const pages = await browser.pages();
let panel = pages.find(p => p.url().includes('sidepanel'));
if (!panel) {
  panel = await browser.newPage();
  await panel.goto(`chrome-extension://${EXT_ID}/sidepanel.html?tabId=${tabId}`, { waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 3000));
}

// Prevent Chrome from throttling the panel (it's a background tab)
const client = await panel.createCDPSession();
await client.send('Emulation.setFocusEmulationEnabled', { enabled: true });
await client.send('Page.setWebLifecycleState', { state: 'active' });

// Set up CDP network interception for structured API responses
await client.send('Network.enable');

const apiResponses = [];
const pendingRequests = new Map();

client.on('Network.requestWillBeSent', (params) => {
  if (params.request.url.includes('api.anthropic.com/v1/messages')) {
    const body = JSON.parse(params.request.postData || '{}');
    if (body.max_tokens > 128) { // skip title-generation calls
      pendingRequests.set(params.requestId, { model: body.model, messageCount: body.messages?.length });
    }
  }
});

client.on('Network.loadingFinished', async (params) => {
  if (pendingRequests.has(params.requestId)) {
    try {
      const resp = await client.send('Network.getResponseBody', { requestId: params.requestId });
      const raw = resp.body;
      if (raw.startsWith('event:')) {
        // SSE streaming response — parse each event
        for (const event of raw.split('\n\n').filter(Boolean)) {
          const dataLine = event.split('\n').find(l => l.startsWith('data: '));
          if (!dataLine) continue;
          try { apiResponses.push(JSON.parse(dataLine.slice(6))); } catch(e) {}
        }
      } else {
        apiResponses.push(JSON.parse(raw));
      }
    } catch(e) {}
    pendingRequests.delete(params.requestId);
  }
});

// Send a task (with duplicate guard)
const task = 'YOUR TASK HERE';
const alreadySent = await panel.evaluate((t) => {
  const userBubbles = document.querySelectorAll('.flex.justify-end.group .bg-bg-300');
  for (const m of userBubbles) {
    if (m.innerText.trim().substring(0, 80) === t.substring(0, 80)) return true;
  }
  return false;
}, task);

if (alreadySent) {
  console.log('Task already sent — skipping to poll phase');
} else {
  await panel.click('.tiptap.ProseMirror');
  await panel.evaluate((t) => {
    const editor = document.querySelector('.tiptap.ProseMirror');
    editor.focus();
    document.execCommand('insertText', false, t);
  }, task);
  await panel.evaluate(() => {
    document.querySelector('button[aria-label="Send message"]')?.click();
  });
}

// Wait for completion (poll Stop button + DOM stability)
let prevText = '';
for (let i = 0; i < 60; i++) {
  await new Promise(r => setTimeout(r, 3000));
  const running = await panel.evaluate(() => !!document.querySelector('button[aria-label="Stop"]'));
  const text = await panel.evaluate(() => {
    const msgs = document.querySelectorAll('.claude-response');
    return msgs.length ? msgs[msgs.length - 1].innerText : '';
  });
  if (!running && text.length > 20 && text === prevText) break;
  prevText = text;
}

// Read structured conversation
const conversation = await panel.evaluate(() => {
  const messages = [];
  const container = document.querySelector('.flex-1.flex.flex-col.px-4');
  if (!container) return messages;
  for (const child of container.children) {
    const userBubble = child.querySelector('.bg-bg-300');
    if (userBubble) { messages.push({ role: 'user', text: userBubble.innerText.trim() }); continue; }
    const claudeResp = child.querySelector('.claude-response');
    if (claudeResp) { messages.push({ role: 'assistant', text: claudeResp.innerText.trim() }); continue; }
  }
  return messages;
});

// apiResponses has raw API JSON (stop_reason, usage, tool calls)
// conversation has the clean per-message text from the DOM
console.log(JSON.stringify({ conversation, apiResponses }, null, 2));

await client.detach();
await browser.disconnect();
```

## Key details

- **Extension ID**: `fcoeoabgfenejglbffodgkkbkcdhcgfn`
- **Text input**: Must use `document.execCommand('insertText')`. Puppeteer's `keyboard.type()` doesn't work with ProseMirror/TipTap contenteditable.
- **Send button**: `button[aria-label="Send message"]`
- **Stop button**: `button[aria-label="Stop"]` — present while the extension is working.
- **tabId is required**: Without it in the URL, the extension loads but can't call the API.
- **Reuse the panel**: Check for an existing sidepanel page before opening a new one.
- **The extension browses in real tabs**: It opens and navigates Chrome tabs. The user's browser is actively used.
- **Prevent throttling**: The panel opens as a background tab. Chrome throttles it unless you call `Emulation.setFocusEmulationEnabled` + `Page.setWebLifecycleState('active')` via CDP. Without this, the extension stalls until the user manually focuses the tab.
- **Protocol timeouts ≠ task failure**: If `panel.evaluate()` times out during polling, the extension may still be working. Never resend without checking if the task is already in the conversation history. The duplicate guard handles this.

## Reading responses

Two complementary methods, both shown in the code above:

**DOM extraction** — structured conversation by role:
- User messages: `.flex.justify-end.group .bg-bg-300` (the chat bubble)
- Assistant messages: `.claude-response`
- Walk children of `.flex-1.flex.flex-col.px-4` in order to get the conversation sequence

**CDP Network interception** — raw API events:
- The extension calls `https://api.anthropic.com/v1/messages?beta=true` for each turn
- Listen on `Network.requestWillBeSent` + `Network.loadingFinished`, then `Network.getResponseBody`
- Responses are SSE streams (`event: ...` / `data: {...}`), not plain JSON. Parse by splitting on `\n\n` and extracting `data:` lines.
- Key event types: `message_start` (model, id), `content_block_start` (tool calls), `message_delta` (stop_reason, usage)
- Filter out title-generation calls (Haiku, max_tokens=128)

Use DOM for the final answer text. Use network interception when you need to know *why* the extension stopped (error vs completion vs tool use) or what it did between turns.

## Why bind mount?

Chrome requires `--user-data-dir` to be a non-default path for remote debugging. But changing
the profile path breaks Chrome's Secure Preferences HMAC, which silently disables extensions.
A symlink doesn't work either. A bind mount makes the same directory (same inodes) available
at a second path, passing both Chrome's path check and its HMAC validation.
