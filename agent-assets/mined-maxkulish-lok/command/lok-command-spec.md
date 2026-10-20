# Phase: Specification (Specification Tasks Only)

**Purpose**: Run the `/spec` skill to produce a lean 5-section specification, run AI review (Ollama + synthesis, with a Claude fallback), apply feedback, and checkpoint for approval or upgrade to full design-doc workflow.

**Entry conditions**: `current_phase: spec` (task_type: specification)

---

## Status: pending or awaiting_input

1. **Invoke**: `/spec [task title and description from Linear]`
   - Pass the full Linear task title + description as context
   - The spec skill will explore the codebase, ask clarifying questions, and produce a 5-section specification
   - After completion, update state:
     - `phases.spec.spec_file: specs/[date]-clo-XX-[slug].md` (or wherever spec was saved)
     - `phases.spec.status: reviewing`
     - `workflow.status: in_progress`

---

## Status: reviewing

### Step 2: AI Review of Specification (Ollama + synthesis)

Before presenting the spec to the user for approval, run the same review pattern used in the design phase - adapted for spec documents. A Claude fallback covers the case where the Ollama leg fails.

**2a. Gather context for reviewers**

Build a context block that gives reviewers the problem framing they need:

- **Linear task**: Fetch via `mcp__linear-server__get_issue` (title, description, labels, comments)
- **Spec file**: The spec produced in Step 1
- **Architecture context**: `docs/arch/`, `docs/adrs/` (relevant subset), `.claude/CLAUDE.md` (Core Architecture Principles)

**2b. Build the spec review prompt**

The review prompt lives in `.lok/prompts/spec-review-prompt.md`. No inline prompt needed here.

**2c. Run AI spec reviews via lok**

Run the lok spec-review workflow:

```bash
lok run .lok/workflows/spec-review.toml \
  "[SPEC_FILE_PATH]" \
  "clo-[XX]" \
  "[LINEAR_TITLE]" \
  "[LINEAR_DESCRIPTION]" \
  "[LINEAR_LABELS]" \
  --dir . \
  --verbose
```

This produces:
- `docs/reviews/clo-[XX]-spec-review-ollama.md`
- `docs/reviews/clo-[XX]-spec-review-synthesis.md`
- `docs/reviews/clo-[XX]-spec-review-claude-fallback.md` (only when the Ollama leg failed)

**2c-post. Check review results**

Read `docs/reviews/clo-[XX]-spec-review-synthesis.md`.

- If it contains `NO_REVIEWS_AVAILABLE`: Both models failed. Note "No AI reviews available" and proceed directly to step 2e (checkpoint).
- If one review file contains `REVIEW_FAILED`: One model failed. Note which and proceed with the available review.
- If both valid: Proceed with full synthesis.

Update workflow state:
- `phases.spec.review_ollama: docs/reviews/clo-[XX]-spec-review-ollama.md`
- `phases.spec.review_synthesis: docs/reviews/clo-[XX]-spec-review-synthesis.md`

**2e. Apply review feedback**

Follow the same pattern as design phase feedback application:

1. **Extract actionable items** from both reviews' "Actionable Feedback" sections
2. **Classify each item**:

| Classification | Criteria | Action |
|---------------|----------|--------|
| **Additive** | Missing acceptance criterion, edge case, or test scenario | AUTO-APPLY to spec |
| **Refinement** | Improves clarity, specificity, or scoping of existing items | AUTO-APPLY to spec |
| **Contradicts prior decision** | Recommends approach rejected in ADRs | ASK USER |
| **New risk identified** | Blind spot not covered | AUTO-APPLY (add to constraints or evaluation) |
| **Ambiguous** | Cannot be clearly classified | AUTO-APPLY with `<!-- reviewer note -->` comment |

3. **Apply non-contradicting items** in a single edit pass to the spec file
4. **Handle contradicting items** one at a time (same UI as design phase):
   ```
   REVIEW CONFLICT - Item [N of M]

   Suggestion (from [Ollama|Claude fallback|synthesis]):
     "[exact suggestion text]"

   This conflicts with a prior decision:
     Source: [docs/adrs/adr-XXX.md]
     Decision: "[relevant excerpt]"

   Options:
     1. [skip]  - Keep our prior decision
     2. [apply] - Override and apply
     3. [note]  - Add as open question

   Your choice:
   ```

5. Update state:
   - `phases.spec.review_applied: true`
   - `phases.spec.applied_suggestions: [list]`
   - `phases.spec.flagged_suggestions: [list]` (if any contradictions)
- Add history entry: `spec_review_applied`

Update state: `phases.spec.status: checkpoint`, `workflow.status: checkpoint`

---

## Status: checkpoint

1. Display spec file location and review results
2. Ask user:
   ```
   SPEC CHECKPOINT

   Specification: [spec file path]
   Scope: [S/M/L from spec header]
   Sub-tasks: [count from spec decomposition]

   ---
   AI REVIEW RESULTS

   Ollama verdict:    [APPROVE | APPROVE_WITH_SUGGESTIONS | NEEDS_REVISION]
   Synthesis verdict: [APPROVE | APPROVE_WITH_SUGGESTIONS | NEEDS_REVISION]

   Auto-applied [N] suggestions:
   - [brief description of each applied change]

   User-resolved [M] conflicts:
   - [suggestion] -> [skip|apply|note]

   (If reviews failed: "AI review unavailable - spec unchanged from draft")
   ---

   Please review the spec - all 5 sections should be complete:
   - Problem Statement (self-contained?)
   - Acceptance Criteria (specific + measurable?)
   - Constraints (Must/Must-not/Prefer/Escalate?)
   - Decomposition (independent sub-tasks?)
   - Evaluation (test table complete?)

   Options:
   1. [approve]  - Spec is approved, start implementation directly
   2. [revise]   - I have feedback (will re-invoke /spec)
   3. [view-ollama] - View full Ollama review
   4. [view-synthesis] - View the review synthesis
   5. [upgrade]  - This is more complex than expected, switch to full design-doc workflow
   6. [pause]    - Pause workflow, continue later

   Your choice:
   ```

3. **If approve**:
   - Update state:
     - `phases.spec.approved: true`
     - `phases.spec.status: complete`
     - `workflow.current_phase: implement`
     - `workflow.status: in_progress`
   - Add history entry: `spec_approved`
   - **Continue to IMPLEMENT phase** (skip PLAN phase - spec decomposition IS the plan)

4. **If revise**:
   - Ask for specific feedback
   - Re-invoke `/spec` with feedback context
   - Re-run AI review (return to `status: reviewing`)
   - Return to checkpoint

5. **If view-ollama**: Display `docs/reviews/clo-XX-spec-review-ollama.md`, return to options
6. **If view-synthesis**: Display `docs/reviews/clo-XX-spec-review-synthesis.md`, return to options

7. **If upgrade**:
   - Update state: `task_type: development`
   - Reinitialize phases with design + plan
   - **Continue to DESIGN phase**

8. **If pause**:
   - Save state
   - Exit with resume instructions

---

## YAML Checkpoint (Required before transition)

Before signaling completion to the dispatcher, verify:

```yaml
# --- Spec phase exit fields ---
phases.spec.spec_file: <path>                    # non-null
phases.spec.approved: true
phases.spec.status: complete
phases.spec.review_ollama: <path|null>           # null if review failed/timed out
phases.spec.review_synthesis: <path|null>        # null if review failed/timed out
phases.spec.review_verdict: <verdict|null>       # null if review failed/timed out
phases.spec.review_completed: <true|false>       # false if reviews failed/timed out
phases.spec.review_applied: <true|false>         # false if no reviews or nothing to apply
phases.spec.applied_suggestions: [<list>]        # empty array if none applied
phases.spec.flagged_suggestions: [<list>]        # empty array if no conflicts
```

History must contain `spec_approved` event.
