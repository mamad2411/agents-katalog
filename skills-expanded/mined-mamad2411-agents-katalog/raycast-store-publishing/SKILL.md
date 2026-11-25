---
name: raycast-store-publishing
description: "Package and submit a Raycast extension to the Raycast Store — manifest metadata, icon and screenshots, changelog/versioning, the publish flow (PR to the extensions repo), and review-guideline readiness. USE WHEN preparing to publish, updating, or passing review for a Raycast extension. Defer exact requirements to developers.raycast.com."
cluster: raycast
version: 1.0.0
---

# Raycast Store Publishing

Getting an extension into the Raycast Store is a metadata + review exercise on top of a working
build (`raycast-core`). This spoke is the checklist; confirm current specifics at
developers.raycast.com.

## Pre-submission checklist (manifest & assets)

- **Identity**: clear `title`, a concise benefit-led `description`, an `author`, and accurate `categories`.
- **Icon**: 512×512 PNG (light + dark friendly); follow Raycast's icon conventions.
- **Commands**: every `commands[]` entry has a meaningful `title` and `subtitle`; no dead commands.
- **Screenshots**: real, representative captures at the required dimensions (use Raycast's window-capture); first screenshot is the hero.
- **Changelog**: a `CHANGELOG.md` entry for this version; bump the version sensibly.
- **README**: what it does, setup (API keys via preferences), and any caveats.

## The publish flow

1. `ray build` clean (typecheck + lint pass; no `console` noise, no secrets committed).
2. Run the publish command (`npm run publish` / `ray publish`) — it opens a **pull request to the `raycastapp/extensions` repository**.
3. Raycast's automated checks + human review run on the PR; respond to review feedback.
4. On merge, the extension goes live in the Store.

## Passing review (common rejections)

- **Secrets in code** → move to `preferences` (password type), read via `getPreferenceValues`.
- **Poor empty/loading/error states** → handle `isLoading`, empty `List`, and failures with toasts.
- **Unclear actions** → every list item needs a sensible primary `Action` and `ActionPanel`.
- **Naming/branding** → don't imply official affiliation; follow trademark/naming rules.
- **Destructive actions without confirmation** → wrap in `confirmAlert`.
- **Performance** → don't block the UI; use the `@raycast/utils` data hooks.

## Updating

- Same flow for updates: edit, add a CHANGELOG entry, bump version, re-run publish (new PR).
- AI extensions: keep `tools[]` descriptions and evals current → `raycast-ai-extensions`.

## Guardrails

- No secrets in the repo — preferences only.
- Real screenshots + 512px icon + accurate categories before submitting.
- Handle loading/empty/error states and confirm destructive actions (review will catch these).
- Treat the Store review guidelines at developers.raycast.com as authoritative; this is a readiness checklist, not the rulebook.
