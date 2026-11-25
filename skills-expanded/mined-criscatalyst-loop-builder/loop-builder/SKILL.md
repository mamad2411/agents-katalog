---
name: loop-builder
description: Build a file-based agent loop (harness) for a long, powerful task BEFORE running it — so you design the loop and only verify the output, instead of supervising every step. Runs a short interview (goal, done-condition, non-goals, verify commands), scaffolds loops/<slug>/ with VISION.md + specs + IMPLEMENTATION_PLAN.md + AGENTS.md + PROMPT files + loop.sh, runs PLANNING, gets ONE plan approval, then loops BUILDING autonomously and hands back the diff + eval results. Trigger when the user says "loop-builder", "/loop-builder", "build a loop", "create a loop for X", "set up an autonomous loop", or asks to run a long autonomous task (a feature, a refactor, a tool, a content batch).
---

# /loop-builder — design the harness, then run the loop

Stop prompting an agent step by step. Instead, define the **goal** + a **verifiable done-condition**; this skill generates the whole file-based harness on disk and then runs the loop. You only verify the output.

**Promise:** from "I babysit every step in case it errors" → "I approve a plan, then I verify the result."

This is **loop engineering**: the leverage is no longer the single prompt, it's the system that prompts, runs, and *verifies* the agent until the goal is met. See `README.md` for the full background and credits.

## When to use

- A long, powerful task: a new feature, a big refactor, a new tool/script, a content batch, a migration.
- The user says: "build a loop", "create a loop for X", "set this up to run on its own", "/loop-builder".

Do NOT use for: 5-minute one-shots, tasks with no objective done-condition, pure-judgment decisions, or single irreversible actions (those stay direct-confirm).

## Guiding principles (loop engineering)

1. **State lives on disk, not in context.** Each iteration starts from fresh context and reloads the files.
2. **VISION.md does not change** during the run (the compass). The PLAN changes (the task order).
3. **Backpressure beats direction:** wrong output is rejected by an automatic eval-gate (tests/lint/build), not by the human.
4. **Maker/verifier split:** the agent that builds ≠ the agent that verifies (models skew positive grading their own work).
5. **Ratchet:** every agent mistake → one line in AGENTS.md, traceable to a real failure.
6. The human **"sits on the loop, not in it"**: design + review, not in the per-step seat.

## Flow (3 phases, only 2 human touchpoints)

```
INTERVIEW (interactive, 4-5 questions)
      │
SCAFFOLD loops/<slug>/  +  PLANNING mode  →  IMPLEMENTATION_PLAN.md
      │
   ┌──┴── GATE 1: human approves VISION + PLAN   (the "design")
   │      ...then the engine runs the WHOLE plan — phase changes are not stops
   │
BUILDING loop (autonomous: maker/verifier, backpressure, commit per task)
      │
   ┌──┴── GATE 2: human verifies the output (diff + eval results)   (the "verify")
```

## PHASE 1 — Interview (interactive, terse)

Ask only these (a single multi-question prompt is ideal). Nothing more.

1. **Goal** — what must be true at the end? (1-2 sentences)
2. **Objective done-condition** — how is "finished" verified *automatically*?
   - Code/software → "tests pass + lint clean + build ok + runs locally"
   - Content/docs → "passes the style guide + readability ≥ threshold + matches the brief"
3. **Non-goals** — what is explicitly out of scope? (prevents scope creep / slop)
4. **Verify commands** — the concrete gate commands (e.g. `pytest -q`, `npm test`, `npm run lint`, `npm run build`).
5. **Run mode** — run now in this session (you watch it), or run unattended in the background (see Engines).

If the user already gave goal + done-condition, skip the covered questions. Infer the rest and state your assumptions; don't ask for the sake of asking.

## PHASE 2 — Scaffold + Planning (autonomous)

### 2a. Create the folder
`./loops/<slug>/` at the project root (kebab-case slug from the goal). Keep it inside the git repo so each iteration is a checkpoint.

```
loops/<slug>/
├── VISION.md                 # the compass (does not change mid-run)
├── specs/<topic>.md          # requirements per topic (outcomes, no implementation)
├── IMPLEMENTATION_PLAN.md    # generated in planning; live status
├── AGENTS.md                 # build/test/lint commands + learnings (<60 lines)
├── PROMPT_plan.md            # planning-mode instructions
├── PROMPT_build.md           # building-mode instructions
└── loop.sh                   # the bash engine (works on any single machine)
```

Copy the templates from this skill's `templates/` folder and fill the `{{...}}` placeholders from the interview. Write one spec per distinct topic of the goal.

### 2b. Pick the engine

| Task shape | Engine | Why |
|---|---|---|
| Anything, any single machine, unattended | **`loop.sh`** (bash `while` loop feeding `PROMPT_build.md` to `claude -p`) | Zero dependencies beyond the Claude CLI. The canonical Ralph loop, and it waits out usage limits instead of dying on them. **Default.** |
| Long overnight closed loop with a completion phrase | **ralph-wiggum plugin** (`/ralph-loop ... --max-iterations N --completion-promise DONE`) | Stop-hook re-feeds the prompt; built-in safeguards. Install: `/plugin install ralph-wiggum@claude-plugins-official` |
| Interactive, in this session | Run the loop steps directly via **subagents** (Task tool): maker subagent + separate verifier subagent | You watch it live; good for the first run while you build trust |
| Recurring heartbeat (triage, digests) | OS scheduler: **cron**/**launchd** (macOS), **Task Scheduler** (Windows), or a `tmux` session running `loop.sh` | No second machine needed — the OS scheduler runs `loop.sh` on a timer |

Default = **`loop.sh`** (portable, single-machine). Record the choice in `AGENTS.md`.

⚠️ Whichever engine you pick, **it gets launched after GATE 1**. Choosing an engine is a design
decision, not a quote to be approved: the human already said "go" to the plan, and no second
consent is needed to start it.

⚠️ **If the run is unattended, use `loop.sh` — not an in-session engine.** Anything driven from inside a Claude session dies with that session when the plan's usage limit is reached, and stays dead until a human restarts it. That is how whole overnight windows get wasted. `loop.sh` catches the limit error, parses the reset time, sleeps, and resumes the same task **without spending an iteration**; unreadable or implausible reset times fall back to a short blind retry.

Copy `templates/loop.sh` into the loop folder and `chmod +x` it. Optional knobs — set `LOOP_NOTIFY_CMD` to get told when it pauses and resumes:

| Variable | Default | Purpose |
|---|---|---|
| `LOOP_NOTIFY_CMD` | — | called as `"$LOOP_NOTIFY_CMD" "<message>"` on pause / resume / done / give-up |
| `LOOP_MAX_WAIT_H` | `24` | total waiting budget before the loop stops and notifies |
| `LOOP_BLIND_WAIT_M` | `30` | wait used when the reset time can't be read |
| `LOOP_SANE_WAIT_H` | `6` | any longer parsed wait is treated as a misparse |

Timestamped history lands in `loops/<slug>/loop.log`.

### 2c. Run PLANNING mode
Follow `PROMPT_plan.md`: read VISION + specs + existing code → gap analysis (do NOT implement; do NOT assume something is missing — search the code first) → write `IMPLEMENTATION_PLAN.md` (prioritized tasks, one line each).

## GATE 1 — Plan approval (1 confirmation)

Show the user, concisely: **VISION.md** (mission + non-goals), **IMPLEMENTATION_PLAN.md** (the ordered task list), the **chosen engine** + done-condition. "Go" → start building. "Change X" → apply + re-show. "Stop" → leave the files for later.

## PHASE 3 — Building loop (autonomous)

> ⚠️ **On "Go" you LAUNCH THE ENGINE. You do not run the tasks yourself.** One launch that
> covers the **whole** plan, first task to last. The nine steps below are what the agents
> *inside* the loop follow — they already live in `PROMPT_build.md`. They are not a to-do
> list for the main session.
>
> **The plan's phases are not checkpoints.** A plan with four phases is four groups of work
> **inside one run** — not four separate runs, and above all not four moments where you stop,
> report, and wait for another "go". There are **exactly two** human touchpoints: GATE 1
> before, GATE 2 after. Adding your own puts the human back inside the loop, which is the
> one thing this skill exists to prevent.
>
> **The tell:** if you catch yourself writing *"phase N is done, shall I start N+1?"*, or
> opening the project's files to implement a task from the plan — **you have stepped into the
> loop**. Stop and launch the engine on the work that remains.
>
> If the work genuinely exceeds one launch (an engine's size limit), split it and **chain the
> runs yourself, without asking**: the approval was GATE 1, not one per chunk. Report back
> when the plan is finished or something is `BLOCKED`.

Each iteration (fresh context) follows `PROMPT_build.md`:
1. **Orient** — read VISION + specs + plan + AGENTS.
2. **Select** — take **one** task (most important not-done).
3. **Investigate** — study the relevant code (don't assume "not implemented").
4. **Implement (maker)** — apply the change, surgically.
5. **Validate (verifier — backpressure)** — a *separate* check runs the verify commands. **Fail → fix & re-validate, do NOT commit. Pass → proceed.**
6. **Update plan** — mark task done + note discoveries in `IMPLEMENTATION_PLAN.md`.
7. **Update AGENTS.md** — append operational learnings only (ratchet), not a diary.
8. **Commit** — descriptive git commit.
9. **Loop** — context cleared, next task. Stop when the plan is empty / done-condition met / max-iterations.

**Guardrails (always, even unattended):**
- Irreversible/external actions (deploy, push to prod, send email/DM, delete) → confirm with the human, never auto.
- Verify with concrete proof, never "green but broken".
- Stuck twice on the same task → escape hatch: mark `BLOCKED` in the plan, move on, report at handback.
- Start with a low iteration budget (10-15) on new tasks.

## GATE 2 — Handback (human verifies)

Deliver a concise report: tasks completed, the **diff/output** to review + verify-command results (the proof), any `BLOCKED` items / autonomous decisions to validate, approximate cost (iterations/tokens). The human approves, or sends it back into the loop with feedback (which becomes a new spec line or AGENTS.md line = ratchet).

## After the run

The `loops/<slug>/` files persist — the loop is re-runnable and improves each run (eventual consistency). For a recurring loop, wire `loop.sh` into your OS scheduler.
