---
name: blueprint-supabase-auth
description: "Add the spec's sign-in with Supabase Auth, open sign-up only as far as the spec says, and prove it."
---

# Sign-in

A published app can be opened by anyone who has its URL, and its publishable key is in the page. Read the spec's
sign-in choice.

- **None**: nobody signs in. Only what `.blueprint/public-access.json` allows for `anyone` is reachable. Say so on the
  main screen's footer.
- **Accounts (email and password)**: Supabase Auth. A sign-in screen, sign-up only if the spec lets people register
  themselves, sign-out. In `supabase/config.toml`: `[auth] enable_signup` as the spec says (not `[auth.email] enable_signup`, which turns
  email sign-in off altogether), `site_url` and
  `additional_redirect_urls` to the local `yarn start` address (the publish step adds the published one).
- **Email link**: the same, with `signInWithOtp`; locally the mail lands in the stack's mail viewer, so `db:start`
  must not leave out `mailpit`.
- **Only a company's people**: say in `.blueprint/open-questions.md` how it is limited (an allowed email domain
  checked in the policies with `(select auth.jwt() ->> 'email')`, or single sign-on on a paid plan).

Roles, if the spec lists them: a `profiles` (or `members`) table keyed by the user's id, written only by whoever the
spec says, and read by the policies — never a value the user can set on themselves.

`test/auth.test.ts`: a user signs in with the right password and is refused with a wrong one; signed out, what the
spec reserves for signed-in people is refused; if sign-up is closed, signing up is refused.

Done when the check passes: `yarn build` and `yarn test` succeed and `test/` has the auth tests.

## Always

- Read `.blueprint/spec.md` first. It is the agreed specification; do not widen it.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Do not run `git init`: a new repository loses the folder's trust and the next unattended step stops at Claude
  Code's trust prompt. The user adds git themselves after the build if they want it.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
