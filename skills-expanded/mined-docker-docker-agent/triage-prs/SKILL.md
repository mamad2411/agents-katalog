---
name: triage-prs
description: Triage open pull requests on docker/docker-agent — apply area/* and kind/* labels, flag merge conflicts (draft + status/needs-rebase + author comment), clear the needs-rebase label once conflicts are resolved, flag unsigned commits (status/needs-signed-commits + author comment), and clear that flag once all commits are verified. Idempotent and API-frugal; designed to run on a recurring schedule.
---

# Triage Pull Requests

Triage open pull requests on the `docker/docker-agent` repository: classify them
with `area/*` and `kind/*` labels, flag those with merge conflicts, clear the
conflict flag once it is resolved, flag PRs with unsigned commits, and clear that
flag once every commit is verified.

This skill is designed to run **unattended on a recurring schedule** (every ~30
minutes). It is written to be **agent-agnostic** — use whatever GitHub access you
have (CLI, REST, GraphQL, an MCP server). Two properties matter more than the
mechanism and must hold no matter how you talk to GitHub:

1. **Idempotency is critical.** The skill runs repeatedly. A given PR must never be
   re-drafted, re-labeled, or re-commented if it is already in the desired state.
   Re-running over the same PRs must produce **zero** changes and, ideally, zero
   write calls.
2. **Minimize GitHub API calls.** Read once, decide everything in memory, then make
   the smallest possible number of writes — see [API budget](#api-budget).

## Scope

Process **open** pull requests (including author-created **drafts**) whose **last
update was within the past 60 minutes**.

Out of scope — skip entirely:
- Closed and merged PRs.
- PRs untouched in the last 60 minutes.

The 60-minute window against the ~30-minute cadence intentionally gives every PR
**two** chances to be processed, so a single missed or failed run is harmless.

> ⚠️ **Never trust GitHub's search index for decisions.** `is:pr label:…` search
> filters (and the `gh --label` / `search/issues` APIs that back them) are **stale**:
> they return PRs that no longer carry a label and miss PRs that do. Before acting on
> any PR, read that PR's **live, per-item** fields (labels, draft state, mergeable
> state). Use search only as a coarse pre-filter, never as the source of truth for a
> mutation.

## API budget

1. **One read pass.** Fetch the in-scope candidate set in a single batched query
   (GraphQL is ideal). For each PR retrieve everything all five rules need at once:
   - `updatedAt`, `isDraft`, and `mergeable` state
     (`MERGEABLE` / `CONFLICTING` / `UNKNOWN`)
   - the current set of labels (live)
   - `title`, `body`, and **linked issues** via `closingIssuesReferences`, including
     each linked issue's labels and native **issue type**
   - the changed files / paths (to infer `area/*`)
   - per-commit signature verification data:
     `commits(last: 100) { nodes { commit { oid signature { isValid } } } }`
     (`signature` is `null` for unsigned commits; `isValid` is `false` for commits
     signed with an unrecognised or invalid key)
   - whether a previous run already posted the conflict comment **and** whether a
     previous run already posted the unsigned-commits comment (two separate bot-comment
     checks — one gate per rule)
2. **Decide fully in memory.** For each PR, compute the complete set of mutations
   for all five rules before issuing any write.
3. **One grouped label mutation per PR.** Fold every label change for a PR — adding
   `area/*`, adding `kind/*`, adding *or* removing `status/needs-rebase`, and adding
   *or* removing `status/needs-signed-commits` — into a **single** label update call.
   Never issue one call per label.
4. **No-op means no call.** If a PR needs no change, make zero write calls for it.
5. **`UNKNOWN` mergeable → do nothing this run.** GitHub computes mergeability
   asynchronously. If the state is `UNKNOWN`, skip the conflict rules for that PR;
   it will be re-evaluated next run once GitHub finishes. (You may still apply
   Rule 1 labels and Rule 4/5 signed-commit checks, which do not depend on
   mergeability.)

## Label taxonomy

Use **only labels that already exist in the repository.** Never invent a label. If
the appropriate label does not exist or the correct value is genuinely ambiguous,
leave that dimension alone (optionally apply `status/needs-triage`) rather than
guessing.

### `kind/*` — the change type (exactly one on a PR)

- `kind/feat` — adds a new feature (Conventional-Commit `feat:`).
- `kind/fix` — fixes a bug (Conventional-Commit `fix:`).
- `kind/docs` — documentation-only change.
- `kind/chore` — maintenance, deps, CI, tooling (`chore:`).
- `kind/refactor` — refactor with no behavior change (`refactor:`).
- `kind/test` — test-only change (`test:`).
- `kind/security` — security fix or hardening.

> **`kind/feat` and `kind/fix` are the canonical labels** — they map to the repo's
> `feat:` / `fix:` commit convention. The older `kind/feature` and `kind/bug` labels
> have been **deleted**; never apply them.
>
> **`kind/*` is for pull requests only.** Issues use GitHub's native **issue type**
> field (`Task`, `Bug`, `Enhancement`, `Epic`, `Initiative`) and must never carry a
> `kind/*` label. When a linked issue informs a PR's kind (see Rule 1), read its
> native issue type, not a `kind/*` label.

### `area/*` — the part of the codebase touched (one or more on a PR)

Infer from the changed paths. Valid values (do not invent others):

`area/a2a`, `area/agent`, `area/api`, `area/ci`, `area/cli`, `area/config`,
`area/core`, `area/deps`, `area/distribution`, `area/docs`, `area/gateway`,
`area/mcp`, `area/models`, `area/providers`, `area/providers/anthropic`,
`area/providers/bedrock`, `area/providers/docker-model-runner`,
`area/providers/gemini`, `area/providers/openai`, `area/rag`, `area/registry`,
`area/runtime`, `area/security`, `area/sessions`, `area/skills`, `area/telemetry`,
`area/testing`, `area/tools`, `area/tui`.

> For Docker Model Runner work, use `area/providers/docker-model-runner`. The legacy
> top-level `area/docker-model-runner` has been **deleted**; never apply it.

Path-hint examples: `pkg/config/**` → `area/config`; TUI code → `area/tui`;
`.github/workflows/**` → `area/ci`; MCP server/tooling → `area/mcp` or `area/tools`;
provider integrations → the matching `area/providers/*`; docs/markdown → `area/docs`.

### `status/*`

- `status/needs-rebase` — the PR has merge conflicts / is out of date with the base
  branch. Applied and removed by this skill (Rules 2 and 3).
- `status/needs-signed-commits` — the PR contains one or more commits that are not
  signed and verified by GitHub. Applied and removed by this skill (Rules 4 and 5).
- `status/needs-triage` — optional fallback when a PR's `kind/*` or `area/*` cannot
  be determined with confidence.

## Rule 1 — Apply `area/*` and `kind/*`

**Trigger:** an in-scope PR missing an `area/*` label and/or a `kind/*` label.

**Skip if:** the PR already has at least one `area/*` *and* one `kind/*` label
(consider it triaged for those dimensions).

**Action — add only the missing dimension:**

- **`kind/*`** (a PR should have exactly one), inferred in this priority order:
  1. If the PR closes/links an issue, use that **issue's native issue type** to guide
     the kind: `Bug` → `kind/fix`; `Enhancement` → `kind/feat`. (Use the PR's own
     signals below to refine, e.g. a docs-only PR closing an Enhancement is still
     `kind/docs`.)
  2. Otherwise infer from the **Conventional-Commit prefix** in the PR title
     (`feat:` → `kind/feat`, `fix:` → `kind/fix`, `docs:` → `kind/docs`,
     `chore:` → `kind/chore`, `refactor:` → `kind/refactor`, `test:` → `kind/test`),
     and from the PR title/body intent.
- **`area/*`** — infer one or more from the files/paths the PR changes.

**Guard rails:**
- Add only the **missing** dimension. Never remove or overwrite an `area/*` or
  `kind/*` label that a human already set.
- Use only existing repository labels (see [taxonomy](#label-taxonomy)); never invent
  one.
- If `kind/*` or `area/*` is genuinely ambiguous, leave that dimension unset
  (optionally add `status/needs-triage`) rather than guessing.
- Fold these label additions into the PR's single grouped label mutation, together
  with any `status/needs-rebase` or `status/needs-signed-commits` change from
  Rules 2–5.

## Rule 2 — Flag merge conflicts

**Trigger:** an in-scope PR whose live mergeable state is `CONFLICTING`.

**Idempotency gate (critical):** if the PR **already** has `status/needs-rebase`, do
**nothing** for this rule — do not re-draft, do not post another comment.

**Action (first time only):**

1. Convert the PR to **draft** — *skip this step if the PR is already a draft*
   (the `isDraft` field from the read pass tells you; converting an already-draft PR
   is a no-op write and violates the "no-op means no call" budget rule).
2. Add `status/needs-rebase` (in the same grouped label mutation as any Rule 1 labels).
3. Post **one** comment addressed to the author, for example:

   > 👋 This PR has merge conflicts with the base branch. Please rebase or merge the
   > latest base branch and resolve them. I've moved it to draft and added
   > `status/needs-rebase`; it'll be picked back up automatically once the conflicts
   > are cleared.

Because the label, the draft conversion, and the comment are always applied together,
the presence of `status/needs-rebase` is a reliable signal that the comment was
already posted — use it as the gate to avoid duplicate comments.

## Rule 3 — Clear resolved conflicts

**Trigger:** a PR that currently has `status/needs-rebase` whose live mergeable state
is now `MERGEABLE`.

**Action:** remove `status/needs-rebase` (fold into the PR's single grouped label
mutation).

**Do not:**
- trigger on `UNKNOWN` mergeable state — only `MERGEABLE` clears the label. If the
  state is `UNKNOWN`, leave `status/needs-rebase` in place and re-evaluate next run
  (see the [API budget](#api-budget) `UNKNOWN` rule); never treat `UNKNOWN` as resolved,
- mark the PR ready for review (leave the draft/ready state to the author), and
- post any comment.

## Rule 4 — Flag unsigned commits

**Trigger:** an in-scope PR where at least one commit has `signature.isValid ≠ true`
(either unsigned — `signature` is `null` — or signed with an unrecognised or invalid
key).

**Idempotency gate (critical):** if the PR **already** has
`status/needs-signed-commits`, do **nothing** for this rule — do not post another
comment.

**Action (first time only):**

1. Add `status/needs-signed-commits` (fold into the same grouped label mutation as any
   Rule 1 / Rule 2 changes).
2. Post **one** comment addressed to the author that:
   - lists the short SHAs (7 chars) of the non-verified commits,
   - explains what "signed and verified by GitHub" means (GPG or SSH key registered in
     their GitHub account),
   - links to <https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits>,
   - notes that the label will be removed automatically once all commits carry a valid
     GitHub-verified signature.

   Example comment:

   > 👋 Some commits in this PR are not signed and verified by GitHub. Please sign your
   > commits with a GPG or SSH key registered in your GitHub account, then force-push.
   >
   > Commits that are not verified: `abc1234`, `def5678`
   >
   > See [GitHub's guide on signing commits](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits)
   > for setup instructions. I've added `status/needs-signed-commits`; it will be
   > removed automatically once every commit in this PR carries a valid
   > GitHub-verified signature.

Because the label and the comment are always applied together, the presence of
`status/needs-signed-commits` is a reliable gate — use it to avoid duplicate comments.

## Rule 5 — Clear resolved signed-commits flag

**Trigger:** a PR that currently has `status/needs-signed-commits` whose commits now
**all** have `signature.isValid == true`.

**Action:** remove `status/needs-signed-commits` (fold into the PR's single grouped
label mutation).

**Do not:**
- post any comment,
- change draft/ready state.

## Execution summary

For each in-scope PR, in one read-then-write cycle:

1. Read its **live** fields (labels, `isDraft`, `mergeable`, linked-issue types,
   changed paths, prior bot comments — one check for the conflict comment, one for the
   unsigned-commits comment — and per-commit signature verification data).
2. Compute the combined set of changes from Rules 1–5 in memory:
   - missing `kind/*` / `area/*` to add (Rule 1),
   - `status/needs-rebase` to add + draft + comment if newly `CONFLICTING` and not
     already flagged (Rule 2),
   - `status/needs-rebase` to remove if flagged and now `MERGEABLE` (Rule 3),
   - `status/needs-signed-commits` to add + comment if any commit is unverified and
     not already flagged (Rule 4),
   - `status/needs-signed-commits` to remove if flagged and all commits are now
     verified (Rule 5).
3. Apply **one grouped label mutation** for all label changes, plus at most one draft
   conversion (only if newly drafting a not-already-draft PR) and at most one comment
   per rule that fires for the first time.
   Skip every PR that needs nothing.

## Report

After the run, output a concise summary of what changed:

- PRs newly labeled, with the `area/*` / `kind/*` added per PR.
- PRs newly flagged `status/needs-rebase` (drafted + commented).
- PRs cleared of `status/needs-rebase`.
- PRs newly flagged `status/needs-signed-commits` (with the list of unsigned commit
  SHAs per PR).
- PRs cleared of `status/needs-signed-commits`.
- PRs skipped because mergeable state was `UNKNOWN` (to be retried next run).
- Any PR left for human triage (ambiguous `kind/*` / `area/*`).

If nothing changed, say so explicitly — for an idempotent run over already-triaged
PRs, "no changes" is the expected and correct outcome.
