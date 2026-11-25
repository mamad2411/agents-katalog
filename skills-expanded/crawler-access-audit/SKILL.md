---
name: crawler-access-audit
description: Audit web crawler access from server logs and robots.txt. Covers robots.txt matching and precedence (RFC 9309), user-agent groups, wildcards and end anchors, crawl-delay, meta robots and X-Robots-Tag, verifying crawler identity, real client IP behind proxies, and AI crawler user-agents. Use for log analysis of bots, compliance checks and crawl-efficiency reports.
---

# Crawler access audit

Goal: decide, for each crawler request in a log, who really made it, which rules applied at that time, and whether it was allowed.

## 1. robots.txt semantics (RFC 9309)
- File is a list of groups. A group starts with one or more `User-agent` lines followed by rules (`Allow`, `Disallow`, `Crawl-delay`, `Sitemap`). Blank lines and comments do not end a group; a new `User-agent` line after rules starts a new group.
- A crawler uses exactly ONE group: the one whose `User-agent` token best matches its product token (case-insensitive, longest match wins). If none matches, use the `*` group. Groups are NOT merged across different tokens, and `*` rules do not apply to a crawler that has its own group. If multiple groups name the same agent, merge those groups.
- Match the product token only (e.g. the name before `/version`), not the whole user-agent string.
- Path matching is on the URL path plus query string, starting at `/`, case-sensitive, prefix-based. `*` matches any sequence of characters, `$` anchors the end of the URL. Rules are matched against the percent-decoded form of unreserved characters; compare after normalising percent-encoding consistently on both sides (encoded slashes stay encoded).
- Precedence: among all matching Allow and Disallow rules in the chosen group, the MOST SPECIFIC rule wins, measured by longest pattern length (octets). On a tie, Allow wins. An empty `Disallow:` allows everything. No matching rule means allowed.
- `/robots.txt` itself is always fetchable. Missing file (404) means everything allowed; server errors (5xx) mean assume disallow; unreachable for long means treat as allowed after caching limits.
- Crawl-delay is not part of RFC 9309; some crawlers honour it, some ignore it. Report violations only if the task asks, comparing the gap between consecutive requests from the same crawler to the delay.
- robots.txt is time-versioned: judge each request against the version in effect at the request timestamp (a change applies from its effective time, not retroactively). Crawlers also cache robots.txt for up to 24 hours, so be explicit if the spec asks for grace periods.

## 2. Page-level directives
- `<meta name="robots" content="noindex, nofollow">` and `X-Robots-Tag` response headers control indexing and snippets, not crawling. A URL blocked in robots.txt cannot have its noindex seen. Header directives can target a specific bot (`X-Robots-Tag: botname: noindex`). They apply to non-HTML files too. When directives conflict the most restrictive applies.
- Do not conflate "disallowed to crawl" with "noindex".

## 3. Identify the crawler correctly
- The user-agent string is self-declared and trivially forged. A claim is only credible if the source IP falls inside the operator's published ranges (or reverse DNS then forward DNS confirms). Requests that claim a crawler name from outside its ranges are impersonated: count them separately, never as that crawler.
- Known AI-related agents (training, search, user-triggered fetch are distinct products from the same company, with separate tokens and often separate rules): GPTBot, OAI-SearchBot, ChatGPT-User (OpenAI); ClaudeBot, Claude-SearchBot, Claude-User (Anthropic); PerplexityBot, Perplexity-User; Google-Extended (a robots.txt-only control token, no separate fetcher); Googlebot; Bingbot; Applebot and Applebot-Extended; CCBot; Bytespider; Amazonbot; Meta-ExternalAgent. Match by exact product token, not by substring of a vendor name.
- Search crawlers, training crawlers and user-initiated agents are different categories; keep them separate in reports when asked by purpose.

## 4. Real client IP behind proxies
- Behind CDNs or load balancers the log's peer address is the proxy. Use `X-Forwarded-For` only when the immediate peer is a trusted proxy. Walk the list from the RIGHT, skipping addresses that belong to trusted proxy ranges; the first non-trusted address is the client. Entries to the left of it are client-supplied and forgeable.
- Use CIDR containment with a real IP library (ipaddress), never string prefixes. Handle IPv6 and IPv4-mapped forms.

## 5. Log parsing hygiene
- Logs rotate: read all files in order, including compressed ones; do not double count overlaps; deduplicate only if the spec says so.
- Parse timestamps with their timezone offsets and compare in UTC. Handle quoted fields with embedded quotes, `-` placeholders, and malformed lines (count them; do not crash).
- Percent-decode paths for matching but keep the raw form for output if the spec asks for it. Strip fragments; keep query strings for matching.
- Count requests, not bytes, unless told. Methods other than GET/HEAD still count as crawler requests unless told otherwise.
- Status code filters are the spec's: robots.txt checks apply regardless of whether the response was 200 or 404.

## 6. Typical outputs
- Per-crawler: total requests, allowed, disallowed (violations), impersonated requests, share of crawl spent on non-canonical or disallowed URLs.
- Non-productive crawl: requests to disallowed paths, URLs missing from the sitemap, parameter/duplicate URLs, redirects and errors.
- Present numbers as integers and in the exact key structure requested.

## 7. Self-checks
1. Hand-evaluate three tricky rules (wildcard, `$`, Allow vs Disallow tie) against sample paths.
2. Verify the group selection for each crawler token, including one with no own group.
3. Re-run the count with a version change in the middle of the log and confirm each side uses its own version.
4. Confirm impersonated and genuine counts add up to total claims per crawler.
