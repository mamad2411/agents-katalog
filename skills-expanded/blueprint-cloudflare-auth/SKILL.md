---
name: blueprint-cloudflare-auth
description: "Put in the sign-in the spec chose; a published Worker is open to anyone."
---

# Sign-in

A published Worker can be opened by anyone who has its URL. Read the spec's sign-in choice.

- **None**: only what the spec says a visitor may see and do is reachable. Say so on the main screen's footer.
  `test/auth.test.ts` proves an operation the spec reserves (if any) is refused without a session.
- **One shared password**: a sign-in screen; the password's PBKDF2 hash (Web Crypto, per-install salt) as a wrangler
  secret (`.dev.vars` locally, in `.gitignore`); a signed, HttpOnly, Secure, SameSite=Lax session cookie; every `/api`
  route except `/api/health` and sign-in refuses without it.
- **One account per person**: a `users` table (PBKDF2 hash with a per-user salt), sign-in and sign-out, roles if the
  spec lists them, checked on the server for every route. If the spec says only a company's people may sign in,
  Cloudflare Access in front of the Worker is the simplest door: say so in `.blueprint/open-questions.md`.

`test/auth.test.ts`: a request without a session is refused, with one it passes; a wrong password is refused.

Done when the check passes: `yarn build` and `yarn test` succeed and `test/` has the auth tests.

## Always

- Read `.blueprint/spec.md` first. It is the agreed specification; do not widen it.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Do not run `git init`: a new repository loses the folder's trust and the next unattended step stops at Claude
  Code's trust prompt. The user adds git themselves after the build if they want it.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
