---
name: pre-goal
description: "Enter phase-by-phase task-and-goal mode for the session: each plan phase becomes a task, each phase gets a transcript-verifiable /goal, and the next goal is handed off inline (and copied to the clipboard when one is available) on approval. Triggers on '/pre-goal', 'phase-by-phase mode', 'task and goal mode', 'run this phase by phase with goals'."
user_invocable: true
---

# Pre-Goal Skill

For this entire session, operate in phase-by-phase task-and-goal mode. Follow this loop exactly.

<setup>
- If a plan exists (from a planning skill, ExitPlanMode, or a plan file you are working from), immediately turn each plan phase into a TodoWrite task before doing any work.
- As new work surfaces mid-session that isn't already a task, add it to the todo list when you discover it. Keep the list current, not retrospective.
- A "phase" maps to one or more tasks. A /goal may cover multiple tasks in the same phase.
</setup>

<per-phase-loop>
For each phase, in order:

1. EMIT GOAL. Output a /goal block for the phase. Every completion condition MUST be transcript-verifiable from session text alone:
   - file/path exists, file contains string (grep pattern)
   - a Bash command ran and produced specific output
   - a test/build command passed
   - a URL returned an expected status
   Do NOT put any condition that needs the user's judgment, approval, confirmation, greenlight, or "talk through with me" inside a /goal. Those are not verifiable by the evaluator and will loop the Stop hook. If a phase needs the user's sign-off, that sign-off lives OUTSIDE the goal (see step 4), not as a goal condition.

2. WORK THE GOAL. Execute the tasks for this phase. Mark each TodoWrite task in_progress when started and completed when its verification passes.

3. SIGNAL DONE. When every condition in the active /goal is satisfied, state plainly: "Phase <n> goal complete" and list each condition with the one-line evidence that satisfied it (the command output, the file path, the grep hit). Then STOP and wait. Do not start the next phase.

4. ON THE USER'S APPROVAL ONLY. After the user approves, hand off the NEXT phase's /goal prompt in both of these ways:
   a) inline in your reply, in a fenced code block (always, regardless of clipboard availability), AND
   b) copied to the user's clipboard when a clipboard tool is available. Detect the platform and use whatever is present:
      - macOS: `printf '%s' '<the goal prompt text>' | pbcopy`
      - Linux (X11): `printf '%s' '<the goal prompt text>' | xclip -selection clipboard`
      - Linux (Wayland): `printf '%s' '<the goal prompt text>' | wl-copy`
   If a clipboard tool is present, run it and confirm in one line that the goal is on the clipboard. If none is available, say so in one line and rely on the inline fenced block. The clipboard step is a convenience, never a hard requirement: the inline fenced block is always the source of truth. Then begin the next phase's loop at step 1.
</per-phase-loop>

<hard-constraints>
- The /goal condition string stays under 4000 characters. Each per-turn goal update or output you produce while a goal is active also stays under 4000 characters.
- Never advance past a phase boundary without the user's explicit approval. Plan approval is not phase approval.
- If no plan exists yet, ask the user (numbered) whether to run the planning step first or to define phase 1 from the task at hand. Do not invent phases silently.
</hard-constraints>

<success-criteria>
- Every phase has a TodoWrite task and a /goal whose conditions are 100% transcript-verifiable.
- No goal contains a human-judgment condition.
- At each approved boundary, the next goal prompt appears inline, and also lands on the user's clipboard whenever a clipboard tool is available (confirmed in one line either way).
- All goal strings and per-turn goal outputs stay under 4000 chars.
</success-criteria>
