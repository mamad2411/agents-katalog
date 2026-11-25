---
name: code-review
description: Standard review of a code change — a diff, pull request, or the develop-phase branch — for correctness, security, integration/API and style, returning an approve/changes verdict and a review.md handoff. Use for a normal pre-merge review or the spine's review phase. For a deep, thorough, rigorous or adversarial review, or for reviewing docs or a design, use deep-review.
allowed-tools: Read, Grep, Glob, Bash, Task, Write
---

# Code review (phase workflow)

The review phase of the SDLC spine: review a code change across aspects and emit a single
verdict + a `review.md` handoff. It is the [multi-aspect review](../../patterns/multi-aspect-review.md)
pattern wired as a skill. Code is its target; **docs/design and deep adversarial audits go to
`deep-review`**.

## When to use

To review a code change — a diff, a PR, or the `develop` phase's output — before it merges, or
as the spine's review step. Not for reviewing docs/design (use `deep-review`), writing code
(`develop`), or designing (`architecture`).

## Process

> **Recall first** — pull the project's relevant prior decisions with its own search, else the
> knowledge vault (see [knowledge-recall](../../patterns/knowledge-recall.md)); factor them in, pass
> the top hits (path + one line why) in every `Task` prompt you send, and skip if nothing is found.

Follow [multi-aspect-review.md](../../patterns/multi-aspect-review.md):

1. **Scope** the change — `git diff` for the branch/PR, or the diff under review (when invoked
   by `develop`, the worktree diff is supplied to you) — and pick the aspects that apply. Detect
   the stack (`python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" stack-detect --repo <repo>`) so the lint aspect runs the right tools.
   **For a pull request, record its head first**: `gh pr view <n> --json headRefOid,baseRefName`
   gives `<sha>` and `<base>`. Then `git fetch origin <base> pull/<n>/head` and review
   `git diff origin/<base>...<sha>`: that commit, not the branch, which can move while you review.
2. **Fan out** one reviewer per aspect (independent, structured findings —
   `severity`, `location`, `issue`, `suggestion`, `evidence`; see
   [patterns/fan-out-fan-in.md](../../patterns/fan-out-fan-in.md)):
   - **correctness / reuse** → [`reviewer`](../../agents/reviewer.md) role;
   - **security** → [`security-engineer`](../../agents/security-engineer.md) role;
   - **integration + API** → `reviewer` (or the relevant stack engineer);
   - **style / lint / warnings** → run the detected stack's real tools yourself, in this session
     (the `stacks` profile's toolchain — ruff/mypy, eslint/tsc, go vet, … — preferring the repo's
     declared commands) and treat their output as evidence.
   - **concurrent-change conflicts** (ADR 0074) → whenever the diff **tightens a contract**: adds
     or changes a claim, lock, lease, dedup guard or status transition; adds a required
     input, parameter or field; makes a validation stricter; changes a signature, schema or return
     type; or removes a default. Look for that contract's **consumers**, not merely the same
     files. This session runs both parts (the `role_scope` hook keeps `gh`, worktrees and tests
     from the lens roles; a lens may do the `git grep`):
     (1) In the base, `git grep` the input, field, enum value or table/column name at
     `origin/<base>`. In open PRs, `gh pr list --state open --limit 21 --json number,headRefName,baseRefName`;
     keep those with the same `baseRefName`, skip the PR under review, then `gh pr diff <n>` each
     and grep the same names. Twenty is the bound: when a 21st comes back, say that more PRs were
     open than were searched.
     (2) After `git fetch origin <base> pull/<n>/head`, `git merge-base --is-ancestor origin/<base> <sha>`
     exiting 1 means the base moved since the head was cut, so its CI did not see the current
     base. Then review a head that contains the current base, or run the affected tests on a
     trial merge: `git worktree add --detach <dir> <sha>`, `git merge --no-commit --no-ff origin/<base>`
     there, run them, `git merge --abort`, `git worktree remove <dir>`.
     *No textual conflict ≠ no semantic conflict*: two guards on one precondition are usually
     mutually exclusive, and a PR adding a caller that lacks a newly required input is green
     against the base it ran on; each merges cleanly and passes its own CI. A check that is not
     required going red after the merge shows the PR as UNSTABLE, which does not block a merge. A
     consumer that breaks is a finding on this diff. For a state transition, reconcile to one guard
     point before either lands, and prefer claiming atomically **at the point of work**.
3. **Verify** each finding against the source (open the file, re-run the tool) — drop or
   downgrade what doesn't hold. Re-running a tool is this session's job: the lens roles are held
   to reading by the `role_scope` hook, so a lens verifies with `git show <base>:<path>`,
   `git log` and `git blame`, and you run the tests and linters. When the question is *"what did
   the original do?"* — a migration, a refactor, a faithful port — **read the original**:
   `git show <base>:<path>`. Do this before sending any corrective that would change behaviour. Memory of an earlier partial read is not
   ground truth, and neither is the pre-image of a truncated diff hunk.
4. **Synthesize one verdict.** Aggregate across aspects: **any `blocker`/`major` → `changes`**,
   else `approve`; dedupe, and on a severity conflict keep the highest.
5. **Write the handoff.** Emit `review.md` (`type, target, iteration, verdict, findings[]` —
   see [patterns/handoff.md](../../patterns/handoff.md)); validate it by reading it back.
   Then **read the file back** — `python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" handoff-load --path <path> --type review` — and fix whatever it reports: this reads the file, so it sees the YAML you typed, and a single
   malformed value (a flow sequence with prose after it, an unquoted `:`) leaves an artifact the
   next phase cannot read (ADR 0096).
   **For a pull request**, post the review on GitHub instead of writing `review.md` (which stays
   the output for a local diff and the spine). Never hand-build a `gh api .../reviews` call. Write
   the findings as JSON to a file (an array, or `{"verdict", "summary", "findings"}`), then:

   ```bash
   python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" pr-review --repo . --pr <n> --head <sha> --findings-json <file> --out <payload-file> --event request-changes
   ```

   `<sha>` is the head recorded in step 1, never a fresh lookup: a fresh one would pin the
   review to a commit nobody reviewed. `<payload-file>` is a `.json` file under the temp
   directory, or under the repository outside any hidden directory (`.git`, `.github`, ...);
   anywhere else, or through a linked directory, is refused. It re-reads the PR and
   refuses (exit 1) when the head is no longer `<sha>`, the PR is closed or merged, or `gh` fails:
   then review the new head, do not post. It pins `commit_id` to `<sha>`, puts a finding inline
   only when its `file:line` is an added or context line of the diff (else in the body, saying
   why), neutralises every `@mention`, and caps sizes. Run its `post.shell`, decoded from JSON,
   straight away. An `approve` verdict posts as a COMMENT, since an APPROVE counts toward branch
   protection's required reviews: pass `--event approve` only when the user asked for an
   approval. `--event comment` posts any verdict as a comment.
6. **In the develop loop:** a `changes` verdict loops back to implementation (bounded — see
   [patterns/review-loop.md](../../patterns/review-loop.md)); `approve` proceeds.

## Output

A `review.md` handoff: an `approve`/`changes` verdict plus aspect-organized findings; for a pull
request, the same review posted on GitHub through `af.py pr-review`. Read-only on the code under
review — it critiques, it does not edit.

## Definition of done

- One explicit verdict, aggregating all aspects (any blocker/major ⇒ changes).
- Every finding carries severity, location, and a concrete fix; findings verified, not guessed.
- `review.md` validates against the review handoff schema, or, for a PR, the review was built
  by `af.py pr-review` for the head that was reviewed and posted with its printed command. No
  code modified.
