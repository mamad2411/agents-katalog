---
name: execute-phase
description: Executes the granular tasks of the current phase, runs verification, and updates the plan.
disable-model-invocation: true
---

You are executing the "/execute-phase" protocol. Your job is to act as the Engineer and write the code.

1. **Resolve Active Plan:** Read `.plan/.active` to get the current plan name (e.g. `user-auth`).
   - If the file is missing or empty, tell me: *"No active plan is set. Run `/list-plans` to select one."* Then stop.
2. **Read the Instructions:** Read `.plan/[active-name]/plan.md` and find the first unchecked `[ ]` phase.
3. **Guard — Check for a Planned Phase:** Look for an `**Atomic Tasks**` section associated with that phase in `plan.md`. If no such section exists, the phase has not been planned yet. Ask:
   *"This phase hasn't been planned yet. Want me to plan it now and then execute? (yes / no)"*
   - **If yes:** Run the plan-phase logic inline — draft granular atomic tasks, acceptance criteria, and verification commands for this phase; append them to `plan.md`; print a summary and ask: *"Does this plan look right? Reply with: **approve** to execute, or **change: [feedback]** to revise."* Repeat until approved, then continue to step 4.
   - **If no:** Confirm *"Run `/plan-phase` first to detail this phase."* and stop.
4. **Execute:** Implement the tasks step-by-step. Remember to follow the global "Ask User Question" rule to get approval before modifying files.
5. **The 3-Strike Error Protocol:** As you write code and run verification commands, if you encounter the exact same error 3 times:
   - **STOP executing immediately.** Do not blindly retry.
   - Log the error, what you tried, and your hypothesis into `.plan/[active-name]/findings.md`.
   - Ask me for help: *"I've hit a roadblock and logged the error in the findings file. How would you like me to proceed?"*
6. **Verify & Update:** Once the code is written, run the verification commands defined in the plan. If they pass, update `.plan/[active-name]/plan.md` by changing the phase's checkbox to `[x]`.
7. **Prompt Next Step:** Inform me the phase is complete and ask: *"Phase complete and verified. Would you like to review the app, or should we run `/plan-phase` for the next item?"*
