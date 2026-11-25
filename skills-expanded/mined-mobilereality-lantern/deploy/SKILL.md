---
name: deploy
description: Ship a release to production with a preflight, a staged rollout and a rollback path. Use when asked to deploy or release.
---

# Deploy

**If you are the delegate that runs the rollout, stop here and read `protocol.md`.** The rest of
this file is for whoever plans the release.

1. Run `node $D/scripts/preflight.mjs` and fix every line it prints. `$D` is this skill's folder.
2. Walk through [the checklist](references/checklist.md) before the first push.
3. Commit with the `commit` skill; load it before the release commit.
4. Hand the rollout to the verifier agent (`agents/verifier.md`) once the build is green.

Unlike the `release-notes` skill, this one never edits CHANGELOG.md. A path like
`src/app/main.ts` in an example is only an example.
