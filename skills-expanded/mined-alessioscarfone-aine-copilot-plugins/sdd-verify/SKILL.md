---
name: sdd-verify
description: 'Compare code changes against spec requirements, validate task completion, and check design alignment before archiving a change. Use when a change has been implemented and you want to review my changes, check before merge, validate my implementation, or get a QA check before closing out. Do not use for implementing changes, creating artifacts, or archiving without prior verification.'
---

Verify that an implementation matches the change artifacts (specs, tasks, design).

**Input**: Optionally specify a change name after `/sdd-verify` (e.g., `/sdd-verify add-auth`). If omitted, check if it can be inferred from conversation context. If vague or ambiguous you MUST prompt for available changes.

Before writing, read the shared project documents for context:
- {ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/prd.md — product requirements, user journeys, functional requirements
- {ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/architecture.md — tech stack, architectural decisions, naming conventions
- {ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/ux.md — UX design decisions, component inventory (if exists)

**Steps**

1. **If no change name provided, prompt for selection**

   List directories in `{ARTIFACT_MAIN_FOLDER}/{CHANGE_SUBFOLDER}/` (excluding `archive`) to get available changes. Use the **AskUserQuestion tool** to let the user select.

   Show changes that have implementation tasks (`tasks.md` exists).
   Mark changes with incomplete tasks as "(In Progress)".

   **IMPORTANT**: Do NOT guess or auto-select a change. Always let the user choose.

2. **Inspect the change directory**

   List files in `{ARTIFACT_MAIN_FOLDER}/{CHANGE_SUBFOLDER}/<name>/` to see which artifacts are present (`proposal.md`, `design.md`, `tasks.md`, `specs/`).

3. **Load all available artifacts**

   Read all files found in `{ARTIFACT_MAIN_FOLDER}/{CHANGE_SUBFOLDER}/<name>/` and its subdirectories.

4. **Verify Completeness**

   **Task Completion**:
   - If tasks.md exists in contextFiles, read it
   - Parse checkboxes: `- [ ]` (incomplete) vs `- [x]` (complete)
   - Count complete vs total tasks
   - If incomplete tasks exist:
     - Add CRITICAL issue for each incomplete task
     - Recommendation: "Complete task: <description>" or "Mark as done if already implemented"

   **Spec Coverage**:
   - If delta specs exist in `{ARTIFACT_MAIN_FOLDER}/{CHANGE_SUBFOLDER}/<name>/{SPECS_SUBFOLDER}/`:
     - Extract all requirements (marked with "### Requirement:")
     - For each requirement:
       - Search codebase for keywords related to the requirement
       - Assess if implementation likely exists
     - If requirements appear unimplemented:
       - Add CRITICAL issue: "Requirement not found: <requirement name>"
       - Recommendation: "Implement requirement X: <description>"

5. **Verify Correctness**

   **Requirement Implementation Mapping**:
   - For each requirement from delta specs:
     - Search codebase for implementation evidence
     - If found, note file paths and line ranges
     - Assess if implementation matches requirement intent
     - If divergence detected:
       - Add WARNING: "Implementation may diverge from spec: <details>"
       - Recommendation: "Review <file>:<lines> against requirement X"

   **Scenario Coverage**:
   - For each scenario in delta specs (marked with "#### Scenario:"):
     - Check if conditions are handled in code
     - Check if tests exist covering the scenario
     - If scenario appears uncovered:
       - Add WARNING: "Scenario not covered: <scenario name>"
       - Recommendation: "Add test or implementation for scenario: <description>"

6. **Verify Coherence**

   **Design Adherence**:
   - If design.md exists in contextFiles:
     - Extract key decisions (look for sections like "Decision:", "Approach:", "Architecture:")
     - Verify implementation follows those decisions
     - If contradiction detected:
       - Add WARNING: "Design decision not followed: <decision>"
       - Recommendation: "Update implementation or revise design.md to match reality"
   - If no design.md: Skip design adherence check, note "No design.md to verify against"

   **Code Pattern Consistency**:
   - Review new code for consistency with project patterns
   - Check file naming, directory structure, coding style
   - If significant deviations found:
     - Add SUGGESTION: "Code pattern deviation: <details>"
     - Recommendation: "Consider following project pattern: <example>"

7. **Generate Verification Report**

   Use three issue severities: **CRITICAL** (must fix before archive), **WARNING** (should fix), **SUGGESTION** (nice to fix).

   ```
   ## Verification Report: <change-name>

   ### Summary
   | Dimension    | Status           |
   |--------------|------------------|
   | Completeness | X/Y tasks, N reqs|
   | Correctness  | M/N reqs covered |
   | Coherence    | Followed/Issues  |
   ```

   List issues by severity, each with a specific, actionable recommendation and file/line reference where applicable.

   **Final Assessment**:
   - If CRITICAL issues: "X critical issue(s) found. Fix before archiving."
   - If only warnings: "No critical issues. Y warning(s) to consider. Ready for archive (with noted improvements)."
   - If all clear: "All checks passed. Ready for archive."

8. **Update tracker on full pass**

   If the Final Assessment has **no CRITICAL issues** (all clear or warnings only), follow the **`sdd-tracker` skill** to set the change status to `verified` with changelog note `"Verification passed"` and suggest proceeding with archiving.

   If CRITICAL issues were found, do **not** update the tracker — the status remains unchanged.

**Verification approach**: Focus on objective checkboxes for completeness; use keyword search and reasonable inference for correctness (avoid false CRITICAL — prefer SUGGESTION over WARNING, WARNING over CRITICAL when uncertain); check for glaring inconsistencies in coherence, not style.

**Graceful degradation**: Verify only what exists — tasks only (if no specs/design), tasks + specs (if no design), or all three dimensions (full artifacts). Always note which checks were skipped.

**Output format**: Use markdown tables for the scorecard; `file.ts:123` notation for code references; specific, actionable recommendations (no vague suggestions like "consider reviewing").
