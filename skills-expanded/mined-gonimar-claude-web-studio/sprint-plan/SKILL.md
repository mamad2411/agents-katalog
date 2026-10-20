---
name: sprint-plan
description: "Plans a sprint — goal, capacity, story selection by priority and dependencies, risks, QA plan link; triages the dependency-update queue (Dependabot/Renovate PRs: green patch/minor merged at sprint start, majors become stories); writes production/sprints/sprint-NN.md and roadmap markers. Use at sprint start."
argument-hint: "[sprint number] [--days N]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Write, Edit, AskUserQuestion
---

# Sprint Plan

Reply in the project conversation language (CLAUDE.md → Language); code, identifiers, paths and commit messages stay in English.

Templates (`.claude/docs/templates/`): `sprint-plan.md`, `roadmap.md`. In the commands below, `<hooks>` is `.claude/hooks/` in copy mode and `${CLAUDE_PLUGIN_ROOT}/hooks/` in plugin mode.

## Phase 1: State
1. **Arguments**: the sprint number `NN` (default: the last sprint in `production/sprints/` + 1); `--days N` is read as the sprint length in working days — the same value step 6 would otherwise ask for, so with it only hours per day and the start date are asked. It is never a deadline or a number of stories.
2. **The previous sprint is closed**: `Status: closed` in its `production/sprints/sprint-NN.md` header. A file written before 0.13 has no `Status:` line: it counts as closed when its roadmap block is folded in `<details>`, open otherwise (`/migrate sprints` adds the line). Open → stop with `BLOCKED (sprint NN open — run /retrospective NN first)` and write nothing: the retrospective is the only writer of a sprint's close, and a plan that folds the previous block as a side effect leaves sprints open and stories counted in two blocks. A project with no sprint file yet is not blocked.
3. **Ready stories** (`production/stories/**`). None → stop with `BLOCKED (no Ready stories — run /create-stories)` and write nothing.
4. **Read**: the roadmap (priority and blocker markers — the stories `/retrospective` carried back to the Backlog are there with their `🔥`/`⛔` intact and compete like any other), the last sprint (retro actions), `production/findings.md` (open BLOCKING findings and their stories).
5. **Backlog**: `production/backlog.md` → one line `Backlog: N open ideas — /backlog review`. An idea enters a sprint only after promotion, never from here.
6. **Capacity and dates**: ask now — days (unless `--days` gave them), hours per day, start date. Parameters are asked here, before any gate, never in the same message as one (rule 7: one turn, one gate).
7. **Calibration**, one sample worded identically in both skills: the **last six closed stories of the roadmap** that carry both `~Nh` and `⏱ Nh`, whichever sprint they belong to. `/retrospective` prints this same rolling ratio next to its own sprint-only one and labels which is which; two skills quoting different numbers under the same name is how a plan stops being trusted.
   - Ratio = Σ⏱ / Σ~, never rounded towards a nicer plan.
   - Three or more such stories → apply it to this sprint's estimates (calibrated estimate = `~Nh` × ratio) and show one line: `Calibration: ratio R over N stories — capacity fits ~X h of estimates`.
   - Fewer than three → "insufficient data, estimates taken as written".

## Phase 2: Dependency queue
1. **Precondition**: `gh` exists and the repository has `.github/dependabot.yml` or `renovate.json`. Otherwise one line — "no update bot configured — `/dependency-audit` sets one up", or "no `gh` — dependency queue not checked" — and on to Phase 3.
2. **List**: `gh pr list --state open --author app/dependabot --json number,title,createdAt,mergeable,statusCheckRollup` (Renovate: `--author app/renovate`). An empty queue is one line; go on to Phase 3.
3. **Classify every PR** from the command output, never from memory or the title alone:
   - **green and safe** — `mergeable: MERGEABLE`, every check `SUCCESS` or `SKIPPED`, and the bump is a patch/minor of a library or any CI-action bump. A merge candidate at sprint start, not a story.
   - **major** — the first version component changes in the title (`from 4.2.2 to 7.0.1`) or the PR body names a breaking change. A story (`chore(deps)`, size S/M, layer from the manifest's directory) or deferred with a written reason in the plan; never merged here, never left open unmentioned (`stack-reference/tooling-devops.md`, Renovate/Dependabot).
   - **red or conflicting** — a failing check or `CONFLICTING`. Stays open, named under risks, never merged.
4. **Show the queue** as a table: number · package · bump · checks · class · action.
5. **Record the gate** before asking: `<hooks>session-state.sh set Task "/sprint-plan Phase 2" Gate "/sprint-plan Phase 2: merge #…?"`. A session that resumes with this `Gate:` open continues here: it merges or not, and never implements a story (rule 7).
6. **Ask**, alone in its message, one `AskUserQuestion`: merge the green safe PRs now (Recommended) · turn them into one story · leave them.
7. **After the answer**: clear the gate (`<hooks>session-state.sh set Gate "—"`). On "merge": `gh pr merge <n> --squash`, one PR at a time, with the output in the message.
8. **Default-branch CI.** After the batch, `gh run list --branch <default> --limit 1`: the default branch's CI should be green before the first story branch starts. This skill **reports** that state — green, red or not run — in the message and, when red, under the plan's risks with the failing job; it does not enforce it: nothing here blocks the plan. The check that holds a story branch back on a red run lives in `/dev-story` Phase 3 (the branch step runs the same `gh run list --branch <default> --limit 1` before creating the branch); fixing it is toolchain work (`/hotfix --chore`), named in the plan.

## Phase 3: Selection
1. **The sprint goal** as one verifiable statement.
2. **Stories** by priority and dependencies, within capacity minus a 20 % buffer, using the calibrated estimates when the ratio applies. First the one that removes the biggest risk.
3. **Blockers and external dependencies** (the roadmap's ⛔ markers) are named explicitly.
4. **Open BLOCKING findings**: each one is either in the sprint (its story) or deferred with a written reason in the plan — never absent.
5. **Stories born from major bumps** compete on priority like any other. One that unblocks the toolchain or the runner (a Node 24 action, a new Go toolchain) goes before the stories that need it.

## Phase 4: Write
Its own turn — never on the merge answer.
1. **Show the plan** rendered (rule 7), from `sprint-plan.md`: the header with dates, capacity, review mode and the calibration ratio applied; the stories; risks and blockers; the `## Dependency updates` section (what was merged, which majors became stories, what was deferred and why, what stays open red).
2. **Gate**, one `AskUserQuestion`: "May I write `production/sprints/sprint-NN.md` and update the roadmap?" — write (Recommended) · show the draft/diff first · not now.
3. After the "write" answer: `touch .claude/.write-consent` (rule 7 — the consent-guard hook checks the marker).
4. **Write** `production/sprints/sprint-NN.md` with `Status: active` in its header.
5. **Update the roadmap** per `templates/roadmap.md`:
   - **Move** the selected stories: add them under a `## Sprint NN (YYYY-MM-DD → YYYY-MM-DD) — goal` subheading **and remove them from the Backlog block in the same edit**, never leaving them in both. A story counted twice makes every later count wrong.
   - Recalculate the `<summary>` count of each block.
   - The sprint is the heading, never a `📅 sprint-NN` marker; `📅` carries ISO dates only.
   - Mark the active story ⏳ and the first one 🔥.
   - Markers inline in the legend's order, IDs as inline links, no prose ordering.
   - Refresh the `Updated:` line.
   - The previous sprint's block is already folded by `/retrospective`; this skill never edits it.
   - Add a row for the new sprint (`⏳ … active`) to the roadmap's `## Docs` → *production/sprints/* block and recalculate its `<summary>` count.
6. **Close the write with the numbers**: `Backlog: N → M, Sprint: 0 → K, overlap none`.

## Phase 5: Commit (documents lane)
Right after the write, one commit gate (rule 7 (4), `.claude/docs/git-workflow.md` § Documents): one `AskUserQuestion` offering `docs: sprint NN`, staging exactly the written files — `production/sprints/sprint-NN.md` and `production/roadmap.md`. Record the gate before asking — `<hooks>session-state.sh set Gate "/sprint-plan Phase 5: commit?"` — and clear it after the answer (`<hooks>session-state.sh set Gate "—"`).
- On the default branch when no story work is in progress.
- When HEAD is a story branch, name it and offer: switch to the default branch and commit there (Recommended — a pipeline-wide document) · commit here (the document belongs to this story) · leave uncommitted.
- Code, configs, workflows and scripts never ride the `docs:` commit; the Phase 2 merges are their own commits on the default branch already.

Nothing is committed without the answer.

Verdict: `READY` | `BLOCKED (sprint NN open — run /retrospective NN first)` | `BLOCKED (no Ready stories — run /create-stories)`.

Next step — one `AskUserQuestion`: `/qa-plan NN` (Recommended) · `/dev-story` directly · revise the sprint. On `BLOCKED`: the command the verdict names (Recommended) · stop here.
