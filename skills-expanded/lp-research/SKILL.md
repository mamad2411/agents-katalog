---
name: lp-research
description: "Deprecated install name for lp-analyze. Use only when the user, a saved prompt, or a marketplace listing still says lp-research. Prefer lp-analyze for pool comparison and risk assessment before capital is deployed."
license: MIT
compatibility: "Install-compatible rename notice. Not a second analysis workflow."
metadata:
  author: "Galleon Labs"
  version: "0.7.1"
  renamed-to: "lp-analyze"
---

# LP research

This skill was renamed to `lp-analyze` in 0.4.0. Keep using that name for pool comparison and risk assessment.

## First useful task

1. If `lp-analyze` is already installed in this harness, load it and continue the user's comparison or due-diligence request there.
2. If it is not installed, tell the user to run `npx skills add galleonlabs/crypto-defi-skills --skill lp-analyze` or to install the full package, then stop. Do not invent a substitute analysis.
3. Do not request approvals, connect a wallet, sign, or submit transactions.

## Boundaries

`lp-research` is an install name, not a parallel research procedure. Discover `lp-analyze` by exact name; do not assume a sibling directory is present. Wallet keys and execution tools stay outside this package.
