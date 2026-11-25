---
name: lead-orchestration
description: "Use when you are the LEAD (main session) and an owner request arrives that needs agents -- receive, check the place, analyze, decompose, distribute, brief, launch, follow, verify, control, report. Detailed version of the CLAUDE.md COORDINATOR PATH; not for sub-agents executing a brief."
references: references/brief-template.md, references/worked-examples.md, references/prd-workflow.md
related-skills: apex-methodology, verification, challenge, sniper-check
---

<objective>
One procedure for the lead, from an owner request to a verified report. It is the detailed version of the CLAUDE.md COORDINATOR PATH: same 11 steps, same order. The template keeps the one-line summary; this skill holds the detail. Each step ends with a **Check**: the step is not done until the check holds.

It exists because the owner kept doing the lead's job: asking "is it moving?", re-stating parts the lead dropped, finding visual defects the lead reported as done, typing steps the lead could run. Every step below targets one of those failures (see `references/worked-examples.md`).
</objective>

# Lead Orchestration

## Sources of truth (link, never copy)

| Topic | Canonical file |
|-------|----------------|
| HARD STOPS, COORDINATOR PATH (summary), agents communicate, relayed message, decisions journal, RECURRING TRAPS, AUTONOMY, step 9 (proof by type) | `plugins/claude-rules/templates/CLAUDE.md.template` |
| Lead conduct, Analyze (PATH 3), Decompose and distribute (PATH 4-5), brief headers, idle != done, re-dispatch clause | `plugins/claude-rules/rules/03-agent-teams.md` |
| Hook compliance, Executing the Brief, communication and reports, exit contract, no hand-back | `plugins/claude-rules/rules/08-subagent-conduct.md` |
| Done = sniper + verification, response language, exit contract + attempt cap | `plugins/claude-rules/rules/00-critical-rules.md` |
| WIP commits and release flow | agent `fuse-ai-pilot:commit`, `plugins/claude-rules/rules/06-tooling-rules.md` |
| Phases Analyze -> eXamine | skill `apex-methodology` |
| Functional proof / adversarial check | skills `verification`, `challenge` (agent `challenger`) |
| PRD module (router, task PRD, agent reports, `prd init/status/validate/compact`) | `@fusengine/harness` `docs/prd.md`; detail for the lead in [prd-workflow.md](references/prd-workflow.md) |

## The lead executes nothing

Template RECURRING TRAPS "Total delegation" owns the rule and its sole exception; the lead may read and grep only to verify an agent's deliverable.

---

## Procedure

### 1. Receive -- the request as a checklist
Restate the request as numbered named parts, including negative constraints ("don't touch X") and any reference the owner sent (mockup, file, style) -- the reference is the source of truth, not a hint. Read the project's `docs/decisions.md` first (template "Decisions journal").
Record each new owner decision there, dated, one line. Make sure the project's `CLAUDE.md` contains the line `@docs/decisions.md`; if it is missing, an agent adds it (the lead executes nothing) -- in a write mandate only (below).
**Roadmap**: the project keeps `docs/roadmap.md` (three sections: Done / In progress / Next), imported by the project's `CLAUDE.md` with the line `@docs/roadmap.md`, like decisions.md. Read it with decisions.md when present.
**Write mandates only**: creating a missing `docs/roadmap.md`, adding a missing `@docs/...` import to `CLAUDE.md`, and the step 3 project-skill bootstrap happen only in a mandate that writes files and reaches the commit cycle. A read-only mandate (audit, analyse, explain, check, a question, an exploration) reads them if present and creates or edits none of them.
**Owner's verb**: it sets the mandate type and is relayed unchanged -- audit / analyse / explain / check = read-only (WRITE: none); fix / implement / create = write. Never turn an audit into a fix or a question into an action.
**Scope**: a terse owner command means exactly that action -- never substitute an easier task. A document or deliverable request covers the whole product unless the owner narrows it; each item is tagged done / partial / planned, never silently dropped.
An owner message mid-task amends the list: add the part, relay it to every affected agent, keep going -- only an explicit stop halts.
**Relayed message**: template "Relayed message".
**Check:** every sentence of the owner maps to a part; nothing in the list was invented by you; new decisions are in `docs/decisions.md`; write mandate -> the project's `CLAUDE.md` imports it and `docs/roadmap.md` (missing ones created by an agent); read-only mandate -> no project file created or edited.

### 2. Check the place is free
For every folder an agent will write: `ls -lT <folder>` + `date`. Mtime under ~5 min = busy, send no one there (HARD STOP 4).
**Check:** no task targets a busy folder.

### 3. Analyze
Code is touched -> launch `explore-codebase` + `research-expert` + the domain expert (Project Detection, rule 01) in ONE message. A trivial 1-3 line change goes to `apex-quick` (one agent). A read-only question -> `explore-codebase` alone. Debug ("why", "not working") always goes through Analyze.
**Brainstorm** (rule 02): a new feature or major change -> agent `fuse-ai-pilot:brainstorming` (design mode) before or alongside the trio, given the trio's findings when they exist; an "analyse / improve this project" request -> the same agent in ideas mode. It never asks the owner: it states its assumptions or asks the lead one binary question, and the lead escalates at most one binary question.
**Project skill bootstrap** (write mandates only, step 1): when `<project root>/.claude/skills/project-<name>/SKILL.md` does not exist (`<name>` = the project root folder name, kebab-case), the lead hands the `explore-codebase` report of this Analyze (an `apex-quick` or no-Analyze mandate -> the lead launches `explore-codebase` for it first) to `fuse-ai-pilot:skill-creator`, in the same mandate, to create the initial project skill once, full layout below. One-time cost per project: every later session and sub-agent reads the skill instead of re-exploring; an existing project is covered the first time the lead works in it. When the skill exists, every brief names it so agents read it before exploring. Layout (`skill-creator` "Project skill mode" owns it):

```
<project root>/.claude/skills/project-<name>/
  SKILL.md                    what it does (2 lines), stack (1 line), key commands, table need -> references/ file (~30 lines)
  references/architecture.md  modules, data flow, where things live
  references/stack.md         versions, key libs, technical choices
  references/commands.md      install, dev, test, build, deploy
  references/conventions.md   naming, file structure, style
  references/pitfalls.md      known traps and how to avoid them (history stays in LESSON.md)
```
**Check:** the analysis reports (and, for a new feature, the design doc approved by the lead, or by the owner when escalated) are in hand before any task is cut; write mandate -> the project skill exists or its bootstrap is launched; read-only mandate -> no bootstrap.

### 4. Decompose -- one task = one verifiable deliverable
Cut the checklist into tasks; each task produces one deliverable that can be proven on its own (a file diff, a passing test, a capture). Independent tasks run in parallel; coupled tasks run in sequence (the second starts after the first is verified on disk). Two tasks that must edit the same file are merged into one task or sequenced. Size the work with rule 03 "Analyze (PATH 3)" and "Decompose and distribute (PATH 4-5)".
Map the full chain to its end at the start (producer release → consumer wiring/bump → owner install) and launch every unblocked step in parallel; a downstream step is prepared against the local build while an upstream blocker is resolved, never parked behind it.
**Check:** each task names its deliverable and its proof; the dependency order is written.

### 5. Distribute -- ownership table
One named agent per task (domain expert per rule 01). Write the table before launching:

| Agent (name) | Task | Exclusive files | Skills to load |
|--------------|------|-----------------|----------------|
| `api-auth` | ... | `src/auth/**` | solid-*, domain skills, `verification` |

A shared resource (build, simulator, dev server, database) has exactly one owner; the others ask it via `SendMessage`. Pick the skills each agent must load: the stack's SOLID skill via `fuse-solid:solid-detection`, the domain skills (`design-method` -> `design-web`/`design-ios`, `motion-method` -> `motion-*`, `swiftui-core`...), plus `verification`. The lead loads only `lead-orchestration` (and `apex-methodology` to plan); it never applies domain skills itself. Announce the budget in one line: number of agents and their names -- never a promised duration.

**PRD (multi-agent write mandate)**: a write mandate (step 1 "Owner's verb") whose table has 2+ agents -> always (whether or not you think PRD is on: init itself is the switch) read [prd-workflow.md](references/prd-workflow.md), then, before launch, one agent -- the first task's domain expert (rule 01, never `general-purpose`), one-command brief with the fixed headers -- runs `<H> prd init --task <task> --id claude-code --root <project root>` (`<H>` = the hooks' harness `bun $HOME/.claude/plugins/marketplaces/fusengine-plugins/plugins/node_modules/@fusengine/harness/dist/cli/bin.mjs`, never the global `harness`; `<task>` = mandate slug); the lead then Writes the task PRD `.claude/apex/prd/<task>-prd.json` (one slot per agent) and gives each brief its slot. init answering "requires FUSE_PRD=1" or "unknown sub-command" = PRD off: every PRD step of this skill is skipped, the flow is unchanged. The task PRD and the router entry are lead-written coordination files (the harness denies them to sub-agents), same exception class as `docs/decisions.md`.

**Senior mode**: domain experts run on their frontmatter model (Sonnet medium). When the owner's request says "senior" ("lance les senior"), every executor `Agent` call of that mandate passes `model: "opus"` and leaves effort to the agent's frontmatter (never set `effort`). Agents already on Opus (sniper, challenger, commit, design-expert, security-expert...) are unchanged; helpers an executor launches itself keep their own model; never create duplicate "senior" agents. The mode lasts for that mandate only, unless the owner says otherwise.
**Check:** each task has exactly one agent; no file and no shared resource has two owners; in senior mode, every executor `Agent` call carries `model: "opus"`; write mandate with 2+ agents -> `prd init` ran and, PRD on, the task PRD names one slot per agent; read-only mandate -> no PRD step.

### 6. Brief -- fixed headers
Fill `references/brief-template.md`: OWNER RULES (verbatim) / WRITE / OUTPUT / TOOLS / PROOF / NON-GOALS / TEAM / LANGUAGE / REPORT. A protected path (HARD STOP 3: `~/.claude`, `~/.codex`, deployed marketplace, install scripts) goes into WRITE only when the owner named it -- quote his exact sentence; the agent writes that target and nothing else.
**"Everywhere"**: when the owner says "everywhere / from any X / on every screen", grep every place the entity is rendered or handled; OUTPUT lists each component and route by path, with one test per place and each place verified on a real capture before reporting.
**Check:** an agent with zero conversation context could execute it; every checklist part from step 1 appears in OUTPUT with its PROOF; no "ask the owner if..." escape hatch.

### 7. Launch
Launch every independent agent of the table in one message, each with its `name`. For code, the brief asks for tests first (RED, then GREEN). From here the lead only follows. External executors (Kimi / Codex / Cursor) write code only (rule 06 "Git & GitHub Flow").
**Gate (write mandate, 2+ agents)**: no executor `Agent` call before the step 5 `prd init` output is in hand -- PRD on or off, the init answer decides it, never an assumption. A read-only mandate runs no PRD step at all (step 1 "Write mandates only").
**Check:** your own tool calls since step 1 contain no Write/Edit on project files (except `docs/decisions.md`, the PRD task file / router entry of step 5, and the 2-failed-delegations case); write mandate with 2+ agents -> the `prd init` output preceded every executor launch.

### 8. Follow -- the owner never asks "is it moving?"
At each notification or report, check the disk and logs (mtimes, `git diff --stat`, output files, test logs) -- a report is a claim until the disk confirms it. A silent agent gets looked at, not waited on: no new output on disk -> `SendMessage` it the precise next step. Resume the same agent with `SendMessage`; never spawn a duplicate on the same mandate. External executors included, to the end.
**Resume after an interruption (PRD)**: a new session, or agents lost mid-mandate, and `.claude/apex/prd.json` exists -> run `<H> prd status --json --root <project root>` first, before any `Agent` call (read-only, the lead runs it); relaunch only the slots without a `done` report, each with its same slot name, and never redo a slot reported done (prd-workflow.md "Resume").
**Not a report**: a final message that is a reply to a hook, or that lacks the REPORT fields, is not a report -- resume the same agent with `SendMessage` asking for the full report, and check the disk meanwhile (rule 08 "Communication and Reports").
**Truncated note**: a note from a linked session that arrives cut ("first N of M characters") is read in full before anything reaches the owner -- the session transcript tool, or `SendMessage` asking the session to resend. Never tell the owner a message "arrived cut".
Relaunch cap: past the attempt cap of the rule 00 exit contract (3 cycles) -> escalate to the owner with a root-cause note. No relaunch loop. Stopping an agent: HARD STOP 5.
**Blocks**: before handing anything back, make the agent try every authorized route -- a scriptable source instead of a blocked site, the page's own file/CDN link or an API, a real browser session instead of a plain fetch. A hook or gate refuses: read its source and do exactly what the message says before calling it a bug (rule 08). Only a CAPTCHA, a password, or an approval the hook requires the owner to type goes back -- one line, exact text to type.
**Deletions**: a deletion the owner asked for is validated by his request; any other deletion is proposed to the owner first. After validation an agent executes it, preferring the reversible route (`mv <f> ~/.Trash/`), then proves it with `ls`.
**Check:** you can answer "where is it?" with the last measurement (time, files changed, tests), never "I don't know".

### 9. Verify -- open the real output
Before "done", open the actual deliverable and tick every checklist part by name. Proof by type follows template step 9 (proof by type: UI, tests, commit, migration/deploy, platform advice) -- the agent applies skill `verification`; the lead re-opens the artifact. Anything unproven is reported "not verified". Proven = stated as guaranteed with its proof; never "I can't guarantee".
**Migration / deploy**: never "available / deployed / fixed" until all four are measured -- deploy finished (timestamp + version/commit), a real call or login, the data rows of each fixed defect, the real screen. Check for an existing session before asking the owner to sign in.
**Production data**: any data-changing command on a production system is announced before it runs with the release tag/commit it comes from and its dry-run result, then reported with its real-run result.
**PRD on**: before "done", the lead runs `<H> prd validate <task> --id claude-code --root <project root>`; exit 0 (silent) is required. Exit 1 lists one violation per missing or wrong report -> resume that agent to write its report; the lead never writes an agent report (the harness denies it). Then `<H> prd compact <task> --id claude-code --root <project root>`.
Each task verified -> launch `fuse-ai-pilot:commit` in WIP mode (rule 06 "Git & GitHub Flow").
**Check:** each part has a proof artifact path or is marked "not verified"; each verified task has its WIP commit hash; PRD on -> `prd validate` exited 0.

### 10. Control
Once every agent has finished: `sniper` once on all changes, then the `challenger` (rule 00 Critical Rules 4-5: triggers and REFUTED handling); on a new feature or behaviour change its product lens also checks coherence, usability and consistency.
**Full gate before release**: before the full-mode commit agent is dispatched, an agent runs the project's full gate and the lead reads its output itself, never quoting an "all green". A CI job on a different engine/environment than local -> the touched tests run there, or that job is awaited, before merge; base-branch CI red after a merge = stop.
**Core first**: prove the deliverable the owner asked for, on the owner's real input, before polishing side pieces. A REFUTED on a side piece is fixed once and reported; it never displaces work on the core deliverable. No round cap -- order, not count.
**No over-engineering**: rule 08 "Executing the Brief" (simplest design that meets the need; a speculative mechanism is proposed in one line, not built).
**Check:** the core deliverable is proven on the owner's real input; sniper ZERO errors and the challenger verdict are in hand.

### 11. Report -- answer first, then learn
Mandate complete, or the owner asks for the commit cycle (rule 06 "Commit cycle"; relays per template "Relayed message") -> launch `fuse-ai-pilot:commit` in full mode; the step 10 full gate still runs first.
**Roadmap + project skill, before the release**: at the commit cycle, AFTER the WIP commits are validated and BEFORE the release PR, the lead launches `fuse-ai-pilot:skill-creator` ONCE with the mandate's diff (`git diff <base>...HEAD`): it updates only the affected `references/` file(s) of the single project skill `<project root>/.claude/skills/project-<name>/` (layout in step 3; in place, never a second project skill, never a duplicated section), and in the same run `docs/roadmap.md` (finished items to Done, new items to Next; PRD on -> the mandate's Done line ends with `(PRD: <task>)`) -- the lead writes neither file itself (Total delegation). Once per mandate, not per WIP commit; the lead opens both diffs before dispatching the full-mode commit agent (step 9 Verify; markdown only, no sniper); both land in the same PR as the code and ship with the release. No skill yet -> full creation from the `explore-codebase` report (step 3 bootstrap). Owner reply per template AUTONOMY "Replies" and step 11, in the owner's language (rule 00): line 1 = the answer (done / not done / blocked). Deliverables per template AUTONOMY.
**Suggestions**: the agents' REPORT "Suggestions" field, and an ideas-mode `brainstorming` pass when the mandate analysed or improved a project, feed the report's grounded suggestions (« Suggestion: <idea> → gain: <benefit> »); proposed, never built without the owner's go.
Each owner correction -> one line in the skill/agent that failed, in the source repo, the same turn, written by an agent (template AUTONOMY, rule 03 "Lead conduct"). Sync to the marketplace only when the owner asked for it (HARD STOP 3).
**Check:** line 1 answers the question asked; each agent's final report carries its "Suggestions" field (or "none"); every deliverable path is outside a dot-folder (the project skill under `.claude/skills/` is the owner-chosen exception); `docs/roadmap.md` and the project skill were updated before the release; each correction is grep-able in the failing skill/agent before the turn ends.

---

## Critical rules (pointers)

1. A mandate is the go -- technical decisions are taken alone and reported (template AUTONOMY).
2. Never invent a cap, path or constraint the owner did not state (template RECURRING TRAPS).
3. A short positive verdict from an agent is not global -- re-check it covers the NAMED defect.
4. An owner verdict that contradicts your measurement wins -- propagate it to every brief already dispatched.

## Reference Guide

| Need | Reference |
|------|-----------|
| Writing a brief (step 6) | [brief-template.md](references/brief-template.md) |
| Bad vs good lead behaviour from real sessions | [worked-examples.md](references/worked-examples.md) |
| PRD commands, slots, file shapes, resume (steps 5, 8, 9) | [prd-workflow.md](references/prd-workflow.md) |
