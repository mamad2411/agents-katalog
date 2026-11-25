---
name: use-auth
description: >
  AUTHENTICATION and the four tables it owns — who the people of this project are, where they are
  stored, and what you may and may not do with them. Load it before any page or door that lists
  accounts, changes roles, shows "who am I", or touches `users`, `sessions`, `accounts`,
  `verification_tokens`. Two facts here are the opposite of what the architecture suggests: those
  tables live in the SAME database as your products (not in a separate auth database), and they are
  not yours — the auth service on :3001 writes them, and deleting any of the four destroys every
  account on the server.
---

# use-auth

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

## 1. 🔒 One database, and the accounts are already in it

`DATABASE_URL` of the auth service points at **the same file as the app** — on a live server,
`file:/opt/fractera/app/data/app.db`. So `users` sits beside `products`, and the data layer `:3300`
lists it like any other table.

This is worth stating because the code's DEFAULT says otherwise: `services/auth/lib/db/index.ts`
falls back to its own `data/auth.db`, and reading only that line leads to "two separate databases",
which is false on every deployment. **Check the running configuration, not the fallback.**

Consequence, and it is the useful half: **you do not need the auth service to READ accounts.** The
data layer answers `/db/tables/users`, and `lib/db` reaches it the same way it reaches products.

## 2. The four tables, and what each is for

| Table | What it holds | Touch it? |
|---|---|---|
| `users` | the account itself: `id`, `email`, `nickname`, `roles` (JSON string), `avatar_url`, `bio`, `locale`, `timezone`, `provider`, `email_verified`, `is_active`, `last_login_at`, timestamps | read freely; write only `roles` / `is_active` / profile fields, through a door that enforces §4 |
| `sessions` | live browser sessions — `user_id`, `expires`, `session_token` | never; the service creates and expires them |
| `accounts` | links to external providers (Google and friends): tokens, `provider_account_id` | never |
| `verification_tokens` | one-time tokens for email confirmation and the like | never |

🔒 **These four are NOT declared in your `SCHEMA` (`lib/db/index.ts`), and that is correct.** The auth
service creates and migrates them. Do not add them to `SCHEMA` "so they are visible" — two owners of
one table is how a migration silently reverts somebody's column.

🔒 **DELETING ANY OF THE FOUR DESTROYS EVERY ACCOUNT ON THE SERVER**, including the owner's own, and
`app.db` is not in git — there is nothing to restore from. The same goes for dropping columns and
renaming them. A "cleanup" that removes tables your `SCHEMA` does not mention would take these first;
that is precisely why this paragraph exists.

**`password` is a bcrypt hash and never leaves the database.** The data layer strips it, along with
session and provider tokens, on the way out (`SECRET_COLUMNS` in `services/data/server.js`). Do not
route around that: a hash that left the database lives on in logs, in answers and in an agent's
context, where it cannot be taken back. Verifying a password is the service's job and yours never.

## 3. What the service does that a table cannot tell you

`:3001` owns everything about BECOMING logged in: the login and registration forms (they live on
`auth.<domain>`, not in your app), the session cookie, provider sign-in, `is_active` enforcement.
Your app never sees the moment of login — it sees a ready cookie. `lib/auth/get-session.ts` asks
`:3001/api/session` and gets `{ userId, email, roles }` or nothing.

Its admin doors, when you do need them: `GET /api/admin/users` (list, paged, `q` search) and
`PATCH|DELETE /api/admin/users/:id`. `PATCH` accepts `nickname`, `email`, `roles`, `is_active` —
**there is no password change in the API**, though the column exists.

**Out of the box:** registration and login by password, roles, sessions. **Missing: password
recovery** — a person who forgets theirs cannot get back in without the owner. Google sign-in and
email through Resend are prepared and need only keys in the panel. Underneath is NextAuth with some
eighty other providers; wiring any of them is a request to the Fractera developers, not slot work.

## 3a. 🔒 Where authentication physically lives in THIS repository

Nothing about it is hidden: read these eight files and you know the whole mechanism. Without that
reading the work is not hard, it is guesswork — which is why this map is here rather than a
description of it.

| File | What it decides |
|---|---|
| `proxy.ts` | the gate on every request: which paths are public, which need a session cookie, and that `/login`, `/register`, `/guest-login`, `/logout` (`AUTH_FORM_PATHS`) are **never served by this app** — they belong to the auth host |
| `lib/auth/get-session.ts` | how a session becomes `{ userId, email, roles }`: one call to `:3001/api/session` with the visitor's cookie. This is the only reader of the session in the whole app |
| `lib/auth/require-roles.ts` | the real lock of a door: `requireRoles(req, [...])` → 401 / 403 / null, plus `groupsOf()` when the answer is "what exactly may they do" |
| `lib/auth/require-role.ts`, `require-admin.ts` | older single-role variants of the same idea |
| `lib/auth/auth-bypass.ts` (+ `.edge.ts`) | why a locked page opens with no login at all: on a node the bypass is on only in `NODE_ENV=development`; `FRACTERA_IP_NODOMAIN_MODE` is the old server line's flag, a node never sets it (the installer leaves it empty) |
| `lib/auth-base-server.ts` | the address of `:3001` derived from the REQUEST host — `<ip>:3001` on an IP, `auth.<apex>` on a domain |
| `lib/runtime-urls.ts` | the same address derived in the BROWSER from `window.location`, plus `registerRedirectUrl()` which builds the sign-up link with `callbackUrl` |
| `components/auth/access-gate.client.tsx` | the visible half: what a person is told when their role is not enough |

**The flow, in one pass.** A visitor opens a protected address → `proxy.ts` checks for
`authjs.session-token` (or `__Secure-authjs.session-token` behind HTTPS) → no cookie and the path is
under `/api/*` → 401 immediately; a page instead renders and its `AccessGate` explains → the person
follows the link to `auth.<domain>/login`, a page of the auth service, **not of this app** → the
service sets the cookie on the shared parent domain → back on your page `get-session.ts` exchanges
that cookie for roles → your door compares them with `requireRoles`.

🔒 **Two consequences that catch people out.** First: on `localhost` the owner at the keyboard opens
the architect layer without any login (`lib/auth/owner-at-machine.ts`), and in local `dev` the bypass
does the same — a screen that works for you there may refuse everyone on the domain, so say which
address you tested on. The node does not answer on the computer's network IP at all. Second: the login page is
a different origin, so never `<Link prefetch>` it — `check:links` refuses that, because the prefetch
fails on CORS.

## 4. 🔒 Rules that must hold wherever roles are written

Whichever path you use — the data layer or the service — these are the rules, and they must live in
exactly ONE place. Splitting them between your door and the service is how they drift apart.

- **A role must exist in `ALL_ROLES`** (`lib/roles.ts`). The body of a request comes from a browser;
  an invented role does not fail loudly, it simply opens nothing, and that is found months later.
- **An account keeps at least one role.** No roles is not "a guest" — a guest is the absence of an
  account.
- **Nobody edits their own account** through an admin screen: that is what stops a person removing
  their own `architect` and locking the project.
- **Only an architect grants or removes `architect`.** An administrator who could hand it out would
  hand it to their own second account, and the difference between the two roles would vanish the same
  day. Compare the CURRENT roles with the REQUESTED ones — the rule guards that one role, not every
  edit.
- **A changed role reaches a signed-in person on their next session read**, not instantly. Say so
  rather than promising immediacy.

`roles` is stored as a **JSON string**, so parse it in one place and hand the array around; two
parsers give one account two different sets of roles on the same screen.

## 5. Building a screen about accounts

It is the dynamic-page model, and `use-dynamic-pages` carries the shape: static shell, data through
`/api/*`, `requireRoles` first line of the door — `proxy.ts` only proves a session EXISTS, so without
it any signed-in person reaches any role's data. Built example to copy:
`app/[lang]/(protectedLayer)/(admin)/administration/users/` with `app/api/users/`.

Never render `password`, never log a whole row, and remember `sessions` and `accounts` hold tokens
that are as good as a password.

## 6. Before you call it done

- Three states on the deployment, not one: guest → 401, signed in with the wrong role → 403 naming
  the role, right role → the data.
- Fetch the page as a guest and grep the markup for account data. Nothing may be there — the shell is
  prerendered.
- Read your own response body once: if `password`, `session_token` or a provider token appears in it,
  stop and fix the door, not the page.
