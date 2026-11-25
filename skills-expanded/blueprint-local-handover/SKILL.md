---
name: blueprint-local-handover
description: "Write the README the user needs: how to start it, where the data is, and how to back it up."
---

# Handover

Write `README.md` in the spec's language, for someone who is not an engineer:

1. What the app does, in two sentences.
2. How to start it: `yarn install` once, then `yarn build` and `yarn start`, then the address to open.
3. Where the data is (`data/app.db`) and how to back it up: stop the app, copy the file. How to restore it.
4. Who can open it (this computer only, or with a password) and how to change that.

Then write `.blueprint/start-here.md`, in the spec's language. It is what the person sees the moment the build
finishes, so it answers "now what?" in the order they will need it:

1. **Start it** — `yarn install` (first time only), `yarn build`, `yarn start`, then the address to open
   (`http://localhost:3000`, or the `PORT` the app uses). How to stop it (Ctrl+C).
2. **Check that it works** — one checkbox per must-have in the spec, each an action and what should happen:
   `- [ ] 本を 1 冊登録する → 一覧に出る`. Use the app's real screen and button names. Add one for sign-in if the
   spec has any.
3. **Your data** — where it is (`data/app.db`) and the one-line backup, with a pointer to the README.
4. **If something goes wrong** — the port is taken (`PORT=3001 yarn start`); opening it from another computer
   (sign-in first, then `HOST` and `ALLOWED_HOSTS` in `.env`); where the security review is
   (`.blueprint/security-review.md`).

Keep it short: it is a first page, not the manual. The README is the manual.

Done when the check passes: `README.md` exists and explains `yarn start` and the backup of `data/app.db`, and
`.blueprint/start-here.md` says how to start it and where to open it, and has the checklist.

## Always

- Read `.blueprint/spec.md` first. It is the agreed specification; do not widen it.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Do not run `git init`: a new repository loses the folder's trust and the next unattended step stops at Claude
  Code's trust prompt. The user adds git themselves after the build if they want it.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
