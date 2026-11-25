---
name: git-atomic-commits
description: >
  Split staged and unstaged git changes into hunk-level atomic Conventional
  Commits (plan first, commit after approval). Trigger on: atomic commits,
  split diff into commits, stage hunks separately, untangle dirty working
  tree, plan commits. Use `git-fixup` instead to fold changes into existing commits.
license: MIT
---

# git-atomic-commits — atomic hunk-level commit planner

Turn a dirty working tree (staged + unstaged) into an ordered set of atomic
Conventional Commits. Plan first; mutate only after explicit approval.

## Rules

| Rule | Behavior |
|------|----------|
| **Tracked-only scope** | Inspect `git status --porcelain`, `git diff HEAD`, `git diff --cached` only. Never stage, modify, or run `git add -N` / `git stash -u` on originally untracked (`??`) files. Warn if an untracked path looks related by dir/filename (read it only to confirm). |
| **Empty tree** | If `git diff HEAD` is empty, print `git status --short` counts (staged/unstaged/untracked), stop, and ask for explicit paths. Never inspect history or suggest reset/rebase. |
| **Append-only, no push** | Never `push`, `rebase`, `reset` (any rewriting mode), `amend`, `stash`, `--force`, or `filter-branch`. Respect hooks and GPG signing (no `--no-verify` unless asked). |

## 1. Preflight — single read-only probe

```bash
for p in MERGE_HEAD rebase-merge rebase-apply CHERRY_PICK_HEAD REVERT_HEAD BISECT_LOG; do
  test -e "$(git rev-parse --git-path "$p")" && echo "ABORT: $p in progress"
done
git status --porcelain
git diff HEAD --numstat
git diff HEAD | git hash-object --stdin
```

- Abort immediately if any check prints `ABORT:`.
- Run `git diff --cached --numstat` only if porcelain shows staged entries (`^[MADRC]`).
- Treat renames as one unit (`rename from/to`) and include deletions.
- Default exclusions (overrideable; list excluded paths in the plan as FYI): binaries (`- -` in numstat), `dist/`, `build/`, `*.png|jpg|pdf|zip`, and standalone lockfiles (`*.lock`, `package-lock.json`, `pnpm-lock.yaml`, `go.sum` — include only when paired with a manifest change, staged whole-file into `chore(deps)` without dumping their diff).
- Large diffs (>20 files or >5000 lines post-exclusion): batch top-level dirs into at most 4–5 parallel subagents to classify hunks while the main session owns final grouping and ordering. If context still overflows, ask the user to narrow paths — never silently truncate.

## 2. Analysis — file then hunk

```bash
git diff HEAD -U0 -- . ':!dist/*' ':!build/*' ':!*.lock' ':!package-lock.json' ':!pnpm-lock.yaml' ':!go.sum' ':!*.png' ':!*.jpg' ':!*.pdf' ':!*.zip'
```

Classify hunks in signal order:

1. **Relation**: same dir/feature, import/call edge, test pairing (`foo.ts` ↔ `foo.test.ts`), colocated docs.
2. **Role**: code (`src/**`) vs test (`*.test.*`, `tests/`) vs docs (`*.md`, `docs/`) vs config/CI (`*.json`, `*.yaml`, `Dockerfile`, `.github/`, `mise.toml`) vs chore.
3. **Hunk context**: `@@ ... @@ <symbol>` header + intent keywords.

**Functional atomicity beats layer split**: a feature plus its test plus its docs ships as one `feat`, not three. Split only orthogonal concerns (`feat` vs `fix` vs `refactor` vs unrelated features) and isolate pure `docs`, `chore(deps|config|ci)`, and `test`-only cleanups. A single file with unrelated hunks must be split across commits; record per-commit evidence as `path:line-range @@ header`.

## 3. Plan & Approval Gate

Order commits dependencies-first (`config/infra → feat → fix → refactor → test → docs`). Format every fenced commit message as strict Conventional Commits v1.0.0:
- Header: `type(scope)!: subject` where `type ∈ {feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert}`, `scope` is a short repo-path noun (`auth`, `ci`, `deps`), and `subject` is imperative, ≤72 chars, no trailing period.
- Body (optional): explain *why*, not what the diff already shows. Use a `BREAKING CHANGE: <description>` footer whenever `!` is set.
- Never put plan metadata (`Commit 1/5`, `Part X of Y`, `depends on #N`) inside the fenced message block; ordering lives in prose around it.

````markdown
1. feat(auth): add OAuth callback
   files: src/auth.ts:12-45 @@ handleCallback, src/routes.ts:8-20, src/auth.test.ts:1-30
   why: completes PKCE redirect flow so login sessions persist; tests co-located so atomic
   depends on: none
   message:
   ```
   feat(auth): add OAuth callback

   complete PKCE redirect flow so login sessions persist
   ```

2. fix(auth): handle token expiry
   files: src/auth.ts:80-95 @@ refreshToken
   why: unrelated bugfix hunk in same file, must split from feat above
   depends on: none — independent, can land in any order
   message:
   ```
   fix(auth): handle token expiry
   ```

Related untracked (ignored, not staged): `src/authExtra.ts` looks related to 1. — run `git add <path>` and re-run if you want it included.
Excluded: `dist/bundle.js (binary)`.
````

End every plan with: `Approve (yes / approve all / edits) to stage per-commit changes, verify git diff --cached -U0, and commit.`

**Stop after outputting the plan.** Require explicit `yes` / `approve all` / per-commit edits before any mutation. If the user edits the plan, re-verify grouping before executing.

## 4. Execute — patch-based partial staging

Before applying commit 1:
- Re-check `git diff HEAD | git hash-object --stdin` against the preflight hash; abort if the working tree drifted.
- If the index has staged changes (`! git diff --cached --quiet`), record pre-staged new-file paths (`git status --porcelain` matching `^A`), clear the index with `git read-tree HEAD`, then run `git add -N -- <those paths>` so pre-staged new files remain tracked with an empty index blob (the only permitted `git add -N`).

For each approved commit in order:
- **Whole-file changes** (every hunk of a tracked file, or a pre-staged new file after `git add -N`): stage directly with `git add -- <paths>` (or `git rm -- <paths>` for deletions).
- **Partial-file splits**: extract verbatim `-U0` hunks for commit N from a fresh `git diff HEAD -U0 -- <file>` against current `HEAD` (regenerate before each commit because prior commits shift line offsets) and apply via stdin so no `.patch` files pollute the tree. (If splitting a brand-new `git add -N` file across multiple commits, run `git rm --cached -- <file>` before applying its first `new file mode` patch.)

```bash
git apply --cached --unidiff-zero --recount <<'PATCH'
... verbatim -U0 hunks for commit N ...
PATCH
git diff --cached -U0   # must match planned files and hunks exactly
git commit -F - <<'EOF'
<exact fenced message>
EOF
```

- On staged diff mismatch or hook failure, abort that commit, leave prior commits intact, and report the remainder as unapplied.
- Finish with `git log --oneline -N` (N = commits created) and `git status --short`.
