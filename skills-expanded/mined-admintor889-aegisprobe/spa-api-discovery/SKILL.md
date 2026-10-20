---
name: spa-api-discovery
category: security
risk_level: medium
default_permission: approval
requires_approval: true
tools:
  - curl.exe
  - Select-String
  - browser
outputs:
  - frontend route evidence
  - API endpoint candidates
  - framework fingerprint
---

# SPA API Discovery Skill

Use this skill when current evidence mentions Angular, React, Vue, Webpack, Vite, JavaScript bundles, source maps, API routes, or a single-page app shell.

- Extract script filenames and route-like strings; do not dump entire bundles into model context.
- Fetch one bundle at a time only when its name suggests routes, main app code, runtime config, or API clients.
- Use PowerShell filters that return matched tokens, not whole minified lines. Prefer `Select-String -AllMatches ... | ForEach-Object { $_.Matches.Value } | Select-Object -Unique -First 30`.
- Do not use `ForEach-Object { $_.Line }` on minified JavaScript bundles; one match can return the entire bundle.
- Search for route and API tokens such as `/api/`, `/rest/`, `login`, `admin`, `account`, `profile`, `record`, `user`, and `token`.
- After API tokens are found, run one follow-up extraction for identity/auth/client routes before testing files or broad content discovery. Look for `login`, `signin`, `signup`, `register`, `logout`, `auth`, `session`, `token`, `account`, `user`, `profile`, and `admin`.
- Keep auth route extraction narrow. Prefer a simple double-quote-only first pass to avoid PowerShell quote mistakes: `$js = curl.exe -s --max-time 10 https://target.example/main.js; [regex]::Matches($js, '"([^"]*(?:/api/|/rest/|#/|/login|/signin|/signup|/register|/auth|/session|/account|/profile|/admin)[^"]*)"', 'IgnoreCase') | ForEach-Object { $_.Groups[1].Value } | Select-Object -Unique -First 40`.
- If that returns only generic words such as `user` or `token`, do not turn them into URL facts. Search for route-shaped tokens with `/` or `#/` next.
- If a candidate login/auth endpoint is identified, confirm the method and field names with one failed request or one bundle token extraction before attempting any bypass.
- Treat discovered route strings as candidates. Confirm with one HTTP request before calling them facts.
- Prefer API discovery before content discovery when the homepage is a SPA shell with few visible server routes.
- Use browser/MCP only when client-side interaction is the smallest useful action, such as observing network calls after login.
