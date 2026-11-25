---
name: adversarial-review
description: "Runs a fresh-context adversarial review of a diff for bugs and security holes, then verifies every finding against the code. Use when asked for an adversarial or security review, or when a diff touches auth, input parsing, secrets, money, shell, SQL or CI."
---

# Adversarial review

The agent that wrote a change shares the reasoning that produced its bugs. This
skill hands the diff to reviewers that have none of that context, tells them to
break it, and then checks each finding against the code. It complements
`code-review` (Standards and Spec axes), and `pre-pr-review` runs the two together.

## 1. Pin the scope

- Resolve the base: the PR's base branch, else the default branch from
  `gh repo view --json defaultBranchRef`. Use `git merge-base HEAD origin/<base>`.
- Record base SHA, head SHA, and whether the tree is dirty.
- The diff is `git diff <base-sha>...HEAD`, plus `git diff HEAD` when dirty.
  Stop and say so when the diff is empty.

## 2. Write the brief

Give the reviewers only:
- the repository path, base and head SHAs, and the exact diff commands;
- the intent of the change in one sentence, taken from the issue, PR or user
  request;
- the path of the repo's `AGENTS.md` or `CLAUDE.md`;
- the matching section of [reviewer prompt](references/reviewer-prompt.md).

Leave out your own explanation of the change, your test results, and which parts
you consider risky. Each of those anchors the reviewer on your view.

## 3. Spawn fresh-context reviewers

A diff is **risky** when it touches access control or auth, transactions or
concurrency, input parsing, secrets, money, shell, SQL, CI or infra.

Run read-only reviewers in parallel. A risky diff gets two: one with the
**Bugs** section, one with the **Security** section. Any other diff gets one
reviewer with both sections.

- Claude Code: the `Agent` tool with `subagent_type: "general-purpose"`, never
  `"fork"` (a fork inherits your context). Send every call in one message with
  `run_in_background: false`.
- Codex: `spawn_agent` without forking the conversation, then wait.

Tell each reviewer to leave the checkout untouched: no edits, commits, pushes,
deploys, or calls to external services. Reviewers write and run repros only in
a scratch worktree, as the reviewer prompt describes. When the diff touches who may read or write what, add the
[authorization-regression](../authorization-regression/SKILL.md) skill to the
security reviewer's brief.

## 4. Verify every finding

Check each finding yourself against the code at the head SHA:

| Verdict | Meaning |
|---|---|
| Confirmed | A repro went red for the claimed reason at the head SHA. A trace alone confirms only when the repro cannot run locally, and the report says why |
| Plausible | The path exists but no repro could run, because it depends on config or input you cannot check |
| Rejected | Name the guard, test or invariant that prevents it |
| Accepted risk | The user decided to live with it, with a reason. Only the user sets this |

Follow [finding verification](../pre-pr-review/references/finding-verification.md)
for each finding: try to refute it, check reachability through real callers,
and treat a reviewer's red repro as a claim to rerun, not as proof. Rerun every
repro yourself in a scratch worktree and confirm it drives the production path.

You wrote the change, so you share its blind spots. Hand a finding to a new
fresh-context verifier when you lean towards Rejected, or when no repro ran.
Give it the finding, the diff commands and the finding-verification file, and
none of your reasoning. Its verdict stands unless you name new evidence.

Judge each finding on the code path alone: severity sounds the same whether the
finding is real or not.

Also mark each finding **introduced** (the diff creates or exposes it) or
**pre-existing** (present at the base SHA). Pre-existing findings go to the
out-of-scope list unless the diff makes them worse.

## 5. Act and report

- Fix confirmed, introduced findings. List the rest for the user.
- Fix the root cause, not the symptom: a SQL injection gets a parameterised
  query, not one escaped string. Grep for the same pattern in sibling code paths
  and fix every instance the diff touches. Ask how the fix could be bypassed.
- Prove each fix with a regression test that goes red at the head SHA and green
  after the fix. Use the `evidence` skill to capture both runs. When no test is
  feasible, say why in the report.
- The judge of a fix is never its author. Re-check fixes with a new fresh-context
  reviewer, scoped to the fix diff and the findings it claims to close. A finding
  counts as addressed only when a changed line removes it. Stop after two rounds.
- Report a table: finding, `file:line`, severity, introduced or pre-existing,
  verdict, action, test. Add base and head SHA and the number of reviewers.
- When the change goes into a PR, `github-pr` records this report as evidence.
