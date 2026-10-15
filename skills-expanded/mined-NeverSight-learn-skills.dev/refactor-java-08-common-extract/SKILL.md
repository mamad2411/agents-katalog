---
name: refactor-java-08-common-extract
description: Extracts shared code packages from capability-layer modules into a `grp-{module}-common` module, adapting the ruleset to the detected product line. Use this skill when the user asks to "extract common module", "run Step8", "check common packages", "extract common", or "consolidate util/cache/constant/enums/exception/config" in a Maven Java service. It is step 8 of 9 of the Java layered-architecture lane in the refactor-chain bundle, and selects the product-line ruleset from the `pom.xml` `<groupId>` (`grp.pt`, `grp.budget`, `gfmis.bgtex` / `com.ctjsoft.gfmis`).
---

# Common Module Extraction — refactor-chain · Java lane · step 08/09

**Bundle:** refactor-chain (orchestrated, self-healing refactor chain-of-skills).
**Lane:** Java layered-architecture (Maven) · **Position:** step 08 of 09 · **Prerequisite:** refactor-java-07-api-naming · **Next:** refactor-java-09-code-optimize.
**Adaptivity:** Selects the product-line ruleset from `pom.xml` `<groupId>` (`grp.pt`, `grp.budget`, `gfmis.bgtex` / `com.ctjsoft.gfmis`).

## Purpose
This step consolidates shared code by extracting the public packages out of capability-layer modules into a `grp-{module}-common` module, so common code is managed in one place. Because directory structures differ between product lines, the skill detects the product line from `pom.xml` and loads the matching ruleset before acting. The public packages extracted into `grp-{module}-common` are: `util`, `cache`, `constant`, `enums`, `exception`, `config`. No business logic is changed during extraction.

## When to use
- The user wants to check whether shared code still lives inside business modules, or to migrate it into the common module.
- Trigger phrases: "extract common module", "Step8 check", "Step8 fix", "check common packages", "extract common", "consolidate shared code".

## Rules enforced
Detect the product line first (Step 0, non-skippable): read the root `pom.xml`, extract `<groupId>` (falling back to `<parent>`'s `<groupId>`), and map it to a product-line directory. Exact match takes priority over prefix match: `grp.pt` → `products/技术中台/`; `grp.budget` → `products/预算/`; `gfmis.bgtex`, `com.ctjsoft.gfmis`, `grp.gfmis` → `products/执行/`; `grp.gfmis.*` prefix → `products/执行/`; `com.ctjsoft.gfmis.v3` → `products/指标/`; any other groupId falls back to the default `products/技术中台/`.

The public packages extracted into `grp-{module}-common` are: `util`, `cache`, `constant`, `enums`, `exception`, `config`.

| ID | Check item | Description | Method |
|------|--------|------|---------|
| S8-01 | `util/` package ownership | Whether utility classes still sit inside the business module | Grep dependency analysis |
| S8-02 | `cache/` package ownership | Whether cache classes still sit inside the business module | Grep dependency analysis |
| S8-03 | `constant/` package ownership | Constant classes | Grep dependency analysis |
| S8-04 | `enums/` package ownership | Enum classes | Grep dependency analysis |
| S8-05 | `exception/` package ownership | Exception classes | Grep to distinguish exception definitions from handlers |
| S8-06 | `config/` package ownership | Configuration classes | Grep for `@MapperScan` / `@ComponentScan` |

Each file is classified as **EXTRACT** (recommended for extraction, added to the migration list automatically), **EVALUATE** (needs human judgment, awaits user confirmation), or **RETAIN** (keep in place, excluded automatically).

## Procedure
1. Run Step 0 product-line detection and load both the common resources (`examples/`, `scripts/`, `templates/`) and the product-line resources (`products/{line}/REFERENCE.md`); product-line rules win on conflict.
2. Read and honor the global encoding-guard rules before any check or migration.
3. Read-only check — scan the source modules, check the target module, run dependency analysis via the classification decision tree, and generate the check report.
4. Confirm the migration list: EXTRACT items are included automatically, EVALUATE items await user confirmation, RETAIN items are excluded.
5. Prepare the `grp-{module}-common` module, then migrate file by file in order (`constant` → `enums` → `exception` → `util` → `cache` → `config`) using the standard 7-step per-file flow.
6. Adjust `pom.xml` dependencies, then run final verification.

## Guardrails
- Do not change business logic; structural refactoring only.
- Keep `package` declarations aligned with directory paths, migrate one file at a time and verify immediately after each, and never move `@MapperScan` configuration classes.

## Verify
Confirm every EXTRACT file was moved into `grp-{module}-common` and each `package` declaration matches its directory path; confirm `@MapperScan` classes were not moved; confirm `pom.xml` dependencies were updated and the project still compiles with no business logic changed.

## References
The exhaustive original governance rules and templates are bundled verbatim under `references/original/` (source of truth).

## Chain position
Runs after refactor-java-07-api-naming. On success the orchestrator advances to refactor-java-09-code-optimize. `refactor-code-solid` runs by default as the final step of the lane.
