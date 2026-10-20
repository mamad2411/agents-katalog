---
name: "create-sp-business-logic-traceability"
description: "Create detailed business logic traceability documentation mapping API parameters → SP logic → database operations → return values with line-by-line code references"
version: 1
created: "2026-06-11"
updated: "2026-06-11"
---
## When to Use
After extracting SP logic, when you need to document how data flows from API call through stored procedure to database and back, with complete traceability for story acceptance criteria and BDD scenarios

## Procedure
1. Gather inputs: API controller file + method, DTO classes, SP .sql file, database table schemas (from .Table.sql files if available)
2. Extract API signature: HTTP method, route, controller method name, all DTO parameters with types
3. Extract SP signature: SP name, all @parameters with types and defaults, OUTPUT parameters, return value
4. Create parameter mapping table: API DTO field → SP parameter (note any transformations, type conversions, or middleware processing)
5. Parse SP line-by-line and document major operations with line numbers: Line 10-15: Validate @employeeId exists in emp_employees, Line 20-25: Resolve branch from zip code via brz_BranchZips, etc.
6. For each business rule in SP: Document as BR-### (Business Rule ID), cite line number range, describe condition + action, map to AC# in story if applicable
7. For each table operation: Document table name, operation (INSERT/UPDATE/DELETE/SELECT), affected columns, WHERE clause conditions, line number
8. Trace data flow for key scenarios: Success path (all validations pass), Failure path (validation fails), Edge case (null handling, default values)
9. Create reverse mapping: For each story Acceptance Criterion, trace to specific SP line numbers and table operations that implement it
10. Document function dependencies: For each function called in SP (e.g., dbo.fnDeptAccess), note what it does (if code available) or flag as dependency requiring separate analysis
11. Create BDD scenario traceability: For each Given/When/Then step, cite exact SP lines and table operations that correspond
12. Generate comprehensive Traceability Matrix with columns: AC# | API Param | SP Param | SP Logic (lines) | Table.Column | Business Rule | Return Field | BDD Scenario
13. Document any gaps: Missing SP logic (SCRIPT_NOT_FOUND), Inferred behavior, Hardcoded values, Commented code that may be relevant
14. Create SP Flow Diagram (pseudocode or flowchart): Show decision points, loops, error handling, table operations in sequence

## Pitfalls
- Do NOT document only happy-path logic - trace error handling paths, validation failures, and edge cases
- Do NOT skip OUTPUT parameters or RETURN values - these are part of the API contract
- Do NOT assume parameter names match - always trace actual assignments (SELECT @branchId = brn_id FROM ...)
- Do NOT ignore IF EXISTS checks - these are critical validations that map to acceptance criteria
- Do NOT forget ELSE branches - they may contain important default behavior or error handling
- If SP calls another SP (EXEC spOtherProc), note the dependency but don't recursively expand unless that SP is also in scope for current story

## Verification
1. Verify every API DTO parameter is traced to either an SP parameter, a hardcoded value, or marked as unused
2. Confirm every SP parameter is traced to a table operation or variable assignment
3. Check that every Acceptance Criterion (AC-###) has at least one SP line number reference
4. Validate that BDD scenario steps map to specific SP logic (Given → line X, When → line Y, Then → line Z)
5. Ensure Traceability Matrix has no empty cells (use "N/A" or "Not used" if parameter doesn't flow to database)