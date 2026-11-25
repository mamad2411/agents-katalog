---
name: homespun
description: >-
  Deploy a real multi-user web app from this conversation, then keep operating
  it. You author an HTML page plus a manifest; `homespun deploy` puts it live on
  its own URL with magic-link sign-in, a shared realtime database, per-role
  read/write/delete permissions, email notifications and file uploads. Owners
  invite other people, who sign in and use it together. You keep read and write
  access to the app's data and its change feed afterwards, so you can query it,
  write to it, watch it and redeploy it in later conversations. Use when the work
  deserves a persistent app people can return to and share, rather than a reply.
  Drives the `homespun` CLI: deploy, read/write data, watch for changes.
---

<!-- homespun skill v1.6.99 -->

# homespun

`homespun` deploys real web apps for you and keeps you connected to them. You
author an HTML page plus a manifest (what data it stores, who may read and write
each part of it), `homespun deploy` puts it live on its own URL, and the relay
supplies the parts you would otherwise have to build: sign-in, a shared database
with a live change feed, per-role permissions, email notifications and file
uploads. The owner invites whoever should have access, and they use it together.

You stay a first-class participant afterwards. Through the exact same collection
API the page itself uses, you can read the app's data, write to it, watch its
feed, and redeploy a new version to the same URL in a later conversation. The app
does not end when this conversation does.

## When to use this

Use `homespun` when the interaction is richer than a text reply, OR when it
should **persist**, OR when **more than one person** needs it: a dashboard
someone reopens next month, a list a household or a team edits together, an
intake form whose submissions you keep reading, a tool that outlives this
conversation. For a one-shot question, just ask in text.

There is no separate "form" primitive: a single-collection app with one page is
how you do the small case, and it is still a real app with a URL, sign-in and
data you can come back to.

## Choosing how to invoke Homespun

Prefer the available native file editor and shell to create, revise and validate
app files. Then use the Homespun interface already authenticated in this client
for account operations. In a persistent coding environment, an already
installed and authenticated CLI is also a good fit. Check that the CLI, its
identity and the needed network route are usable before relying on it; shell
availability alone is not enough.

For hosted MCP, the server cannot read a path in the agent sandbox. `html_path`
works only when a local stdio MCP server shares the filesystem; hosted MCP
rejects it. When the shell can reach the upload URL, `document_upload` bridges
the authored file into MCP deployment: compute the exact UTF-8 byte length and
SHA-256 hex digest, request a session with `{ size, sha256, app_id? }`, PUT the
unchanged raw UTF-8 bytes to `upload_url` with
`Authorization: Bearer <upload_token>`, then pass `document_id` to
`deploy_app`. The ticket only authorizes upload of those declared bytes, expires
after 15 minutes, and is not an account key. Identical ticket and deploy
parameters replay the original result for 24 hours; changed bytes or parameters
need a fresh session. Any network-capable shell can perform the PUT without the
Homespun CLI. Keep durable account secrets out of shell commands. If upload
network access is unavailable, use inline `html`. See `MCP-INVOCATION.md` for
the complete MCP tool flow.

## Setup

**This section describes the CLI route.** Everything below it assumes a
working `homespun` command and a key. Use it in a persistent coding environment
where the CLI is usable; MCP clients should follow `MCP-INVOCATION.md`. If you
were pointed here to set up the CLI, this is the whole of it: two commands,
then `references/registering.md` for the sign-in.

If the `homespun` command isn't on your PATH yet, install it first:
`npm i -g @homespunapps/cli`.

The hosted relay (`https://homespun.dev`) is the default: `homespun agent register`
works out of the box. The CLI needs:

- **An agent API key.** Either pre-provided by the operator (as
  `HOMESPUN_API_KEY`), or obtained yourself via `homespun agent register` (see
  `references/registering.md`). Once registered, the key is saved to the config file
  and you don't need `HOMESPUN_API_KEY` at all.
- **A relay URL.** Only relevant when targeting a relay other than the hosted
  default (local dev, staging): set `HOMESPUN_URL` (or pass `--url`) to point
  at it. Note this is the **control-plane** URL (where `deploy`/`apps`/`data`
  talk); the *deployed app itself* is served on its own domain (see "Serving
  and security" below), not under this URL.

Output is JSON on stdout. Errors are `{"error":{"code","message"}}` on stderr
with a non-zero exit.

<!-- homespun:core:start -->

## The data model: collections and the change feed

An app's *storage* is built from one primitive. Everything an app stores is a
**collection**, a named, mutable, queryable set of rows, each with a `key`, a
`data` payload, an optimistic-lock `version`, and an `author`. Every write
(create, update, delete) also lands on the app's **change feed**, an ordered log
you and the page can both subscribe to. One data primitive, one feed. There is no
separate "event" type and no template/app split: an app IS its HTML plus its
manifest plus its collections.

That covers storage only. An app also has an identity layer (sign-in, an owner,
members and roles), permissions expressed per collection and per operation, email
notification rules, scheduled sends, inbound webhooks and binary attachments. All
of those are declared in the same manifest and documented below.

**Append-only collections are how you get "events."** If you want an
audit trail or a one-shot journaled fact ("this happened") rather than a
mutable row, declare the collection `appendOnly: true` in the manifest (see
below) and only ever `create` into it, never `update`/`delete`. You get
exactly what a v1 "event" gave you (an ordered, immutable, replayable log),
expressed through the same collection API instead of a second primitive.

The three things you build:

1. **A manifest**, which declares the app's collections (with row schema and
   which roles may read, write and delete each), who the app is visible to,
   which email notifications it sends, which external hosts its page may fetch
   from, and whether it may load CDN scripts/styles.
2. **An HTML page**, which talks to its own data exclusively through
   `window.homespun.collections.*` and `window.homespun.feed`, injected by the
   relay at runtime, and reads who is signed in from `window.homespun.session`.
3. **Deploys**: `homespun deploy` puts the app live; `homespun deploy --app <id>`
   redeploys it in place, same URL.

After that, you (the agent) read and write the same collections the page
reads and writes, via `homespun data`, and watch the app's live feed via
`homespun apps watch`. You see the same data the people using the app see, from
the CLI.

**`homespun.collections` is a FLAT API, not per-collection objects.** Every
method takes the collection NAME as its first argument. There is NO
`homespun.collections.<collectionName>` object: `homespun.collections.bookings`
is `undefined`. Always pass the name as a string:

```js
homespun.collections.create("bookings", { name, slot });   // server mints the key
homespun.collections.snapshot("bookings");                 // returns the rows (array)
homespun.collections.get("bookings", key);                 // one row, or undefined
homespun.collections.on("bookings", (delta) => { ... });   // live deltas; returns unsubscribe
homespun.collections.update("bookings", key, data);        // optimistic-locked update
homespun.collections.delete("bookings", key);              // soft-delete (tombstone)
```

So `homespun.collections.snapshot("bookings")` returns the rows, but
`homespun.collections.bookings.snapshot()` throws (there is no `.bookings`
object to call `.snapshot()` on). Same for every method: the name is an
argument, never a property.

**Querying a collection server-side (`list`).** `snapshot` returns the whole
in-memory mirror; `homespun.collections.list(name, { where, sort, limit })` is a
NETWORK read that asks the relay to **filter and order DB-side** and return a
page - use it to fetch just a subset (a status, a date range) without pulling
everything into the mirror. `where` is an **AND** of `{ field, op, value }`
conditions; `op` is one of `eq` / `neq` / `in` / `notIn` / `gt` / `lt` / `gte` /
`lte`, with the **same pinned comparison semantics as a notify `when`** (same-
type only, no coercion, dates compared as ISO-8601 strings; `in`/`notIn` take a
non-empty array). `sort` is a `{ field, dir }` list (`dir` `"asc"`/`"desc"`).

```js
const page = await homespun.collections.list("tasks", {
  where: [
    { field: "status", op: "in", value: ["open", "blocked"] },
    { field: "due", op: "lte", value: "2026-01-31" },
  ],
  sort: [{ field: "due", dir: "asc" }],
  limit: 50,
});
// page.rows, page.next_cursor, page.has_more
```

The agent side is the same query over the CLI: `homespun data <app> <coll> list
--where '<json-array>' --sort '<json-array>'`. Two rules to know:

- **The filter never widens what you can read.** Read permission + any row
  scoping are applied FIRST, then the filter - so a filtered list is always a
  **subset** of what you could already read. A caller who cannot read the
  collection is refused (`collection_read_forbidden`) whether or not a filter is
  present. **Field names are restricted** to simple identifiers (letters,
  digits, `_`) and both field names and values are passed to the database as
  bound parameters, so a query can never be used for injection.
- **Pagination.** A `where` filter works with the normal `since`/`next_cursor`
  cursor. A custom `sort` returns a single page (raise `limit` to see more) and
  cannot be combined with `since` in this version. Arbitrary-field filtering is
  currently unindexed, so keep collections that you filter heavily modest in
  size.

**The row shape you read back.** Every row the page reads (via
`homespun.collections.snapshot(name)`, `homespun.collections.get(name, key)`,
and the `row` on an `upsert` delta from `homespun.collections.on(name, ...)`)
is a `HomespunRow` with exactly these fields, camelCase, translated from the
snake_case wire at the SDK boundary:

```ts
{
  key: string;        // server-minted row id
  data: unknown;      // the payload you wrote
  version: number;    // optimistic-lock counter
  author: { kind: "human" | "agent" | "grant" | "visitor" | "anon"; id: string };
  createdAt: string;  // ISO 8601 timestamp (camelCase, NOT created_at)
  updatedAt: string;  // ISO 8601 timestamp (camelCase, NOT updated_at)
}
```

The row's `author` is **server-stamped and tamper-proof**, but read the name
carefully: it records who wrote the row **LAST, not who created it**. Every
update rewrites it, so a row Alice created and Bob (or your own agent) later
edited comes back with Bob as its `author`, and Alice is not recorded anywhere
on the row afterwards. `createdAt` tells you WHEN a row was created; nothing on
the wire tells you by WHOM. If you need "the person who created this row" as a
permission boundary, that is the `creator` subject in the manifest (see "Who may
change a row" below), enforced server-side, not a field you read back here.

Its `kind` is one of `"human"`, `"agent"`, `"grant"` (a grant-link holder),
`"visitor"` (a recognised anonymous visitor on a public/link app, see "Visitors:
recognising someone with no account"), or `"anon"` (the sentinel for a writer
with no identity at all: an app that mints no visitor identity, and every row
written before visitor identities existed). **That is a DIFFERENT enum from
`homespun.session.kind`**, whose values are `"owner"`, `"member"`, and
`"anonymous"`. So do not special-case `row.author.kind === "anonymous"` to
mirror the session enum: it silently never matches, because a row author uses
`"anon"`. Resolve an author to a display name with
`homespun.members.nameFor(row.author)`.

Storing a self-declared name is fine and is not the same thing as attribution:
a guestbook, RSVP, or booking legitimately keeps the responder's stated name
in `data` (e.g. `data.name`), and you should render it as what they called
themselves. The one rule is that a self-declared field is never PROOF of who
wrote the row. Render `data.name` as their stated name and
`homespun.members.nameFor(row.author)` as who actually wrote it last
(server-stamped); never treat the former as the latter.

**Anonymous visitors on a PUBLIC (or LINK) app get a session automatically,
with no login.** The relay hands every visitor an anonymous session
(`homespun.session.kind === "anonymous"`), and a collection whose `write` list
includes `"anyone"` accepts writes from those anonymous visitors. That is what
makes public forms (bookings, RSVPs, contact submissions) work: any visitor
can `homespun.collections.create("bookings", ...)` with no per-visitor token,
no login, and no participant to mint first. (You will NOT see a `GET
/_hs/session` error for these visitors: on a public/link app that endpoint
answers 200 with an explicit anonymous marker rather than an alarming 401.)

**A PRIVATE app gates anonymous visitors with a sign-in page automatically. A
PUBLIC (or LINK) app does not: it serves the page straight to them, with no
sign-in prompt anywhere.** That is the point of public, but it has a
consequence you must design for: **if a public/link app has ANY owner-only or
member-only surface (a `read: ["owner"]` collection, an admin panel,
a moderation view), the page MUST render its own sign-in control, or the owner
can never reach it.** They will open their own app, be handed an anonymous
session like everybody else, and stay `kind: "anonymous"` forever. Nothing in
the platform offers them a way in on a public app; only your page can.

The control is one line: `homespun.session.login()` (see "Recipe: public
submits, only the owner reads"). Note also that sessions are **per-origin**:
being signed in on the main site does NOT sign a person in to
`<slug>.<usercontent-domain>`. Only the `/authorize` hand-off `login()`
triggers creates an app session on the app's own origin.

**Email a person when a collection changes (`notify`).** Declare a `notify`
array in the manifest to have the relay send a plain-text email when a row is
created or updated. This is declarative: you write the rule, the relay resolves
the recipients and sends. A recipient is always a principal the platform
already knows, resolved to that principal's own verified account email (or,
for the `submitter` target below, the address the row's own author entered),
never an address named in the manifest or the row, so a manifest can never
email an arbitrary stranger.

```json
"notify": [
  {
    "on": "create",
    "collection": "bookings",
    "to": ["owner"],
    "subject": "New booking: {{name}}",
    "body": "{{name}} booked {{slot}}."
  },
  {
    "on": "update",
    "collection": "bookings",
    "when": { "field": "status", "changedTo": "confirmed" },
    "to": ["owner", "members"],
    "subject": "Confirmed: {{name}}",
    "body": "{{name}}'s booking for {{slot}} is now confirmed."
  }
]
```

Rules of the road:

- **`on`** is `"create"` or `"update"`. **`collection`** must be one you declared.
- **`to`** is a non-empty array drawn from a closed target grammar:
  `"owner"`, `"members"`, `"submitter"`, `"author"`, `"creator"`,
  `"role:<name>"` (a declared custom role) and `"field:<relationName>"` (a
  declared relation on the rule's own collection). A literal email address is
  always rejected at deploy. `"owner"` and `"members"` resolve to *verified
  account emails*. `"submitter"` (see "Confirmation emails" below) emails the
  person who submitted the row, at the address they themselves entered; it is
  only allowed when the rule declares a `submitterEmailField`, and only when
  the operator has enabled the external path (otherwise the rule is rejected
  at deploy with `notify_submitter_not_enabled`). Every target, including
  `"owner"` and `"members"`, is authorized against the triggering row before
  it is sent, so a resolved recipient who cannot read that row receives
  nothing rather than an email. See the reference below before targeting a
  role or a relation.
- **`when`** is optional and holds exactly ONE operator besides `field`. The
  *level* forms fire whenever the after-write value satisfies the comparison:
  `equals` / `notEquals` (`{ "field": "x", "equals": "v" }`), `in` / `notIn`
  (`{ "field": "status", "in": ["paid", "shipped"] }`, a non-empty array), and
  `gt` / `lt` / `gte` / `lte` (`{ "field": "amount", "gte": 100 }`). The one
  *edge* form, `{ "field": "x", "changedTo": "v" }`, fires only on the
  *transition* into that value (`update` only) - so "status BECAME confirmed"
  emails once, not on every later save where it is already confirmed. Omit
  `when` to fire on every create/update.
  - **Comparison semantics (pinned).** Comparisons are **same-type only and
    never coerce**: a stored number never matches a string operand and vice
    versa. Numbers compare numerically; strings (and **dates written as ISO-8601
    strings**, e.g. `"2026-01-31"`) compare lexicographically. A **missing or
    null field never fires any operator** - including `notEquals`/`notIn`, so a
    row that lacks the field is never treated as "not equal".
  - **`field`** names one of the row's OWN top-level keys - the same single-row,
    top-level-only scope the `{{fieldKey}}` templates use. There are no nested
    paths (`a.b`), no array indexing, and no cross-row aggregates ("email me when
    there are 10 signups" is not expressible in a `notify` rule; count
    client-side or in the agent instead).
- **`subject`** / **`body`** are plain-text templates. The only dynamic piece is
  `{{fieldKey}}`, interpolating one top-level row field as literal text (a
  missing field renders empty; there are no expressions, paths, or HTML). Values
  are escaped, so a submitted value can never inject into the subject or a mail
  header.
- A burst of writes to one rule is **coalesced into a single digest email** per
  recipient, and each app has an hourly send cap - so a flood of public
  submissions can't bury an owner's inbox. A failed send never affects the
  write; the row is saved regardless.
- **`channels`** is an optional non-empty array naming which transports carry
  the rule, defaulting to `["email"]`. **`excludeActor`** is an optional
  boolean deciding whether the write's own actor is dropped from the resolved
  audience; its default depends on the rule's own targets and channels. Both
  are covered in full in the reference below.

> **Read `references/notify-targets.md` before writing a `to` that names
> `"role:<name>"`, `"field:<relationName>"`, `"author"` or `"creator"`.** It
> has the full grammar for each, worked examples (including the relation
> declaration `field:` depends on), the `channels` and `excludeActor` keys,
> and a worked example of the row-level authorization gate that silently
> suppresses a recipient who cannot read the row that fired the rule, which is
> the single most common way a rule looks broken while working exactly as
> declared. Do not target a role or a relation from memory: the authorization
> interaction is not guessable and getting it wrong reads as a missing
> notification rather than as an error anywhere.
>
> If this skill reached you over HTTP rather than as files on disk, fetch it
> with `homespun skill show --section notify-targets`, or
> `GET <relay>/skills/homespun/references/notify-targets.md`.

**Confirmation emails to the submitter (`to: ["submitter"]`).** To email the
person who submitted a public form - an order/booking/signup confirmation - add
`"submitter"` to `to` and declare **`submitterEmailField`**, the name of the row
field that holds the email address they entered. The relay emails *that row's
own submitted address, and only that address*.

```json
"notify": [
  {
    "on": "create",
    "collection": "signups",
    "to": ["submitter"],
    "submitterEmailField": "email",
    "subject": "Thanks for signing up, {{name}}",
    "body": "We received your signup and will be in touch."
  }
]
```

How the consent + anti-abuse rules keep this safe:

- **Consent gate.** `"submitter"` is allowed **only** when the rule declares a
  `submitterEmailField`, and (when the collection has a schema) that field must
  be a real declared field of the collection. A `to: ["submitter"]` rule without
  `submitterEmailField` is a hard deploy error. The address is read from the row
  the submitter themselves wrote - the manifest can never *name* an address, so a
  confirmation can never be aimed at the owner, a member, or any third party.
- **Own-address-only.** The recipient is always the row's own
  `submitterEmailField` value. If that value is missing, blank, or not a plausible
  email, the confirmation is silently dropped (nothing is sent, nothing retries).
- **Single-use.** A given row is confirmed **at most once per rule**, even if the
  row is later updated - a row edit never re-spams the submitter. (Use two
  distinct rules if you want a separate confirmation-vs-update email.)
- **Per-app daily cap.** External confirmations are bounded by a per-app daily
  cap, separate from the owner/member hourly cap, so a flood of public
  submissions cannot spray unbounded confirmation mail.
- **Operator flag.** The whole external path is gated behind the relay's
  `NOTIFY_EXTERNAL_ENABLED` setting. While it is off (the default), any
  `to: ["submitter"]` rule is rejected at deploy. The hosted relay has it enabled.

**Fire on a date (`schedules`), by email or webhook.** Where `notify` fires on a change,
`schedules` fires on a **date**: declare a `schedules` array to have the relay
email the owner/members a set number of days before, on, or after a date stored
in a row. A once-a-day scan at **08:00 in the app's time zone** finds rows whose
`dateField + offsetDays` equals today and sends. Recipients resolve to verified
owner/member emails exactly like `notify`, and delivery reuses the same digest +
hourly cap, so a schedule can never email a stranger either.

```json
"schedules": [
  {
    "collection": "bills",
    "dateField": "dueDate",
    "offsetDays": -3,
    "to": ["owner"],
    "subject": "Bill due soon: {{name}}",
    "body": "{{name}} ({{amount}}) is due on {{dueDate}}."
  }
]
```

Rules of the road:

- **`collection`** must be one you declared; **`dateField`** must be a field of
  it holding a calendar date (an ISO `"YYYY-MM-DD"` string is ideal; a full ISO
  datetime or epoch-millis number is interpreted in the app's time zone; an
  unparseable/missing value is skipped, never fired).
- **`offsetDays`** is an integer: **negative = before** the date (`-3` = "3 days
  before"), **`0` = on the day**, **positive = after**. The reminder fires when
  `dateField + offsetDays` is today in the app's time zone.
- **`to`** is a non-empty array of `"owner"` and/or `"members"` (same closed role
  set as `notify`; `"submitter"` and literal addresses are rejected).
- **`when`** is an optional *level* condition evaluated against the row on the
  fire day - any of the level operators `equals` / `notEquals` / `in` / `notIn` /
  `gt` / `lt` / `gte` / `lte` (same pinned same-type, no-coercion, dates-as-ISO-
  strings semantics as `notify`), e.g. only remind while `status` is `"unpaid"`,
  or while `amount` is `{ "gte": 100 }`. (The `changedTo` *edge* form is not
  valid here, since a scheduled scan has no before-state.) Omit `when` to remind
  for every row.
- **`subject`** / **`body`** are the same `{{fieldKey}}` plain-text templates as
  `notify`.
- **A rule may fire a WEBHOOK instead of an email.** Swap `to`/`subject`/`body`
  for `url` (or `urlFromSetting`), plus the optional `connection` and
  `bodyTemplate`, and the same date match POSTs to your endpoint instead of
  mailing anyone. A rule fires **exactly one** action: declaring both an email
  and a webhook shape, or neither, is a deploy error naming which. The delivery
  is the same signed, retried, SSRF-guarded path `webhooks` uses, so the
  mechanics live with it in `references/webhooks.md` under "A schedule that
  fires a webhook". Reach for it to drive a machine off a date (expire a
  listing, poke a fulfilment system, nudge a Slack channel) rather than a person.
- **Recurrence is client-driven**: the relay is a dumb date-matcher and fires a
  given row **exactly once per date** (a re-scan, restart, or replica never
  re-alerts). For a recurring reminder, have your page advance the date field
  after each occurrence (e.g. set `nextDue = lastDone + interval`); the next
  date then becomes the next reminder.
- The app's **time zone** is an IANA name like `Europe/Berlin`; unset means UTC,
  so every reminder fires at **08:00 UTC** until you set one. Deploying an app
  that declares `schedules` with no time zone set returns a `warnings[]` entry in
  the deploy result saying exactly that. Set the zone with `homespun apps update
  <app> --timezone <IANA zone>` (it then shows up under `homespun apps show`).
  Free apps have a per-day reminder cap and a rule-count cap, both modest by design.
- **Need a worker on a timer, not an email or webhook relative to a row date?** Use
  `agentTasks` with `on: "schedule"` (`every` or `cron`). It wakes the owner's
  `homespun work` worker on a clock and needs no cron on the machine. See the
  `agentTasks` section and `references/agent-tasks.md`.
- **The whole feature is gated on the relay's `SCHEDULES_ENABLED`, and a deploy never tells
  you.** It is **enabled on the hosted relay**, so reminders fire there. On a self-hosted relay
  with it off, the scan worker simply never starts: the manifest still validates, the deploy
  still succeeds, and no reminder ever fires. So on a self-hosted relay a successful deploy is
  **not** evidence a reminder will arrive, so check the variable.

**POST to a URL when a collection changes (`webhooks`).** The machine-consumer
sibling of `notify`. Instead of emailing a person, the relay fires a signed HTTP
`POST` to a URL you name, so an app can push its row changes to Slack, Zapier, a
CRM, or another agent. It uses the same `on` / `collection` / `when` trigger
grammar as `notify` above, and it can carry a stored credential (static token or
full OAuth2) so it writes straight into a third-party API.

> **This section lives in a separate file. Read it before writing a `webhooks`
> rule** (`references/webhooks.md`, alongside this SKILL.md). It has the payload
> shape, the HMAC signature and how to verify it, the at-least-once delivery and
> idempotency rules, the Connections API, the generic OAuth2 setup, and the
> host-binding rule that stops a credential being sent to the wrong host. Do not
> author a webhook rule from memory: the signing and host-binding details are not
> guessable, and getting them wrong either fails silently or sends a token
> somewhere it should not go.
>
> If this skill reached you over HTTP rather than as files on disk, fetch it with
> `homespun skill show --section webhooks`, or
> `GET <relay>/skills/homespun/references/webhooks.md`.

<!-- homespun:core:end -->


## Keeping this skill up to date

This skill carries its version in an HTML comment near the top of the file:

```
<!-- homespun skill vX.Y.Z -->
```

**The skill version is the homespun package version** (`@homespunapps/relay`,
`@homespunapps/cli`, `@homespunapps/core`, all kept in lockstep by the release
script). `scripts/cut-release.sh` updates this comment alongside the
`package.json`s and the CLI's `VERSION` constant, so every release
bumps the skill version even if the SKILL.md content didn't change.
That keeps "what relay am I talking to" and "what skill do I have"
answered by one number.

The relay you talk to publishes its own version of this skill at
`GET /skills/homespun/SKILL.md/version`. **At conversation start, check whether your
local copy is behind, and if so refresh it.**

The check is a short shell snippet:

```sh
LOCAL_VER=$(grep -m1 -oE '<!-- homespun skill v[0-9]+\.[0-9]+\.[0-9]+' <path-to-your-local-skill> | grep -oE '[0-9]+\.[0-9]+\.[0-9]+$')
REMOTE_VER=$(homespun skill version --plain)
# If the relay is on an old image that lacks a version comment, the probe
# returns "0.0.0". Don't clobber a newer local copy with the older relay
# skill; skip the update and proceed with what's local.
if [ "$REMOTE_VER" = "0.0.0" ]; then
  : # nothing to do
elif [ "$LOCAL_VER" != "$REMOTE_VER" ]; then
  homespun skill show > <path-to-your-local-skill>   # overwrites with the relay's current skill
fi
```

Where `<path-to-your-local-skill>` is wherever YOUR runtime stores the
homespun skill (e.g. `~/.claude/skills/homespun/SKILL.md` for Claude Code,
`~/.cursor/rules/homespun.mdc` for Cursor, the relevant section of
`~/.codex/AGENTS.md` for Codex / Gemini-style concatenated files).

The two `grep`s above are intentionally strict:

- `-m1` stops at the first match in the file, so prose mentions of the
  pattern (this very section!) don't double-count.
- `[0-9]+\.[0-9]+\.[0-9]+` only matches a real semver triple, so a
  literal `<!-- homespun skill vX.Y.Z -->` in documentation is skipped.

Rules:

- If the local file has no `<!-- homespun skill v... -->` comment, treat it as
  stale and run `homespun skill show > <path>`.
- If `REMOTE_VER` is `0.0.0`, skip the update: the relay is on an old
  image without a version comment, and clobbering your (presumably newer)
  local copy with that would be a downgrade.
- If the network is unreachable or `homespun skill version` fails, **do not
  update**: proceed with the local skill you have.
- Don't loop. Check once at conversation start; if you've already refreshed in
  this run and it's still mismatched, stop and report the error to
  the human.
- If you've hand-edited the local skill (added your own notes), save your
  changes first, because `homespun skill show > <path>` is a clobbering write.

## Discover the CLI with `--help`

**Before using a command, run its help.** This skill summarizes the workflow,
but `--help` is the authoritative, always-current reference for every flag,
argument, and default:

- `homespun --help`: the command list and global options.
- `homespun <command> --help`: every flag and option for that command, e.g.
  `homespun deploy --help`, `homespun apps --help`, `homespun apps watch --help`,
  `homespun data --help`.

If a command errors or you are unsure of an option name, **run `--help`
instead of guessing**: the CLI is self-documenting and the help text reflects
the installed version, which this skill may not.

### If `homespun` exits 75 ("CLI upgrade required")

The relay you're talking to needs a newer `@homespunapps/cli` than you have
installed. The CLI signals this with **exit code 75** (`EX_TEMPFAIL`) and a
stderr message that starts with `homespun: this relay requires @homespunapps/cli >=
<version>`. If that message includes a `To upgrade: <command>` line, the
command is correct for how `homespun` was installed on this machine, so there's
nothing to guess.

What to do, in this order:

1. **Run the printed upgrade command once.** If no command is printed (the
   message says "vendored" or "unknown" install), stop and ask the human to
   bump `@homespunapps/cli`; don't try to install one yourself.
2. **Re-run your original `homespun` command once.** If it succeeds, continue.
3. **If it still fails with exit 75 after one upgrade + retry**, stop and
   report the error to the human. Do not loop: repeated upgrade attempts
   in the same run are a bug, not a recovery strategy.

**Registering, and claiming.** Before you can deploy you need an agent API key,
and that key needs a human owner. If `homespun agent register` and
`homespun deploy` already work for you, you are past this and can skip it.

> **Read `references/registering.md` if you do not yet have a working key**, or
> if a command fails with `agent_not_claimed` or `unauthorized`. It has the
> registration flow, where the key is stored, and the claim handshake that
> attaches you to a human. Do not guess at a workaround for `agent_not_claimed`:
> the fix is a claim code only the human can mint.
>
> Over HTTP rather than on disk: `homespun skill show --section registering`.
<!-- homespun:core:start -->

## Authoring an app: the manifest

The manifest is a plain JSON Schema 2020-12 document with one namespaced
extension key, `x-homespun-manifest`. It is the **whole consent surface**: what
it declares is exactly what the relay enforces at runtime, so be as precise
as you can: unknown keys are hard rejected (a typo is a deploy-time error,
never silently ignored), and there are no implicit grants: `owner` is never
auto-added to a permission list.

**Visibility is not a manifest field.** Whether an app is `private`, `link`,
or `public` is a deploy-time flag (default `private`; with the CLI,
`homespun deploy --visibility <private|link|public>`), not something you
declare in this manifest. There is no visibility key here to set, so don't go
looking for one when building a public app. The manifest governs what data the
app stores and who may write it; visibility governs who may open the app at all
(see "Serving and security").

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$defs": {
    "GroceryItem": {
      "type": "object",
      "properties": {
        "name": { "type": "string", "maxLength": 200 },
        "checked": { "type": "boolean" }
      },
      "required": ["name"]
    },
    "AuditEntry": {
      "type": "object",
      "properties": {
        "action": { "type": "string" },
        "detail": { "type": "string" }
      },
      "required": ["action"]
    }
  },
  "x-homespun-manifest": {
    "app": {
      "name": "Grocery list",
      "description": "Shared household grocery list",
      "icon": "🛒"
    },
    "collections": {
      "items": {
        "schema": { "$ref": "#/$defs/GroceryItem" },
        "read": ["owner", "member"],
        "write": ["owner", "member"],
        "delete": ["owner", "member"]
      },
      "audit": {
        "schema": { "$ref": "#/$defs/AuditEntry" },
        "read": ["owner"],
        "write": ["owner"],
        "delete": ["owner"],
        "appendOnly": true
      }
    },
    "externalHosts": ["https://api.example.com"],
    "cdn": false
  }
}
```

> **SAFETY: `read` is MANDATORY on every collection.** A deploy that leaves it
> off is refused, `permission_role_invalid`, naming the collection. This is not
> paperwork: an ABSENT `read` never meant "nobody can read", it meant EVERYONE
> who can open the app reads every row, which on a `public` or `link` app is
> every anonymous visitor on the internet. That default was taken up by silence
> rather than by choice on most collections ever deployed, so silence stopped
> being an available answer. Say which you mean:
>
> - `"read": ["owner"]` for anything a person would not want shown to
>   strangers (names, emails, phone numbers, messages, orders, bookings, any
>   personal data). Add `"member"` when staff read it too.
> - `"read": ["creator"]` for "everyone sees only their own rows".
> - `"read": ["anyone"]` when the data really is public. This is exactly the old
>   absent-key behaviour, written down, and it is perfectly legal: a menu, a
>   published schedule, a price list.
> - `"read": []` when nobody reads the rows through the data API at all (an
>   audit log you only ever read as the owner, for instance, would still list
>   `"owner"`).
>
> Pick the narrowest one that works. Every visitor can hit the data API
> (`GET /_hs/c/<collection>`) directly, so the page is never what protects the
> rows, the `read` list is.
>
> **Rule of thumb: collecting data FROM the public? Restrict who can READ it.**
> The "public submits, only the owner reads" recipe below is exactly this shape:
> `orders` sets `read: ["owner"]` because the submissions are private, while
> `menu` sets `read: ["anyone"]` because it is meant to be world-readable.
>
> Adding a `read` list to a collection that never had one is **never** blocked
> by the redeploy compat check. Silence already granted the widest scope there
> is, so any list you write is at most as wide, and a narrowing needs no
> re-consent. Bringing an older app into compliance is a plain redeploy.
> (An app published to the community before the key became mandatory still
> installs and trials fine; only a new deploy is held to the rule.)

Fields, exactly:

- **`x-homespun-manifest.app`**: `name` (required, ≤80 chars), `description`
  (≤280 chars), `icon` (a single **pictographic** emoji: a geometric/symbol/
  letter/digit codepoint such as the half-circle "◐" is rejected with
  manifest_invalid, "icon must be an emoji, not a letter, digit, or symbol").
  Shown to the human as the app's display
  identity, and used to build the served page's head identity automatically:
  the relay injects a favicon (`icon` rendered as an SVG, falling back to the
  Homespun mark), a `<title>`/meta description, and Open Graph / Twitter
  share-preview tags (a generated 1200x630 card from the name, description,
  and icon) into every served document. Any of these tags you write in your
  own HTML win: the relay never duplicates or overrides an author-supplied
  `<title>`, meta description, icon link, or og/twitter tag. Two optional
  keys tune this:
  - **`indexable`**: boolean, default `false`. Search indexing is OPT-IN:
    every app ships `noindex` (robots meta + `X-Robots-Tag` header, and its
    host's robots.txt disallows crawling) until you set `indexable: true` on
    a **`public`** app, which flips the robots.txt to allow, drops the
    noindex signals, and lists the app in the platform sitemap. The flag has
    no effect on `link`/`private` apps: their visibility is the access
    control and they are never indexable.
  - **`ogImage`**: an `https://` URL (≤2048 chars) used as the share-preview
    image (`og:image`/`twitter:image`) instead of the generated card. The
    relay never fetches it; it is only emitted as the meta-tag value.
- **`x-homespun-manifest.collections`**: a map of collection name →
  `{ schema?, read, write, update?, delete, countRead?, relations?, keyClaim?,
  immutable?, serverSet?, appendOnly?, unique?, retention?, mirror?,
  anonWriteBudget?, antiAbuse?, seedOnInstall? }`.
  An app may declare zero collections (a purely presentational app).
  - **`schema`**: `{ "$ref": "#/$defs/<Name>" }` into the document's own
    `$defs`. Optional: omit it for a schemaless collection (rows validated
    only at your own discretion). Cross-document refs are not supported.
    **A declared schema is STRICTLY ENFORCED:** any `create`/`upsert`/`update`
    whose `data` fails the schema is rejected `422 row_schema_violation`, with
    the failing JSON Schema paths listed in the error's `details`. Nothing in
    this block is advisory: `schema`, `write`, `update`, `delete`, `read` and
    `appendOnly` are all enforced by the relay on every request, through the
    same door for browser visitors and for you as the agent. A non-conforming
    write never lands.
  - **`write`**: required, non-empty array of roles that may CREATE rows in
    this collection (`create`, and the create half of `upsert`). It ALSO gates
    updates unless the collection declares its own `update` list, so on a
    collection with no `update`, `write` means "may add rows **and** may
    overwrite every row already in the collection, including other people's".
    Read "Who may change a row" below before you leave it that way. Putting
    `"anyone"` in `write` makes `update` **required**, so the dangerous half of
    that sentence can no longer be reached by saying nothing.
  - **`update`**: array of roles that may change an EXISTING row (`update`, and
    the update half of an `on:`-field upsert). **Omitted means "same as
    `write`"**, so a collection that leaves it off is governed by `write` for
    both halves. **REQUIRED whenever `write` includes `"anyone"`**: leaving it
    off there is refused at deploy with `permission_role_invalid`, because the
    inherited list would let any anonymous caller overwrite rows it did not
    create. Every affirmative answer stays legal, including `update: ["anyone"]`
    if you genuinely want the inherited behaviour, said out loud. The one
    exception is `appendOnly: true`, which already refuses every update and so
    neither needs nor permits an `update` list. Optional everywhere else.
    Declare it to split adding from editing:
    `write: ["anyone"]` plus `update: ["creator"]` is "anyone may add a row,
    only the person who created it may change it", which `write` alone cannot
    express. It takes the same subjects `delete` does, including the
    row-scoped `creator` / `editor` / `author`, because by the time it is
    checked a target row exists. An explicit `update: []` is legal and means
    nobody may update: rows can be created and deleted but never edited. (For
    "never edited AND never deleted", use `appendOnly` instead, and use it
    *alone*: declaring `appendOnly: true` alongside any `update` list, empty or
    not, is rejected at deploy as a contradiction.)
  - **`delete`**: required, non-empty array of roles that may delete rows.
  - **`read`**: **required** array of roles. **It IS enforced, server-side, on
    every read** (list, single-row get, and the live change feed), exactly the
    way `write` and `delete` are. Semantics:
    - **Omitted**: rejected at deploy, `permission_role_invalid`, naming the
      collection. It used to be optional, and an omitted list meant anyone who
      could open the app could read every row: on a public/link app, every
      anonymous visitor. Nothing about that default has changed for apps that
      already carry it, and a stored manifest is still re-validated leniently so
      an app published under the older rule keeps installing. What changed is
      that you can no longer arrive at it by saying nothing. Write
      `"read": ["anyone"]` if that is what you want.
    - **`[]` (empty)**: legal, and the opposite of omitting it. Nobody may read
      the rows through the data API. Note that this includes you: an agent
      that needs to read the collection must list `"owner"`, since an agent
      principal carries its owner's authority automatically (there is no
      separate `"agent"` role to list; see the **`Roles`** entry under
      `x-homespun-manifest.collections` below).
    - **Declared, and the caller holds one of the listed roles**: the read is
      allowed and returns every row.
    - **Declared, and the caller holds none of them** (including an explicit
      empty `read: []`): the read is refused `403 collection_read_forbidden`,
      whose `hint` names the roles the collection requires. This applies to the
      data API itself, so a visitor calling the collection endpoint directly is
      refused just as the page would be.
    - **A row-scoped `read`** (`["creator"]`, `["editor"]`, or the older
      `["author"]`) scopes reads to the caller's *own* rows: a list returns only
      the rows that match, and a get on a row that does not returns `404
      row_not_found` (the same error a missing key returns) rather than a 403,
      deliberately, so a caller cannot probe which keys exist. **Every other
      verb answers the same way**: an update, a delete, and a keyed upsert that
      lands on an existing row all return `404 row_not_found` for a row `read`
      does not reach for you, rather than a 403 (or, for the upsert, rather than
      the row body). The write doors never confirm a key the read door refused
      to confirm. On a row you *can* read, a refused update or delete still
      returns the honest `403 collection_write_forbidden` /
      `collection_delete_forbidden` with the roles that were consulted. **Prefer
      `creator`**: `editor` and `author` both mean "wrote it last", so the first
      time anyone else touches a row it drops out of its original writer's view.
      An anonymous visitor to a public/link app satisfies these through the
      per-browser visitor identity, so `read: ["creator"]` means "each visitor
      sees their own rows" (see "Visitors: recognising someone with no
      account"). A caller with no identity at all, including a visitor on an app
      that declares nothing a visitor could reach, is refused `403` outright.
    - Matching is **literal, with no implicit grants beyond the platform's
      `owner` ⇒ `member` hierarchy** (see "Roles your app defines" below):
      `read: ["member"]` does not silently include a declared custom role, and
      under a bare row-scoped read list even the owner is scoped to their own
      rows unless they also list `"owner"`. This already covers you: an agent
      principal always carries its owner's authority, so `read: ["owner"]`
      admits you with no separate entry needed.
    - `read` is applied **on top of** app visibility, never instead of it: a
      `private` app still requires a signed-in session before any read role is
      even considered.
  - **`countRead`**: optional array of roles. Opts the collection into a
    **count-only public aggregate**: the roles listed may read the collection's
    live row COUNT without being able to read the rows. It is fully independent
    of `read`, so the common shape is `read: ["owner"]` + `countRead:
    ["anyone"]`: the owner reads the rows, everyone sees only how many there
    are (the "3 spots left" counter without exposing who signed up). Semantics:
    - **Omitted** (default): no one may read the count; the endpoint refuses
      `403 collection_count_forbidden`. A collection never leaks a count it did
      not opt into.
    - **Declared**: a caller holding one of the listed roles may `GET
      /_hs/count/<collection>` (or call `homespun.collections.count(name)`) and
      gets `{ "count": N }`, the number of live rows only, never any row data
      and no field values. A plain-role list is a whole-collection total with
      no filtering, which is the "3 spots left" shape.
    - **A row-scoped subject returns the caller's OWN count.** `countRead`
      takes the same vocabulary `read` does: `countRead: ["creator"]` is "how
      many rows have I added", and a declared relation is "how many name me".
      The count is filtered by exactly the predicate the same subject filters a
      *list* by, so it can never include a row the caller could not have
      listed. This replaces the two-collection split apps used to write to fake
      a personal counter. A caller with no identity at all is refused rather
      than handed a zero.
    - It does **not** relax `read`: the rows stay exactly as protected as
      before, so this is safe to add to a collection that captures private
      submissions.
    - **Known leak, and it is on you to avoid it:** a whole-collection
      `countRead: ["anyone"]` beside a row-scoped `read` is an existence
      oracle. The rows are private, but a polled total moves by one on every
      create and delete, so on a low-volume collection an outsider learns when
      individual rows appear and vanish. If the number is meant to be personal,
      scope it (`countRead: ["creator"]`); publish the whole-collection total
      only when the total itself is genuinely public.
  - **`relations`**: optional object mapping a relation NAME to `{ "field":
    "<top-level field>", "set": "caller" | "writer" }`. Names a row scope of the
    collection's own: "the caller whose principal id is the value in this row's
    `<field>`". A declared name is then a permission subject in `update`,
    `delete` and `read`, bare or as `<role>:<relation>`, and rejected in `write`
    and `countRead` exactly like `creator`. **`set` is required on any relation a
    permission list names**, and a deploy that omits it is refused: `"caller"`
    makes the server stamp the field on create and refuse every later change to
    it, `"writer"` lets the create set it freely and then lets only the row's
    creator change it (the agent-writes-for-a-human shape). At most 8 per
    collection, and the field must be a declared, string-capable property when
    the collection declares a schema. See "Rows that belong to a person" below,
    which is where the recipes are.
  - **`keyClaim`**: optional string, one of `"free"` (default), `"server"` or
    `"caller"`. Decides **which row key a caller may claim** when creating a
    row, which `write` says nothing about. `"free"` is today's behaviour and is
    what you get by saying nothing: any key, and the first caller to a guessable
    one owns that slot for good. `"server"` refuses a caller-supplied key
    outright, so every key is minted by the relay. `"caller"` requires the key
    to **be** the caller's own principal id, which makes a one-row-per-person
    collection squat-proof by construction. See "Who may CLAIM a row key" below,
    which is where the recipes are; it is the first thing to reach for on any
    per-user collection.
  - **`immutable`**: optional array of up to 16 top-level field names, settable
    when the row is created and **frozen** afterwards. An update that omits one
    carries the stored value forward; one that sends a *different* value is
    refused `400 invalid_request` and nothing lands; sending it back unchanged
    is fine. It applies to every caller, `owner` included, because
    it is a fact about the row rather than about who is asking. Use it to pin
    anything a permission rule is keyed on: a relation field without
    `set: "caller"` is chosen by whoever `write` admits, and without a freeze
    they can keep choosing after the fact. When the collection declares a
    schema, every name must be a declared top-level property of it.
  - **`serverSet`**: optional object mapping a field name to a definition the
    relay fills in when a row is CREATED. **This computes a value, it does not
    validate one.** There is no condition form, "reject if the total is over
    X" is out of scope on purpose (issue #1238): the manifest is the
    install-time consent screen, an expression language over row contents
    cannot be summarised into one sentence a person reads before installing,
    and LLM-authored authorization measurably gets *worse*, not better, when
    handed that kind of escape hatch. If a field cannot be computed cleanly
    from data the app already has, `serverSet` is the wrong tool. Exactly two
    forms, one per field:
    - **Lookup**, `{ "from": "<collection>", "keyField": "<field>", "take":
      "<field>" }`: `keyField` names a field on the row being written whose
      value is the ROW KEY of a row in the `from` collection, and `take`
      names the field to copy off that row. Matched by row key only, never by
      an arbitrary field value.
    - **Arithmetic**, `{ "product": [...] }` or `{ "sum": [...] }`: each
      entry is either a `serverSet` field declared EARLIER in the same
      collection, or a plain field on the row being written.

    A caller-supplied value for a `serverSet` field is **rejected, never
    silently overwritten**: `422 server_set_field_supplied`, on both the
    browser door and the agent door, from every principal including you as
    the owner's agent. On create the field's mere presence in the payload is
    refused, whatever value it carries. On update, sending the row's existing
    value back unchanged is fine (the honest-echo case every frozen field
    allows), but a payload that changes it is refused the same way. A
    lookup's `keyField` is implicitly frozen too, exactly like a field in
    `immutable`: freezing only the computed field and leaving its input open
    would let a later update retarget an already-computed value at a
    different source row without ever touching the field itself. A missing
    or deleted source row fails the WRITE, `422 server_set_source_missing`,
    rather than landing with a blank value: an order line cannot reference a
    product that does not exist. Depth is exactly one: a lookup's `take` may
    not itself name a field that is `serverSet` on the source collection. At
    most 8 `serverSet` fields per collection, and each must be a declared
    top-level property of the collection's own schema. Evaluation happens
    once, on create; the frozen `keyField` is what makes that safe, so a
    product's price changing tomorrow correctly leaves an order line already
    written at the price it sold for.

    Worked example, a shop that prices its own order lines:
    ```json
    "order_lines": {
      "schema": { "$ref": "#/$defs/OrderLine" },
      "serverSet": {
        "unitPrice": { "from": "products", "keyField": "productKey", "take": "sellPrice" },
        "productName": { "from": "products", "keyField": "productKey", "take": "name" },
        "lineTotal": { "product": ["unitPrice", "quantity"] }
      },
      "write": ["anyone"], "update": ["anyone"], "delete": ["owner"], "read": ["anyone"]
    }
    ```
    A caller creates a row with only `productKey` and `quantity`; the relay
    looks up the named product, fills in `unitPrice` and `productName`, and
    multiplies `unitPrice` by the caller's own `quantity` into `lineTotal`.
    Sending any of `unitPrice`, `productName` or `lineTotal` in the create
    payload is refused, on either door, so a public order form cannot forge
    its own price.
  - **`appendOnly`**: optional, either a boolean (default `false`) or
    `{ "except": [...] }`. Set `true` for a journal/event-shaped collection:
    rows can be created but never updated or deleted. **This is enforced, not
    advisory:** an update or delete against an append-only collection is refused
    `403 append_only` for *every* role, including `owner`, and that
    check runs before the role match, so an append-only violation reports
    `append_only` rather than a misleading "forbidden". Model an edit as a new
    row. Because that check runs first, `appendOnly: true` and an `update` list
    contradict each other and the deploy is **rejected** if you declare both:
    there is nobody left for the `update` list to admit. Pick one.
    - **`{ "except": ["owner"] }`** keeps all of that for everyone the list does
      not name, and lets `owner` update and delete under the
      collection's ordinary rules. Only `owner` may be named: it is the one
      that can already remove a row from an append-only collection
      with a purge, so this hands out no reach it did not have, it lets the
      owner (and you, acting as them) **correct** a row instead of only destroying it. **Prefer it over a bare
      `true` whenever a wrong row would otherwise be stuck in the app for
      good**, which is most journals: a mistyped entry in a `true` collection
      cannot be fixed by anybody, ever. An excepted role still has to satisfy
      the collection's own `update` / `delete` list, so the exception opens the
      gate rather than granting the verb, and an `update` list beside it is
      legal and meaningful.
  - **`unique`**: optional array of top-level field names. Declaring a field
    here means at most one **live** row in the collection may hold any given
    value for it, checked and enforced on every create, upsert, and update
    (string values are compared trimmed and case-folded; a row that leaves the
    field absent, `null`, or empty claims no slot, so many rows may share "no
    value"). A colliding write is refused `409 unique_conflict` naming the
    field, with a hint to send a different value or to upsert on that field
    instead of creating a duplicate. Deleting a row frees the value it held,
    which is also why a restore can lose a race: `409 restore_conflict` fires
    when another live row claimed that value while this row sat tombstoned,
    and the row stays recoverable so you can resolve it and restore again. It
    is also the field an ingest rule's `upsertOn` merge key must name: a merge
    key with no enforced uniqueness would let two concurrent deliveries create
    duplicate rows instead of merging into one. **Adding a field to `unique`
    on a redeploy is never a compat break by itself, even on a collection that
    already holds live rows:** the relay backfills the constraint over every
    row already there, and if two or more of them already share a value for
    the new field, the WHOLE redeploy is rejected `409
    unique_backfill_conflict` naming the field, rather than landing a
    constraint the current data cannot hold. Delete or edit the colliding
    rows and redeploy again.
  - **`retention`**: optional object, `{ maxRows?, maxAgeDays? }` with at
    least one bound present. Caps how many rows the collection keeps, by count
    and/or by age: a background sweeper hard-deletes live, non-seed rows over
    either bound on a slow cadence. The prune is feed-silent (no tombstone, no
    per-row delete event), so a watching client learns via a resync signal
    rather than a flood of deletes. The author default, the owner's runtime
    override, and the full mechanics live at
    https://docs.homespun.dev/agents/collection-retention/; this is only the
    manifest shape.
  - **`mirror`**: optional string, one of `"auto"` (default), `"eager"`, or
    `"server"`. Decides how much of the collection the browser's local mirror
    holds. `"auto"` mirrors rows up to the per-account cap and then flags the
    collection server-backed; `"eager"` always mirrors every row, ignoring
    that cap; `"server"` never mirrors at all, so the SDK marks the collection
    server-backed from the start. A server-backed collection reads through
    `homespun.collections.list()` and `.count()` instead of the synchronous
    `.snapshot()`, since there is no full local copy to read synchronously.
    Reach for `"server"` on a collection too large, or too private in
    aggregate, for every visitor's browser to hold a complete copy of.
  - **`anonWriteBudget`**: optional object, `{ perIpPerDay, perAppPerDay }`,
    **both required** once you declare the key at all. A daily TOTAL on how
    many rows anonymous visitors may add to this collection: `perIpPerDay`
    caps one visitor's network, `perAppPerDay` caps the collection as a
    whole across every visitor combined. `0` in either field means
    unlimited for that dimension. This is a **different control** from the
    platform's built-in per-IP rate limiter: the rate limiter bounds how
    fast a stranger can write, this bounds how MANY they can ever write in a
    day, which is what stops a slow drip of anonymous rows from quietly
    filling your app's own row quota before you ever get to use it. **Only
    accepted on a collection whose `write` list includes `"anyone"`**;
    declaring it anywhere else is rejected at deploy, because a budget on a
    collection anonymous visitors cannot write to at all could never apply.
    Never applies to your own writes as owner, or to a member's.
  - **`antiAbuse`**: optional string, only `"turnstile"` today. Requires a
    Cloudflare Turnstile verification token on every anonymous write to this
    collection: the page fetches a token from a Turnstile widget and the SDK
    attaches it to the write, or the relay refuses with `turnstile_required`
    (missing) or `turnstile_verification_failed` (rejected). **Fails open**:
    if Cloudflare cannot be reached in time, the write proceeds rather than
    being blocked, so a Cloudflare outage never takes down every public form
    on the platform at once. `anonWriteBudget` above is the backstop that
    makes that acceptable: even during a real outage, a stranger's total is
    still bounded by the daily budget, so declare a budget alongside this
    rather than relying on Turnstile alone. Also only accepted on a
    collection whose `write` list includes `"anyone"`, and only when the
    relay operator has Turnstile configured; if you get a deploy error
    naming it, the relay is not configured for it and you should drop the
    key or ask the operator to enable it.
  - **`seedOnInstall`**: optional boolean (default `false`). Only meaningful on
    a *template* (a published/first-party snapshot someone installs). Set `true`
    to pre-fill this collection with the template's starter rows when the
    template is installed: the new app is born with those rows already in it.
    Leave it off (the default) for a collection whose content the users
    themselves submit, so it installs empty. The starter rows live alongside
    the template, not in the manifest (first-party templates author a
    `templates/<dir>/seed.json`); this flag only decides *which* collections
    receive them at install. It is read once, at install time, and has no
    effect on a live app's later redeploys or on normal writes. Seeded rows are
    real rows: they count against the installing owner's quota and carry a
    synthetic template author, so no human or agent holds the `author` role on
    them. **Privacy:** if you later publish that app as a community template, the
    LIVE rows of its `seedOnInstall` collections are captured and become PUBLIC
    to every platform user once approved. So keep example-only starter data in a
    `seedOnInstall` collection, never real personal data (names, emails,
    addresses, private messages). When you publish, pass `attest_example_only:
    true` on the `community` tool to attest you have checked this.
  - **Roles** (the full vocabulary): `owner` (the human who owns the app, and
    you, when you act as their agent: see below), `member` (a human invited
    as a collaborator), `anyone` (any authenticated-or-not visitor, subject
    to the app's visibility), plus three **row-scoped** subjects decided per
    **You (the deploying/owning agent) ARE the owner, authority-wise.** There
    is no separate `agent` role you need to list: an agent principal is
    authorized for EXACTLY what the human who owns it is authorized for,
    nothing more and nothing less, so `["owner"]` already means you. `agent`
    still parses today and behaves exactly like `owner` wherever it appears
    (write it in a fresh manifest and the deploy still succeeds, with an
    advisory to migrate), but it is a deprecated alias on its way out: prefer
    `owner` in anything you write from now on. Beyond that one collapse there
    is still no other role hierarchy except the platform's own `owner` ⇒
    `member`: a caller matches a declared or custom role only by being named
    in it, so **list every subject that should have the verb**.

    One exception worth knowing rather than relying on: `purge` and `restore`
    are gated on `owner` DIRECTLY, not on the collection's lists, so you (as
    the owner's agent) can always remove or bring back a row regardless of
    what `delete` says.

    target row rather than carried by the caller: `creator` (created the row),
    `editor` (wrote the row last), and `author` (an older name for `editor`,
    still accepted, discouraged because the word reads like "creator" and does
    not mean it). All three are valid in `update`, `delete` and `read`, and
    rejected in `write` and `countRead`. **`creator` is the one to reach for**;
    see "Who may change a row" below for the full table and why the distinction
    is a security property, not a naming preference.
- **Deleting is recoverable, purging is not.** `delete_row` writes a soft
  tombstone: the row keeps its data, its creator and its history, and
  `restore_row` brings it back with its version bumped. `list_deleted_rows` is
  the recovery bin and reports a `recoverable_until` per row (30 days after the
  delete by default). Both are owner-or-agent only and are independent of the
  collection's permission lists. `purge` is the permanent verb: it scrubs the
  row's contents immediately and `restore_row` refuses it. Two restore failures
  are worth handling rather than retrying: `restore_conflict` (another live row
  took a `unique` value this one held while it was deleted) and a quota refusal
  (the app filled up after the delete released its slot). Both leave the row
  tombstoned and still recoverable.

- **`x-homespun-manifest.externalHosts`**: an array of `https://` origins
  (DNS name, optional single leftmost `*.` wildcard, no path/query/IP
  literal) the page's `fetch`/`XMLHttpRequest` is allowed to reach. This is
  the **only** way a deployed app can talk to anything besides its own data
  API. See "Serving and security" below.
- **`x-homespun-manifest.cdn`**: boolean, default `false`. Set `true` to allow
  `<script src>`/`<link rel=stylesheet>` from any `https:` origin (a CDN).
  It does **not** widen what the page can `fetch()`; that's `externalHosts`
  only, kept separate on purpose so a page can load, say, a charting library
  from a CDN without also being able to exfiltrate data to arbitrary hosts.
- **`x-homespun-manifest.routes`**: optional array (at most 8) declaring a
  real, indexable URL for every row of one collection: a product page, a
  listing, an article. Before this key, every path under your app served the
  identical HTML; a route is the one way the manifest asks the relay to serve
  DIFFERENT content (title, description, canonical URL, a server-rendered
  summary block, and optionally JSON-LD) at different paths. Each entry:
  ```json
  {
    "path": "/p/:code",
    "collection": "products",
    "matchOn": "code",
    "title": "{name} | {app.name}",
    "description": "{name}, {colour}, NPR {sellPrice}",
    "summary": ["name", "colour", "sellPrice"],
    "schemaType": "Product",
    "indexable": true
  }
  ```
  - **`path`**: literal segments plus EXACTLY one `:param` segment. No
    wildcards, no regex, no nested params, and no two routes may share a
    shape (same literal segments, `:param` in the same position) or reuse a
    reserved path (`/_hs/*`, `/b/*`, `/robots.txt`, `/favicon.ico`,
    `/.well-known/security.txt`, `/sitemap.xml`).
  - **`collection`**: required. **The collection's `read` list MUST
    explicitly include `"anyone"`.** A route server-renders row content into
    HTML on the open web, so this is refused at deploy otherwise: the
    relay will not guess that you meant to publish something, even where an
    absent `read` would otherwise default to readable.
  - **`matchOn`**: the literal string `"key"` (the row's own key) or a field
    named in that collection's own `unique` list. Either way resolution is
    an indexed lookup, never a scan.
  - **`title`**: required, ≤200 chars. `description`: optional, ≤400 chars.
    Both may interpolate `{field}` (a top-level scalar field of the matched
    row) or the fixed `{app.name}` / `{app.slug}` tokens.
  - **`summary`**: up to 12 top-level scalar field names, rendered as a
    bounded, escaped block in the page body: real markup present before any
    script runs, which is what makes the page genuinely crawlable rather
    than only the meta tags.
  - **`schemaType`**: one of `Product`, `Article`, `Event`, `Offer`, or omit
    for no JSON-LD.
  - **`indexable`**: boolean, default `false`. Independent of the app-level
    `app.indexable` above: you can keep your app shell out of search while
    still wanting every product page found, or the reverse. An indexable
    route is listed in a per-app `/sitemap.xml` (on the app's own host, not
    the shared platform one), and that app's `robots.txt` points at it.
  - A request that matches no live row returns the app shell with a `404`
    status (scoped strictly to declared route patterns; every other path on
    your app keeps returning `200` exactly as before). A row edit is
    reflected the next time its page is fetched, at the same up-to-60-second
    edge staleness every served document already has (fine for a
    catalogue), so don't treat the server-rendered summary as authoritative
    for stock or price at the moment of purchase; the hydrated client view
    is the live one.
  - **Declaring or widening `routes` breaks the redeploy compat check** the
    same way a widened `externalHosts` does: it is publishing data to the
    open web, so it needs `--force` and a person reading the consent
    sentence, not a silent redeploy.
- **`x-homespun-manifest.capabilities`**: optional array from a STRICT
  allowlist of 21 names. Each granted name flips its `Permissions-Policy`
  directive from denied to `self` on the served app document; everything you
  don't list stays denied, and an unknown value is a hard validation error. The
  allowlist, grouped by purpose:
  - **Media**: `"camera"` (getUserMedia video), `"microphone"` (getUserMedia
    audio), `"autoplay"` (play media without a user gesture), `"fullscreen"`
    (Fullscreen API), `"picture-in-picture"` (the app's own `<video>` in a PiP
    window), `"encrypted-media"` (EME / DRM playback of the app's own media).
  - **Device sensors and location**: `"geolocation"` (Geolocation API),
    `"accelerometer"`, `"gyroscope"`, `"magnetometer"` (the corresponding
    Sensor APIs), `"xr-spatial-tracking"` (WebXR headset and pose tracking).
  - **Interaction**: `"clipboard-write"` (write to the system clipboard),
    `"web-share"` (the Web Share API), `"display-capture"` (screen or window
    capture via getDisplayMedia), `"screen-wake-lock"` (the Screen Wake Lock
    API, to stop the display sleeping on a propped-up tablet).
  - **Connected hardware**: `"serial"` (Web Serial), `"usb"` (WebUSB),
    `"hid"` (WebHID), `"midi"` (Web MIDI). Each still requires the user to
    pick a device in the browser's own chooser.
  - **Credentials and payment**: `"publickey-credentials-get"` (WebAuthn
    `navigator.credentials.get`, so passkeys and security keys work),
    `"payment"` (the Payment Request API).

  None of these is a way to send data anywhere. What an app may `fetch`, and
  what it may post a form to, is decided only by `externalHosts` (and `cdn`
  for scripts); a capability grant never widens either.

  Example: `"capabilities": ["camera"]` lets the page call
  `getUserMedia({ video: true })`, while microphone stays blocked. Accuracy
  caveat: `"picture-in-picture"` and `"encrypted-media"` grant these features to
  the app's OWN media (its own `<video>`), not to an embedded cross-origin
  provider. Handing PiP or DRM to a framed YouTube player is gated by the embed
  origin, not by these grants, so declaring them does not enable those buttons
  on a third-party embed (see `embeds` below).
- **`x-homespun-manifest.embeds`**: optional array of `https://` origins
  (same rules as `externalHosts`: DNS name, optional single leftmost `*.`
  wildcard, no path/query/IP literal) the page may embed in an `<iframe>`,
  emitted as a `frame-src` grant. Display-only: it does **not** widen
  `connect-src` or `form-action`, so framing a site never lets the page send
  data to it. For a YouTube player use the privacy-preserving nocookie host:
  `"embeds": ["https://www.youtube-nocookie.com"]`. Declaring a non-empty
  `embeds` list also relaxes the document's `Referrer-Policy` from `no-referrer`
  to `strict-origin-when-cross-origin`, so the embed provider receives your
  app's origin (scheme + host only, never the path or query) as the `Referer`.
  YouTube and most providers require this to validate the embedder, and reject
  the player otherwise ("Error 153"). Apps that do not declare `embeds` keep
  `no-referrer`.

  Working YouTube example (declare the embed, then use the embed URL form and
  the `allow` list the player needs):

  ```html
  <!-- manifest: {"x-homespun-manifest":{"embeds":["https://www.youtube-nocookie.com"]}} -->
  <iframe
    src="https://www.youtube-nocookie.com/embed/VIDEO_ID?rel=0"
    title="Video"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; fullscreen"
    allowfullscreen
  ></iframe>
  ```

  The `allow` attribute is what a video player uses to request playback
  features; keep it even though the app document currently denies most of these
  at the `Permissions-Policy` level. Clicking play works regardless. Two known
  limits today: the player's fullscreen and picture-in-picture buttons stay
  inert (the document `Permissions-Policy` grants those only to `self`, not to a
  cross-origin frame), and DRM-only videos that require `encrypted-media` will
  not play. Ordinary public videos play once `embeds` is declared. Use the same
  pattern for other providers (a map, a form, a calendar): declare the origin in
  `embeds`, then iframe it.
- **`x-homespun-manifest.embedAncestors`**: optional array of origins that
  will be allowed to frame THIS app in someone else's `<iframe>`. It is the
  opposite direction from `embeds`, which says what the app may frame, not
  who may frame the app.

  The origin grammar is stricter than `embeds`: **exact origins only, no
  wildcard, ever.** `https://your-form-partner.example` is accepted;
  `https://*.example.com` is refused with a clear error, unlike `embeds`
  which does allow a single leftmost `*.`. The one exception is local
  development: `http://localhost:PORT` and `http://127.0.0.1:PORT` are
  accepted over plain `http`, and no other host may use `http`.
  `"embedAncestors": ["https://www.example-partner-site.com"]` is the whole
  declaration; no path, query, or userinfo is allowed.

  **Declaring this field does nothing by itself, on most apps, and that is
  not a bug to work around.** The origins only take effect when, at the
  moment of the request, the app's visibility is `public` **and** its
  manifest needs no visitor identity, meaning no collection both admits
  anonymous create (`write: ["anyone"]`) and scopes `update`/`delete` to a
  row subject such as `creator` or `own`. An app that needs visitor identity
  relies on a cookie that a cross-site frame cannot carry, so framing it
  would not work anyway; the field is left declared but inert rather than
  rejected, so check the app's own collections before assuming an embed will
  actually render. A plain public form, `write: ["anyone"]` with no
  row-scoped `update`/`delete`, is the shape that qualifies.

  A manifest that declares a non-empty `embedAncestors` **cannot be published
  as a community template.** A published template's origins would let its
  author decide who may frame every installed copy of the app, not just
  their own, which none of this app's other grants (`embeds`,
  `externalHosts`) create. Remove `embedAncestors` before publishing.

  **The embed automatically resizes to fit its content, with nothing to
  write.** Every app already loads the SDK, and the SDK already posts the
  document's rendered height to its parent whenever the app is framed, so a
  fixed-height iframe on the embedder's page grows and shrinks to match the
  app instead of scrolling internally or leaving dead space below a short
  form. There is no manifest key for this and nothing to opt into: it is
  gated purely on being framed at all, which only happens for an origin the
  manifest already listed.

  **Handing the embed to the person who is embedding it.** They need two
  things: an origin to declare in `embedAncestors` (their own site's origin,
  exact, no path) and a way to actually put the app on their page. Two
  options, and the first is the one to reach for:

  - **The inline snippet (the default).** A self-contained `<iframe>` plus a
    small `<script>` that listens for the resize message and grows the
    iframe to match. No homespun-hosted script involved, so it keeps working
    even if homespun is briefly unreachable after the page has loaded. The
    app's owner shell shows a ready-to-copy version of this on the app's
    Settings tab, filled in with the app's real URL, once the app has at
    least one origin declared. Hand them that rather than retyping it by
    hand, since it carries origin and window-source checks on the
    `message` listener that must not be simplified away: a listener that
    resizes on any message, from any window, is a defect, not a
    convenience.
  - **The hosted convenience script**, `https://<main-domain>/embed.js`. A
    single `<script>` tag that creates the iframe itself:

    ```html
    <script src="https://<main-domain>/embed.js"
            data-app="https://your-app.<usercontent-domain>/"
            data-height="600"
            data-title="Your form"></script>
    ```

    Simpler to paste, at the cost of one more script fetched from homespun on
    every page load. The inline snippet is the one to lead with; this is the
    convenience for someone who would rather not hand-maintain the markup.

  > **Read `references/embedding.md` before building an app that declares
  > `embedAncestors`.** It documents the `homespun.embed` SDK namespace: how to
  > read the framing page's visitor context (campaign parameters, referrer,
  > page URL), which the framed document cannot otherwise see, and how to tell
  > that page a submission completed so its analytics can record the
  > conversion. An embedded lead form that skips both gives the site owner
  > leads they cannot attribute, which is usually the entire reason they
  > embedded it.
  >
  > If this skill reached you over HTTP rather than as files on disk, fetch it
  > with `homespun skill show --section embedding`, or
  > `GET <relay>/skills/homespun/references/embedding.md`.

  **A public, anonymous-write form is a spam target, embedded or not, and
  embedding makes it easier to find.** Any collection this app admits
  anonymous writes to (`write: ["anyone"]`) should also declare
  `antiAbuse: "turnstile"` and `anonWriteBudget` on that same collection (see
  both above) once the app is meant to be embedded. Turnstile only works when
  the relay operator has configured it; if a deploy is refused naming
  `antiAbuse`, the relay is not configured for it and either drop the key or
  ask the operator to enable it. `anonWriteBudget` has no such prerequisite
  and is the backstop that still holds even during a Turnstile outage
  (Turnstile fails open), so declare it regardless of whether Turnstile is
  available.

### Who may change a row: `update`, `creator`, `editor`

`write` is two capabilities wearing one name. It says who may ADD a row and,
unless you say otherwise, it also says who may CHANGE every row already there.
The `update` list is how you separate those two, and the row-scoped subjects are
how you say *whose* rows.

> **SECURITY: a `write` list is also an OVERWRITE list.** If a collection's
> `write` admits a caller, that same caller may overwrite **any** row in that
> collection, not just their own, unless an `update` list narrows it. So
> `write: ["anyone"]` on a per-user collection means every signed-in visitor may
> rewrite every other visitor's row, and since an update also restamps the row's
> `author`, the original writer's row can vanish from their own
> `read: ["author"]` view in the same request. **How reachable that is depends
> entirely on whether your row keys are guessable.** An app keyed on something
> predictable (`profile`, `settings`, a date like `2026-07-27`, a username, an
> email address) hands any signed-in user a working takeover: they call
> `homespun.collections.update("journal", "2026-07-27", ...)` and the row is
> theirs. An app that only ever calls `create()` gets server-generated keys, so
> it is protected by nobody being able to guess a key, which is secrecy, not
> authorization. Neither app is safe by construction. **Declare `update`.**

**Wrong**, and it looks careful: any signed-in visitor may rewrite any entry,
and the rewrite makes that entry theirs, so it drops out of its original
writer's `read: ["author"]` view at the same moment. **This no longer deploys
at all**: a collection with `"anyone"` in `write` and no `update` list is
refused `permission_role_invalid`, because the omitted list would inherit
`write`. It is kept here because it is the shape people reach for.

```json
"entries": {
  "write":  ["anyone"],
  "delete": ["author"],
  "read":   ["author"]
}
```

**Right:**

```json
"entries": {
  "write":  ["anyone"],
  "update": ["creator"],
  "delete": ["creator"],
  "read":   ["creator"]
}
```

Anyone signed in may add a row; only the person who created it may change,
remove or see it, and no later write by anyone, including the app's own agent,
can transfer that.

> **SECURITY: `creator` settles who OWNS a row, NOT which rows a caller may
> CLAIM. Declare `keyClaim`.** The recipe above closes the overwrite hole and
> leaves a land-grab open behind it, and the two are easy to mistake for one. A
> create is gated by `write` alone, so **by default** the first caller to
> `upsert("journal", "2026-07-27", ...)` a guessable key becomes its creator,
> permanently. Predictable keys (`profile`, `settings`, a username, an email
> address, today's date) are exactly the ones an app reaches for, and every one
> of them is claimable by whoever writes it first. Afterwards the person the
> slot was meant for is locked out of their own key: their update is denied by
> `update: ["creator"]`, and their create dedups onto the squatter's live row
> and hands its contents back instead. Deleting is not a way out either, because
> a create over a tombstoned key stamps a fresh creator, so the slot simply
> changes hands again. `unique` does not rescue this: it constrains a data
> field's values, and a collision is a hard `409`, so the legitimate user is
> denied all the same.
>
> **`keyClaim` is the fix, and it is one line.** See "Who may CLAIM a row key"
> immediately below. The advice this note used to give, "let the server mint the
> key", is still fine and is now spelled `keyClaim: "server"`, but it protects
> by unguessability rather than by authorization; `keyClaim: "caller"` is the
> stronger answer wherever the row belongs to one person.

#### Who may CLAIM a row key: `keyClaim`

`write` says who may add a row. `keyClaim` says **which** row. They are
different questions and a per-user collection needs both answered.

| Value | Means | Reach for it when |
|---|---|---|
| `"free"` (default) | any key the caller sends, first one wins the slot | the key is meaningless to fight over (a log line, an event) |
| `"caller"` | the key **must be** the caller's own principal id | one row per person: a profile, a preference set, a private bag |
| `"server"` | a caller-supplied key is refused; the relay mints every key | rows are found by listing or by a `unique` field, never by a composed name |

**`keyClaim: "caller"` is squat-proof by construction**, which is why it beats
an unguessable key: the only key anybody can claim is the one nobody else can
hold, so there is no race to lose. Omit the key and the relay fills in the
caller's own id (it is the only legal value); send a different one and the
create is refused `403`. It also survives the tombstone path that defeats every
other shape: delete your row and the slot is still only yours.

```json
"profiles": {
  "keyClaim": "caller",
  "write":  ["anyone"],
  "update": ["creator"],
  "delete": ["creator"],
  "read":   ["creator"]
}
```

```js
// The page does not compose the key at all. Both of these write the caller's
// own row, and neither can reach anybody else's.
await homespun.collections.create("profiles", { display: "Ada" });
await homespun.collections.upsert("profiles", homespun.session.humanId, { display: "Ada" });
```

The id to use is the caller's own: `homespun.session.humanId` for a signed-in
person, `homespun.session.visitorId` for an anonymous visitor on an app that
mints one. Under `"caller"` a principal with **no** identity cannot create at
all, which is deliberate: a row keyed on nothing is a row the collection's own
rules can never evaluate.

`keyClaim` never loosens anything. It is only ever an extra refusal on top of
`write`, so adding it to a live collection can only narrow what is accepted.
Loosening it back to `"free"` on a collection that had it is a compat break and
the redeploy is refused without `force`, because the land grab re-opens on rows
already written.

**The three row-scoped subjects, and why there are three:**

| Subject | Means | Use it? |
|---|---|---|
| `creator` | the identity that CREATED the row. Stamped once, never moves. | **Yes. Default to this one.** |
| `editor` | the identity that wrote the row LAST. Moves on every update. | Only when you genuinely mean "whoever touched it last". |
| `author` | the LAST writer, exactly like `editor`. The original name, accepted forever. | Discouraged in new manifests: it reads like "creator" and is not. |

All three are valid in `update`, `delete` and `read`, and rejected in `write`
and `countRead` (a create has no pre-existing row to scope against, and a count
is an aggregate, not a per-row view). If your app declares custom roles, the
suffix forms narrow one of them the same way: `<role>:own` limits it to the rows
that holder wrote LAST, and `<role>:creator` to the rows they CREATED.

**`editor` and `author` transfer; `creator` does not.** The moment anyone else
writes a row, including you doing a routine cleanup or a status flip, you
become its editor. Under `update: ["author"]` the person who created the
row then loses the right to edit it, and under `read: ["author"]` loses sight of
it entirely. That is why `update: ["author", "owner"]`, which looks like the
natural shape for an agent-assisted per-user app, quietly locks the human out of
their own row the first time you touch it. Use `creator` for "this row
belongs to this person", and reserve `editor` for "the last person to touch
this".

**Anonymous visitors DO satisfy row-scoped subjects, on an app that asks for
it.** A visitor to a `public` or `link` app is given a stable per-app identity
automatically, and their rows are stamped with it rather than with the shared
`anon` sentinel. So `write: ["anyone"]` plus `update: ["creator"]` plus
`read: ["creator"]` does what it reads like: every visitor may add a row, and
each one may then edit and see only their own. This is the shape to reach for
whenever a public app needs per-person data and you do not want to force a
login. See "Visitors: recognising someone with no account" below for what it
costs and what it cannot do, and read that section before you rely on it,
because it identifies a **browser, not a person**.

Two cases still fall back to the `anon` sentinel, and in both of them nothing
is claimable by anybody:

- **An app that never declares a row-scoped permission a visitor could reach.**
  The identity is minted only for an app that declares one (the exact rule is in
  the section below), so an app with no such declaration keeps stamping `anon`
  and its anonymous writers can never edit or re-read what they wrote.
- **Rows written before this existed.** They keep the `anon` author they were
  written with. Nothing was migrated, deliberately: handing an old shared-
  sentinel row to whichever browser happens to arrive next is exactly the leak
  the identity exists to close.

A grant link (`homespun grants mint`) remains the way to hand ONE named person
a stable identity you control, and `homespun.session.login()` remains the way to
get a real account behind it. The visitor identity is neither of those; it is
the zero-friction floor beneath both.

### Visitors: recognising someone with no account

A visitor to a `public` or `link` app is handed a **stable, per-app identity**
by the relay, with no login and nothing for you to build. Their rows are stamped
with it, so `creator`, `editor`, `author`, every `:own` / `:creator` suffix and
every relation you declare work for them exactly as they work for a member.

Read `homespun.session.visitorId` for the current browser's id. It is the
visitor's counterpart to `homespun.session.humanId`, and it is what you put in a
relation field when you need to name yourself and the relation does not carry
`set: "caller"`. `homespun.session.kind` stays `"anonymous"` for a visitor,
because that is exactly what their standing in the app is: no membership, no
account, the `anyone` role and nothing more. Test for a visitor with
`session.visitorId !== null`, never by looking for a fourth `kind`.

**It identifies a BROWSER, not a person. Read the whole of this list before you
design around it.**

- A **cleared cookie** is a new visitor. The old rows still exist and are now
  reachable by nobody.
- A **second device** is a different visitor. The same human on their phone and
  their laptop is two visitors with two sets of rows and no way to join them.
- A **private/incognito window** is a different visitor, and stops being one
  when the window closes.
- A **different browser** on the same machine is a different visitor.
- It **expires**. The clock slides forward on every visit, so someone who keeps
  using the app keeps their rows; someone who disappears for the full window
  comes back as a stranger.
- It is **never proof of who anyone is**. Anyone can throw one away and take
  another as many times as they like, so it must never gate anything that
  matters, be rendered as a name or an account, or be treated as a signal of
  good behaviour.
- It is **never shared across apps**. The same browser on two of your apps has
  two unrelated ids, and neither app can tell they are the same browser.

If any of that is unacceptable for what you are building, you need a real
identity, not a visitor: `homespun.session.login()` for an account, or a grant
link for one named person. **Say so in the page.** An app that lets a visitor
build up something they would be upset to lose should tell them plainly that it
is remembered in this browser only, rather than letting them discover it on a
new phone.

The **install screen says it for you**, and says it in exactly these words, so
you do not have to word it yourself and must not contradict it:

> **This app can recognise you when you come back.** It remembers this browser
> so you can see and edit the things you add. It recognises a browser, not a
> person: clear your cookies, or use another device, and it will not know you.

That line is driven by the same predicate the relay mints on, so it appears
exactly when the app really would be given an identity. It is disclosure at
install, not in the running page: an app whose whole value is what a visitor
accumulates should still say it where they can see it while they are using it.

**When the identity is minted, and when it is not.** This is a privacy rule, not
a performance one, so it is worth stating exactly. An app gets a visitor
identity only when ALL of these hold:

1. Its visibility is `public` or `link`. A `private` app already signs everyone
   in, so its viewers have real identities.
2. It is served on its own `<slug>.homespunapps.com` subdomain (the standard
   hosted setup).
3. Its manifest declares a permission a visitor could actually satisfy: **some
   collection has `"anyone"` in its `write` list, AND that same collection's
   `read`, `update` or `delete` names a row-scoped subject a visitor can hold**,
   which means one of `creator`, `editor`, `author`, one of that collection's
   own relation names, or the narrowed forms `anyone:own`, `anyone:creator`,
   `anyone:<relation>`.

**An app that declares none of that is never given a cookie at all.** Nothing is
minted, nothing is stored, and nothing identifies the visitor. Both halves of
rule 3 matter: a collection nobody anonymous can write to gives a visitor
nothing to own, and a collection with no row scope treats every caller alike
whether it recognises them or not. Note also that only `anyone:` narrows count.
`reviewer:creator` does not qualify an app, because a visitor can never hold
`reviewer`.

So a public guestbook with `write: ["anyone"]` and `read: ["anyone"]` gets no
identity, and a team app full of `<role>:creator` scopes gets none either. Add
`update: ["creator"]` to an `anyone`-writable collection and the app starts
recognising returning visitors from its next deploy; take it away again and it
stops on the very next request.

The recipe, in full:

```json
"suggestions": {
  "write":  ["anyone"],
  "read":   ["creator"],
  "update": ["creator"],
  "delete": ["creator"]
}
```

Anyone may add a suggestion; each visitor sees, edits and deletes only their
own; nobody sees anybody else's. Add `"owner"` to `read` if the app's owner
should see every row, and remember that `read: ["creator", "owner"]` means the
owner sees ALL rows, not just their own (matching is literal, and a matched role
wins over a row scope).

### Roles your app defines: `roles` and `includes`

The built-in subjects (`owner`, `member`, `anyone`, plus the
row-scoped `creator` / `editor` / `author`) describe a person's relationship to
the *platform*. They cannot say "a reviewer", "a coach", "a front-desk shift
lead", because those are relationships to *your app*. Declare those yourself,
under `x-homespun-manifest.roles`, and then use the names as permission subjects
exactly as you would a built-in one.

```json
"x-homespun-manifest": {
  "roles": {
    "viewer":      { "label": "Viewer",      "description": "Can see the board" },
    "contributor": { "label": "Contributor", "description": "Can move cards", "includes": ["viewer"] },
    "admin":       { "label": "Admin",       "description": "Runs the board", "includes": ["contributor"] }
  },
  "collections": {
    "cards": {
      "read":   ["viewer"],
      "write":  ["contributor"],
      "update": ["contributor"],
      "delete": ["admin"]
    }
  }
}
```

**Declaring a role grants nothing.** A permission list naming it is what grants
something. `roles` says the name exists (and what to call it on screen); the
collection lists say what it can do. That split is deliberate: there is one place
to read to find out what any role may do, and it is the collection.

**`includes` composes roles, transitively.** In the manifest above, `admin`
includes `contributor`, and `contributor` includes `viewer`, so a person holding
`admin` holds `contributor` and `viewer` too, everywhere. That is why `read`
names only `viewer`: write the shared part once, in the base role, instead of
repeating `["viewer", "contributor", "admin"]` in every list and getting one of
them wrong in six months. Composition only ever ADDS; there is no way to subtract, because a
rule that takes access away cannot be summarized on an install screen without
the reader having to work out an ordering.

`includes` may only name roles declared in the same block, may not name a
built-in (their meaning is fixed by the platform), and may not cycle. Deploy
enforces that plus the size caps, and each error names the offending role and
the fix, so write what you mean and let the validator correct you.

**A person may hold several roles at once.** A member is given roles with
`homespun members set-role --app <app> --human <humanId> --custom-role
reviewer,scheduler` (comma-separated), and holds the union of what each one
grants, plus everything those roles include. `--clear-role` drops them back to a plain
member. A member may hold up to 8 declared roles; if you want more than that on
one person, declare a role that `includes` the others and hand out that one
instead.

A **grant link** is different: `homespun grants mint --app <app> --role <name>`
mints a link carrying exactly ONE role, because a link *is* a handout of that
role. The link's holder still gets everything that role includes.

A grant-link holder gets the **live mirror** on the same terms as anyone else:
`collections.snapshot()` and `collections.on()` see exactly what their HTTP reads
see, no more and no less. If the link was minted with a pin (one row key, or a
filter), the live mirror is narrowed by it too, so an app cannot use the socket
to reach past a pin the read door enforces.

**A grant link works on a private or link app, not just a public one.** The
holder opens the URL, the relay claims the link for them and remembers it in the
browser, and the app loads. They never need a Homespun account, and they are
never asked to sign in. This is the normal way to hand an app to someone outside
your members list: shop staff, a helper, a neighbour. Send them the URL exactly
as `homespun grants mint` printed it, fragment and all, because the part after
the `#` is the secret and a URL trimmed at the `#` opens nothing.

**Role names are also usable in the narrowing forms.** `reviewer:creator` on
`update` means "a reviewer, and only on rows they created"; `reviewer:own` means
"and only on rows they wrote last". The base of the suffix must be a declared
role, since the built-in row scopes already have their own bare names.

**Check what you actually built** with `homespun members roles --app <app>`. It
reports, per declared role and per collection, the EFFECTIVE access a holder has
(separately for members and for grant-link holders, whose floors differ), and
what each role includes. It is computed by asking the real authorizer, not by
re-reading your manifest, so it is the answer enforcement will give.

Two things worth knowing before you design around roles:

- **A custom role never implies `member`.** A grant-link holder carrying
  `reviewer` is `{anyone, reviewer}` and nothing else, so a collection with
  `read: ["member"]` is invisible to them. A signed-in member carrying
  `reviewer` is `{anyone, member, reviewer}`. If both populations should see a
  collection, list both subjects.
- **`owner` carries `member`, and that hierarchy is the platform's, not yours.**
  It is not expressed through `includes` and cannot be changed by a manifest.
  The app owner already outranks every role you declare, so there is no reason
  to give them one.

### Rows that belong to a person: `relations`

`creator` and `editor` answer "who touched this row". They cannot answer "whose
row is this", because the person a row is ABOUT is usually not the person who
typed it. A shift the manager assigned, a task the agent filed on someone's
behalf, a packing list that belongs to one traveller: in every one of those the
owner is a **field of the row**, and until you declare it, that field is just
text any writer can overwrite.

`relations` gives that field a name and makes it enforceable.

```json
"tasks": {
  "schema": { "$ref": "#/$defs/Task" },
  "relations": {
    "assignee": { "field": "assignedTo", "set": "writer" },
    "reporter": { "field": "reportedBy", "set": "caller" }
  },
  "read":   ["assignee", "admin"],
  "write":  ["contributor"],
  "update": ["assignee", "admin"],
  "delete": ["reporter", "admin"]
}
```

`assignee` now means "the caller whose own principal id is the value in this
row's `assignedTo` field". It is a subject exactly like `creator`: usable in
`update`, `delete` and `read`, and rejected in `write` and `countRead` for the
same two reasons (a create has no row to compare against, and a count is an
aggregate over the whole collection rather than one person's view).

**The value is a principal id, not a name or an email.** A page reads its own
from `homespun.session.humanId`, and everyone else's from
`homespun.members.list()`. An agent uses the human id it already holds. A field
holding `"alice@example.com"` or `"Alice"` matches nobody and grants nothing,
silently, so put an id there.

**`set` is what makes it authorization rather than a claim, and a relation any
permission list names must declare it.** There are two answers, and the deploy
refuses a referenced relation that gives neither:

- **`set: "caller"`**: the SERVER fills the field in with the caller's own id
  when the row is created, overwriting whatever the client sent, and refuses
  every later attempt to change it. Use it when the row belongs to whoever made
  it.
- **`set: "writer"`**: the create sets the field to whatever it likes, and
  afterwards **only the principal who created the row may change it**. This is
  the **agent creates a row that a human owns** shape: the agent writes
  `assignedTo: "<the human's id>"`, and from that moment the human can edit and
  read their own row even though they could never have created it, while nobody
  else admitted by `update` can reassign it out from under them.

Under `set: "writer"` a non-creator's update may still send the field back
unchanged, or leave it out entirely (it carries forward). Sending a *different*
value is refused `403 relation_set_forbidden` and **nothing lands**, the rest of
the payload included: the write is refused rather than quietly stripped, because
data that does not arrive with no error is worse than an error.

**It is the CREATOR, not the author.** The author of a row is whoever wrote it
last and it transfers on every write, so a rule keyed on it would be defeated in
two requests: edit the row once without touching the relation field to become
its author, then edit again and name whoever you like. The creator is stamped
once and does not move.

A relation name may not collide with a built-in subject or a role you declared,
and its `field` must be a schema-declared property that can hold a string
(`"type": "string"`, or `["string", "null"]` for a row that starts unassigned).
Deploy enforces that plus the per-collection cap, naming the relation and the
fix in the error.

**Narrowing works too.** `admin:assignee` on `update` means "an admin, and only
on rows assigned to them". It is the same shape as `<role>:own` and
`<role>:creator`, which keep their existing meanings unchanged: `:own` is the
last writer, `:creator` is the creator, and neither is a relation you declare.

**Read scoping is real, and it is a filter, not just a check.** Under `read:
["assignee"]` a `list()` returns only the caller's own rows, on every page, and
a direct `get()` of somebody else's row returns **not found**, never
"forbidden", so a caller cannot learn which keys exist. The live feed follows
the same rule: an entry reaches only the person its data names. Two consequences
worth knowing:

- A **delete** entry carries the row's last-known data, so the person the row
  named still learns it was removed.
- **Reassigning** a row moves it: the new assignee starts seeing it, the old one
  stops. The old assignee's browser keeps a stale copy until it reconnects, at
  which point it drops out entirely.

> **SECURITY: `set: "caller"` decides who a row BELONGS to, not which key a
> caller may take.** This is the same trap the `creator` warning above
> describes, and declaring a relation does not close it. A create is gated by
> `write` alone, so under a `"free"` `keyClaim` on a guessable key (`profile`, a
> username, today's date) the first caller wins the slot, and a later create on
> the same live key **dedups and hands that row's current contents back to
> whoever tried**, even under `read: ["<relation>"]`. **Declare `keyClaim`**:
> `"caller"` for a one-row-per-person collection, `"server"` where the key is
> incidental. Upserting on the relation field itself (`on: "<field>"`, with the
> field declared `unique`) also resolves to the caller's own row and nobody
> else's.

> **A relation with no `set` at all is refused at deploy.** It used to be legal
> and it was a rule keyed on a field every writer controls: whoever `write`
> admitted chose who the row belonged to and could keep choosing on every later
> update, so an assignee could reassign somebody else's task to themselves, or
> hand it away and lose it. Say `"caller"` or `"writer"` and the question has an
> answer. The error names the collection, the field and both values.
>
> **To pin the assignment even for the creator, add the field to `immutable`.**
> `set: "writer"` lets the creator reassign the row later, which is usually what
> you want; `immutable` says the create is the last word, for everyone:
>
> ```json
> "tasks": {
>   "relations": { "assignee": { "field": "assignedTo", "set": "writer" } },
>   "immutable": ["assignedTo"],
>   "write":  ["owner"],
>   "update": ["assignee"],
>   "delete": ["owner"],
>   "read":   ["assignee"]
> }
> ```
>
> With `set: "caller"` the server owns the field outright and no `immutable`
> entry is needed.

**Anonymous visitors satisfy no relation**, for the same reason they satisfy no
`creator`: they have no identity to compare a field against. If the collection
declares `set: "caller"`, an anonymous visitor cannot even create the row, which
is deliberate: a row nobody owns, in a collection whose rules are about
ownership, is worse than a refused write. Give visitors a real identity first
(`homespun.session.login()`, or a grant link).

#### Recipe: everyone sees only their own rows

The per-user collection, done properly. Anyone signed in may add a row; the
server decides whose it is; nobody else can see it, edit it or delete it.

```json
"entries": {
  "schema": { "$ref": "#/$defs/Entry" },
  "relations": { "owner_": { "field": "ownedBy", "set": "caller" } },
  "read":   ["owner_"],
  "write":  ["anyone"],
  "update": ["owner_"],
  "delete": ["owner_"]
}
```

with `ownedBy` declared as a `"type": "string"` property of `Entry`. The page
never sets `ownedBy`; the server does. This is stronger than the `creator`
version of the same recipe in one specific way: the owning field is **data**, so
your agent can hand a row to a different person later by writing the field,
which `creator` can never do. It is weaker in one way too: without `set:
"caller"`, whoever `write` admits picks the value, so leave `set` on unless you
mean to allow that.

(Note the trailing underscore in `owner_`: `owner` itself is a built-in subject
and is rejected as a relation name.)

#### Recipe: the agent files it, the human owns it

The shape the four first-party templates were faking. You (the owning agent)
are the only writer; each row names the person it is for; that person can then
read and correct their own.

```json
"reports": {
  "schema": { "$ref": "#/$defs/Report" },
  "relations": { "subject": { "field": "forPerson", "set": "writer" } },
  "read":   ["subject", "owner"],
  "write":  ["owner"],
  "update": ["subject", "owner"],
  "delete": ["owner"]
}
```

`set: "writer"` is what this recipe is for: you are choosing who the row is for,
so the value has to be yours to write, and it stays yours. The subject can read
and correct their own row through `update`, but they cannot point `forPerson`
at somebody else, because only the row's creator (you) may move it. Use
`set: "caller"` instead when the row belongs to whoever made it.

### Schema gotchas (two that bite at deploy time)

- **`maxLength` cannot exceed the per-row byte cap.** A whole row's serialized
  `data` is capped at 64 KiB (`MAX_ROW_DATA_BYTES`), so a string field that
  declares `maxLength` larger than that cap can never actually be filled to that
  length: a value near it is rejected `413` at runtime. To catch that mismatch
  where you can see it, the deploy now **rejects** such a schema with
  `collection_schema_invalid` naming the offending `maxLength`. Keep every
  string `maxLength` at or under 64 KiB (in practice, size each field to what it
  actually holds, a name is `maxLength: 200`, not `2000000`). This is a
  single-field impossibility check only: it never sums fields, so a
  large-but-possible `maxLength` still deploys. A collection declaring
  `storage: "document"` (below) is measured against ITS larger cap instead.

### When a row is one document: `storage: "document"`

Sometimes a row is not a record with fields you filter on, it is **one document
the browser reads and writes whole**: a mind map, a diagram, a graph of nodes and
edges. Declaring `storage: "document"` on the collection raises its per-row cap
from 64 KiB to **256 KiB** (`MAX_DOCUMENT_ROW_DATA_BYTES`).

```json
"collections": {
  "maps": {
    "storage": "document",
    "schema": { "$ref": "#/$defs/MindMap" },
    "read": ["creator"], "write": ["member"],
    "update": ["creator"], "delete": ["creator"]
  }
}
```

**What you give up.** The payload stops being indexed. Filtering still WORKS, it
just stops being something the platform keeps fast as the collection grows, so
reach for this when the querying happens in the browser rather than on the
server. Keep the fields you genuinely filter or sort on (an owner id, a title, a
timestamp) as small top-level fields; only the bulky part is the document.

**Why it is opt-in rather than just a bigger cap for everyone.** The cost of a
large payload is not storage, it is index maintenance: the row index hashes every
leaf of the document, so a graph, which is all leaves, is the worst possible
shape for it. Measured at 64 KiB, an indexed insert costs ~54x an unindexed one.
Excluding these rows from that index is what makes the larger cap affordable, and
it is why the two decisions are one declaration rather than two.

**It is not a way to store files.** Images and other binary content belong in
attachments, with only the attachment id in the row, whichever mode you declare.
A base64 data URL in a row is the single most common reason apps run into the cap,
and `storage: "document"` is the wrong fix for it.

**A row over the cap is refused `413 row_size_exceeded`**, and the error names the
collection, the actual size, the cap, and which of the two you are on.

- **Intra-document `$ref` across `$defs` is NOT resolved, inline it.** A
  collection's `schema` may `$ref` a `$defs` entry, but a `$ref` FROM one
  `$defs` entry TO another sibling `$defs` entry is not resolved: the sibling
  ref is out of scope when the entry is compiled, so the deploy is REJECTED
  with `collection_schema_invalid` ("can't resolve reference"). Inline the
  shared shape into each `$def` that needs it instead of referencing a
  sibling. So this does NOT work:

  ```json
  "$defs": {
    "Address": { "type": "object", "properties": { "city": { "type": "string" } } },
    "Order": {
      "type": "object",
      "properties": { "ship_to": { "$ref": "#/$defs/Address" } }
    }
  }
  ```

  Inline `Address` directly inside `Order` instead:

  ```json
  "$defs": {
    "Order": {
      "type": "object",
      "properties": {
        "ship_to": {
          "type": "object",
          "properties": { "city": { "type": "string" } }
        }
      }
    }
  }
  ```

### Recipe: public submits, only the owner reads

The highest-value thing `read` buys you: a collection the world can write to but
only the owner can see. Order queues, RSVP lists, job applications, booking
requests, contact and feedback boxes are all this shape.

```json
"collections": {
  "menu": {
    "schema": { "$ref": "#/$defs/MenuItem" },
    "read": ["anyone"],
    "write": ["owner"],
    "delete": ["owner"]
  },
  "orders": {
    "schema": { "$ref": "#/$defs/Order" },
    "write": ["anyone", "owner"],
    "update": ["owner"],
    "delete": ["owner"],
    "read": ["owner"]
  }
}
```

`orders` declares `update` even though only staff read it: without that line,
`write: ["anyone"]` would let any visitor rewrite any order that already exists,
not only add their own (see "Who may change a row").

An anonymous customer can POST an order (it lands with an `anon` author), but
listing `orders` gives them `403 collection_read_forbidden`: only the owner
(you included, acting as their agent) can read the queue, and that is enforced
by the relay, so hitting the data API directly gets them nothing the page
would not show them either. `menu` declares `read: ["anyone"]`, so it stays
readable by every visitor, which is exactly what you want for the half of the
app the customer is supposed to see. That is the affirmative way to say "this
part is public", and it is the only way to say it now that an absent `read` is
a deploy error.

Adding `"creator"` to that `read` list lets each submitter see their own row back
(an order status page) without seeing anyone else's, but only for submitters who
are *signed in*: a row-scoped subject needs a stable identity to match a row
against, and an anonymous visitor has none, so it stays a `403` for them. Use
`creator` rather than the older `author` here: `author` means the row's LAST
writer, so the first time the owner (or you, acting for them) edits an order,
that order would drop out of the customer's own status page. Keep the queue
`read: ["owner"]` when the customer never signs in.

**The recipe is not finished until the page has a sign-in control.** This app is
public, so nobody, including its owner, is ever prompted to sign in: the owner
opens it, gets the same anonymous session every customer gets, and `orders` is a
`403` for them too. Ship a quiet sign-in affordance, hidden once the viewer is
already owner or member:

```html
<button id="signin" hidden>Staff sign in</button>

<script>
  window.addEventListener("DOMContentLoaded", async () => {
    await homespun.ready; // session.kind is resolved by the time this resolves
    if (homespun.session.kind === "anonymous") {
      const btn = document.getElementById("signin");
      btn.hidden = false;
      btn.onclick = () => homespun.session.login(); // comes back to this page
    } else {
      renderOrderQueue(); // owner/member: the owner-only read now succeeds
    }
  });
</script>
```

`homespun.session.login()` is a full-navigation redirect to the relay's
`/authorize` hand-off, with the current page as the return target:

```
https://<main-domain>/authorize?app=<slug>&return=<absolute URL to come back to>
```

### Signing in as a different account

A viewer is normally handed straight back the account they are already signed in
with on the main domain, which is what you want almost always. When it is not,
`homespun.session.login({ switchAccount: true })` asks first: the relay shows a
one-screen chooser naming the current account, with "use a different account"
next to it.

**You rarely need to pass it.** `session.logout()` arms the chooser for the very
next `login()` from that app on its own, so the ordinary "sign out, sign in as
someone else" gesture already works with the two buttons you have. Pass the flag
only for an explicit "switch account" control.

A second account chosen this way applies **to this app only**. The viewer stays
signed in as whoever they were on the main domain, and every other app they are
signed in to is untouched: app sessions are per app, so one browser can be two
different people in two different apps.

`login()` builds that URL itself, from the auth origin the relay sends the page at
connect time and the app's own slug, so **nothing is hardcoded and you should
prefer it** over hand-writing the URL. An anonymous visitor is bounced through
the relay's login page; on the way back, an owner or member is handed a one-time
grant that mints an app session on the app's own origin, and lands on `return`
with `homespun.session.kind === "owner"` (or `"member"`), at which point the
owner-only reads work. A signed-in visitor who is neither returns to the page
still anonymous and with no grant, so the control is safe to leave in public.

If you must build that URL by hand (a plain `<a href>`, or a page not using the
SDK): `<main-domain>` is the relay's own domain (`homespun.dev` for the hosted
relay, whatever `MAIN_DOMAIN` is configured to otherwise, so this is exactly
the part `login()` saves you from hardcoding). `return` is optional and must be an
absolute URL on the app's OWN origin. Anything else (another app, an
off-platform host, `http:`, a malformed value) is not an error, it is silently
replaced with the app's root. The slug is the leftmost label of the app's own
hostname on the hosted usercontent domain (`location.hostname.split(".")[0]`),
though `homespun.app.slug` is always right and is what `login()` uses.

### Recipe: a public count without exposing the rows

When the page needs to show "3 spots left" or "128 people signed up" to an
anonymous visitor, do NOT make the whole collection world-readable to get the
number, that leaks every submission. Opt the collection into the count-only
aggregate with `countRead` while keeping `read` locked down:

```json
"collections": {
  "signups": {
    "schema": { "$ref": "#/$defs/Signup" },
    "write": ["anyone"],
    "update": ["owner"],
    "delete": ["owner"],
    "read": ["owner"],
    "countRead": ["anyone"]
  }
}
```

`update: ["owner"]` is what holds a visitor to adding a signup rather than
rewriting somebody else's; without it, `write: ["anyone"]` grants both.

The page reads the number with `homespun.collections.count(name)`, which
resolves to a plain integer:

```js
const taken = await homespun.collections.count("signups");
document.getElementById("left").textContent = `${Math.max(0, 50 - taken)} spots left`;
```

An anonymous visitor gets the live count but a `GET /_hs/c/signups` (or
`homespun.collections.snapshot`) still returns nothing: the rows stay
owner-only. The count is a whole-collection total of live (non-deleted) rows;
there is no field projection and no filtering in v1. A collection that never
declared `countRead` refuses the count with `403 collection_count_forbidden`.

This recipe is what makes the number public, on purpose: the count moving
from 49 to 50 tells every visitor a row was just created (or from 50 to 49
that one was deleted), even though the row's own fields never leave the
server. Fine for a spots-left counter, where that fact is the whole point.
Avoid this shape on a collection where a row's mere existence is itself
sensitive (a waitlist for something embarrassing, an incident log); scope
`countRead` to match `read` instead (see "Known leak" above), or accept the
count is not truly private. Deploying a collection with this exact pair
returns a `warnings[]` entry in the deploy result naming the collection, the
same mechanism the schedules-without-timezone warning above uses; it never
blocks the deploy.

<!-- homespun:core:end -->

## Writing the HTML: `window.homespun`

The relay injects `window.homespun` into every served app document. The page
talks to its own data **only** through this bridge.

**Script ordering.** `window.homespun` is defined **synchronously during
parse**, before any script of yours runs. The relay injects two things into the
`<head>`: a tiny inline bootstrap that defines `window.homespun` immediately,
and the real SDK bundle as `<script src="/_hs/sdk.<hash>.js" defer>` that loads
after parsing and takes over. Because the bootstrap runs first, referencing
`homespun.*` at the top level of a plain inline `<script>` is safe: it never
throws. The bootstrap buffers any method call made before the bundle finishes
loading (the call resolves once the bundle attaches), and synchronous reads
(`collections.snapshot`, `feed.cursor`, `session.kind`, ...) return the same
pre-`ready` defaults documented below until the data has loaded.

So gating your init on `DOMContentLoaded` is **no longer required**. It stays
perfectly harmless (every example below still does it, and it works), but you
can just as well run your init inline. What you should always do is **`await
homespun.ready`** (or `homespun.ready.then(...)`) before your first synchronous
read, so the session and the initial collection snapshots are in place:

```html
<script>
  async function init() {
    await homespun.ready; // session + initial snapshots are ready
    render();
    homespun.collections.on("items", render);
  }
  init();
</script>
```

| Surface | What it does |
|---|---|
| `homespun.ready` | `Promise<void>`. Resolves once the session is resolved and every declared collection has been snapshotted into the local mirror. `await` it before your first synchronous read. |
| `homespun.collections.snapshot(name)` | Synchronous read of every row currently in the local mirror. `[]` before `ready`. |
| `homespun.collections.get(name, key)` | Synchronous point read; `undefined` if absent/deleted. |
| `homespun.collections.count(name)` | `Promise<number>`: the collection's live row count from the server. Works even when the caller cannot read the rows, if the manifest opted in with `countRead` (the "3 spots left" shape). Network read, not a mirror read. Rejects `collection_count_forbidden` when not opted in. |
| `homespun.collections.on(name, handler)` | Live deltas for one collection, already folded into row shape: `{kind:"upsert", collection, row: HomespunRow}` or `{kind:"delete", collection, row:{key, deletedAt}}`. Returns an unsubscribe function. |
| `homespun.collections.create(name, data)` | `POST`; the server generates the row key. Returns the created `HomespunRow` FLAT. (The raw `POST /v1/apps/:id/collections/:name` REST endpoint instead wraps it as `{ "row": ... }`; see "Raw REST envelopes" if you call the API directly.) |
| `homespun.collections.upsert(name, key, data)` | Create-or-return-existing for a caller-supplied key (idempotent). |
| `homespun.collections.update(name, key, data, {ifMatch?})` | Optimistic-locked update. A stale `ifMatch` rejects with `code:"conflict"` and `details.current` set to the winning row. |
| `homespun.collections.delete(name, key, {ifMatch?})` | Soft-delete (tombstone). |
| `homespun.feed.on(handler, {collection?})` | Unfiltered (or single-collection-filtered) live change feed: every create/update/delete across the app, in order. Each entry is a raw `FeedEntry`: `{seq, op:"create"\|"update"\|"delete", collection, key, data, author, ts}`. **Note the field is `op`, not `kind`**: `feed.on` and `collections.on` carry different shapes (see below). |
| `homespun.feed.cursor` | Highest feed `seq` applied locally so far (memory-only). |
| `homespun.app.{slug,name,description,icon,visibility,collections}` | Manifest-derived, safe-to-expose facts about this app. |
| `homespun.session.{kind,humanId}` | Who's looking at the page right now: `"owner"` \| `"member"` \| `"anonymous"`, and their human id (`null` if anonymous). |
| `homespun.session.displayName` | The viewer's own name (`null` when anonymous). Self-facing only: falls back to a name derived from their email when they haven't set one, same rule the dashboard uses for its own greeting. |
| `homespun.session.login(opts?)` | Full-navigation redirect to the identity provider's `/authorize` flow. Pass `{switchAccount: true}` to offer an account chooser instead of reusing the account the viewer is already signed in with on the main domain. |
| `homespun.session.logout()` | Revokes this app's session server-side, clears the stored token, and reloads as anonymous. The next `login()` from this app offers the account chooser automatically. |
| `homespun.members.list()` | Every human Member of this app (always including its owner) plus every Agent its owner currently owns, as `{kind:"human"\|"agent", id, displayName, role?}`. Names only: never an email, and never anything derived from one for anyone other than themselves. |
| `homespun.members.nameFor(author)` | Resolve a row's or feed entry's own `author` (`{kind, id}`) straight to a display name, never throws. Falls back to `"a member"` / `"an agent"` for an id no longer in the directory (a removed member, an unclaimed/reassigned agent), and `"a visitor"` for an anonymous author. |
| `homespun.uploadBlob(file, opts?)` / `homespun.downloadBlob(id)` / `homespun.saveBlob(id, filename?)` | Binary attachment upload/download. Names kept from v1 for continuity. To DISPLAY an app's own attachment, a bare `<img src=/_hs/attachments/id>` works. The read route is gated on the APP's visibility, not per collection: a public or link app serves its attachments to anyone, including anonymous visitors, and a private app requires a signed-in owner/member session. `downloadBlob(id)` is the JS-bytes read: use it with `URL.createObjectURL` only when you need the raw bytes in JS (canvas, re-upload), not as the display path. |

A minimal grocery-list page against the manifest above:

```html
<!doctype html>
<meta charset="utf-8" />
<ul id="list"></ul>
<input id="new-item" placeholder="Add an item" />
<button id="add">Add</button>

<script>
  // `window.homespun` is defined synchronously during parse, so this init could
  // run inline; the DOMContentLoaded wrapper is optional (and harmless) here and
  // just guarantees the elements below exist. What matters is `homespun.ready`,
  // awaited before the first read. See "Script ordering" above.
  window.addEventListener("DOMContentLoaded", () => {
    const list = document.getElementById("list");

    function render() {
      list.innerHTML = "";
      for (const row of homespun.collections.snapshot("items")) {
        const li = document.createElement("li");
        // The row's real author, server-stamped and tamper-proof (never a
        // client-written `by` field (see "Rules of thumb" below).
        const by = homespun.members.nameFor(row.author);
        li.textContent =
          row.data.name + (row.data.checked ? " ✓" : "") + " (added by " + by + ")";
        li.onclick = () =>
          homespun.collections.update("items", row.key, {
            ...row.data,
            checked: !row.data.checked,
          });
        list.appendChild(li);
      }
    }

    homespun.ready.then(render);
    // Live updates, from a member's own edits AND from `homespun data upsert`
    // calls the agent makes later.
    homespun.collections.on("items", render);

    document.getElementById("add").addEventListener("click", async () => {
      const input = document.getElementById("new-item");
      if (!input.value.trim()) return;
      await homespun.collections.create("items", {
        name: input.value.trim(),
        checked: false,
      });
      input.value = "";
    });
  });
</script>
```

Rules of thumb:

- **`await homespun.ready` before your first synchronous read** (see "Script
  ordering" above). `window.homespun` is defined synchronously during parse, so
  referencing it at the top level of a plain inline `<script>` is safe and
  `DOMContentLoaded` gating is optional; `ready` is the signal that the session
  and the initial collection snapshots are actually in place.
- **`collections.on` and `feed.on` are not interchangeable.** `collections.on`
  gives you a row-shaped delta already folded for one collection
  (`{kind:"upsert"|"delete", row}`). Reach for it when you just want to
  re-render on change, as in the example above. `feed.on` gives you the raw,
  unfolded `FeedEntry` (`{seq, op, collection, key, data, author, ts}`,
  field is **`op`** not `kind`) across the whole app (or one collection via
  `{collection}`). Reach for it when you need ordering/`seq`, cross-collection
  events, or the entry's own metadata (`author`, `ts`) rather than just the
  resulting row.
- **`.textContent`, never `.innerHTML`**, for anything containing human- or
  agent-authored text: the same injection discipline as any other web page.
- **Never invent a client-side `by`/`author` field for what the row's real,
  server-stamped `author` already is.** A page-written field like
  `{ ...data, by: "Alice" }` is just ordinary row data: any visitor can set
  it to anything, so it proves nothing about who actually wrote the row. This
  is a rule about attribution, not about data: storing a self-declared name is
  fine (a guestbook or RSVP legitimately records the responder's stated name in
  `data`, and you should render it as what they called themselves), the narrow
  rule is only that such a field is never PROOF of authorship.
  Render the row's own `author` instead: `homespun.members.nameFor(row.author)`
  (or `entry.author` off the feed) turns the tamper-proof `{kind, id}` the
  relay stamped into a real name. Greet the current viewer the same way, with
  `homespun.session.displayName`, falling back to something generic (e.g.
  "Sign in" or "Welcome") when it's `null`.
- **No relay-injected stylesheet or CSS variables in v2.** Unlike the v1
  viewer, a deployed app gets no default styling: you own 100% of the
  CSS from the first paint. Write real, theme-aware CSS (respect
  `prefers-color-scheme` yourself) rather than assuming a house style exists.
- **Network access is manifest-gated, not blanket-blocked.** A v2 app is a
  real top-level page (not a sandboxed iframe): `fetch`/`XMLHttpRequest` work
  against `'self'` (its own data API) plus whatever origins you declared in
  `externalHosts`; nothing else. `<script src>`/`<link rel=stylesheet>` from
  an external `https:` origin additionally requires `cdn: true`. Images,
  fonts, and media may load from any `https:` origin (or `data:`) regardless
  of `cdn`/`externalHosts`: those are display-only and can't exfiltrate
  data. Anything not covered by one of these is blocked by the app's CSP;
  there is no escape hatch besides declaring it in the manifest and
  redeploying.

### Let your app's users upload a file

**This is the RIGHT way to collect a photo (or any file) from an end user** (a
visitor adding a picture to their app). Build an in-page browser file input that
POSTs the bytes to the app's own `POST /_hs/attachments` route via
`homespun.uploadBlob`. The bytes travel browser -> relay directly and **never
pass through the agent or the model context**, so it costs you no tokens and is
the correct UX. Do NOT route an end user's photo through the agent (having them
hand you bytes to `attachments upload`) just to store it: that is slow, and the
base64 would enter the model context and cost tokens proportional to the file
size.

`homespun.uploadBlob(file, opts?)` lets a person, inside your rendered app, hand
a file (an image, a PDF, a CSV) straight to the app from their browser. It POSTs
the bytes to the app's own `POST /_hs/attachments` route, runs the identical
hardened pipeline every other upload does (byte-sniff, allowlist, size cap,
quota), and resolves to an `AttachmentRef` whose `id` you store like any other
attachment id:

```html
<input id="file" type="file" accept="image/*" />
<script>
  window.addEventListener("DOMContentLoaded", () => {
    document.getElementById("file").addEventListener("change", async (e) => {
      const file = e.target.files[0];
      if (!file) return;
      const ref = await homespun.uploadBlob(file); // { id, mime, size, filename }
      // Reference it from a row: a field declared `format: homespun-attachment-id`
      // validates the id, and the bytes read back at /_hs/attachments/<id>.
      await homespun.collections.create("photos", { image: ref.id, caption: "" });
      const img = document.createElement("img");
      // Display an app's OWN attachment with a bare URL. The
      // `/_hs/attachments/<id>` route is gated on the APP's visibility: a
      // public/link app serves anyone, a private app needs an owner/member
      // session. Either way an <img src> on the app's own page just works. Use
      // homespun.downloadBlob(id) + URL.createObjectURL only when you need the
      // raw bytes in JS (canvas, a Blob to hand elsewhere).
      img.src = "/_hs/attachments/" + ref.id;
      document.body.appendChild(img);
    });
  });
</script>
```

**Who may upload depends on the target collection.** `homespun.uploadBlob` is
the **owner-or-member** convenience: it carries the visitor's app-session token
and posts to `POST /_hs/attachments`, so an anonymous visitor is refused
(`upload_forbidden` on a public/link app, `unauthorized` on a private one). If
`homespun.session.kind` is `"anonymous"` and you want a signed-in upload, send
them through `homespun.session.login()` first.

To instead accept uploads from **anonymous in-page visitors**, declare the
target collection with `write: ["anyone"]` and have the browser POST directly to
`POST /_hs/attachments?collection=<name>`. This is a plain `fetch`, not
`uploadBlob`, because `uploadBlob` does not set the `?collection=` param:

```js
const body = new FormData();
body.append("file", file);            // the field name is exactly "file"
body.append("filename", file.name);   // optional, display only
const res = await fetch("/_hs/attachments?collection=photos", { method: "POST", body });
const ref = await res.json();         // 201 { attachment_id, mime, size, filename }
// The upload does NOT create a row. Write the id into one yourself:
await homespun.collections.create("photos", { image: ref.attachment_id });
```

**The upload stores bytes and returns an id; it never writes a row.** The
`?collection=` param is read only to check that collection's `write` list. If
you forget the follow-up `create`, the bytes are stored, count against quota,
and are referenced by nothing.

Anonymous uploads are image-only (server-sniffed), and bounded four ways:
`ANON_UPLOAD_MAX_BYTES` per file (**5 MB**), `ANON_BYTES_PER_APP` in total
(**50 MB**), `ANON_UPLOADS_PER_IP_PER_APP_DAY` (**20** per browser per day), and
a per-IP limiter on `/_hs/*` writes (**60 per minute**). A stranger can never
exhaust the owner's storage.

Either way the bytes count against the **app owner's** blob quota, and an
uploader who goes too fast gets a clean `rate_limited` error.

## Serving and security: what an app's origin can and can't do

Each deployed app is served **top-level**, at its own subdomain
(`<slug>.homespunapps.com`), not embedded in an iframe. A few things follow
from that:

- **No cookies on the app's origin.** The usercontent domain strips every
  inbound `Cookie` header and drops every outbound `Set-Cookie`: nothing on
  that origin ever reads or sets one. Session state lives in the browser's
  `localStorage`, scoped per-app-origin, and is established via
  `homespun.session.login()` (a redirect to the identity provider) rather than a
  cookie.
- **`connect-src` is `'self'` plus your declared `externalHosts`, never
  wider**, regardless of the `cdn` flag. `cdn: true` only widens
  `script-src`/`style-src` (code you load), not what the page can fetch,
  keeping "can load a charting library" and "can exfiltrate data" as two
  separate grants.
- **Visibility gates who can open the app at all**: `private` (only the
  owner plus invited members, sign-in gated; this is the default), `link`
  (anyone with the URL), `public` (listed and discoverable). This is
  orthogonal to the per-collection `write`/`update`/`delete` role lists in the
  manifest; visibility controls who can load the page, the manifest roles
  control who can write which collection once they are on it.
- **Only a private app gets a sign-in gate.** A public or link app serves its
  page to anonymous visitors directly, so if it has any owner-only or
  member-only surface, the page itself has to offer the way in
  (`homespun.session.login()`); otherwise the owner is stuck anonymous on their
  own app. Sessions are per-origin: signing in on the main site does not sign a
  person in to an app. See "Recipe: public submits, only the owner reads".

### Working with no network: `offline`

Set `"offline": true` in `x-homespun-manifest` and the app installs a service
worker, so a viewer who has opened it once can open it again with no connection
at all. Without this, an installed app shows the browser's network-error page
the moment the signal drops.

```json
"x-homespun-manifest": {
  "app": { "name": "Shop stock" },
  "offline": true,
  "cdn": false,
  "collections": { "...": {} }
}
```

Four things to know before you set it.

- **It caches the SHELL, not data.** The document, the SDK, the icons and your
  deployed assets are cached; collection rows, sessions and attachments always
  go to the network. So an offline app opens and paints, and
  `homespun.collections.*` still needs a connection. Design the page to render
  something useful before its data arrives, and to say so plainly when it
  cannot reach the relay.
- **Only on a `public` app.** A `private` or `link` app decides per request, on
  the server, whether you get the app or a sign-in page. A cached copy would
  answer that on the device instead, so the worker is simply not served to
  those apps and the key is ignored. If the data is sensitive, keep the app
  public and put the protection where it belongs: `"read": ["owner", "member"]`
  on the collections. A public app with member-only collections gives you a
  page anyone can load and data only your people can see.
- **Cannot be combined with `cdn`.** Declaring both is a deploy error. An app
  that pulls React or a font from another origin cannot paint with no
  connection, and the worker will not cache another origin's bytes. Inline what
  you need instead. Your own assets shipped via the deploy bundle are cached
  and work offline.
- **Redeploys still take effect immediately** while the viewer is online: the
  page revalidates on every load and a new deploy replaces the worker and drops
  the previous version's cache. You do not have to think about cache-busting.

## Deploying and iterating

`homespun deploy` is the one command for both creating and redeploying, decided
by whether you pass `--app`, not by two separate verbs. Tell the human their
new app is private until they invite members or change its visibility.

**Canonical shape, a directory with two fixed filenames:**

```sh
homespun deploy ./my-app
#   reads ./my-app/index.html and ./my-app/manifest.json, no discovery
#   heuristics, both files required
```

**Escape hatch, a single HTML file plus an explicit manifest:**

```sh
homespun deploy ./index.html --manifest ./manifest.json
# --manifest also accepts inline JSON
```

**Create** (no `--app`) calls `POST /v1/apps`:

```sh
homespun deploy ./my-app
# private by default; add --visibility link|public to share wider

homespun deploy ./my-app --visibility public --slug grocery-list
# -> { app_id, slug, visibility, url, version, created: true }
```

- `--slug` is accepted with `--visibility public`, `--visibility private`,
  or no `--visibility` at all (the default is private). An explicit
  `--visibility link` app always gets a server-generated slug; passing
  `--slug` with it is rejected before the request even goes out.

**Redeploy** (`--app <id-or-slug>`) calls `POST /v1/apps/:id/versions`:

```sh
homespun deploy ./my-app --app grocery-list
# -> { app_id, version, visibility, created: false, compat, breaks? }
```

- **Send only what changed.** On a redeploy every content field is optional and
  an omitted one keeps what is live: the HTML, the manifest and the asset set
  each carry forward on their own. Ship the document alone with
  `homespun deploy ./index.html --app grocery-list` (no `--manifest`), or the
  manifest alone with `homespun deploy --app grocery-list --manifest ./manifest.json`
  (no file argument at all). A directory deploy still ships both, which is right
  when both changed. Over MCP the same rule applies to `deploy_app`: omit
  `manifest` for an HTML-only change, omit `html` for a manifest-only one, and
  omit `assets` to keep the current files. `assets: []` is the explicit "clear
  the asset set", and omitting all three is refused, since nothing would change.
  A create can inherit nothing, so it always needs both halves.
- `--slug`/`--visibility` cannot be changed here: slug is immutable for the
  app's lifetime; change visibility with `homespun apps update --visibility`.
- **The compat gate.** By default the relay refuses a redeploy on either of
  two grounds, and they point in opposite directions.
  - It *strands existing rows*: a collection removed, a row schema tightened,
    or a collection flipped `appendOnly`. Rows written under the old contract
    could stop making sense.
  - It *widens what the app's install screen says*, so a user installing today
    would be asked to approve something the current users never saw. Either
    some collection now reaches further than the live manifest does, or the
    app asks for more outside itself: a `capabilities` entry added, `cdn`
    turned on, or a new host in `externalHosts`, `embeds`, or a webhook
    target. The break quotes that sentence back to you.

  It fails `422` with `details.breaks[]` naming every offending path. Taking
  access AWAY is always compatible and never asks: dropping a role from
  `read`/`write`/`delete`, dropping a capability, host or webhook, turning
  `cdn` off, or adding `update: ["creator"]` to a `write: ["anyone"]`
  collection so only each row's creator can edit it, all redeploy clean.
  Stripping an app back to fewer permissions never needs `--force`. Pass
  `--force` to redeploy anyway (a removed collection is detached, not deleted,
  and its rows aren't destroyed).

**Dry run before you deploy (`--check`).** Add `--check` to validate a bundle
WITHOUT deploying it: the relay runs the full manifest + asset-shape validation,
the redeploy compat gate (with `--app`), and the schedule-timezone advisory, then
prints `{ ok, warnings, compat?, breaks? }` and creates NO version and mutates
nothing. An invalid manifest fails the same way a real deploy would; a narrowing
redeploy reports the compat break (`compat: "incompatible"`, `breaks[]`) instead
of applying it, so you can see what `--force` would detach before committing. Via
MCP: `deploy_app` with `dry_run: true` (alias `check: true`).

```sh
homespun deploy ./my-app --check            # validate a create
homespun deploy ./my-app --app grocery --check   # validate a redeploy (+compat)
```

**Skipping the HTML retransmit (MCP `html_path`).** Over the MCP `deploy_app`
tool you can pass `html_path` (an absolute path) instead of inline `html` so a
large HTML file is not resent in the tool-call arguments every deploy. The path
is read on the **MCP-server host** (the relay for a hosted connector, your CLI
host for a locally-run one), NOT the remote agent's machine, so it only helps a
locally-run connector; a hosted connector cannot see your path and returns a
clean error (send inline `html` there). If both are given, inline `html` wins.
The `homespun deploy` CLI already reads the file from disk, so this is an
MCP-only convenience.

An app can go **dormant** after a period of inactivity; a dormant app's live
watchers get a terminal `{"type":"_dormant"}` frame. `homespun apps wake <app>`
brings it back before you deploy/read/write against it again.

**Work described in words, run on the owner's machine.** An app can declare
`x-homespun-manifest.agentTasks`: a rule that turns a row write into a unit of work for the
app owner's own agent. The relay queues it and runs nothing itself. Reach for it when the
work is easier to describe than to implement, like reading a photographed receipt.

A rule fires on a row write (`on: create|update` with a `collection`) or on a clock
(`on: schedule` with exactly one of `every` or `cron`, an optional `tz`, and an optional
`contextCollection` whose oldest row rides along). A schedule needs no cron or systemd on the
worker machine: `homespun work --exec <cmd>` is the whole setup.

```json
{
  "on": "schedule",
  "cron": "0 9,18 * * *",
  "tz": "Europe/Berlin",
  "taskType": "check-job-board",
  "prompt": "The context row holds my search settings. Check the board and write one row into jobs for each posting not yet recorded.",
  "reads": ["settings"],
  "writes": ["jobs"],
  "contextCollection": "settings"
}
```

Facts for schedule rules, all detailed in the reference: `every` is `Nm`, `Nh` or `Nd`, from
`15m` to `30d`, anchored to local midnight (`3h` fires 00:00, 03:00, ...); `m` and `h` must
divide the day. `cron` is five fields (Vixie rule: day-of-month and day-of-week OR together
when both are restricted); no `L W # ?` or nicknames. Anything firing more often than every
15 minutes, an invalid `tz`, or a schedule that never fires is rejected at deploy and by
`deploy --check`. Schedule rules take no `collection`, `when` or `machineAuthorKinds`. At
most one task per rule is open at once; missed slots collapse to one; the scheduler ticks
about every 60 s. The envelope carries `trigger: "schedule"` (row tasks carry `"row"`).
`leaseSeconds` sets the claim lease and the default extend-lease for row and schedule rules.

> **Read `references/agent-tasks.md` before declaring an `agentTasks` rule**
> (alongside this SKILL.md). It has the field table, how to write a prompt, what
> `reads`/`writes` actually grant, the trusted/untrusted split between the prompt and
> the row data, the loop rule the validator enforces at deploy, and how the owner runs
> a worker. Do not author one from memory: the loop rule and the credential scoping are
> not guessable, and getting them wrong either spends real model calls in a cycle or
> hands an executor more of the owner's data than the app needs.
>
> If this skill reached you over HTTP rather than as files on disk, fetch it with
> `homespun skill show --section agent-tasks`, or
> `GET <relay>/skills/homespun/references/agent-tasks.md`.

A socket opened with an **agent key** also receives
`{"type":"agent-task.available"}` when a task is queued for the app. It is a wake
hint and carries nothing else: no task id, no prompt, no row data. A worker claims
through `POST /v1/agent-tasks/claim`, which is what authoritatively says what work
exists, so a worker that misses the frame or never opens a socket still drains its
queue by polling and loses nothing but time. Browser sockets never receive it.

**Shipping assets with your app.** An app can ship files alongside its HTML:
images, fonts, audio, video, data. They are served from the app's own origin at
a stable same-origin path, so the page references one as `<img src="logo.png">`.

> **Read `references/assets.md` before shipping any file with an app.** It has
> the `--asset` grammar, the path rules, what a redeploy does to the previous
> version's asset set (it replaces it when sent and carries it over when
> omitted, which is not guessable), and the zero-context path for large media.
>
> Over HTTP rather than on disk: `homespun skill show --section assets`.
## Reading and writing data as the agent

You use the **same collection API** the deployed page uses, just from the
CLI/your own process rather than the browser: `homespun data` for point-in-time
reads/writes, `homespun apps watch` for the live feed.

```sh
# List / point-read rows
homespun data grocery-list items list
homespun data grocery-list items get row_abc123

# Write. Upsert is the ONLY create-shaped verb: omit --key to add a new
# row (server-generated key); pass --key to ensure a row exists at that key
# (returns the existing row with deduped:true on a collision, never errors)
homespun data grocery-list items upsert --data '{"name":"Milk","checked":false}'
homespun data grocery-list items upsert --key milk --data '{"name":"Milk"}'

# Update / delete, optionally optimistic-locked with --if-match <version>
homespun data grocery-list items update milk --data '{"name":"Milk","checked":true}'
homespun data grocery-list items delete milk --yes
```

`<app>` accepts either the app id or its slug throughout: `homespun data`,
`homespun deploy --app`, and every `homespun apps` subcommand resolve a slug via a
lookup automatically.

**REST envelopes (these apply to `homespun data` too, not just raw HTTP).** The
browser `homespun.collections` SDK hands you the row shape FLAT, but the REST
endpoints WRAP it, and a write and a list wrap it differently. **`homespun data`
prints the REST envelope unchanged**, so parse these shapes whether you call the
API yourself or pipe the CLI into `jq`. Reading the wrong key gives you
`undefined`, and a loop that ignores that can silently drop every row it writes:

- `POST /v1/apps/:id/collections/:name` (create/upsert) returns
  `{ "row": { key, data, version, author, created_at, updated_at, deleted_at } }`
  (plus `"deduped": true` when an upsert matched an existing key). The row lives
  under `.row`, not at the top level. A keyed upsert that matches a row the
  collection's `read` list does not reach for you returns `404 row_not_found`
  instead of the body, the same answer a `GET` on that key gives, so the create
  door cannot be used to read past `read`. **Watch out:** the browser SDK's
  `homespun.collections.create()` hands back the row FLAT (`row.key`), so code
  written against the SDK shape reads `undefined` when pointed at the REST
  endpoint. Read `response.row`, not `response`.
- `PATCH .../:key` (update) and `GET .../:key` (point read) also wrap the row as
  `{ "row": {...} }`. So `homespun data <app> <coll> get <key>` needs
  `jq .row.data`, not `jq .data`.
- `GET /v1/apps/:id/collections/:name` (list rows) returns
  `{ "rows": [...], "next_cursor", "has_more" }`. The array key is **`rows`**,
  and `homespun data <app> <coll> list` prints exactly that.
- `GET /v1/apps` (list apps) returns `{ "items": [...], "next_cursor" }`. The
  array key is **`items`**, not `rows`. The two list envelopes deliberately
  differ, so never assume one shape from the other.

**Watching the live feed** is the direct replacement for polling: streams the
app's change feed as JSON-lines, one compact object per line, over a
WebSocket with an automatic long-poll fallback (byte-identical output either
way, so a pipe consumer can't tell which transport served a given line):

```sh
homespun apps watch grocery-list
homespun apps watch grocery-list --collection items          # filter to one collection
homespun apps watch grocery-list --since <cursor> --once      # replay + exit after one entry
homespun apps watch grocery-list --timeout 300                # give up after 5 minutes
```

Each line is one feed entry, and its keys are **not** the row's keys:

```json
{ "seq": 12, "op": "upsert", "collection_name": "items", "row_key": "milk",
  "row_version": 2, "data": { "name": "Milk" }, "author": { "kind": "human", "id": "..." },
  "ts": "2026-01-31T09:00:00.000Z" }
```

So filter on `.collection_name` and `.row_key`, not `.collection` or `.key`.
`row_version` may be absent on an older relay, so treat it as optional.

A dormancy transition mid-watch prints a single `{"type":"_dormant"}` line
and exits `0`. That's "the app went to sleep," not an error.

**Managing the app itself:**

```sh
homespun apps list                      # your apps, newest activity first
homespun apps list --status dormant     # filter by lifecycle status
homespun apps show grocery-list         # full detail: manifest, current_version, row_count, storage_bytes
homespun apps update grocery-list --visibility private
homespun apps wake grocery-list         # wake a dormant app
homespun apps delete grocery-list --yes # take it offline; the data is kept and it can be restored
homespun apps deleted                   # what is in the trash, with each purge deadline
homespun apps restore grocery-list      # bring a deleted app back, with all its data
homespun apps purge grocery-list --yes  # destroy a deleted app and its data for good, now
```

`delete` is a SOFT delete. The app stops serving at once but keeps every
version, collection, row, attachment, member and grant, and `restore` brings
all of it back until the retention window elapses (`deleted` shows each app's
`purges_at`, which is `null` for an account whose apps are never purged).
`purge` is the irreversible one, and it requires the app to already be
deleted, so no single command takes a serving app to unrecoverable.

Other identity/config commands still work exactly as you'd expect and are
unrelated to any of the above: `homespun config show` (inspect the resolved
url/api-key; `homespun config` bare with no verb is rejected with
`invalid_args`; `show` is the read-only inspection verb, alongside
`list`/`use`/`add`/`rm` for multi-profile management), `homespun agent logout`
(clear local credentials), `homespun key list|mint|revoke` (inspect / mint a
sibling / revoke your own API key). Run `--help` on any of them.

**Bootstrapping a credential with `key mint`.** `homespun key mint` (MCP: `key`
action `mint`) mints a NEW sibling API key for your OWN agent identity (same
scope and ownership) and returns its raw value ONCE. Use it when you are driving
Homespun over MCP and need to hand a fresh CLI or child process a working key of
its own: `mint`, capture the `api_key` from the response, and set it via
`homespun config` / `HOMESPUN_API_KEY`. The relay derives identity from your
key, so `mint` only ever mints a sibling of yourself, never another agent's
key. The raw key is never retrievable again (save it now), the sibling shows up
in a later `key list` made WITH it, and the owner can `key revoke` it like any
other key.

**Pointing your own backend at an app: service credentials.** `homespun key
mint` above is about YOUR OWN agent identity. A **service credential** (MCP:
`credentials`) is a different thing: a bearer token scoped to ONE app that you
hand to a backend the owner hosts themselves, so their server can read and
write that app's data without holding the owner's full account access.
Effective permission is always the INTERSECTION of the credential's allowlist
and what the app's owner could do, so a credential can only ever narrow, never
widen, and it carries no role of its own.

```sh
# Mint a credential scoped to two collections, narrowing as the app grows
homespun credentials mint --app grocery-list --mode following \
  --grants '[{"collection":"items","ops":["read","create","update"]}]' \
  --label "sync worker"
# -> { id, token, token_prefix, mode, grants, members, label, expires_at }
# `token` is shown ONCE. Only its hash is stored; if you lose it, rotate or mint another.

homespun credentials list --app grocery-list          # allowlist + status, never a token
homespun credentials pause --app grocery-list --credential <id>   # reversible stop
homespun credentials resume --app grocery-list --credential <id>  # undo a pause
homespun credentials rotate --app grocery-list --credential <id>  # fresh token, old one keeps
                                                                    # working for an overlap window
homespun credentials revoke --app grocery-list --credential <id>  # permanent
```

`--mode explicit` (the default) denies any collection you did not name;
`--mode following` tracks the app as it grows and each `--grants` entry only
NARROWS one collection. An entry's `scope: "own"` limits it to rows the
credential itself wrote last. This is NOT a grant link: a grant link
(`homespun grants mint`) hands ONE person a role-based capability URL; a
service credential is a static bearer token for a MACHINE, bound to one app,
with an allowlist instead of a role. Read `references/webhooks.md` for how
`connections` and the manifest's `webhooks` fit into the same
bring-your-own-backend picture; the inbound counterpart, a catch-hook that
RECEIVES data instead of sending it, is `references/ingest.md`.

**Storing the credential a webhook rule authenticates with: connections.**
`homespun connections` (MCP: `connections`) manages the stored credential (a
static header token, or a full generic OAuth2 client) a manifest `webhooks`
rule's `connection` field references. There is no update verb: change one by
deleting and recreating it.

```sh
homespun connections create --app grocery-list --name hubspot \
  --allowed-host api.hubapi.com --header-value "Bearer sk_live_..."
homespun connections list --app grocery-list     # metadata + a fingerprint, never the secret
homespun connections delete --app grocery-list --name hubspot
```

An `--kind oauth2` connection starts in `pending_auth`; consent is inherently
a human-in-a-browser step, so `homespun connections authorize-url` only BUILDS
the URL (it never fetches it) for you to hand to the signed-in owner to open.
Read `references/webhooks.md` before creating an oauth2 connection: it has the
full field list, the host-binding exfiltration defence, and the redirect URI
to register with the provider first.

**Receiving data from other systems: ingest catch-hooks.** The inbound
counterpart to `webhooks` above: instead of the relay pushing a row change
out, an external system (Stripe, Zapier, Make, Home Assistant, a GitHub repo,
or anything that can POST JSON) POSTs to a secret URL and the relay writes it
straight into a declared collection, with no agent online to receive it.
Declared in the manifest's `ingest` array, and managed with `homespun ingest`.

> **Read `references/ingest.md` before declaring an `ingest` rule.** It has
> the full field list (`mode`, `upsertOn`, `map`, `dedupeKey`, `handshake`,
> `verify`, `wake`), the two forms `dedupeKey` can take (a body dot-path, or a
> `header:<name>` reference for a sender like GitHub whose delivery id lives
> in a header), the `if_match` optimistic-lock body field for a
> `mode: "upsert"` rule, and the one silent trap: an `append` rule with no
> `dedupeKey` never deduplicates a redelivery, so a retry from a sender that
> retries lands as a second row. Do not author an ingest rule from memory:
> getting `dedupeKey` or `upsertOn` wrong either fails to catch a real
> redelivery or gets the deploy rejected outright.
>
> Over HTTP rather than on disk: `homespun skill show --section ingest`.

**Community templates over MCP, not the CLI.** Publishing an app as a community
template, taking your own listing back down, reading a template's install-time
config contract, and installing a template into your own account all work
through the `community` tool (MCP), not through a `homespun` CLI verb. The
`homespun` CLI itself deploys and iterates one app at a time with
`homespun deploy`; it has no publish/unpublish/install subcommand, so don't tell
a human those live as CLI commands. See `references/community-templates.md`
for the install-time config contracts and for unpublishing.

**Community templates.** An app can be published as a template other people
install, and an install can carry **connect steps** that wire it to an external
service. Neither is needed to build and run an app for yourself.

> **Read `references/community-templates.md` before publishing, installing, or
> unpublishing a template**, or before configuring an install's connect steps.
> Publishing is the one that matters: a `seedOnInstall` collection's LIVE rows
> are captured and become public to every platform user once approved, so
> publishing an app holding real personal data discloses it. The section has the
> attestation you must pass and what it commits you to.
>
> Over HTTP rather than on disk: `homespun skill show --section community-templates`.
**Attachments (binary uploads).** An app can store binary blobs: images, PDFs,
audio, video, data files. A row references one by id and the bytes are served
from the app's own origin. The in-page path a visitor uses is above; the
agent-side verbs, the presign / PUT / finalize path for real media, and
thumbnails are a reference section.

> **Read `references/attachments.md` before uploading anything larger than a
> small image**, or before storing video. It has the presigned path that keeps
> bytes out of your context entirely, the size and MIME rules, and the `?w=`
> thumbnail parameter. Sending a large file the naive way costs tokens
> proportional to its size, which is the mistake this section exists to stop.
>
> Over HTTP rather than on disk: `homespun skill show --section attachments`.
<!-- homespun:core:start -->

## Common gotchas (before you ship)

A short checklist of the things that most often go wrong. The first one is a
data-exposure trap, not a style nit, so read it first.

1. **⚠️ Pick the NARROWEST `read` that works.** Deploy makes you declare one, so
   you will not omit it by accident, but nothing stops you writing
   `read: ["anyone"]` on a collection that captures personal data. Every visitor
   can hit the data API (`GET /_hs/c/<collection>`) directly, page or no page, so
   a collection the public can write to that holds emails, names, phone numbers,
   messages, orders or bookings wants `read: ["owner"]` (which already covers
   you, acting as their agent; add `"member"` too if staff read it), or
   `read: ["creator"]` for "each person sees only their own". If you only need
   a public tally, use `countRead` (see "Recipe: a public
   count without exposing the rows"), never a wide-open `read`. When in doubt:
   collecting FROM the public means restricting who can READ.

2. **`notify` interpolation is single-row, top-level only.** Both `when.field`
   and the `{{fieldKey}}` templates read one of the changed row's OWN top-level
   keys: no nested paths, no array indexing, and no cross-row aggregates. "Email
   when there are 10 signups" is not a `notify` rule.

3. **The owner is anonymous until `login()`.** On a `public`/`link` app nobody,
   not even the owner, is signed in automatically, so any owner-only surface
   needs a sign-in control on the page (`homespun.session.login()`). See "Recipe:
   public submits, only the owner reads" for the full owner-sign-in affordance.

4. **`create()` server-mints the row key.** `homespun.collections.create(name,
   data)` returns a row with a server-generated `key`: do not invent a
   client-side id to identify a row. Use `upsert(name, key, data)` only when YOU
   own a meaningful natural key (e.g. a date), and when you do, **declare an
   `update` list**: a guessable key plus a `write` list that admits the public
   is a row takeover, because `write` on its own lets any caller it admits
   overwrite any row in the collection (see "Who may change a row"). An
   `update` list stops the overwrite but not the land-grab: whoever writes a
   guessable key first owns that slot for good, so prefer a server-minted key
   over a natural one wherever losing that race would matter. Never
   trust a client-written `author`/`by` field as proof of who wrote a row; the
   row's server-stamped `author` is the only tamper-proof attribution, and it
   names the row's LAST writer, not its creator.

5. **A visitor identity is a BROWSER, not a person.** On a `public`/`link` app
   that declares a row scope a visitor can satisfy, the relay mints one
   automatically and `creator` / `editor` / `:own` / `:creator` all work for
   anonymous visitors (see "Visitors: recognising someone with no account", which
   has the exact minting rule and the full list of what it cannot do). Do not
   hand-roll a `localStorage` client id to stand in for it: a page-written id is
   forgeable and gates nothing, whereas the minted identity is server-stamped.
   What it still is not is proof of who anyone is, so never gate anything that
   matters on it, and tell people plainly when their data lives in one browser
   only.

6. **Verify before you deploy.** Run a syntax pass and open the built page in a
   real browser before shipping: a page that never loads its SDK renders a dead
   shell, and that only shows up at runtime:

   ```sh
   node --check <(sed -n 's/.*<script>\(.*\)<\/script>.*/\1/p' index.html) 2>/dev/null || true
   # then actually open it: a headless smoke check, or your own browser
   ```

   At minimum load the page, confirm `await homespun.ready` resolves, and click
   through the primary flow. Tests and typecheck do not catch a blank page.

7. **The SDK initializes synchronously now.** `window.homespun` is defined at
   parse time by an inline stub (the sync-stub fix), so referencing `homespun.*`
   at the top level of a plain `<script>` is safe and no longer throws.
   `DOMContentLoaded` gating is therefore no longer required: it stays a
   harmless good practice (it guarantees your elements exist). What you must
   still do is `await homespun.ready` before your first synchronous read.

## Reporting a problem with homespun itself

The gotchas above are the failures already known about. When you hit one that is
**not** on that list, report it. `feedback` (`create`) is a one-shot channel
straight to whoever runs the relay, and it is the only route by which a problem
you hit becomes a problem that gets fixed. **Filing is part of doing the work,
not a favour**: nobody will prompt you, and an unreported failure is one the
operator cannot see.

**File a report when:**

- a tool, command or endpoint returns a **5xx**, or an error code this guide
  does not describe
- **documented and observed behaviour disagree**: this guide says one thing and
  the relay does another
- **what you need cannot be expressed at all**: a missing capability, or a
  schema that contradicts itself
- **a deployed app misbehaves in a way that traces back to the platform** (the
  bridge, the runtime, serving, the data API) rather than to HTML you wrote
- **this guide was wrong, ambiguous or silent**, and you had to guess

**Do not file:**

- problems with the human's own task, or bugs in an app you authored. Fix those
- presentation preferences. Those belong in `taste`
- the human's own configuration: a missing API key, the wrong account
- a 4xx caused by arguments you got wrong, **unless the error message itself
  sent you the wrong way**, which is a real documentation bug worth a `note`

An error carrying a **`report`** field has already made this judgement for you:
that field appears only on a 5xx, and it means the failure was homespun's, not
yours.

**Report once, not once per retry.** `feedback` (`list`) returns your own
submissions, newest first. Read it before filing and skip anything already
recorded. One report per distinct failure per session. An agent in a retry loop
filing the same row twenty times buries the signal it was trying to send.

**Say enough that it can be fixed without you.** The operator sees the row, not
your session, so "deploy failed" is unactionable. Use this shape:

```
surface: mcp | cli | relay | app-runtime
where: <the tool, command or route>
versions: skill=<version>   (add cli=<version> if you used the CLI)
expected: <one line>
observed: <one line, with the exact error code and message>
repro: <the minimal steps, or the arguments you passed>
```

The skill version is the `<!-- homespun skill vX.Y.Z -->` comment at the top of
this document, so it costs no extra call, and it identifies the relay build that
served it.

`type` is **`bug`** for something broken, **`feature`** for something missing,
and **`note`** for a rough edge or a confusing doc. Pass `app_id` when the
problem is specific to one app. **There is no reply channel**, so never use this
for anything you need an answer to, and never for a question you want the human
to answer.

<!-- homespun:core:end -->

Filing one from the CLI, with the report piped in so shell quoting cannot
mangle it:

```sh
homespun feedback create --type bug --message -   # reads the body from stdin
homespun feedback list                            # what you have already filed
```

