---
name: idea-to-completion
description: Takes a rough idea to project completion with research, plan, implement-verify loop, and human-in-the-loop gates. Use when the user has a vague or high-level idea and wants to reach a shippable outcome with iterative review.
---

# Idea to Completion (Loop + Human-in-the-Loop)

This skill runs an **end-to-end workflow** from a **rough idea** to **project completion**. It includes **loops** (implement → verify → human review → repeat if needed) and **two human-in-the-loop gates**: one after the plan, one after each implementation pass until the human approves.

## When to use

- The user has a rough or vague idea (e.g. "Add a dashboard for X", "We need better error reporting").
- The outcome should be shippable or project-complete (code, tests, docs, ready for deploy or handoff).
- You want the human to approve the plan and then approve the implementation (with the option to request changes and loop).

## Phase 1: Clarify the idea

- **Research:** Use the main agent or the **explore** subagent to understand the codebase: what exists, what patterns are used, what’s missing for the idea.
- **Summarize:** In 2–4 sentences, state what "done" would look like for this idea (scope, main deliverables, out of scope). Present this to the user.
- **Optional:** If the idea is still very vague, ask the user one or two short clarifying questions (e.g. "Should this be API-only or include a UI?"). Then incorporate their answer into the summary.

## Phase 2: Plan and first human gate

- Invoke the **planner** subagent with the clarified idea (and research summary). Get: scope, numbered steps, dependencies, risks/alternatives.
- Present the **plan** to the user in a clear, readable form.

Then output **Gate 1 handoff**:

```
--- HUMAN REVIEW: PLAN ---
Please review the plan above. Reply with one of:
- "Approved" or "Go ahead" → I will proceed to implementation.
- "Refine: [your feedback]" → I will update the plan and show you again (then ask for approval).
- "Abort" → I will stop.
--- END GATE ---
```

**Stop.** Do not start implementation until the user has approved the plan (or asked to refine; then re-plan and show again, and stop at the gate again until they approve).

## Phase 3: Implement → Verify → Human review (loop)

- **Implement** the plan (or the next chunk if you are iterating). Follow project rules. Include tests and minimal docs where appropriate. Do not merge, tag, or deploy.
- **Verify:** Invoke the **verifier** subagent. Summarize: what was done, what passed, what (if anything) failed or is incomplete.
- **Review package for human:** Produce a short summary: what changed in this pass, how it fits the plan, any risks or follow-ups.

Then output **Gate 2 handoff**:

```
--- HUMAN REVIEW: IMPLEMENTATION ---
Please review the changes (and diff if available). Reply with one of:
- "Approved" or "Looks good" → I will proceed to Phase 4 (completion).
- "Request changes: [your feedback]" → I will address your feedback and run implement → verify → this gate again (loop). You can say "Request changes: focus on X" to narrow scope.
- "Abort" → I will stop; no completion steps.
--- END GATE ---
```

**Stop.** Do not run Phase 4 until the user has approved.

- **If the user says "Request changes":** Apply their feedback (or clarify if needed), then run **Implement → Verify → Review package → Gate 2** again. Repeat until they reply "Approved" or "Abort."
- **If the user says "Refine" at Gate 1:** Go back to Phase 2 (update plan, show plan, output Gate 1 again).

## Phase 4: Completion (after approval only)

Run **only** after the user has approved at Gate 2 (e.g. "Approved" or "Looks good").

- **Completion checklist:** Generate a short checklist for "project completion" in your context, e.g.: tests pass, docs updated, env/config noted, release notes or changelog entry drafted.
- **Release notes / changelog:** Draft release notes or a changelog entry for this work. Do not push or tag unless the user explicitly asks.
- **Handoff:** State what is left for the human (e.g. "Run your deploy process", "Create the tag when ready", "Open a PR if needed"). Do not run deploy or destructive commands unless the user explicitly instructs you to.

If the user said "Abort" at any gate, confirm abort and do not run Phase 4.

## Loop summary

- **Gate 1 (plan):** Approve plan → continue to Phase 3. Refine → re-plan and show Gate 1 again. Abort → stop.
- **Gate 2 (implementation):** Approved → Phase 4. Request changes → loop: implement → verify → Gate 2 again. Abort → stop.

Never assume approval. At each gate, wait for the user’s reply before proceeding.
