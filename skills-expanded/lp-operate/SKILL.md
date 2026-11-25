---
name: lp-operate
description: "Deprecated install name for lp-execute. Use only when the user, a saved prompt, or a marketplace listing still says lp-operate. Prefer lp-execute for explicit wallet liquidity actions."
license: MIT
compatibility: "Install-compatible rename notice. Not a second execution workflow."
metadata:
  author: "Galleon Labs"
  version: "0.7.1"
  renamed-to: "lp-execute"
---

# LP operate

This skill was renamed to `lp-execute` in 0.4.0. Keep using that name for explicit wallet liquidity actions.

## First useful task

1. If `lp-execute` is already installed in this harness, load it and continue the user's explicit fund-moving request there. Exact confirmation, one-send tracking, receipt checks, and chain-state reconciliation still apply.
2. If it is not installed, tell the user to run `npx skills add galleonlabs/crypto-defi-skills --skill lp-execute` or to install the full package, then stop. Do not construct calldata, request approval, sign, or submit.
3. A recommendation, a prepared plan, or a connected wallet is not authorization.

## Boundaries

`lp-operate` is an install name, not a parallel execution procedure. Discover `lp-execute` by exact name; do not assume a sibling directory is present. Never import private keys. A user-controlled wallet stays outside this package.
