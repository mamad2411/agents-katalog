---
name: implement-next-phase
description: Prepare to implement the next pending todo phase from a solutionize sketch plan (frontmatter todos); implementation only after explicit user approval.
disable-model-invocation: true
metadata:
  dependencies: sketch
  dependents: modify-sketch
---

## Invoking this skill

Use when the partner attaches this skill and provides the **sketch plan** path. That plan includes YAML **`todos`** (one per phase, each **`content`** matches the corresponding **`### Phase N - …`** heading in **`## Sketch`**) plus a **`## Sketch`** section in the file body.

**Non-negotiable:** Until the partner **explicitly approves** proceeding (for example: "go ahead," "implement," "proceed with Phase 2"), you **do not** edit application code, tests, config, or assets for the work. Preparation (reading, searching, analysis, questions) is allowed; building is not, until that approval.

**Chat during preparation:** Do **not** deliver a research report, findings recap, or summary of what you learned. Do **not** restate or summarize the sketch, the plan, or the codebase in chat. The partner already has the plan. In chat, write **only**: **concise** questions when something blocks you or is unclear; **brief** asks when the plan or `todos` need fixing; and—when you have **no** further questions—a **single short line** requesting approval to implement, naming the active phase by its todo **`content`** (for example: ready to implement `Phase 1 - …` when you approve). No other preparation prose in chat.

---

## Git staging (before each phase cycle)

Every time this skill starts a **fresh phase cycle**—the first pending phase in the plan, or the next pending phase after earlier ones were implemented—run `git add -A`, then read and prepare. Do not commit. Do not begin step 1 below until staging is done.

This checkpoints work from the prior phase (or any other unstaged edits) before new preparation or implementation begins.

---

## First actions, in order

1. **Read the sketch plan file** the partner gave you. Parse YAML **frontmatter** and read the file body (**`## Sketch`** section).

2. **Pick the active phase from `todos`:** Take the **first** todo whose status is **`pending`** (or unset / not **`completed`**). That todo's **`content`** is the active phase label. If **`todos`** is missing, empty, or there is **no** pending item, **stop** and ask the partner to fix the plan or supply a proper solutionize sketch before continuing.

3. **Orient to the sketch:** In **`## Sketch`**, open the **`### Phase N - …`** section whose heading text matches the active todo **`content`**; read that section's **Objective** and bullets for implementation scope. If **no** heading matches, **stop** and ask the partner to align todos with the sketch. Skim earlier phases in the sketch for ordering and dependencies.

4. **Gather context (read-only):**
   - Read completed-phase material the partner points to, or earlier sections of the same plan if they record what was done.
   - Open files linked or named in the sketch for this phase; follow callers/callees as needed.
   - Use search and repo reads until **you** could implement without guessing. Keep that picture **internal**; do not write it to chat.

5. **Reconcile and question:** If research **contradicts** the sketch, omits something the code requires, or surfaces anything **odd** (missing symbols, wrong paths, tests that no longer match), ask **one tight question** (or a minimal set) in chat—no surrounding narrative. If anything in the phase is **vague or ambiguous**, ask the same way rather than assume.

6. **Handoff when ready:** If you still have open questions, stay on step 5; do not ask for approval until they are resolved. When you have **no** further questions, send **only** the short approval-request line described under **Chat during preparation** (phase named by todo **`content`**). **Stop.** Do not implement until the partner explicitly approves.

---

## After approval

When the partner approves, implement **only** that phase per the sketch and prior answers; keep scope tight. If approval was for a specific phase number, do not roll forward into the next phase without a new cycle of this skill or explicit instruction.

**No cross-phase scaffolding:** Do not change code so this phase can stand alone when the sketch defers work to a later phase. Do not add defaults, placeholders, temporary checks, stubs, no-ops, or similar bridging work to paper over gaps between this phase and a future one—**unless** the sketch explicitly requires that in this phase.

**Immediately after** your implementation edits for that phase, edit the sketch plan file: set the active phase's todo **`status`** to **`completed`** in YAML frontmatter. Do this before any other follow-up work on the plan or codebase.