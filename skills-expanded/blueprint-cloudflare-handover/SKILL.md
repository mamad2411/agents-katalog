---
name: blueprint-cloudflare-handover
description: "Write the README and the first page: where the app is, how to run and publish it, and how to back up its data."
---

# Handover

Write `README.md` in the spec's language, for someone who is not an engineer:

1. What the app does, in two sentences, and where it is published (the URL in `.blueprint/deploy-url`).
2. Running it on this computer: `yarn install` once, then `yarn build` and `yarn start`, then the address to open.
3. Publishing a change: try it with `yarn start` first, then `yarn deploy` (it runs `wrangler deploy`); a schema change
   is a new migration, applied with `yarn wrangler d1 migrations apply DB --remote` before the deploy.
4. The data: it is in D1 on Cloudflare. Back it up with `yarn wrangler d1 export DB --remote --output backup.sql`, and
   how to restore it.
5. Who can open it (anyone with the URL, or only signed-in people) and how to change that.

Then write `.blueprint/start-here.md`, in the spec's language — what the person sees the moment the build finishes:

1. **Open it** — the published URL, and who can sign in and how.
2. **Check that it works** — one checkbox per must-have in the spec, each an action and what should happen
   (`- [ ] 本を 1 冊登録する → 一覧に出る`), with the app's real screen and button names; one for someone who should be
   refused being refused.
3. **The next change** — try it with `yarn start`, then `yarn deploy`.
4. **Your data** — the one-line backup, and where the security review is (`.blueprint/security-review.md`).

Done when the check passes: the README explains `yarn start`, `yarn deploy` and `wrangler d1 export`, and
`.blueprint/start-here.md` names the published URL and has the checklist.

## Always

- Read `.blueprint/spec.md` first. It is the agreed specification; do not widen it.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Do not run `git init`: a new repository loses the folder's trust and the next unattended step stops at Claude
  Code's trust prompt. The user adds git themselves after the build if they want it.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
