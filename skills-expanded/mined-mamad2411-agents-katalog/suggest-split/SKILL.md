---
name: suggest-split
description: "Splits a too-large pull request into smaller ones and gives you the commands."
---

# Suggest Split — Help an author divide a large PR into smaller ones

When invoked, take a pull request that's too large or too mixed to
review safely and produce a concrete split proposal — what each smaller
PR contains, what order to merge them in, and the git commands to make
each new branch. The skill is **read-only**: it suggests; the author
(or their developer) executes.

This skill is the natural follow-on to `/code-review` when PH-01 (Scope)
or PH-02 (Size) fires high. `/code-review` flags the problem; this
skill produces the actionable how-to.

---

## Input

| Parameter | Required | Description |
|---|---|---|
| `target` | Yes | PR number (`142`), branch ref (`feat/payments`), or commit range (`main..HEAD`) |
| `project-name` | No | Output folder under `.architecture/`. Defaults to working-directory basename |

**Example invocations:**

```
/sulis:suggest-split 142
/sulis:suggest-split feat/payments
/sulis:suggest-split main..HEAD
```

If the target is a PR number and `gh` is available, treat it as a
GitHub PR and pull metadata. Otherwise resolve from local git.

---

## Workflow

### 1. Resolve the diff

```bash
WORK="/tmp/suggest-split/{project}-$(date +%s)"
mkdir -p "$WORK"

if command -v gh >/dev/null && [[ "$TARGET" =~ ^[0-9]+$ ]]; then
  gh pr view "$TARGET" --json number,title,baseRefName,headRefName \
    > "$WORK/pr-meta.json"
  gh pr diff "$TARGET" > "$WORK/diff.patch"
  BASE=$(jq -r .baseRefName "$WORK/pr-meta.json")
  HEAD=$(jq -r .headRefName "$WORK/pr-meta.json")
fi

git diff --name-status "$BASE...$HEAD" > "$WORK/files.txt"
git log --format='%H %s' "$BASE..$HEAD" > "$WORK/commits.txt"
```

### 2. Categorise changes by file path

Read each changed file and put it into a category. Heuristics (apply
in order — first match wins):

| Pattern | Category |
|---|---|
| Path matches `migrations/`, `db/migrate/`, `prisma/migrations/`, `alembic/versions/` | **migration** |
| Path matches `*.sql`, `*.proto`, `*.graphql`, `*.avsc`, `openapi.*`, `swagger.json` | **schema** |
| Path matches `*.test.*`, `*_test.*`, `__tests__/`, `tests/`, `spec/` | **test** |
| Path matches `*.tf`, `*.tfvars`, `Dockerfile`, `docker-compose*`, `k8s/`, `helm/`, `.github/workflows/`, `.gitlab-ci*` | **infra** |
| Path matches `*.md`, `docs/`, `README*` | **docs** |
| Path matches package-lock files (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Cargo.lock`, `Gemfile.lock`, `poetry.lock`, `go.sum`) | **lockfile** |
| Commit message of any commit touching this file starts with `refactor:` or `chore:` | **refactor** |
| Everything else | **feature** |

A single file may fit two categories (e.g., a migration file with a
schema change inside). Use the most specific. Migration > schema > test
> infra > docs > lockfile > refactor > feature.

### 3. Group categories into a proposed split

Default split when the categorisation has variety:

| Order | Piece | Contents | Dependency |
|---|---|---|---|
| 1 | **Refactor** | All `refactor` files. Behaviour-preserving changes. | None — can merge first; should not change tests. |
| 2 | **Schema / Migration** | All `schema` and `migration` files plus immediately-adjacent code (e.g., new model classes) | Depends on Refactor merging first (so the schema is added against the latest structure) |
| 3 | **Infrastructure** | `infra` files | Depends on Schema (if the infra change supports the new schema) |
| 4 | **Feature** | All `feature` files plus the matching `test` files | Depends on Schema + Infrastructure |
| (n/a) | **Docs** | Bundled into the piece that introduces the documented behaviour. Avoid a docs-only PR unless the docs change is unrelated. |
| (n/a) | **Lockfiles** | Bundled into whichever piece introduces the dependency change that produced them. Don't split lockfiles into their own PR — they're regeneration, not a change. |

The split has **at most four pieces**. If the diff doesn't have enough
variety to produce four meaningful pieces, propose fewer (2 or 3).
Single-piece "the diff is already atomic" outputs are valid — emit a
short explanation and stop.

If the diff has more variety than four pieces (e.g., touches 8
independent subsystems), propose a two-pass split: recommend splitting
once now into broad pieces, then re-running `/sulis:suggest-split` on the
larger pieces.

### 4. Generate git commands per piece

For each piece, emit the exact git command sequence to create its
branch from `main` (or the agreed base) and stage just that piece's
files. Use **`git checkout -b`** + **`git checkout <head> -- <files>`**
pattern (cherry-pick-style without using cherry-pick — safer for
non-experts; doesn't rewrite history).

Example per-piece block:

```bash
# Piece 1 of 3 — Refactor
git checkout main
git pull
git checkout -b feat/payments-refactor

# Bring just the refactor files from the original branch
git checkout feat/payments -- \
  src/payments/client.ts \
  src/payments/types.ts \
  src/lib/http-client.ts

git add -A
git commit -m "refactor: extract HTTP client and payment types"
git push -u origin feat/payments-refactor

# Then: open a PR for feat/payments-refactor.
# Wait for it to merge before starting Piece 2.
```

Always:
- Include `git checkout main && git pull` to start from the freshest base
- Use clear branch names with `feat/`, `refactor/`, `chore/`, `infra/`
  prefixes per Conventional Commits style
- Group `git checkout <head> -- <files>` calls when the file list is
  long (use line continuations, not one command per file)
- Stop short of opening the PR — the author does that step

### 5. Write the suggestion artifact

Write to **the originating review bundle** if one exists (the `/code-review`
report directory for this PR), so the suggestion lives alongside the
review that flagged the split:

```
.architecture/{project}/code-reviews/PR-{number}-{TIMESTAMP}/
└── SPLIT-SUGGESTION.md
```

If no review bundle exists (the user ran `/sulis:suggest-split`
standalone), create a new bundle at the same path pattern with the
suggestion file and no REVIEW.md.

### 6. Summarise to the user (FE-01..FE-11 MUST — short)

Founder English. Plain language. The artifact does the work.

**Standard shape (3-4 sentences):**

> Looked at your pull request. It splits cleanly into {N} pieces — {one-line summary}. The proposed split and the exact git commands for each piece are at `.architecture/{project}/code-reviews/PR-{number}-{TIMESTAMP}/SPLIT-SUGGESTION.md`. Run them in order — merge Piece 1's pull request before starting Piece 2.

---

## SPLIT-SUGGESTION.md format

Two tiers, same convention as `/code-review`'s REVIEW.md.

### Tier 1 — For the author

```markdown
# Split suggestion for PR-{number}

> **Why split:** {1-2 sentences in plain English. Reference the
> hygiene findings from the originating /code-review if applicable.
> Acknowledge the work that's there before suggesting changes.}

## The split — {N} pieces

### Piece 1 — {name in plain English}

**What's in it:** {1-2 sentences in plain language. List the {N} files briefly.}

**Why this comes first:** {dependency explanation in plain English. "This is a behaviour-preserving change — nothing else depends on it, and it's the safest to merge first."}

**When this is merged:** Open the PR for Piece 1, get it merged into `main`, then start Piece 2.

### Piece 2 — {name}
...

## After all pieces are merged

The original branch `{HEAD}` can be deleted — its changes will all be
on `main` via the smaller PRs.

If you'd rather not do the split, that's fine — the original PR is
still merge-able with the changes the code review suggested. The split
is a recommendation, not a requirement.
```

### Tier 2 — Technical detail (the git commands)

```markdown
## Technical detail — commands to make each piece

> Run these commands in order. Each piece becomes a new branch off the
> latest `main`. Open one PR per branch. Merge in dependency order
> (Piece 1 first, then Piece 2, etc.).

### Piece 1 — Refactor

```bash
git checkout main && git pull
git checkout -b refactor/extract-http-client

git checkout {HEAD} -- \
  src/lib/http-client.ts \
  src/payments/types.ts

git add -A
git commit -m "refactor: extract HTTP client and payment types"
git push -u origin refactor/extract-http-client

# Open the PR: gh pr create --base main --head refactor/extract-http-client
# Wait for merge before starting Piece 2.
```

### Piece 2 — Database migrations
...

### Piece N — Feature
...

## File-to-piece mapping

{Full inventory of every changed file and which piece it belongs to.
This is the audit trail — if the founder asks "where does
src/foo/bar.ts go?" the answer is here.}

| File | Status | Piece |
|---|---|---|
| `src/lib/http-client.ts` | added | 1 (refactor) |
| `src/payments/types.ts` | modified | 1 (refactor) |
| `migrations/20260521-coupons.sql` | added | 2 (migration) |
| `src/coupons/handler.ts` | added | 3 (feature) |
| `src/coupons/handler.test.ts` | added | 3 (feature) |
| ... | ... | ... |

## Categorisation rationale

{Short notes on any non-obvious categorisation decisions. Example:
"`src/payments/client.ts` could have been refactor or feature. Placed
in refactor because the commit log shows two `refactor:` commits
touching it before any `feat:` commit."}
```

---

## Gotchas

- **Read-only by design.** This skill never executes git commands. It
  proposes them. The author copies, the author runs (or asks a dev to).
  Per "executing actions with care" in CLAUDE.md, history-changing
  operations need explicit author opt-in.
- **Avoid cherry-pick.** The `git checkout -b` + `git checkout <head> -- <files>`
  pattern is safer for non-experts than `git cherry-pick`. It doesn't
  rewrite history; it doesn't get confused by merge commits; and if it
  goes wrong, `git reset --hard` undoes it.
- **Lockfiles aren't a piece.** Don't propose a lockfile-only PR.
  Lockfiles regenerate from `package.json` / `requirements.txt` /
  etc. — they're a side-effect, not a change.
- **Docs follow the change.** Don't propose a docs-only PR unless the
  docs change is genuinely unrelated to the code. Same-PR docs are
  cheaper to review.
- **Single-piece output is fine.** If the diff is already atomic and
  small, say so. "Your PR is already shaped well — no split needed.
  Address the code-review findings in the same branch."
- **Founder English on the summary.** The chat output is for the
  founder, not for the engineer. Strip internal IDs. Use plain
  language. The artifact carries the detail.

---

## Composition

- **With `/code-review`** — natural follow-on. When PH-01 or PH-02
  fires high, `/code-review`'s Tier 1 report names this skill as the
  next step. The suggestion artifact lives inside the same review
  bundle.
- **With `/sulis:harden-codebase`** — independent. Harden implements deltas;
  split rearranges changes into PRs. They don't conflict.
- **With future `/sulis:apply-split` (deferred)** — a v0.2 version of
  this skill could optionally execute the proposed git commands after
  explicit author confirmation. Out of scope for v0.1. The artifact's
  Tier 2 commands are designed to be both human-readable and
  machine-executable so the future apply skill can reuse them.

---

## See Also

- [`../code-review/SKILL.md`](../code-review/SKILL.md) — flags the
  hygiene issues that motivate splitting
- `plugins/sulis/references/pr-hygiene-standard.md` — PH-01 Scope and
  PH-02 Size primitives this skill helps the author address
- [`../../references/hardening-deltas.md`](../../references/hardening-deltas.md)
  — file-layout context (this skill writes alongside review bundles)
