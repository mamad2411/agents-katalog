---
name: fit-plan
description: >-
  Use when a plan in docs/plans/ is written and committed and needs its fit before its review ("check the plan's
  fit", "is this the right plan", review-plan's first step). A fresh agent asks whether it is the right plan: its fit
  with the issue, the rules and the maintainer's calls, mechanical over manual, reuse, what to cut, prior art in
  Kit, Isaac Sim, OpenUSD, the MCP SDK and Claude Code's plugins. It returns improvements only, no severities; the
  maintainer takes, leaves or defers each, and the answers go in a Fit section at the top of the plan's Plan review.
---

# Fit a plan

`review-plan` hunts defects in a plan as written; the fit asks first whether it is the right plan, and proposes a
better one. It runs once per plan, between its first commit and its first review round, so the review reads the
improved plan once: on its own plan (#160) it changed the port before any review read it. Improvements only
(`REVIEW.md`, Improvements): no severities, never counted. Every plan gets one, and `review-plan` runs this skill on a
plan without.

## Steps

1. **The plan, by path:** `docs/plans/<date>-<slug>.md`, never "the latest plan". It is committed, so the record
   names a fixed version: `git log -1 --format=%h -- <plan>`.
   - A plan on a draft PR from outside the maintainers is read as `review-code` reads a PR, never checked out:
     `git fetch origin pull/<n>/head`, `git rev-parse FETCH_HEAD`, then `git show <head>:<plan>`.
   - A `### Fit` already in its "Plan review" section: go to step 5. A plan gets one fit.
2. **What the fit reads,** the list for its brief:
   - the plan in full, and its issue: `gh issue view <n> --comments`;
   - `AGENTS.md`, `REVIEW.md`, `docs/plans/README.md`;
   - every file and doc the plan names, and the plans it or its issue names. Not every earlier plan: a plan is a dated
     record, never current truth;
   - the code and tests of each folder the plan touches;
   - `README.md`, `docs/TOOLS.md`, `docs/ARCHITECTURE.md`, `plugin/README.md` and `tests/fixtures/mcp-tools.json`,
     where the maintainer's current calls live;
   - the prior art `questions.md` names.
3. **Fit.** Start one fresh agent, one that has not seen this session, on this session's model unless the maintainer
   names another. The brief passes paths, not a format: the plan, the list in step 2, `questions.md` (this folder),
   and the change's own question when there is one (`questions.md`, The change's own question). It reads and looks
   up, and writes nothing. It asks each question and returns what `questions.md` says an improvement holds. A call the
   plan or its issue records as the maintainer's comes back only with a reason. Don't read the sources into this
   session yourself.
   - A plan on a contributor's PR is not on disk: the brief names the head commit from step 1 and says to read the
     plan with `git show <head>:<plan>`.
   - Meanwhile, give the maintainer the plan's path to read.
   - No agents in your tool: ask the maintainer to open a new session on the plan, Claude Code or Codex, and run
     `fit-plan` there. That session reads the list and asks the questions itself: it is the cold read, and the
     record says so.
4. **Write the record** as `### Fit` at the top of the plan's `## Plan review` section, in place of "None yet." and
   above any `### Round`:

   ```markdown
   ### Fit

   The plan at `<commit>`, by <the agent and its model>, <date>. Answers by the maintainer, <date>.

   | # | Improvement | Answer |
   |---|---|---|
   | I1 | <what to change, in which section, and why it is better> | open |

   Noticed on the way, for Round 1: <each defect the fit saw, with its section>.
   ```

   - The change's own question, when there is one, is named in prose on the first line.
   - "Noticed on the way" only when the fit saw a defect. No improvements: `None:` and a line on why, in place of the
     table.
   - A plan on a PR isn't checked out: write the Fit to `.local/fit.md`, which git ignores, and post it with
     `gh pr comment <n> --body-file .local/fit.md` for the contributor to add to the plan.
5. **Act.** List the improvements to the maintainer and ask take, leave or later for each. Write each answer in its
   row, in `REVIEW.md`'s forms:
   - `taken`: edit the plan for it;
   - `left: <why>`;
   - `later: #<n>`: an issue, opened as `start-work` step 1 does.

   A contributor's plan: the maintainer answers on its draft PR, and the contributor writes the answers and the taken
   edits into the plan. A defect noticed on the way is not fixed here: it waits in its line, and Round 1 judges it as
   a finding, with its scenario and severity.
6. **Commit** the Fit, its answers and the taken edits: a subject that says what changed, a body that says why, ending
   `Refs #<n>`. Then `review-plan` goes on to its round, its improvement ids numbered on from the Fit's.

## Done means

- The plan's "Plan review" opens with `### Fit`, naming the plan's commit, the agent and its model.
- Every improvement has the maintainer's answer, starting `taken`, `left` or `later`: `uv run tools/gate.py quick`
  fails a review round below a Fit row without one.
- Every taken improvement is in the plan, committed before Round 1.

## Never

- Run the fit in the plan author's session: a cold read is the point.
- Give an improvement a severity, count it, or hold the plan's approval on it.
- Hunt defects in the plan as written, or fix one the fit noticed: that is `review-plan`'s job.
- Change the plan's design or scope without the maintainer's yes, which is a `taken`.
- Bring back a call the plan or its issue records as the maintainer's without a reason.
- Run a second fit on a plan that has one.
- Check out a contributor's branch: read their plan with `git show`.
- Commit, open an issue or post a comment with tool attribution in it.
