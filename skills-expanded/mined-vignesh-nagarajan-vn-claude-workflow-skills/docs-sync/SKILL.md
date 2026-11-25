---
name: docs-sync
description: Work out which documentation a code change made stale and update only those files, using a per-repo .claude/docs-map.yml instead of re-reading every doc. Use after changing behavior, routes, commands, environment variables, dependencies, schemas, or UI; when asked to update or check the docs; and before calling any change done in a repo that keeps its docs current.
---

# docs-sync

A change that leaves the docs stale is not done. The cost trap is that "check the docs" usually means re-reading every doc in the repo. The map turns it into a targeted edit.

## Order of operations

```bash
python <skill>/scripts/stale_docs.py
```

That prints the docs a change made stale, and the source file that triggered each one. Open only those, edit only the affected sections, and re-run to confirm.

If it reports no map, set one up:

```bash
python <skill>/scripts/stale_docs.py --init
```

That writes `.claude/docs-map.yml` from a template. Fill it in against the actual repo, then commit it.

## Flags

| Flag | Effect |
| --- | --- |
| `--base main` | Also count everything this branch changed since it forked from `main`. Use when reviewing a whole PR. |
| `--staged` | Only what is staged. Use from a pre-commit hook. |
| `--verify` | Exit nonzero if a mapped doc is stale and was not itself edited. Use in CI. |
| `--json` | Machine readable. |

## Writing the map

Keys are globs over source paths. Values are the docs that depend on them.

```yaml
"app/api/**":
  - README.md
  - docs/API.md

"package.json":
  - README.md
  - docs/DEPLOYMENT.md
```

Rules that keep the map honest:

- Map to the **narrowest** doc that owns the fact. If routes live in `docs/API.md`, do not also list the README unless the README genuinely restates routes.
- A glob that maps to five docs is usually wrong. It means one doc is repeating another, which is the real problem to fix.
- Env vars, commands, and dependencies are the three that go stale most often. Map them explicitly.
- Add a map entry the same day you add a doc. A map nobody maintains is worse than no map, because it reports clean.

## Editing the stale doc

Change the smallest span that carries the fact. Do not rewrite surrounding prose, do not reorder sections, do not "improve" adjacent text. A docs-sync diff should be readable as a fact update.

Bump any `Last verified` or `Last updated` date in the files you touched.

Prose in the edit follows [prose-guard's rules](../prose-guard/references/rules.md). Run that linter afterwards if the edit was more than a few words.

## When there is no map

For a repo without one, do not fall back to reading everything. Grep for the changed identifier across `*.md` and open only the hits:

```bash
git grep -ln "OLD_ENV_VAR\|oldFunctionName" -- "*.md"
```

Then offer to write the map so the next change is cheap.
