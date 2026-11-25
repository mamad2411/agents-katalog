---
name: diagnostic-foundations-http-api-debugging
description: "Request-level forensics: headers, status semantics, timing, and auth layers isolated step by step."
---
# Debug HTTP APIs methodically

> Request-level forensics: headers, status semantics, timing, and auth layers isolated step by step.

**Track:** 🧰 Engineering Essentials · **Domain:** Diagnostic Foundations · **Level:** foundation · **~25 min**

**Who this is for:** All Software Engineers

## When to Use This Skill

Request-level forensics: headers, status semantics, timing, and auth layers isolated step by step.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Reproduce with curl/httpie outside your app — isolate client vs server
2. Read status codes literally: 4xx yours, 5xx theirs, 3xx follow redirects explicitly
3. Diff working vs failing requests header-by-header; auth and content-type first
4. Trace DNS→TLS→TTFB timings to locate network-layer stalls
5. Check response bodies for error envelopes even inside 200s
6. Capture evidence (verbose output) before changing anything

## Common Pitfalls

- Postman-vs-curl discrepancies from auto-set headers
- Proxies/VPNs silently rewriting requests mid-flight

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill diagnostic-foundations-http-api-debugging
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill diagnostic-foundations-http-api-debugging -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills