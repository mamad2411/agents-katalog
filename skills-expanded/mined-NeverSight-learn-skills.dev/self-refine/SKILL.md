---
name: self-refine
version: 1.0.0
description: >-
  Iterative self-critique with structured verification. Prevents shallow
  one-shot answers. Use when you need depth, iteration, self-review, verified
  delivery, or high-stakes output. /self-refine
---

# Self-Refine — Iterative Execution with Self-Critique

Never treat a first draft as the final output. For any non-trivial task, work in
visible phases: draft → verify → fix → deliver.

## Before / After

**Without this skill:**
> User: "Analyze the pros and cons of approach A vs B."
> Agent: Writes a long analysis, ends with "In conclusion, A is better." No
> self-check, no assumptions listed, no acknowledgment of gaps.

**With this skill:**
> Agent: States the goal and DoD → drafts analysis → runs a checklist (any
> missing angles? unsupported claims? weakest assumption?) → fixes two gaps →
> delivers final version with a change log and remaining caveats.

---

## Complexity Grading

Assess complexity first to decide how much process to apply:

| Level | Characteristics | Process |
|-------|----------------|---------|
| **Light** | Single fact, one-liner, clear short answer | Restate goal → answer directly (still no fabrication) |
| **Medium** | Multi-step reasoning, some ambiguity | Full 7 steps, 1–2 self-check rounds |
| **Heavy** | Deep analysis, high risk, many unknowns | Full 7 steps, up to 3 rounds, multi-path exploration |

If the user explicitly wants speed: declare "Light mode" and deliver. Otherwise default to Medium or above.

---

## Core Rules

1. **First draft ≠ final draft.** Must pass at least one self-check before marking anything as final.
2. **Fixed sequence:** Understand → Decompose → Draft → Verify → Iterate → Deliver. Never skip verification.
3. **Not done until done.** If the Definition of Done is not met, either iterate or explicitly list what remains unfinished and why.
4. **Iteration cap: 3 rounds.** If still not satisfactory, stop, state remaining risks, and ask the user to decide.

---

## Workflow (7 Steps)

### 1. Reframe the Task
- Restate the goal in your own words.
- Surface **implicit requirements** (audience, format, boundaries).
- Write a **Definition of Done (DoD):** a checkable list of acceptance criteria.

### 2. Decompose
- Break into smallest executable units. Tag **dependencies** and **risk points**.

### 3. First Draft
- Produce version 1. Mark **assumptions** and **uncertain parts**.
- For **Heavy** tasks: explore 2–3 reasoning paths on key decision points, compare, then pick the best to develop further.

### 4. Self-Check (Critical)
Run through the DoD item by item:
- Anything missing? Logic gaps or contradictions? Which items pass, which fail?
- **Assumption reversal test:** If a key assumption turns out false, does the conclusion still hold? What is the weakest link?
- Output an **issue list** (itemized, sorted by severity).

### 5. Verify (Checklist)

Go through each item — **PASS** or **FAIL**:

- [ ] Every DoD item addressed?
- [ ] No unsupported claims stated as fact?
- [ ] Assumptions explicitly listed?
- [ ] Weakest link identified and acknowledged?

Any **FAIL** → go to step 6.
All **PASS** → go to step 7.

### 6. Iterate
- Fix each issue from the list (or explain why it cannot be fixed).
- Produce an improved version, **return to step 4**.
- Label "Iteration n / max 3".

### 7. Final Delivery
- Output the final version.
- Attach a **change log** (what was fixed, what limitations remain).
- One sentence: why this meets the DoD.

---

## Implementation Tasks (Code / Repos)

Execute sub-tasks incrementally, but each unit must have a **verifiable output + mini self-check**. Before the final delivery, run the full step 4–5 once. Verification must reference **actual file contents or command output** — never claim "verified" from memory.

---

## What "Multi-Round" Means

This skill does not add extra API calls. "Multi-round" means:
- **Default:** Complete draft → verify → (if needed) iterate → final, all within a single response.
- **Cross-message:** If a single response cannot fit everything, end with "continuing at step X next" and ask the user to say "continue".
- **Forbidden:** Checklist has FAILs but writing "improvements internalized" without showing the actual changes.

---

## Anti-Patterns

- Long draft followed by immediate sign-off, no self-check.
- Self-check says "all good" with no issue list.
- All items PASS but the issue list still has open items.
- Iterating past the cap without stopping.
