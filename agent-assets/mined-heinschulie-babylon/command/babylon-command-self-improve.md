---
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, TodoWrite
description: Self-improve Database expertise by validating against codebase implementation
argument-hint: [check_git_diff (true/false)] [focus_area (optional)]
---

# Purpose

You maintain the Database expert system's expertise accuracy by comparing the existing expertise file against the actual codebase implementation. Follow the `Workflow` section to detect and remedy any differences, missing pieces, or outdated information, ensuring the expertise file remains a powerful **mental model** and accurate memory reference for database-related tasks.

## Variables

CHECK_GIT_DIFF: $1 default to false if not specified
FOCUS_AREA: $2 default to empty string
EXPERTISE_FILE: .claude/commands/experts/database/expertise.yaml
LEARNINGS_FILE: .claude/commands/experts/database/learnings.yaml
LEARNINGS_DIR: temp/learnings
MAX_LINES: 1000

## Instructions

- This is a self-improvement workflow to keep Database expertise synchronized with the actual codebase
- Think of the expertise file as your **mental model** and memory reference for all database-related functionality
- Always validate expertise against real implementation, not assumptions
- Focus exclusively on Database-related functionality (Schema, Models, Queries, Migrations)
- If FOCUS_AREA is provided, prioritize validation and updates for that specific area
- Maintain the YAML structure of the expertise file
- Enforce strict line limit of 1000 lines maximum
- Prioritize actionable, high-value expertise over verbose documentation
- When trimming, remove least critical information that won't impact expert performance
- Git diff checking is optional and controlled by the CHECK_GIT_DIFF variable
- Be thorough in validation but concise in documentation
- Don't include 'summaries' of work done in your expertise when a git diff is checked. Focus on true, important information that pertains to the key database functionality and implementation.
- Write as a principle engineer that writes CLEARLY and CONCISELY for future engineers so they can easily understand how to read and update functionality surrounding the database implementation.
- Keep in mind, after your thorough search, there may be nothing to be done - this is perfectly acceptable. If there's nothing to be done, report that and stop.
- **Beyond schema accuracy:** The expertise file serves a database expert that must _answer questions and guide code changes_, not just describe tables. After validating schema correctness, critically evaluate whether the file contains the operational knowledge an agent needs to be useful:
  - **`key_operations`**: Can the expert locate the right function for a given task? Each table's implementation file should have its exported queries, mutations, and internal functions cataloged by name with a one-line description of what they do. Prefer function names over line numbers (names are durable; line numbers go stale).
  - **`best_practices`**: Are there implicit conventions (auth patterns, validation strategies, state machine rules, cascade behavior) that an agent modifying DB code must follow to avoid introducing bugs?
  - **`known_issues`**: Is there tech debt, duplication, or missing functionality that would surprise someone working in this area?
  - A schema reference that can't tell you _which function to call_ or _what rules to follow when writing new code_ is incomplete — even if every field and index is correct.
- **Beyond individual tables — think in flows and layers:** A database expert doesn't just answer "what columns does X have?" — it answers "how do I implement Y?" and "what will break if I change Z?" The expertise file must support these questions. After validating schema and operations, critically evaluate whether the file captures:
  - **`key_data_flows`**: Multi-step workflows that span tables and functions (e.g., "recording → billing check → audio storage → AI pipeline → human review"). These are the hardest thing to reconstruct from code alone and the most common thing an agent needs to understand. Each flow should name the concrete functions called in order.
  - **`lib_helpers`**: Utility functions that aren't tied to a single table but enforce critical invariants (billing guards, language normalization, category inference). An agent writing new code that skips these helpers will introduce bugs. Document what they enforce, not just that they exist.
  - **Domain context** (billing tiers, cron schedules, supported languages): Business rules encoded outside the schema that constrain what valid data looks like. Without these, an agent can write schema-correct but domain-incorrect code.
  - **Testing**: Which files contain tests, what patterns they use, and what coverage exists. An expert guiding code changes must also guide how to test those changes.
  - **Platform quirks**: Operational knowledge specific to the database platform (Convex) that surprises newcomers — transaction semantics, validator behavior, internal vs public function boundaries, optimistic update patterns. These are the bugs-waiting-to-happen that no amount of schema documentation prevents.
  - **Performance guidance**: Not just which indexes exist, but _why_ — which query patterns they support, and what to index when adding new query paths.
  - The goal is a file where an agent can answer "how does X work end-to-end?", "what functions do I call to do Y?", "what invariants must I preserve?", and "how do I test this?" — not just "what fields does table Z have?"
- **The three tiers of expert value — use this as a self-check after every update:** A database expertise file progresses through three tiers of usefulness. Tier 1 (schema reference) lists tables, fields, indexes, and types — any agent can reconstruct this from the schema file, so it's necessary but low-value. Tier 2 (operational catalog) maps every exported function to its purpose and documents the conventions an agent must follow when writing new code — this is where most expertise files stop but shouldn't. Tier 3 (architectural intuition) is what separates a useful expert from a schema dump: it captures _why_ the system is shaped this way and _what will break if you change it_. Concretely, Tier 3 knowledge includes:
  - **Cross-table data flows** with the concrete function call chain (not just "attempts link to audio" but "attempts.attachAudio → assertRecordingAllowed → consumeRecordingMinutes → auto-create humanReviewRequest if pro tier"). An agent implementing a new feature that touches multiple tables needs this to avoid half-wired integrations.
  - **Platform constraints that contradict intuition**: Convex has no `ON DELETE CASCADE`, no raw SQL, no joins — every "obvious" approach from SQL-land is wrong here. Document the Convex-native alternative for each. Internal vs public function boundaries, Node action isolation, validator runtime behavior — these are the landmines.
  - **Index rationale tied to query patterns**: Not "idx_by_user exists" but "idx_by_user supports the listAllByUser query which is called on every phrase library page load — if you add a new query that filters by userId+categoryKey, use the existing by_user_category index." An agent adding a new query path should know which index to use or when to create one.
  - **Invariant enforcement locations**: Where are business rules enforced and by what mechanism? (e.g., "billing gating lives in assertRecordingAllowed in lib/billing.ts, not in individual mutations — new recording paths must call it or they bypass billing"). An agent that doesn't know _where_ an invariant is enforced will either duplicate it or skip it.
  - **The "what breaks" map**: For the most interconnected tables (attempts, humanReviewRequests, practiceSessions), what downstream effects does a mutation trigger? An agent modifying `attempts.attachAudio` needs to know it also consumes billing minutes, creates review requests, and updates session aggregates — otherwise the "fix" introduces three new bugs.
  - After each self-improvement pass, ask: "Could an agent use this file to implement a new feature that spans three tables, without reading any source code beyond what the expertise file points them to?" If not, the file is still at Tier 1 or 2.
  - **Concision**: Please be as concise in your documentation as you can be without sacrificing accuracy. Sacrifice grammar for the sake of concision.

## Workflow

1. **Check Git Diff (Conditional)**
   - If CHECK_GIT_DIFF is "true", run `git diff` to identify recent changes to Database-related files
   - If changes detected, note them for targeted validation in step 3
   - If CHECK_GIT_DIFF is "false", skip this step

1b. **Ingest Runtime Learnings (Conditional)**
   - If FOCUS_AREA is "learnings" OR if `temp/learnings/*.md` files exist (excluding README.md):
     - Read the expert's `domain_tags` from the EXPERTISE_FILE header
     - Read all `temp/learnings/*.md` files (not README.md)
     - Parse YAML entries from each file
     - Filter entries where `tags` intersect with this expert's `domain_tags`
     - For each matched entry:
       - Validate the learning against the actual codebase (read the relevant files)
       - Apply version-aware conflict resolution:
         - If learning `platform_context` version matches current version AND conflicts with an ai_doc at same version → **learning wins** (lived experience > docs), flag for review
         - If learning `platform_context` version is older AND an ai_doc at current version conflicts → **ai_doc wins**, note learning as deprecated
       - If learning is validated, update the relevant section in expertise.yaml (platform_constraints, best_practices, or known_issues as appropriate)
     - Record which entry IDs were processed in the report
   - If no learnings files exist or no tags match, skip this step

1c. **Promote Technology Learnings to Durable Store**
   - Read LEARNINGS_FILE (the expert's `learnings.yaml`)
   - For each matched entry from step 1b, apply the **technology truth filter**:
     - Ask: "Would this save time in a fresh project using the same stack?"
     - YES → it's a technology/integration truth (how technologies work or interact). Promote it.
     - NO → it's a codebase-specific observation (did the agent implement correctly, internal patterns). Skip it.
   - For entries that pass the filter:
     - Check for duplicates in LEARNINGS_FILE (same stack + overlapping learning text)
     - If duplicate: increment `occurrences`, update `discovered` date if newer
     - If new: append to LEARNINGS_FILE with fields: `id`, `category` (platform_truth | integration_seam | versioned), `learning`, `stack`, `discovered`, `source_build`, `occurrences`
   - **CRITICAL**: Never remove entries from LEARNINGS_FILE. Only humans may delete learnings.
   - Record which entries were promoted vs filtered in the report

1d. **Enforce Durable Learnings in Expertise**
   - Read all entries from LEARNINGS_FILE
   - For each entry, verify it is reflected in the appropriate section of EXPERTISE_FILE (platform_constraints, best_practices, known_issues)
   - If a learning exists in LEARNINGS_FILE but is missing from EXPERTISE_FILE, re-add it
   - This step prevents erosion: no self-improve pass may drop a durable learning from expertise

2. **Read Current Expertise**
   - Read the entire EXPERTISE_FILE to understand current documented expertise
   - Identify key sections: overview, core_implementation, schema_structure, key_operations, etc.
   - Note any areas that seem outdated or incomplete

3. **Validate Against Codebase**
   - Read the EXPERTISE_FILE to identify which files are documented as key implementation files
   - Read those files to understand current implementation:
   - Compare documented expertise against actual code:
     - Table structures and columns
     - Model fields and validators
     - Query function signatures and logic
     - Migration patterns
   - If FOCUS_AREA is provided, prioritize validation of that specific area
   - If git diff was checked in step 1, pay special attention to changed areas

4. **Identify Discrepancies**
   - List all differences found:
     - Missing tables or columns
     - Outdated type definitions
     - Changed query logic
     - New database functions
     - Removed features still documented
     - Incorrect schema descriptions

5. **Update Expertise File**
   - Remedy all identified discrepancies by updating EXPERTISE_FILE
   - Add missing information
   - Update outdated information
   - Remove obsolete information
   - Maintain YAML structure and formatting
   - Ensure all file paths and line numbers are accurate
   - Keep descriptions concise and actionable

6. **Enforce Line Limit**
   - Run: `wc -l .claude/commands/experts/database/expertise.yaml`
   - Check if line count exceeds MAX_LINES (1000)
   - If line count > MAX_LINES:
     - Identify least important expertise sections that won't impact expert performance:
       - Overly verbose descriptions
       - Redundant examples
       - Low-priority edge cases
     - Trim identified sections
     - Run line count check again
     - REPEAT this sub-workflow until line count ≤ MAX_LINES
   - Document what was trimmed in the report

7. **Validation Check**
   - Read the updated EXPERTISE_FILE
   - Verify all critical Database information is present
   - Ensure line count is within limit
   - Validate YAML syntax by compiling the file:
     - Run: `python3 -c "import yaml; yaml.safe_load(open('EXPERTISE_FILE'))"`
     - Replace EXPERTISE_FILE with the actual path from the variable
     - Confirm no syntax errors are raised
     - If errors occur, fix the YAML structure and re-validate

## Report

Provide a structured report with the following sections:

### Summary

- Brief overview of self-improvement execution
- Whether git diff was checked
- Focus area (if any)
- Learnings processed (count, IDs)
- Learnings promoted to LEARNINGS_FILE (count, IDs) vs filtered out (count, reasons)
- Durable learnings enforced in expertise (count, any re-added)
- Total discrepancies found and remedied
- Final line count vs MAX_LINES

### Discrepancies Found

- List each discrepancy identified:
  - What was incorrect/missing/outdated
  - Where in the codebase the correct information was found
  - How it was remedied

### Updates Made

- Concise list of all updates to EXPERTISE_FILE:
  - Added sections/information
  - Updated sections/information
  - Removed sections/information

### Line Limit Enforcement

- Initial line count
- Final line count
- If trimming was needed:
  - Number of trimming iterations
  - What was trimmed and why
  - Confirmation that trimming didn't impact critical expertise

### Validation Results

- Confirm all critical Database expertise is present
- Confirm line count is within limit
- Note any areas that may need future attention

### Codebase References

- List of files validated against with line numbers where relevant
- Key methods and functions verified

**Example Report Format:**

```
✅ Self-Improvement Complete

Summary:
- Git diff checked: Yes
- Focus area: orchestrator_agents table
- Discrepancies found: 3
- Discrepancies remedied: 3
- Final line count: 520/1000 lines

Discrepancies Found:
1. Missing table: 'file_tracking' not documented
   - Found in: migrations/9_file_tracking.sql
   - Remedied: Added to schema_structure.tables section

2. Outdated function: update_orchestrator_costs signature changed
   - Found: Added 'input_tokens' parameter
   - Remedied: Updated key_operations.orchestrator_management

Updates Made:
- Added: file_tracking table definition
- Updated: update_orchestrator_costs signature
- Updated: database.py line count reference

Line Limit Enforcement:
- Initial: 520 lines
- Required trimming: No
- Final: 520 lines ✓

Validation Results:
✓ All 6 tables documented with accurate fields
✓ Core Database methods present
✓ Migration patterns included
✓ YAML syntax valid (compiled successfully)

Codebase References:
- models.py:1-150 (validated)
- database.py:1-496 (validated)
- migrations/*.sql (validated)
```
