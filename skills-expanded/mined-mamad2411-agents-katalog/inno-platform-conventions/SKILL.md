---
name: inno-platform-conventions
description: "Use when writing or reviewing code inside an app repo's app/ directory: stack policy, storage, identity, and the files CI will reject if touched. Load this before writing any application code for an Innovation Platform app."
---

# inno-platform-conventions

## Version gate: do this first

Before anything else in this skill, do these five steps in order.

1. If no `inno-platform` tools are available at all, the platform address is
   probably unset. Tell the user to open their platform's panel, copy the
   configure command from its Connect Claude Code card, run it in a terminal,
   and restart Claude Code. Then STOP.
2. Read the `version` field of `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`
   and call the `get_platform_status` MCP tool with it as `plugin_version`.
3. If the `Plugin:` line says `OUTDATED`, `version not reported`, or
   `reported version is not a MAJOR.MINOR.PATCH triple`, STOP. Tell the user
   to run the commands that line gives, then restart Claude Code and start
   again. Do not continue on a stale plugin: its guidance may describe
   platform behavior that no longer exists. If there is no `Plugin:` line at
   all, the platform sets no minimum version: go on to the next step.
4. If the `Plugin:` line says `current` and adds that a newer version
   `is available`, that is advice, not a block. Mention it once, with the
   commands from the `Update commands:` line, and go on to the next step.
5. If the status has no `Template repo:` line, the platform is older than
   v0.15.8. Say so, ask the user's admin to upgrade it, and STOP before any
   step that needs an instance value. Never fall back to a literal value.

Carry on.

The Innovation Platform deploys a Cloudflare Workers gateway (Durable
Object + Container) in front of your app. The gateway is a platform-pinned
build input (the deploy job builds it from the promoted platform source,
outside your checkout; it is never vendored into your repo) and policed by
CI; your job is everything under `app/`. These rules are not style
preferences: each one maps to a CI gate that will fail the deploy.

**Fetch the contract before writing app code:** call `get_app_contract` with
`sections: ["2", "3", "4"]` (the requirements R1 to R9, the recommendations,
and the stack policy), adding the section for the app's type (`1.1` for
`function`, `1.1` and `1.2` for `mcp-function`, `1.2` and `1.3` for
`mcp-container`)
and `2.2` or `2.3` when the app uses a connection or reads platform
variables. If `get_app_contract` refuses the arguments, or the platform is
older than v0.16.14, call it with no arguments and read the sections needed
from the whole contract. Every contract or section answer opens with the
CURRENT digest-pinned recommended base images. The tool is the live source:
never restate contract values from memory or hard-code a base-image digest.
This skill says how to apply the contract while writing code, and names the
part of it that is authoritative for each rule.

## Refusals every tool shares

Six refusals any of the platform's MCP tools can answer are named once, in
the instructions the platform's MCP server sends when a client connects,
rather than in each tool's description. Those instructions are the
authoritative text, so read what each means there; this is what to do next
when a tool answers one:

- `account_inactive`: the account can no longer sign in. Relay the message,
  which tells the user to contact a platform admin; nothing in the call
  fixes it.
- `rate_limited`: wait a minute. Inside one skill run it usually means
  something is looping, or several subagents are calling at once.
- `forbidden`: the caller lacks the standing the tool's description names.
  Don't retry it and don't work around it locally; the app's owner or a
  platform admin has to act.
- `app_not_found`: no app has that name. Check the name with the user.
- `invalid_email`: the value is not an email address. Ask the user for the
  address again.
- `upstream_error`: a service the platform calls failed, or the call failed
  in a way the platform did not expect. Its message says what was running,
  and one retry may succeed. A platform before v0.16.9 answers an
  unexpected failure with `internal_error` instead.

## Deployment types: `container` (below), `function`, `mcp-function`, `mcp-container`

Most of this skill describes the **`container`** type (a Docker container the
gateway fronts). The other three differ from it in ways one contract section
each states; read the one for the app's type:

- **`function`** (§1.1): the app is its own Cloudflare Worker behind the
  *same* gateway. Its entry is `app/index.ts` exporting
  `export default { fetch(request, env, ctx) }`, with no port, no `EXPOSE`
  and no Dockerfile (`inno-containerize` does not apply). Its storage is the
  app's **own bindings**, `env.DATA` (D1) and `env.FILES` (R2), instead of
  `http://storage.internal`. `GET /healthz` is a **route** in the `fetch`
  handler, answering **exactly 200**. Every npm package it imports is
  declared as the **Node apps** paragraph below says.
- **`mcp-function`** (§1.1 and §1.2): a function app whose consumer is an MCP
  client instead of a browser. It serves the MCP **Streamable HTTP**
  transport at `POST /mcp`, stateless (no `sessionIdGenerator`), and has no
  Cloudflare Access and no sign-out link: the platform is the OAuth
  Authorization Server and the gateway the Resource Server, so never read
  the `Authorization` header or route `/.well-known/oauth-protected-resource`
  yourself. Identity is still the gateway's headers (**Identity** below).
- **`mcp-container`** (§1.3): that same MCP contract from the container
  shape, for a non-TS/JS stack or work a Cloudflare Worker can't host. The
  Dockerfile rules are `inno-containerize`.

Identity (read the header, never build auth), ephemerality, the protected
and injected files, and the safety-gate discipline below are **identical**
across the types (sign-out applies to the browser-facing types only). The
rest of this skill's code examples are the container reference; translate
them into the `fetch` handler for a function or mcp-function app.

## Releases: push = checks, tag = deploy

A push to the default branch runs the platform's safety gates and deploys
NOTHING: push work in progress freely; that run is the safety preflight
(`inno-safety-preflight` narrates it). Deploys happen only when a `v*`
release tag is pushed (`inno-ship` handles versioning and tagging).

## Stack: the user's choice; Python/Starlette is the tested path

Any stack that meets §2 is acceptable, and **no CI gate checks the language
or framework** (§4, the stack policy). **Python/Starlette is the tested
stack**: the template's reference app (`app/main.py`, plain Starlette) uses
it, so choosing it means starting from a known-good working example.
**Alternative stacks are equally fine.** This holds for new and migrated
apps alike (`inno-migrate-app` keeps the original stack by default): don't
"correct" an app to Starlette in either direction.

Whatever the stack, pin dependencies in its own manifest under `app/`
(`requirements.txt` for the Python reference, where the template's copy is
the source for its pins; `package.json` for Node; `go.mod` for Go) and keep
them CVE-clean: the `deps` and `container` gates fail the build otherwise.
R8 says what each gate audits, and §4 names the known FastAPI trap: check
that the lockfile resolves a clean Starlette before committing to it.

**Node apps: commit `app/package-lock.json`, and declare every import.**
§1.1's **Dependencies** bullet and R8 are the rule; this is how to follow it:

- In a function-shaped app (`function`, `mcp-function`), every package
  your Worker imports by bare name is listed in `app/package.json` itself,
  under `dependencies`. Nothing is installed at the repo root, and CI
  installs with `--omit=dev`, so an undeclared import fails the bundle, and
  so does one listed only under `devDependencies`, with an error titled
  `devDependency imported at runtime` naming the package. Move such a
  package with `inno-ship`'s **Moving a devDependency into dependencies**,
  which keeps its specifier and its locked version. A container app's
  Dockerfile builds its own runtime tree, but list its runtime imports
  under `dependencies` too: the `deps` gate audits only those (R8).
- Regenerate the lockfile with `npm install` inside `app/` whenever you
  change dependencies, and commit both files together. A function-shaped app
  (`function`, `mcp-function`) that ships `app/package.json` must commit
  `app/package-lock.json`: the `app-deps` job fails, naming the file, when it
  is missing or out of step, and that job runs on **every push to the
  default branch**, so the preflight catches it before you tag. The `deps`
  gate builds a throwaway lockfile to audit when none is committed, so its
  own green proves nothing about this.
- A container app should commit it too: while an admin has the release-age
  cooldown on (`safety.min_release_age_days` above 0), an app shipping
  `app/package.json` with no committed, parseable `app/package-lock.json`
  fails the `dep-age` gate, because ranges have no single publish date to
  check.
- That app-owned lockfile under `app/` is fine; a lockfile at the **repo
  root** is not (**Files you must not touch** below).

## Rendering: escape by default, never string-built HTML

Whatever the framework, **never build HTML with string interpolation or
concatenation**. The current user's identity (`X-Forwarded-User`) is
attacker-influenced input (anyone who can reach the gateway with a valid
sign-in controls their own email string, and it flows straight into your
pages), so unescaped interpolation is a stored or reflected XSS that the
`sast` job's semgrep OWASP scan and human review both reject. That scan
covers the whole repository except the platform-owned root `src/` and the
directories semgrep skips by default at any depth (`test/`, `tests/`,
`build/`, `dist/`, `vendor/` and `node_modules/`), so your Dockerfile,
`.github/workflows/deploy.yml` and any root-level script are scanned too;
R8 is the authoritative scope. Use your stack's auto-escaping template
engine. In the Python reference, `Jinja2Templates(directory="templates")`
autoescapes by default: route all dynamic content through
`templates.TemplateResponse(request, "page.html", {...})`.

**Response headers.** A browser-facing app (`container`, `function`) should
send a baseline of security headers on its HTML responses (§3), set in one
middleware in the app so they travel with the code through the gated
deploy. `get_app_security` §9 is the one place that names each header and
gives a starting Content-Security-Policy per deployment pattern, including
how an SPA allows its bootstrap script: take the headers and the policy
from there, not from memory. For a `container` app the CI run's
response-header report shows what the app sends today; R8 says when it runs
and that it never blocks a deploy.

## Accessibility: native elements first

Every browser-facing app (`container`, `function`; the two MCP types have no
browser UI) should meet WCAG 2.2 Level AA (§3), and a school or unit with
its own accessibility policy is governed by that policy. **Fetch the
`get_app_accessibility` MCP tool before writing UI code**: it is the live
source for what that takes. The habits below cost nothing up front, and
they are a reminder, not a substitute for the served notes:

- **Native elements first.** A `<button>` for an action, an `<a href>` for
  navigation, a visible `<label for>` on every input, a native `<dialog>` for
  a modal.
- `<html lang>` and a specific `<title>` on every page, one `<main>`, and
  headings in order.
- **Visible focus.** Never remove the focus outline without a
  `:focus-visible` style in its place.
- **Single-page apps:** a route change updates `document.title` and moves
  focus to the new view.

None of this is a gate by default. For a `container` app the CI
accessibility report runs against the built image, and whether it can fail
the deploy is the app's `safety.a11y.mode`, which a platform admin sets: the
served notes' mode table says what each mode does, and
`inno-safety-preflight` reads the report. A `function` app gets no automated
report, so a review against the served notes is its only check.

## Persistence: the storage client, never local disk

Container disk is **ephemeral**: it is wiped on every restart and every
redeploy (R6). Never write a local SQLite file, never `open(path, "w")` app
data to disk. Use the storage client shipped in the template
(`app/storage.py`):

```python
from starlette.responses import JSONResponse, PlainTextResponse
from storage import Storage, current_user

db = Storage()

# a POST route, since it writes: Route("/visits", visits, methods=["POST"])
async def visits(request):
    user = current_user(request)
    if user is None:  # a route that needs a person
        return PlainTextResponse("no signed-in user", status_code=403)
    await db.execute("CREATE TABLE IF NOT EXISTS visits (email TEXT PRIMARY KEY, n INTEGER)")
    await db.execute("INSERT INTO visits (email, n) VALUES (?, 1) ON CONFLICT(email) DO UPDATE SET n = n + 1", [user["email"]])
    rows = await db.query("SELECT n FROM visits WHERE email = ?", [user["email"]])
    return JSONResponse({"visits": rows[0]["n"]})
```

The caller is read and "no user" handled before any per-person query, as
the **Identity** section below says. A route that changes state is never a
GET, and on a browser app it also takes the origin check `get_app_security`
§12 sets (from platform v0.16.19).

`Storage()` defaults its base URL to `http://storage.internal`, which the
gateway's outbound handler intercepts and routes to the app's own D1
database and R2 bucket. **Leave `INNO_STORAGE_BASE` unset**: locally and in
production the default is correct; only override it if you're running the
app process entirely outside the container (unusual). File storage is
`put_file`/`get_file`/`list_files`/`delete_file` against the same client,
backed by R2. Non-Python stacks call the plain-HTTP endpoints R5 lists
directly.

A listing can be partial. `list_files` returns the keys as an ordinary list
that also carries `truncated`, which is true when the gateway stopped
listing at its cap (R5 gives the cap), so the keys are only part of the
bucket: track keys in D1 rather than walk a bucket that size. The JS
client's `listFiles` returns an array with the same flag, not enumerable,
so deep equality and JSON see only the keys. A repo created from an older
copy of the template has a listing with no `truncated`: reading it raises
`AttributeError` in Python, and in JS it is `undefined`, so a partial
listing reads as complete. Check the repo's `app/storage.py` or
`lib/storage.js` before relying on the flag, and if it lacks it, copy the
current one from the template repo (the `Template repo:` line of the status
you read in the Version gate). The current client keeps the old shapes but
one: its identity helper (`current_user`, or `currentUser` in JS) answers no
user for a caller with no identity where an older one answered an empty
email, and its answer adds `member` (**Identity** below). So after the
copy, make every place that reads the helper handle no user first.

**Two body caps on that gateway, and the SQL one is the easy one to hit**
(R5 is authoritative for both). A `{sql, params}` body over **4 MiB** (on
the SQL endpoints, and on the `/_storage/linked/{app}/sql/*` twins a data
link exposes) is refused `400 bad_request`, exactly the answer malformed
JSON gets, so an oversized bulk insert reads as a syntax error rather than a
size problem: send it in batches. A file `PUT` whose declared
`Content-Length` is over **25 MiB** is refused `413 too_large`, and one sent
with no `Content-Length` at all (a chunked body, for example) is refused
`411 length_required`, so an upload route checks the size itself, with its
own message, and sends the body with its length. Neither applies to a function-shaped app, which reaches
`env.DATA`/`env.FILES` with no gateway in between.

## Identity: read the header, never build auth

The gateway decides who reaches the app and tells you who the caller is, in
the identity headers. R3 (`get_app_contract` §2) is the authoritative text
for every header the gateway owns and for the three kinds of caller an app
serves; this is how to apply it. Decide per request what each kind of
caller may see and do, and never assume a caller is a member.

Read the caller through the template's identity helper:
`current_user(request)` in `app/storage.py` (Python),
`currentUser(request.headers)` in `lib/storage.js` (a JS or TS container),
and `currentUser(request.headers)` from `app/identity.ts` in a `function` or
`mcp-function` app. Each answers no user (`None` in Python, `null` in
JavaScript and TypeScript) when `X-Forwarded-User` is empty or missing, and
otherwise `{ email, groups, member }`, where `member` is true exactly when
a group ends `-users` (the caller holds the app's members group). A stack
with no helper reads the headers by the same contract. Check the repo's
helper before relying on that answer: an older one answers an empty email,
not no user (below). In a route that needs a person, handle no user first,
before any per-person read or write:

```python
user = current_user(request)
if user is None:  # a route that needs a person
    return PlainTextResponse("no signed-in user", status_code=403)
```

**Never default the absence back into a value** (`or ""`, `?.email`,
`?? ""`, `"unknown"`): a placeholder bound into `WHERE owner = ?` is one key
that every caller with no identity shares, and a SQL `NULL` is no better.
The helper answers no object at all, so code that reads the email without
the check fails rather than share a key; keep it that way. Contract §3
(from contract 32) is the authoritative text for this rule.

Refuse a caller with no user only in a route that needs a person, never in
a middleware or ahead of routing: the platform's health probe,
`GET /healthz`, arrives with empty identity headers (R3 states it from
contract 32, and the gateway sent it that way before) and must get its 200
(R2). In a route that needs a person, the branch is the one-line refusal
above. **An MCP app refuses inside MCP**, with a tool result marked as an
error or a JSON-RPC error, never with an HTTP status: §1.2 and §1.3 make it
a MUST from contract 32 and say why.

A repo made from a template older than platform v0.16.19 has an older
helper: it answers an empty email rather than no user and has no `member`,
and a function-shaped repo has no `app/identity.ts`. Copy the current
helper from the template repo (the `Template repo:` line of the status you
read in the Version gate), as **Persistence** above says for the storage
client. Where that template has no such helper either, read an empty or
missing `X-Forwarded-User` as no user in the app's own code, by the same
rule.

- `X-Forwarded-Email` carries the same email as `X-Forwarded-User`: the
  gateway injects both, so either one works and neither is more
  authoritative. Read `X-Forwarded-User` by default and treat
  `X-Forwarded-Email` as its alias if you see it in a request dump.
- **An address is not a person.** Both headers carry the caller's email
  address, which can change for one person and pass to another. From
  platform v0.16.12 the platform admits a member by the identity provider
  account their grant is pinned to, wherever the sign-in carries that
  account's subject (R3 says when it does), but both headers stay the
  address. So anything your app keys on the address, its own data or its
  own role store, still goes to whoever holds the address, and a member
  whose address changed no longer finds what was kept under the old one.
  Key on `X-Forwarded-User` all the same: no header carries the account
  itself yet.
- **`X-Forwarded-Groups`** carries at most two groups, both this app's own,
  in this order: the members group when the caller is a member, and the open
  group while the app is open. Their names are in the `App groups:` line of
  the status you read in the Version gate, with the app's name in place of
  `{app}`. It never carries the platform admin group, another app's groups,
  or any other group, so use it only to tell a member from an open-access
  visitor (the helper's `member` is that test); any finer role (an editor,
  a staff view, an in-app admin) needs your own role store keyed on
  `X-Forwarded-User`, and only for a caller who has one. Every person an
  app admits carries at least one of the two, so a visitor admitted only
  because the app is open carries the open group alone.
- **An empty identity is no user: an expected caller, not a fault, and
  never a member or a key.** The platform's health probe, `GET /healthz`,
  arrives with empty identity headers (on contract 32 the only request that
  does, R3), and a request that never passed the gateway (the app run
  locally, a test) can carry none; the helper reads both as no user. A
  person the platform refuses never reaches your code: the gateway answers
  them itself, with a plain 403 "No access" page, or a 503 "Try again
  shortly" page when it cannot ask the platform. A gateway built from
  platform v0.16.10 on shows that 503 page too while it cannot obtain the
  sign-in keys it checks people against, where an older one answers 401;
  `GET /healthz` keeps its 401 on both.
- **How fast a change reaches the header** is R3's to state: within the
  gateway's cache, at most 60 seconds on an MCP app and 10 seconds on a
  browser app.
- **An older live browser app can differ.** A browser app (`container`,
  `function`) not redeployed since v0.14.3's gateway still receives every
  group the caller holds, so an older live app you are debugging may show
  extra groups, and there the three proxy headers below may be
  caller-written. R3 names the case; the app's next deploy ends it.

The gateway also sets three proxy headers you may trust: `X-Forwarded-Host`
(the hostname the request arrived on; build links from it),
`X-Forwarded-Proto` (always `https`) and `X-Forwarded-For` (the client
address from Cloudflare's edge, removed when unknown). It deletes
`Forwarded` and drops the Cloudflare Access session cookies. Every other
header, including `X-Real-IP`, `True-Client-IP` and `X-Forwarded-Port`,
reaches you exactly as the client sent it: never use one for identity,
origin or an access decision.

**Never implement login pages, sessions, password storage, or an "auth
disabled" dev path**: the gateway strips inbound copies of the headers it
owns before injecting its own values, so there is no spoofing surface as
long as you don't add one. A missing user is no user in local dev too:
send the headers yourself (**Keep `ENVIRONMENT=production`** below) rather
than default the absence into a value.

## Configuration & secrets (Variables)

App-level values (one API key the whole app shares, a base URL, a feature
flag) are **Variables**: set once with `set_app_variable` (or the app
page's Variables tab), delivered to your running code as ordinary
environment variables. Read them the normal way for your shape:
`os.environ["MY_KEY"]` / `process.env.MY_KEY` in a container app,
`env.MY_KEY` off the fetch handler's `env` in a function-shape worker.
Never commit them (`gitleaks` fails the build on the full history) and
never build a settings page to collect them. Names, secrecy and timing are
§2.3's and `set_app_variable`'s description to state; the one that touches
code is that a change briefly restarts a container app. A route that
spends an app-level key needs the limits `get_app_security` §5 sets, per
client and globally.

An app may describe the variables it reads in `app/inno-variables.json`;
§2.3's **Declaring what an app wants** is the format and its rules. Write
one whenever your app depends on a variable an owner wouldn't otherwise
know to set: a required name with no value then shows as missing in
`list_app_variables` and the panel's Variables tab, and `app_status` names
it. Two things to know when you edit it. A file that breaks a rule is
refused whole while the deploy stays green, and the reason surfaces in the
run log (`inno-ship`'s **Declared variables** section says where). And
deleting the whole file does not clear the declarations: commit it as `{}`
instead.

## Per-user backend access (Connections)

Identity above is about *your app* knowing who's using it. Some apps also
need to call **another** service *as that same person* (a per-user API or
SaaS account the app fronts: a departmental system, a niche tool, a dev
instance). For that, use a **Connection**, never a single hardcoded
credential shared by every user. The dividing line: if every user of your
app would reach the backend with the exact same key, that's a plain app
secret, a **Variable** (above), not a Connection; if the backend tells your
users apart, it's a Connection.

Connections are reachable from **`mcp-container`** apps only in v1; the
other three types can't consume one yet. Setting one up (discovering how
the backend signs people in, choosing among the three strategies, calling
`set_app_connection`) and wiring the code that consumes it (the template's
`connections.get(name, callerAssertion)` helper, every seam answer the code
must branch on, and what to do when the repo's template client is older)
is a full workflow of its own: use the `inno-add-connection` skill rather
than wiring this ad hoc. The rules the code must hold are §2.2 and
`get_app_security` §8. Two rules shape every line of that code:

- Read the inbound `X-Caller-Assertion` header off the request you are
  serving and pass it straight through to the seam; never keep, persist or
  log it.
- Use the returned credential for the one backend call at hand, cache it
  in memory only until its `expires_at`, and never write it to disk or a log
  line. On `NotConnected`, relay its `connect_url` to the user; on
  `ConnectionLocked` (a subclass of `NotConnected`, so catch it first), tell
  them to **re-authorize this MCP client** (in Claude: `/mcp`, then
  re-authenticate that server), never to reconnect the backend, which
  loops.

## Sign out: one link, no session code

Every browser-facing app includes a "Sign out" link (footer is fine)
pointing at the platform-wide Cloudflare Access logout (R4):

```html
<a href="https://{TEAM_DOMAIN}/cdn-cgi/access/logout">Sign out</a>
```

`{TEAM_DOMAIN}` is environment-specific: **never guess it** or copy it from
another instance. Take the ready-made URL, when scaffolding, from the
`Sign-out URL (all apps):` line of the status you read in the Version gate;
it is the only source available to you, since the gateway config that
carries the team domain is injected at build time rather than living in
your repo.

It must be the *team* domain, not `/cdn-cgi/access/logout` on the app's own
hostname: the per-app logout clears only that app's cookie, which the
still-live global Access session silently re-issues. Known caveat, not a
bug: if the user's Okta session is still alive, revisiting an app signs them
back in without a prompt, so a full sign-out on a shared machine also
requires signing out of Okta.

## Logging: stdout, one event per line

Log like it's a contract: one event per line to stdout, plain text or JSON
(§3). That stream is what surfaces in the app's panel **Logs tab** and the
`get_app_logs` MCP tool, whose description says what each line carries and
how its source column tells your container's lines from the gateway's. That
column does not separate a function app's gateway from the app's own
Worker. Log well now and runtime debugging (`inno-manage-app`'s Runtime
issues guidance) is actually useful later instead of a wall of noise.

## Keep `ENVIRONMENT=production`

There is nothing for you to configure here. The platform's injected gateway
config pins `ENVIRONMENT` to `production` on every deploy, and the deploy
refuses a gateway config that says anything else (R7, and
`get_platform_docs`' **Environment & config integrity**). No wrangler config
may live in your repo (below), and `ENVIRONMENT` is a reserved Variable name
that `set_app_variable` refuses. For local dev, pass mock identity headers
straight to the locally run container, and try each of the three kinds of
caller R3 names; never add an "auth disabled in dev" code path:

```bash
# A member: the members group from the App groups: line of the status.
curl -H 'X-Forwarded-User: user@example.com' -H 'X-Forwarded-Groups: <members group>' http://localhost:8080/
# Signed in but not a member: the open group alone, as an open app sends it.
curl -H 'X-Forwarded-User: user@example.com' -H 'X-Forwarded-Groups: <open group>' http://localhost:8080/
# No identity, as the gateway sends it: the headers present and empty.
curl -H 'X-Forwarded-User;' -H 'X-Forwarded-Groups;' http://localhost:8080/
```

## Files you must not touch

The platform injects the gateway's build inputs at build time (its
`package.json`, `package-lock.json`, `tsconfig.json` and `wrangler.jsonc`)
into a build directory of its own outside your checkout, and **none of the
following may exist in your repo at all**. R7 is the authoritative list,
with the reason for each; the `config-integrity` gate fails outright,
naming each path it finds ("delete `<file>`: the platform injects ...").
Never create or restore one locally, even to "match the template": there is
no version of these files that belongs in your repo.

- `src/`, all of it, at the repo root. The platform owns that directory, and
  anything of yours under it (a source file, `src/node_modules/`,
  `src/package.json`, `src/tsconfig.json`) could shadow the gateway's
  dependencies, so the gate fails the repo with a "delete src/" message.
  Put your code under `app/`; an `app/src/` directory is yours and fine.
- `package.json` and its lockfile (`package-lock.json`) **at the repo
  root**: nothing is installed there. Your app's own build files under
  `app/` (a Node app's `app/package.json`, etc.) are yours and fine.
- `tsconfig.json`, repo root only, same rule. For a function-shaped app the
  deploy itself places the gateway's `tsconfig.json` at the repo root during
  the build, because the app Worker builds from your checkout; that copy is
  the platform's, and a committed one still fails the gate.
- `wrangler.jsonc`, any competing `wrangler.json` or `wrangler.toml`, and a
  `.wrangler/` directory. Wrangler's config discovery order means an
  unvetted `wrangler.json` would silently take priority over the platform's
  injected `wrangler.jsonc` anywhere discovery decides which config to read.
  The deploy pins every wrangler call to an explicit config, and the gate
  rejection is the independent belt to that pin.
- Root-level `.env` / `.env.*` files: wrangler loads them at deploy time and
  adopts unset keys, so a committed one could redirect the deploy's API
  calls.
- Every package manager's project config at the repo root: `.npmrc`,
  `.yarnrc`, `.yarnrc.yml`, `.pnpmfile.cjs`, `pnpm-workspace.yaml` and
  `bunfig.toml`. A `.npmrc` is rejected at **any** depth, `app/.npmrc`
  included, because npm expands environment variables into it, which makes
  it a credential-exfiltration channel. The other package managers' files
  are allowed inside `app/`. Install from the public registry and never
  commit a `.npmrc` anywhere.
- A `scaffold/` directory. Registration prunes the template's
  deployment-type scaffolds out of your repo, best effort, so a surviving
  `scaffold/` means the prune did not happen and the repo is carrying both
  variants' files. While `app/.needs-build` is present the directory is
  allowed (an unbuilt repo can run CI before a prune lands), and
  `scaffold-check` skips that run's deploy anyway; deleting the marker to
  start building re-arms the check, so delete `scaffold/` with it. When
  `register_app` warns that the repository has no `scaffold/<preset>/`, or a
  prune answers `scaffold not applied`, follow what it says.
- **A directory symlink anywhere in the repo**, at any depth and dangling
  ones too; a symlink that resolves to a *file* stays legal. The gate walks
  your tree without following links, so anything behind a directory link
  (an `app/.npmrc`, say) would never be inspected. `config-integrity` has no
  policy toggle, so a repo carrying one cannot deploy until the link is
  removed.

Keep secrets and local env out of the repo entirely: an app-level key or
config value belongs in a **Variable** (`set_app_variable`, or the app
page's Variables tab), delivered to your code as a real environment
variable.

The one file checked by content rather than by absence is `CLAUDE.md`: the
gate checks that five headers from the template are present (the rest of
the file is yours to extend). **The header check is type-blind.** Three
headers are required of every app, whatever its type:
`## Innovation Platform App`, `## Identity (do not build auth)` and
`## What CI enforces`. The remaining two are variant groups, and ANY member
of a group satisfies the gate: `## Persistence (use the storage client)` or
`## Persistence (use your bindings)`, and `## Container contract`,
`## Function contract`, or the legacy `## Worker contract`, which still
passes. The gate never asks what type your app is, so a container app
carrying the function headers passes, and the reverse passes as well. If
you're hand-authoring `CLAUDE.md` (see `inno-new-app`'s empty-repo path),
copy the template's version for your type: `scaffold/function/CLAUDE.md`,
`scaffold/mcp-function/CLAUDE.md` or `scaffold/mcp-container/CLAUDE.md` in
the template repo (the `Template repo:` line of the status you read in the
Version gate) for those three types, and the template's root `CLAUDE.md`
for `container`. Those are the only four: there is no `scaffold/container/`,
because the container files ARE the template root.

Everything under `app/` (routes, templates, requirements, your own modules)
is yours to change freely.
