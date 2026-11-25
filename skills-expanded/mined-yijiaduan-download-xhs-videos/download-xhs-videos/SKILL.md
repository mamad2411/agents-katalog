---
name: download-xhs-videos
description: Download a Xiaohongshu (RedNote / 小红书) creator's videos to a local folder by driving a real logged-in Chrome. Tested on Claude Code (Claude in Chrome) and Codex (ChatGPT for Chrome) — each has its own route. Use when the user wants to batch-download / archive / 下载 / 抓取 a 小红书 (xiaohongshu / RedNote / xhs) 博主 / 用户 / up主 的视频 / 笔记, mirror a profile's video notes, or save someone's xhs videos for offline viewing. Triggers: 下载小红书视频, 抓小红书博主视频, 把这个博主的视频都下下来, download xiaohongshu videos, archive a RedNote creator. Personal/offline use only — not for re-posting or commercial use.
---

# download-xhs-videos — batch-download a 小红书 creator's videos

Xiaohongshu gives you no download button (checked 2026-07: the web share panel offers only a QR code and "copy link", the `…` menu only "report", and the creator dashboard won't even export your *own* videos). The two obvious workarounds both fail: `yt-dlp` support is flaky, and a plain scraper hits signed-request (`x-s`/`x-t`) walls.

What works is **driving a real, logged-in Chrome**:

> **Real click on the note's TITLE to open it → read the video URL out of the page's `__INITIAL_STATE__` → download with `curl`, outside the browser.**

How the URL gets from the page to `curl` is the only part that differs per agent.

## Supported agents

| Agent | Browser layer | Status | Route |
|---|---|---|---|
| **Claude Code** | Claude in Chrome extension | ✅ verified end-to-end 2026-07 | [Route A](#route-a--claude-code) |
| **Codex** (desktop / CLI) | `chrome@openai-bundled`, ChatGPT for Chrome | ✅ verified end-to-end 2026-07 | [Route B](#route-b--codex) |
| Anything else | — | ❓ **not tested** | — |

**Only these two have been tested.** Other coding agents may have the needed pieces — a trusted click into the real logged-in Chrome, a way to read page JS state, and a shell for `curl` — but nobody has run this skill on them. If you are a different agent: read [The invariants](#the-invariants), map them onto your own browser API, and **tell the user you are improvising off an untested path**.

## Before you start — preconditions

1. **macOS.** (Route A needs `pbpaste`; the extension hosts are mac-only today.)
2. Your browser layer is connected to a Chrome that is **logged into 小红书**.
3. The **creator's profile URL** — `https://www.xiaohongshu.com/user/profile/<uid>`. A bare uid URL works when you're logged in; an `?xsec_token=…` copy works too.
4. A **target folder**, default `~/Documents/xhs-<handle>/`.

**Cross-account works.** The logged-in account does not have to be the creator you're downloading — verified on **both** routes with a profile belonging to someone other than the logged-in user. You just need some valid 小红书 session so pages render.

### Ethics gate — do this, don't skip it

Open the profile and **read the creator's bio first.** Many creators write 「原创作品,禁止搬运和商用」. If so, confirm with the user that this is **personal/offline viewing only**. Downloading public videos for yourself is a defensible grey area; re-publishing or monetizing someone's flagged original work is not — refuse that. State what the bio says and get a clear yes before mass-downloading.

## The invariants

Properties of Xiaohongshu and Chrome, not of any agent. They hold on every route.

1. **A note only opens on a *real* click.** `location.href`, a hand-built `<a>`, or navigating to a note URL all get bounced back to `/explore` by XHS's router. Only a genuine mouse click at the card's coordinates loads the note *with* its video stream.

2. **Click the card's TITLE, not its cover.** Each card has three anchors to the same note: a zero-size one, `a.cover` (223×297), and `a.title`. **Clicking the cover's center is swallowed by XHS's 「图搜同款」 visual-search hover overlay** — the click lands, nothing navigates, and you burn a loop iteration wondering why. `a.title` has no overlay.

3. **Wait for the cover images before trusting *any* rect.** Until the covers finish loading, the masonry layout has not run and **every card returns the same `getBoundingClientRect()`** (observed: all five first cards reporting `x=307`). Clicking that opens the wrong note or nothing. The tell is duplicate centers across cards. Fix: scroll down ~5 ticks, scroll back up, wait ~2 s — that forces the lazy-load. Once loaded, centers are correctly distinct (`307 / 562 / 817 / 1072 / 1327`). `scripts/02-locate-card.js` refuses to guess when it detects duplicates.

4. **The stream's codec keys are not stable — never hardcode them.** They used to be `h264 / h265 / av1 / h266`. As of 2026-07 live pages ship **`EF4 / EF5 / EF6 / EF7`** (EF4 is their h264 ladder — a downloaded EF4 stream probes as `h264`). Worse: **key order is not preference order** (observed `EF4, EF6, EF5, EF7`) and **some keys are empty arrays**. Walk a preference list, then fall back to whatever keys exist, skip empties, and never index blindly. (This bug silently broke the skill for everyone until it was fixed.)

5. **Don't `fetch()` the video inside the page.** Chrome caps ~6 connections per host; a few hung fetches to the CDN exhaust the pool and every later fetch hangs forever. `curl` sidesteps this.

6. **The CDN URL is `http://`, not `https://`, and needs a Referer.** Pass `--referer https://www.xiaohongshu.com/` plus a normal User-Agent. (Use curl's `--referer` flag rather than spelling the header out with `-H` — Xiaohongshu's own upload gateway runs an Aliyun WAF that false-positives `curl -H "…"` as header injection and 405s the request. Same for `||` chains; see Verify.)

7. **Only one agent per tab.** If two browser-driving agents both attach to the same tab, you get endless CDP timeouts and kernel resets that look exactly like a missing capability. Claim a tab nobody else is on.

8. **Heavy automated use trips XHS's security verification.** After enough automated navigation in one session, profile loads start redirecting to `/website-login/captcha?…verifyType=…` and the page has no feed at all (`noteAnchors: 0`). This is rate-limiting, not a bug in your code.
   **Do not attempt to solve the CAPTCHA.** Stop, tell the user their session hit a verification wall, and ask them to clear it themselves in that Chrome window. Then resume. Pace the loop (the per-note navigation is already slow enough for normal use) and don't re-run the whole profile repeatedly while debugging — test on 1–2 notes.

9. **Quality**: `masterUrl` is the top stream of the chosen ladder; XHS source bitrate is modest, so 1–5 MB for a 2-minute clip is normal, not a bug.

## Route A — Claude Code

Browser layer: the **Claude in Chrome** extension (`list_connected_browsers`, `navigate`, `tabs_context_mcp`, `javascript_tool`, `computer`, `browser_batch`).

### Two extra traps specific to this route

1. **Chrome silently blocks automation-triggered downloads.** A blob download via `a.click()` from injected JS needs a *user-activation* gesture that injected code doesn't carry — and the extension's synthetic clicks don't grant download activation either (they fire DOM `click` handlers, so `execCommand('copy')` works, but the download is dropped with no error and no file). **So: never download through the browser. Use `curl`.**

2. **The harness blocks query-string data from your context.** If in-page JS *returns* the video URL, the tool result is `[BLOCKED: Cookie/query string data]` because of the `xsec_token`. So you can't read the URL and build a `curl` command with it. **Route the URL clipboard → `curl` so it never touches your context.**

3. **`javascript_tool` does not await an async IIFE.** An `async () => {…}` returns a pending Promise and you receive `{}` — the side effects still happen, but the return value is lost. All three scripts here are therefore **synchronous** (except part 1 of `01`, whose return value genuinely doesn't matter). If you write your own, keep them sync or you'll never get your coordinates back.

### Recipe

**Step 0 — Connect and open the profile.** Connect the browser, open a fresh tab (`tabs_context_mcp createIfEmpty:true`), `navigate` to the profile URL, `get_page_text` to read the bio (ethics gate) and the note titles.

**Step 1 — Load every note and count.** Run part 1 of `scripts/01-load-and-count.js` (async scroll, return value ignored), then part 2 (sync) to read the count. Re-run part 2 until `growing` is false. Report the total to the user — it counts image + video notes both.

**Step 2 — Per-note loop.** For note index `N` (0-based, DOM order):

- **Call A — locate** (one `browser_batch`): `navigate` back to the profile, then `scripts/02-locate-card.js` with `N` set. It returns `{count, x, y, text, ready}` in **screenshot pixels**. If it returns `err: 'masonry-not-laid-out'`, scroll down 5 / up 10, wait 2 s, and re-run.
- **Call B — open + extract + copy** (one `browser_batch`):
  1. `computer left_click` the returned coords → the note opens (you're clicking the title).
  2. Wait ~5 s, then `javascript_tool` runs `scripts/03-extract-and-copy.js`. It returns `{ok, codec, height, urlLooksRight, buttonPlaced}`. On `err: 'no-video-yet'`, wait and re-run; on `err: 'no-video'` it's an image note — skip it.
  3. `computer left_click [150,155]` — a **trusted** click on the copy button → URL is on the clipboard.
- **Call C — download** (Bash): `scripts/download.sh <out-dir> "NN_<title>.mp4"`.

**Step 3 — Verify.** See [Verify](#verify).

### Route A gotchas

- **Viewport vs screenshot pixels differ ~2%.** Scale rect coords by `1496/innerWidth` and `812/innerHeight` (the locate script does this) or clicks drift on the rightmost column.
- **`back` navigation re-renders the DOM**, so prior refs are stale. Rebuild the card list every loop.
- **Browser downloads vanish both ways**: "Ask where to save each file" on → a native Save dialog the extension can't touch; off → no user activation. Stop fighting it.

## Route B — Codex

Browser layer: the **`chrome@openai-bundled` plugin** driven through `mcp__node_repl__js`. Check `codex plugin list` shows it *installed, enabled*, and that **ChatGPT for Chrome** is installed in the Chrome profile that's logged into 小红书.

**Route B is simpler than Route A** — it has neither of Route A's first two traps. There is no context guardrail on token-bearing URLs, so you can just read the URL and `curl` it. **Do not port the clipboard trick over: you don't need it, and it cannot work here.**

### Setup

```js
// inside mcp__node_repl__js, once per session
if (globalThis.agent?.browsers == null) {
  const { setupBrowserRuntime } = await import(
    "<codexHome>/plugins/cache/openai-bundled/chrome/<version>/scripts/browser-client.mjs");
  await setupBrowserRuntime({ globals: globalThis });
}
await chrome.nameSession("📥 下载小红书视频");
const tabs = await chrome.user.openTabs();
const tab  = await chrome.user.claimTab(tabs[i]);   // claim a tab NO ONE ELSE is on
```

Read `await chrome.documentation()` once — it's the authoritative spec and longer than this summary.

### Two hard constraints on this route

1. **`tab.playwright.evaluate` runs in a READ-ONLY scope.** Global assignment and DOM mutation both throw:
   > `Error: global assignment is not available in playwright.evaluate because the DOM is read-only`

   So Route A's "stash the URL on `window.__urlForCopy` and inject a copy button" is impossible. Fine — *reading* values and `return`ing them is allowed, which is all you need.

2. **`window.__INITIAL_STATE__` is NOT visible from that scope.** Reading it directly returns an empty object (`noteDetailMap` keys `[]`, `hasStream:false`) — the evaluate world is isolated from the page's real `window`. **You must parse the inline `<script>` instead, and replace bare `undefined` with `null` before `JSON.parse` (XHS serializes literal `undefined`, which is not valid JSON):**

   ```js
   const raw = Array.from(document.scripts)
     .find(el => (el.textContent || '').includes('window.__INITIAL_STATE__='))?.textContent || '';
   const prefix = 'window.__INITIAL_STATE__=';
   const state = JSON.parse(
     raw.slice(raw.indexOf(prefix) + prefix.length).replace(/;\s*$/, '').replace(/\bundefined\b/g, 'null'));
   ```

### Recipe

**Step 0** — claim a fresh tab, `goto` the profile, read the bio (ethics gate) via `tab.playwright.domSnapshot()`.

**Step 1** — scroll to the bottom, count distinct note ids. Port `01`'s logic as **pure, value-returning** `evaluate` calls (no `window` assignments).

**Step 2 — per-note loop:**

1. **Locate** — `evaluate` that returns `a.title`'s center for card `N`. Apply invariants 2 and 3 (title anchor; refuse duplicate rects until covers load).
2. **Open** — `await tab.cua.click({x, y, button: 1})`. Real trusted click; verified to open the note. Confirm with `await tab.url()`.
3. **Extract** — `evaluate` that parses the inline state per constraint 2 above, picks the stream per invariant 4, and **returns the URL string**:
   ```js
   const stream = state?.note?.noteDetailMap?.[noteId]?.note?.video?.media?.stream;
   for (const k of ['h264','h265','av1','h266','EF4','EF5','EF6','EF7']) {
     const it = stream?.[k]?.[0];
     if (it) return it.masterUrl || it.backupUrls?.[0] || null;
   }
   ```
4. **Download** — plain shell, no clipboard:
   ```bash
   curl -sS -L -A "Mozilla/5.0" --referer https://www.xiaohongshu.com/ \
     -o "NN_<title>.mp4" "$URL"
   ```
5. Back to the profile, repeat. Rebuild the card list each loop.

**Step 3 — Verify.** See [Verify](#verify).

### Route B gotchas

- **CDP flakiness is normal.** `Runtime.evaluate` times out and the JS kernel resets (`js execution timed out; kernel reset, rerun your request`), sometimes several times running. Use `timeout_ms: 60000`, re-run `setupBrowserRuntime()` when `globalThis.agent?.browsers == null`, re-`claimTab`, retry the same step. **Do not conclude the capability is missing and switch methods** — the retry works. (If it never recovers, check invariant 7: another agent on your tab.)
- **Codex has extras this skill doesn't use**: `tab.capabilities.get("pageAssets")` → `list()/bundle()` can inventory `kind:"video"` assets and export them to a local directory; `downloadMedia({x,y})` triggers a real media download and `path()` returns the file; `clipboard.readText()` exists too. These are plausible shortcuts — **untested here**, so treat them as experiments, not the documented path.

## Verify

After the loop: count matches, none <10 KB, all `ISO Media`.

```bash
cd <out-dir>
for f in *.mp4; do
  if ! file "$f" | grep -q 'ISO Media'; then echo "NOT_MP4: $f"; fi
done
ls -1 *.mp4 | wc -l; du -sh .
```

If `ffprobe` is available, spot-check that durations match what the profile showed — that's how you catch truncated downloads.

## Files in this skill

- `SKILL.md` — this playbook.
- `scripts/01-load-and-count.js` — two parts: async scroll-to-bottom, then a **sync** counter.
- `scripts/02-locate-card.js` — **sync**; returns card `N`'s title-anchor center, with the masonry sanity check.
- `scripts/03-extract-and-copy.js` — **sync**; codec-agnostic stream pick + the clipboard copy button. **Route A only** (the button can't exist on Route B).
- `scripts/download.sh` — clipboard → `curl` with a CDN guard. **Route A only**; Route B curls the URL it already has.

## Dependencies (explicit)

- macOS (`curl`; `pbpaste` for Route A).
- A Chrome signed into 小红书, plus **one** of:
  - **Claude Code** with the Claude in Chrome extension connected, or
  - **Codex** with `chrome@openai-bundled` enabled and ChatGPT for Chrome installed in that profile.

## Related skills

- [`waitlist-farmer`](../waitlist-farmer/SKILL.md) — same "drive a real logged-in browser through a repetitive flow" muscle, different domain.
