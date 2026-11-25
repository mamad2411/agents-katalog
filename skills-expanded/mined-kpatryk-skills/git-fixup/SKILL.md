---
name: git-fixup
description: >
  Fold staged and unstaged git changes into existing branch commits via
  hunk-level fixup!/amend! commits and incremental --autosquash rebase.
  Trigger on: git fixup, autosquash, fold review feedback or bugfixes into
  earlier commits, amend previous commits on a PR branch. Use
  `git-atomic-commits` instead when changes should become new commits only.
license: MIT
---

# git-fixup — hunk-level fixup planner & incremental autorebaser

Absorb a dirty working tree (staged + unstaged files and hunks) into existing
commits on the current branch via `git commit --fixup` and newest-to-oldest
incremental `git rebase -i --autosquash`, proposing a fresh Conventional Commit
for any unmatched hunks. Plan first; create backup branches and mutate only
after explicit approval.

## Rules

| Rule | Behavior |
|------|----------|
| **Tracked-only scope** | Inspect `git status --porcelain`, `git diff HEAD`, `git diff --cached` only. Never stage, modify, or run `git add -N` / `git stash -u` on originally untracked (`??`) files. Warn if an untracked path looks related by dir/filename (read it only to confirm). |
| **Empty tree** | If `git diff HEAD` is empty, print `git status --short` counts (staged/unstaged/untracked), stop, and ask for explicit paths. Do not create backup branches, inspect history, or run rebase. |
| **Branch boundary & no push** | Target only commits inside `<base>..HEAD`. Never rewrite commits at or before `<base>` unless the user explicitly provides a range. Never run `git push` (normal or force). Respect hooks and GPG signing (no `--no-verify` unless asked). |

## 1. Preflight — single read-only probe

```bash
for p in MERGE_HEAD rebase-merge rebase-apply CHERRY_PICK_HEAD REVERT_HEAD BISECT_LOG; do
  test -e "$(git rev-parse --git-path "$p")" && echo "ABORT: $p in progress"
done
BRANCH="$(git symbolic-ref --quiet --short HEAD || echo DETACHED)"
test "$BRANCH" = "DETACHED" && echo "ABORT: detached HEAD"
git status --porcelain
git diff HEAD --numstat
git diff HEAD | git hash-object --stdin
```

- Abort immediately if any check prints `ABORT:`.
- Resolve branch base `<base>`:
  - **User-provided base/range**: validate `git rev-parse --verify <base>` and `git merge-base --is-ancestor <base> HEAD`, then review scope with `git log --oneline --no-decorate <base>..HEAD` and `git log --oneline --name-only <base>..HEAD | head -50`.
  - **Auto-resolved base**: resolve merge-base in order against `origin/HEAD`, `origin/main`, `origin/master`, `main`, or `master` (`git merge-base HEAD <ref>`). In a single-branch repo with no distinct base, use the root commit (`git rev-list --max-parents=0 HEAD`) and include it in candidates. Print the chosen base and source in the plan for confirmation.
- List candidate target commits newest-first (`git log --oneline --no-decorate <base>..HEAD`). If `@{upstream}` exists, mark any candidate absent from `git rev-list @{upstream}..HEAD` as `[PUSHED]` in the plan and warn that amending it rewrites published history.
- Default exclusions (overrideable; list excluded paths in the plan as FYI): binaries (`- -` in numstat), `dist/`, `build/`, `*.png|jpg|pdf|zip`, and standalone lockfiles (`*.lock`, `package-lock.json`, `pnpm-lock.yaml`, `go.sum` — include only when paired with a manifest change).

## 2. Analysis — hunk-to-commit matching

```bash
git diff HEAD -U0 -- . ':!dist/*' ':!build/*' ':!*.lock' ':!package-lock.json' ':!pnpm-lock.yaml' ':!go.sum' ':!*.png' ':!*.jpg' ':!*.pdf' ':!*.zip'
```

Split changes into `-U0` hunks (`path:line-range @@ header`). A single file with unrelated hunks must be split if they belong to different target commits or if one hunk is unmatched. Match each hunk to candidate commits in `<base>..HEAD` in signal order:

1. **Line blame & log intersection**: check which commit in `<base>..HEAD` introduced or last touched the hunk's old-file line range (`@@ -<start>,<count> ... @@`):
   ```bash
   git log --oneline <base>..HEAD -L <start>,<end>:<path>
   ```
   (For pure insertions where `<count>` is `0`, inspect surrounding context lines `<start>-3,<start>+3`.)
2. **File & test/doc pairing**: `git log --oneline <base>..HEAD -- <path>`. Pair colocated tests and docs with their feature commit (`src/foo.ts` ↔ `src/foo.test.ts`, `docs/foo.md`).
3. **Symbol & scope match**: match `@@ ... @@ <symbol>` function/class names, imports, and commit scope/subject (`feat(auth)` vs `fix(db)`).

Classify each matched group into one action:

- **`fixup`** (`git commit --fixup=<sha>`): default when hunks fix a bug, typo, edge case, lint issue, or add/update tests inside the target commit's existing scope without changing its commit message contract.
- **`squash`** (`git commit --fixup=amend:<sha>`): when hunks expand the target commit's scope or contract enough that its commit message needs updating. Provide the replacement Conventional Commit message in the plan.
- **`fresh`** (unmatched hunks → new commit on top of `HEAD`): when hunks introduce an orthogonal change that does not belong to any commit in `<base>..HEAD`. Never force-fit unmatched hunks into an unrelated historical commit.

Format `fresh` and `squash` replacement messages as strict Conventional Commits v1.0.0 (`type(scope)!: subject` with `type ∈ {feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert}`, short repo-path `scope`, imperative `subject` ≤72 chars with no period, optional *why* body and `BREAKING CHANGE:` footer, and no plan metadata inside the fenced block).

## 3. Plan & Approval Gate

Order `fixup` / `squash` targets from **newest target commit (closest to `HEAD`) to oldest target commit (closest to `<base>`)** — matching the incremental autorebase execution order. Place any `fresh` commits after the fixup items.

````markdown
Branch: feat/oauth-login (range: a1b2c3d..HEAD, 3 candidate commits)
Base: a1b2c3d (source: user-provided | auto: merge-base with origin/HEAD — confirm)
Backups to create (both auto-removed after clean rebase, kept on conflict):
  - orig:   backup/fixup-feat-oauth-login-<ts>-orig
  - staged: backup/fixup-feat-oauth-login-<ts>-staged

1. [fixup] -> e4f5g6h fix(auth): handle token expiry [LOCAL]
   files: src/auth.ts:80-95 @@ refreshToken, src/auth.test.ts:45-68
   why: git log -L 80,95:src/auth.ts traces directly to e4f5g6h; adds missing 401 retry guard and unit test
   rebase step: GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash e4f5g6h~1

2. [fixup] -> b2c3d4e feat(auth): add OAuth callback [PUSHED — warn: rewrites upstream history]
   files: src/auth.ts:12-30 @@ handleCallback
   why: lines 12-30 were introduced in b2c3d4e; fixes state parameter validation in PKCE flow
   rebase step: GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash b2c3d4e~1

3. [fresh] -> new commit on top of HEAD
   files: config/mise.toml:4-8
   why: orthogonal tool version pin; no commit in a1b2c3d..HEAD touched mise.toml or build tooling
   message:
   ```
   chore(config): pin prek to 0.5
   ```

Related untracked (ignored, not staged): `src/authHelper.ts` looks related to 2. — run `git add <path>` and re-run if you want it included.
Excluded: `dist/app.js (binary)`.

Approve (yes / approve all / edits) to confirm the base/scope above, create backup branches, stage per-target hunks, run newest-to-oldest incremental autorebase, and auto-remove all backup branches after a clean rebase.
````

**Stop after outputting the plan.** Require explicit `yes` / `approve all` / per-item edits (confirming `Base:`) before creating backup branches or mutating. If the user reassigns a hunk, changes a `fresh` commit to a `fixup`, or overrides `<base>`, re-run the `<base>..HEAD` scope review and re-verify newest-to-oldest ordering before executing.

## 4. Execute — backups, partial staging, & incremental autorebase

### 4.1 Drift check & `-orig` backup

- Re-check `git diff HEAD | git hash-object --stdin` against the preflight hash; abort if the working tree drifted.
- Sanitize branch name (`SAFE_BRANCH="$(printf '%s' "$BRANCH" | tr '/' '-')"`) and timestamp (`TS="$(date +%Y%m%d-%H%M%S)"`):
  ```bash
  ORIG_BACKUP="backup/fixup-${SAFE_BRANCH}-${TS}-orig"
  STAGED_BACKUP="backup/fixup-${SAFE_BRANCH}-${TS}-staged"
  git branch "$ORIG_BACKUP" HEAD
  ```
- If the index has staged changes (`! git diff --cached --quiet`), record pre-staged new-file paths (`git status --porcelain` matching `^A`), reset the index with `git read-tree HEAD`, and run `git add -N -- <those paths>` so pre-staged new files remain tracked with an empty index blob (the only permitted `git add -N`).

### 4.2 Stage hunks & create `fixup!` / `amend!` / `fresh` commits on top of `HEAD`

Process planned items in order (all `fixup`/`squash` items first, then any `fresh` commits):

- **Whole-file changes** (every hunk of a tracked file, or a pre-staged new file after `git add -N`): stage directly with `git add -- <paths>` (or `git rm -- <paths>` for deletions).
- **Partial-file splits**: extract verbatim `-U0` hunks for item N from a fresh `git diff HEAD -U0 -- <file>` against current `HEAD` (regenerate before each commit because prior commits shift line offsets) and apply via stdin so no `.patch` files pollute the tree. (If splitting a brand-new `git add -N` file across multiple commits, run `git rm --cached -- <file>` before applying its first `new file mode` patch.)
  ```bash
  git apply --cached --unidiff-zero --recount <<'PATCH'
  ... verbatim -U0 hunks for item N ...
  PATCH
  git diff --cached -U0   # must match planned files and hunks exactly
  ```
- Commit according to the item's action:
  - **`fixup`**: `git commit --fixup="<target-sha>"`
  - **`squash`** (non-interactive message replacement via `amend:`):
    `git commit --fixup="amend:<target-sha>" -m "<approved replacement subject>" -m "<optional replacement body>"`
  - **`fresh`**:
    ```bash
    git commit -F - <<'EOF'
    <exact fenced Conventional Commit message>
    EOF
    ```
- On staged diff mismatch or hook failure, abort before rebasing, report state, and point the user to `$ORIG_BACKUP`.

### 4.3 Create `-staged` backup before rebasing

```bash
git branch "$STAGED_BACKUP" HEAD
```

If any explicitly excluded tracked files still have unstaged modifications, stash only those paths (`git stash push -m "git-fixup-excluded-${TS}" -- <excluded-paths>`) so `git status --porcelain` has no tracked dirty entries before rebase begins.

### 4.4 Newest-to-oldest incremental autorebase

Iterate over each unique `<target-sha>` from **newest (closest to original `HEAD`) to oldest (closest to `<base>`)** so every older target remains an unmodified ancestor keeping its exact SHA until its turn:

1. Rebase from `<target-sha>`'s parent (or `--root` if `<target-sha>` is the root commit):
   ```bash
   if git rev-parse --verify -q "${target_sha}~1" >/dev/null; then
     GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash "${target_sha}~1"
   else
     GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash --root
   fi
   ```
2. Verify the tree invariant immediately after each increment exits 0:
   ```bash
   git diff --quiet "$STAGED_BACKUP" HEAD
   ```
3. **On conflict or invariant mismatch**: run `git rebase --abort` (if a rebase directory exists), keep prior completed increments and both backup branches, report which `<target-sha>` conflicted, and print recovery options:
   - Inspect remaining `fixup!` commits: `git log --oneline <base>..HEAD`
   - Restore pre-rebase committed state: `git reset --hard "$STAGED_BACKUP"`
   - Restore original branch state: `git reset --hard "$ORIG_BACKUP"`

### 4.5 Cleanup backups & report

After all incremental rebase steps pass `git diff --quiet "$STAGED_BACKUP" HEAD`:

1. Delete both backup branches: `git branch -D "$STAGED_BACKUP" "$ORIG_BACKUP"`
2. If `git-fixup-excluded-${TS}` was stashed in 4.3, restore it with `git stash pop`.
3. Print `git log --oneline <base>..HEAD`, `git status --short`, and confirmation that `$ORIG_BACKUP` and `$STAGED_BACKUP` were removed.
