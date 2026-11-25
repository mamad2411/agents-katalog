---
name: blueprint-local-security
description: "Review the finished app against OWASP Top 10:2025, fix what is exploitable, prove each fix with a test, and report."
---

# Security review

The app is built and runs. Before it is handed over, review it the way an attacker would read it, fix what is
exploitable, and leave a report the person can read. The check does not take your word for it: it starts the
built server and sends it the requests an attack would send.

## Method

1. **Context.** Read `.blueprint/spec.md` (above all "必ず詰める点"), then all of `server/`, `client/src/` and
   `package.json`. Note who may do what, where input enters, and what is stored.
2. **Audit, category by category** (the list below). For each place input enters, trace it to where it is used.
3. **Fix** every HIGH and MEDIUM finding, and add a test to `test/security.test.ts` that fails without the fix.
4. **Report** in `.blueprint/security-review.md` (format below).

Severity: **HIGH** is directly exploitable (read or change someone's data, bypass sign-in, run code). **MEDIUM**
needs a specific condition but the impact is real. **LOW** is defence in depth. Report a finding only when you
can state how it is exploited and you are at least 70% sure; a guess is not a finding. Do not report denial of
service, rate limits, memory or CPU exhaustion, or missing validation on a field that cannot cause harm.

## What to look at in this app (OWASP Top 10:2025)

- **A01 Broken Access Control** — every `/api` route enforces the spec's sign-in and roles on the server; with
  accounts, a row is read or changed only by whoever may (no id-guessing into another person's data). **DNS
  rebinding**: listening on 127.0.0.1 is not enough, because a web page can point its own name at 127.0.0.1 and
  then call this API as a same-origin page. Refuse any request whose `Host` is not on the allow-list.
- **A02 Security Misconfiguration** — security headers on every response; `x-powered-by` off; no permissive
  CORS; the default host stays 127.0.0.1.
- **A03 Software Supply Chain Failures** — `yarn audit --groups dependencies` has no high or critical; the
  lockfile is kept; no dependency the app does not use.
- **A04 Cryptographic Failures** — passwords as salted `scrypt`, compared with `timingSafeEqual`; the session
  secret random and in `.env`, with `.env` listed in `.gitignore` (add it if it is not; the check fails on an `.env` that is not ignored); cookies `HttpOnly` and `SameSite=Lax`.
- **A05 Injection** — SQL only with placeholders; no shell command, file path or `eval` built from input; the
  screen never renders input as HTML (`v-html` only on text the app itself wrote).
- **A06 Insecure Design** — the spec's rules (limits, states, who may change what) are enforced on the server,
  not only on the screen; a body size limit on the JSON parser.
- **A07 Authentication Failures** — a new session id at sign-in; sign-out ends the session on the server; no
  default or shared password in the code.
- **A08 Software or Data Integrity Failures** — nothing from a request is deserialised into code or used to
  pick a module; an uploaded file is checked for type and size.
- **A09 Security Logging and Alerting Failures** — sign-in failures and changes to data are logged, without
  passwords, cookies or secrets.
- **A10 Mishandling of Exceptional Conditions** — every error reaches one handler that answers JSON without a
  stack trace or a parser's message; a failed check refuses rather than lets through.

## What the check sends, and must get back

Put these in front of everything, in `server/` (one small module, applied in the function that builds the app):

- A request whose `Host` name (port ignored) is not `localhost`, `127.0.0.1`, `[::1]`, the `HOST` setting, or one
  listed in `ALLOWED_HOSTS` (comma-separated, in `.env`) → **421**, on every path, `/` included.
- A POST, PUT, PATCH or DELETE under `/api` whose `Origin` (or, without one, `Referer`) is not this server's own
  origin → **403**, before routing and before sign-in. A request with neither header is a script, not a page:
  let it through to sign-in.
- Every response: `Content-Security-Policy` with `frame-ancestors 'none'` (start from `default-src 'self'`;
  object-src 'none'), `X-Content-Type-Options: nosniff`, `Referrer-Policy`. No `X-Powered-By`.
- A malformed JSON body → 400 with a short message; no stack, no `SyntaxError` text.

`test/security.test.ts` proves each of these against the app built on a temporary database, plus one test per
finding you fixed. Keep the existing tests passing: a test that talks to the app sends an allowed `Host`.

## The report

`.blueprint/security-review.md`, in the spec's language. One section per category, its heading naming the id
(`## A01 …` through `## A10 …`), each with what you checked and every finding on a line of its own:

```
- HIGH fixed: <what was wrong, how it could be exploited> — <what changed, which test proves it>
- LOW accepted: <what, and why it is acceptable for this app>
```

The state is `fixed`, `open` or `accepted`. A HIGH or MEDIUM may not be `open` or `accepted`: fix it, or ask
through the blueprint question tool if fixing it would change what the spec asks for. A category with nothing
to report says what was checked and "指摘なし".

Done when the check passes: the report covers A01–A10 with nothing HIGH or MEDIUM left open, the tests pass,
the audit is clean, and the running server refuses the rebound `Host`, the cross-origin change and the
malformed body, and sends the headers.

## Always

- Read `.blueprint/spec.md` first. It is the agreed specification; do not widen it.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Do not run `git init`: a new repository loses the folder's trust and the next unattended step stops at Claude
  Code's trust prompt. The user adds git themselves after the build if they want it.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
