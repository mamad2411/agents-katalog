---
name: index-on-search-engine
description: >-
  Register a (new) website or subdomain on Google + Bing so it gets crawled and
  indexed, using the claude-in-chrome browser against Ivan's already-logged-in
  Google Search Console and Bing Webmaster Tools. Use when the user asks to
  "index this on Google/Bing/Brave", "register on search console", "submit the
  sitemap", "get this site indexed", "why isn't my site on Google", "set up
  search engine indexing", or after launching a new site/subdomain under
  websites/. Covers the live-and-crawlable prerequisite check, GSC domain-property
  coverage, Bing site-add + HTML-meta-tag verification (via a redeploy), sitemap
  submission, per-URL request-indexing, the Brave reality, and the auth/OAuth
  safety boundaries. Pairs with geo-audit (AI-search visibility) and the
  marketing-skills:ai-seo strategy skill.
---

# Index a site on search engines (Google + Bing)

Playbook for getting a freshly-launched site/subdomain crawled and indexed. Verified end-to-end on `kids.aitraining.id` (2026-06-27). Do it through the **claude-in-chrome** browser, which uses Ivan's logged-in accounts.

## 0. Prerequisite — the site must be live AND crawlable

Indexing is impossible if crawlers can't reach a clean 200. Before touching any webmaster tool, verify from the shell (use `dangerouslyDisableSandbox: true` for curl):

```bash
curl -s -I https://SITE/            # must be HTTP 200 (not 302→SSO, not connection-closed)
curl -s -I https://SITE/ | grep -i x-robots-tag      # must be EMPTY (no noindex header)
curl -s https://SITE/ | grep -oiE '<meta[^>]*robots[^>]*>'   # must NOT contain noindex
curl -s https://SITE/robots.txt     # AI/search bots Allowed, sitemap line present
curl -s -o /dev/null -w '%{http_code}' https://SITE/sitemap.xml   # 200
```

Gotchas:
- **Vercel**: the auto-generated per-deployment URLs (`*-hash-*.vercel.app`) carry deployment-protection (302 → `vercel.com/sso-api`) AND `noindex`. The **production custom domain** does not. Always test the real domain, not a deploy URL.
- A "connection closed" / no-DNS error means the domain isn't wired yet — fix DNS/domain attachment first (Cloudflare CNAME `sub` → `cname.vercel-dns.com`, DNS-only/grey-cloud), then come back.

## 1. Google Search Console

Browser: `https://search.google.com/search-console`. Ivan is logged in.

- **Check the property type first.** `aitraining.id` is a **Domain property** (`resource_id=sc-domain:aitraining.id`). A domain property **auto-covers every subdomain** (kids.aitraining.id, www, etc.) — no new property, no new verification. Just use it.
- **Submit the sitemap**: left nav → Sitemaps → "Add a new sitemap" → enter the **full** sitemap URL (`https://SUB.domain/sitemap.xml`, full URL works under a domain property) → Submit. Expect "Sitemap submitted successfully".
- **Request indexing (fastest single-page nudge)**: top "Inspect any URL" bar → paste the page URL → Enter → wait ~5s → **REQUEST INDEXING** → wait ~10s for the live test → "Indexing requested, added to priority crawl queue".

If the site is NOT under an existing domain property: add a new property. Prefer the **Domain** type (one TXT record in Cloudflare covers all subdomains) — but that needs DNS access. The URL-prefix type + HTML-tag verification (same meta-tag trick as Bing below) is the no-DNS fallback.

## 2. Bing Webmaster Tools

Browser: `https://www.bing.com/webmasters/home`. **Bing has no "domain property" concept** — every subdomain is its own site and needs its own verification.

1. Site dropdown (top-left) → **Add a site**. Two methods appear:
   - **Import from GSC** (left) — easy but triggers a Google **OAuth grant** to Microsoft. Treat that as explicit-permission territory; default to manual.
   - **Add manually** (right) — enter `https://SUB.domain/` → Add. **Use this.**
2. **Verify via HTML Meta Tag** (the method you control without DNS):
   - The modal shows `<meta name="msvalidate.01" content="CODE" />`. Zoom to read CODE exactly.
   - Add it to the site in code. **Next.js App Router**: in `layout.tsx` `metadata`, add
     ```ts
     verification: { other: { "msvalidate.01": "CODE" } },
     ```
     (renders the exact meta tag). **Leave it in permanently** — removing it un-verifies the site.
   - Redeploy (`vercel --prod --yes`), then `curl -s https://SUB.domain/ | grep msvalidate` to confirm it's live, THEN click **Verify**.
3. **Submit sitemap**: left nav → Sitemaps → "Submit sitemap" → full sitemap URL → Submit (status goes "Processing").
4. **Request indexing**: URL Inspection → paste URL → Inspect → **switch to the "Live URL" tab** → "Request indexing" → Submit (daily quota ~100 URLs).

### Bing gotcha — stale "Indexing allowed? No"
The **"Bing Index"** tab reflects Bing's last *cached* crawl. If you just (re)deployed, it can wrongly say "Indexing allowed? No" from a mid-deploy fetch. **Don't panic** — verify the live site has no noindex (section 0), then use the **"Live URL"** tab, which fetches fresh. "URL can be indexed by Bing" + "No SEO/GEO issues found" = you're fine. Then request indexing.

## 3. Brave

No submission tool / webmaster console. Brave runs its own crawler plus some Bing. It picks sites up via **inbound links + Google/Bing presence**. The lever: add internal links from already-indexed sibling sites (e.g. footer link on aitraining.id + aurelivan.com → the new site). That's the single biggest organic discovery accelerator anyway — do it for all three engines.

## 4. Safety boundaries (do NOT cross)
- Never enter passwords, complete 2FA, solve CAPTCHAs, or create accounts. If a tool shows "Sign in", **stop and ask the user to log in themselves**, then retry.
- Granting cross-service OAuth/SSO (e.g. Bing "Import from GSC") is explicit-permission territory — prefer the manual + meta-tag path that needs no grant.
- Sitemap submission, URL inspection, and request-indexing inside an already-logged-in console are the authorized core actions.

## 5. Expectations
Submitting ≠ indexed. After submission, `site:SUB.domain` typically returns nothing for **days to ~2 weeks**. Re-check `site:` on Google/Bing/Brave later (the geo-audit / ai-seo skills cover ongoing visibility). Record launch + submission state in memory (see `kids-aitraining-launch` for the template).
