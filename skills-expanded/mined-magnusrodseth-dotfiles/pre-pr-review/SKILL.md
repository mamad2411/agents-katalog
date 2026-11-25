---
name: pre-pr-review
description: "Runs adversarial-review and code-review in parallel on one merge-base diff and verifies every finding. Use before opening or updating a PR with a code change, or when a finished task needs review."
---

# Pre-PR review

Two reviews on one diff, with one report. `adversarial-review` asks where the
change breaks. `code-review` asks whether it follows the repo's standards and
does what the issue asked. Run this skill in the main session: both reviews
spawn reviewer subagents, and a subagent cannot spawn its own.

## 1. Pin the scope

Follow `adversarial-review` step 1. Record base SHA, head SHA, dirty or clean,
and `git diff --shortstat <base-sha>...HEAD`. Both reviews use this diff.

Size the diff on two marks:
- **risky**: as `adversarial-review` step 3 defines it.
- **short**: under about 300 changed lines in the shortstat.

## 2. Find the spec

Look for the originating issue in the PR body's closing references, the commit
messages, then the branch name. Fetch it with
`gh issue view <n> --json title,body,comments` and save it to a scratch file.
A spec file the user named counts too.

With no issue and no spec file, the Spec axis is skipped and the report says
"no spec". This skill acts as `code-review`'s issue tracker, so proceed without
asking the user or running `/setup-matt-pocock-skills`.

## 3. Load both skills and write the briefs

Read these files in full:
- `~/.agents/skills/adversarial-review/SKILL.md` and its
  `references/reviewer-prompt.md`
- `~/.agents/skills/code-review/SKILL.md`. Open it by path. In Claude Code the
  name `code-review` also resolves to a built-in bug-review command, which is a
  different tool.

Write each brief by its skill's rules. For `code-review`, the fixed point is
the base SHA and the spec is the scratch file from step 2. Its brief follows the
same isolation as `adversarial-review` step 2: leave out your explanation of the
change, your test results, and which parts you consider risky.

## 4. Spawn every reviewer in one message

Pick the first row that matches. A risky diff always gets four reviewers,
whatever its length.

| Diff | adversarial-review | code-review |
|---|---|---|
| risky | Bugs and Security, one reviewer each | Standards and Spec, one reviewer each |
| not risky, not short | one reviewer with both sections | Standards and Spec, one reviewer each; one reviewer with both briefs when the spec fits on one screen or there is no spec |
| not risky, short | one reviewer with both sections | one reviewer with both briefs, reporting under separate headings |

Why: on [Aprende-AS/Eksamensportalen-Master-repo#205](https://github.com/Aprende-AS/Eksamensportalen-Master-repo/pull/205)
(access checks plus transactions) Bugs and
Security found largely the same defects independently, and Standards and Spec
each caught something no other reviewer did. The Bugs/Security overlap is
redundancy worth paying for only where a missed defect is expensive.

Every reviewer gets a fresh context. In Claude Code, use `Agent` with
`subagent_type: "general-purpose"` and `run_in_background: false`, never
`"fork"`. In Codex, use `spawn_agent` without forking, then wait. Reviewers leave the
checkout untouched: no edits, commits, pushes, deploys, or calls to external
services. Bugs and Security reviewers write and run repros in a scratch
worktree, as `adversarial-review`'s reviewer prompt describes.

## 5. Verify every finding

- Bugs and Security: `adversarial-review` step 4. It requires a red repro for
  Confirmed and a fresh verifier for findings you would reject.
- Standards and Spec: [finding verification](references/finding-verification.md).
  A baseline smell stays a design judgement unless it breaks a documented
  standard.

Verification is done when every candidate has a disposition backed by evidence
or by a named evidence gap.

## 6. Act and report

Fix Bugs and Security findings by `adversarial-review` step 5. Fix confirmed
Standards findings that the diff introduced. Bring a Spec gap that changes scope
to the user before acting on it.

Report:
- a header with base SHA, head SHA, the table row you picked, reviewer count,
  and spec source or "no spec";
- `## Bugs`, `## Security`, `## Standards` and `## Spec`, each a table of
  finding, `file:line`, severity, introduced or pre-existing, verdict, action
  and test, using its source skill's verdicts;
- one closing line with confirmed findings per section.

Keep the four sections separate and rank only within a section. When the change
goes into a PR, `github-pr` records this report as evidence.
