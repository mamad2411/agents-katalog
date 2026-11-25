---
name: autopilot
description: Use this skill whenever the user wants to ship a side project end-to-end on a deterministic, repeatable agent harness. Also trigger when the user says "/autopilot", "ship my side project on autopilot", "set up the harness", "wire up Archon for me", or "run the 5-decision setup". Takes idea + target user + stack as input, scaffolds three input files (idea.md/user.md/stack.md) plus done.md per feature, installs Archon, drops in the canonical SCOPE→BUILD→DEPLOY→FIRST-USER workflow with three approval gates, and runs it end-to-end. Human-in-the-loop: agent pauses at each gate (continue/revise/kill). Never auto-pushes to live URL without DEPLOY-gate approval. Appends one new rule to the project CLAUDE.md after every run.
---

# Autopilot — Build the Harness That Ships Your Side Projects

The reusable 5-decision harness that turns every side-project session from improvisation into execution. One Saturday to wire. Every project after runs the same way.

Ship With AI artifact #24 · post-LtM methodology · companion to [How To Build The Harness That Ships For You](https://shipwithai.substack.com/).

## When to run

Invoke when the user:

- Types `/autopilot` or `/autopilot "<idea in one sentence>"`
- Asks to "ship a side project end-to-end," "set up the harness," "wire Archon," "make my agent ship for me"
- Wants to start a new side-project session that ships rather than wanders

Do NOT invoke when the user wants to:

- Add a feature to an existing in-flight session (use whatever harness is already in place)
- Run an autonomous overnight build on an existing harness (use [night-shift](../night-shift) instead)
- Plan or scope a new feature inside an already-shipped project (use [collect-feedback](../collect-feedback))

## Input surface

- `/autopilot` → operate on `cwd` (must be a git repo with at least one commit, or a fresh empty directory)
- `/autopilot "the idea in one sentence"` → operate on `cwd` with the idea pre-filled

If `cwd` is not a git repo and no path is given, run `git init` first and warn the user.

## Process

### Phase 1 — Discovery (silent, ~10 seconds)

Read, in order, and form an internal picture:

1. `git status` and `git log --oneline | head -5` — confirm it's a git repo
2. `ls -F` — see what's already in the directory
3. Check for existing `idea.md` / `user.md` / `stack.md` / `done.md` — note overwrite risk
4. Check for `.archon/workflows/` — note whether Archon is already wired here
5. Check `CLAUDE.md` for existing `## Lessons` section — preserve and append, don't overwrite

Do not print anything user-facing during this phase.

### Phase 2 — Interview (exactly three questions)

Ask these three questions, in this order, and wait for the user to answer each before proceeding. Do **not** ask follow-up questions. Three questions is the budget.

**Q1.** What are you building? (One to three sentences. Plain English. No tech detail yet.)

> Example: "A tool that lets a parent generate a custom bedtime story for their kid in under 60 seconds, using the kid's name and 3 favorite themes."

**Q2.** Who is the one specific first user? (A real person if possible. Job, context, what they currently use instead, what would make them switch.)

> Example: "Sara, my sister-in-law, mom of a 4-year-old, currently reads from a stack of 6 worn books, would switch if she could give her daughter a story with her own name in it."

**Q3.** What's your stack default? (Language, framework, deploy target. One line each.)

> Example: "TypeScript, Next.js 14 app router, Vercel."

All other calibration comes from Phase 1 discovery. Do not ask follow-ups.

### Phase 3 — Scaffold (silent, ~30 seconds)

1. Write `idea.md` from Q1 (3 sentences max — see template below).
2. Write `user.md` from Q2 (1 named user, structure who/currently/switch-trigger).
3. Write `stack.md` from Q3 (3 lines: language/framework/deploy).
4. If `archon` is not on PATH, run `bash ${SKILL_DIR}/scripts/install-archon.sh` and wait for it to finish.
5. Drop `${SKILL_DIR}/assets/ship-side-project.yaml` into `.archon/workflows/`.
6. Print the four file diffs and the install confirmation. Wait for explicit `go` before proceeding to Phase 4.

If Archon is already installed at the system level, skip step 4 and print "Archon already installed at $(which archon)."

### Phase 4 — Run (Archon does the work)

On the user's exact reply of `go`:

1. Print: "Starting harness. The agent will pause at three approval gates. Approve via `/workflow approve <run-id>` or reject with feedback at each."
2. Run `archon workflow run ship-side-project "<one-line task description from idea.md>"` — Archon takes over from here.
3. The Archon workflow walks SCOPE → scope-gate → BUILD (loop until COMPLETE) → build-gate → DEPLOY → deploy-gate → FIRST-USER → patch.
4. Each `approval:` node pauses with a `gate_message` and waits for `/workflow approve <run-id>` (or reject). The skill is done once Archon hands control back at the patch step.

Do **not** auto-confirm any gate on the user's behalf. Even if the agent thinks the artifact is fine.

Do **not** modify the workflow YAML mid-run. The harness is the constant.

### Phase 5 — Reflection (silent, ~15 seconds)

After Archon returns:

1. Read the patch output from the final node.
2. Append it to the project's `CLAUDE.md` under a `## Lessons` section (create if missing).
3. Print: "One new rule added to CLAUDE.md. Next session starts smarter."
4. Print the live URL and the drafted FIRST-USER message side by side.

## Output templates

### idea.md

```markdown
# Idea

{One sentence: what it does.}

{One sentence: why it's worth building.}

{One sentence: what makes it different from what already exists.}
```

### user.md

```markdown
# Target User

**Who:** {name + role/context, e.g. "Sara, mom of a 4-year-old"}

**Currently does:** {what they use instead today}

**What would make them switch:** {the one specific trigger}
```

### stack.md

```markdown
# Stack Defaults

**Language:** {e.g. TypeScript}
**Framework:** {e.g. Next.js 14 app router}
**Deploy:** {e.g. Vercel}
```

### done.md (per feature, written by the SCOPE stage)

```markdown
# Done — {feature name}

- {acceptance line 1, machine-checkable wherever possible}
- {acceptance line 2}
- {acceptance line 3}
```

### CLAUDE.md ## Lessons section (appended by Phase 5)

```markdown
## Lessons (added {today as YYYY-MM-DD})

- {one rule extracted from this run's failure modes — phrased as a positive
   directive the agent can act on, not as a negative complaint}
```

## Anti-patterns to avoid

1. **No more than three input questions.** Three is the budget. Stack is the third.
2. **No auto-confirming any gate.** Every transition between stages waits for explicit user input. Reading the agent's output is the user's job.
3. **No skipping the patch step.** The patch step is what makes the harness compound. Always run it. Never let the user skip it.
4. **No editing the workflow YAML on behalf of the user.** The harness is the constant. Don't suggest "improvements" mid-run.
5. **No running `vercel deploy --prod` (or any deploy command) without DEPLOY-gate confirmation.** Live URLs are visible. Confirm first.
6. **No more than five features in SCOPE.** If the agent proposes six, ask which two collapse into one. Five is the ceiling per run.
7. **No overwriting an existing CLAUDE.md `## Lessons` section.** Always append.

## What "done" looks like

The skill completed successfully when:

- `idea.md` + `user.md` + `stack.md` exist in the project root
- Archon is installed and `.archon/workflows/ship-side-project.yaml` is in place
- Archon has run end-to-end, paused at three gates, and produced a live URL
- A drafted message to the first user exists in the terminal output
- One new rule has been appended to the project `CLAUDE.md ## Lessons` section

The user should now be able to:

- Re-run `archon workflow run ship-side-project "<task>"` against any future side project with a fresh `idea.md` + `user.md` + `stack.md`
- Trust the workflow to ship without supervising every step
- Watch session N+1 take less time than session N (because CLAUDE.md keeps growing)

## Start here

Begin with Phase 1 (silent discovery). Output nothing user-facing until Phase 2 (the three questions).
