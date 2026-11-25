---
name: agile-project-lifecycle
description: Full agile development lifecycle at project level: rough idea → requirements → development → unit/integration/e2e tests → feedback loop with human-in-the-loop until completion. Replit-style iterative flow. Use when building a project from a rough idea with full test pyramid and iterative feedback.
---

# Agile Project Lifecycle (Replit-Style, Full Loop + HITL)

This skill runs a **project-level** workflow that mimics an **agile development lifecycle**: from a rough idea through **requirements**, **development**, **unit**, **integration**, and **e2e tests**, with a **feedback loop** and **human-in-the-loop gates** until the human declares completion. It works **iteratively** on the whole project (or current slice) and loops until the user is satisfied.

## When to use

- The user has a rough idea and wants a **working project** (not just a plan or a single feature).
- You want the full **agile-style** flow: requirements → develop → unit → integration → e2e (or manual test) → human feedback → repeat.
- The human should approve **requirements** first, then **each iteration** (approve / give feedback / move to next slice / mark complete).

## Replit-style behavior

- **Project-level:** Work on the project as a whole; each iteration delivers a runnable slice.
- **Test pyramid:** Unit tests (fast, many) → integration tests (services, DB, API) → e2e or manual test (full flow). See [reference.md](reference.md) for definitions.
- **Runnable every iteration:** After each pass, the project should build and run (or tests run); the human can try it and give feedback.
- **Loop until complete:** Human can say "Feedback: ..." to iterate on the same slice, "Next iteration" to move on, or "Complete" to finish.

---

## Phase 0: Discovery and requirements

- **Research:** Use **explore** (or main agent) to understand the codebase: stack, structure, existing tests, what’s there vs what’s missing for the idea.
- **Clarify:** Summarize what "done" looks like in 2–5 sentences. If the idea is vague, ask 1–2 short clarifying questions and incorporate answers.
- **Requirements:** Produce a short **requirements** section the human can approve:
  - **User-facing outcomes** (e.g. "User can see a list of X", "API returns Y when Z").
  - **Acceptance criteria** (testable conditions; 3–7 bullets).
  - **Out of scope** for this project/session (1–3 bullets).
  - **Technical constraints** if relevant (stack, env, performance).

Then output **Gate 1: Requirements**:

```
--- HUMAN REVIEW: REQUIREMENTS ---
Please review the requirements above. Reply with one of:
- "Approved" or "Go ahead" → I will proceed to iteration planning and first development cycle.
- "Refine: [your feedback]" → I will update requirements and show again (then ask for approval).
- "Abort" → I will stop.
--- END GATE ---
```

**Stop.** Do not start development until the user has approved the requirements (or refined; then re-output requirements and Gate 1 again).

---

## Phase 1: Iteration planning

- Invoke the **planner** subagent with the approved requirements. Get:
  - **Slices** (incremental deliverables, e.g. "Slice 1: API + unit tests", "Slice 2: UI + e2e").
  - For **current slice**: scope, steps, and which test levels apply (unit / integration / e2e per [reference.md](reference.md)).
- Present the iteration plan (current slice + optional next slices). No Gate here unless you want one; the main loop gate is after each development cycle.

---

## Phase 2: Development cycle (loop)

For the **current slice** (or the whole project if it’s small), run this cycle. Repeat until the user says "Complete" or "Next iteration" (and then either start next slice or go to Phase 3).

### 2.1 Develop

- Implement the current slice: code, structure, and minimal docs. Follow project rules.
- Keep the project **runnable** (e.g. `npm run build`, `python -m app` or equivalent). Do not merge/tag/deploy unless the user asks.

### 2.2 Unit tests

- **Write** unit tests for the new/changed logic (per [reference.md](reference.md): fast, isolated, no external I/O).
- **Run** the unit test suite. Fix failures until unit tests pass. Report: how many, pass/fail.

### 2.3 Integration tests (if applicable)

- If the slice involves APIs, DB, or services: **write** integration tests that hit real or test doubles (per [reference.md](reference.md)).
- **Run** integration tests. Fix failures until they pass. Report: how many, pass/fail. If the project has no integration test harness yet, add minimal setup or document "Integration tests: manual steps for now" and skip automated run.

### 2.4 E2E or manual test

- If the slice is user-facing or has a critical path: **write** e2e tests (e.g. Playwright, Cypress) or a **manual test checklist** (steps the human can run). See [reference.md](reference.md).
- **Run** e2e if present; otherwise present the checklist. Report: e2e pass/fail or "Please run manual checklist and report back."

### 2.5 Verify and build

- Invoke the **verifier** subagent: confirm implementation matches the slice scope, tests run, and nothing obvious is broken.
- Ensure **build and run** succeed (e.g. `npm run build && npm start` or project equivalent). Summarize: build OK, run OK or issues found.

### 2.6 Feedback gate (Gate 2)

Produce a **short iteration summary** for the human:

- What was built this cycle (current slice).
- Unit / integration / e2e (or manual) results.
- How to run and try the project (command or link).
- Suggested "next" (next slice or "ready for completion" if done).

Then output **Gate 2: Iteration feedback**:

```
--- HUMAN REVIEW: ITERATION ---
Please try the project and review this iteration. Reply with one of:
- "Approved" or "Next iteration" → I will start the next slice (or go to Phase 3 if no more slices).
- "Feedback: [your feedback]" → I will address your feedback and re-run this development cycle (develop → unit → integration → e2e → verify → this gate again). Loop until you say "Approved" or "Next iteration".
- "Complete" → I will proceed to Phase 3 (completion). Use this when the project is good enough to ship or hand off.
- "Abort" → I will stop.
--- END GATE ---
```

**Stop.** Do not proceed to the next slice or Phase 3 until the user replies.

- **If "Feedback: ...":** Apply feedback, then run **2.1 → 2.2 → 2.3 → 2.4 → 2.5 → 2.6** again (same slice). Loop until they say "Approved", "Next iteration", or "Complete".
- **If "Approved" or "Next iteration":** If there is a next slice, go to Phase 1 (iteration planning for next slice) and then Phase 2 for that slice. If no more slices, go to Phase 3.
- **If "Complete":** Go to Phase 3.
- **If "Abort":** Stop; no Phase 3.

---

## Phase 3: Completion (after "Complete" or final approval)

Run **only** when the user said "Complete" or approved the final iteration with no more slices.

- **Completion checklist:** Tests (unit/integration/e2e) pass, project builds and runs, docs/README updated, env/config documented.
- **Release notes / changelog:** Draft release notes or changelog entry. Do not push or tag unless the user asks.
- **Handoff:** What the human does next (deploy, open PR, run in production). Do not run deploy or destructive commands unless the user explicitly instructs.

If the user said "Abort" at any gate, confirm abort and do not run Phase 3.

---

## Loop summary

- **Gate 1 (requirements):** Approve → continue to Phase 1–2. Refine → re-output requirements and Gate 1 again. Abort → stop.
- **Gate 2 (iteration):** Approved / Next iteration → next slice or Phase 3. Feedback → re-run development cycle (2.1–2.6) and Gate 2 again. Complete → Phase 3. Abort → stop.

Never assume approval. At each gate, wait for the user’s reply. For test levels and when to use unit vs integration vs e2e, see [reference.md](reference.md).
