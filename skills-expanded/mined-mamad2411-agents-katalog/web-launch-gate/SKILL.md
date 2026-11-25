---
name: web-launch-gate
description: Pre-launch security, privacy, and abuse gate for web applications. Mandatory pre-flight before any public deployment.
version: 1.0.0
author: [AUTHOR] + Athena
created: 2026-05-22
context_trigger:
  topics: ["deploy", "launch", "ship", "go live", "push to production", "publish", "host", "make public", "vercel", "netlify", "firebase hosting", "app hosting"]
  files: ["vercel.json", "netlify.toml", "firebase.json", "Dockerfile", "docker-compose.yml", "next.config.*", "vite.config.*"]
who: Athena (agent)
what: 16-point pre-launch checklist covering secrets, auth, privacy, abuse prevention, and legal basics
when: Before ANY web app, API, or publicly accessible service is deployed — whether for a client, personal project, or Athena itself
where: Runs as a blocking gate before deployment commands
why: Vibe-coded apps without security review ship liabilities, not products. This gate prevents the most common catastrophic misses.
how: Sequential checklist audit → pass/fail per item → BLOCK deployment if any critical item fails
---

# Web Launch Gate

> **Trigger**: Activates automatically when deploying any web-facing application.
> **Authority**: This gate is MANDATORY. Do not skip items marked 🔴.

---

## Pre-Flight Checklist

Run every item before deploying. Items marked 🔴 are **blocking** — deployment MUST NOT proceed if they fail. Items marked 🟡 are **warnings** — flag to the user but don't block.

---

### 1. Secrets & Keys

| # | Check | Severity | How to Verify |
|---|-------|----------|---------------|
| 1.1 | `.env` / `.env.*` is in `.gitignore` | 🔴 Critical | `grep -n "\.env" .gitignore` |
| 1.2 | No API keys, tokens, or passwords hardcoded in source | 🔴 Critical | `grep -rn "sk-\|sk_live\|AKIA\|ghp_\|glpat-\|xoxb-\|Bearer [A-Za-z0-9]" --include="*.{ts,js,py,tsx,jsx}" .` |
| 1.3 | No secrets in `console.log`, `print()`, or error responses | 🔴 Critical | `grep -rn "console\.log.*key\|console\.log.*secret\|console\.log.*token\|console\.log.*password" --include="*.{ts,js,tsx,jsx}" .` |
| 1.4 | All keys loaded from environment variables or secret manager | 🔴 Critical | Manual review of config/init files |
| 1.5 | Frontend code does NOT contain server-side keys | 🔴 Critical | Check `src/`, `public/`, `app/` for any `process.env.SECRET_*` usage that gets bundled client-side. In Next.js, only `NEXT_PUBLIC_*` vars reach the browser — everything else must stay server-side. |

---

### 2. Authentication & Authorization

| # | Check | Severity | How to Verify |
|---|-------|----------|---------------|
| 2.1 | Auth is implemented if any user data is stored | 🔴 Critical | Review auth provider setup |
| 2.2 | Protected routes/API endpoints require authentication | 🔴 Critical | Test unauthenticated access to protected endpoints |
| 2.3 | JWT `verify_jwt` is `true` for edge functions / API routes | 🔴 Critical | Check `supabase/config.toml` or middleware config |
| 2.4 | RLS (Row Level Security) enabled on all database tables | 🔴 Critical | `SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname = 'public';` |
| 2.5 | Password minimum length ≥ 8 characters | 🟡 Warning | Check auth config |

---

### 3. Input Validation & Injection

| # | Check | Severity | How to Verify |
|---|-------|----------|---------------|
| 3.1 | No raw SQL string concatenation (use parameterized queries / ORM) | 🔴 Critical | `grep -rn "execute.*f\"\|execute.*%s\|\.query.*\+\|\.query.*\`\$\{" --include="*.{ts,js,py}" .` |
| 3.2 | User input is sanitized before rendering in HTML (XSS prevention) | 🔴 Critical | Check for `dangerouslySetInnerHTML`, `innerHTML`, `v-html`, or unescaped template literals |
| 3.3 | File uploads validated (type, size, extension whitelist) | 🟡 Warning | Check upload handlers for MIME type and size checks |
| 3.4 | CORS configured to allow only known origins (not `*` in production) | 🔴 Critical | `grep -rn "Access-Control-Allow-Origin.*\*\|cors.*origin.*\*" .` |

---

### 4. Data Privacy

| # | Check | Severity | How to Verify |
|---|-------|----------|---------------|
| 4.1 | Privacy policy exists if collecting ANY user data (name, email, analytics, cookies) | 🔴 Critical | Check for `/privacy` route or linked policy page |
| 4.2 | You know WHERE user data is stored (DB region, provider, backups) | 🔴 Critical | Document in README or deployment notes |
| 4.3 | API responses don't return more data than the client needs | 🟡 Warning | Review API response shapes — no full DB rows with internal IDs, emails of other users, etc. |
| 4.4 | User data deletion path exists (GDPR right to erasure) | 🟡 Warning | If serving EU users, there must be a way to delete user data on request |

---

### 5. Security Headers

| # | Check | Severity | How to Verify |
|---|-------|----------|---------------|
| 5.1 | `X-Content-Type-Options: nosniff` | 🟡 Warning | Check response headers |
| 5.2 | `X-Frame-Options: DENY` or CSP `frame-ancestors` | 🟡 Warning | Prevents clickjacking |
| 5.3 | `Strict-Transport-Security` (HSTS) header set | 🟡 Warning | Forces HTTPS |
| 5.4 | `Content-Security-Policy` configured | 🟡 Warning | Prevents inline script injection |

> **Shortcut**: Most hosting platforms (Vercel, Netlify, Firebase Hosting) handle some of these automatically. Still verify with `curl -I https://your-app.com`.

---

### 6. Abuse Prevention

| # | Check | Severity | How to Verify |
|---|-------|----------|---------------|
| 6.1 | Rate limiting on API endpoints (especially auth, AI calls, webhooks) | 🔴 Critical | Check for rate-limit middleware or provider-level limits |
| 6.2 | Rate limiting on expensive operations (LLM calls, email sends, file processing) | 🔴 Critical | Someone WILL find your endpoint and loop it |
| 6.3 | CAPTCHA or bot protection on public forms | 🟡 Warning | hCaptcha, Turnstile, or reCAPTCHA on signup/contact forms |
| 6.4 | Cost caps / billing alerts set on cloud providers | 🟡 Warning | Vercel, Supabase, OpenAI, Google Cloud — set spending limits |

---

## Execution Protocol

When this gate activates:

1. **Run each section's checks** against the codebase being deployed
2. **Report results** as a pass/fail table to the user
3. **If ANY 🔴 item fails**: State clearly that deployment should not proceed and list the specific fixes needed
4. **If only 🟡 items flag**: Inform the user of the warnings but do not block deployment
5. **Log the audit result** — note which items were checked and their status

### Quick-Scan Commands (Copy-Paste Ready)

```bash
# 1. Check .gitignore covers secrets
grep -n "\.env" .gitignore

# 2. Scan for hardcoded keys (common patterns)
grep -rnI "sk-\|sk_live_\|AKIA\|ghp_\|glpat-\|xoxb-\|Bearer " --include="*.ts" --include="*.js" --include="*.py" --include="*.tsx" --include="*.jsx" .

# 3. Scan for console.log with sensitive terms
grep -rnI "console\.log.*key\|console\.log.*secret\|console\.log.*token" --include="*.ts" --include="*.js" --include="*.tsx" --include="*.jsx" .

# 4. Scan for dangerous HTML injection
grep -rnI "dangerouslySetInnerHTML\|innerHTML\|v-html" --include="*.ts" --include="*.js" --include="*.tsx" --include="*.jsx" .

# 5. Check for wildcard CORS
grep -rnI "Access-Control-Allow-Origin.*\*\|cors.*origin.*true" --include="*.ts" --include="*.js" --include="*.py" .

# 6. Check security headers
curl -sI https://YOUR-APP-URL | grep -iE "strict-transport|x-content-type|x-frame|content-security"
```

---

## When This Skill Does NOT Apply

- Local-only tools (CLI scripts, desktop apps not exposed to network)
- Private repos with no deployed frontend/API
- Internal dashboards behind VPN with no public access

---

## Source

Codified from:
- r/vibecoding pre-launch checklist (PaddleboardNut, 2026-05)
- OWASP Top 10 (2021 edition — injection, broken auth, security misconfig, XSS)
- Athena v9.8.0 security hardening sprint (keychain migration, RLS deployment, mutable search_path fix)
- Real-world deployment failures observed across client projects
