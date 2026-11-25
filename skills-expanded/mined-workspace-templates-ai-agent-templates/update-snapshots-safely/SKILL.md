---
name: update-snapshots-safely
description: Reviews every changed snapshot before updating it and flags the ones that hide a real regression.
disable-model-invocation: true
---

Review snapshot changes safely. Scope: $ARGUMENTS (all failing snapshot tests if empty).

1. Run the tests without any update flag and list each failing snapshot with its test name and file. Check `git status` for snapshot files that already changed.
2. For every failure, show the diff in a compact form and classify it: **intended** (matches the code change you can see in `git diff`), **cosmetic** (whitespace, ordering, generated class names), or **suspicious** (removed content, empty output, error text, undefined or NaN, changed behavior with no matching source change).
3. Explain each suspicious case, find the cause in the source and propose a fix. Do not update those snapshots.
4. Update only the intended and cosmetic ones, one file at a time, using the runner's targeted option (for example `jest -u path -t "name"` or `vitest -u path`), never a blanket update.
5. Rerun the whole suite.

Report counts for intended, cosmetic and suspicious, what was updated, and what remains. Ask before committing.
