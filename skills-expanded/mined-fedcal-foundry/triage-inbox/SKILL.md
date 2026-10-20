---
name: triage-inbox
description: Work through the open issues and pull requests of a repository against that project's own contribution rules, producing a prioritised action list and the exact gh commands to apply it. Use for a backlog sweep, a triage rota shift, or before a release when the inbox must be cleared. Not for fixing the bugs, reviewing code, or changing policy.
disallowed-tools: Edit
user-invocable: true
argument-hint: "[--limit 100] [--since 30d] [--apply|--dry-run] [--only issues|prs]"
model: sonnet
effort: medium
metadata:
  foundry.vertical: governance
  foundry.io: "open issues + PRs -> review.v1 + prioritised action script"
license: Apache-2.0
---

# Triage the inbox

A backlog sweep that produces opinions is wasted work. This skill produces **decisions with
commands**: every item leaves the pass classified, prioritised, and with a next action that a
human can execute or approve in one go.

**Default is `--dry-run`.** Nothing is written to GitHub until the action list has been read.
Mass-mutating a stranger's backlog is how automation loses trust permanently.

## Step 1 — Load the project's own rules

Triage against *this* project's rules, not generic ones. Read and quote them in the report:

```bash
ls CONTRIBUTING.md SUPPORT.md SECURITY.md GOVERNANCE.md .github/ISSUE_TEMPLATE/ 2>/dev/null
grep -niE 'stale|response|reproduc|scope|will not|out of scope' CONTRIBUTING.md SUPPORT.md
gh label list --limit 200 --json name,description
mcp__plugin_foundry-core_foundry__runbook_get triage    # project-specific triage runbook, if one exists
```

Extract, and state the source line for each: the required bug-report fields, the stale windows,
the published response times, the stated scope and non-goals, the label taxonomy in use, and
the security reporting route.

**If these files do not exist**, say so plainly, use the defaults from the `issue-triager`
agent, label them as defaults, and add "run `bootstrap-oss`" as the first item of the action
list — an untriageable backlog is usually a missing-rules problem.

## Step 2 — Fetch the inbox

```bash
command -v gh >/dev/null && gh auth status >/dev/null 2>&1 || echo 'DEGRADED: no gh'

gh issue list --state open --limit "${LIMIT:-100}" \
  --json number,title,body,labels,createdAt,updatedAt,author,comments,assignees,milestone \
  > .foundry/scratch/$SESSION/issues.json

gh pr list --state open --limit "${LIMIT:-100}" \
  --json number,title,body,labels,createdAt,updatedAt,author,isDraft,reviewDecision,mergeable,statusCheckRollup,files,additions,deletions \
  > .foundry/scratch/$SESSION/prs.json
```

Degraded mode without `gh`: work from a caller-supplied export or the local checkout, produce
the action list as a script, and state in the report that live state was not read. If no data
is available at all, stop and report `blocked`. **Never fabricate a backlog.**

## Step 3 — Order the queue

Do not process by number. Process in the order that reduces harm fastest:

1. **Security-looking items**, any age (`grep -iE 'vulnerab|exploit|CVE|RCE|XSS|injection|traversal|secret|token'`).
2. **PRs from first-time contributors** older than the published review time — this is the
   highest-attrition queue in the project.
3. **New items** created since the last sweep (`--since`), oldest first.
4. **`status:needs-info`** past its window (close or nudge).
5. **Unlabelled backlog**, oldest first (`gh issue list --search 'no:label'`).
6. **`priority:p3` and stale candidates** last, in bulk.

Report the queue sizes before starting; if the total exceeds what one sitting can absorb, do the
first three categories and say what was left, rather than doing all of them badly.

## Step 4 — Classify each item

Delegate the per-item protocol to the `issue-triager` agent — reproducibility check, label
taxonomy, severity vs priority, duplicate detection, report rewriting, closing wording, stale
policy. Do not reimplement it here.

Batch the items (20–30 per invocation) so the agent's context stays useful, and require it to
return `finding.v1` entries rather than prose.

## Step 5 — Pull requests get their own checks

Issues and PRs fail differently. For every open PR, record:

| Check | Command / field | Action when it fails |
|---|---|---|
| CI status | `statusCheckRollup` | If red for an external contributor, comment with the failing job name and the local command to reproduce — do not just leave the red X. |
| Mergeability | `mergeable` | `CONFLICTING` ⇒ ask for a rebase, with the command. |
| Linked issue / accepted RFC | body `Closes #` | Unsolicited large PR with no issue ⇒ this is the **worst** outcome for both sides; respond within the day. |
| Size | `additions + deletions` | > 400 changed lines with no prior discussion ⇒ ask to split, and say which part will be reviewed first. |
| Signed-off / CLA | `git log --format='%(trailers:key=Signed-off-by)'` on the branch | Point at the exact fix (`git rebase --signoff`). |
| Who spoke last | last comment author | **Maintainer last ⇒ contributor's turn. Contributor last ⇒ our debt**, and it counts in the review-latency metric. |
| Draft | `isDraft` | Excluded from latency metrics; do not nag. |
| Staleness | `updatedAt` | Never stale a PR whose last message was from a maintainer. |

A PR that has been waiting on the project for longer than the published review time is a
**defect of the project**, and appears in the report as such, not as a stale candidate.

## Step 6 — Produce the action list

Write two artifacts:

**`.foundry/blackboard/<wave>/triage-inbox.json`** — a `handoff.v1` whose `artifacts[]` point at
the `issue-triager` `review.v1` batches, with a `summary` of ≤ 300 tokens containing the counts
and the top escalations.

**`.foundry/blackboard/<wave>/triage-actions.sh`** — the executable action list, grouped and
commented, safe by construction:

```bash
#!/usr/bin/env bash
set -euo pipefail
# Generated <date> against <owner/repo>@<sha>. Review before running.

### 1. ESCALATE — security, do not run blindly
# gh issue view 812   # suspected undisclosed vulnerability; move to a private advisory

### 2. LABEL (safe, reversible)
gh issue edit 790 --add-label 'type:bug,status:confirmed,priority:p2,sev:medium' \
                  --remove-label 'status:needs-triage'

### 3. ASK FOR INFO
gh issue comment 774 --body-file .foundry/scratch/<session>/comments/774.md

### 4. CLOSE (each has a comment; read them first)
# gh issue close has no --comment-file: comment first, then close. Verified against gh 2.74.0,
# whose only close flags are -c/--comment and -r/--reason.
gh issue comment 731 --body-file .foundry/scratch/<session>/comments/731.md
gh issue close   731 --reason 'not planned'

### 5. REVIEW DEBT — needs a human, no command generated
# PR #688 waiting 41 days on us (published target: 5 days)
```

Rules for the script: `set -euo pipefail`; no destructive verbs beyond `close` and label edits;
no `--force`; comments live in files so they can be read and edited before sending; every close
carries a reason and a comment; must pass `bash -n`.

Never generate: `gh issue delete`, comment deletion, user blocking, branch deletion, or anything
touching repository settings. Those are human actions, listed as recommendations.

## Step 7 — Report

Report these numbers, with the previous sweep's values when available:

- Items processed / total open.
- By outcome: confirmed, needs-info, duplicate, closed, escalated, deferred.
- **Review debt**: count and median age of PRs where the project spoke last.
- Items now unlabelled: must be 0.
- Backlog delta since the last sweep.
- The three items that most need a maintainer decision, by number, with the question each poses.

If the review-debt median exceeds the published response time in `SUPPORT.md`, that is the
headline of the report, above everything else, and it is routed to `community-manager` — no
amount of triage fixes an unstaffed review queue.

## Exit criteria

- [ ] Project rules read and quoted, or their absence reported with `bootstrap-oss` recommended.
- [ ] Live state fetched with `gh`, or degraded mode announced in the report.
- [ ] Queue ordered by the Step-3 priority, and queue sizes reported before processing.
- [ ] Every processed item has exactly one `type:`, `status:` and `priority:` label proposed.
- [ ] Zero items left carrying `status:needs-triage` among those processed.
- [ ] Security-looking items escalated privately and never discussed in a public thread.
- [ ] Every close action has a reason **and** a comment file that states a reopen condition.
- [ ] `triage-actions.sh` passes `bash -n` and contains no destructive verb.
- [ ] `handoff.v1` validates via `mcp__plugin_foundry-core_foundry__contract_validate`.
- [ ] `--apply` was used only after the action list was reviewed; otherwise the run is a dry run
      and says so.

## What this skill deliberately does not cover

- **Fixing anything.** No patches, no PR pushes.
- **Code review.** Delegate to `superpowers:requesting-code-review`; if absent, say review was
  not performed rather than approximating it.
- **Merging or approving PRs.**
- **Changing policy** — stale windows, response times, scope statements belong to
  `community-manager` and `governance-architect`.
- **Handling a vulnerability** beyond routing it — `security-advisory`.
- **Moderation**: bans, comment deletion, lock-downs. Recommended, never executed.
- **Milestone and roadmap planning** — PMO vertical.
- **Repository settings**: branch protection, required checks, auto-merge.

## References

- Per-item protocol: the `issue-triager` agent in this plugin.
- Label seed: `${CLAUDE_PLUGIN_ROOT}/templates/labels.json`.
- `references/gh-recipes.md` — query and batching recipes, including rate-limit handling.
