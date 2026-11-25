---
name: web-product-rebrand
description: Rebrand cloned web apps or audit old-brand leaks.
version: 1.0.0
author: Me
license: MIT
metadata:
  hermes:
    tags: [rebrand, whitelabel, brand-audit, grep, pm2]
    related_skills: [publish-site, cloudflare-temporary-deploy]
---

# Web Product Rebrand & Audit

## When to Use
Use when a cloned/white-label web app needs rebranding, or when asked to verify a completed rebrand has no original-brand leaks (titles, OG, manifest, footer, console watermarks).

Rebrand a cloned web app or verify a finished rebrand: every user-facing surface (title, OG, manifest, footer, console watermark, file/branch names) must carry the new brand. Work text-first with grep, never trust a visual screenshot scan.

## Audit procedure (does the rebrand leak the original brand?)

1. `grep -rhi "<title>" public/*.html` — list all `<title>` tags, check each for old brand set.
2. `grep -rli <newbrand> public/ | wc -l` **and** `grep -rli <newbrand> public/` — count + list files carrying new brand (index, dashboard, login, manifest, sw.js all count).
3. In each HTML file: `<meta property="og:title">`, `<title>`, footer `&copy;`/brand div, manifest `name`/`short_name`, `sw.js`.
4. Console watermarks live in `js/*.js`, shown via `console.log('%c...')` — grep for old brand in JS too.
5. Overall leak check: `grep -rli <oldowner> public/ index.js` where `<oldowner>` = previous owner's handle/domain strings.

## Pitfalls
- pm2 process name may differ from folder name (`exsalapi` vs `Exsalaapi`). Identify by pid — `pm2 list` (%CPU/mem) matches `ss -tlnp` — never assume process name equals directory name.
- Grep hits on `original`, `data-original-value`, `originalIndex` are generic scrambling/debug vars — NOT brand leaks. Skip lines where the term is a JS variable.
- `grep -i` on brand keyword catches the term inside words/URLs/comments — filter; only references to the brand identity count.
- `grep -li` returns file list — also run the count version to scale the check (18 files vs 5 titles).

## Finish-report format
Maintainer-style summary: what was found (counts + files), server status (pm2 name, uptime, port via `ss -ltnp`), git head (log -1). Ask before additional changes; confirm what remains — never assume "done" for a rebrand you did not run.
