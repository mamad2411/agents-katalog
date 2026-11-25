---
name: twitter-x-scraping
description: Use when scraping public Twitter/X timelines or lists through Nitter-style mirrors with axios and Playwright fallback, including anti-bot challenge handling and pagination limits.
---

# Skill: Scraping Nitter.net for Tweets

This codebase scrapes [nitter.net](https://nitter.net) — an open-source Twitter frontend — to collect tweets from a list or profile within a time window. The technique works without a Twitter API key.

## Core Methodology

### 1. URL Structure

Nitter mirrors Twitter's URL layout:

| Target | Nitter path |
|--------|------------|
| Twitter List | `/i/lists/<listId>` |
| User Profile | `/<handle>` |
| Paginated | append `?cursor=<cursor>` |

### 2. Fetch Strategy: axios → Playwright fallback

Start with plain HTTP (`axios`). If nitter serves an anti-bot challenge page (detected by the string `"Verifying your request"` in the HTML), permanently switch to a headed Playwright/Chrome session for the rest of the run.

```ts
// challengeSolver.ts — detect challenge
const CHALLENGE_MARKER = 'Verifying your request';
export function isChallengePage(html: string): boolean {
  return html.includes(CHALLENGE_MARKER);
}

// scrapeNitterList.ts — switch modes on detection
if (isChallengePage(html)) {
  useBrowserMode = true;
  const browserHtml = await fetchWithBrowser(url, debug);
  return { html: browserHtml, url };
}
```

### 3. Browser Anti-bot Bypass

When challenge is detected, launch a real system Chrome (not headless) with automation signals suppressed:

```ts
import { chromium } from 'playwright';

const browser = await chromium.launch({
  channel: 'chrome',
  headless: false,
  args: ['--disable-blink-features=AutomationControlled'],
});

const context = await browser.newContext({ locale: 'en-US' });
await context.addInitScript(() => {
  Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
});

const page = await context.newPage();
await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });

// Wait for challenge to auto-resolve
await page.waitForSelector('.timeline-item', { timeout: 30000 });
const html = await page.content();
```

**Key**: reuse a single browser/page instance across all subsequent fetches (singleton pattern) — don't re-launch per page.

### 4. Retry Logic with Backoff

For HTTP 429 / 502 / 503, retry up to 10 times with exponential backoff (2s base, max 60s), respecting `Retry-After` and `X-Rate-Limit-Reset` headers:

```ts
const maxRetries = 10;
const baseDelayMs = 2000;

for (let attempt = 0; attempt <= maxRetries; attempt++) {
  const res = await axios.get(url, {
    headers: FETCH_HEADERS,
    timeout: 30000,
    validateStatus: (s) => (s >= 200 && s < 400) || s === 429 || s === 502 || s === 503,
  });

  if (res.status === 429 || res.status === 502 || res.status === 503) {
    const ra = res.headers['retry-after'];
    if (ra && /^\d+$/.test(ra)) {
      await sleep(Math.min((parseInt(ra) + 2) * 1000, 5 * 60 * 1000));
      continue;
    }
    const jitter = Math.floor(Math.random() * 250);
    const waitMs = Math.min(baseDelayMs * Math.pow(2, attempt) + jitter, 60_000);
    await sleep(waitMs);
    continue;
  }

  if (res.status === 200) return res.data;
}
```

Use a browser-like User-Agent header:
```ts
const FETCH_HEADERS = {
  'User-Agent': 'Mozilla/5.0 (compatible; MyBot/1.0) Node.js',
  'Accept-Language': 'en-US,en;q=0.9',
  'Accept': 'text/html,application/xhtml+xml',
  'Accept-Encoding': 'gzip, compress, deflate, br',
};
```

### 5. HTML Parsing with Cheerio

Nitter renders server-side HTML. Parse it with `cheerio` (jQuery-like API):

```ts
import * as cheerio from 'cheerio';

const $ = cheerio.load(html);

// All tweets on the page
const $items = $('.timeline .timeline-item').filter((_, el) =>
  $(el).find('.tweet-body').length > 0
);

$items.each((_, el) => {
  const $el = $(el);

  // Tweet URL and ID
  const href = $el.find('a.tweet-link').first().attr('href'); // e.g. "/user/status/12345"
  const id = href?.match(/status\/(\d+)/)?.[1];

  // Timestamp — from the `title` attribute of the date link
  const title = $el.find('.tweet-date a').attr('title'); // e.g. "Apr 15, 2026 · 10:00 AM UTC"
  const timestamp = new Date(title?.replace(/\s*[·•]\s*/g, ' ') ?? '');

  // Tweet text
  const text = $el.find('.tweet-content.media-body').text().trim();

  // Author
  const username = $el.find('.tweet-header a.username').attr('title');
  const displayName = $el.find('.tweet-header a.fullname').attr('title');

  // Images
  $el.find('.attachments .attachment.image').each((_, img) => {
    const src = $(img).find('img').attr('src');  // relative URL
    const fullSrc = `https://nitter.net${src}`;
  });

  // Engagement stats
  $el.find('.tweet-stats .tweet-stat').each((_, stat) => {
    const icon = $(stat).find('.icon-container > span').attr('class') ?? '';
    const n = parseInt($(stat).text().replace(/\D/g, '') || '0');
    if (icon.includes('icon-heart')) console.log('likes:', n);
    if (icon.includes('icon-retweet')) console.log('retweets:', n);
  });

  // Is a retweet?
  const retweetedBy = $el.find('.retweet-header').text().trim() || undefined;

  // Quoted tweet
  const $quote = $el.find('.quote').first();
  if ($quote.length) {
    const quoteText = $quote.find('.quote-text').text().trim();
    const quoteUser = $quote.find('.tweet-name-row a.username').text().trim();
  }
});
```

### 6. Cursor-Based Pagination

Nitter exposes a "show more" link with a `?cursor=` param:

```ts
function findNextCursor($: cheerio.CheerioAPI): string | undefined {
  const href = $('div.show-more a').last().attr('href') ?? '';
  const m = href.match(/[?&]cursor=([^&]+)/);
  return m ? decodeURIComponent(m[1]) : undefined;
}

// In the pagination loop:
let cursor: string | undefined;
while (pagesFetched < maxPages) {
  const url = `https://nitter.net/i/lists/${listId}${cursor ? `?cursor=${encodeURIComponent(cursor)}` : ''}`;
  const html = await fetchPage(url);
  const $ = cheerio.load(html);
  // ... parse tweets ...
  const next = findNextCursor($);
  if (!next) break;
  cursor = next;
}
```

### 7. Date-Bounded Stopping

Stop pagination as soon as the oldest non-retweet on a page is older than `startDate`, avoiding unnecessary fetches:

```ts
// After parsing all tweets on a page:
const oldestNonRTMs = Math.min(
  ...pageTweets.filter(t => !t.retweetedBy).map(t => t.timestampMs)
);

if (oldestNonRTMs < startDate.getTime()) {
  console.log('Reached tweets older than start date; stopping.');
  break;
}
```

***

## Quick-Start: Minimal End-to-End Example

```ts
import axios from 'axios';
import * as cheerio from 'cheerio';

const LIST_ID = '1585430245762441216';
const BASE = 'https://nitter.net';
const HEADERS = {
  'User-Agent': 'Mozilla/5.0 (compatible; MyBot/1.0) Node.js',
  'Accept': 'text/html,application/xhtml+xml',
};

async function scrapeListPage(cursor?: string) {
  const url = `${BASE}/i/lists/${LIST_ID}${cursor ? `?cursor=${encodeURIComponent(cursor)}` : ''}`;
  const res = await axios.get(url, { headers: HEADERS, timeout: 30000 });
  const $ = cheerio.load(res.data);

  const tweets: { id: string; text: string; timestamp: string }[] = [];

  $('.timeline .timeline-item').filter((_, el) =>
    $(el).find('.tweet-body').length > 0
  ).each((_, el) => {
    const $el = $(el);
    const href = $el.find('a.tweet-link').first().attr('href') ?? '';
    const id = href.match(/status\/(\d+)/)?.[1] ?? href;
    const title = $el.find('.tweet-date a').attr('title') ?? '';
    const timestamp = new Date(title.replace(/\s*[·•]\s*/g, ' ')).toISOString();
    const text = $el.find('.tweet-content.media-body').text().trim();
    tweets.push({ id, text, timestamp });
  });

  const nextHref = $('div.show-more a').last().attr('href') ?? '';
  const nextCursor = nextHref.match(/[?&]cursor=([^&]+)/)?.[1];

  return { tweets, nextCursor: nextCursor ? decodeURIComponent(nextCursor) : undefined };
}

async function main() {
  let cursor: string | undefined;
  let allTweets: { id: string; text: string; timestamp: string }[] = [];

  for (let page = 0; page < 5; page++) {
    const { tweets, nextCursor } = await scrapeListPage(cursor);
    allTweets.push(...tweets);
    console.log(`Page ${page + 1}: +${tweets.length} tweets (${allTweets.length} total)`);
    if (!nextCursor) break;
    cursor = nextCursor;
    await new Promise(r => setTimeout(r, 1000)); // polite delay
  }

  console.log(JSON.stringify(allTweets, null, 2));
}

main();
```

***

## Empirical Findings (Apr 2026)

### Instance Selection

`nitter.net` itself is often up but **headless Playwright returns "Oh noes!" (rate-limited/blocked)**. Always use `headless: false` or `channel: 'chrome'`. Working instances confirmed Apr 15 2026:

| Instance | Status |
|----------|--------|
| `nitter.tiekoetter.com` | ✅ reliable, used successfully |
| `nitter.privacyredirect.com` | ⚠️ TLS timeout |
| `nitter.catsarch.com` | ✅ listed as up |
| `xcancel.com` | ✅ listed as up |
| `nitter.net` | ✅ up but may block headless |

Check live status at: **https://status.d420.de/**

Build a priority list and auto-fallback. Accept an instance as valid only after `.timeline-item` is found in DOM, not just by page title:

```ts
const ok = await page.waitForSelector('.timeline-item', { timeout: 10000 })
  .then(() => true).catch(() => false);
// Don't trust page.title() — error pages can spoof it
```

### Headless Always Fails

Nitter instances actively detect headless Chromium and return a blank/error page. **Always use `headless: false`** (or `channel: 'chrome'` which implies headed). The `--disable-blink-features=AutomationControlled` arg and `navigator.webdriver` override are also necessary:

```ts
const browser = await chromium.launch({
  headless: false, // REQUIRED — headless gets blocked
  args: ['--disable-blink-features=AutomationControlled'],
});
await context.addInitScript(() => {
  Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
});
```

### Pagination: Cursor URL Construction

The `div.show-more a` href is a **relative URL** like `?cursor=DAA...`. Do NOT construct `baseUrl + href` naively — the correct form is:

```ts
// ✅ correct
const nextUrl = `${baseUrl}/${handle}${nextHref}`; // nextHref starts with "?"

// ❌ wrong — this double-encodes or drops the path
const nextUrl = new URL(nextHref, baseUrl).href;
```

Verify by logging the constructed URL before `page.goto()`.

### Timestamp Parsing

The `.tweet-date a` element has two useful attributes:
- `title` — **full absolute date**: `"Apr 14, 2026 · 5:47 PM UTC"` — always use this for cutoff comparisons
- `textContent` — **relative display**: `"19h"` or `"Apr 14"` — unreliable for parsing

The `·` separator is a Unicode middle dot (`\u00B7`), not ASCII. Split on it:

```ts
const datePart = title.split('·')[0].trim(); // "Apr 14, 2026 "
const date = new Date(datePart); // reliable
```

Do not try to parse `"19h"` — if `title` is missing, skip or don't cutoff on that tweet.

### Pinned Posts

The first `.timeline-item` is often a **pinned post** that can be years old, causing a false early cutoff. Skip it:

```ts
const isPinned = item.classList.contains('pinned') ||
  !!item.querySelector('.pinned-icon, .icon-pin');
if (isPinned) continue;
```

Also: check the **oldest non-pinned** tweet's date for the cutoff, not just the oldest tweet.

### Avatar Scraping (No Auth)

The CSS selector reference lists `.tweet-header a.tweet-avatar img.avatar[src]` — **use this instead of unavatar.io** to get avatars directly from Nitter without a third-party service:

```ts
const avatarSrc = $el.find('.tweet-header a.tweet-avatar img.avatar').attr('src');
// Returns a relative path like /pic/pbs.twimg.com%2F...
// Decode it:
const avatarUrl = avatarSrc
  ? 'https://pbs.twimg.com/' + decodeURIComponent(avatarSrc.replace('/pic/', '').replace('pbs.twimg.com%2F', ''))
  : undefined;
```

Or just store the Nitter-proxied URL: `${instance}${avatarSrc}` (will break if instance changes).

**Avoid `unavatar.io/twitter/<handle>`** — it 301-redirects to `/x/<handle>` and has a low anonymous daily rate limit (hits quickly when backfilling many users). Use it only as a fallback when Nitter avatar is unavailable.

### Tweet Author URL Points to Original on Retweets

On a retweet, `a.tweet-link href` points to **the original author's tweet** (e.g. `/originalAuthor/status/123`), not `/@swyx/status/...`. This is what you want for linking to the source. Extract the author from the href:

```ts
const authorMatch = href.match(/^\/([^/]+)\/status/);
const author = authorMatch?.[1]; // original author's handle
```

***

## Dependencies

```json
{
  "axios": "^1.7.2",
  "cheerio": "^1.0.0",
  "playwright": "^1.58.2"
}
```

Install Playwright browsers once: `npx playwright install chrome`

***

## CSS Selector Reference

| Data | Selector |
|------|----------|
| Tweet container | `.timeline .timeline-item` (filter: has `.tweet-body`) |
| Tweet link / ID | `a.tweet-link[href]` → extract `/status/(\d+)/` |
| Timestamp | `.tweet-date a[title]` |
| Tweet text | `.tweet-content.media-body` |
| Author username | `.tweet-header a.username[title]` |
| Author display name | `.tweet-header a.fullname[title]` |
| Avatar | `.tweet-header a.tweet-avatar img.avatar[src]` |
| Images | `.attachments .attachment.image img[src]` |
| Videos | `.attachments .gallery-video img[src]` (poster) |
| Link card | `.card a.card-container[href]` |
| Likes | `.tweet-stat span.icon-heart` → sibling text |
| Retweets | `.tweet-stat span.icon-retweet` → sibling text |
| Replies | `.tweet-stat span.icon-comment` → sibling text |
| Quote tweets | `.tweet-stat span.icon-quote` → sibling text |
| Retweet banner | `.retweet-header` (non-empty = is a retweet) |
| Quoted tweet block | `.quote` |
| Quoted text | `.quote .quote-text` |
| Next page cursor | `div.show-more a[href]` → extract `?cursor=` |
