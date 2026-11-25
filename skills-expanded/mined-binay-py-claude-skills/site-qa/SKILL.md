---
name: site-qa
description: Crawl a website in a headless Chromium browser and produce a prioritized QA report — console errors, failed requests, broken images and links, mobile sideways-scroll, missing viewport/title/description/Open Graph tags, images without alt, unlabeled form fields, page weight and load time — with desktop and mobile screenshots. Use before handing a site to a client, after a deploy, or when asked "check my site / is anything broken".
---

# site-qa

`scripts/site-qa.mjs` is zero-dependency Node 22+. It launches its own headless Chrome / Edge / Brave / Chromium with a temporary profile, so it never touches the user's browser or logins. Set `BROWSER=/path/to/chrome` if none is found.

```
node site-qa.mjs https://example.com                     # up to 20 same-site pages
node site-qa.mjs https://example.com --max-pages 50 --out qa-report
node site-qa.mjs http://localhost:5173 --no-external      # skip outbound link checks
node site-qa.mjs https://example.com --keep-query          # treat ?a=1 and ?a=2 as different pages
```

Output in `--out` (default `qa-report/`): `report.md` (issues by severity, then a per-page table), `report.json`, `desktop.png` (1366×900) and `mobile.png` (390×844) of the start page.

## How to use the report
- Read `report.md` and LOOK at both screenshots. Many layout problems only show up visually.
- **High** = broken for users: page errors, JS exceptions, failed requests, broken images, broken links (to pages, same-site files like PDFs, and outbound), sideways scroll on mobile, no viewport tag. Fix these first.
- **Medium** = hurts reach or accessibility: missing description or Open Graph tags (plain WhatsApp/Facebook link previews), missing `<h1>`, images without alt, unlabeled inputs, pages over 3 MB or slower than 8 s.
- **Low** = polish: lang attribute, favicon, duplicate titles, tiny tap targets, empty links.
- "Link refused the checker" means the site blocks bots (LinkedIn, Instagram and others do). Check those by hand; they aren't proven broken.
- When fixing issues, re-run against the same URL to confirm. After a deploy, run it against the live URL, not localhost.

## Notes
- Each page loads twice, once at desktop and once at mobile size with a mobile user agent. Errors seen only on mobile are labeled as such.
- It crawls only same-origin links found in `<a href>`. Pages reachable only through JS navigation or forms won't be found. Pass their URLs as separate runs. If the start URL redirects (http → https, apex → www), the crawl follows the final origin.
- Linked same-site files (PDFs, images, feeds) are checked with a plain request, also under `--no-external`; up to 100 such and outbound links per run.
- It never submits forms or clicks buttons, so it's safe to run against production.
