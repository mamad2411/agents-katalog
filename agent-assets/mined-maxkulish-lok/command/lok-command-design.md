# Phase: Design

**Purpose**: Create design document (informed by discovery phase output), review with multiple AI models, auto-apply feedback, and get user approval.

**Entry conditions**: `current_phase: design`

---

## Status: pending or awaiting_input

1. **Check if design doc exists**: `docs/design-docs/clo-XX-*.md`

2. **If design doc does NOT exist**:
   - Display: "Starting design phase. This will be interactive."
   - Update state: `phases.design.status: in_progress`

   **2a. Load Discovery Context**:

   Check if the discovery phase produced artifacts:
   - Read `phases.discovery.discovery_report` from workflow YAML
   - Read `phases.discovery.approach_chosen` from workflow YAML
   - Read `phases.discovery.prd_file` from workflow YAML

   If discovery was completed (not skipped):
   - Display: "Using discovery report and chosen approach as design input."
   - The discovery report, PRD, and chosen approach will be passed to `/design-doc:create` as context.

   If discovery was skipped:
   - Display: "Discovery was skipped. Proceeding with Linear task context only."

   **2b. Check task complexity for Specification Engineering**:
   - Check if Linear task has 3+ subtasks (via `mcp__linear-server__get_issue`)
   - If task has 3+ subtasks OR description references multiple distinct components:
     ```
     SPECIFICATION CHECK

     This task appears complex (subtasks: N / multiple components detected).

     Before creating the design doc, run /spec to produce a self-contained
     autonomous task blueprint (acceptance criteria, constraint architecture,
     decomposition into ~2-hour subtasks).

     Run /spec first? (yes/no/skip)
     - yes: Run /spec CLO-XX now, then continue to design doc
     - no: Proceed directly to design doc
     - skip: Always skip this check for future tasks this session
     ```
   - If user selects **yes**: Invoke `/spec CLO-XX`, wait for completion, then continue
   - If user selects **no** or task has <3 subtasks: Proceed directly

   - **Invoke**: `/design-doc:create CLO-XX --discovery`
     (The `--discovery` flag tells create to include discovery phase output in the Background > Prior Research section.
     It reads the discovery report path from the workflow YAML and incorporates the chosen approach,
     prior-art findings, assumption map, and stress test results into the design doc context.)
   - After completion, update state:
     - `phases.design.design_doc: [path]`
     - `phases.design.draft_ready: true`
   - Add history entry: `design_draft_ready`
   - **Invoke AI Review**: `/design-doc:review CLO-XX`
     - Display: "Running automated AI review (Ollama, with Claude fallback, up to 5 minutes)..."
     - Wait for the review and its synthesis to complete
     - Update state:
       - `phases.design.review_ollama: docs/reviews/clo-XX-review-ollama.md`
       - `phases.design.review_synthesis: docs/reviews/clo-XX-review-synthesis.md`
       - `phases.design.review_verdict: [synthesis verdict]`
       - `phases.design.review_completed: true`
     - Add history entry: `design_review_complete`
     - **If the review and its fallback both fail**: Skip apply step, continue to checkpoint (review is advisory)
   - **Apply Review Feedback** (see section below)
   - Update state:
     - `phases.design.status: checkpoint`
     - `workflow.status: checkpoint`

3. **If design doc exists but not finalized**:
   - Display: "Design document exists but not finalized."
   - **If `review_completed: false`**: Run `/design-doc:review CLO-XX` then Apply Review Feedback
   - **If `review_completed: true` but `review_applied: false`**: Run Apply Review Feedback only
   - Update state: `phases.design.status: checkpoint`

---

## Apply Review Feedback

This step runs automatically after both review files are written. It reads, consolidates, and acts on the actionable items from both AI reviewers without waiting for the user - **except** when a suggestion contradicts a documented prior decision.

**Prior decision sources to load** (read these files before classifying any suggestion):
- `docs/adrs/` - Architecture Decision Records (61 files)
- `docs/investigations/` - Spike results and technology evaluations
- `docs/context/system-patterns.md` - Active patterns and invariants
- `.claude/CLAUDE.md` - Core Architecture Principles and Intent sections

**Step 1 - Extract actionable items from both reviews**

Read the `## 8. Actionable Feedback` section from each review file. Build a combined list. Where the same point appears in both reviews, mark it as **high-confidence**.

**Step 2 - Classify each item**

For each actionable item, determine its classification:

| Classification | Criteria | Action |
|---------------|----------|--------|
| **Additive** | Fills a gap in the design doc (missing section, missing AC, missing edge case) | AUTO-APPLY |
| **Refinement** | Improves clarity, adds specificity, corrects typos or vague language | AUTO-APPLY |
| **Contradicts prior decision** | Recommends technology/pattern explicitly evaluated and rejected in docs/ | ASK USER |
| **New risk identified** | Points out a risk or blind spot not covered in docs/ | AUTO-APPLY (add to risks section) |
| **Ambiguous** | Cannot be clearly classified | AUTO-APPLY with inline `<!-- reviewer note: ... -->` comment |

**lok-specific contradiction heuristics** - flag for user if suggestion recommends:
- Breaking the Backend trait interface without migration path
- Adding unsafe code blocks without justification
- Hardcoding API keys or secrets (must use env vars + SecretString)
- Blocking the tokio runtime with sync operations
- Adding telemetry or analytics dependencies
- Breaking the existing CLI interface contract

**Step 3 - Apply non-contradicting items**

Edit the design document in a single pass. For each AUTO-APPLY item:
- Add missing acceptance criteria to the AC list
- Expand incomplete sections
- Add edge cases to the implementation plan
- Add identified risks to security/performance sections
- Fix vague language

After the pass, update state:
- `phases.design.review_applied: true`
- `phases.design.applied_suggestions: [list of what was applied, one line each]`
- Add history entry: `review_applied`

**Step 4 - Handle contradicting items (ASK USER)**

If any contradicting items were found, present them **one at a time**:

```
REVIEW CONFLICT - Item [N of M]

Suggestion (from [Ollama|Claude fallback|synthesis]):
  "[exact suggestion text]"

This conflicts with a prior decision:
  Source: [docs/adrs/adr-002-in-process-whisper.md]
  Decision: "[relevant excerpt from that document]"

Options:
  1. [skip]  - Keep our prior decision, ignore this suggestion
  2. [apply] - Override the prior decision and apply the suggestion
  3. [note]  - Add suggestion as an open question in the design doc

Your choice:
```

After all items are resolved, update state:
- `phases.design.flagged_suggestions: [list with user's choice for each]`
- Add history entry: `review_conflicts_resolved`

---

## Status: checkpoint

1. Display design document location
2. Display AI review results and what was applied
3. Ask user:
   ```
   DESIGN CHECKPOINT

   Design document: docs/design-docs/clo-XX-[description].md

   ---
   AI REVIEW RESULTS

   Ollama verdict:    [APPROVE | APPROVE_WITH_SUGGESTIONS | NEEDS_REVISION]
   Synthesis verdict: [APPROVE | APPROVE_WITH_SUGGESTIONS | NEEDS_REVISION]

   Auto-applied [N] suggestions:
   - [brief description of each applied change]

   User-resolved [M] conflicts:
   - [suggestion] -> [skip|apply|note] (reason: prior decision in [source])

   (If reviews failed: "AI review unavailable - design doc unchanged from draft")
   ---

   Please review the updated design document.

   Options:
   1. [approve] - Design is approved, finalize it
   2. [feedback] - I have changes to make
   3. [view-ollama] - View full Ollama review
   4. [view-synthesis] - View the review synthesis
   5. [pause] - Pause workflow, continue later

   Your choice:
   ```

4. **If view-ollama**: Display `docs/reviews/clo-XX-review-ollama.md`, return to options
5. **If view-synthesis**: Display `docs/reviews/clo-XX-review-synthesis.md`, return to options

6. **If approve**:
   - **Invoke**: `/design-doc:finalize CLO-XX`
   - Update state:
     - `phases.design.finalized: true`
     - `phases.design.status: complete`
     - `workflow.current_phase: plan`
     - `workflow.status: in_progress`
   - Add history entry: `design_finalized`
   - **Continue to PLAN phase**

7. **If feedback**:
   - Ask for specific feedback
   - Update design document
   - Stay in checkpoint state

8. **If pause**:
   - Save state
   - Exit with resume instructions

---

## YAML Checkpoint (MANDATORY before advancing to plan phase)

Before setting `workflow.current_phase: plan`, write ALL of the following fields to the workflow YAML in a single update:

```yaml
# --- Design phase exit fields ---
phases.design.status: complete
phases.design.design_doc: <path to docs/design-docs/clo-XX-*.md>
phases.design.draft_ready: true
phases.design.discovery_context_used: <true|false>  # whether discovery report was available
phases.design.review_ollama: <path|null>            # null if review failed/timed out
phases.design.review_synthesis: <path|null>         # null if review failed/timed out
phases.design.review_verdict: <verdict|null>        # null if review failed/timed out
phases.design.review_completed: <true|false>        # false if reviews failed/timed out
phases.design.review_applied: <true|false>          # false if no reviews or nothing to apply
phases.design.applied_suggestions: [<list>]         # empty array if none applied
phases.design.flagged_suggestions: [<list>]         # empty array if no conflicts
phases.design.finalized: true
workflow.current_phase: plan
workflow.status: in_progress
```

If any field cannot be determined, set it to `null` with a YAML comment explaining why.
Do NOT advance to the plan phase until every field above is written.
