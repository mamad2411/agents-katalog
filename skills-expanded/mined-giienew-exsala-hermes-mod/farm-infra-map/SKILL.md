---
name: farm-infra-map
description: "Use when farming accounts: map tempmail, CF bypass, proxy."
---

# Farm Infra Map (verified 2026-10-21)

Operator wants: when ordered to farm, use ALL already-available infra. This skill maps what exists on disk. Paths below are VERIFIED.

## Proxy pools
- `~/app/premium_proxies.txt` — **PREMIUM pool (200 proxies, 2026-10-21), 2 creds sets (c88pa77mj24b / fzlgy72eo60s), format `user:pass@host:port`** ← DEFAULT pool
- `~/app/proxies.txt` — format `user:pass@host:port` (no scheme)
- `~/app/farms/oxylabs/valid_proxies.txt` — format `http://user:pass@host:port`
- `~/app/farms/oxylabs/valid_proxies_live.txt` — verified live (9 proxies)
- `~/app/farms/dahl/proxies.txt` — dahl farm pool
- `~/app/farms/thc/proxies.txt` — thc farm pool
- `~/app/proxies_9router.txt` — 9router pool
- `~/app/proxies9.txt` + `proxies.txt` — solver pool
- scheme autodetect: `user:pass@host:port` → `http://`

Proxy-rotation: never retry a dead port — skip to next line. Per-account sticky IP. Load balancing round-robin.

## CF bypass (anti-bot)
- `~/app` — anti-detect browser (Camoufox)
- `~/app` — CF challenge solver (Docker, node, port?) — `docker compose up` sejak worker?
- `~/app` — cloudscraper node, scrape CF-protected pages
- `~/app` — GTM/Turnstile solver; has `auto_check.py`, `cf_frame_*.html`, `proxies9.txt`; anti-bot

## Tempmail — Exsala API (verified live 2026-10-21, key=`gionova14`)
Base URL: `https://api.your-provider.com`
- V1: `GET /api/tools/tempmail/create?apikey=KEY` → `data.email`, `data.token`; inbox: `GET /api/tools/tempmail/inbox?token=X&apikey=KEY`
- V2: `GET /api/tools/tempmail-v2/create?apikey=KEY` → `data.email`, `data.token`; inbox: `GET /api/tools/tempmail-v2/inbox?token=X&apikey=KEY`
- V3: `GET /api/tools/tempmail-v3/create?apikey=KEY` → `data.email`, `data.token`; inbox: `GET /api/tools/tempmail-v3/inbox?token=X&apikey=KEY`; read: `GET /api/tools/tempmail-v3/read?token=X&id=EMAIL_ID&apikey=KEY`
All inbox return `data.total` + `data.emails`. ALL endpoints need `apikey=`. The `url_inbox` returned by create does NOT include apikey — must append.

**Turnstile bypass:** `GET /api/tools/bypass/turnstile?sitekey=SITEKEY&url=<urlencoded>&apikey=KEY` → `data.token` (solved=true). Live verified on getcontact example.

**VERIFY key before use**: `gionova14` is correct; `adminexsala14` was wrong. Test with a create call first.

## Tempmail — Worker (verified live 2026-10-21)
Base: `http://tempmail.ayogiakbar.cv` (Cloudflare Worker `me-agent.web.id` domain)
- `GET /generate` → `{"email":"xyz@me-agent.web.id"}`
- `GET /inbox?email=X` → `{"email":..., "count":N, "messages":[...]}`
- `GET /latest?email=X` → `{"email":..., "messages":[...]}`
- `GET /otp?email=X` → `{"email":..., "otp":...}`
Worker does NOT need apikey. Used when sites accept `.web.id` captures.

## Gmail — Dot-trick + IMAP inbox (operator, verified setup)
- `~/farming/gmaildot.js` — CLI read Gmail via IMAP app password. Args: `--email`, `--password`, `-inbox`, `-create` (dot-trick gen), `--search subject:OTP`, `--json`, `--body`. Deps: `node`, npm pkg `imap` + `mailparser` (installed in ~/farming).
- Config: `~/farming/gmaildot.config.json` → `{email:"you@gmail.com", password:"brxc fxhl pcvq utne"}` (verified live 2026-10-21 — IMAP OK, 10.866 emails)
- App password (operator): `brxc fxhl pcvq utne`
- Key fact: dot-trick (`.`) variants all land in SAME inbox — thousands of near-unique addresses from one Gmail. `--create`/`--dottrick` generates 12-15 per base. Chain: generate variant → target signup uses variant → check OTP on base Gmail via `node gmaildot.js -inbox -s "subject:OTP" --json`.
- Run from `~/farming/`.

## When operator says "farming" (revised wiring)
1. Check infra map (this skill) — use existing tools, don't build from scratch.
2. Pick tempmail (exsala API, key=gionova14, version by target block), pick proxy pool, pick CF/turnstile solver if target has anti-bot.

## Account farming
- `~/web-account-farm/` — existing harness: `farm.py` (pipeline: mailbox→browser→target signup, dry-run + live), `playbook.py` (demo fns on example.com), `config.json`, `accounts.json` output. Run: `python3 farm.py --target demo --count N --proxies pool.txt --proxy-mode rotate`. Targets in `TARGETS` dict; need real signup URL + selectors + anti-bot vendor per target.
- Skill `farm/web-account-farming` (HTTP vs anti-bot) is active.
- Skill `farm/firecrawl-account-farming` active for firecrawl targets.

## When operator says "farming"
1. Check infra map (this skill) — use existing tools, don't build from scratch.
2. Pick tempmail (operator-provided), pick proxy pool, pick CF/turnstile solver if target has anti-bot.
3. Run from `~/web-account-farm/`.
4. Save results to `accounts.json` only on success.
