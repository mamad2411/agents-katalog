---
name: inno-add-connection
description: Use when an app needs to reach an external backend AS EACH INDIVIDUAL USER (a per-user API or SaaS account the app fronts, such as a departmental system, a niche tool or a dev instance) rather than with one shared app key. Discovers how people sign in to that backend, provisions a Connection with set_app_connection (a pasted token, the backend's own login, or a per-user client ID/secret pair), and wires the app to consume it. mcp-container apps only in v1.
---

# inno-add-connection

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

Some apps don't just read and write their own database: they call out to
another service **on behalf of the person using them**, and that other
service needs to know *which* person it's talking to. A Connection is the
platform's way of handing your app a live, per-user credential for that
outside service without your app ever holding a master key to everyone's
accounts. This skill walks through recognizing when that's what you need,
figuring out how the backend signs people in, setting the Connection up, and
wiring the app's code to use it.

Requires the `inno-platform` MCP server (ships with this plugin's `.mcp.json`).
If this is the first call against it this session, expect a browser Okta
login; that's expected, not an error.

**Read the contract's Connections section before you start:** call
`get_app_contract` with `sections: ["2.2"]`. If `get_app_contract` refuses
the arguments, or the platform is older than v0.16.14, call it with no
arguments and read the sections needed from the whole contract. §2.2 is the
authoritative text for the seam the app calls, every answer the seam can
give and whose each is to fix, the three strategies, and the five connection
tools. This skill is the workflow around it, and points at its subsections
(**The app-facing seam**, **What the app MUST NOT do**, **Availability**,
**Configuring a connection**, **Visibility and oversight**) rather than
restating them.

Platform tool calls share one per-person budget, which the platform's server
instructions state. This skill never needs anywhere near it, so an answer of
`rate_limited` here means something is looping, or several subagents are
calling at once; stop and reconsider rather than retrying. That refusal and
the others any platform tool can give are explained once, in
`inno-platform-conventions`' **Refusals every tool shares** section.

**Speak the user's language,** per the plugin README's **House style**
section. Here that means "connect your app to {backend} as each person,"
"sign in to {backend} once," "a token you create in your {backend} account and
paste in." Never "OAuth," "PKCE" or "client secret." Those words are fine in
your own reasoning and in the tool calls you make, just not in the sentences
you say back to a non-technical user.

**No catalog, no steering.** This skill doesn't maintain or suggest a list of
backends. If the target is a big enterprise service that already has its own
first-party integration for AI assistants, it's fine to mention that exists,
but don't block or discourage the user from connecting to it this way either.
This path is most useful for the long tail: a departmental API, a small
internal tool, a niche SaaS, a dev or test instance, anything without a
ready-made integration.

## 1. Confirm this app actually needs a Connection

Check all three before doing anything else:

- **Per-user, not shared.** A Connection is for a backend where each person
  sees or does *their own* things: the backend itself tells users apart. If
  every user of your app would use the exact same key or token to reach the
  backend (one shared service account), that's **not** a Connection. It's a
  plain app secret, which belongs in the app's **Variables**
  (`inno-manage-app`'s `set_app_variable`, or the Variables tab on the app's
  page; the app reads it as an ordinary environment variable), and a route
  that spends it needs the limits `get_app_security` §5 sets, per client
  and globally. Point the user there and stop here.
- **The app is `mcp-container`.** Only container-shaped MCP apps can reach the
  platform's Connections seam in v1 (§2.2's **Availability** says why). If the
  app is `function`, `mcp-function`, or plain `container`, say plainly that
  this app type can't consume a Connection yet, and stop; don't half-wire it.
  (If you're not sure of the app's type, check `app_status` or ask the user.
  A `container` app that only serves a browser UI, with no MCP endpoint, is
  also out of scope today.)
- **The user owns or administers the app.** `set_app_connection` is gated
  server-side to the app's owner or a platform admin. A `forbidden` answer
  means exactly that; don't try to work around it locally.

If any of these isn't true, explain which one in plain terms and stop.

## 2. Find out how people sign in to the backend

Ask the user, in plain terms, how people currently get into the backend
day-to-day. Offer it as a short choice, not open-ended jargon:

- **"They log in on the backend's own website"**: likely the sign-in path
  (behind the scenes, an OAuth authorization-code login). But don't stop
  there: many backends that people log into *also* let each user mint a
  personal token in their account settings. If they do, that paste-a-token
  path is the better choice here (it needs no client registration and no
  backend admin), so ask the follow-up: "Can you also create an API key or
  personal token inside your {backend} account?" A "yes" moves you to the
  paste path even though people normally log in on the website.
- **"They create a token or key in their account settings and paste it
  somewhere"**: the paste-a-token path.
- **"They create an API client (an ID and a secret, two values) in the
  backend's portal"**: the paste-a-pair path (`oauth2_client_creds`). Some
  backends (HPE Aruba Central / GreenLake is the canonical example) have no
  browser login for APIs and no single token to paste: each user mints their
  own *API client* in the portal, gets a client ID and client secret pair,
  and the platform uses that pair to fetch short-lived tokens for them
  automatically. The tell: the backend's API docs say the only way to get a
  token is POSTing the pair to a token URL.
- **"I'm not sure"**: probe for the answer instead of guessing. Read
  `references/discovery.md` and follow its recipe: it fetches the backend's
  discovery documents and makes one unauthenticated request, then says what
  each response tells you and how to fill the configuration from it. Report
  what you found back to the user in plain terms (for example "It looks like
  {backend} uses sign-in with your account, the same way it does in a
  browser" or "It looks like {backend} issues personal tokens you'd create in
  your account settings") and confirm before moving on. If discovery comes
  back inconclusive, fall back to asking the user directly, or ask them to
  check their backend account's settings page for anything called "API key,"
  "personal access token," or "developer settings."

## 3. Choose the strategy and fill in the configuration

Three strategies, which §2.2's **Configuring a connection** describes.
Prefer the first whenever the backend supports it: it needs no cooperation
from anyone else. The `config` shape each one takes, with an example, is in
`set_app_connection`'s description of its `config` argument; what follows
is how to choose and fill it.

- **`secret_form`** (preferred, zero-admin): the backend issues
  user-generatable tokens (a personal access token or API key created in
  account settings). No client registration, no backend admin: the user
  creates their own token and pastes it once.
  - `probe_url` is a cheap "who am I" endpoint the platform calls with the
    pasted token to confirm it actually works before saving it.
  - `delivery` says how the app sends the token on real calls: `bearer` for a
    standard `Authorization: Bearer <token>` header, or `header` with the
    name some backends expect instead.
  - `help_text` is **strongly recommended**: it is the only instruction the
    user sees on the connect form, right above the paste box, so without it
    they face a blank box. Make it the plain, specific answer to step 2's
    "where do you create that token?", for example *"Create a personal access
    token at Settings → Developer → Tokens in your Acme account, then paste
    it here."*

- **`oauth2_client_creds`** (also zero-admin): the backend's only token flow
  is POSTing a client ID and secret to a token URL, and each user can mint
  their **own** pair in the backend's portal (a "personal API client"). Each
  user pastes their own pair on the connect form; the platform test-mints a
  token before saving (a bad pair is rejected on the spot) and fetches fresh
  tokens as they expire.
  - `token_endpoint` is the URL the pair is POSTed to. Leave `client_auth` at
    its default unless the backend's docs say otherwise.
  - `help_text` is **strongly recommended** for the same reason as
    `secret_form`'s: it is the only instruction shown above the two paste
    boxes.
  - **No callback URL registration, no `client_id` or `client_secret`
    arguments, ever**: the pair belongs to each user, not to the app, and
    the tool refuses definition-level credentials for this strategy. If what
    the user has is ONE pair everyone would share (a service account an
    admin made), that's not this: it's the shared-key case step 1 already
    excluded.

- **`oauth2_code`**: the backend has real user login and you can get (or the
  user can self-register) an OAuth client for it. Fill the config from what
  discovery found, or from the backend's own developer docs;
  `references/discovery.md` maps each discovery field to its config field.
  - `client_auth`: **omit it entirely** for a public (secret-less) client.
  - `pkce`: **omit it.** PKCE is on unless you pass an explicit `false`, and
    `false` is a real downgrade, since PKCE is what binds an authorization
    code to the client that asked for it. Set it only after a connect
    attempt actually fails because the backend rejects `code_challenge`, and
    relay the warning the write then returns: it is the only report of the
    downgrade on any surface.
  - `refresh`: `references/discovery.md` says which value to pick.
  - `revocation_endpoint` is **optional but worth setting** when the backend
    (or its discovery document) advertises one: it is where the platform
    revokes a user's token at the backend when they disconnect from the
    **Connections tab on their account page**. That is the only disconnect
    that ever calls it (`disconnect_user_connection` is local only, whoever
    calls it). Omit the endpoint and every disconnect only forgets the token
    platform-side: the credential stays live at the backend until it
    expires.
  - `scopes` is **not** part of `config`: pass it as the top-level `scopes`
    argument (step 4), the minimal set the app needs.

  The client must be registered against the platform's **single** callback
  URL, the same for every app and every backend: the `Connections callback:`
  line of the status you read in the Version gate. Quote it from there;
  never build it. If the user can self-register a client (many
  developer-console backends let any account owner do this), have them do it
  and hand you the `client_id` and `client_secret`. If they can't, because it
  needs a backend admin, read `references/oauth-client-request.md` and give
  the user the copy-paste request it holds (endpoints, the callback URL, the
  grant type) to send that admin, instead of asking them to become an OAuth
  expert.

## 4. Provision the Connection

### Present the configuration, THEN ask for approval

`set_app_connection` is a **create-or-replace upsert**, not a create: a call
naming an existing `app` and `connection` overwrites that definition with
whatever you pass, with no confirmation from the platform and no merge, and a
change of strategy or of any endpoint a credential is sent to deletes every
user's stored credential for it in the same write. The tool's description
states both rules, including which fields are safe to omit. Any other change
leaves those credentials in place while the definition around them moves,
though they were obtained under the old one. On a live
connection this means you can silently retarget or break something the app's
users are connecting through right now.

So before you call it, **write into your visible reply** what you are about
to write and what it touches, the same present-then-approve rule the
plugin's other skills apply to `register_app`:

- The `app` and `connection` name, and, checked with **`list_connections`
  first**, whether a connection by that name **already exists**. If it does,
  say plainly that this replaces the existing definition and what changes.
  Read its `sinks=` field (the addresses credentials actually go to today)
  and its `connected=` count (how many people hold a credential that a change
  of address would delete) rather than trusting its `label`.
- The backend this points at (its address in plain terms) and the strategy:
  a token the user pastes, signing in on the backend's own site, or pasting
  their own API client ID and secret.
- Whether a `client_secret` is being sent (say *that* it is, never the
  value). Never applicable for `oauth2_client_creds`, which has no
  definition-level secret.
- The blast radius, in the user's terms: a brand-new connection affects
  nobody until people connect; **replacing** an existing one affects everyone
  already connected through it. A changed strategy or backend address makes
  the platform delete every user's stored credential and saved consent for
  it and notify each connected user, so they all have to connect again (and
  are shown the new destination first).

Then stop and get an explicit yes. Don't fold it into the tool-approval
prompt: the user cannot approve what they have not seen.

### Make the call

**Re-running this on an EXISTING connection is destructive** whenever the
strategy or an endpoint a credential is sent to changes (the tool's
description names those fields), so **iterating on a live connection's
config costs your users a reconnect each time.** Get the endpoints right
before the first call; that is what the approval step above is for. If you
must correct one later, tell the user that everyone connected will have to
reconnect, and expect the tool's response to report how many credentials it
invalidated. Re-supplying an unchanged config is free.

Users are shown the destination **hostname** before their credential goes
anywhere, so an endpoint that doesn't visibly match the backend they expect
will (rightly) make them stop. When the disclosure page shows for an
`oauth2_code` connection is the `connections.consent` setting's to say
(`get_config` with `app` prints its description). A credential host that no
connection on the platform was using before notifies the platform admins:
routine oversight, not a fault, so a legitimate new backend simply shows up
in their feed once.

Call the `set_app_connection` MCP tool:

```
set_app_connection({ app, connection, label, strategy, config,
                     client_id?, client_secret?, scopes?, disabled? })
```

- `connection`: a short machine-safe name for this backend within the app
  (for example `crm` or `ticketing`). It is the string the app's code passes
  to `connections.get(...)` later.
- `label`: the human-readable name shown to the user when they connect (for
  example "Acme CRM").
- `strategy` and `config`: from step 3.
- `client_id` and `client_secret`: only for `oauth2_code`.
- `scopes`: the minimal set the app needs.
- `disabled`: omit it for the normal case. `true` pauses the connection for
  every user, and it is the reversible switch: stored credentials are kept
  and resume when re-enabled (compare `remove_app_connection` below).

The tool checks every endpoint against a denylist of non-public hosts, and
that check is **syntactic, never a DNS lookup**: a public hostname that
happens to resolve to a private address is not caught, so read the endpoint
you were handed rather than treating the gate as proof it is external. If the
call is refused `connections_config_invalid`, its message names the rule (a
non-public endpoint, a missing field, a bad strategy and config pairing): fix
that one thing and retry. A call that fails changed nothing (only the audit
row it writes first may remain), so a retry repeats the whole of it. An
`app_busy` answer (from platform v0.16.11) means another change to the app,
such as another edit of this connection or its pause, is in flight: retry
once after a moment, never in a loop.

Four answers are **not** bad arguments, so don't retry blindly:

- **`connections_disabled` or `connections_key_invalid`**: passing a
  `client_secret` needs the platform's encryption key, and it is unset or
  malformed. Relay the message to the user and stop: nothing you change in
  the arguments fixes it, and the person who can fix it is a platform admin,
  not them. (A platform before v0.16.9 answers the malformed case with
  `internal_error`.)
- **A warning about `refresh: "rotating"`**: the call **succeeded**
  (rotating is supported). Relay the warning that concurrent refreshes for
  one user can race into a spurious disconnect; it is a flag, not a failure
  to retry.
- **A `NOTE:` that users type their credentials at one site but stored
  tokens are sent to another** (`oauth2_code`, when `token_endpoint` or
  `revocation_endpoint` is on a different domain from `authorize_endpoint`).
  The call **succeeded**, and the note repeats on every later write of the
  same configuration. Some real backends split this way (Google signs people
  in at accounts.google.com and issues tokens at oauth2.googleapis.com), and
  it is also exactly what a configuration built to collect users' tokens
  looks like. Do not treat it as an error and do not quietly change
  endpoints to make it go away. Tell the user plainly that the sign-in page
  and the token address are on different sites, and confirm both addresses
  against the backend's own documentation before anyone connects. On shared
  hosting and SaaS domains the platform compares the full hostname, so two
  instances of one vendor (`dev1.service-now.com` and `dev2.service-now.com`)
  count as different sites and raise the note.
- **A `Note:` that stored credentials were invalidated although no endpoint
  changed** ("the connection was changed by another call while this one
  ran, or credentials were left under its name"). The call **succeeded**.
  Either someone else changed this connection between your read and your
  write, so credentials stored under their version were removed rather than
  carried back to yours, or this is a new connection and credentials an
  earlier one left under its name were removed. Those users were notified to
  reconnect. Run `list_connections` and check the stored definition is the
  one you meant before anyone connects. From platform v0.16.11 an
  overlapping edit is refused `app_busy` instead, so on an existing
  connection this note should be rare.

Tell the user in plain terms what just got stored (the backend's address and
how the app will reach it, kept encrypted on the platform). **Never echo a
secret** (a pasted token, a client secret) back into the conversation once
it's been sent.

**Updating a Connection later is a full replace, not a merge.** Resend
`label`, `strategy`, `config` and `scopes` with every call, not just the
field you're changing: omitting `scopes`, for instance, silently clears it.
The tool's description names the fields that are safe to omit. Run
`list_connections` before any re-call, per the approval gate above.

**`remove_app_connection` is the destructive one, and it is not the pause
switch.** It deletes the definition **and every credential the app's users
have already stored for it**; nothing is recoverable, and each user has to
connect again from scratch once a replacement definition exists. If the goal
is "stop this for now," that is `disabled: true` above. Reach for removal
only when the connection is genuinely going away, and confirm with the user
by name first: it is idempotent, but the first call already took the
credentials. It answers `app_busy` the same way as `set_app_connection`:
retry once after a moment, never in a loop.

## 5. Wire the app to consume it

In the app's code, use the template's `Connections` helper (from
`app/storage.py` in a Python container, `lib/storage.js` in a JS one) rather
than talking to the backend directly with a stored key. The whole trick is
passing through **this request's** `X-Caller-Assertion` header: that header
is what lets the platform hand back a credential for *the calling user*
rather than a shared one. The seam's answers are §2.2's **The app-facing
seam**, the app's prohibitions its **What the app MUST NOT do**, and
`get_app_security` §8 holds the three absolute rules for code that holds a
user's credential.

**Check the repo's client first.** If the repo's `app/storage.py` (or
`lib/storage.js`) has no `ConnectionLocked` or no `ConnectionsError`, it came
from an older copy of the template and cannot take the branches below: read
`references/older-template-client.md`, which says what breaks and how to
replace the client, before writing them.

**Reading the header inside an MCP tool.** A tool function isn't handed the
raw HTTP request as an argument, so you reach for it through the server's
request context, and the accessor differs by package. Pick the one that
matches what the app actually imports:

- **The official MCP Python SDK** (`mcp`): the default stack `inno-new-app`
  recommends for `mcp-container`, and where `mcp.server.transport_security`
  comes from. Declare a `Context` parameter on the tool; the inbound request
  hangs off it as `ctx.request_context.request`.
- **The standalone `fastmcp` package**: no `Context` parameter needed. Call
  `get_http_request()` from `fastmcp.server.dependencies` (the same module
  that provides `get_access_token`).

The sample below is written for the official SDK; the swap for standalone
`fastmcp` is in the comment at the top of it.

```python
from mcp.server.fastmcp import Context
from storage import Connections, ConnectionLocked, ConnectionsError, NotConnected  # template helpers

# On the standalone `fastmcp` package instead? Drop the Context import and the
# ctx parameter, and get the request from the dependency:
#   from fastmcp.server.dependencies import get_http_request
#   request = get_http_request()

connections = Connections()  # points at http://storage.internal by default

@mcp.tool()
async def list_incidents(ctx: Context) -> dict:
    # The gateway forwards X-Caller-Assertion on every request, empty when the
    # platform issues none (then the seam answers 503 connections_disabled,
    # a platform admin's to fix). Echo it either way; lookup is case-insensitive.
    request = ctx.request_context.request
    caller_assertion = request.headers.get("x-caller-assertion")
    try:
        cred = await connections.get("crm", caller_assertion)
    except ConnectionLocked:
        # Catch this BEFORE NotConnected (it is a subclass): connected, but
        # locked for this MCP client. Re-authorizing the client fixes it.
        return {"error": "Your CRM connection is locked for this assistant. "
                         "Re-authorize this connector (in Claude: /mcp, then "
                         "re-authenticate this server) and try again."}
    except NotConnected as e:
        # Do NOT swallow this: surface the link so the user can link once.
        return {"error": f"Not connected to your CRM: open {e.connect_url} "
                         "to link your account (one time), then try again."}
    except ConnectionsError as e:
        # Any other failed seam call: e.status is the HTTP status and e.code
        # the answer's error code (get_app_contract §2.2 says whose each is).
        if e.code == "connections_def_disabled":
            return {"error": "Your CRM connection is paused right now. "
                             "Try again later; you don't need to reconnect."}
        raise
    # cred is {"access_token": ..., "header": ..., "expires_at": ...}
    token = cred["access_token"]
    # ... make the backend call with `token`; keep it in memory only ...
```

In a JS container, `connections.get(name, callerAssertion)` takes the
assertion you read off `request.headers` in your `POST /mcp` handler, and the
same branches read:

```js
try {
  const cred = await connections.get("crm", callerAssertion);
} catch (e) {
  if (e instanceof ConnectionLocked) {
    return "Re-authorize this connector (/mcp → re-authenticate) and try again.";
  }
  if (e instanceof NotConnected) {
    return `Not connected to your CRM: open ${e.connect_url} to link your account (one time), then try again.`;
  }
  throw e;
}
```

Rules that hold regardless of language:

- **Pass the real inbound assertion, never a fabricated one.** Read it off
  the request you are serving right now and pass it straight through; don't
  hardcode it, cache it across requests or users, or invent one.
- **Never persist or log the assertion itself.** Echo it onto the seam call
  and drop it (§2.2's **What the app MUST NOT do** says why).
- On success you get back a live credential for *that* user (an
  `access_token`, or a ready-made `header`, depending on strategy) plus an
  `expires_at`. Use it for the backend call you're about to make; cache it
  **in memory only**, until `expires_at`, and never write it to disk, a
  database row, or a log line.
- On `NotConnected`, don't treat it as an error to swallow: relay the connect
  link it returns (`connect_url`) to the user in the words of §2.2's
  **Tool-copy convention**: *"Not connected to {Backend}: open {connect_url}
  to link your account (one time), then try again."* That's the one time this
  flow surfaces a URL instead of a plain-language sentence: it's a real link
  the user must click.
- **`ConnectionLocked` means connected, but locked for this MCP client**
  (`not_connected` with `locked: true`; §2.2's **The `locked: true` flag**
  says what produces it). **The fix is re-authorizing the MCP client**,
  never `connect_url`: in Claude, run `/mcp` and re-authenticate that server.
  Removing and re-adding the connector is usually not enough. Do **not** tell
  the user to reconnect the backend: connecting stores a credential, while
  only a new authorization writes the key into the grant, so they loop,
  connecting over and over while the app reports the same thing. Check for
  `ConnectionLocked` first, since it is a subclass of `NotConnected` and
  would otherwise be caught by the parent clause.
- **Every other non-success answer is not the user's fault**, so don't send
  any of them down the connect-link path. Each raises `ConnectionsError` in
  both template clients, with the HTTP status as `.status` and the answer's
  `error` code as `.code` (`null` in JS, `None` in Python, when the body
  carried none). Branch on `e.code`, as the sample above does, never on the
  message. §2.2's **The app-facing seam** lists every code and whose each is
  to fix; the ones a working app meets, and what it does:
  - **`503 connections_def_disabled`**: the Connection is **paused** by its
    owner or a platform admin, and the user's own connection is intact. Tell
    the user it is paused right now, not that they need to reconnect, and
    retry later.
  - **`503 connections_disabled`**, or any other `503`: the platform's own
    Connections setup is missing or broken. Nothing in the app fixes it:
    retry later, and tell a platform admin.
  - **`502 connections_upstream_error`**: the backend's own token endpoint
    failed while the platform was renewing the credential. The backend's
    outage, not the user's connection: retry later.
  - **`429 rate_limited`** (with `Retry-After: 60`): the seam's abuse brake.
    Wait the `Retry-After` interval, then retry. If a tool trips this in
    normal use, it is calling the seam per backend request instead of
    caching the credential in memory until `expires_at`.
  - **`401 connections_bad_assertion`** and **`403
    connections_not_declared`** are the **app's** to fix: echo the
    `X-Caller-Assertion` of the request you are serving now, not one kept
    from an earlier request, and check the connection name you passed
    against `list_connections`.
- Add a small `whoami` or status tool so the user (and you, while testing)
  can confirm the Connection is live and see which backend identity it
  resolves to, without needing to exercise a real feature first.

## 6. Verify

After shipping, have the user open the connect link once: they sign in on the
backend's own page (`oauth2_code`), paste the token they generated
(`secret_form`), or paste their API client's ID and secret
(`oauth2_client_creds`). For `oauth2_code` they must finish that sign-in in
the same browser that opened the connect link; a login completed anywhere
else is refused ("Finish in the browser you started in") and nothing is
stored. From then on, every tool call the app makes to that backend runs as
them, automatically, with nothing to repeat per session. Confirm it worked
using the `whoami` or status affordance from step 5 before calling the
feature done.

### Debugging: who is actually connected

Two MCP tools read and reset the *sessions* (the per-user side), and you
don't need any app code to use them. Prefer them over inferring state from a
failing tool call. Who may call each, and what it returns, is in its
description.

- **`list_user_connections`** answers who has connected their account to
  which backend. It is the fastest answer to "did my connect actually
  land?", and it works before the app's own `whoami` tool exists. It is
  distinct from `list_connections`, which lists the backend **definitions**
  an app has configured. When an address has passed from one person to
  another, read §2.2's **Visibility and oversight** (a stored credential is
  its account's) before concluding that a connect failed.
- **`disconnect_user_connection`** deletes one user's stored credential for
  one backend: the lever for "my connection is stuck, make it ask me again."
  It touches **one** user's session only, and the connection stays
  configured for everyone else, which is what makes it the right tool rather
  than `remove_app_connection`. It is **local only** and never revokes the
  credential at the backend, even for a user disconnecting their own
  session; to revoke upstream as well, the user disconnects from the
  **Connections tab on their account page**. Whether a reconnect shows the
  disclosure page again is the `connections.consent` setting's to say
  (`get_config` with `app` prints its description).

### Debugging: what the connect page is telling you

When the user reports an error page after opening a connect link, read
`references/connect-page.md` before changing anything: each title the page
can show has one meaning and one next step, and its most common one ("Not
available") deliberately hides which of several causes it is.

## References

- `references/discovery.md`: the probe recipe for step 2 when the user isn't
  sure how the backend signs people in (which `/.well-known/*` documents to
  fetch, how to read a `WWW-Authenticate` header, and how each finding maps
  to a config field), and the field mapping for an `oauth2_code` config in
  step 3.
- `references/oauth-client-request.md`: the copy-paste request for step 3
  when a backend admin needs to register the OAuth client.
- `references/connect-page.md`: what each connect-page error means and what
  to check, for step 6 when a user reports one.
- `references/older-template-client.md`: what an older template client lacks
  and how to replace it, for step 5 when the repo's client has no
  `ConnectionLocked` or no `ConnectionsError`.
