---
name: qa-answer-review-program
description: >-
  Program lens of qa-answer-review: check whether the system actually does what a prepared meeting
  answer says — find the endpoint, screen, job or validator in the source repositories, and the
  release tag that ships it. Use WHENEVER the work is "program review of a prepared answer", "does
  the system really do this", "does this API exist / which version", "ระบบทำแบบที่ตอบได้จริงไหม",
  or when qa-answer-review fans out its lenses. Read-only.
---

# Program lens

Per row: **can the code back this answer up today, and in which release?**

## Where to look

- **Routes:** the API's route inventory if the project keeps one, otherwise the controllers /
  routers themselves. External surfaces (public API, webhooks, API keys, file import) usually live
  in their own module — find them once and list them in your evidence.
- **Screens:** the web apps' menu / route config, then the page component. Note which app and
  which role the screen belongs to; a feature absent from one role's menu is not absent from the API.
- **Release:** `git tag --contains <commit>` on the fix/feature commit. Release tags vs UAT builds
  are different things; merged-not-tagged = "not released yet".
- **Behaviour details** (duplicate / idempotency guards, error responses, validation): read the DTO
  and the service, quote file:line.

## Verdicts

- `OK` — found, released; the note names the feature the way the customer sees it (screen or API
  name), never a file path.
- `ADJUST` — exists but narrower than stated (one form only, UAT only, no export button).
- `WRONG` — the system does the opposite or has nothing like it.
- `OPEN` — the answer says "to be agreed" and the code has no position yet; say what the current
  code would do by default if relevant.
- `N/A` — pure process / commercial rows.

`git grep` has no `\b`; use `([^0-9A-Za-z]|$)`. Output contract and tone rules: `answer-review/SKILL.md` §1.
