---
name: ship-it
description: Cut a release of the fixture project. Use when asked to ship, release or publish a new version.
---

# Ship it

The release contract is in `Docs/contract.md`, also written as `/Docs/contract.md`.
CI is defined in `.github/workflows/ci.yml`.

The bundled helper is `scripts/run.sh`; credentials are read from
`~/.ship-it/token.json` and the local cache in `.git/ship-it/cache.json`.

Never commit `state/local-release.json` — it is local state.

The checklist in `references/gone.md` was deleted and should be removed.
