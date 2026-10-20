---
name: edu-src
category: security
risk_level: high
default_permission: approval
requires_approval: true
tools:
  - fofa_search
  - fofa_stats
  - curl.exe
  - browser
outputs:
  - JS-extracted API routes and sensitive tokens
  - IDOR candidate parameters (userId, orderId, studentId, etc.)
  - exposed sensitive file evidence
  - reproducible finding with one request proof
---

# Edu SRC Operator Skill

Use this skill when the user wants to hunt on educational SRC targets (.edu.cn). Core principle: IDOR and info leaks produce 90% of valid findings; CVE scanning does not. Never run bulk scanners on edu targets.

## Target selection

- Use `fofa_search` to find targets. Prioritize systems with obvious functionality over static pages.
- Prefer: login panels, student/teaching systems, OA/office automation, API docs, monitoring dashboards.
- After getting FOFA results, pick 3-5 targets that look most promising. Do not process the entire list in one session.
- For each target, open the browser ONCE. Load the page, then analyze. Resist the urge to feed the URL to a scanner.

## JS analysis (highest ROI activity)

- Open browser DevTools Sources tab. Identify main JS bundles: `main.*.js`, `app.*.js`, `chunk-*.js`, `runtime*.js`.
- Do NOT dump entire minified JS into context. Use in-browser Ctrl+F or narrow extractions.
- Search JS for these patterns, one category at a time:

```
# API routes
/api/  /rest/  /v1/  /v2/  /v3/  /graphql  baseURL  axios.  fetch(

# Hidden admin routes
/admin  /manage  /system  /monitor  /console  /backstage

# Sensitive tokens and keys
accessToken  refreshToken  apiKey  secret  password  appId  appSecret
Authorization  Bearer  token:

# Internal infrastructure
192.168.  10.  172.16  .internal  intranet  mysql  redis  jdbc
```

- For each JS discovery, extract only the matched line (not the surrounding 500 lines).
- A route string from JS is a candidate, not a fact. Confirm with one curl request before acting on it.
- If the JS reveals API endpoints with numeric parameters (`/api/user/123`, `/api/order?id=456`), flag these as IDOR candidates immediately.

## Network request analysis

- With browser DevTools Network tab open, reload the page or perform one natural action (login, search, click a nav item).
- Filter to XHR/Fetch only. Identify:
  - The shape of API responses: which fields come back (userId, phone, idCard, email, role, token)
  - Auth mechanism: cookie-based, header-based (Authorization: Bearer), or custom
  - Any numeric ID in request URLs or bodies
- If a response includes sensitive fields the frontend doesn't display, that is an info leak finding.
- Do NOT replay every request you see. Pick the one most likely to contain a user-specific ID.

## IDOR testing (where findings happen)

- If registration is open, register account-A. If not, skip to unauthenticated testing.
- Find one API call that returns data specific to account-A (profile, orders, messages, etc.).
- Note the exact request: URL, method, headers, and the parameter that identifies the user.
- Change that parameter to a different value. Acceptable sources for the new value:
  - A user ID discovered in JS
  - An ID from a public listing page
  - Increment/decrement by 1
  - If you registered account-B, use account-B's ID
- Send ONE modified request via curl (not browser, to avoid cookie pollution). Observe the response.
- If it returns account-B's data: horizontal IDOR confirmed. Stop and report.
- If the API has a `role` or `type` field in the response, try changing it in the request: vertical IDOR.
- Do NOT iterate through sequential IDs. One confirmed mismatch is enough evidence.

## Sensitive path probing (low-frequency, manual)

- For each target, try at most 10 paths total. Pick from the list below based on what the target's tech stack suggests.
- Use `curl.exe -s -i --max-time 8 <url>/<path>`. One path at a time, 3+ seconds apart.
- If a path returns 404, move on immediately. Do not try variations of it.
- If it returns 200/302/403/401, note the finding and decide whether to go one level deeper.

```
# API docs (SpringBoot / generic)
/swagger-ui.html
/swagger-ui/index.html
/v2/api-docs
/v3/api-docs
/doc.html

# SpringBoot actuators
/actuator
/actuator/heapdump
/actuator/env

# Monitoring panels
/druid/index.html
/nacos/

# Config and VCS leaks
/.env
/.git/HEAD
/.git/config
/.DS_Store
/robots.txt

# Common backup files
/backup.zip
/www.zip
/backup.sql
/wwwroot.zip

# Debug pages
/phpinfo.php
/test.php

# Admin consoles
/admin/
/manager/
```

- Stop probing immediately if you receive a WAF block page or 429 rate limit. Switch to a different target.

## Unauthenticated access

- Before any auth testing, try accessing discovered admin/monitoring paths without credentials.
- Many SpringBoot/Druid/Nacos panels on edu sites have no auth at all.
- If a monitoring panel loads without login, that is a valid finding. Extract one screenshot as evidence, then stop with that target.

## Evidence collection

- For every confirmed finding, capture:
  - One screenshot of the vulnerable page/response via browser
  - One curl command that reproduces the issue (for the report)
- Do NOT dump full HTML pages or full API responses with hundreds of user records into context.
- A finding is "confirmed" when: you made one request that proves the vulnerability exists AND you can explain the impact in one sentence.

## Hard stops

- NEVER run nuclei, dirsearch, ffuf, or any bulk scanner against edu targets.
- NEVER iterate through sequential IDs in a loop.
- NEVER send more than 20 requests to a single target in one session.
- NEVER modify or delete data. Read-only IDOR and info leaks are sufficient for valid SRC reports.
- If a target returns a WAF page, captcha, or 429 — stop that target immediately. Do not attempt bypass without asking the user.
- Do not test student/personal systems (宿舍管理, 学生信息管理 labeled as such). Stick to institutional systems.
