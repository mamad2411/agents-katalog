---
name: arc-bug-fixer
description: >
  Picks up a bug ticket filed by arc-bug-finder (in GitHub Issues, GitLab, or
  Linear), critically reviews and re-validates it, then implements, verifies, and
  ships the fix — branch, conventional commit, PR, and ticket update. Reviewing
  is the core competency: it re-reproduces the defect, confirms the cited root
  cause still exists, and chooses the best fix rather than trusting the ticket
  blindly. Delegates plan formatting to arc-planning-work,
  commit/PR mechanics to arc-conventional-commits / arc-git-pr-check.
  TRIGGER when: user asks to fix/resolve/implement a filed bug, points at a bug
  ticket or issue number, says "fix this bug", "resolve W-######", or "work the
  bug backlog".
  DO NOT TRIGGER when: user is reporting a NEW bug or asking "why is this
  happening" (use arc-bug-finder to research + file first), or planning greenfield
  features (use arc-defining-work).
---

# Bug Fixer

The implementation counterpart to [arc-bug-finder](../arc-bug-finder/SKILL.md).
Where the finder **researches and files** a bug, the fixer **reviews, resolves,
and ships** it.

The input is a **filed bug ticket**; the output is a **merged-ready PR** that
closes that ticket, with the ticket updated to reflect the resolution.

This skill modifies product code — but only after it has independently confirmed
the bug is real and the cited root cause is correct. A ticket is a hypothesis, not
a work order.

## Operating Principles

- **Review before you repair.** The finder's root cause and recommended fix are a
  starting point, not gospel. Re-reproduce the defect and re-confirm the root cause
  at `file:line` yourself before changing a line. Findings drift: the code may have
  moved, the bug may already be fixed, or the recommended fix may be wrong.
- **Fix the cause, not the symptom.** Patch where the defect originates, not where
  it manifests. If the ticket conflated the two, correct it.
- **Every fix is verified.** The bug is not "fixed" until you have reproduced it
  failing, applied the change, and reproduced it passing — plus a regression test
  that would have caught it.
- **Smallest correct change.** Minimize blast radius. Match the surrounding code's
  conventions, naming, and patterns. No drive-by refactors in a bug PR.
- **One ticket, one PR.** Cross-link if the fix reveals adjacent defects; file the
  new ones via [arc-bug-finder](../arc-bug-finder/SKILL.md) rather than smuggling
  unrelated fixes into this PR.

## Workflow Overview

```
1. Intake the ticket          → fetch the bug from its tracker (GitHub|GitLab|Linear)
2. REVIEW & validate          → re-reproduce, re-confirm root cause, vet the fix
   ├─ valid + cause confirmed  → continue
   ├─ already fixed / stale    → close with evidence, stop
   └─ not a bug / can't repro  → bounce back with findings, stop
3. Decide the fix             → adopt or improve the recommended option
4. Plan (for non-trivial)     → ordered tasks mapped to acceptance criteria
5. Branch + implement         → smallest correct change, repo conventions
6. Verify                     → repro gone, regression test added, suite green
7. Ship                       → conventional commit, PR linking the ticket
8. Update the ticket + report → status, PR link, what changed and why
```

## Step 1: Intake the Ticket

Identify the bug to fix and pull its full body. Detect the tracker the same way
arc-bug-finder does (probe `git remote -v`, `gh auth status`/`.github/`,
`.gitlab-ci.yml`/`glab`, `LINEAR_API_KEY`/Linear MCP). Confirm if ambiguous.

| Tracker | Fetch the ticket |
|---------|------------------|
| GitHub  | `gh issue view <number> --comments` (read body **and** any plan comments) |
| GitLab  | `glab issue view <iid>` or `GET /projects/:id/issues/:iid` |
| Linear  | Linear MCP / GraphQL `issue` query by identifier |

If the user gives only a symptom and no ticket number, **search for the ticket**
(error string / route / W-number) before assuming none exists. If genuinely none
exists, this is intake, not a fix — hand off to
[arc-bug-finder](../arc-bug-finder/SKILL.md) first, then return here.

Parse the arc-bug-finder body into its parts — you will check each: **Summary**,
**Steps to Reproduce**, **Acceptance Criteria** (verifiable checklist), **Root Cause**
(`file:line` + originating commit), **Recommended Fix** (ranked options),
**Research Notes**, **Blast Radius**.

## Step 2: Review & Validate (the core competency)

Do **not** skip this even when the ticket looks airtight. Produce a short
**review verdict** before touching code.

1. **Re-reproduce.** Follow the Steps to Reproduce exactly. Run the failing test,
   or write a minimal repro (do not commit it). Confirm the symptom is real,
   current, and deterministic on the current default branch. If it does not
   reproduce, find out why before proceeding.
2. **Re-confirm the root cause.** Open the cited `file:line`. Does the described
   defect actually exist there *now*? Code drifts after filing — re-anchor by
   grepping the error string / symbol if the line moved. Trace the path yourself
   (component → handler → service → data) and verify the cause produces the symptom.
3. **Check it isn't already resolved.** `git log` since the ticket was filed; search
   merged PRs and the originating commit (`<sha>`) for a later fix. If fixed, go to
   *Already-fixed* below.
4. **Vet the recommended fix.** Is option A actually correct and lowest-risk? Does a
   dependency upgrade vs. patch vs. workaround still apply? Consult the framework's
   skill (Next.js, Convex, Clerk, Stripe, Vercel, etc.) and official docs before
   committing to an approach. You may override the ticket's recommendation — record
   why.
5. **Confirm severity & scope.** Re-check blast radius: who else calls the broken
   code, and is the data/role/viewport dependency as stated? Adjust severity if the
   ticket over- or under-rated it.

Write the verdict in the ticket-update buffer:

```
REVIEW VERDICT
- Reproduced: yes/no (how)
- Root cause confirmed: yes/no — now at `path:NN` (moved from `path:MM`)
- Already fixed: no | yes (PR #..)
- Fix approach: adopt Option A | switch to <X> because <reason>
- Severity: confirmed S2 | adjusted S2→S3
```

### Branch points

- **Already fixed / cannot reproduce on current main.** Do not write code. Comment
  on the ticket with the evidence (commit/PR that fixed it, or repro attempt), set
  it to the tracker's closed/won't-fix state, and report. Ask the user before
  closing if there is any doubt.
- **Not a bug / works as designed / invalid.** Bounce it back: comment with your
  findings, recommend a label like `wontfix`/`invalid`, and stop. Do not force a
  fix for a non-defect.
- **Real but root cause wrong.** Correct the Root Cause section on the ticket
  (comment), then proceed with the true cause.

## Step 3: Decide the Fix

State the chosen approach in one or two sentences: what changes, where, and why it
is the smallest correct change. If you departed from the ticket's recommendation,
say so and why. Note the regression test you will add.

## Step 4: Plan (non-trivial fixes only)

A one-line fix needs no plan — go to Step 5. For multi-file or risky fixes, produce
an ordered task plan mapped to the ticket's acceptance criteria and post it to the
ticket:

- GitHub / Linear / Agile Accelerator / PRD → [arc-planning-work](../arc-planning-work/SKILL.md)
  (GitHub: `gh issue comment` with the plan per `GITHUB_MODE.md`).

Reuse the existing `**Branch:** feat/...` convention from those skills, but for a
defect prefer a `fix/` branch (see Step 7).

## Step 5: Branch & Implement

1. **Branch** off the up-to-date default branch:
   `fix/W-XXXXXX-<short-slug>` (use `feat/` only if the fix is really an enhancement).
   If you are already on a clean feature branch for this ticket, reuse it.
2. **Implement the smallest correct change** at the confirmed root cause. Follow the
   repo's layered architecture and naming. Read neighboring code first so the change
   reads like it belongs.
3. **Touch only what the fix needs.** No reformatting, no unrelated renames. If you
   spot an adjacent defect, note it for a separate ticket — do not fix it here.
4. For Salesforce repos, follow the `sf-2gp-pipeline` skill's conventions (virtual
   methods, DI, `@TestVisible` setters, `with sharing`); for web repos, follow the
   project's framework skill.

## Step 6: Verify the Fix

The fix is not done until all of these hold — show the evidence:

1. **Repro now passes.** Re-run the exact reproduction from Step 2; the symptom is
   gone.
2. **Regression test added.** Add a test that fails on the old code and passes on the
   new — ideally encoding the ticket's acceptance criteria. This is
   mandatory; a fix with no test guarding it can silently regress.
3. **Existing suite is green.** Run the project's test commands (e.g. `sf apex test
   run --wait 10 --code-coverage`, `pnpm run test:unit`, relevant E2E) and lint.
   Quote the result. Keep org-wide coverage above the project threshold.
4. **No new breakage in the blast radius.** Exercise the other call sites the review
   flagged.
5. **Visually confirm UI fixes.** For a UI defect, run the app / use the `dogfood`
   skill or agent-browser to confirm the screen now renders correctly, and capture
   an after-screenshot for the PR/ticket.

If any check fails, return to Step 5. Never ship on a red suite — report the failure
instead.

## Step 7: Ship

1. **Commit** with Conventional Commits per
   [arc-conventional-commits](../arc-conventional-commits/SKILL.md):
   `fix: <summary> (W-XXXXXX)` — `fix:` for a defect (patch), `feat:` only if it was
   really an enhancement. Squash & merge is the project default.
2. **Open the PR** via [arc-git-pr-check](../arc-git-pr-check/SKILL.md)
   (`bin/run.sh --type fix --summary "<...>"`), which commits-if-needed, pushes,
   creates the PR, and enables squash auto-merge. It also guards against committing
   on the default branch.
3. **Link the ticket from the PR** so it auto-closes on merge: GitHub `Fixes #<n>`
   / `Closes #<n>` in the PR body; GitLab `Closes #<iid>`; Linear — put the issue
   identifier (e.g. `WSM-000079`) in the PR title/branch for magic-word linking.
4. **PR body** = the fix in brief: root cause (with `file:line`), what changed, how
   verified (tests + before/after), and any follow-up tickets filed.
5. Do **not** merge or deploy unless the user explicitly asks. Deploy Convex/web only
   from merged `main`, never a feature branch.

## Step 8: Update the Ticket & Report

Update the source ticket and then report to the user.

**On the ticket** (comment + state change):
- Post the **review verdict** and the **resolution**: root cause confirmed, fix
  applied, PR link, tests added.
- Move to the in-review/done state appropriate to the tracker (GitHub: rely on
  `Fixes #` to close on merge, or move on the project board; GitLab: same; Linear:
  set state to In Review / Done).
- Attach the after-screenshot for UI fixes.

**To the user** (concise):
- Ticket ID / W-number and one-line **review verdict** (was it valid?).
- **PR URL** and branch.
- One-line **root cause** and **what changed** (`file:line`).
- **Verification**: tests added + suite result.
- Any **additional defects** discovered and filed separately.

## Cross-Skill Delegation

| Need | Delegate to |
|------|-------------|
| Fetch / research the bug if no ticket exists yet | [arc-bug-finder](../arc-bug-finder/SKILL.md) |
| Implementation plan on GitHub / Linear / AA / PRD | [arc-planning-work](../arc-planning-work/SKILL.md) |
| Commit message convention | [arc-conventional-commits](../arc-conventional-commits/SKILL.md) |
| Commit + push + PR + auto-merge (GitHub) | [arc-git-pr-check](../arc-git-pr-check/SKILL.md) |
| GitLab MR + CI/CD mechanics (`glab`, `.gitlab-ci.yml`) | [arc-gitlab-glab](../arc-gitlab-glab/SKILL.md) |
| Fixing several independent bugs at once | `arc-parallel-implement` skill (one branch/PR each) |
| Salesforce deploy + test loop | `sf-2gp-pipeline` / `deploy-and-test` skills |
| Confirm a UI fix in the running app | `dogfood` skill or agent-browser |

## Working a Backlog

When asked to "work the bug backlog" or fix several tickets:
- List open bugs (`gh issue list --label type:bug --state open`, GitLab/Linear
  equivalents) and triage by severity (S1 → S4) then priority.
- Fix them one ticket / one PR at a time. For independent bugs across different
  files, the `arc-parallel-implement` skill can fan out — each gets its own branch,
  commit, and PR. Do not batch dependent or same-file fixes in parallel.

## Rules

- **Review every ticket before fixing** — re-reproduce and re-confirm the cited
  root cause at `file:line`. A ticket is a hypothesis.
- Never ship a fix without a **regression test** and a **green suite** — quote the
  evidence.
- Smallest correct change; fix the cause, not the symptom; no unrelated refactors.
- One ticket → one PR; cross-link related defects, file new ones via arc-bug-finder.
- Match the repo's branch/commit/label and ticket-numbering conventions; link the
  ticket so it closes on merge.
- Do not merge or deploy unless explicitly asked; deploy only from merged `main`.
- Never commit or expose API tokens (`LINEAR_API_KEY`, `GITLAB_TOKEN`); read from
  env and delete temp files holding secrets or screenshots.
