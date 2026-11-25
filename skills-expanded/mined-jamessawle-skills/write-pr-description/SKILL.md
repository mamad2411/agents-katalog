---
name: write-pr-description
description: Use this skill whenever someone asks to write, draft, generate, or produce a PR description, pull request body, or PR summary for a branch that does not yet have one. Focuses the description on the reasoning behind the change — the problem being solved, why this approach was chosen over alternatives, what trade-offs were accepted, and how to verify — rather than restating the diff. Gathers context from the linked issue or ticket, the branch's commit messages, and follow-up questions to the user when context is missing. Trigger for "write a PR description", "draft the PR body", "generate PR description", "PR summary", "describe this PR", "help me write the PR", or any request to produce description text for a pull request before it is opened. Do not trigger for reviewing an existing description, opening the PR itself, or summarising a merged PR.
license: MIT
compatibility: Requires git access to the branch being described. Optionally uses the GitHub CLI (gh) to fetch linked issue bodies when commit messages reference an issue.
allowed-tools: Bash, Read
argument-hint: "[branch-name]"
metadata:
  author: jamessawle
  version: "1.0"
---

# Write PR Description

Produce a pull request description focused on the reasoning behind a change rather than a restatement of the diff.

## Arguments

- `$0` (optional) — Branch name to describe. Defaults to the current branch.

If no branch is supplied and the working directory is not a git repository, stop and ask which branch to describe.

## Principles

1. **Reasoning over restatement.** Every sentence should add something the diff cannot show. If a sentence would still be true after `git revert`, delete it.
2. **Lead with the problem.** The reader should understand why the PR exists before they read what it does.
3. **Make trade-offs explicit.** Name the alternative rejected and why. "Considered X, chose Y because Z" is more useful than describing Y alone.
4. **Write for the future reader.** Not the current reviewer (who has the diff), but someone hunting for context six months later.
5. **Be honest about risk.** Surface follow-up work, known gaps, and migration concerns; give the reviewer something concrete to verify.
6. **Match length to substance.** A one-line fix gets a one-line description. Padding small PRs with ceremonial sections trains readers to skim past structure when it matters.

Use neutral framing ("X was considered, rejected because…") rather than first-person voice — a PR description should outlive any individual author.

## Workflow

### Step 1: Identify the branch and its base

Determine the branch (`$0` or current) and base. Default base order: `origin/HEAD` symbolic ref > `main` > `master`.

```bash
git rev-parse --abbrev-ref HEAD
git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null || true
```

If the branch has no commits beyond the base, stop and report that.

### Step 2: Gather context

Run these in parallel; they are independent.

```bash
git log --no-merges --format='%H%n%s%n%b%n---' <base>..<branch>
git diff --stat <base>..<branch>
git diff --name-status <base>..<branch>
```

Commit messages are the richest free source of reasoning. The diff stat is for sizing the description and spotting whether the PR touches docs, tests, config, or production code — do not paste the diff into the description.

Scan commit subjects, bodies, and the branch name for linked issues (`#123`, `closes #123`, `PROJ-789`). For GitHub-style references, fetch with `gh issue view <number> [--repo <owner/repo>] --json title,body,labels` if `gh` is available. For Jira-style references, note them for the user but do not attempt to fetch.

Treat issue bodies as input, not as the final description. Issue bodies describe the problem; PR descriptions explain the resolution.

### Step 3: Identify gaps

Mentally answer:

1. What problem motivated the change?
2. Why this approach? What alternatives were considered?
3. What trade-offs were accepted?
4. How should a reviewer verify it works?
5. Is anything intentionally deferred?

If commits and the linked issue answer a question, use that material. For questions that remain unanswered, decide whether the answer is inferable from the diff with high confidence (a one-line null-check fix has an obvious "why") or whether to ask.

### Step 4: Ask only for genuinely missing context

Skip questions the existing context already answers. Group remaining questions into a single message rather than asking serially. Cap at three per round. For single-line fixes, dependency bumps, or docs typos, skip this step entirely.

Typical questions, in priority order:

1. **The problem** — what prompted this change?
2. **Alternatives** — what other approaches were considered, and why ruled out?
3. **Risk areas** — where would the author most want a reviewer to push back?
4. **Verification** — how was this tested?

### Step 5: Draft

There is no required template. Use sections only when they carry weight. A typical medium-sized PR uses:

- An opening paragraph (1–3 sentences) stating the problem and chosen approach, with no heading.
- `## Why`, `## Approach`, `## Trade-offs` or `## Notes`, `## How to verify` — included only when each has something substantive to say. Drop any section that would only contain a trivial line.

If a linked issue exists, end with `Closes #N` so the issue auto-closes on merge.

Before drafting, read the worked example closest to this PR's archetype (paths relative to this SKILL.md). Read one, not all three:

- `references/bug-fix.md` — bug fix where the choice of fix is non-obvious
- `references/trivial.md` — single-line fix, typo, or dependency bump where ceremony would be noise
- `references/refactor.md` — refactor where the "why" is the entire point

Use the example as a structural model — do not copy phrasing. If the PR straddles archetypes (e.g. a bug fix that also restructures a module), read the closest match and expect to deviate.

### Step 6: Present

Present the draft as plain markdown text in the assistant message — do not write it to a file unless asked. Do not open the PR. This skill produces description text only; opening the PR is a separate action.
