---
name: "extract-stored-procedure-logic"
description: "Extract complete business logic from SQL Server stored procedures including parameters, tables, functions, control flow, and traceability"
version: 1
created: "2026-06-11"
updated: "2026-06-11"
---
## When to Use
When analyzing legacy stored procedures for migration, documentation, or story creation where you need to understand exact business rules and data operations

## Procedure
1. Locate the stored procedure .sql file in the database script folder (typically *.StoredProcedure.sql or *.sql)
2. Read the entire SP file contents using read tool - handle encoding issues (UTF-16, UTF-8 with BOM, wide characters)
3. Extract SP metadata: name (CREATE PROCEDURE [dbo].[spName]), parameters with types and defaults, return type
4. Parse and document parameter list: @paramName datatype(length) = defaultValue, noting which are INPUT, OUTPUT, or both
5. Identify all table references: INSERT INTO, UPDATE, DELETE FROM, SELECT FROM, MERGE - capture table names and operations
6. Extract function calls: dbo.FunctionName(...) or schema.FunctionName(...) - note what functions are called and with what parameters
7. Document control flow: IF/ELSE branches, CASE statements, WHILE loops, TRY/CATCH blocks - capture conditions and logic paths
8. Trace variable assignments: DECLARE @var, SET @var = value, SELECT @var = column - understand data transformations
9. Identify stored procedure calls: EXEC spOtherProc @param1, @param2 - note dependencies on other SPs
10. Extract business rules: validation checks (IF EXISTS, IF @value > X, etc.), calculations, defaults, data manipulations
11. Document transaction handling: BEGIN TRANSACTION, COMMIT, ROLLBACK - understand atomicity requirements
12. Capture error handling: RAISERROR, THROW, error codes, error messages - note failure scenarios
13. Map data flow: Input params → temp tables/variables → table operations → output params/result sets
14. Create traceability matrix: For each API parameter, trace to SP parameter → table column → output field
15. If file has encoding issues (wide chars, BOM), use bash with iconv or python to convert: python -c "import sys; print(sys.stdin.buffer.read().decode('utf-16-le', errors='ignore'))" < file.sql
16. Generate SP Logic Summary document with sections: Purpose, Parameters, Tables Accessed, Functions Called, Business Rules (numbered), Control Flow (pseudocode), Dependencies, Error Handling, Traceability (input→table→output)

## Pitfalls
- Do NOT skip dynamic SQL blocks (EXEC(@sql) or sp_executesql) - these contain critical logic that may reference tables/columns not visible in static analysis
- Do NOT ignore commented-out code - it may represent disabled features that need to be preserved or documented as technical debt
- Do NOT assume parameter names match table columns - always trace the actual variable assignments (SELECT @customerId = cst_id FROM ...)
- Do NOT miss implicit type conversions (varchar to int, datetime formats) - these can cause subtle bugs in reimplementation
- Do NOT overlook transaction isolation levels (SET TRANSACTION ISOLATION LEVEL) - these affect concurrency behavior
- Do NOT forget to document GOTO labels and cursor operations (legacy patterns) - modern code may need different approach
- If SP file is missing (SCRIPT_NOT_FOUND), search for similar names: sp*, usp_*, proc_*, or check sys.procedures in database dump if available

## Verification
1. Confirm all parameters from SP signature are documented with types, defaults, and usage
2. Verify every table mentioned in SP is listed with operation type (INSERT/UPDATE/DELETE/SELECT)
3. Check that all function calls are documented with SP name that calls them
4. Validate business rules are numbered and each has a condition + action
5. Ensure traceability matrix maps API params → SP params → table columns → return values
6. Cross-reference extracted logic against API controller code that calls the SP to ensure parameter alignment