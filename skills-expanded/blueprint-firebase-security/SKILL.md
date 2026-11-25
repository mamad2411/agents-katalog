---
name: blueprint-firebase-security
description: "Before production, review the app against OWASP Top 10:2025, fix what is exploitable, prove it on the emulators, and redeploy dev."
---

# Security review

Everything is built and runs on dev. Before production, review it the way an attacker would read it, fix what
is exploitable, and leave a report the person can read. On Firebase the attacker does not need the screen: the
web config is public, so anyone can call Firestore and the callable functions directly with their own client.
The rules and the functions are the whole defence.

## Method

1. **Context.** Read `.blueprint/spec.md` (above all "必ず詰める点" and the access table), then `firestore.rules`,
   `functions/src/`, `firebase.json` and the web app's source. Note who may do what and where input enters.
2. **Audit, category by category** (the list below). For each rule and each callable, ask what a signed-in
   stranger, a signed-out visitor and a user of another role can do with a hand-written request.
3. **Fix** every HIGH and MEDIUM finding, and prove it in `test/blueprint/security.spec.ts` against the
   emulators: the attack is refused (`assertFails`, or the callable throwing) and the legitimate use still works.
4. **Report** in `.blueprint/security-review.md` (format below).
5. **Redeploy dev** the way the deploy-dev step does (new `.blueprint/build-id`, `firebase deploy --project dev`),
   even when nothing changed, so production ships exactly what dev now runs. Do not deploy to `prod`.

Severity: **HIGH** is directly exploitable (read or change someone's data, bypass sign-in or a role, run code).
**MEDIUM** needs a specific condition but the impact is real. **LOW** is defence in depth. Report a finding only
when you can state how it is exploited and you are at least 70% sure; a guess is not a finding. Do not report
denial of service, rate limits, quota exhaustion, or missing validation on a field that cannot cause harm.

## What to look at in this app (OWASP Top 10:2025)

- **A01 Broken Access Control** — every `match` opens only what the access table says; ownership and role come
  from `request.auth` (custom claims), never from a field the client wrote; `list` queries cannot read past what
  `get` allows; every callable checks `context.auth` and the role itself.
- **A02 Security Misconfiguration** — the rules end in deny-all; Hosting sends `Content-Security-Policy` (with
  `frame-ancestors 'none'`, and `connect-src` / `script-src` listing exactly the Firebase and Google hosts the
  app uses), `X-Content-Type-Options: nosniff` and `Referrer-Policy`; App Check enforced; no emulator setting
  reaches the production build.
- **A03 Software Supply Chain Failures** — `yarn audit` clean of high and critical at the root and in
  `functions/` (install `functions/` with yarn); no dependency the app does not use.
- **A04 Cryptographic Failures** — no service account key, private key or admin credential anywhere in the
  project or the built site; secrets for functions in Secret Manager, not in code or `.env` that is deployed.
- **A05 Injection** — the screen never renders stored text as HTML (`v-html` only on text the app wrote);
  functions build no query, URL, shell command or file path from input without checking it.
- **A06 Insecure Design** — the spec's rules (limits, states, who may change what) are in the rules or the
  functions, not only in the screen; field lists pinned with `keys().hasOnly` and `affectedKeys().hasOnly`.
- **A07 Authentication Failures** — only the sign-in providers the spec names are enabled; a signed-out or
  unverified user gets nothing the spec does not allow them.
- **A08 Software or Data Integrity Failures** — roles and privileges are set only by functions (custom claims),
  never by a document a user can write; uploaded files are checked by Storage rules for type and size.
- **A09 Security Logging and Alerting Failures** — privileged actions and refusals in functions are logged
  without tokens or personal data beyond what the spec needs.
- **A10 Mishandling of Exceptional Conditions** — callables throw `HttpsError` with a short message, never a
  stack or an internal error text; a failed check refuses rather than lets through.

## The report

`.blueprint/security-review.md`, in the spec's language. One section per category, its heading naming the id
(`## A01 …` through `## A10 …`), each with what you checked and every finding on a line of its own:

```
- HIGH fixed: <what was wrong, how it could be exploited> — <what changed, which test proves it>
- LOW accepted: <what, and why it is acceptable for this app>
```

The state is `fixed`, `open` or `accepted`. A HIGH or MEDIUM may not be `open` or `accepted`: fix it, or ask
through the blueprint question tool if fixing it would change what the spec asks for. A category with nothing
to report says what was checked and "指摘なし". Write the report before step 5, so the deploy comes after it.

Done when the check passes: the report covers A01–A10 with nothing HIGH or MEDIUM left open, the rules end in
deny-all, Hosting sends the headers, no private key is in the project, both audits are clean,
`emulator-test.sh security` passes, and dev serves a build deployed after the report and still renders.

## Always

- Read `.blueprint/spec.md` first. It is the agreed specification; do not widen it.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Never enable billing, deploy to production, delete data or handle a credential unless this step's gates say the
  user approved exactly that.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
