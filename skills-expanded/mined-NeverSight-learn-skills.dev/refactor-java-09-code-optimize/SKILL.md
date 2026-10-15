---
name: refactor-java-09-code-optimize
description: Optimizes Java engineering code quality on `@Service` and `@Repository` classes, adapting the ruleset to the detected product line. Use this skill when the user asks to "optimize module code", "fix SQL injection", "enhance logging", "clean up code", "run Step9", or "code review optimization" on a Maven Java service. It is step 9 of 9 of the Java layered-architecture lane in the refactor-chain bundle, and selects the product-line ruleset from the `pom.xml` `<groupId>` (`grp.pt`, `grp.budget`, `gfmis.bgtex` / `com.ctjsoft.gfmis`).
---

# Engineering Code Optimization — refactor-chain · Java lane · step 09/09

**Bundle:** refactor-chain (orchestrated, self-healing refactor chain-of-skills).
**Lane:** Java layered-architecture (Maven) · **Position:** step 09 of 09 · **Prerequisite:** refactor-java-08-common-extract · **Next:** refactor-code-solid (default final pass).
**Adaptivity:** Selects the product-line ruleset from `pom.xml` `<groupId>` (`grp.pt`, `grp.budget`, `gfmis.bgtex` / `com.ctjsoft.gfmis`).

## Purpose
This step performs systematic code-quality optimization on `@Service` and `@Repository` classes. It repairs SQL injection vulnerabilities (parameterizing value concatenation, whitelisting dynamic table names, regex-validating dynamic column names), enhances logging (unified Lombok `@Slf4j`, method-entry and exception logging), and cleans up redundant code (`StringBuffer` → `StringBuilder`, redundant variable elimination, nested-condition simplification, unified empty-collection checks). Because optimization rules differ between product lines, the skill detects the product line from `pom.xml` and loads the matching ruleset first.

## When to use
- The user wants to optimize service/DAO code quality, harden against SQL injection, add logging, or remove redundant code.
- Trigger phrases: "optimize module code", "fix SQL injection", "security fix", "enhance logging", "@Slf4j", "clean up code", "code optimization", "engineering code optimization", "code review optimization".

## Rules enforced
Detect the product line first (Step 0, non-skippable): read the module's `pom.xml`, extract `<groupId>` (falling back to `<parent>`'s `<groupId>`), and map it to a product-line directory. Exact match takes priority over prefix match: `grp.pt` → `products/技术中台/`; `grp.budget` → `products/预算/`; `gfmis.bgtex`, `com.ctjsoft.gfmis`, `grp.gfmis` → `products/执行/`; `grp.gfmis.*` prefix → `products/执行/`; `com.ctjsoft.gfmis.v3` → `products/指标/`; any other groupId falls back to the default `products/技术中台/`.

Selection rules:
- **Process**: Java classes annotated with `@Service` or `@Repository`.
- **Skip**: classes whose total line count exceeds 1000 (recorded in the skip list).
- **Exclude**: interface files, Mapper interfaces, Controllers, configuration classes, DTO/Model.

Optimization priority: (1) SQL injection repair on the DAO layer — `sql-injection-rules.md`; (2) logging enhancement on Service and DAO — `logging-rules.md`; (3) code logic optimization on Service and DAO — `code-optimization-rules.md`.

Immutable red lines: do not modify class names; do not modify method signatures; do not modify existing log statements; do not modify the algorithmic flow of business logic.

## Procedure
1. Run Step 0 product-line detection and load both the common resources (`examples/`, `scripts/`, `templates/`) and the product-line resources (`products/{line}/REFERENCE.md`); product-line rules win on conflict.
2. Read and honor the global encoding-guard rules before any check or repair.
3. Scan and filter: find all `*ServiceImpl.java`, `*DaoImpl.java`, and `*DAO.java` (with `@Repository`) under the target directory, consulting the known oversized-file list.
4. Analyze each file for type and risk points.
5. Execute optimizations in priority order: SQL injection repair, then logging enhancement, then code logic optimization.
6. Self-check, then generate the change report using the report template.

## Guardrails
- Do not change business logic; structural refactoring only.
- After the first file, confirm the optimization style with the user before auto-continuing; emit a progress report every 5–10 files; never touch class names, method signatures, existing logs, or algorithmic flow.

## Verify
Confirm SQL injection points were parameterized or whitelisted, `@Slf4j` logging is present where required, and redundant code was cleaned; confirm class names, method signatures, existing logs, and business algorithms are unchanged; confirm the change report reflects every file processed and skipped.

## References
The exhaustive original governance rules and templates are bundled verbatim under `references/original/` (source of truth).

## Chain position
Runs after refactor-java-08-common-extract. On success the orchestrator advances to refactor-code-solid (default final pass). `refactor-code-solid` runs by default as the final step of the lane.
