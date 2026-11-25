---
name: "resolve-script-not-found-sps"
description: "Systematically locate missing stored procedures flagged as SCRIPT_NOT_FOUND by searching filesystem, inferring from code, or requesting DBA delivery"
version: 1
created: "2026-06-11"
updated: "2026-06-11"
---
## When to Use
When story documentation has SCRIPT_NOT_FOUND flags and you need to either find the actual .sql file, infer the SP logic from calling code, or document the gap for DBA action

## Procedure
1. Read the story/epic document and extract all SCRIPT_NOT_FOUND entries - note the inferred SP name and which API calls it
2. Search filesystem for SP using multiple patterns: find . -iname "*{spName}*" -type f (e.g., *spAddNewLead*, *AddNewLead*, *usp_AddNewLead*)
3. If not found by exact name, search for partial matches: find database folder -name "*.StoredProcedure.sql" | grep -i "addnewlead" or grep -i "addlead"
4. Search for SP references in controller/service code: grep -r "spName" codebase/ to see how it's called (may reveal actual SP name or show it's EF/LINQ query instead)
5. Check if SP is called via ORM (Entity Framework, Dapper): search for .FromSqlRaw, .ExecuteSqlCommand, connection.Execute - if yes, SP may not exist (inline SQL or LINQ)
6. If SP appears to be called but file not found: Use bash/python to list ALL .sql files and their first 5 lines to find SPs with different naming: for f in *.sql; do echo "=== $f ==="' head -5 "$f"; done | grep -A5 "CREATE PROCEDURE"
7. Check for alternative SP locations: Util database folder, migration scripts folder, seed data folder, or separate database project
8. If SP truly missing: Open one of the FOUND SP files to check encoding, then use same method to search again (may need encoding conversion)
9. Analyze calling code to infer SP logic: look at parameters passed, how results are used, what tables/columns are referenced in surrounding code - document as "Inferred Logic from Code"
10. For each SCRIPT_NOT_FOUND SP: Create a resolution entry with Status (Found at {path} | Inferred from code | DBA delivery required) and Next Steps
11. If SP found: Run extract-stored-procedure-logic skill to document it fully
12. If SP inferred from code: Document the inferred logic with CLEAR flag "Logic inferred from {file}:{line}, NOT from actual SP - requires DBA validation"
13. If SP cannot be found or inferred: Create DBA Request document with SP name, calling API, expected parameters (from DTO), expected behavior (from API logic), Priority (Critical/High/Medium based on story priority)
14. Update story document: Replace SCRIPT_NOT_FOUND: spName with either Found: path/to/sp.sql | Inferred: see section X.Y | DBA Request: ticket JIRA-123

## Pitfalls
- Do NOT assume SP doesn't exist just because filename doesn't match - it may be named differently (e.g., proc_AddLead instead of spAddNewLead)
- Do NOT skip searching in *.sql files without .StoredProcedure.sql extension - some DB exports use different naming
- Do NOT forget to check if logic is in application layer (EF LINQ queries) instead of SP - modern codebases may have migrated away from SPs
- Do NOT infer SP logic without documenting the source - always note which code file/line the inference came from
- If encoding issues prevent grep/find from working, use python or iconv to convert files first: iconv -f UTF-16 -t UTF-8 file.sql | grep "CREATE PROCEDURE"

## Verification
1. Confirm every SCRIPT_NOT_FOUND entry has been resolved to one of three states: Found, Inferred, or DBA Request
2. For Found SPs: Verify the .sql file actually contains a CREATE PROCEDURE statement for that SP name
3. For Inferred SPs: Verify the code reference is documented and the inferred logic matches calling code's expectations
4. For DBA Requests: Verify ticket/request includes SP name, calling context, expected signature, and priority
5. Update all story documents to remove generic SCRIPT_NOT_FOUND flags and replace with specific status