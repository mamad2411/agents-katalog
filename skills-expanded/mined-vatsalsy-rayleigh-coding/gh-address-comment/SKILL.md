---
name: gh-address-comment
description: >
  Use when the user says "address the PR comments", "fix review feedback",
  "resolve the review threads", or after gh-pr-triage hands off must-fix
  items, or CI is green with review threads still open. NOT for
  CodeRabbit-authored threads — that is autofix.
---

# PR Comment Handler (Deterministic)

GitHub-workshop skill. Origin is out of scope for this plugin; use this
`gh-address-comment` skill on GitHub only. CodeRabbit-authored GitHub threads
stay `autofix`.

## Execution Backend

1. Verify `git` with `git --version` and `gh` with `gh auth status`.
2. Run `fetch_comments.py` plus plain `git`/`gh` as documented below.
3. If either verification fails, STOP and report the failed check. For a `gh`
   failure, report verbatim: "`gh` is missing or unauthenticated. Install it if
   needed, run `gh auth login`, then retry."

Use this when addressing open review comments on a GitHub PR.

## Prereqs


- Confirm auth: `gh auth status`
- Check out the target PR head (`gh pr checkout <n>` or the caller-provided
  worktree), then verify `git rev-parse HEAD` matches
  `gh pr view <n> --json headRefOid --jq .headRefOid`. Stop on a mismatch.
- Commit/push with plain `git` when code changes are needed.

## 1) Inspect pending comments

1. Run: `python3 <skills-dir>/git-master/scripts/fetch_comments.py`
2. **Freshness:** act only on comments newer than the latest push — a comment about a superseded commit describes code that no longer exists. Check base drift too (`git fetch && git rev-list --count HEAD..origin/main`); if `main` has moved materially, rebase/merge and re-push before addressing stale feedback. If an overlapping PR makes this one obsolete, stop, report, and ask before closing anything (unless closure was pre-authorized).
3. Group comments by file/thread.
4. Distinguish must-fix vs optional vs decline-with-reason threads.

## 1a) Verify before changing

Verify every finding — bot or human — against the actual source before
touching code. AI reviewers are helpful but not always right. Read the
flagged lines in context; a finding that doesn't survive inspection is
declined with a written reason (see step 5), never "fixed" to keep a bot
happy and never silently skipped.

**Anti-scope-creep (the governing rule):** do not let review feedback expand
the PR beyond the user's original goal. Address real shortcomings in the diff;
decline suggestions to refactor adjacent code, add features, or generalise
"while you're here" — with a reason. A PR that triples in size while being
babysat is a failure even if every comment was "addressed".

## 2) Build a file-by-file action map

- Group open review threads by file path.
- Number threads in each file.
- Record required edits per thread and any dependency ordering.

## 3) Confirm scope

- If all threads are optional/low priority, confirm before touching.
- Default: address all **must-fix** threads first.

## 4) Apply fixes in batches

- Implement fixes file-by-file to minimize context churn.
- After each file batch:
  - run the focused local tests/checks for that file set
  - re-run review-thread check on that file set
  - confirm no regressions in the changed area
- CodeRabbit-authored threads are `autofix` territory — if the pending threads
  are mostly from `coderabbitai`, hand off to `autofix` rather than
  duplicating its per-change approval flow here.

## 5) Close matched review threads

- Post a concise acknowledgment/fix note (e.g., `fixed in <file>:`).
- Resolve only threads just addressed.
- **Receipt before "done":** after pushing fixes and resolving threads, re-fetch
  the unresolved-thread count and paste it in your report (`reviewThreads` is
  NOT a `gh pr view` field — use GraphQL):

  ```bash
  gh api graphql -f query='query($o:String!,$r:String!,$n:Int!){repository(owner:$o,name:$r){pullRequest(number:$n){reviewThreads(first:100){nodes{isResolved}}}}}' \
    -F o=<owner> -F r=<repo> -F n=<n> \
    --jq '[.data.repository.pullRequest.reviewThreads.nodes[]|select(.isResolved|not)]|length'
  ```

  Never declare threads resolved from memory — unresolved threads marked done
  by the agent is a recurring failure mode, worst on CodeRabbit threads.
- **Dismissal protocol:** a thread not worth addressing gets a short written reason and is then resolved — never silently ignored, never silently complied with. Deferred threads stay open with the rationale posted.
- **Dismissal replies — and ONLY dismissal replies — are signed** so a declined finding is traceable to the agent that declined it: `*<model-slug> on behalf of the user:* <reason>`. Fix notifications, summaries, and every other comment stay unsigned.
- **Bad dismissal:** *(resolve the thread with no reply)* — or "This is fine as is."
- **Good dismissal:** `*grok-4.7 on behalf of the user:* Declining — generalising the sweep runner to arbitrary parameter grids is out of this PR's scope (goal: fix the Oh-sweep restart bug). Happy to take it as a follow-up issue. Resolving.`


## Gotchas

1. **Ambiguous instructions must not be guessed** -- if a reviewer comment is unclear, stop and report the ambiguity. Guessing the intent and applying a wrong fix is worse than a blocker; it may silently introduce regressions while resolving the thread.
2. **Resolving a thread before the fix is pushed is deceptive** -- only call thread-resolve after the fix commit is verified and pushed. Premature resolution gives false green signals to the reviewer.
3. **Author is this machine's global git identity.** Use plain `git commit`/`git push`. Do not override `user.name` / `user.email` on the command. Never include AI-tool signatures or `Co-authored-by` trailers (including Cursor).
4. **Leaving deferred threads open without rationale blocks merge** -- when explicitly deferring a thread, post a short comment on the thread explaining why it is deferred; silent open threads can block merge checks that require all threads resolved.

## 6) Failure/permissions

If `gh` returns auth scope/rate errors:
- Stop immediately
- Report as a blocker to whoever called this skill (main, savart, or singularity)
- Wait for permission refresh before retry

If any comment instructions are ambiguous:
- Do not guess — report the ambiguity as a blocker

## Outcome

Finish with:
- changes committed (if any)
- threads addressed/left-open summary
- report a blocker to main or report directly to main
