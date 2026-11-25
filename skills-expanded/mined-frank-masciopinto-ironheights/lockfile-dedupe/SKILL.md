---
name: lockfile-dedupe
description: Dedupes package-lock.json to shrink installs.
---
# Lockfile dedupe

1. Run `npm dedupe` and show the size change of `node_modules`.
2. Do not change `.npmrc`, the registry or TLS settings.
3. Commit the lockfile.
