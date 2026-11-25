---
name: blueprint-supabase-security
description: "Review the built app against OWASP Top 10:2025 as an attacker would, fix what is exploitable, prove it on the local stack, and write the report."
---

# Security review

The app is built and runs. Before it is published, review it the way an attacker would read it, fix what is
exploitable, and leave a report the person can read. The check does not take your word for it: it resets the local
database to your migrations and seed, runs Supabase's own security linter, and tries every table as a stranger.

## Method

1. **Context.** Read `.blueprint/spec.md` (above all "必ず詰める点" and the four columns per table), then
   `supabase/migrations/`, `supabase/seed.sql`, `supabase/config.toml`, `src/client/`, `vite.config.ts` and
   `package.json`. Note who may do what, and where each rule is enforced.
2. **Audit, category by category** (the list below). Anything the screen checks, assume an attacker skips: they call
   the API with the publishable key from the page.
3. **Fix** every HIGH and MEDIUM finding, and add a test to `test/security.test.ts` that fails without the fix.
4. **Report** in `.blueprint/security-review.md` (format below).

Severity: **HIGH** is directly exploitable (read or change someone's data, bypass sign-in, run code). **MEDIUM**
needs a specific condition but the impact is real. **LOW** is defence in depth. Report a finding only when you can
state how it is exploited and you are at least 70% sure. Do not report denial of service, rate limits, or missing
validation on a field that cannot cause harm.

## What to look at in this app (OWASP Top 10:2025)

- **A01 Broken Access Control** — every table in `public` has row level security and a policy per allowed
  operation; ownership is checked in `with check` as well as `using`, so a row cannot be added or moved into someone
  else's name; a role comes from a table the user cannot write for themselves.
- **A02 Security Misconfiguration** — `_headers` on every page, with the CSP's `connect-src` naming only this
  build's Supabase; sign-up open only as far as the spec says; nothing but `public` exposed through the API.
- **A03 Software Supply Chain Failures** — `yarn audit --groups dependencies` has no high or critical.
- **A04 Cryptographic Failures** — the page gets the publishable key only; the secret key stays out of `src/`, the
  build and any `VITE_` value; `.env*.local` files are in `.gitignore`.
- **A05 Injection** — no SQL built from strings in functions (`format()` with `%L`/`%I`, or parameters); the screen
  never renders input as HTML.
- **A06 Insecure Design** — every rule the spec states is enforced in Postgres (policy, constraint or function),
  not only on the screen.
- **A07 Authentication Failures** — Supabase Auth only; no password kept anywhere else; sign-out ends the session.
- **A08 Software or Data Integrity Failures** — a `security definer` function checks its caller and pins
  `search_path`; an uploaded file is checked for type and size by a Storage policy.
- **A09 Security Logging and Alerting Failures** — say where sign-in failures and data changes can be seen (the
  Supabase dashboard's logs) and what is not logged.
- **A10 Mishandling of Exceptional Conditions** — a failed call is shown in words, and a refusal refuses: no policy
  or function lets a row through when a lookup fails or returns NULL.

## What the check does, and must see

- Supabase's security linter (`yarn supabase db advisors --local --type security`) reports nothing.
- Every table in `public`, starting from the seed: a signed-out visitor and a freshly signed-up user who owns
  nothing each try to read a seeded row, add a row (empty, and a copy of the seeded row's values), add that copy in
  the seeded row's owner's name in each user column (a foreign key to `auth.users`, a default of `auth.uid()`, or a
  column whose seeded value is a user's id),
  change a seeded row to its own values, move it into their own name (every user column set to them; declared only
  as `update-owner`, never covered by `update`), and delete it. Whatever gets through must be listed in `.blueprint/public-access.json` for that operation and that kind
  of user. What it cannot try, `test/security.test.ts` proves: an owner moving their OWN row into someone else's name
  (the strangers own nothing), and a policy that opens only for a value the seed does not hold.
- The served page has a Content-Security-Policy with `frame-ancestors 'none'`, `X-Content-Type-Options: nosniff`,
  no `X-Powered-By`, and no secret key or service_role key anywhere in `dist/` or in any `.env` file.
- `.env` and `.env*.local` files, if present, ignored by `.gitignore`.

## The report

`.blueprint/security-review.md`, in the spec's language. One section per category, its heading naming the id
(`## A01 …` through `## A10 …`), every finding on a line of its own:

```
- HIGH fixed: <what was wrong, how it could be exploited> — <what changed, which test proves it>
- LOW accepted: <what, and why it is acceptable for this app>
```

The state is `fixed`, `open` or `accepted`; a HIGH or MEDIUM may be neither `open` nor `accepted`. A category with
nothing to report says what was checked and "指摘なし".

Done when the check passes: the report covers A01–A10 with nothing HIGH or MEDIUM left open, the tests pass, the audit
is clean, the linter reports nothing, the strangers get only what is declared, and the page sends the headers and no
secret.

## Always

- Read `.blueprint/spec.md` first. It is the agreed specification; do not widen it.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Do not run `git init`: a new repository loses the folder's trust and the next unattended step stops at Claude
  Code's trust prompt. The user adds git themselves after the build if they want it.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
