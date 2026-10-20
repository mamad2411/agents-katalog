---
name: cmd-commit
description: Command — Create git commits for all uncommitted changes and land them on the project's mainline, matching the repo's existing commit style
---

# /commit

Create well-structured git commits for all uncommitted changes in the current repository. **Match the repo's existing commit style exactly** — never introduce a new convention.

## Requirements

- **Commit everything**: "all uncommitted changes" means ALL — every modified, staged, and untracked path in `git status`. Never leave a file out, **and never pause to ask whether to commit one**, because you judge it incidental, "not part of my change," **a separate feature, or code you didn't write** — none of those is a reason to skip _or to ask_. If it doesn't belong with the main commit, give it its own commit. Invoking `/commit` IS the authorization to commit everything; there is no further confirmation step. The only files whose contents you keep out of a commit are (a) genuine secrets/credentials, (b) files the user explicitly named, or (c) **generated artifacts** — reproducible scratch/output with no review value, which you _gitignore_ rather than commit (see _Artifact triage_). Say which you skipped or ignored, and why. Done = a clean working tree.
- **File-based commits**: commit whole files only, never partial files or line hunks
- **Gradual commits**: limit each commit to **20–25 files maximum**. Split larger changesets into multiple focused commits. Improves reviewability, makes `git bisect` effective, keeps history readable.
- **Land on the project's mainline, never push**: commit locally on the current branch, then land the work where the project keeps it (see _Step 4_). **Never create a branch on your own initiative** — a branch you're only on because of the harness "branch first" default is _not_ the project's workflow; its commits get landed on the mainline and the branch deleted. **Never push** — the user pushes.
- **No `git -C`**: operate from the repo's working directory
- **Enumerate paths, don't bulk-add**: stage with explicit `git add <path> …`, never `git add -A` / `git add .`. This is a safety mechanism so a stray credential file can't be swept in silently — **not** license to leave files out. Every uncommitted change still gets committed (see _Commit everything_ above).
- **No amend**: create new commits; only amend if the user explicitly asks
- **Co-author**: match existing style. Include a `Co-Authored-By` line only if recent commits include one. Do not introduce it on a solo project that has never used it.

## Mode detection (do this first)

Before any other action, check for plan mode:

- System instructions include "Plan mode is active"
- An active plan file path exists (e.g., `~/.claude/plans/<name>.md`)

### If plan mode IS active → plan the commits

> Read-only git commands (`git status`, `git diff`, `git log`) are permitted in plan mode. Write operations (`add`, `commit`, `push`) are blocked.

1. Gather:
   - `git status` — see uncommitted changes
   - `git diff` — understand what changed
   - `git log -5 | cat` — match existing commit style
2. Extract style dimensions from `git log` (see Step 1 below).
3. Run _Artifact triage_ (read-only here): note which paths are generated artifacts to be **gitignored** vs authored files to commit. Then group the authored files logically — every authored file lands in some commit; grouping distributes them, it never drops any. (`.gitignore` edits and `git rm --cached` are writes — describe them in the plan, don't run them.)
4. The Commit Plan must be the content of the plan file you present — `ExitPlanMode` presents the harness's plan file, `PresentPlan` the file you name — because the plan review covers only that file. If it holds a plan whose work is implemented — committed, or about to be committed by this run — replace it with the Commit Plan. Only if it holds a plan whose work is not yet implemented (still in progress or not yet approved), stop and ask the user: "The plan file still holds an unfinished plan — replace it with the commit plan, or keep it and commit outside plan mode?"

   Commit Plan template:

```
## Commit Plan

### Artifacts to gitignore (if any)

- `<pattern>` — <why it's generated scratch, not source>

### Commit 1: <short summary>
**Files:**
- path/to/file1
- path/to/file2

**Message:**
~~~
<draft message using extracted style — do NOT use placeholder text>
~~~

### Commit 2: <short summary>
...
```

5. Note the planned **landing** (Step 4). Checkout/merge/branch-delete are write ops, blocked in plan mode — describe, don't run (the Step 4 heuristic reads — `@{upstream}`, file-existence checks — are read-only and permitted; only the checkout/merge/branch -d writes are blocked):
   - On the default branch → commits stay on it; nothing to land.
   - On a side branch with a feature/PR workflow → `leave on <cur>` for you to push/PR.
   - On any other side branch → `will merge <cur> into <default> and delete <cur>` (no push).
6. Inform the user:
   - Commits planned: N
   - Files staged: M
   - Where the work will land (per the line above)
   - When auto-review's plan gate (`planGate: true` in `bb auto-review status --json`) or the agent-hooks plan-review hook (installed) is active, the commit plan goes through the calibrated plan review before it reaches you; that review checks grouping, file coverage, artifact and secret triage, and message style, so what you see has already been revised.
   - Review the plan; after exiting plan mode, run `/commit` again to execute.

### If plan mode is NOT active → execute commits

Proceed to Step 1.

## Step 1: Extract commit style (REQUIRED)

```bash
git log -5 | cat
```

Extract from the output:

- **Verb form**: imperative ("Add"), imperative-with-s ("Adds"), past tense ("Added"), or prefix ("feat:")
- **Subject length**: typical chars; some repos run shorter
- **Subject capitalization**: sentence case, all-lowercase, or mixed
- **Body format**: prose paragraphs, bullet points, or no body at all
- **Body width**: ~72 or ~80 chars
- **Co-author line**: exact format used, or absent
- **Footers**: `Refs:`, `Closes:`, `BREAKING CHANGE:` — only if the repo uses them

You MUST use the extracted style. Do not invent. Do not copy an example from this command or from `Skill(commit-writer)` — those are illustrative, not prescriptive.

**Judge by specificity, and look past noise.** Housekeeping commits — version bumps ("Bump version to 1.2.0"), merge commits, squashed-history commits — are workflow artifacts, not style signals; ignore them when reading the log. A subject that is a **bare generic placeholder** — a context-free token naming nothing specific, such as `init`, `Initial commit`, `wip`, `update`, `stuff` standing alone, or a lone verb (`add` / `create` / `delete`) with no object — is not a style either. There is a real style to match as long as the sample holds **any** specific subject ("Add rate limiting", "Fix off-by-one in pagination cursor"): learn from those, ignore the noise. If the recent five are all housekeeping or bare placeholders, widen the sample with `git log -20 | cat` (full format, so body shape survives) before concluding there is no style. Only when nothing specific remains do you go to Step 2.

For deeper guidance on writing the message body itself, invoke `Skill(commit-writer)`.

## Step 2: Fallback — empty repo, or no specific style to learn from

Use the sensible default when EITHER the repo has zero commits (`git log` returns nothing) OR — after ignoring housekeeping and widening per Step 1 — every sampled subject is a **bare generic placeholder**: a context-free token naming nothing specific, such as `init`, `Initial commit`, `wip`, `update`, `stuff`, `changes` standing alone, or a lone verb (`add` / `create` / `delete`) with no object. The typical case is a fresh repo whose only commits are placeholders like `init` or `wip`. The list is illustrative, not exhaustive — the test is whether the subject names something specific ("Add rate limiting" and "Update OTel to v1.30" do; bare `add` or `update` does not).

A single vague commit is not a style; mimicking it just yields more one-word commits (`create`, `add`, `delete`). Default to: imperative-with-s subject ("Adds X"), prose body explaining what + why. Do **not** copy the placeholder's genericity, and do **not** introduce conventional commits (`feat:`, `fix:`) as a default — that is a project-wide editorial decision, not a sensible default.

Boundary: a short, no-body subject that is _specific_ ("Fix off-by-one in pagination cursor", "Remove the deprecated auth flag") is a real style — match it. Only bare, context-free subjects are disqualified.

## Artifact triage (before staging)

Before staging anything, look at each uncommitted path and judge it by its **nature, not its relevance to your change**:

- **Authored** — code, config, docs, fixtures, lockfiles, checked-in generated source/migrations, anything a human wrote or that the repo already tracks as a source of truth → **commit it.** Always. Even if it's unrelated to your change, a separate feature, or written by someone else. Relevance is _never_ a reason to skip (see _Restrictions_).
- **Generated artifact** — machine-produced, reproducible scratch/output with **no review value** _and_ not already tracked by the repo as a source of truth: the kind of thing a `.gitignore` exists to exclude. Judge case-by-case — there is **no fixed list** — but typical shapes are browser snapshots like `.playwright-cli/`, Playwright traces/screenshots, coverage reports, `node_modules/`, `*.log` debug logs, `.DS_Store`, `__pycache__/`, and **uncommitted** `dist/` / `build/` output. → **gitignore it; do not commit its contents.**

**The bright line:** ask "_was this generated_?" — never "_is this part of my change_?". The falsification test: **if you find yourself reasoning about whether the file's _content_ is useful to your change, you're testing relevance, not nature — commit it.** A file being unrelated, incidental, or not-yours makes it none of these — it gets committed. **When you are genuinely unsure of a file's nature, commit it** — the safe default never skips authored source.

> **Generated ≠ artifact.** A lockfile, a `*.pb.go`, a checked-in migration, a generated `schema.sql`, a `dist/` the repo intentionally tracks — all machine-produced, yet they carry review value or are the repo's source of truth → **commit them.** The artifact test is "reproducible scratch with no review value that the repo does not already track." If git already tracks a path as committed source, treat it as authored unless it is plainly stale scratch.

### Handling an artifact

For each path you classify as an artifact:

1. **Secrets first.** Scan its contents for credentials (the same patterns `Skill(commit-writer)` uses, run directly against the file). If it matches, **do NOT gitignore it** — escalate to the secrets stop (permitted stop #2): tell the user a credential is in `<path>` and let them scrub/rotate. Silently ignoring a token-bearing log would hide a leak. A clean artifact continues below.
2. **Pick the narrowest correct ignore pattern.** Default to the exact path or a scoped glob (`.playwright-cli/*.yml`). Use a whole-directory pattern (`.playwright-cli/`) **only after confirming the directory holds no authored files** (`git status --porcelain <dir>`); a directory mixing scratch with a real `config.ts` gets a file-glob, never the bare dir. **Never an extension-only glob** (`*.yml`, `*.json`) — it silently hides real config; before adding any glob, check what it already matches in the tree.
3. **Append to `.gitignore`** — repo root, or the nearest package-level `.gitignore` in a monorepo; create it if absent. First `grep -qxF '<pattern>' .gitignore` and **skip the append if the pattern is already present.**
4. **Untracked artifact** → the pattern alone drops it from `git status`. **Already-tracked artifact** (it landed in history on a prior run, possibly now modified) → `git rm --cached <path>` so the ignore takes effect — the file stays on disk, staged as a deletion.
5. **Verify before committing:** run `git status` and confirm the artifact path is gone (not still modified/staged). A typo'd pattern that leaves it visible must **not** pass as a clean tree — fix the pattern.
6. **Commit** the `.gitignore` edit (plus any `git rm --cached` removals) as its own housekeeping commit, **in the repo's extracted style** (Step 1) — the subject `Ignore <thing> scratch artifacts` is illustrative, not prescriptive.
7. **Report** each gitignored/untracked path on its own line — `Gitignored <path> — <why it's scratch>` — so the user always sees what was reclassified, exactly as visible as a skipped-secret report.

If triage leaves **no authored files** (everything was an artifact), the housekeeping commit is the entire result — say so; do not report "nothing to commit." If every pattern was already present (no `.gitignore` change needed), say that too.

This is the **third and only other** permitted reason not to commit a file's contents, alongside (a) secrets/credentials and (b) user-named files. It adds no new _stop_ — you act on it autonomously; the lone exception is the secret-in-artifact escalation in step 1, which is just stop #2.

## Step 3: Execute

1. `git status` — see all uncommitted changes. **If the working tree is clean** (no untracked, no modified, no staged), STOP and tell the user "Nothing to commit, working tree clean." Do NOT proceed; do NOT invent files to stage; do NOT create an empty commit.
2. `git diff` — understand what changed
3. **Artifact triage** (see _Artifact triage_ above) — for each untracked or changed path, decide _authored_ vs _generated artifact_, and for every artifact run the full _Handling an artifact_ procedure (steps 1–7: secrets-check, narrowest pattern, dedup, `git rm --cached` if already tracked, verify, housekeeping commit, report). Everything authored continues below.
4. Group related files logically per commit (20–25 file cap) — this distributes ALL **authored** uncommitted files across commits; it never excludes authored source.
5. `git add <specific-files>` (never `-A` or `.`)
6. Create the commit using HEREDOC format for proper message formatting:

```bash
git commit -m "$(cat <<'EOF'
<subject>

<body>
EOF
)"
```

7. Repeat for remaining changes
8. Final `git status` — the tree MUST be clean. Anything still uncommitted is a bug unless it is an allowed exclusion (secret/credential, user-named, or a gitignored artifact); name any skipped or ignored file and the reason. "Done" means a clean tree, not "the files I judged relevant are committed."

## Step 4: Land the work on the project's mainline

Once Step 3 leaves a clean tree, get the commits where the project keeps them — don't strand
them on a side branch. **Never push** at any point; the user pushes. To choose the integration
strategy interactively (merge / PR / keep / discard) instead, use `/ship`; Step 4 is the
fire-and-forget path.

```bash
# Resolve the project's mainline — don't hardcode "master"; strip any remote prefix
default=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^[^/]*/##')
[ -z "$default" ] && { git show-ref -q --verify refs/heads/main && default=main || default=master; }
cur=$(git branch --show-current)
```

- **Detached HEAD** (`cur` is empty) → **STOP.** The commits are on a detached HEAD, not a branch;
  landing would orphan them. Tell the user: `HEAD is detached — commits are on the detached HEAD. Reattach ('git switch -c <name>' or 'git switch <branch>') before /commit again.`
- **Already on `$default`** (`cur` = `default`) → the commits are already on the mainline. Done.
- **On a side branch** (`cur` ≠ `default`) → decide: the project's workflow, or a fake branch?
  - **Feature / PR project → leave it.** Keep the commits on `cur`; do **not** merge or delete.
    Report: `Committed on '<cur>'. Project uses a feature/PR workflow — left for you to push/PR.`
    Treat the project as feature/PR if **any** of these hold (all cheap, no network):
    - the branch name looks like a feature branch — matches
      `^(feat|feature|fix|bugfix|hotfix|chore|release)/`;
    - the branch tracks a remote upstream — `git rev-parse --abbrev-ref @{upstream}` succeeds
      (a real, shared branch, not a throwaway);
    - PR infrastructure exists — `.github/PULL_REQUEST_TEMPLATE*`, a PR-gating
      `merge.sh` / `.githooks/pre-push`, or a `pr-validate*` workflow;
    - the project's `CLAUDE.md` documents a branch/PR workflow.
  - **Otherwise → land it on the mainline** (master-workflow project, or a fake harness
    branch — both want the commits on `$default`):
    ```bash
    # the mainline must exist locally before we can land on it
    git show-ref -q --verify "refs/heads/$default" && git checkout "$default"
    git merge "$cur"        # PLAIN merge — never --ff-only, never --squash, never rebase
    git branch -d "$cur"    # delete the merged side branch — don't leave it dangling
    ```
    Report: `Landed '<cur>' on '<default>' and deleted the branch. Not pushed.`
    - **If `$default` doesn't exist locally or `git checkout "$default"` fails** (real mainline
      is `trunk`/`develop`, or `origin/HEAD` is unset) → **STOP, do not merge.**
      Report: `Couldn't check out the mainline '<default>' — landing skipped; commits are safe on '<cur>'. Set origin/HEAD or land manually.`
    - **If `git branch -d "$cur"` refuses** (`not fully merged`) → **don't force.** The merge
      already succeeded, so the commits are safe on `$default`; report the error verbatim and
      tell the user to inspect, then `git branch -D "$cur"` manually if that's what they want.

**Conflict safety:** if `git merge` reports conflicts, **STOP** — leave the merge in progress,
tell the user exactly which files conflict, and add: `You are now on '<default>' with a merge in progress — resolve and 'git commit', or 'git merge --abort' to cancel.` Never auto-resolve, never
silently `git merge --abort`, never force.

## Restrictions

- In plan mode: only read-only git commands; write the plan to the plan file. The Step 4 landing (checkout / merge / branch -d) is a write op — describe it, never run it.
- NEVER `git -C` (operate from the repo's working directory)
- NEVER `git add -A` or `git add .` — always specify files
- NEVER `git push` — landing the work is a **local** merge; the user pushes
- NEVER create a branch on your own initiative — commit on the current branch and land per Step 4
- When landing on the mainline, use a PLAIN `git merge` — NEVER `--ff-only`, `--squash`, or rebase
- NEVER merge a feature/PR-workflow branch into the mainline or delete it — leave it for the user to push/PR (see Step 4)
- NEVER `git commit --amend` unless explicitly requested
- NEVER skip hooks (`--no-verify`) unless explicitly requested
- NEVER invent a commit style — match the repo's existing one
- NEVER leave a changed file uncommitted because you deemed it "unintended" or "unrelated" — commit it (its own commit if needed). The only contents you keep out of a commit are genuine secrets/credentials, user-named files, or **generated artifacts** (which you _gitignore_ instead — see _Artifact triage_); say so in each case.
- NEVER pause to ask the user whether to commit a file, and NEVER treat committing something as an "editorial call." The permitted stops are exactly two: (1) a clean working tree, (2) a detected secret/credential. **Every other reason to stop or ask is invalid** — "I didn't write it," "it's a separate feature," "it looks unrelated" all mean _commit it in its own commit_, not _ask first_. The one judgment you _do_ make silently is **nature, not relevance**: a generated, no-review-value artifact gets gitignored (no asking), everything authored gets committed (no asking), and when you're unsure which, you commit.

## Arguments

`[optional message hint]`
