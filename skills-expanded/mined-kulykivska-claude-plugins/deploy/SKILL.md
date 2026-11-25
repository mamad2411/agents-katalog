---
name: deploy
description: >-
  Deploy a Fly.io-hosted app safely and verify the rollout. Trigger on
  "deploy", "ship it to prod", or after merging work that must go
  live. Covers the push-to-main pipeline, the local flyctl fallback, the
  release_command gotcha, and post-deploy verification.
---

# Deploy (Fly.io)

## Default path: push to main

For apps wired to CI (deploy = push to main), the deploy IS the
push. Run the pre-push-review gate first, push, then watch CI through to the
Fly release.

## Manual path: local flyctl

```bash
fly deploy -a <app> --remote-only
fly status -a <app>          # all machines should reach `started`
```

**Known gotcha**: machines can get stuck in state `created` when the app has
a `release_command`. Fix: deploy via local flyctl without
the release_command (comment it out of fly.toml for the deploy, run the
migration manually), then restore.

## Post-deploy verification (always)

1. `fly status -a <app>`: every machine `started`, latest version.
2. `fly logs -a <app>` for the first minute: no crash loops, no tracebacks.
3. Curl the health endpoint AND one real feature endpoint; check the JSON,
   not just 200.
4. If the deploy included a model/artifact change: confirm the served model
   version/registry entry, and refreeze snapshots if serving behavior
   changed.

## Rollback

- Code: `fly releases -a <app>` then `fly deploy --image <previous-image>`.
- Models: use the model-registry restore flow (R2 models/archive/<version>/ +
  restore workflow) instead of redeploying code.
