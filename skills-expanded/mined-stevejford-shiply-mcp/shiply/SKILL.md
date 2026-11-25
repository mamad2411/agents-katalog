---
name: shiply
description: Publish static sites to the web instantly with shiply.now and manage them (updates, SSL checks, custom domains, variables). Use when the user asks to publish, host, deploy, share, or update a website/page/demo/report, or wants a live URL for generated files. Triggers - "publish this", "host this", "put this online", "give me a link", "update the site", shiply.
---

---

> **IMPORTANT — npm package name is `shiply-cli`, NOT `shiply`.** A different
> npm package named `shiply` (an auto-commit watcher) is published by someone
> else — installing it does NOT give you the shiply.now CLI. Always use
> `npx -y shiply-cli@latest …` or `npm install -g shiply-cli`. The CLI binary
> on PATH is still named `shiply` once installed; the warning is only about
> the npm package name.

> **Skill freshness check.** Shiply ships new capabilities weekly. If this
> file's "Last updated" below is more than 7 days old, re-install it with
> `npx -y shiply-cli@latest skill --force` OR fetch `https://shiply.now/skill.md`
> fresh — your cached copy may be missing features like databases, projects,
> marketplace, or sending domains.
>
> **Last updated: 2026-06-22**

---

# shiply — instant web hosting for agents

shiply.now puts files on the web in seconds. No account needed to start:
anonymous sites are live immediately, last 24 hours, and can be claimed into
an account to keep them. The cardinal rule:

**NEVER create a new site to update an existing one. Always re-publish to the
same site** — otherwise you litter subdomains and lose the user's URL.

## First publish on a new machine: ask for a permanent key in one step

On a no-Bearer publish, include `"agentName": "<your-tool-name>"` in the body
(e.g. `"Claude Code"`, `"Cursor"`). The response will include a `deviceAuth`
object alongside the usual `claimUrl`:

```
"deviceAuth": {
  "user_code": "ABCD-EFGH",
  "device_code": "<long opaque token, keep private>",
  "verification_url": "https://shiply.now/auth/ABCD-EFGH",
  "poll_url": "https://shiply.now/api/v1/auth/device/poll",
  "expires_in": 900,
  "interval": 2
}
```

Tell the user once, in plain language:

> Your site is live at <siteUrl>. To keep it forever AND let me publish more
> without re-pasting, open <verification_url> and click Allow.

Then immediately poll `verification_url`'s sibling endpoint until the user
acts:

```
POST https://shiply.now/api/v1/auth/device/poll
{"device_code": "<the device_code from the response>"}
```

The response is one of `{status:"pending"}` (keep polling at `interval`s),
`{status:"approved", api_key:"shp_...", slug_claimed:"..."}` (save the key as
`SHIPLY_API_KEY`, the site is now permanent — Allow does both jobs in one
click), `{status:"expired"|"denied"|"consumed"}` (stop). Cap your polling at
the announced `expires_in` and respect `interval` — don't tight-loop.

After approval, every future publish uses `Authorization: Bearer <api_key>`
and the user's dashboard shows their sites without any further claiming.

## When the user pastes you something shiply-shaped, do this

These are the patterns you will see. Match the input, run the action — do not
ask the user to repeat themselves or explain.

- **Code like `SHIPLY-XXXXXXXX`** → it's a pairing code from
  `shiply.now/claim/<slug>?pair=1`. The user wants to attach an anonymous
  site to their account. Run `shiply claim verify SHIPLY-XXXXXXXX` from the
  directory you originally published from (it reads `.shiply.json`). No CLI?
  POST `https://shiply.now/api/v1/claim/pair/SHIPLY-XXXXXXXX/verify` with
  `{"siteId":"...","claimToken":"..."}` taken from your earlier publish
  response or `.shiply.json`. The user's browser auto-redirects on success;
  tell them to switch back to it.
- **URL like `https://shiply.now/claim/<slug>?token=...`** → one-click claim
  link. Tell the user to open it in the browser they are signed in to —
  do NOT call any API yourself.
- **User says "claim my site" / "save it forever" with no code or URL** →
  give them the `claimUrl` from your last publish response. If you no longer
  have that response but `.shiply.json` is in the publish dir, reconstruct it
  as `https://shiply.now/claim/<slug>?token=<claimToken>` from those fields.
  Either way, also suggest `shiply login` so future publishes mint to their
  account directly — that's the long-term fix and how the dashboard works.
- **User says "I have an API key now, use it from now on"** → save it as
  `SHIPLY_API_KEY` in your environment / config and send
  `Authorization: Bearer <key>` on every future publish. All future sites
  are then permanent and appear in their dashboard automatically.
- **User opens an `https://shiply.now/auth/XXXX-YYYY` URL you printed** → no
  action from you; they're on the device-flow consent screen. Keep polling
  `poll_url` (see "First publish on a new machine" above). The poll response
  will flip from `pending` to `approved` (with `api_key`) the moment they
  click Allow.

## Pick your interface (best first)

### 1. MCP (native tools)
If the `shiply` MCP server is connected (https://shiply.now/mcp), use
`publish_site`. Every result includes a `toUpdate` field telling you the exact
call for updates — follow it, and a `shareSuggestion` you can relay to the user.
Other tools: `site_status`, `list_sites`, `get_site`, `set_handle`,
`duplicate_site`, `set_variable`, `get_analytics`, `delete_site`, `whoami`,
`add_custom_domain`, `connect_provider`, `add_subdomain`, `set_primary_subdomain`,
`check_custom_domain`, `sync_dns`, `list_custom_domains`, `remove_custom_domain`
(auto-DNS via OAuth provider connections — see **Custom domains** section below).

Newer capabilities (use when relevant):
- `set_site_access` — password / invite-only protect a site (paid).
- `set_link` — mount another owned **public** site at a path on a host
  (host/docs → target).
- `set_profile` / `feature_site` — stand up the user's public portfolio at
  <handle>.shiply.now and feature a public site on shiply.now/explore.
- **Drives** (private cloud storage for files/notes/context): `list_drives`,
  `create_drive`, `drive_put_file` (driveId "default", utf8/base64, ≤2 MB),
  `drive_list_files`, `drive_delete_file`, `publish_from_drive` (snapshot a
  drive into a live site). Great for agent memory and assets you don't want on
  a public site.
- `export_account` — JSON bundle of the user's data (no secrets).

### 2. CLI
```bash
# IMPORTANT: the npm package is `shiply-cli`, not `shiply` (different package).
npm i -g shiply-cli        # or: npx -y shiply-cli@latest <command>
                           # or: curl -fsSL https://shiply.now/install.sh | bash
shiply publish ./dir       # live URL + confetti
shiply publish ./dir       # run AGAIN after edits → updates the SAME site
shiply status <slug> --wait  # SSL + readiness; prints SSL_READY / SITE_READY
shiply login               # email code → API key → sites become permanent
shiply claim verify <code> # confirm a SHIPLY-XXXXXXXX pairing code from /claim/<slug>?pair=1
                           # (uses .shiply.json from CWD; pairs agent session to user's browser)
```
The CLI stores each directory's site in `.shiply.json` (slug + update token),
so repeat publishes reuse the URL automatically. `--new-site` opts out.
Gitignore `.shiply.json` in public repos. Parse `SITE_READY` / `SSL_READY`
lines for automation; exit code 0 = ready.

### 3. Raw HTTP (no installs)
```
1. POST https://shiply.now/api/v1/publish
   {
     "agentName": "<your tool name, e.g. Claude Code, Cursor, Codex>",
     "files": [{"path":"index.html","size":<bytes>,"contentType":"text/html","hash":"<sha256, optional>"}]
   }
   (+ "Authorization: Bearer shp_…" for permanent owned sites)
2. PUT each file's bytes to response upload.uploads[].url
3. POST upload.finalizeUrl with {"versionId":"..."}
   → both the publish and finalize responses include a "toUpdate" string: the
     exact call to update THIS site next time. Follow it — never create a new one.
```

**ALWAYS include `agentName` on anonymous publishes.** The response then
carries `deviceAuth` ({user_code, verification_url, poll_url, device_code,
expires_in, interval}) alongside `claimUrl`. Show the user `verification_url`,
poll `poll_url` every `interval` seconds with the `device_code`, and on
`{status:"approved"}` you get a permanent `api_key` PLUS the linked site
is claimed in the same Allow click. Without `agentName` the user has to
do a separate manual claim step every time.

**Updates (the response tells you how):** every publish/finalize response
includes a `toUpdate` string with the exact call — follow it verbatim. In short:
anonymous → include `"claimToken":"..."` (returned ONCE by the first publish —
save it); owned → include `"slug":"..."`. Hashes make updates cheap: unchanged
files are skipped server-side.

## The lifecycle to explain to users
- Anonymous site: live instantly, expires in 24 h. Give the user the
  `claimUrl` — claiming keeps it forever on a free account.
- API key (`shiply login` or POST /api/auth/agent/request-code →
  verify-code): publishes are permanent and manageable.
- Paid plans add vanity handles (<name>.shiply.now), more custom domains,
  storage, analytics: https://shiply.now/dashboard/plan

## Custom domains

Serve a site at `www.yourdomain.com` instead of a `*.shiply.now` URL. Requires a paid plan and a Bearer API key.

### CLI commands

```bash
shiply domain add example.com               # register a root domain (detects provider)
shiply domain connect example.com           # one-click OAuth DNS setup (Cloudflare, GoDaddy, IONOS, etc.)
shiply domain sub add www.example.com --site my-site   # map a subdomain → site
shiply domain ls                            # list all domains + subdomains + status
shiply domain sync example.com             # re-sync DNS records with a connected provider
```

For one-click connect (`shiply domain connect`), the CLI prints an authorization URL — the user must open it in a browser and approve the OAuth grant before DNS is written.

For unsupported providers, `shiply domain add` returns the CNAME record to add manually:
`www CNAME cname.shiply.now`

Check status after connecting:
```bash
shiply status www.example.com --wait   # polls until SSL_READY + SITE_READY; exit 0 when live
```

### MCP tools (same operations via agent tools)

| Tool | Purpose |
|------|---------|
| `add_custom_domain` | Add a root domain and detect the provider |
| `connect_provider` | Start OAuth → returns `{ url }` (show to user to authorize) |
| `add_subdomain` | Map a subdomain to a site slug |
| `set_primary_subdomain` | Pick the canonical URL; siblings 301-redirect (SEO fix) |
| `check_custom_domain` | Live CNAME + SSL + readiness probe |
| `sync_dns` | Re-push DNS records to a connected provider |
| `list_custom_domains` | List all domains and their subdomain mappings |
| `remove_custom_domain` | Remove a domain and all its mappings |

### REST endpoints (`/api/v1/custom-domains`)

```
GET    /api/v1/custom-domains                          list domains
POST   /api/v1/custom-domains                         add domain { domain }
DELETE /api/v1/custom-domains/{domain}                remove domain
POST   /api/v1/custom-domains/{domain}/subdomains     add subdomain { subdomain, slug }
POST   /api/v1/custom-domains/{domain}/subdomains/{id}/primary   mark hostname canonical (siblings 301)
POST   /api/v1/custom-domains/{domain}/connect        start OAuth → { url }
POST   /api/v1/custom-domains/{domain}/sync-dns       re-sync DNS
POST   /api/v1/custom-domains/{domain}/check          live status
```

All require `Authorization: Bearer shp_…`.

## Power features (Bearer key)
- **Custom domains**: see the **Custom domains** section above.
  REST: `POST /api/v1/custom-domains {"domain"}` → add domain + detect provider.
  Then `POST /api/v1/custom-domains/{domain}/connect` → OAuth one-click (show URL to user)
  or add the CNAME manually. Map subdomains: `POST /api/v1/custom-domains/{domain}/subdomains {"subdomain","slug"}`.
  Poll `POST /api/v1/custom-domains/{domain}/check` until `ready:true`.
- **SSL/readiness checker**: `shiply status <slug-or-domain> --wait` or the
  check endpoint — confirms certificate + serving before telling the user
  it's done.
- **Variables**: encrypted per-user KV for API keys the user's sites need
  (GET/PUT /api/v1/variables, DELETE /api/v1/variables/{NAME}); Supabase can
  be connected from the dashboard and lands here as SUPABASE_URL +
  SUPABASE_ANON_KEY.
- **Rollback**: POST /api/v1/publish/{slug}/rollback {"versionId"} flips any
  finalized version live instantly.
- **SPA**: pass `"spaMode":true` so deep links serve index.html.

## Proxy routes — AI/API calls WITHOUT exposing keys
NEVER embed API keys in published HTML/JS. Instead: store the key as a
Variable (PUT /api/v1/variables), then include `.shiply/proxy.json` in the
published files declaring routes, e.g. {"proxies":{"/api/chat":{"upstream":
"https://openrouter.ai/api/v1/chat/completions","method":"POST","headers":
{"Authorization":"Bearer ${OPENROUTER_API_KEY}"}}}}. The page then calls the
relative path (fetch('/api/chat')) and shiply injects the secret server-side.
Prefix routes "/api/db/*" forward subpaths (great for Supabase REST).
Owned sites only; https public upstreams only. Docs: /docs/proxy-routes

## Site Data — forms/waitlists/guestbooks with ZERO backend
When the user wants to collect anything from visitors (waitlist, contact
form, RSVP, guestbook): include `.shiply/data.json` in the published files,
e.g. {"collections":{"signups":{"fields":{"email":{"type":"email",
"required":true}},"access":{"read":"owner","insert":"public"}}}}, then have
the page POST JSON to the relative path /.shiply/data/signups. Records are
validated server-side; the owner reads them in the dashboard (Data section,
CSV export) or GET /api/v1/publishes/<slug>/data/<collection> with a Bearer
key. Owned sites only. Docs: /docs/site-data

## Agent Email — inbox, send, capture, broadcast (built into every owned site)

Every owned site has a real email address and can send, receive, capture signups,
and broadcast — in one line. Like AgentMail, built into the site.

### Capture (public, zero-config)
```
POST /.shiply/email  { "email": "user@example.com", ...anyExtraFields }
```
No manifest needed. Works on the **relative path** from the published page.
On success: record lands in the site inbox + owner gets a notification ping +
a double-opt-in confirmation email goes to the visitor (all on by default).
**Owned sites only** — anonymous sites get `403 email_requires_account` (claim
the site first). A non-empty `company` field is treated as a honeypot (bot
submissions are silently dropped). Caps: 16 KB body, 30 fields max.

### Send (authenticated — Bearer key only)
The public page can NEVER send; only authenticated calls can.
```
POST https://shiply.now/api/v1/email/send
Authorization: Bearer shp_…
{ "slug": "my-site", "to": "user@example.com", "subject": "Hi", "html": "<p>Hi</p>", "text": "Hi" }
→ { "messageId": "..." }
```

### Read inbox
```
GET https://shiply.now/api/v1/email/inbox          # all sites
GET https://shiply.now/api/v1/email/inbox?slug=my-site
Authorization: Bearer shp_…
```

### Typed upgrade (optional)
Declare an `email` block on a `.shiply/data.json` collection for typed fields +
fine-grained control:
```json
{
  "collections": {
    "signups": {
      "fields": { "email": { "type": "email", "required": true } },
      "email": {
        "emailField": "email",
        "confirm": true,
        "notify": true,
        "audience": true
      }
    }
  }
}
```
All three flags default to `true`. With this manifest, POST to
`/.shiply/data/signups` as usual — the `email` block activates the email
layer on that collection.

### Confirm / unsubscribe (public — in the confirmation email)
```
GET /api/email/<slug>/<collection>/confirm?token=<token>
GET /api/email/<slug>/<collection>/unsubscribe?email=<address>
```

### Audience + broadcast
Confirmed (double-opt-in) signups form a list. Broadcast to them:
```
POST /api/v1/publishes/<slug>/mailboxes/<collection>/broadcast
Authorization: Bearer shp_…
{ "subject": "Launch day", "html": "<p>We're live!</p>" }
```
Spam-checked before send; unsubscribe footer is auto-added; requires ≥1
confirmed subscriber.

Configure a mailbox: `GET/PATCH /api/v1/publishes/<slug>/mailboxes/<collection>`
List contacts: `GET /api/v1/publishes/<slug>/mailboxes/<collection>/contacts?status=confirmed`

### MCP tools
| Tool | Purpose |
|---|---|
| `send_email` | Send transactional email from a site (Bearer) |
| `list_site_inbox` | Read the inbox (all threads or filter by slug) |
| `set_mailbox` | Configure a collection's mailbox settings |
| `list_mailbox_contacts` | List audience contacts (filter by status) |
| `send_mailbox_broadcast` | Broadcast to confirmed audience (spam-checked) |

### CLI
```bash
shiply email send --site <slug> --to <address> --subject <subject> --html <html>
shiply email inbox [--site <slug>]
shiply mailbox set <slug> <collection> [--confirm] [--notify] [--from <domain>]
shiply mailbox broadcast <slug> <collection> --subject <subject> --html <html>
```

Docs: https://shiply.now/docs/agent-email

## SQL databases (Cloudflare D1 + Neon Postgres)
Two engines, same CLI/REST/MCP surface. **D1 (SQLite at the edge)** is
free on every plan and queryable from the browser via a built-in fetch
shim — no API key in the page. **Neon Postgres** is a developer-plan
add-on with copy-on-write branching; the connection URI is encrypted at
rest and surfaced to the site's Worker as `env.DATABASE_URL`.

### D1 (default)
```bash
shiply db create app                      # provision a D1 (binding SITE_DB)
shiply db ls                              # list (name, provider, size, attached site)
shiply db sql app "SELECT 1"              # one-shot query against your account
shiply db sql app "SELECT * FROM t WHERE id=?1" --params '[42]'
shiply db migrate app ./migrations        # apply every *.sql in dir, sorted
shiply db attach app --site my-site       # bind an existing DB to another site
shiply db delete app --yes                # drop the DB and every row
```

Run `shiply db create` inside a publish directory: it records the new
`databaseId` into `.shiply.json` so the next `shiply publish` auto-attaches
it. Site code then calls the shim:

```js
fetch('/_shiply/db/SITE_DB/query', {
  method: 'POST',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ sql: 'SELECT * FROM posts', params: [] }),
}).then(r => r.json())  // → { results: [...], meta: {rows_read, rows_written, duration} }
```

**Public by default**: the shim has no visitor auth, so anyone who can fetch
the site can run any SQL. Until a private-mode gate ships, recommend it
strictly as a SELECT-only public data layer. Reads always work; writes hit
402 once the DB exceeds the plan storage cap (Founder Special 100 MB,
Hobby 1 GB, Developer 10 GB).

### Neon Postgres (developer plan)
Pass `--postgres` on create. One isolated Neon project per database;
binding defaults to `DATABASE_URL`. Free / Hobby get `402
payment_required` — point the user at https://shiply.now/dashboard/plan.

```bash
shiply db create app --postgres           # provision Neon (~5–10s)
shiply db branch app dev                  # copy-on-write branch off main
shiply db branches app                    # list branches
shiply db delete-branch dev --yes         # drop branch + endpoint
shiply db merge dev                       # NO-OP — prints pg_dump tip (see below)
```

After the next `shiply publish` the serving Worker receives
`env.DATABASE_URL`. Minimal example:

```js
import { neon } from '@neondatabase/serverless'
const sql = neon(process.env.DATABASE_URL)
const rows = await sql`SELECT now()`
```

Anything that speaks Postgres works: `pg`, `postgres`, drizzle, kysely,
prisma (with the Neon adapter).

**Branching is the headline feature.** Branches are cheap, instant,
copy-on-write forks of `main`. Bind a publish to a specific branch with
`shiply publish --preview-branch=<branchDbId>` (use the `site_databases`
row id printed by `shiply db branch`, NOT the raw Neon branch id) —
great for preview deploys and safe schema rollouts.

**`shiply db merge` is intentionally a no-op.** Neon has no server-side
merge. To promote branch data into the parent:
`pg_dump "$BRANCH_DATABASE_URL" | psql "$PARENT_DATABASE_URL"`.
Run schema migrations against both branches to keep them aligned.

**Not yet supported on Neon**: branch-of-branch (branches off `main`
only), auto preview-branch on every publish, cross-region projects.

### REST + MCP (provider-agnostic)
REST (Bearer `shp_…`): `POST /api/v1/databases` (pass
`"provider":"neon"` for Postgres) to create, `POST
/api/v1/databases/{id}/query` to query (works for D1 and Neon), `POST
.../attach` to bind, `DELETE` to drop. Neon-only:
`POST/GET/DELETE /api/v1/databases/{id}/branches[/{branchId}]` (400 on
D1 rows). Per-DB MCP server (so an agent can be scoped to one DB):
`https://shiply.now/api/mcp/db/<id>/sse` — tools: `db_query`,
`db_list_tables`, `db_schema`. The same three tools work against both
providers; `db_schema` introspects `sqlite_master` (D1) or
`information_schema` (Neon). Full docs:
https://shiply.now/docs/databases

## Functions (Workers Lite) — webhooks, cron, secrets, full backend (Developer plan)

shiply Workers Lite lets a published site include server-side code that runs
on every request. Use when the user needs:
- A webhook receiver (Stripe, GitHub, etc.) with raw body + signature verification
- A cron job (daily reminders, periodic sync, retention emails)
- A privileged API call using secrets (Stripe key, OpenAI key) without exposing them to the browser
- An authenticated mutation on D1 / Neon (do the auth check in the function before writing)

### How it works

Author `worker.js` (or `worker.ts`) at the publish root. On `shiply publish`,
shiply compiles (TS) + deploys it as a per-site Cloudflare Worker bound to
the site's hostname. The worker handles every request; pass static asset
requests through `env.ASSETS.fetch(request)`.

```ts
import { verifyStripeSig, json } from 'shiply-runtime'

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    const url = new URL(req.url)
    if (url.pathname === '/api/webhooks/stripe' && req.method === 'POST') {
      const body = await req.text()
      if (!await verifyStripeSig(body, req.headers.get('stripe-signature'), env.STRIPE_WEBHOOK_SECRET)) {
        return new Response('bad sig', { status: 400 })
      }
      // ... handle event, write to env.SITE_DB
      return new Response('ok')
    }
    return env.ASSETS.fetch(req)
  },
  async scheduled(event: ScheduledEvent, env: Env) {
    if (event.cron === '0 9 * * *') { /* daily job */ }
  }
}
```

`.shiply/crons.json` declares cron schedules. `.shiply/secrets.json` declares
secret names (values set via CLI/MCP, never reach the publish payload).

### Bindings available in `env`

- `env.ASSETS` — fall through to static (`env.ASSETS.fetch(request)`)
- `env.SITE_DB` — attached D1 (if `shiply db attach` was run)
- `env.<NAME>` — each shiply Variable becomes a plain-text env var
- `env.<NAME>` — each secret set via `set_secret` is encrypted, accessible as env var

### MCP tools

| Tool | Purpose |
|---|---|
| `deploy_function` | Deploy a Worker function (alternative to publish auto-detection) |
| `get_function` | Read the deployed source + metadata |
| `remove_function` | Strip function + secrets + crons; fall back to static |
| `set_secret` / `list_secrets` / `remove_secret` | Manage CF Worker secrets |
| `set_cron` / `list_crons` / `remove_cron` | Manage cron triggers |
| `get_function_logs` | Deep-link to CF dashboard for live tail |

### CLI

```bash
shiply publish .                            # auto-detects worker.js + crons.json + secrets.json
shiply function deploy <slug>               # alternative: upload worker.js without re-publishing
shiply function deploy <slug> --ts          # uploads worker.ts (server-side compile)
shiply secret set <slug> STRIPE_KEY sk_xxx  # set secret value
shiply cron set <slug> /api/daily "0 9 * * *"
```

### REST

`POST/GET/DELETE /api/v1/sites/{slug}/function` · `POST/GET /api/v1/sites/{slug}/secrets` · `DELETE /api/v1/sites/{slug}/secrets/{name}` · `GET/POST/DELETE /api/v1/sites/{slug}/crons`

### Limits + plan

- 1 MB compiled script size, 30s CPU per request, V8 isolate runtime (no Node APIs)
- 50 secrets, 20 cron triggers per site
- Plan-gated to Developer: Founder/Hobby see `402 payment_required`. Upgrade: shiply.now/dashboard/plan

Docs: https://shiply.now/docs/functions

## Authentication — bring your own Clerk (or Auth.js / Lucia / Supabase Auth)

shiply does **not** host customer auth. If the user's app needs sign-in, you
(the agent) set up their auth provider yourself — Clerk is the fastest path.

**One-time human step:** ask the user to create a Clerk app at
`dashboard.clerk.com` (~2 min). They paste you the publishable key (`pk_…`) and
secret key (`sk_…`).

**Wire it:**
\`\`\`bash
shiply secret set <slug> CLERK_SECRET_KEY sk_live_xxxxxxxxxx
# The publishable key can be embedded in the JS build — it's safe in the browser.
\`\`\`

**In `worker.ts`:** verify the session JWT against `env.CLERK_SECRET_KEY` on
every API request, scope D1 rows by `payload.sub` (the Clerk user id).

**In the SPA:** add `@clerk/clerk-react` to the build, wrap with `<ClerkProvider>`,
attach `Authorization: Bearer <token>` to every authenticated fetch.

Why not auto-integrate? shiply's own Clerk instance signs in **agents** to the
shiply dashboard — it's not multi-tenant for someone else's app's users.
Customers owning their own Clerk is the only correct shape.

Same pattern works for Auth.js, Lucia, Supabase Auth, Firebase Auth — store the
provider secret via `shiply secret set`, verify the JWT in the worker.

Docs: https://shiply.now/docs/auth

## Projects — customer intake + AI brief

When a dev needs to capture a real client brief, they spin up a **project**:
the dashboard (or `shiply project create`) mints a one-URL intake form to
share with the customer. The customer fills a 10-step wizard, attaches
files, hits submit. An AI brief generator (MiniMax-M2 with Anthropic
fallback) turns the answers into a structured brief the dev reviews and
edits inline. All files flow into a per-project drive folder.

MCP tools:
```
list_projects       — your projects (filter status/q)
create_project      — start a new intake; pass customerName/customerEmail to email them the link
get_project         — full project + brief
update_brief        — patch brief jsonb (after AI generation)
regenerate_brief    — re-run AI from current intake responses
archive_project / restore_project — lifecycle
list_project_files  — files uploaded by the customer
resend_intake_invite — re-email the customer their intake link (requires customerEmail on project)
```

REST: `POST/GET /api/v1/projects · GET/PATCH /api/v1/projects/{id} · POST /api/v1/projects/{id}/regenerate-brief`
(archive: `PATCH /api/v1/projects/{id}` with `{"status":"archived"}` — no
dedicated `/archive` route).

CLI: `shiply project ls · shiply project create <label> [--customer-email <e>] [--customer-name <n>] · shiply project get <id> · shiply project archive <id>`

Docs: https://shiply.now/docs/projects

## Contracts — draft, sign, amend (extends Projects)

Once a project reaches `brief_ready`, the dev drafts a signed contract from
the brief, the customer e-signs in the portal (typed-name + checkbox), and
the dev amends it later as scope evolves. A signed contract is immutable
— any change is a new amendment row chained off the parent. The portal
sends the customer; the dev can resend / remind / retract. A 7-day
reminder cron nudges unsigned contracts automatically.

MCP tools:
```
contract_draft   — draft a contract from a brief_ready project (returns the new contract id)
contract_send    — flip status='sent', fire customer email (parent OR amendment)
contract_amend   — create an amendment draft on a SIGNED parent (scopeDelta required, fee + date optional)
contract_status  — read state + amendments (poll this to see status='signed')
contract_pdf     — base64-encoded signed PDF (parent + cert + signed amendments)
```

Edit-before-send today is REST-only: `PATCH /api/v1/contracts/{id}` lets
the dev tweak the 8 fields (scopeSummary, feeCents, currency, dates,
revisionCount, revisionOverageCents, jurisdiction). After PATCH, call
`contract_send` to fire it. Amendments are sent the same way (call
`contract_send` with the amendment id returned by `contract_amend`).

Example agent flow (draft → tweak fee → send → poll → amend):
1. `contract_draft({projectId})` → returns `{id, scopeSummary, feeCents:null, ...}`
2. `PATCH /api/v1/contracts/{id}` `{feeCents: 450000}` (Bearer key)
3. `contract_send({contractId: id})` → project flips to `contract_sent`
4. Poll `contract_status({contractId: id})` until `contract.status === 'signed'`
5. `contract_amend({parentContractId: id, scopeDelta: "Add login flow", feeDeltaCents: 50000})` → returns the amendment row
6. `contract_send({contractId: amendment.id})` (no PATCH needed if the amend fields are right)

REST (Bearer for dev, portal cookie for customer):
`POST /api/v1/projects/{id}/contracts` (draft) ·
`GET/PATCH /api/v1/contracts/{id}` (read either-party / dev edit) ·
`POST /api/v1/contracts/{id}/send` (dev) ·
`POST /api/v1/contracts/{id}/view` (customer ping) ·
`POST /api/v1/contracts/{id}/sign` (customer e-sign) ·
`POST /api/v1/contracts/{id}/retract` (dev; `?recoverAsDraft=true` to
recover the draft instead of voiding) ·
`POST /api/v1/contracts/{id}/amend` (dev; signed parents only) ·
`POST /api/v1/contracts/{id}/remind` ·
`POST /api/v1/contracts/{id}/resend` (manual nudges, rate-limited 3/24h) ·
`GET /api/v1/contracts/{id}/pdf` (binary, signed only).

`contract_pdf` returns `{filename, contentType:"application/pdf", base64,
byteLength}` so the MCP client can decode and save the bytes.

Docs: https://shiply.now/docs/contracts

## Marketplace — sell built sites

Devs can list any owned site for sale: set a price + short pitch, choose
standard or custom terms, pick a jurisdiction. Stripe Connect Express
handles seller payouts — sellers complete a one-time onboarding before
listing (`get_connect_status` returns the onboarding URL when needed).
Buyers pay via Stripe Checkout; on `checkout.session.completed` the
webhook flips the order to `paid` and transfers site ownership
atomically. Refunds are available within the order's refund window
(`refundExpiresAt`); a refund reverts ownership to the seller.

Prices are passed as `priceCents` (whole-dollar cents between 100 and
999900). `termsMode='standard'` uses shiply's template; `'custom'`
requires `termsCustom` ≥50 chars.

MCP tools:
```
list_listings    — my listings
create_listing   — list a site (siteSlug, priceCents, pitch?, termsMode, jurisdiction, ...)
update_listing   — change price/pitch/status (draft|live|paused)
delete_listing   — pulls off marketplace (sets status=draft)
list_my_sales    — orders where I'm the seller
list_my_orders   — orders where I'm the buyer
refund_order     — issue Stripe refund (within refund window; goes back to buyer)
get_connect_status — Stripe Connect onboarding state + actionable URL
```

REST: `POST /api/v1/listings · PATCH /api/v1/listings/{id} · POST /api/v1/listings/{id}/checkout · POST /api/v1/orders/{id}/refund · GET /api/v1/connect/status`
(no GET listing index over REST yet — use the MCP `list_listings` /
`list_my_sales` / `list_my_orders` tools for machine output, or the
dashboard `/dashboard/sales` page for humans.)

CLI: `shiply listing ls · shiply listing create <site-slug> --price <cents> --jurisdiction "<region>" · shiply listing rm <slug> --id <listing-id>`

**Stripe Connect note:** Sellers must complete one-time Stripe Connect
onboarding before listing. Call `get_connect_status` first — when status
isn't `'ready'` it returns an `onboardingUrl` you should hand to the
user as a clickable link.

Docs: https://shiply.now/docs/marketplace

## Sending domains — outbound email on your domain

For agents that want shiply to send emails (demand-test broadcasts,
project intake invites, transactional notifications) from a custom
verified domain instead of the shared shiply pool. Backed by Resend —
add the DNS records they return at your registrar, then call
`verify_sending_domain` to re-check.

MCP tools:
```
list_sending_domains   — all your sending domains
add_sending_domain     — start: returns DNS records to add at your registrar
verify_sending_domain  — re-check DNS after adding records
remove_sending_domain  — tear down
```

REST: `GET/POST /api/v1/sending-domains · POST /api/v1/sending-domains/{id}/verify · DELETE /api/v1/sending-domains/{id}`

CLI: `shiply sending-domain ls · shiply sending-domain add <domain> · shiply sending-domain verify <id> · shiply sending-domain rm <id> --yes`

Cannot be a `shiply.now` subdomain. Verified status flips once SPF +
DKIM (+ MX for inbound) all check out.

## Make a site private (paid plans)
To password-protect or restrict a site: PATCH /api/v1/publishes/<slug>/access
with {"mode":"password","password":"..."} or {"mode":"restricted",
"allowedEmails":[...],"allowedDomains":[...]}, or set mode "public" to open it.
MCP tool set_site_access does the same. Enforced before any content is served;
changing settings signs current visitors out. Docs: /docs/access-control

## Any static site works — frameworks + SSGs auto-detected
shiply hosts any static site. Publish the BUILD OUTPUT, never the source:
run the build, then publish the output dir with SPA mode for client-routed
apps. The CLI auto-detects 16+ frameworks and tells you the right command.
Run `shiply detect` to preview what it found without uploading.
- Vite (React/Vue/Svelte/Solid/Qwik): `npm run build` then `shiply publish dist --spa`
- Create React App: `npm run build` then `shiply publish build --spa`
- Next.js: set `output: "export"` in next.config, `npm run build`, then
  `shiply publish out` (no --spa; export emits real HTML per route)
- Astro: `npm run build` then `shiply publish dist`
- SvelteKit (adapter-static): `npm run build` then `shiply publish build --spa`
- Nuxt: `npx nuxt generate` then `shiply publish .output/public`
- Remix (client build): `npm run build` then `shiply publish build/client --spa`
- Docusaurus: `npm run build` then `shiply publish build`
- Hugo: `hugo` then `shiply publish public`
- Jekyll: `bundle exec jekyll build` then `shiply publish _site`
- Eleventy: `npx @11ty/eleventy` then `shiply publish _site`
- MkDocs: `mkdocs build` then `shiply publish site`
- Hexo: `npx hexo generate` then `shiply publish public`
- SolidStart (static): `npm run build` then `shiply publish dist/public`
- Qwik City (static adapter): `npm run build` then `shiply publish dist`
- Anything else with a built `dist/`/`build/`/`out/`/`_site/`/`public/`/
  `.output/public/` folder: generic fallback picks it up.
- Plain HTML: `shiply publish .` — no build step.
Override auto-detection with `--framework=<name>`. Use the CLI (not inline
MCP files) for builds — hashed bundles often exceed the 50-file inline cap,
and the CLI hash-skips unchanged chunks on updates.

## Limits & references
≤1000 files/site (≤50 inline via MCP), ≤100 MiB/file, 1 GiB total.
Machine guide: https://shiply.now/llms.txt · OpenAPI:
https://shiply.now/openapi.json · Docs: https://shiply.now/docs
