---
name: aislop
description: Run the aislop code-quality scan with `bb aislop scan` — by default only on what the current branch changed against its root branch (committed or not), or on uncommitted, staged, or all files.
---

# aislop scan

`bb aislop scan` runs `npx aislop@latest scan` in the checkout, on the machine the
thread's environment lives on. Its exit code and report are aislop's own; a
one-line `aislop: scanning …` header on stderr says exactly what was compared.

```sh
bb aislop scan                         # this branch vs its root (default)
bb aislop scan --scope changes         # uncommitted changes vs HEAD (incl. untracked)
bb aislop scan --scope staged          # staged changes only
bb aislop scan --scope all             # the whole directory
bb aislop scan --base origin/develop   # branch scope against another ref
bb aislop scan packages/api --include src --exclude src/generated -d
bb aislop scan --json                  # aislop's JSON report on stdout
```

## Scopes

- `branch` (default) — every file changed since the branch forked from its root:
  commits on the branch plus staged, unstaged, and untracked files. The comparison
  point is `git merge-base HEAD <root>`, so commits that landed on the root after
  the fork are not reported as yours.
  - The root is the thread environment's merge-base branch, else its default branch
    (only when the scanned directory is inside that checkout), else `origin/HEAD`,
    else `main`/`master`, whichever exists first. The remote copy (`origin/<root>`)
    is used when it exists, so on the root branch itself the scan covers unpushed
    commits plus uncommitted work.
  - `--base <ref>` replaces the root; the merge-base is still used.
- `changes` — uncommitted changes against `HEAD`, untracked files included.
- `staged` — only what is staged.
- `all` — the whole directory, no diff.

## Notes

- The directory defaults to the current directory; a relative argument resolves
  against it. From a plain terminal (no thread) the scan runs on the bb server's
  own machine.
- `--timeout` defaults to 15m (max 25m). The first run downloads aislop through npx.
- Output past bb's 1 MiB CLI limit is truncated with a note; narrow with
  `--include` or drop `-d`/`--verbose`. Truncated `--json` output is not valid JSON.
- A base that cannot be resolved exits 2 with the reason, without running aislop.
