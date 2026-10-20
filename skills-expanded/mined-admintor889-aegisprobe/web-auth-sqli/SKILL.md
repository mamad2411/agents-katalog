---
name: web-auth-sqli
category: security
risk_level: high
default_permission: approval
requires_approval: true
tools:
  - curl.exe
  - browser
outputs:
  - auth endpoint evidence
  - login bypass validation
  - authenticated context
---

# Web Auth SQLi Skill

Use this skill when current evidence mentions login, auth, JWT, session cookies, user APIs, SQL errors, Sequelize, SQLite, or credential testing.

- First identify the exact login endpoint, method, and JSON field names from observed forms, API calls, or a small failed request.
- In PowerShell, JSON POST requests must use stop-parsing: `curl.exe --% -s -i --max-time 10 -X POST https://target.example/api/login -H "Content-Type: application/json" -d "{\"email\":\"user@example.com\",\"password\":\"test\"}"`.
- Use one credential or bypass hypothesis per turn, then observe status, cookies, JWT presence, role hints, and error messages.
- If SQLi is plausible, prefer minimal auth-bypass payloads against the login field before running any scanner.
- Do not brute force. Do not spray credential lists. Default credentials are a single validation hypothesis, not a loop.
- If authentication succeeds, store only the fact and token/cookie shape in the summary; avoid echoing full secrets unless needed for the next approved request.
- After auth, choose one high-value read-only route next, such as current user, profile metadata, role-gated navigation, or owned records.
