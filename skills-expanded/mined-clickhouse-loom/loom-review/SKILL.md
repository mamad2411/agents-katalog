---
name: loom-review
description: Reviews a Loom PR or diff against Loom's invariants and area rules and for needless complexity, verifying each finding before reporting it with severity and file:line. Use when asked to review a PR, branch or diff, or to post review comments. After your own push, start the loom-reviewer agent instead.
argument-hint: "[pr-number | branch | diff-range]"
metadata:
  internal: true
---

# Loom review

Review as a senior Loom maintainer would: report real problems (wrong results, data loss, cross-tenant reads, auth bypass, unbounded cost, broken operator rollouts) and code that is harder to read than its job needs, concisely and with evidence. Formatting the formatters own and speculative refactors are out of scope.

## 1. Get the change

```bash
gh pr view <n> --json title,body,baseRefName,headRefOid,files,comments
gh pr diff <n>                                  # or: git diff origin/main...<branch>
```

Read each changed file in full where the hunk alone does not show the invariant. For a diff over ~3000 lines, split it by package: review the parts in parallel from a session, in sequence inside `loom-reviewer`.

## 2. Gates

Do not give a verdict until each gate is addressed; a gate you could not close goes under "Blind spots" with what would close it.

1. **Contract.** What the title, body, changelog category and tests promise. A "Performance Improvement" promises a measured benefit; a "Bug Fix" promises the bug cannot recur (a regression test). State findings as broken promises or violated invariants.
2. **Impacted surface.** Follow the changed value, field, setting or state through unchanged callers, sibling ops, both transports (HTTP and MCP), the SDKs, the CLI, the workers and the dashboard.
3. **Failure and divergence.** Retries, partial writes, cancellation, a worker pass interrupted halfway, two replicas or two colours running at once during a deploy, a cache that outlives the row.
4. **Evidence.** Each material claim maps to a test, a measurement with its command, or a reason none is possible.
5. **Simplicity.** The change is the smallest design that does the job, and a new team member could follow it.

## 3. Loom invariants

The checklist is the files the diff touches, not a copy of them:

- the **Invariants** in [AGENTS.md](../../../AGENTS.md), for every diff;
- the rule for each area the diff touches (the `paths:` frontmatter of `.claude/rules/*.md` maps paths to rules; inside `loom-reviewer`, search it with the Grep tool): every bullet in it is a check;
- the "also in the same PR" column of `loom-change` for each kind of change in the diff (generated files, snapshots, manifests, docs).

Read each rule in full before judging its area. Also check what no rule owns: a hot-path query that is unbounded or untagged, a hook that can throw, block or print a secret in a user's session, an example or README that does not run as written, and public text (code, docs, PR body) that names people, hosts, internal namespaces, dates or other products.

## 4. Readability and simplicity

The code should read as if an experienced Python engineer wrote it by hand. Each of these is a finding, P3 unless it hides a bug (then rate the bug):

- an abstraction, class, flag or parameter with one caller and no second use in sight;
- a defensive branch, `try`, fallback or retry for a state the code cannot reach;
- a comment that restates the code, narrates the change ("now", "updated to", "per review"), or runs past two lines where one would do;
- a name that describes the mechanism rather than the domain (`data`, `result2`, `handle_stuff`);
- duplicated logic where an existing helper in `server/core/` or the domain's `store/` already does it;
- a compatibility shim, adapter or mode for a replaced internal path (tolerance for build N-1 and `ignored_args` for a removed wire field are required, not shims);
- a test that asserts the implementation (mock call order) instead of the behaviour (the row read back).

## 5. Verify before reporting

For each candidate finding, try to prove it wrong: read the caller, the test, the migration, run the test or a one-line probe. Drop it if it does not survive. Keep a serious, plausible risk you could not prove as "needs verification", with the evidence that would settle it.

## 6. Report

```
Verdict: approve | request changes | needs verification
Findings (most severe first)
  - [P0–P3] file:line — the violated invariant, the concrete input or state that breaks it, the fix
Missing tests or evidence
Blind spots
```

P0: data loss, a cross-tenant read, an auth bypass. P1: wrong results or a broken rollout on a common path. P2: an edge-case bug or a missing test for a promised behaviour. P3: a stale claim, a readability or simplicity finding, a missing cleanup.

Nothing found is a valid result: say "no findings" and list what was checked. Write each finding in the `loom-writing` voice: the problem first, no praise or softening.

## 7. Posting on GitHub

Post only when the requester asked for comments on the PR. Then post one review with one inline comment per finding, on the line it is about, not a wall of text in one comment:

```bash
review=$(mktemp) && cat > "$review" <<'JSON'
{"commit_id": "<head sha>", "event": "COMMENT", "body": "<verdict and blind spots, two or three lines>",
 "comments": [{"path": "server/memory/app/search/graph.py", "line": 88, "side": "RIGHT", "body": "P2 — <problem, failing input, fix>"}]}
JSON
gh api repos/ClickHouse/loom/pulls/<n>/reviews --input "$review"
```

- `line` is a line of the diff's new side; a finding outside the diff goes in the review body with its `file:line`.
- A one-line fix goes in a `suggestion` block so the author can apply it.
- `event` stays `COMMENT` from an agent; `APPROVE` and `REQUEST_CHANGES` are a maintainer's call.
- Do not repeat a point another reviewer already made in an open thread (`loom-address-review` §1 lists the threads); add evidence to that thread instead.
