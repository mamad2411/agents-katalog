---
name: blueprint-firebase-deploy-production
description: "Deploy the same build to the production project."
---

# Publish to production

This is the **deploy-production** gate: the user has approved it. Deploy the same source that was verified on dev — do not change anything between the two.

1. `yarn build`, then give this build an id and ship it with the site:
   `node -e 'console.log(require("crypto").randomUUID())' > .blueprint/build-id && cp .blueprint/build-id dist/blueprint-build.txt`,
   then `firebase deploy --project prod`. The check compares the served id with `.blueprint/build-id`, so it
   proves THIS build is live. Git is not needed for this.
2. Tell the user the URL and that the next change should go through dev first.
3. Write `.blueprint/start-here.md`, in the spec's language. It is what the person sees the moment the build
   finishes, so it answers "now what?" in the order they will need it:
   - **Open it** — the production URL (`https://<prod-project-id>.web.app`) and who can sign in, and how.
   - **Check that it works** — one checkbox per must-have in the spec, each an action and what should happen
     (`- [ ] 申請を 1 件出す → 承認者の一覧に出る`), using the app's real screen and button names; one for
     someone who should be refused (another account, a signed-out visitor) being refused.
   - **The next change** — edit, try it on dev (`https://<dev-project-id>.web.app`), then publish to production;
     never straight to production.
   - **Costs and safety** — the budget alert and where it goes; where the security review is
     (`.blueprint/security-review.md`).

   Keep it short: it is a first page, not the manual.

Done when the check passes: the production site serves the id this deploy wrote to `.blueprint/build-id`, and
`.blueprint/start-here.md` names the production URL and has the checklist.

## Always

- Read `.blueprint/spec.md` first. It is the agreed specification; do not widen it.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Never enable billing, deploy to production, delete data or handle a credential unless this step's gates say the
  user approved exactly that.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
