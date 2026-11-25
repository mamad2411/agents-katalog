---
name: helpmeplan
description: Guided planning workflow — takes a project from brainstorm to a build-ready spec/ folder (per-area plans, project structure, M0→Mn roadmap) through 5 phases (brainstorm, scope, design, mockups, architecture). Use when the user wants to plan a project, continue planning, or asks "where were we" about planning. Detects current phase from the filesystem and resumes.
argument-hint: "[status | spec | redo <phase-number>]"
---

# helpmeplan — guided planning workflow

Guide the user from raw idea to a build-ready `spec/` folder, one phase at a time.

**This skill is fully self-contained.** All phase definitions, questions, and templates live in [phases.md](phases.md) in this skill folder. Never depend on any file outside this folder for workflow rules — the project may not have a WORKFLOW.md, and that's fine.

Core model: `planning/` is the "src" of planning (working files, messy is fine); `spec/` is the "dist" (distilled build plan — per-area plans, project structure, roadmap — the only thing coding needs). **Work happens in `planning/`, conclusions get promoted to `spec/`. If it's not in the spec, it doesn't get built.**

## Invocation modes

- **(no args)** — detect state, then resume the active phase
- **`status`** — detect state, report it, stop. No work.
- **`spec`** — jump to `spec/` distillation. If phases are incomplete, list the gaps and get explicit confirmation before proceeding.
- **`redo <n>`** — reopen completed phase n: flip its status back to `in-progress` and resume it. Warn that later phases may need revisiting.

## Step 1 — Detect state (always, before anything else)

The filesystem is the state. No memory needed.

1. Look for `planning/` and `spec/` in the project root.
2. If `planning/` doesn't exist → offer to scaffold (Step 2), then start phase 1.
3. Otherwise, for each phase in [phases.md](phases.md), check its deliverable file:
   - missing → phase not started
   - exists with `Status: in-progress` line → phase active
   - exists with `Status: done` line → phase complete
4. Active phase = the first phase that is not complete.
5. Report a one-line orientation before working, e.g.:
   > Phase 3 (design) is active — brand.md started, styleguide.html not yet built. Phases 1–2 done.

## Step 2 — Scaffold (when structure is missing)

Ask once before creating files, then create whatever is missing (never overwrite existing files):

```
planning/
├── 1-brainstorm/ideas.md
├── 2-scope/scope.md
├── 3-design/brand.md          # styleguide.html gets built during phase 3, not stubbed
├── 4-mockups/                 # mockup files (one per UI surface) get built during phase 4, not stubbed
├── 5-architecture/architecture.md
└── decisions.md
```

Each stub comes from its template in [phases.md](phases.md) and starts with `Status: in-progress` (the first line of the file). Also offer to generate a `WORKFLOW.md` in the project root from [workflow-doc.md](workflow-doc.md) — human-readable documentation of this process; the skill never reads it back.

## Step 3 — Work the active phase

Read the active phase's section in [phases.md](phases.md), then:

- **Ask questions 1–2 at a time**, conversationally. Never dump the full question list. Use AskUserQuestion for discrete choices (e.g. "blend in vs. stand out"); free-form chat for open-ended ones (brainstorming).
- **Capture as you go** — write the user's answers into the phase's deliverable file continuously, in the user's voice, not at the end.
- **Log decisions** — whenever a real choice gets made, append one line to `planning/decisions.md`: `- [phase] decision — why`.
- **Build phase artifacts** where the phase calls for them (styleguide.html in phase 3, mockup pages in phase 4; see [phases.md](phases.md)). Offer to publish HTML as Artifacts for click-through review. Mockups are throwaway: never upgrade them into real code.

## Step 4 — Gate before advancing

Each phase has a "done when" criterion in [phases.md](phases.md). When it looks met:

1. Restate the criterion and ask the user to confirm phase exit. **The user is the gatekeeper — never self-approve.**
2. On confirmation: flip the deliverable's `Status:` line to `done`, announce the next phase in one line.
3. If the user wants to skip ahead or work out of order: **warn once** (name what's incomplete and the risk), then comply. This skill is a guide, not a cop.

## Step 5 — Distill the spec/ folder

When all 5 phases are done (or the user forces it via `spec`):

1. Read every deliverable in `planning/`.
2. Write a `spec/` folder in the project root:

   ```
   spec/
   ├── README.md        # entry point + index
   ├── structure.md     # planned codebase layout
   ├── roadmap.md       # build order: M0, M1, M2…
   └── plans/           # one plan file per area — named for THIS project
       └── <area>.md
   ```

   - **`README.md`** — what the project is (one paragraph), the v1 feature list one sentence each (from scope), the **Not doing** list (later/no, so scope creep stays visible), and a linked index of every other spec file.
   - **`plans/<area>.md`** — one plan file per project-relevant area. Pick the split that fits *this* project (per feature, per surface, or per subsystem — e.g. a web app might get `auth.md`, `editor.md`, `sharing.md`; a CLI might get one file per command group). Don't force a fixed set. Each plan covers: what it does and why (from scope), behavior including empty/error/working states, which mockup(s) it must look like (link them + the styleguide), which architecture components it maps to, and its edge cases and open questions.
   - **`structure.md`** — the planned file/folder layout of the real codebase as an annotated tree (what lives where and why), plus naming conventions and where new code of each kind should go. Derived from architecture; the real code is laid out to match this file (rooted in `build/` when the overnight script does the building).
   - **`roadmap.md`** — build order as milestones **M0, M1, M2…**. M0 is the walking skeleton: project scaffold matching `structure.md` plus the thinnest end-to-end slice that actually runs. Each milestone states: goal in one line, which `plans/` files it draws from, and a verifiable **done when**. Order by dependency first, then risk — put the scariest/most load-bearing work early. Every v1 feature in README.md must appear in exactly one milestone.
3. Quality bar: *a stranger could build the project from `spec/` alone, working in roadmap order.* Read it back with that test in mind; fix gaps before presenting.
4. After coding starts: if reality forces a change, update the relevant `spec/` file first, then the code.

## Step 6 — Offer the overnight build script

Once `spec/` is delivered, offer **once** to generate `overnight.sh` in the project root — a script the user launches before walking away. It runs Claude Code unattended overnight to build the project from `spec/`, so the user can test the result the next morning.

What the generated script must do:

- Run the agent in a **detached tmux session** so it survives closing the terminal (`tmux attach -t overnight` to watch live). **tmux is required** — when generating the script, check it's installed; if missing, offer to install it (`brew install tmux` / `apt install tmux` / `pkg install tmux` on Termux) or ask the user to. If running under Termux on a phone, grab `termux-wake-lock` first so the device doesn't sleep.
- Launch `claude -p "<kickoff prompt>" --permission-mode bypassPermissions`, teeing output to a timestamped log file.
- **Everything the run produces goes in a `build/` directory** — the script `mkdir -p`s it, the log lives there, and the prompt confines the agent to it. The project root stays clean: no code, configs, logs, or reports scattered next to `planning/` and `spec/`.
- The kickoff prompt tells the agent: build from `spec/` only, **entirely inside `build/`** (lay out the code per `spec/structure.md` rooted there, never write outside it), in `roadmap.md` order starting at M0; verify each milestone's "done when" before advancing; `git commit` after each milestone; **append to `build/BUILD-LOG.md` after each milestone** (what was built, how the "done when" was verified, any deviation from spec and why) so there's a readable mid-run record even if the run dies overnight; when finished or blocked, write `build/MORNING-REPORT.md` — what shipped, how to test it, what's unfinished and why.

Template (adapt the prompt to the project):

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
command -v termux-wake-lock >/dev/null 2>&1 && termux-wake-lock
mkdir -p build
LOG="build/overnight-$(date +%Y%m%d-%H%M).log"
PROMPT='Build this project from spec/ only, entirely inside the build/ directory —
never write files outside build/. Lay out the code there following spec/structure.md.
Work through spec/roadmap.md in order, starting at M0. Verify each milestone'\''s
"done when" before advancing, and git commit after each milestone. After each
milestone, append an entry to build/BUILD-LOG.md: what you built, how you verified
the "done when", and any deviation from spec and why. When finished or blocked,
write build/MORNING-REPORT.md: what shipped, how to test it, and what is unfinished
and why.'
command -v tmux >/dev/null 2>&1 || {
  echo "tmux is required. Install it first: brew install tmux / apt install tmux / pkg install tmux (Termux)" >&2
  exit 1
}
CMD="claude -p $(printf %q "$PROMPT") --permission-mode bypassPermissions"
tmux new-session -d -s overnight "$CMD 2>&1 | tee $(printf %q "$LOG")"
echo "Agent running in tmux session 'overnight' — watch: tmux attach -t overnight"
echo "Log: $LOG — in the morning, read build/MORNING-REPORT.md"
```

After writing the file, make it executable — `chmod +x overnight.sh` (on Linux/macOS/Termux; skip on Windows) — otherwise the user hits "Permission denied" on `./overnight.sh`. Then tell them the exact command to run: `./overnight.sh`.

When offering, **warn plainly**: `bypassPermissions` means the agent runs commands without asking. The user should commit/push everything first and only run it in a directory (and on a machine) they're comfortable handing over. Generate the script and stop — **never launch it yourself**; it's the user's to run.

## Rules

- Filesystem is the only state — always re-detect, never assume.
- Never overwrite user content; append and edit surgically.
- One phase at a time; questions in small doses.
- Warn on skipping, never block.
- All workflow knowledge lives in this folder — keep it portable (copying `.claude/skills/helpmeplan/` to another machine/project must be sufficient).
