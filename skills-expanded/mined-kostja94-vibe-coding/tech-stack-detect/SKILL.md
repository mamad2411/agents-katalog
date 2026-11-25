---
name: tech-stack-detect
description: Detect a website's complete technology stack through 8-layer analysis — HTTP headers, cookies, robots.txt, DNS records, HTML source, JavaScript globals, network requests, and SSL certificates. Identifies frameworks, CMS, hosting, CDN, analytics, payment, auth, and email providers behind any URL.
when_to_use: Use when the user asks what tech stack a website uses, what framework or CMS powers a site, wants to analyze a competitor's technology choices, or pastes a link asking "what is this built with?" / "这个网站用的什么技术栈".
license: Proprietary
compatibility: Requires curl or PowerShell Invoke-WebRequest, nslookup, and network access. Layers 6-7 require a browser automation tool (e.g., Playwright MCP); skip them gracefully if unavailable.
metadata:
  author: harness-engineering
  version: "1.0.0"
allowed-tools: Bash(curl:*) Bash(nslookup:*) Read WebFetch
---

# Tech Stack Detection

Analyze a website's technology stack through eight detection layers. Start with Layer 1–5 (fast, shell + web fetch only, no browser), then escalate to Layer 6–7 (browser-based) for deep JS and network analysis. Report confidence per finding.

The layered order matters: each layer is cheaper than the next, and earlier layers often make later ones unnecessary. Do not jump to the browser before exhausting the fast layers — most stacks are fully identified by L1+L2+L3+L5 in under 10 seconds.

## Execution Order (Mandatory)

```
1. L1: HTTP Response Headers (shell)
2. L2: Cookies from Set-Cookie header (same L1 request, zero extra cost)
3. L3: robots.txt (one web fetch)
4. L4: DNS records MX/TXT/NS (shell — nslookup)
5. L5: HTML Source + Meta Tags (web fetch)
6. L6: JS Globals + Version Extraction (browser_navigate + browser_evaluate)
7. L7: Network Requests (browser_network on → reload → off → read captures)
8. Report: Structured output with categories and confidence
```

All signature tables live in the `references/` directory, split by category:

- [references/signatures.md](references/signatures.md) — L1-L4 (headers / cookies / robots.txt / DNS) + L6-L8 (JS reference / network / SSL)
- [references/signatures-platforms.md](references/signatures-platforms.md) — L5 platforms: frameworks, CMS, ecommerce, page builders, AI builders, WP plugins
- [references/signatures-services.md](references/signatures-services.md) — L5 third-party services: marketing, analytics, chat, payment, compliance, etc.
- [references/csp-mining.md](references/csp-mining.md) — CSP domain → service mapping
- [references/ai-builder-fingerprints.md](references/ai-builder-fingerprints.md) — AI builder / vibe-coding platform fingerprints (which platforms are detectable and which are fundamentally not)

Consult the relevant file while interpreting each layer's raw output — do not guess from memory.

## Layer 1: HTTP Response Headers

Fetch response headers with the shell. On Windows PowerShell:

```powershell
$r = Invoke-WebRequest -Uri "TARGET_URL" -UseBasicParsing
$r.Headers.GetEnumerator() | % { "$($_.Key): $($_.Value)" }
```

On Unix/Mac:

```bash
curl -sI -L TARGET_URL
```

Match the output against the header table in [references/signatures.md](references/signatures.md#layer-1-http-response-headers) — it maps `X-Powered-By`, `Server`, `X-Vercel-Id`, `CF-Ray`, and similar headers to frameworks and platforms.

### CSP Mining

The `Content-Security-Policy` header is a free technology roster: a strict CSP must whitelist every external domain the page loads scripts, styles, fonts, and API calls from, so it inadvertently lists the site's third-party dependencies. Parse each directive (`script-src`, `connect-src`, `img-src`, `font-src`, `frame-src`) and match domains against [references/csp-mining.md](references/csp-mining.md). Confidence is **High** — CSP is authoritative, and `connect-src` often reveals backend services invisible in the DOM.

## Layer 2: Cookies (from Set-Cookie)

Examine `Set-Cookie` headers from the same L1 response — no extra request needed. Platform cookies (`wp-settings-`, `_shopify_`, `laravel_session`, `connect.sid`, `__stripe_mid`, `_ga`) are high-confidence signals. Full pattern table: [references/signatures.md](references/signatures.md#layer-2-cookies).

## Layer 3: robots.txt

Fetch `TARGET_URL/robots.txt`. Distinctive `Disallow` paths reveal frameworks (`/wp-admin/` → WordPress, `/_next/` → Next.js, `/_nuxt/` → Nuxt.js). A `Sitemap:` line is a bonus — it gives you a URL inventory for deeper analysis. Pattern table: [references/signatures.md](references/signatures.md#layer-3-robotstxt).

## Layer 4: DNS Records (MX / TXT / NS)

Query DNS with the shell:

```powershell
nslookup -type=MX TARGET_DOMAIN
nslookup -type=TXT TARGET_DOMAIN
nslookup -type=NS TARGET_DOMAIN
```

MX records identify the email provider (Google Workspace, Microsoft 365, Cloudflare Email Routing, 腾讯企业邮箱). TXT records reveal domain verifications (Search Console, Stripe, Meta, Atlassian). NS records identify the DNS host (Cloudflare, Route 53, GoDaddy). Pattern tables: [references/signatures.md](references/signatures.md#layer-4-dns-records).

## Layer 5: HTML Source + Meta Tags

Fetch the page HTML (via web fetch, or `browser_get` with the `text` selector if a browser session is already open) and scan for framework signatures, meta tags, CSS framework classes, and third-party script sources. Key markers: `__NEXT_DATA__` → Next.js, `data-v-` attributes → Vue, `ng-version` → Angular, `wp-content/` → WordPress, `cdn.shopify.com` → Shopify. Full tables split by category:

- **Platforms** (frameworks, CMS, ecommerce, page builders, AI builders, WP plugins): [references/signatures-platforms.md](references/signatures-platforms.md)
- **Third-party services** (marketing, analytics, chat, auth, payment, compliance, etc.): [references/signatures-services.md](references/signatures-services.md)

## Layer 6: JS Globals + Version Extraction

Requires a browser automation tool. Navigate to the URL, wait for load, then read [scripts/detect-js-globals.js](scripts/detect-js-globals.js) and run its entire content with `browser_evaluate`. It extracts framework versions (React, Next, Vue, Angular, jQuery), framework globals, CMS and ecommerce platforms, marketing/analytics pixels, social auth, page builders, cookie compliance tools, JS libraries, payment/auth providers, PWA status, and build tool hints in one JSON payload. If the result is too large, split it into two evaluations: versions+framework+cms+ecommerce first, then the remaining groups.

If no browser tool is available, skip this layer and note the gap in the report — do not fabricate version numbers.

## Layer 7: Network Request Analysis

Requires a browser automation tool with network capture:

1. Start capture (`browser_network on`)
2. Reload the page (`browser_reload`)
3. Wait ~3 seconds (`browser_wait 3000`)
4. Stop capture (`browser_network off`)
5. Get the capture directory (`browser_network path`)
6. Read the capture files in the returned directory

Match request URLs against the network pattern table in [references/signatures.md](references/signatures.md#layer-7-network-request-analysis) — it identifies App Router vs Pages Router chunk paths, tRPC/GraphQL endpoints, Supabase/Firebase backends, headless CMS calls, and analytics beacons.

## Layer 8: SSL/TLS Certificate (Optional)

Only when hosting is still unclear after L1–L7. On PowerShell:

```powershell
$r = Invoke-WebRequest -Uri "TARGET_URL" -UseBasicParsing; $r.BaseResponse.ServerCertificate.Subject
```

On Unix/Mac:

```bash
openssl s_client -connect TARGET_HOST:443 -servername TARGET_HOST 2>/dev/null | openssl x509 -noout -issuer -dates
```

Issuer CN maps to platforms (Let's Encrypt → self-hosted, Amazon → AWS ACM, Cloudflare Inc → Cloudflare proxy). Table: [references/signatures.md](references/signatures.md#layer-8-ssltls-certificate).

## Reporting

Produce the final report using the exact structure in [references/report-template.md](references/report-template.md): a summary table (Category / Technology / Version / Confidence / Detected By) followed by per-layer raw findings.

Confidence rules:

- **High**: confirmed by 2+ independent layers (e.g., L1 header + L5 HTML marker + L2 cookie)
- **Medium**: single strong signal (e.g., L5 HTML marker only)
- **Low**: circumstantial (e.g., CSS class pattern without JS confirmation)

Never inflate confidence. A guess labeled Low is useful; a guess labeled High is misinformation.

## Quick Scripts

For L1+L2 in one shot, use the bundled scripts:

- `scripts/detect-quick.ps1 <url>` — PowerShell: headers + cookies + CSP extraction
- `scripts/detect-quick.sh <url>` — Bash equivalent

These cover the two cheapest layers; continue with L3–L5 manually.

## Cost Reference

| Layer | Tool | Cost | When to Run |
|-------|------|------|-------------|
| L1 Headers | Shell | <2s | Always first — CSP is a free service roster |
| L2 Cookies | Shell | 0s | Always (rides on L1) |
| L3 robots.txt | Web fetch | <2s | Always |
| L4 DNS | Shell | <3s | For org-level info (email, verification) |
| L5 HTML | Web fetch | <5s | Always |
| L6 JS Globals | Browser | <8s | For versions + deep detection |
| L7 Network | Browser | <15s | When backend/API identification needed |
| L8 SSL | Shell | <3s | Optional, when hosting unclear |

Minimum viable detection (L1+L2+L3+L5) completes in under 10 seconds with no browser.
