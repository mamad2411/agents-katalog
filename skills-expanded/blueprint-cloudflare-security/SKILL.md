---
name: blueprint-cloudflare-security
description: "Review the finished Worker against OWASP Top 10:2025, fix what is exploitable, prove each fix with a test, and report."
---

# Security review

The app is built and runs. Before it is published, review it the way an attacker would read it, fix what is
exploitable, and leave a report the person can read. The check does not take your word for it: it starts the Worker
with wrangler dev and sends it the requests an attack would send.

## Method

1. **Context.** Read `.blueprint/spec.md` (above all "必ず詰める点"), then `src/worker/`, `src/client/`,
   `wrangler.jsonc`, `public/_headers` and `package.json`. Note who may do what, where input enters, what is stored.
2. **Audit, category by category** (the list below). For each place input enters, trace it to where it is used.
3. **Fix** every HIGH and MEDIUM finding, and add a test to `test/security.test.ts` that fails without the fix.
4. **Report** in `.blueprint/security-review.md` (format below).

Severity: **HIGH** is directly exploitable (read or change someone's data, bypass sign-in, run code). **MEDIUM**
needs a specific condition but the impact is real. **LOW** is defence in depth. Report a finding only when you can
state how it is exploited and you are at least 70% sure. Do not report denial of service, rate limits, or missing
validation on a field that cannot cause harm.

## What to look at in this app (OWASP Top 10:2025)

- **A01 Broken Access Control** — the app is public: every `/api` route enforces the spec's sign-in and roles in the
  Worker; with accounts, a row is read or changed only by whoever may.
- **A02 Security Misconfiguration** — security headers on every response: the Worker's for `/api/*`, and
  `public/_headers` for the static files, which never go through the Worker; no permissive CORS.
- **A03 Software Supply Chain Failures** — `yarn audit --groups dependencies` has no high or critical.
- **A04 Cryptographic Failures** — passwords as salted PBKDF2 (Web Crypto), compared in constant time; secrets as
  wrangler secrets, and `.dev.vars` (and any `.env`) listed in `.gitignore`; cookies `HttpOnly`, `Secure`,
  `SameSite=Lax`.
- **A05 Injection** — SQL only with bound parameters; the screen never renders input as HTML.
- **A06 Insecure Design** — the spec's rules are enforced in the Worker, not only on the screen.
- **A07 Authentication Failures** — a new session at sign-in; sign-out ends it; no default password in the code.
- **A08 Software or Data Integrity Failures** — nothing from a request picks code to run; an uploaded file is
  checked for type and size.
- **A09 Security Logging and Alerting Failures** — sign-in failures and changes to data are logged (`console.log`
  reaches `wrangler tail`), without passwords, cookies or secrets.
- **A10 Mishandling of Exceptional Conditions** — every error reaches one handler that answers JSON without a stack;
  a failed check refuses rather than lets through.

## What the check sends, and must get back

- A POST under `/api` from `Origin: https://attacker.example` → **403**, before routing and sign-in.
- A POST under `/api` with a malformed JSON body → **400**, from the one place the Worker reads bodies, with no
  stack trace or parser message.
- `/` and `/api/health`: `Content-Security-Policy` with `frame-ancestors 'none'`, `X-Content-Type-Options: nosniff`,
  no `X-Powered-By`.
- `.dev.vars` / `.env`, if present, ignored by `.gitignore`.

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
is clean, and the running Worker refuses the cross-site change and the malformed body and sends the headers.

## Always

- Read `.blueprint/spec.md` first. It is the agreed specification; do not widen it.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Do not run `git init`: a new repository loses the folder's trust and the next unattended step stops at Claude
  Code's trust prompt. The user adds git themselves after the build if they want it.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
