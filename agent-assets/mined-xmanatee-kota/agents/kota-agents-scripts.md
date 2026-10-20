# Repository Scripts

This directory contains deterministic repository maintenance and generation
commands.

- Scripts derive checked-in artifacts from source-owned contracts; generated
  outputs are never edited by hand.
- Every generator supports a non-writing freshness check for build and CI use.
- Keep paths rooted at the repository and output ordering deterministic.
- Put product/runtime behavior in `src/` or the owning client, not here.
