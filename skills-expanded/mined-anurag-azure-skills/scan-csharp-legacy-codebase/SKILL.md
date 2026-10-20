---
name: "scan-csharp-legacy-codebase"
description: "Scan, pull, and deeply understand the LeadPerfection C#/.NET Framework legacy codebase — controllers, middleware, DTOs, stored procedures, EF context — and produce structured analysis artifacts for modernization use."
version: 1
created: "2026-06-21"
updated: "2026-06-26"
---
## When to Use
Use this skill whenever you need to:
- Understand what a legacy C# controller action does before writing an epic template or target design
- Extract business logic from a stored procedure or Sales.cs/middleware method
- Map legacy DTOs (SalesDTO, ApptDetailDTO, etc.) to target Java Records
- Find which tables a stored procedure reads/writes
- Identify all methods in a controller that belong to a specific epic/domain
- Validate that a target design accurately reflects the legacy implementation
- Answer questions about legacy authentication, RBAC (ValidateUser.cs, BaseClass.cs), or data access patterns
- Scan the LeadPerfectionContext.Context.cs (36K lines) to discover stored procedure bindings

Codebase root: C:/Users/madahuja/Desktop/Epic-Workflow/LeadPerfection/LeadPerfection

Key file locations (all relative to codebase root):
- Controllers:       LeadPerfection/Controllers/*.cs  (SalesApiController, CustomersController, InstallerController, LeadsController, etc.)
- Middleware:        LP.middleware/*.cs  (Sales.cs 1328L, Leads.cs, Installer.cs, etc.)
- DTOs:             LP.middleware/dataTransferObjects/*.cs  (SalesDTO.cs, ApptDetailDTO.cs, SalesApptDetailDTO.cs, etc.)
- Data Models:      LP.middleware/Data/*.cs  (entity classes, spXxx_Result.cs SP result wrappers)
- EF Context:       LP.middleware/Data/LeadPerfectionContext.Context.cs  (36,535 lines — all SP bindings)
- Helper/Auth:      LP.middleware/Helper/ValidateUser.cs, BaseClass.cs, RedisConnection.cs
- SQL Scripts:      C:/Users/madahuja/Desktop/Epic-Workflow/i417_database_script_05082026/i417_database_script_05082026/*.sql  (3,473 files)
- SQL SPs pattern:  dbo.spXxx.StoredProcedure.sql or dbo.spXxx.UserDefinedFunction.sql

## Procedure
1. STEP 1 — IDENTIFY SCOPE: Determine which domain/epic you are analyzing. Map it to its controllers and middleware files using the domain classification: SalesService → SalesApiController.cs + Sales.cs; LeadService → LeadsController.cs + Leads.cs; AccessControl → ValidateUser.cs + BaseClass.cs + TokenController.cs; etc.
2. STEP 2 — SCAN CONTROLLER: read the relevant controller file (e.g., LeadPerfection/Controllers/SalesApiController.cs). For each public action method extract: (a) HTTP verb from attribute or convention, (b) route/action name, (c) request parameters (body, query, headers), (d) which middleware method it calls (e.g., new Sales().GetSalesApptDetail(...)), (e) what it returns.
3. STEP 3 — SCAN MIDDLEWARE: read the corresponding LP.middleware/*.cs file (e.g., LP.middleware/Sales.cs). For each method called from the controller extract: (a) full method signature, (b) which stored procedure it calls via EF context (look for context.spXxx(...) or context.Database.SqlQuery patterns), (c) parameters passed to SP, (d) any business logic BEFORE/AFTER the SP call (validation, transformation, config lookups), (e) return type and mapping.
4. STEP 4 — SCAN EF CONTEXT for SP binding: grep LP.middleware/Data/LeadPerfectionContext.Context.cs for the SP name to find its exact C# binding signature, parameter types, and return type. Command: grep -n 'spWSGSalesApptDetail\|spWSUSalesApptDetail' 'C:/Users/madahuja/Desktop/Epic-Workflow/LeadPerfection/LeadPerfection/LP.middleware/Data/LeadPerfectionContext.Context.cs' | head -40
5. STEP 5 — SCAN SQL STORED PROCEDURE: Find and read the actual T-SQL file. Pattern: find 'C:/Users/madahuja/Desktop/Epic-Workflow/i417_database_script_05082026' -name '*spWSGSalesApptDetail*'. Read the full SQL to extract: (a) all input parameters (@Param type), (b) temp tables or CTEs, (c) every SELECT/INSERT/UPDATE/DELETE with table names, (d) IF/ELSE business rules, (e) config lookups (con_config, tblAccessItems), (f) cursor/loop patterns, (g) error handling (RAISERROR, TRY/CATCH).
6. STEP 6 — SCAN DTOs: read the relevant DTO files (e.g., LP.middleware/dataTransferObjects/SalesDTO.cs, SalesApptDetailDTO.cs). For each DTO class extract all properties with their C# types. Map each property to its corresponding target Java Record field.
7. STEP 7 — SCAN DATA MODEL ENTITIES: For each table referenced in the SP, find its C# entity class in LP.middleware/Data/. Read column names, types, and relationships. This reveals the legacy schema structure for migration mapping.
8. STEP 8 — SCAN AUTH / RBAC PATTERN: If the method has access control, read LP.middleware/Helper/ValidateUser.cs. Key methods: userHasAccess(ActionName, empId) → calls FNHasAPIAccess SP; appkeyHasAccess(ActionName) → calls spGetAPIAppKeyPermissions. Read LP.middleware/Helper/BaseClass.cs for checkValidation() pattern.
9. STEP 9 — PRODUCE STRUCTURED ANALYSIS: Write findings to src/output_workflow/LegacyAnalysis/{EpicId}/{ControllerName}_analysis.md with sections: (1) Controller Action Inventory table, (2) Per-method: middleware call chain, SP name, parameters, (3) SP business logic (T-SQL excerpts), (4) DTO → Java Record mapping table, (5) Table access map (which tables are read/written per SP), (6) Auth/RBAC pattern, (7) Modernization notes (risks, hidden logic, config-driven rules).
10. STEP 10 — EMIT BR PSEUDO-CODE: For every stored procedure found, produce a BR-{nn} entry with: Legacy T-SQL excerpt (key IF/ELSE, config lookups, RBAC checks) + Target Java pseudo-code with '// Legacy SP line N: ...' traceability comments. Follow the exact format used in ApplicationDesign.md BR sections.

## Pitfalls
- LeadPerfectionContext.Context.cs is 36,535 lines — NEVER read it in full. Always grep for the specific SP name first, then read only the surrounding 20-30 lines.
- SQL files are named dbo.spXxx.StoredProcedure.sql — use find with a wildcard: find ... -name '*spWSGSalesApptDetail*' to locate them. Some SPs may have multiple files (e.g., v1, v2, v3 variants).
- Sales.cs is 1,328 lines — read it in chunks using offset/limit. Do NOT read the entire file at once.
- The SalesApiController uses new Sales().MethodName() — the middleware class is instantiated inline, not injected. The actual business logic is always in the LP.middleware/*.cs file, not the controller.
- Legacy auth uses thread-local or static patterns in BaseClass.cs and ValidateUser.cs — do NOT assume standard DI. Map these to the target FeignClient calls to EP-01 AccessControlService.
- Many SPs use con_config table lookups (SELECT datavalue FROM con_config WHERE datakey='XYZ') — these become tenantConfigService.get*Config() calls in the target Java service.
- tblAccessItems RBAC checks (HasAccess flag, ActionName string) → map to accessControlClient.hasPermission(userId, resource, action) in Java.
- Some DTOs are in LP.middleware/dataTransferObjects/ AND also have duplicates in LeadPerfection/Models/ — always prefer the middleware DTO as the authoritative source.
- SQL SP files may not exist for all SPs if they are dynamically built or are part of a larger script. In that case, extract logic from the EF Context binding and middleware method comments.
- Do not scan the entire i417_database_script_05082026 folder — it has 3,473 files. Always search by SP name pattern first.
- spWSUSalesApptDetail3 is the v3 update SP — the controller has v1 (UpdateSalesApptDetail), v2 (UpdateSalesApptDetail2), v3 (UpdateSalesApptDetail3) all calling the same or similar SPs. Always check all three variants.
- The LP.middleware/Data/spXxx_Result.cs files are the EF result-set wrapper classes — they reveal the exact columns returned by each SP, which directly maps to the target DTO/Java Record fields.

## Verification
1. grep -c 'public.*HttpPost\|public.*HttpGet\|public.*Route' 'C:/Users/madahuja/Desktop/Epic-Workflow/LeadPerfection/LeadPerfection/LeadPerfection/Controllers/SalesApiController.cs' — should return ~20+ methods
2. grep -n 'spWSGSalesApptDetail' 'C:/Users/madahuja/Desktop/Epic-Workflow/LeadPerfection/LeadPerfection/LP.middleware/Data/LeadPerfectionContext.Context.cs' | head -5 — should return the EF method binding
3. find 'C:/Users/madahuja/Desktop/Epic-Workflow/i417_database_script_05082026' -name '*SalesAppt*' | head -10 — should return matching SQL files
4. The output analysis file exists at src/output_workflow/LegacyAnalysis/{EpicId}/{File}_analysis.md
5. Every SP referenced in the epic template has a corresponding BR-{nn} entry with T-SQL excerpt AND Java pseudo-code in the analysis output
6. The DTO mapping table covers every property in the legacy DTO and maps it to a Java Record field with type conversion notes