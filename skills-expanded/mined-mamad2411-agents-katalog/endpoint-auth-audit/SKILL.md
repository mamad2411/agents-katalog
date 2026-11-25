---
name: endpoint-auth-audit
description: "Use when checking if a public URL/API/webhook has auth."
version: 1.0.0
platforms: [linux, macos]
metadata:
  hermes:
    tags: [security, auth, webhooks, api, cloudflare, probe]
    related_skills: [dogfood, systematic-debugging, requesting-code-review]
---

# Endpoint Auth Audit

Live-check whether a public HTTP surface actually requires authentication. Do not
answer from docs, attachment previews, or GET-only scrapes.

**Core principle:** Auth is what happens when the *correct* method hits the
handler with *no* credentials. A GET 404 on a POST webhook is not evidence of a
lock.

## When to use

- User asks "does this URL have auth?", "is this open?", "who can call this?"
- Attached `@url` preview shows `{"error":"not found"}`, 401/403 ambiguity, or empty body
- Public webhook / tool endpoint / tunnel hostname (Vapi, Stripe, Slack, custom HITL)
- Suspected missing shared-secret, CF Access, or Bearer <REDACTED>

## Workflow

### 1. Don't trust the attachment alone

Browser/Firecrawl attachments often **GET** the URL. Webhooks commonly:

| Method | Typical unauthenticated response | Meaning |
|--------|----------------------------------|---------|
| GET | 404 `not found` / 405 | Route exists for other methods only — **not** "locked" |
| OPTIONS | 501 / missing CORS | Unrelated to app auth |
| POST no auth | 200 with business JSON | **No auth** |
| POST no auth | 401/403 + `WWW-Authenticate` or app error body | Auth present |
| Any | 302 → `*.cloudflareaccess.com` | CF Access in front |

Always re-probe with `curl` (or equivalent) yourself.

### 2. Run a method × credential matrix

Use `scripts/probe-endpoint-auth.sh <url>` or the equivalent curls. Minimum set:

1. `GET` baseline (headers + body)
2. `POST` empty JSON `{}` — **no** `Authorization`
3. `POST` realistic payload for the product (e.g. Vapi tool-calls envelope) — no auth
4. `POST` with wrong `Authorization: Bearer <REDACTED> and/or `X-Vapi-Secret: test`
5. Note `WWW-Authenticate`, `cf-ray`, redirects, status, and a short body prefix

**Verdict rules:**

- If (2) or (3) returns **2xx and the app processes the body** (not a generic edge block) → **no auth**
- Wrong credentials that still process the body → secret is **not enforced**
- Only (4) works while (2)/(3) fail closed → auth works
- CF 1010/1020 on some clients but curl works → client/UA filtering, **not** app auth

### 3. Stay non-destructive

When the server accepts tool/RPC calls:

- Prefer unknown/no-op names (`ping`, `list_tools`, empty `toolCallList`)
- Do **not** invent real side-effecting tool names to "see what happens"
- One short probe is enough once you have a processing response

### 4. Map public hostname → origin

For `*.cm.xyz` and other tunnel fronts, search machines/infra for the hostname:

```bash
rg -n 'hostname-here\.cm\.xyz' ~/machines ~/git --glob '!**/.git/**' --glob '!**/nixpkgs/**'
```

Typical pattern (Cloudflare Tunnel ingress in home-manager):

- `ask-cooper.cm.xyz` → `http://127.0.0.1:8788`
- sibling hostnames on the same tunnel config

Report: public host, local bind, which LaunchAgent/service owns it, whether
tunnel Access or only origin auth applies.

### 5. Report shape (keep it tight)

Lead with the answer in one line, then a small evidence table:

```
**No auth** — unauthenticated POST is processed by the HITL server.

| Request | Result |
|---|---|
| GET /path | 404 {"error":"not found"} |
| POST no creds | 200 {"results":[...]} |

Routing: tunnel hostname → 127.0.0.1:PORT (path to nix/config).
Blast radius: unknown tools ignored; registered tools would be callable.
Fix options: shared secret header, CF Access on hostname, or both.
```

Do not dump full header blocks unless the user wants deep debug.

## Pitfalls

- **GET 404 ≠ protected** — most webhooks only implement POST
- **Attachment/Firecrawl is GET** — always re-probe the real method
- **Wrong Bearer <REDACTED> still 200s** — proves the header is ignored, not that auth is optional-by-design
- **CF error 1010** on Python `urllib` / odd UAs while `curl` works — not app auth; retry with curl + normal UA
- **Invoking real tools** during a probe — stay on unknown/no-op names
- **Code-only conclusions** — live response beats reading the handler if the host is up

## Support files

- `scripts/probe-endpoint-auth.sh` — curl method/credential matrix
- `references/cooper-hitl-vapi.md` — ask-cooper.cm.xyz /vapi/tools case notes
