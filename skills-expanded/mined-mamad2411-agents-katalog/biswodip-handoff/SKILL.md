---
name: biswodip-handoff
description: Write or update handoff.md — goal, current state, active files, changes made, failed attempts, next steps — so the next session resumes without re-deriving context. Use when context is running out, when the user says continue later or starts a new chat, after a milestone, or when asked for a handoff, status file or session summary.
license: Apache-2.0
metadata:
  author: Biswodip Goj
  version: 2.2.0
  homepage: https://github.com/Biswadipgoj
---
# Handoff — write `handoff.md` before the context runs out

A session ends: context fills, a limit is hit, the person leaves. The next session starts blind unless you leave it something. `handoff.md` is that something — the one file the next agent reads first.

## When to write it

- **Proactively**, when roughly 70% of the context window is used, or before a long tool run that might exhaust it.
- When the person says "continue later", "new chat", "you're running out", "hand this over".
- After any milestone: phase complete, finding fixed, release gate run.
- **Update it, never restart it.** It is a living file at the repository root.

## The six sections — exactly these, in this order

```markdown
# Handoff — <project> — <ISO date/time>

## 1) Goal
What we are trying to achieve, in one paragraph, in the user's terms. Include the
acceptance criteria and anything explicitly out of scope. This section changes rarely.

## 2) Current state
Where things actually stand right now: branch, last commit, what builds, what passes,
what is broken. Statuses only from evidence (VERIFIED / PARTIAL / UNVERIFIED / BLOCKED /
OPEN). Include the phase of the lifecycle you are in.

## 3) Active files
The handful of files being worked on, each with one line on its role and its state.
Paths, not descriptions of paths. Mark files that must not be touched.

## 4) Changes made
What has actually been changed, in order, with why. Commands that were run and their
exit codes. Links to evidence under .biswodip/evidence/.

## 5) Failed attempts
What was tried and did not work, and why. This is the most valuable section: it stops
the next session burning context repeating your dead ends. Include the error, not just
"didn't work".

## 6) Next steps
The ordered list of what to do next, specific enough to act on without re-deriving
context. First item should be executable immediately. Include open questions for the
user and anything blocked on them.
```

## Rules

- **Concrete over prose.** `src/api/orders.ts:118 — ownership check added, test missing` beats "working on order security".
- **Failed attempts are mandatory.** If nothing failed, write "none yet" — do not delete the section.
- Record exact commands and exit codes, not impressions.
- Never put secrets, tokens or keys in it. Reference the env var name.
- Keep it under ~400 lines. Prune sections 4 and 5 as work lands; sections 1, 2, 6 stay current.
- The file is committed with the work, so write it for a stranger — assume no chat history at all.
- On resuming: read `handoff.md` **first**, verify section 2 against reality (`git status`, run the build) before trusting it, then continue from section 6. A handoff that disagrees with the repository is out of date — fix it as you go.

## Commands

```bash
node bin/biswodip.mjs handoff init     # scaffold handoff.md with the six sections
node bin/biswodip.mjs handoff update   # refresh branch, commit, status and changed files
node bin/biswodip.mjs handoff show     # print it
```

`update` refreshes the facts it can read from git and leaves your prose alone. Everything the tool cannot know — goal, failed attempts, next steps — is yours to write. Template: `reports/HANDOFF-TEMPLATE.md`.
