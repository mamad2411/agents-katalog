---
name: team-game
description: "Delivers a playable web-game slice: game-concept check → engine ADR → branch → simulation, rendering and UI overlay in parallel, optional multiplayer server → frame-budget measurement → accessibility settings → commit and PR → review. Use for 'build the prototype', 'make it playable', 'game feature F-NNN'."
argument-hint: "[prototype | feature F-NNN]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, Skill, AskUserQuestion
model: opus
---

# Team: Game

Reply in the project conversation language (CLAUDE.md → Language); code, identifiers, paths and commit messages stay in English.

File writes and any mutation (git, deploy) happen only after an explicit "May I write?" / "Proceed?" — each one `AskUserQuestion` (proceed (Recommended) · show the draft/diff first · not now) → "yes". After the "write" answer: `touch .claude/.write-consent` (rule 7 — the consent-guard hook checks the marker). A partial report on BLOCKED at any stage is mandatory.

**Consent for delegated work is collected by this skill.** A subagent spawned through `Task` cannot ask the user. Before each `Task` batch, the "Proceed?" question names the agents and the files each will create or change; that answer covers those files. A specialist that needs to go beyond its brief (another file, a new dependency, a protocol or schema change) stops and reports it, and the parent asks.

Agents below are spawned with a studio `subagent_type`: `web-studio:<name>` in plugin mode, `<name>` in copy mode. Commands are `/web-studio:<name>` in plugin mode and `/<name>` in copy mode; a bare `/code-review` in plugin mode runs Claude Code's built-in review, not the studio's (coordination-rules § Subagents). **This skill runs another studio skill through the `Skill` tool**, one skill after another; the called skill keeps all of its phases and gates, and its verdict comes back as text this skill quotes. `‖` below means one `Task` batch of agents launched together — never two skills at once. In the commands below, `<hooks>` is `.claude/hooks/` in copy mode and `${CLAUDE_PLUGIN_ROOT}/hooks/` in plugin mode.

## Phase 1: Readiness
`docs/specs/game-concept.md` (missing → `/game-concept` through the `Skill` tool and read its verdict line: continue only on `APPROVED` or `GO`; `NEEDS REVISION`, `NO-GO` or `PIVOT` → stop with `BLOCKED (stage 1: game-concept <verdict>)` and the partial report); the engine ADR (missing → `/architecture-decision` through the `Skill` tool: continue only on `ACCEPTED`; `PROPOSED`, `NEEDS REVISION` or `REJECTED` → `BLOCKED (stage 1: architecture-decision <verdict>)` — no slice is built on an undecided engine); **budgets** in technical-preferences (frame time, draw calls, memory, load on 4G emulation) — quote them, they are the yardstick of Phase 4; `.claude/docs/git-workflow.md`. **Scope**: `prototype` → branch and commit scope `prototype`; `feature F-NNN` → the story `S-NNN` when the slice is one story, else `F-NNN`. **Multiplayer** (the concept or the feature is networked) → the protocol comes first: `api-designer` in Phase 3 before `multiplayer-engineer` starts.

## Phase 2: Branch
Per `.claude/docs/git-workflow.md` (one story = one branch = one PR), as `/dev-story` Phase 3:
1. One `AskUserQuestion`: branch `feat/<scope>-<slug>` from an up-to-date default branch and start (Recommended) · stay on the current branch `<name>` (it already belongs to this slice) · stop. The "start" answer is the consent for the branch and the session-state update.
2. `git fetch origin`. If the current branch is the default branch, or is already merged into `origin/<default>` (`git merge-base --is-ancestor HEAD origin/<default>`): `git switch <default> && git pull --ff-only origin <default>`. Never continue on a merged branch.
3. `git switch -c feat/<scope>-<slug>`.
4. Record the start through the studio's writer: `<hooks>session-state.sh set Task "<slice> …" Branch feat/<scope>-<slug> Next "/code-review --diff"`.
5. **Stamp the story cards** (`feature F-NNN` scope; the `prototype` has no card): on the metadata line of every story card the slice implements (`production/stories/F-NNN/S-NNN-*.md`), set `Status: In Progress` and write `Started: YYYY-MM-DDTHH:MM` with the actual time (as `/dev-story` Phase 3 step 5 — `/story-done` measures the duration from it and refuses a card that never left `Ready`). The "start" answer of step 1 covers these edits; the cards ride the slice's `feat(<scope>)` commit in Phase 5 (staged by name), so the stamp never lands on the default branch by itself.

## Phase 3: Parallel implementation
`web-game-engineer` (simulation, loop, input, audio, saves) ‖ `threejs-engineer` or `web-game-engineer` (rendering) ‖ `angular-engineer`/`vue-engineer` (UI overlay/menus from the UX spec) ‖ `multiplayer-engineer` + `go-engineer` (if networked; protocol via `api-designer` first) — one `Task` batch after the "Proceed?" question. Product code and tests are written by these Tier-3 engineers, never by this skill (coordination-rules § Subagents).

## Phase 4: Measurements and accessibility
`performance-engineer` (frame, draw calls, memory, load on 4G emulation) ‖ `accessibility-specialist` (menus, settings) — one `Task` batch. The measurements are written to `docs/ops/measurements/YYYY-MM-DD-<topic>.md` (rule 12: a number cites an artefact) — the file is named in the "Proceed?" question.
**Budget exceeded**: every measured number is compared with its budget from Phase 1. Any number over budget → the verdict is `PARTIAL (over budget: frame 22 ms > 16.7 ms, draw calls 410 > 300, …)` with the measured value, the budget and the measurement file for each — never a `PLAYABLE` that hides the numbers, never a silent skip when a measurement could not be taken (then: `PARTIAL (not measured: …)`). The fixes go to the Phase 3 engineers as a new `Task` batch with consent, or to the next slice.

## Phase 5: Commit and PR
As `/dev-story` Phase 6 (git-workflow, step "Implement"):
1. **Status.** On every story card stamped in Phase 2 set `Status: Review` (as `/dev-story` Phase 6 step 1 — `/story-done` requires it), and the session state to `Next: /code-review --diff` through `<hooks>session-state.sh`; the Phase 2 "start" answer covers this edit, and the card rides the commit below.
2. **Commit gate**, one `AskUserQuestion`: commit and push (Recommended) · commit only · not now. Before asking, record it — `<hooks>session-state.sh set Gate "/team-game Phase 5: commit?"` — and clear it after the answer (`<hooks>session-state.sh set Gate "—"`), so an open gate survives the next turn (rule 7).
3. **Stage by name.** Read `git status --short` first and deal with every unplanned `??` entry (delete a spike, add a file deliberately if it belongs to the slice, otherwise leave it and name it); the story cards of Phase 2 are among the slice's files. Never `git add -A`.
4. `git commit -m "feat(<scope>): <slice title>"` (`feat(S-NNN): …` for one story, `feat(F-NNN): …` for several, `feat(prototype): …` for the prototype), then `git push -u origin feat/<scope>-<slug>`. Never commit on the default branch.
5. **Find out what starts CI** (`grep -l "pull_request" .github/workflows/*.yml`, each workflow's `on:`). When only `pull_request` starts the checks, open the PR as a draft in this step (`gh pr create --draft --fill`) so they run during review; `/story-done` marks it ready and merges it. Otherwise say which run to expect and its id.
6. **Wait for CI** only for a run that exists: one background `gh run watch <run-id> --exit-status`; no polling, no `AskUserQuestion` as a pause.

## Phase 6: Summary
The "fun" criterion from the concept — the user plays and decides (one `AskUserQuestion`: fun as specified · not yet — say what is missing · skip for now); this skill never marks it itself. A summary of numbers (measured vs budget), open findings, the branch, the commit and the PR (or why there is none). The code review runs after the commit, as the hand-off below.

Verdict: `PLAYABLE` | `PARTIAL (over budget: …)` | `PARTIAL (not measured: …)` | `PARTIAL (open: …)` | `BLOCKED (stage 1: game-concept <verdict>)` | `BLOCKED (stage 1: architecture-decision <verdict>)` | `BLOCKED`. Next step — one `AskUserQuestion`: `/web-studio:code-review --diff` (copy mode `/code-review --diff`) — then `/story-done` (Recommended on PLAYABLE) · commit first (when Phase 5 was declined) · `/story-done` (when the review already passed) · the next slice · fix the open findings first. Run the next skill only on that answer.
