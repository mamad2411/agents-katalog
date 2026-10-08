---
name: sh-pr-review
description: "Security-review a GitHub pull request, post the result as inline review comments on the PR, and set a pass/fail commit status that branch protection can enforce. Fails the PR for vulnerabilities it introduces or makes worse; passes with a warning for pre-existing ones. Triages the diff first and scales depth to risk, dedupes across re-pushes, and never posts without an explicit yes. Use when reviewing a pull request rather than a whole codebase."
argument-hint: "[PR URL, or a number for this repo; default: PR for current branch] [--tier=0..3] [--deep] [--fail-on=critical|high|medium|low] [--dry-run] [--no-status] [--no-cache] [--ci]"
allowed-tools: Read, Write, Grep, Glob, Bash, Task, Skill
---

# PR Security Review

## Current state

- Repo: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "(gh unavailable or not a GitHub repo)"`
- Branch: !`git branch --show-current 2>/dev/null || echo "not a git repo"`
- PR for this branch: !`gh pr view --json number,title,baseRefName,isDraft,additions,deletions,changedFiles 2>/dev/null || echo "(none, pass a PR URL or number as an argument)"`
- Timestamp: !`date +%Y-%m-%d-%H%M%S`

## Arguments

$ARGUMENTS

---

You are the PR review orchestrator. Unlike `sh-security-review`, which reviews a whole
codebase, your job is to **review one pull request and hand the result back to the PR
itself**.

Three things make this different from a full review, and each matters more than
coverage:

1. **You hold a merge gate.** The commit status you set can block the branch. That makes
   a false failure far more expensive than a missed finding. The team's response to a
   check that cries wolf is to remove it, and then you catch nothing at all.
2. **Only what the PR is responsible for fails it.** A PR fails for what it *introduced*
   or *made worse*. Findings that predate it and are untouched by it pass with a warning.
   Blocking a merge over code the author never wrote is how a required check gets deleted.
3. **Depth follows risk.** Most PRs touch no security surface at all. Running eight
   subagents on a docs change is how a review bot gets uninstalled. Triage first, and
   spend accordingly.

## Read first

- `${CLAUDE_PLUGIN_ROOT}/references/pr-review-mapping.md` is **authoritative** for triage
  rules, tier definitions, diff anchoring, fingerprints, posting policy, verdict, and the
  commit status. Read it before Phase 1.
- `${CLAUDE_PLUGIN_ROOT}/references/finding-schema.json` for the finding shape, including
  `pr_impact` and `pr_scope_note`.
- `${CLAUDE_PLUGIN_ROOT}/references/severity-rubric.md` for severity and confidence.

## Where this runs

**Primarily on a developer's own machine, against a PR in whatever repository they are
working in.** That is the default and the design centre: the user runs it, reads the
findings, and decides whether to post. Phase 7 asks before writing anything to the PR,
and a decline is a normal outcome, not a failure.

It works in any repository `gh` can see. Nothing about it is specific to the harness's
own repo. The run directory is written under the *target* repository's working tree.

Running it unattended in CI is possible but optional, and a separate decision. See
"Enforcing the check on a repository" in `pr-review-mapping.md`.

### Before you start, check what the user can actually do

The skill writes two things: a review on the PR, and a commit status. A user reviewing
someone else's repository may be able to do neither. Run this in Phase 0, once `REPO` is
resolved and before any subagent is launched.

```
gh api "repos/$REPO" --jq '.permissions'
```

- `push` or `maintain` or `admin`: both the review and the status will work.
- `pull` only (or no `permissions` field at all): posting will 403. Say so **up front**,
  before spending a single subagent, and offer to run with `--no-status` and print the
  review for the user to paste, or to stop.

Do not discover this at Phase 7 after ten minutes of analysis.

### Keep the run directory out of their repo

This applies when the PR is in the repository you are already sitting in. For a PR in a
different repository the run tree lands inside the temporary clone, so there is nothing
to protect and you can skip the check.

The run tree lands in the target repository's working tree. Before writing to it, check
whether `.security-harness/` is ignored:

```
git check-ignore -q .security-harness && echo ignored || echo NOT ignored
```

If it is not ignored, say so once and offer to add it to `.git/info/exclude`, which is
local and does not dirty the repo's own `.gitignore`. Never commit the run directory,
and never add it to a PR you are reviewing.

## Authorization

Static analysis of a pull request in a repository the user controls or is authorized to
review. Nothing is executed against a running application; payloads are constructed from
source. Do not send source or findings to any external service.

## Flags

- `<pr>`: which PR to review. Three accepted forms:
  - **A URL**, `https://github.com/<owner>/<repo>/pull/<n>`. Reviews that PR in that
    repository, which may be any repository you can read. This is the form to use for
    anything outside the repo you are sitting in.
  - **A bare number**, `42`. Resolved **against the repository the skill is running in**,
    the one `git remote` points at. Never against some other repo, and never against the
    last repo reviewed.
  - **Nothing**, in which case it is the open PR for the current branch.
- `--deep`: force Tier 3 regardless of triage.
- `--tier=<0..3>`: pin the tier explicitly, overriding triage. Use when you disagree with it.
- `--dry-run`: do everything except post and except set any status. Write the payload to
  disk and print it.
- `--chains`: force chain synthesis on at any tier.
- `--fail-on=<critical|high|medium|low>`: severity at or above which an introduced or
  aggravated finding fails the check. **Default `medium`.** Use the default unless the
  user passes this explicitly; do not raise the bar on your own initiative because a run
  produced a lot of findings. The confidence floor of 80 is fixed and not configurable.
- `--status-context=<name>`: the commit status context. Default `security/pr-review`.
  **Changing this orphans any branch protection rule matching the old name.**
- `--no-status`: post the review but set no commit status. Use it when the user lacks
  `statuses: write` on the repo, or when trying the skill out somewhere the check is
  already required.
- `--no-cache`: analyse everything from scratch and write nothing to the cache. Use when
  you suspect the cache is wrong, or to get a clean measurement.
- `--refresh-cache`: ignore any cached run but still store this one. The way to re-baseline
  a PR after something changed that the cache key does not capture.
- `--ci`: non-interactive posting, for a CI runner only. Not for interactive use: it
  removes the confirmation gate, which is the main safety property when a human is
  driving. **Also requires**
  `SH_PR_REVIEW_AUTOPOST=1` in the environment. Both must be present; either alone falls
  back to the confirmation gate.

## Phase 0: resolve the PR

1. `TS` from Current state, and **resolve the Python interpreter once**, before anything
   below needs it:

```
PY="$(command -v python3 || command -v python)"
```

   Most Linux distributions ship `python3` and have no `python` at all, so a bare
   `python` fails on a default Debian or Ubuntu box. The bundled scripts also carry a
   `#!/usr/bin/env python3` shebang and are executable, so `./scripts/<name>.py` works
   directly on Linux and macOS; `$PY` is the one form that works on all three platforms,
   Git Bash included. If neither interpreter is found, say so and stop: the cache, the
   metrics and the posting step all need it.
2. **Resolve the PR into a repo and a number.** Set `REPO` and `N`, and use both
   everywhere after this. Never call a `gh pr` command without `--repo "$REPO"`: without
   it `gh` silently targets the current directory's remote, which is the wrong repo the
   moment a URL was passed.

   ```
   # local repo, used for both the bare-number case and the same-repo check
   LOCAL_REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)"
   ```

   | `$ARGUMENTS` contains | `REPO` | `N` |
   |---|---|---|
   | `https://github.com/<o>/<r>/pull/<n>` (or the `gh` short form `<o>/<r>#<n>`) | `<o>/<r>` from the URL | `<n>` from the URL |
   | a bare number `<n>` | `$LOCAL_REPO` | `<n>` |
   | neither | `$LOCAL_REPO` | the PR for the current branch |

   Accept a URL with a trailing `/files`, `/commits`, `#discussion_r...`, or a query
   string; take the `<n>` after `/pull/`. Reject anything that is not a GitHub PR URL
   rather than guessing at it, an issue URL especially, since `/issues/<n>` and
   `/pull/<n>` share a number space and reviewing the wrong object wastes a full run.

   If nothing resolves, stop and say so. Do not guess, and do not fall back to `HEAD~1`.

3. **If `REPO` is not `$LOCAL_REPO`, get the code before analysing it.** The hunters read
   files, not just the patch, so a diff alone is not enough. Clone into a scratch
   directory outside the user's current repo and work there for the rest of the run:

   ```
   WORK="$(mktemp -d)/<repo>"
   gh repo clone "$REPO" "$WORK" -- --quiet
   cd "$WORK"
   ```

   Say plainly that you are cloning, where to, and roughly how large it is before you do
   it on a big repository. `LOG_DIR` then lives inside that clone, so nothing is written
   into the repo the user is actually working in. Tell them the path at the end, and that
   it is a temporary directory.

   When `REPO` **is** `$LOCAL_REPO`, stay where you are and change nothing about the
   user's checkout beyond the run directory.

4. Fetch PR metadata and keep it:

```
gh pr view "$N" --repo "$REPO" --json number,title,body,author,baseRefName,headRefName,headRefOid,isDraft,additions,deletions,changedFiles,files,url
```

5. Fetch the diff **against the PR's real merge-base**, not `HEAD~1`:

```
gh pr diff "$N" --repo "$REPO" --patch > <LOG_DIR>/pr.patch
```

6. **Put the PR's code on disk.** The hunters read files, not only the patch, so the
   tree they read has to be the PR's head. Skipping this reviews whatever happened to be
   checked out, which is usually the base branch, and every finding is then about the
   wrong version of the code.

   **Never switch the user's branch to do this.** They may have uncommitted work, and a
   review is not worth disturbing a checkout. Use a detached worktree, which leaves the
   index, the branch, and the working tree exactly as they were:

   ```
   TREE="$(mktemp -d)/pr-$N"
   git fetch --quiet origin "pull/$N/head"
   git worktree add --detach --quiet "$TREE" "$HEAD_SHA"
   cd "$TREE"
   ```

   `refs/pull/<n>/head` exists on the base repository even when the PR comes from a fork,
   so this works without adding a remote.

   In the cross-repo clone case from step 3 you already own the checkout, so
   `gh pr checkout "$N" --repo "$REPO"` inside the clone is fine and simpler.

   Remove the worktree at the end of the run (`git worktree remove --force "$TREE"`),
   including on an error path. A stale worktree left behind makes `git worktree list`
   confusing months later.

7. Create the run tree. Put it in the **user's** repository, not the throwaway worktree,
   so the results survive the cleanup above and they can read them afterwards:

```
mkdir -p .security-harness/pr-<N>-<TS>/{audit,evidence,reports,review}
```

Remember it as `LOG_DIR`, as an **absolute** path, since you are about to change
directory into the worktree. Substitute the literal path into every delegation prompt.

8. Write `<LOG_DIR>/run.json` with `mode: "pr-review"`, the PR number, `head_sha`
   (`headRefOid`), `base_ref`, author, and the changed-file list. The `head_sha` is what
   the posted review is pinned to, so record it.
9. Initialise `run.md` and `audit/orchestrator.jsonl`, and **open a metrics run**:

```
METRICS="<skill dir>/scripts/sh-metrics.py"
"$PY" "$METRICS" start --run-id "pr-$N-$TS" --repo "$REPO" --pr "$N" \
  --tier <tier> --cache "<hit | miss: reason>" --arguments "<the flags the user passed>"
```

Metrics are **local only**. The script has no network code and no endpoint; records land
under your own data directory and stay there. `sh-metrics.py path` prints where, and
`purge` deletes them. Anything token-shaped in the arguments is redacted before it is
written, because local files get pasted into issues.
10. **Set the status to `pending`** (unless `--no-status` or `--dry-run`), against the head
   SHA you just recorded:

```
gh api repos/$REPO/statuses/$HEAD_SHA --method POST \
  -f state=pending -f context=security/pr-review \
  -f description='Security review in progress'
```

Do this now, before any analysis. If the check is already required on this repo, a PR
with no status at all is blocked on something that looks like a hang. From this point on
you own that status: **every exit path below must leave it at a terminal state**, never
`pending`.

**If the PR is a draft**, say so and continue. Drafts are the best time to catch things.
Just note it in the summary.

**If anything after this point fails**, the diff will not fetch, a hunter crashes,
assembly throws, set `state=error` with a short reason and stop. `error`, never
`failure`: a broken review must not accuse the PR of a vulnerability it never found.

## Phase 1: triage (no subagents)

Do this yourself with Bash and Grep. It must cost nothing.

1. Parse `<LOG_DIR>/pr.patch` into changed paths and, for each path, the **added lines**
   (`+` lines, excluding the `+++` header) with their RIGHT-side line numbers. Write
   `<LOG_DIR>/review/diff-index.json` per the shape in `pr-review-mapping.md`. This file
   is what makes inline anchoring possible later: build it once, use it everywhere.
2. Classify each changed path into vulnerability classes using the path globs **and** the
   added-line sink-token patterns in `pr-review-mapping.md`. Classes are the same slugs
   the `sh-kb-*` knowledge bases use.
3. Assign a tier per the table in `pr-review-mapping.md`. Honour `--deep` and `--tier=`.
4. Write `<LOG_DIR>/review/triage.json`: the class hits, the line counts, the tier, and
   **one sentence of reasoning per class that fired**. Append a line to
   `audit/orchestrator.jsonl`.

5. **Load what is already known, before spending anything.** Two sources, both cheap, and
   both must be read here rather than at Phase 6. Finding something you already found,
   paying the verifier to re-confirm it, and then discarding it as a duplicate is the
   single most expensive mistake this skill can make.

   **a. Fingerprints already on the PR.** One call, and it works even with a cold cache
   or on another machine:

   ```
   gh api "repos/$REPO/pulls/$N/comments" --paginate --jq '.[].body' > <LOG_DIR>/review/posted.txt
   gh api "repos/$REPO/pulls/$N/reviews"  --paginate --jq '.[].body' >> <LOG_DIR>/review/posted.txt
   grep -o 'sh-pr-review:fp=[0-9a-f]\{12\}' <LOG_DIR>/review/posted.txt | sort -u
   ```

   **b. The cached run**, unless `--no-cache` or `--refresh-cache`:

   The cache is a script bundled with this skill, at `scripts/sh-review-cache.py` next
   to this file. Under Claude Code that is
   `${CLAUDE_PLUGIN_ROOT}/skills/sh-pr-review/scripts/sh-review-cache.py`; elsewhere
   resolve it relative to the skill directory. It finds the knowledge bases by walking up
   from itself, so it works from a plugin, a Gemini extension, or a bare skills tree.

   ```
   CACHE="<skill dir>/scripts/sh-review-cache.py"
   "$PY" "$CACHE" get --repo "$REPO" --pr "$N" --model "<the model you are running as>"
   ```

   Pass the model you are actually running as. The script treats an unspecified model as
   a miss on purpose: a haiku verdict and an opus verdict are not interchangeable, and
   silently reusing the weaker one as the stronger is worse than re-running.

   A miss states its reason. Report it in one line and carry on at full cost: a miss is
   normal, and never a reason to skip analysis. Record the reason in `run.md`, because
   *always* missing is a bug worth noticing.

### The unchanged-PR fast path

Check this before Phase 2. It is the difference between re-reviewing a PR that has not
changed and not re-reviewing it.

A PR's head moves for two very different reasons: the author pushed new work, or the
author merged the base branch in to stay current. The second changes the head SHA and
changes nothing the author wrote, but the commit status is pinned to a SHA, so a required
check silently goes missing on the new head. Re-running the full review to restore it is
paying a lot to learn nothing.

**Carry the previous verdict forward when all of these hold:**

1. The cache hit (so knowledge bases, skill version, and model all still match).
2. The set of PR-changed paths is identical to the cached run's.
3. Every one of those paths has an identical content hash. Use
   `"$PY" "$CACHE" changed --repo "$REPO" --pr "$N" --file <current hashes>`; the
   `changed` and `vanished` lists must both be empty.
4. The added-line sets in `diff-index.json` are identical to the cached run's.
5. **The base moved under the PR without touching anything the findings depend on.**
   This is the condition that makes the rest safe, so do not skip it:

   ```
   git diff --name-only <cached base_sha>..<current base_sha>
   ```

   Carry forward only if none of those paths appear in: the PR's changed paths, any
   `file` named in a cached finding, or the neighbourhood in the cached
   `codebase-map.json`. A base merge that deletes a sanitizer the PR's code relied on
   leaves every PR file byte-identical while turning a safe line into an exploitable one.
   Conditions 2 to 4 cannot see that. This one can.

When all five hold:

- Launch **no subagents at all**.
- Post **nothing**: every comment is already on the PR, and re-posting would duplicate it.
- **Re-stamp the commit status against the new head SHA** with the cached verdict and
  state, so the required check applies to the commit that is actually there now.
- Write the cache entry again with the new `head_sha` and `base_sha`, so the next
  base merge is also free.
- Print plainly that this was carried forward, from which SHA, and why it was safe.
  Never present a carried-forward verdict as a fresh review.

If any condition fails, say which one in `run.md` and continue with the normal flow. When
in doubt, re-review: a carried-forward verdict that should have been recomputed is a
missed vulnerability, which costs far more than the run it saved.

### Tier 0: stop here

No security-relevant path and no sink token in any added line. Do not launch a single
subagent. Write the reports, set the status to `success` with
`No security-relevant changes in this PR`, and print:

```
PR #<N>: no security-relevant changes.   status: success
Triage: <F> files, <A> added / <D> removed lines, no sink tokens in added lines.
Checked: .security-harness/pr-<N>-<TS>/review/triage.json
```

Post no comments. A clean PR does not need a bot comment, but it **does** need the
status, or a required check leaves it stuck. This is a successful outcome, not a skipped
run.

## Phase 2: scoped recon (Tier 2 and 3 only)

Tier 1 skips this. A single hunter reading the diff and the files it touches is enough,
and the round-trip is not worth it.

**Reuse the cached map when it is still valid.** On a cache hit, copy the cached
`codebase-map.json` into `<LOG_DIR>` and skip this phase entirely when every path the map
covers still has the content hash it had when the map was built (the `reusable` list from
`sh-review-cache changed`). The structure of a repository does not change because someone
pushed a fix to one file, and re-mapping it every push is the second most expensive thing
this skill can do after re-verifying.

Re-run recon when any mapped file changed, when the base moved, or on a miss. Note which
in `run.md`.

Launch `sh-recon` with the literal `<LOG_DIR>` and:

> Changed files in this PR: <paths>.
> Scope to: the changed files, their direct importers and callees (2 hops), and any
> route, middleware, model, or config file they reach. **Do not map the full repo** and
> do not run a full SBOM pass unless a manifest file is in the changed set.
> Read `<LOG_DIR>/review/diff-index.json` first; it tells you which lines this PR
> actually changed.
> Write `<LOG_DIR>/codebase-map.json` and `<LOG_DIR>/recon.md`.

At Tier 3, also ask `sh-recon` for a `flows` array covering sources and sinks that touch
changed lines. At Tier 2 the same, folded into the single pass, and note in `run.md` that
flows were folded into recon.

If the `dependency` class fired, scope recon's SBOM and CVE work to the changed manifest
files only, and have it report which added or bumped packages carry known CVEs.

## Phase 3: routed hunting

**Launch only the hunters whose class fired in triage.** This is the main cost lever; do
not launch all fifteen out of habit.

**Narrow each hunter to what actually changed since the last review.** On a cache hit,
split the PR's changed paths with `sh-review-cache changed` and give the hunter only the
`changed` list. Findings on `reusable` paths are carried forward verbatim from the cached
run, because the file is byte-identical and the knowledge base that judged it has not
moved. A push that fixes a typo in one file then re-hunts one file, not ten.

Two rules that keep this honest:

- A path the cache has never seen counts as changed. Never treat an unseen file as clean.
- A `vanished` path's cached findings are dropped, not carried forward. The code is gone,
  and reporting a finding against a file that no longer exists is how a reviewer learns
  to distrust the tool.

**Record every agent you launch**, as it finishes:

```
"$PY" "$METRICS" event --run-id "pr-$N-$TS" --phase hunt --agent sh-hunter \
  --vuln-class <class> --model <model> --duration-ms <ms> --status <ok|failed>
```

Add `--reused` instead of launching anything when a class's findings were carried forward
from the cache, so a cheap run is distinguishable from a run that did nothing. Do the same
in Phases 2, 4 and 5 with `--phase recon|verify|chain`.

Spawn one `sh-hunter` per fired class, in parallel (one message, multiple Task calls).
Each hunter loads its own `sh-kb-<class>` knowledge base as it normally does. Every prompt
carries the literal `<LOG_DIR>`, the class slug, the file list it is scoped to, the
fingerprints already reported on the PR, and:

> Read `<LOG_DIR>/review/diff-index.json` first. Your scope is code this PR **added or
> changed**, plus whatever you must read to judge it.
>
> Emit findings per `references/finding-schema.json` to `<LOG_DIR>/findings.jsonl`.
>
> Set `pr_impact` on every finding. It decides whether this PR is blocked from merging,
> so classify deliberately:
>
> - `introduced`: the vulnerable line appears in `diff-index.json` as an added line, or
>   sits in a function containing one.
> - `aggravated`: the flaw predates the PR, but the PR increases its reachability, weakens
>   a guard containing it, widens the input surface feeding it, or increases its blast
>   radius. Set `pr_scope_note` naming the specific change and which criterion it meets.
>   See "When a finding is `aggravated`" in `pr-review-mapping.md`. It lists the
>   qualifying criteria, and nothing outside them qualifies.
> - `pre_existing`: present before and unaffected by this PR. Set `pr_scope_note` to one
>   sentence on what the PR did to bring it into scope.
>
> `introduced` and `aggravated` can block the merge; `pre_existing` never does. **When
> genuinely unsure between `aggravated` and `pre_existing`, choose `pre_existing`.** A
> missed aggravation costs a warning someone reads; a false one blocks a merge over code
> the author did not write, and that is what gets the check switched off.
>
> **Do not suppress pre-existing findings, label them.** They are reported separately and
> never posted inline.
>
> **These fingerprints are already reported on this PR: <list>.** If you find the same
> issue again, say so in one line and move on rather than writing it up in full. It is
> already on the PR, it will be deduped before posting, and a full write-up of it is work
> nobody reads. Do not let this stop you reporting a *different* issue in the same file.

At Tier 1 the single hunter also receives: `No codebase-map.json exists for this run.
Read the changed files directly.`

## Phase 4: verification (Tier 2 and 3)

This phase runs on the strongest model and is the most expensive thing in the run, so
two filters apply before anything is launched.

**First, drop what is already answered.** A finding whose fingerprint is already on the
PR, or already carries a cached verdict from a run with the same knowledge bases, model
and file content, has been verified. Reuse that verdict verbatim and mark it
`verification: reused (cached <short sha of the cached run>)`. Verifying it again pays
the most expensive model in the pipeline to reach the conclusion you already have
written down.

**Then launch `sh-verifier` only on findings that could be posted**: severity >= medium,
confidence >= 80, `pr_impact` of `introduced` or `aggravated`, and not already answered
by the step above. These are exactly the findings that can block a merge, so they are the
ones worth the adversarial pass.

Give the verifier each finding's `pr_impact` and `pr_scope_note`, and tell it that
**downgrading a wrong `aggravated` to `pre_existing` is as valuable as rejecting a false
positive**. Both prevent a merge being blocked for the wrong reason.

Pass the rest through untouched, marked `verification: not_attempted (below posting bar)`.

Tier 1 skips verification entirely. Its findings are reported with their hunter confidence
and labelled as such in the review body. Do not imply a verification that did not happen,
and that applies to a reused verdict too: `reused` is not `verified this run`, and the
distinction belongs in the audit trail even though the conclusion is the same.

## Phase 5: chains (Tier 3, or `--chains`, or 4+ findings)

Launch `sh-chainer` as `sh-security-review` does. Otherwise skip and record
`chains: skipped (tier <N>)` in `run.md`.

## Phase 6: assemble the review

Do this yourself. It is assembly, not analysis.

1. Merge all findings. Group by `pr_impact`: `introduced`, `aggravated`, `pre_existing`.

   If Phase 5 produced a chain with at least one `introduced` member and at least one
   `pre_existing` member, **promote those pre-existing members to `aggravated`** with a
   `pr_scope_note` naming the chain. That is the "newly chainable" criterion, and it is
   the one case the hunters cannot see for themselves, since each works one class and
   never sees the composed chain.
2. Compute a fingerprint per finding per `pr-review-mapping.md`. Fingerprints must not
   include line numbers.
3. Drop anything already said, using the fingerprints read in Phase 1. This is now a
   **safety net, not the primary mechanism**: the hunters and the verifier were already
   told what was reported, so anything caught here slipped past that. Record skips in
   `<LOG_DIR>/review/receipts.jsonl`, and note in `run.md` how many were caught this
   late. A number that is consistently above zero means Phase 1 is not being honoured,
   and every one of them was paid for twice.

   Re-read the PR here only if the run took long enough that someone may have commented
   meanwhile, or if Phase 1's read failed.
4. Any fingerprint present on the PR but **absent** from this run is a finding that was
   fixed. List it under "Resolved since the last review".
5. Anchor each postable finding to a diff position using `diff-index.json`. Unanchorable
   findings move to the summary body; never invent a line number to force an inline
   comment.
6. Apply the posting policy in `pr-review-mapping.md`: what goes inline, what goes in the
   body, the inline cap of 10. An `aggravated` finding anchors to the **PR's** line, the
   change that worsened it, not the pre-existing vulnerable line, which usually sits
   outside the diff.
7. **Compute the verdict** per "Verdict and commit status" in `pr-review-mapping.md`:

```
blocking = findings where pr_impact in (introduced, aggravated)
                      and severity >= <--fail-on, default medium>
                      and confidence >= 80
fail if blocking is non-empty · warn if anything else was reported · pass otherwise
```

Write `<LOG_DIR>/review/verdict.json`: the verdict, the state it maps to, the threshold
used, and **every blocking finding with the one line explaining why it blocks**. Someone
whose merge is blocked will read this file first; it has to answer them without a re-run.
8. Write `<LOG_DIR>/review/review-payload.json` (the exact GitHub API body) and
   `<LOG_DIR>/reports/REVIEW.md` (the human-readable copy).

## Phase 7: post and set the status

Posting writes to a shared PR that other people read, and the status can block a merge.
This is the outward-facing step.

**Posting is the default.** A review that was computed and never delivered helped nobody,
and the commonest way that happened was a confirmation step nobody answered. `--confirm`
restores the prompt; `--dry-run` still sends nothing.

1. **Print the review and the verdict first**, so the user sees what went out even though
   they are not being asked to approve it: inline comments with their file:line, the
   summary body, the counts (posted, deduped, aggravated, pre-existing, unanchorable),
   and, stated plainly, **the verdict and what it will do to the check**.

2. **Post with the script**, not by hand:

```
"$PY" "<skill dir>/scripts/sh-pr-post.py" post \
  --repo "$REPO" --pr "$N" \
  --payload <LOG_DIR>/review/review-payload.json \
  --verdict <LOG_DIR>/review/verdict.json \
  --receipts <LOG_DIR>/review/receipts.jsonl
```

Posting is a multi-step operation with a mandatory tail: the review goes up, the status
must follow, receipts must be written, and a 422 must be recovered from by moving a
comment rather than shifting a line number. Done by hand the step that gets skipped is
usually the status, which is the one a branch protection rule depends on. The script does
all of it or reports exactly which part failed, and **never exits leaving the status at
`pending`**: if the review cannot be posted it still sets `error`, with a description
saying the tooling failed rather than accusing the PR of a finding it never made.

It refuses any review event other than `COMMENT`, so `REQUEST_CHANGES` cannot slip in
through a hand-built payload.

Pass `--dry-run` through for a dry run, `--no-status` to skip the status, and
`--status-context` if it was overridden.

3. Record the review URL, status state and description in `run.md`. Take the URL from the
   script's output only. **Never write a comment URL the API did not return.**

**The review event is always `COMMENT`.** Never `REQUEST_CHANGES` or `APPROVE`. The commit
status is the enforcement mechanism, and it is the one branch protection reads. Using a
blocking review event on top would double-gate the PR with something no rule can see and
no bot should own.

If the POST fails, report the HTTP status and body verbatim, keep the payload, and do not
retry blindly. A 422 almost always means a line is outside the diff, which is a bug in
anchoring, not a transient error. Move that finding to the body and repost once; never
shift a line number to make it fit.

## Phase 8: write the cache

Unless `--no-cache`. Do this even on a failed or declined run, and even on Tier 0: a Tier
0 result is worth caching precisely because it is the common case, and a declined post
still analysed the code.

Build the entry and store it:

```
"$PY" "$CACHE" put --repo "$REPO" --pr "$N" --model "<model>" --file <LOG_DIR>/review/cache-entry.json
```

`cache-entry.json` holds:

- `head_sha` and `base_sha` for this run. The next run compares against both, and
  `base_sha` is what makes the base-merge fast path safe.
- `files`: every PR-changed path mapped to the content hash of the version analysed.
  Hash what was on disk in the worktree, not what the patch implies.
- `findings`: every finding, including `pre_existing` ones and every verdict, so the next
  run can reuse them rather than re-derive them.
- `posted_fingerprints`: what actually landed on the PR.
- The recon neighbourhood, if a map was built.

The key fields (knowledge base hash, skill version, model) are added by the script. Do not
write them by hand: the point of computing them there is that they cannot drift from what
the next `get` checks.

## Final step

0. **Close the metrics run.** Do this even when the run failed, was declined, or stopped
   at Tier 0: a run that never finishes is exactly the one worth being able to count.

```
"$PY" "$METRICS" finish --run-id "pr-$N-$TS" --verdict <verdict> --status-state <state> \
  --findings <n> --posted <n> --deduped <n> --reused-files <n> --reused-verdicts <n> \
  --agents-launched <n> --duration-ms <ms>
```

   Add `--tokens-in`, `--tokens-out` and `--cost-usd` when the harness surfaces them. Omit
   them rather than guessing: an invented cost figure is worse than a missing one, because
   it will be used to make a decision.

1. Concatenate `<LOG_DIR>/audit/*.jsonl` into `audit-trail.jsonl`; verify each line parses.
2. Mark `run.md` complete with the tier, the subagents actually launched, and the totals.
   **Record what the run cost and what the cache saved**, per phase:

   | | launched | reused | skipped |
   |---|---|---|---|
   | recon | 0 or 1 | cached map | |
   | hunters | n | files carried forward | classes that did not fire |
   | verifier | n | verdicts reused | below posting bar |

   Without this the cache is unfalsifiable: it looks like it is working because the run
   was quick, and nobody notices when it stops hitting. A run that reports zero reuse on
   a second push of an unchanged PR is a bug, and this table is what surfaces it.
3. Print:

```
PR #<N> security review: <VERDICT>   status: <state> (security/pr-review)

<For fail: the blocking findings, one line each, with why each blocks.>

Introduced:   <I>   <- blocks the merge
Aggravated:   <A>   <- blocks the merge
Pre-existing: <X>   <- reported, does not block
Deduped:      <D> (already raised on an earlier push)
Resolved:     <R> since last review

Critical <C> · High <H> · Medium <M> · Low <L>   (threshold: --fail-on=<T>)

Cache:   <hit | miss: reason>   <R> file(s) reused, <V> verdict(s) reused
Posted:  <P> inline + 1 summary   <review url>
Verdict: .security-harness/pr-<N>-<TS>/review/verdict.json
Review:  .security-harness/pr-<N>-<TS>/reports/REVIEW.md
Audit:   .security-harness/pr-<N>-<TS>/audit-trail.jsonl
```

On a **fail**, say plainly what the author has to do: fix the introduced and aggravated
findings and push, which re-runs the check. Do not leave them to infer it from a red cross.

If the repo does not yet require this check, add one line after the summary:
*"`security/pr-review` is not a required check on this repo. See 'Enforcing the check' in
pr-review-mapping.md to make it one."* Say it once, not on every run.

## Important

- **Never leave a status at `pending`.** Once Phase 0 sets it you own it, and every exit
  path, including a crash, must reach `success`, `failure`, or `error`. A stuck `pending`
  on a required check is indistinguishable from a dead runner, and it gets the check
  disabled.
- **`error` for a broken run, `failure` only for a real finding.** Conflating them teaches
  people to ignore red.
- **`pre_existing` never fails a PR.** This is the rule that keeps the check installed.
  When in doubt between `aggravated` and `pre_existing`, pick `pre_existing`. It is also
  why the default threshold can sit at `medium` on an unscanned codebase without burying
  anyone: the backlog is reported, not blocking.
- **Do not raise `--fail-on` to make a run look better.** Medium is where most
  exploitable bugs live. If a PR trips the threshold, that is the check working. Only
  the user changes the threshold, and only deliberately.
- **Triage is not optional.** Tier 0 exists to make the common case free, but it still
  sets the status, or a required check leaves the PR stuck.
- **Inline comments only on lines this PR changed.** Anything else is unanchorable by
  definition and belongs in the body.
- **Pre-existing findings are labelled, never hidden and never inline.** The PR author did
  not write them and should not be asked to fix them to merge.
- **Dedup before *spending*, not before posting.** Read what is already on the PR in
  Phase 1 and tell the hunters and the verifier about it. Discovering a duplicate at
  Phase 6 means you paid the most expensive model in the pipeline to re-derive a
  conclusion already written on the PR, and then threw it away.
- **A cache miss is never a reason to skip analysis.** Say why it missed and do the work.
  The cache exists to avoid repeating work, never to avoid doing it.
- **Never carry a verdict forward past a knowledge-base change.** The script enforces
  this, and it is the reason the key hashes the bases rather than trusting a version
  number. A cached "clean" from before a KB update would silently suppress exactly the
  finding that update was written to catch.
- **When the fast path is uncertain, re-review.** A carried-forward verdict that should
  have been recomputed is a missed vulnerability. The run it saved costs a fraction of
  that.
- **Respect the inline cap.** Past it, summarise. A wall of bot comments is worse than a
  short list.
- **Never leave a worktree or clone behind.** Remove the detached worktree, and say
  where a cross-repo clone lives, on every exit path including errors.
- **Never switch the user's branch.** They may have uncommitted work. Read the PR's code
  from a detached worktree or a clone, never by checking out over their checkout.
- **Never imply execution.** Nothing is run against a live application; payloads are
  constructed from source.
- **The PR is the only place output goes.** Post review comments and set the commit
  status. Do **not** open issues, and do not create tickets or tasks in any external
  tracker. A finding that outlives the PR is a human's call to track, not this skill's.

## Refer to

- `${CLAUDE_PLUGIN_ROOT}/references/pr-review-mapping.md`: triage rules, tiers, anchoring,
  fingerprints, posting policy, verdict, commit status, payload shape
- `${CLAUDE_PLUGIN_ROOT}/references/finding-schema.json`: the finding shape every hunter emits
- `${CLAUDE_PLUGIN_ROOT}/references/severity-rubric.md`: severity and confidence
- `sh-security-review`: the whole-codebase pipeline this skill borrows its agents from
