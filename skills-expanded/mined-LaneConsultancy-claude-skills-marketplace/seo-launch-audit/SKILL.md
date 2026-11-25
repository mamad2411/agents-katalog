---
name: seo-launch-audit
description: >
  Fast pre-launch technical SEO gotcha checker. Runs a full sitemap crawl
  and returns a hard SHIP / SHIP WITH WARNINGS / DO NOT SHIP verdict.
  Catches staging robots.txt shipped to prod, noindex leftovers, canonical
  tags pointing to staging, www/non-www both live, mixed content, soft
  404s, missing OG tags, and redirect chains. Use when user says "launch
  audit", "pre-launch SEO", "go-live check", "SEO gotchas", "newly
  launched site", "check site launched correctly", or asks to verify a
  recently-deployed site. For deeper scored audits, use claude-seo:seo-technical.
user-invokable: true
argument-hint: "[url]"
allowed-tools:
  - Read
  - Write
  - Bash
  - WebFetch
---

# SEO Launch Audit

A pre-flight check for newly-launched websites. Every check returns PASS, WARN, or FAIL. The overall verdict is binary in spirit: if any check FAILs, the site is NOT ready to ship. This skill is deliberately strict — launch audits are about catching embarrassing go-live bugs, not negotiating scores.

**Not this skill's job:** deep technical audits (use `claude-seo:seo-technical`), Core Web Vitals scoring, schema validation (use `claude-seo:seo-schema`), accessibility audits.

---

## Procedure

### Step 1. Parse and normalize the URL

Accept the URL from the argument. Normalize:
- Add `https://` if missing
- Strip query strings and fragments
- Record both `www.` and non-`www.` variants for later comparison

Abort with a clear error if the URL is unreachable (see Error Handling below).

### Step 2. Detect available tools

Check which MCP tools are available before starting:

- **DataForSEO MCP** — prefer `mcp__dataforseo__api_request` with `method: "POST"`, `path: "/v3/on_page/instant_pages"`, `data: [{...}]`, and `noAiMode: true` for batch page analysis (status codes, redirect chains, on-page issues)
- **curl via Bash** — always available; use for robots.txt, sitemap, precise redirect/status checks, and as fallback when MCP isn't available

Note which tools were used in the report footer.

### Step 3. Fetch and parse robots.txt

```bash
curl -sSL -o /tmp/robots.txt -w "%{http_code}" https://<domain>/robots.txt
```

Parse for:
- HTTP status code (200 expected, 404 → WARN)
- Any `User-agent: *` block with `Disallow: /` → **FAIL: site blocks all crawlers** (classic staging-robots-shipped gotcha)
- `Sitemap:` directives — collect URLs
- AI crawler rules (informational, not scored here — belongs in `claude-seo:seo-technical`)

### Step 4. Discover and fetch sitemap(s)

Try in order:
1. Sitemap URLs from robots.txt
2. `/sitemap.xml`
3. `/sitemap_index.xml`

If sitemap is an index (contains `<sitemapindex>`), fetch each child sitemap and merge URL lists.

If no sitemap is found: emit WARN, and fall back to crawling homepage `<a href>` links (same-host only, dedupe) to build a URL list. Document this in the report.

### Step 5. Crawl every URL

**Full sitemap crawl** — do not sample. For each URL:

1. **Status + redirect chain** via parallel curl (use `xargs -P 20` or similar for speed):
   ```bash
   curl -sSLI -o /dev/null --max-time 15 -w "%{http_code}|%{url_effective}|%{num_redirects}\n" <url>
   ```
   Record status code, final URL, and redirect count. Flag `num_redirects > 1` as WARN.

2. **Fetch HTML** to a per-URL file (e.g., `/tmp/audit/html/<slug>.html`):
   ```bash
   curl -sSL --max-time 20 -o <file> <url>
   ```

3. **Parse HTML with Python's `html.parser`** — NOT regex/grep. Attribute values often contain apostrophes, quotes, HTML entities, and angle brackets inside JS, which break regex-based extraction and produce false positives (confirmed during skill development).

   Use this parser inline (save to `/tmp/tb_parse.py` or equivalent, then invoke):

   ```python
   import sys, hashlib
   from html.parser import HTMLParser

   class MetaExtractor(HTMLParser):
       def __init__(self):
           super().__init__()
           self.title_open = False
           self.title = ""
           self.canonical = ""
           self.robots = ""
           self.description = ""
           self.viewport = ""
           self.og = {}
           self.hreflang = []
           self.mixed_content = []
           self.h1_depth = 0
           self.h1_count = 0
           self.h1_texts = []
           self._h1_buf = ""

       def handle_starttag(self, tag, attrs):
           a = dict(attrs)
           if tag == "title":
               self.title_open = True
           elif tag == "h1":
               self.h1_depth += 1
               if self.h1_depth == 1:
                   self.h1_count += 1
                   self._h1_buf = ""
           elif tag == "link":
               rel = (a.get("rel") or "").lower()
               if rel == "canonical" and a.get("href"):
                   self.canonical = a["href"]
               elif rel == "alternate" and a.get("hreflang"):
                   self.hreflang.append((a["hreflang"], a.get("href", "")))
           elif tag == "meta":
               name = (a.get("name") or "").lower()
               prop = (a.get("property") or "").lower()
               content = a.get("content", "")
               if name == "robots":      self.robots = content
               elif name == "description": self.description = content
               elif name == "viewport":  self.viewport = content
               elif prop.startswith("og:"): self.og[prop] = content
           # Mixed content: http:// in src/href on (assumed) https page
           for attr in ("src", "href"):
               val = a.get(attr, "")
               if val.startswith("http://"):
                   self.mixed_content.append((tag, attr, val))

       def handle_data(self, data):
           if self.title_open:
               self.title += data
           if self.h1_depth > 0:
               self._h1_buf += data

       def handle_endtag(self, tag):
           if tag == "title":
               self.title_open = False
           elif tag == "h1":
               if self.h1_depth > 0:
                   self.h1_depth -= 1
                   if self.h1_depth == 0:
                       self.h1_texts.append(" ".join(self._h1_buf.split())[:200])
                       self._h1_buf = ""

   # Usage: python3 parse.py <url> <html_file>
   url, path = sys.argv[1], sys.argv[2]
   p = MetaExtractor()
   with open(path, "r", encoding="utf-8", errors="replace") as f:
       p.feed(f.read())
   # Output TSV: url \t canonical \t robots \t title \t desc_len \t og_title \t og_desc \t og_image \t viewport \t hreflang_count \t mixed_content_count \t h1_count \t first_h1
   print("\t".join([
       url, p.canonical, p.robots, p.title.strip(),
       str(len(p.description)),
       "Y" if p.og.get("og:title") else "N",
       "Y" if p.og.get("og:description") else "N",
       "Y" if p.og.get("og:image") else "N",
       "Y" if p.viewport else "N",
       str(len(p.hreflang)),
       str(len(p.mixed_content)),
       str(p.h1_count),
       (p.h1_texts[0] if p.h1_texts else ""),
   ]))
   ```

   Run it in parallel across all fetched HTML files (xargs -P 20). Collect results into a single TSV for analysis.

4. **Extract from each parsed row:**
   - `<link rel="canonical" href="...">` — flag if missing, empty, or not matching the page URL (allowing trailing slash + protocol match)
   - `<meta name="robots" content="...">` — flag if contains `noindex`
   - `<title>` — flag if empty or matches known defaults ("Home", "Untitled", "Page")
   - `<meta name="description">` — flag if empty (length 0) or suspiciously short (<50 chars) on non-tag/category pages
   - Open Graph triple: `og:title`, `og:description`, `og:image` — flag if any missing on the homepage
   - `<meta name="viewport">` — flag if missing
   - `<link rel="alternate" hreflang="...">` — validate codes if present
   - `<h1>` tag count — flag if 0 (no H1) or >1 (multiple H1s)
   - Mixed content: flag any `http://` in `src` or `href` on any page fetched over HTTPS

**Important parser notes:**
- Do NOT use `grep -oE 'content="[^"]+"'` or similar — it breaks on single quotes inside double-quoted attributes and vice versa, producing false "short description" or "missing canonical" WARNs.
- If `html.parser` fails on malformed HTML, fall back to `BeautifulSoup(html, "html.parser")` if available; otherwise flag the page as "could not parse" and continue.

**If DataForSEO MCP is available**, batch URLs via `mcp__dataforseo__api_request` using `method: "POST"`, `path: "/v3/on_page/instant_pages"`, `data: [{...}]`, and `noAiMode: true` for status/redirect checks (faster on large sites), but still use the Python parser for meta extraction — the DataForSEO response doesn't include every meta tag we need.

### Step 6. Run cross-domain checks (once per audit)

1. **HTTP → HTTPS redirect:**
   ```bash
   curl -sSL -o /dev/null -w "%{http_code} %{url_effective}\n" http://<domain>/
   ```
   Expect final URL to be `https://`. If not, FAIL.

2. **www vs non-www:** hit both `https://domain/` and `https://www.domain/`. Exactly one should return 200; the other should redirect (301) to the canonical variant. If both return 200 independently, FAIL.

3. **Trailing slash consistency:** pick 3 random sampled URLs. Try each with and without trailing slash. If both variants return 200 independently (no redirect between them), WARN.

4. **Soft 404 check:** request a URL that clearly doesn't exist (e.g., `/this-page-does-not-exist-<random>/`). Expect a 404 status. If it returns 200, WARN (soft 404).

5. **Favicon:** request `/favicon.ico` (or the URL declared in homepage `<link rel="icon">`). 4xx → WARN.

6. **IndexNow key file:** the key filename is a UUID chosen by whoever enabled IndexNow, so it can't be guessed directly. Check for indirect evidence instead:
   ```bash
   curl -sSL https://<domain>/ | grep -i indexnow
   curl -sSL https://<domain>/robots.txt | grep -i indexnow
   ```
   No hit on either → WARN. This is a "best effort" check, not a guarantee of absence: a site can have IndexNow enabled (e.g. via Cloudflare's IndexNow toggle) without any of these traces. Note the limitation in the report.

7. **Bing Places claim:** cannot be checked via HTTP at all. Word this as a manual confirmation item in the report rather than an automated check. Ask the user to confirm the business is claimed on Bing Places (bing.com/places). Unconfirmed → WARN. Matters because ChatGPT's live web search runs on Bing's index, so a site optimised only for Google is invisible to it. See `~/.agents/skills/references/shared-seo/local-seo-playbook-2026.md` (Part 6) for background.

### Step 7. Classify every finding

**FAIL — launch blockers (site is broken or invisible):**

| Check | FAIL condition |
|---|---|
| robots.txt | Missing, or `User-agent: *` with `Disallow: /` |
| Page status | Any sitemap URL returns 4xx or 5xx |
| Meta robots | Homepage or any sampled page has `noindex` |
| Canonical tag | Points to a non-production host (staging, localhost, `http://` on an HTTPS site, different domain) |
| HTTPS | HTTP does not redirect to HTTPS, invalid/expired cert, or mixed content on homepage |
| www/non-www | Both variants return 200 with no redirect between them |
| Sitemap | Missing when site has >1 page, malformed XML, or any listed URL 404s |

**WARN — ship-but-fix (ugly but not invisible):**

| Check | WARN condition |
|---|---|
| Redirect chain | Any page has >1 redirect hop, or a redirect loop |
| Soft 404 | Non-existent URL returns 200 instead of 404 |
| Title | Missing, empty, default ("Home", "Untitled"), or duplicated across >3 pages |
| Meta description | Missing on homepage or >20% of sampled pages |
| Open Graph | `og:title`, `og:description`, or `og:image` missing on homepage |
| H1 tag | Page has zero `<h1>` tags (missing page headline), or more than one `<h1>` tag (ambiguous headline; common CMS/theme bug). Report the offending URL and H1 text(s). |
| Viewport | `<meta name="viewport">` missing |
| Favicon | 404 on expected path |
| Trailing slashes | Both `/page` and `/page/` return 200 independently |
| hreflang | Invalid language codes, missing return tags, or self-reference missing (multilingual sites only) |
| Sitemap in robots.txt | Sitemap exists but not referenced in robots.txt |
| robots.txt | 404 (not strictly required but recommended) |
| IndexNow | No evidence of an IndexNow key file or integration found (e.g. Cloudflare's IndexNow toggle) |
| Bing Places | Business not confirmed as claimed on Bing Places (manual confirmation item, cannot be checked via HTTP) |

**PASS** — check ran and no issue found.

### Step 8. Write the report

Always write to `seo-reports/launch-audit-YYYY-MM-DD.md` in the current working directory. Use today's date. Create the `seo-reports/` directory if it doesn't exist.

Use this template exactly:

```markdown
# Launch Audit: <domain>

**Date:** YYYY-MM-DD
**URL audited:** https://<domain>/
**Verdict:** <SHIP | SHIP WITH WARNINGS | DO NOT SHIP>
**Summary:** X FAIL, Y WARN, Z PASS

## Verdict

<One-line verdict with reason. Examples:>
<- DO NOT SHIP — 3 blocking issues must be fixed before go-live.>
<- SHIP WITH WARNINGS — no blockers, but 5 issues should be fixed soon.>
<- SHIP — all launch-critical checks passed.>

---

## FAILs (fix before launch)

### 1. <Short issue title>
- **What:** <concrete finding>
- **Where:** <URL or file path>
- **Likely cause:** <e.g., staging robots.txt shipped to production>
- **Fix:** <concrete remediation>
- **Evidence:**
  ```
  <curl command output or response excerpt>
  ```

<repeat for each FAIL>

---

## WARNs (fix soon, not blocking)

### 1. <Short issue title>
<same structure as FAILs>

---

## PASSed checks

- robots.txt: accessible, not blocking all crawlers
- HTTPS: enforced with valid certificate
- www/non-www: one variant redirects to the other
- Sitemap: found at <path>, valid XML, all URLs reachable
- <etc — compact one-line entries>

---

## Pages crawled

| URL | Status | Redirects | Canonical | noindex? |
|---|---|---|---|---|
| /                 | 200 | 0 | self | no |
| /services/        | 200 | 0 | self | no |
| <etc>             |     |   |      |    |

---

## Audit metadata

- **Tools used:** <curl | DataForSEO MCP + curl>
- **Pages crawled:** N
- **Sitemap source:** <URL or "fell back to homepage link crawl">
- **Duration:** Xs
```

### Step 9. Print terminal summary

After writing the report, emit a brief terminal summary:

```
Launch audit complete for <domain>.
Verdict: <VERDICT>
<X FAIL, Y WARN, Z PASS>
Report: seo-reports/launch-audit-YYYY-MM-DD.md
```

If verdict is DO NOT SHIP, list the FAIL titles inline (one per line) so the user sees them without opening the report.

---

## Error Handling

| Scenario | Action |
|---|---|
| URL unreachable (DNS fail, connection refused, timeout) | Emit FAIL with the connection error. Abort audit. Do not write a report. |
| Invalid URL format | Reject at step 1 with a clear error message. Do not proceed. |
| No sitemap found | WARN. Fall back to crawling homepage `<a href>` links (same-host only) to build URL list. Note in report. |
| robots.txt returns 404 | WARN (not a blocker — robots.txt is optional). Continue. |
| DataForSEO MCP unavailable | Silently use curl. Note "Tools used: curl" in report footer. |
| Individual page returns 5xx | Record as FAIL for that page. Continue auditing remaining URLs. |
| Cert expired or invalid | FAIL under HTTPS category. Continue with `-k` to complete remaining checks, but note the cert issue prominently. |
| Sitemap is malformed XML | FAIL. Fall back to homepage link crawl with a note. |
| Very large site (>500 URLs) | Warn the user in the terminal before starting: "This site has N URLs — full crawl will take ~M minutes. Proceeding…" Continue — no sampling. The user asked for full crawl. |

---

## Key principles

1. **Default to strict.** A launch audit that says "looks good" when something's wrong is worse than no audit. When in doubt, FAIL.
2. **Evidence over assertion.** Every FAIL and WARN must include a concrete evidence snippet (curl output, response header, HTML excerpt). No hand-waving.
3. **Don't negotiate.** Binary verdict. "DO NOT SHIP" doesn't become "SHIP WITH WARNINGS" because the user pushes back. If the user disagrees, they can fix the issue or override manually — the skill's job is to call it.
4. **Fast is a feature.** This runs at go-live time. Don't stall on optional enhancements when curl will do the job.
