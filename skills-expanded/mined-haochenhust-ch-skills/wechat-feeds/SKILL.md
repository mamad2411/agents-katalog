---
name: wechat-feeds
description: Maintain a local, incrementally-updated library of WeChat Official Account (公众号) articles as Markdown + a SQLite index, and pull new posts on demand. Use when the user wants to subscribe to 公众号, fetch/update 公众号 articles, build a searchable feed of specific accounts, or says "update my feeds" / "拉一下公众号" / "增量更新公众号文章". Bundles a self-contained Bun scraper (tool/) that drives a logged-in Chrome via a tiny CDP proxy.
allowed-tools: Bash, Read
---

# wechat-feeds

Build and maintain a local library of WeChat Official Account (微信公众号) articles. The bundled tool (`tool/`) logs into the 公众号 admin platform in your own Chrome, then pulls each subscribed account's article list and full text into `data/<account>/<date>-<title>.md`, with a SQLite index (`feeds.db`) for querying.

Two things this skill does:
1. **Set up / maintain the library** — install, log in, subscribe to accounts.
2. **Incrementally update** — pull new articles up to now (the `update-feeds` workflow below), including automatic session re-login handling.

## How it works (architecture)

```
CLI (bun, tool/src)  ──HTTP──▶  cdp-proxy.mjs  ──WebSocket(CDP)──▶  your Chrome (logged into mp.weixin.qq.com)
```

- The scraper never talks to WeChat directly. It asks the CDP proxy to run `fetch()` **inside a logged-in mp.weixin.qq.com tab**, so every request is same-origin and carries the real login cookie — no separate auth, no easy anti-crawl trip.
- Login state is a `token` (in `session.json`) plus the browser's cookie. The token expires often; the cookie lasts a few days. `refresh` re-derives the token from a still-valid cookie; when the cookie itself dies you re-login in the browser once.

## Prerequisites

- **Bun** (runs the CLI; uses `bun:sqlite`) — https://bun.sh
- **Node.js 22+ or Bun** (runs the CDP proxy; needs a global `WebSocket`)
- **Google Chrome** you can start with remote debugging
- A **WeChat Official Account** you can log into `mp.weixin.qq.com` with (any account works — the 图文素材 search reads other public accounts' published articles)

## One-time setup

All commands run from the `tool/` directory.

```bash
cd tool
bun install

# 1. Start Chrome with remote debugging (keep it running).
#    macOS:
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
#    Linux:   google-chrome --remote-debugging-port=9222
#    Windows: chrome.exe --remote-debugging-port=9222

# 2. Start the CDP proxy (separate terminal; keep it running).
node cdp-proxy.mjs        # or: bun cdp-proxy.mjs

# 3. Log in — opens the 公众号 login page; scan with WeChat.
bun run src/cli.ts login

# 4. Subscribe to accounts (by name or by a share link to one of their articles).
bun run src/cli.ts add 公众号名称
bun run src/cli.ts add https://mp.weixin.qq.com/s/xxxxx
bun run src/cli.ts list
```

Optional — wire login-expiry alerts to a channel of your choice (Feishu / Slack / email / desktop). When unset, the alert just prints to the console:

```bash
# macOS desktop notification example:
export WECHAT_FEEDS_NOTIFY_CMD='osascript -e "display notification \"$WECHAT_FEEDS_MSG\""'
```

## The `update-feeds` workflow

Incrementally update all subscribed accounts to now. Run the steps in order; **never do anything destructive** (don't clear cookies, don't log out).

### 1. Current time & pre-update baseline
- `TZ=Asia/Shanghai date '+%Y-%m-%d %H:%M'` — note current time.
- Latest article date already in the DB (the "before" baseline):
  ```bash
  cd tool && sqlite3 -readonly feeds.db "SELECT date(MAX(publish_time),'unixepoch','+8 hours') FROM articles WHERE fetched_at IS NOT NULL;"
  ```

### 2. Check the runtime
- CDP proxy healthy: `curl -s http://localhost:3456/health` → expect `"connected":true`. If no response, the proxy isn't running — start it (`node cdp-proxy.mjs`) and make sure Chrome is up with remote debugging.
- An mp tab exists: `curl -s http://localhost:3456/targets | grep -o 'mp.weixin.qq.com' | head -1`. If empty, open one and wait:
  ```bash
  curl -s "http://localhost:3456/new?url=https://mp.weixin.qq.com/" ; sleep 6
  ```

### 3. Run the incremental pull (background)
Pulls take a few minutes — run in the background from `tool/`:
- If the user passed args, pass them straight through: `bun run src/cli.ts pull <args>` (e.g. `--since=2026-05-01`).
- Otherwise default to the last ~two weeks (efficient; paging stops automatically once it reaches older articles):
  ```bash
  SINCE=$(TZ=Asia/Shanghai date -v-14d '+%Y-%m-%d'); bun run src/cli.ts pull --since=$SINCE
  ```
  (GNU `date`: `SINCE=$(date -d '14 days ago' '+%Y-%m-%d')`.)

### 4. Monitor output; handle re-login (the key step)
Track the background command's output:
- **If you see `🔗 登录链接已通知`**: the browser login has fully expired (the cookie died — happens roughly every few days; normal, not an error). This pull round skips every account. Re-login and re-run, in this order:
  1. Tell the user: open `https://mp.weixin.qq.com/` in the CDP-controlled Chrome (the one started with `--remote-debugging-port`) and log in (the browser usually remembers the account — often no QR scan needed).
  2. After they confirm login, **run `bun run src/cli.ts refresh` first** to sync the token (required — pulling with the old token gives `200040 invalid csrf token`). Wait for `✅ 刷新成功`.
  3. Then **re-run step 3's pull** with the same `--since` window. This time the session is valid and it pulls in full.
- **If no re-login notice appears**, the session is valid — just wait for the pull to finish (exit 0). Don't re-trigger pull while it's running.

### 5. Report
After the pull completes:
- Latest date & total now:
  ```bash
  sqlite3 -readonly feeds.db "SELECT date(MAX(publish_time),'unixepoch','+8 hours'), COUNT(*) FROM articles WHERE fetched_at IS NOT NULL;"
  ```
- Summarize new-article counts per account from the output.
- Report to the user: **updated from [before date] to [latest date], N new articles**, and list the accounts with the most additions.

## Reading the library

- **Markdown body**: `data/<account nickname>/<YYYY-MM-DD>-<title>.md` — YAML frontmatter (title/author/date/url/digest) + Markdown text.
- **SQLite index** (`feeds.db`): query what exists, who posted, when, and where the file is.

```sql
accounts(fakeid PK, nickname, alias, added_at)
articles(id PK, fakeid FK, title, url, author,
         publish_time,   -- Unix SECONDS  → datetime(publish_time,'unixepoch','+8 hours')
         fetched_at,     -- Unix MILLIS   → datetime(fetched_at/1000,'unixepoch','+8 hours'); NULL = metadata only, body not fetched
         file_path)
```

Use `fetched_at IS NOT NULL` to mean "body actually fetched" (more reliable than `file_path`).

## CLI reference

```
bun run src/cli.ts login              log into the 公众号 platform (QR)
bun run src/cli.ts add <name|url>     subscribe to an account
bun run src/cli.ts list               list subscriptions + article counts
bun run src/cli.ts pull               pull new articles (default max 100/account)
bun run src/cli.ts pull --today       only today's
bun run src/cli.ts pull --date=MM-DD  a specific date
bun run src/cli.ts pull --since=YYYY-MM-DD   from a date to now
bun run src/cli.ts pull --max=50      cap per account
bun run src/cli.ts pull --concurrency=6   accounts pulled in parallel (default 4; higher = faster but more rate-limit risk)
bun run src/cli.ts refresh            re-derive token from a live cookie
bun run src/cli.ts relogin            send a re-login alert (cookie fully dead)
bun run src/cli.ts keepalive          for a scheduler (cron/launchd): refresh, alert if dead
bun run src/cli.ts status             show login status
```

## Notes & red flags

- **Rate limits**: WeChat's `appmsgpublish` endpoint is frequency-controlled. The tool paces itself (per-article + per-page sleeps) and defaults to concurrency 4. Pushing concurrency high risks anti-crawl. If accounts start failing, lower it and re-run.
- **Accounts >14 days behind** may be missed by the default window — pass a wider `--since=YYYY-MM-DD`.
- **Keep the Chrome mp tab open** (can be minimized) — every API call runs inside it.
- **Nothing secret is committed**: `feeds.db`, `session.json`, `config.json`, and `data/` are gitignored. Your subscription list lives in `feeds.db`, not in source.
- **Use responsibly**: this drives your own logged-in session against WeChat's platform. Respect WeChat's Terms of Service, article copyright, and reasonable request rates. For personal reading/archival of accounts you follow.
```

