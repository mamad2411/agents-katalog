---
name: "deep-dive-sp-analysis-for-stories"
description: "Master workflow to analyze stored procedures for epic/story documentation - locate SPs, extract logic, create traceability, resolve SCRIPT_NOT_FOUND issues"
version: 1
created: "2026-06-11"
updated: "2026-06-11"
---
## When to Use
When you have a story or epic document with SCRIPT_NOT_FOUND flags or incomplete SP documentation and need to produce comprehensive business logic details with full traceability

## Procedure
1. Read the target story/epic document (e.g., jira_epic_deep_dive.md) and identify all stories that reference stored procedures
2. For each story: Extract list of SPs from SP Scripts column or SP-Side Rules sections - note which are marked SCRIPT_NOT_FOUND vs which have file paths
3. Run resolve-script-not-found-sps skill for all SCRIPT_NOT_FOUND entries: systematically search filesystem, check calling code, create DBA requests for truly missing SPs
4. For all FOUND SPs (either pre-existing paths or newly discovered): Run extract-stored-procedure-logic skill to create detailed SP Logic Summary for each
5. For all INFERRED SPs (logic inferred from code): Document the inferred logic with clear flags and request DBA validation
6. For each SP with extracted logic: Run create-sp-business-logic-traceability skill to map API → SP → DB → Return with line numbers
7. Update story Functional Notes section: Replace generic "SP-Side Rules" with detailed Business Rules citing SP file:line numbers
8. Update story Acceptance Criteria: Add SP line number references to each AC that involves database operations (e.g., AC-002: Territory assigned via spAddNewLead lines 45-52)
9. Update story Traceability section: Replace placeholders with actual file:line references (e.g., SP: dbo.spAddNewLead.StoredProcedure.sql:45-52)
10. Update BDD scenario comments: Add code reference comments in .feature files (e.g., # See spAddNewLead.sql line 45: IF @brn_id IS NULL)
11. Create new section in story doc: ## Stored Procedure Deep Dive with subsections for each SP: Purpose, Full Signature, Business Rules (numbered with line refs), Table Operations (with line refs), Control Flow, Dependencies
12. For stories with multiple SPs: Create SP Interaction Diagram showing call sequence (e.g., spAddNewLead calls spAddNewLeadCustom at line 120, which calls spUpdateBranchStats)
13. Generate SP Verification Checklist per story: List all SPs with status (Analyzed | Inferred | DBA Pending), coverage % (how many lines documented), dependencies resolved Y/N
14. Update story Definition of Done: Add "SP business logic documented with line-level traceability" and "All SCRIPT_NOT_FOUND resolved to Found/Inferred/DBA-Request"
15. Create summary report: Total SPs analyzed, Total lines of SQL documented, SCRIPT_NOT_FOUND resolved count, DBA requests created, Traceability matrix completeness %

## Pitfalls
- Do NOT process stories sequentially if SPs are shared across stories - analyze each unique SP once, then reference it in all stories that use it
- Do NOT re-extract SP logic if it's already been done - check if SP Logic Summary exists before re-running extraction
- Do NOT update story docs without preserving existing content - use surgical edits to add SP details, don't overwrite entire sections
- If a story has 5+ SPs, consider creating a separate SP_ANALYSIS.md document and linking from story rather than embedding everything (keeps story doc readable)
- Do NOT mark SP as "Analyzed" if encoding issues prevented full read - mark as "Partial - encoding issues" and document what was extracted vs what failed

## Verification
1. For each story: Verify all SP references have status (Found/Inferred/DBA-Request) - no more generic SCRIPT_NOT_FOUND flags
2. Confirm Functional Notes section has numbered Business Rules with SP file:line citations
3. Check Traceability section has file:line references for all AC#s that involve database operations
4. Validate BDD scenarios have code reference comments for key Given/When/Then steps
5. Verify SP Verification Checklist shows 100% of SPs resolved (even if resolution is "DBA Pending")
6. Run grep/search to ensure no instances of "SCRIPT_NOT_FOUND" remain without resolution status