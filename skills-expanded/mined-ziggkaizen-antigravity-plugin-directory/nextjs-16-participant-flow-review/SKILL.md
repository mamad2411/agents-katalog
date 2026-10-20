---
name: nextjs-16-participant-flow-review
description: Reviews Next.js 16 participant, anonymous voting, credential, ballot, referrer, analytics, and URL-handling flows for privacy and trust-boundary leakage. Use when working on participant-web, voting UI, credential entry, route params, searchParams, redirects, logs, analytics, or Server/Client boundaries in trust-sensitive flows.
license: MIT
compatibility: Requires a Next.js 16 project. Scripts require Node.js 20.9.0+ and are read-only.
---

# Next.js 16 Participant Flow Review

Use this skill for anonymous voting, credential handling, participant UI, ballot submission, and other trust-sensitive Next.js 16 frontend flows.

## When to Use

- Reviewing `participant-web`.
- Implementing or reviewing anonymous voting, credential entry, ballot preparation, ballot submission, receipt, or verification flows.
- Changing route params, search params, redirects, `Link` targets, `router.push`, `redirect`, `NextResponse.redirect`, analytics, logging, or referrer policy.
- Deciding Server Component, Client Component, Server Action, Proxy, or WebCrypto boundaries for sensitive flows.
- Checking that participant and admin apps remain separate.

## Workflows

- `workflows/participant-flow-review-workflow.md`: Use for a full privacy, URL, referrer, logging, analytics, Server/Client, and app-boundary review.

## Resources

- `resources/nextjs-16-voting-leakage-checklist.md`: Checklist for URL, referrer, analytics, log, and browser-history leakage.
- `resources/nextjs-16-trust-boundary-map.md`: Boundary map for participant-web, admin-web, identity/session data, and anonymous voting credentials.

## Scripts

Run scripts with `--help` before use.

- `scripts/nextjs-16-route-leakage-check.mjs`: Scans routes and source for suspicious credential/token usage in paths, search params, redirects, links, and logs.
- `scripts/nextjs-16-env-public-check.mjs`: Scans `.env*` files and source for sensitive-looking `NEXT_PUBLIC_*` variables.
- `scripts/nextjs-16-referrer-policy-check.mjs`: Checks whether credential/voting surfaces appear to have an explicit referrer policy.

## Examples

- `examples/safe-voting-entry-flow.md`: A safe pattern for entering or exchanging a voting credential without URL leakage.

## Operating Guidance

1. Treat URL design, referrers, logs, analytics, and screenshots as security-relevant in participant flows.
2. Keep credentials, secrets, session identifiers, blind-signature material, and ballot-sensitive values out of URLs and client-visible telemetry.
3. Keep anonymous voting correctness independent from participant identity sessions.
4. Use Server Components by default and small Client Component islands only for browser-only interactions.
5. Keep backend trust checks on the server; browser crypto support does not replace backend verification.
6. For referrer-sensitive flows, prefer `Referrer-Policy: no-referrer`.
7. Report any suspected leak with the exact file, route, API surface, and safer alternative.
