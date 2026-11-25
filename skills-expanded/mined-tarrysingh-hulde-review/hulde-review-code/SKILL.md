---
name: hulde-review-code
description: Run a deep, language-profile-driven code review — quality, security, performance, maintainability, and modernization analysis with pluggable language support
argument-hint: [options]
---

# /hulde-review-code

Run a production-grade, language-profile-driven code review engine against the current codebase. Each detected language is matched to a **Language Profile** that defines exactly what deep analysis means for that language — static rules, semantic capabilities, migration targets, and LLM review context.

## Options

- `$ARGUMENTS` may contain:
  - `--security-only` — Only run security-related rules
  - `--legacy` — Enable all legacy language rules (Fortran, COBOL, Ada, RPG, etc.)
  - `--strict` — Treat medium findings as high
  - `--language <id>` — Only analyze files matching this language profile (e.g., `fortran`, `typescript`, `cobol`)
  - `--deep` — Force LLM deep review on ALL files (not just complex ones)
  - `--migration` — Generate migration plan even for modern languages
  - `--profile-status` — Just print profile readiness status and exit
  - A path — Scope to a specific directory or file

---

## Phase 0 — Pre-flight

1. Set `PROJECT_ROOT` to the current working directory.

2. **Load Language Profiles.** Import the language profile system from `@hulde-review/core`:
   ```typescript
   import {
     ALL_PROFILES,
     getProfileForFile,
     getReadyProfiles,
     getProfileStatus,
   } from "@hulde-review/core";
   import { checkAllProfiles, getProfileSummary } from "@hulde-review/core";
   ```

3. **If `--profile-status` is set**, run `checkAllProfiles()` and print the status table, then exit:
   ```
   ╔══════════════════════════════════════════════════════════════╗
   ║  LANGUAGE PROFILE STATUS                                    ║
   ╠══════════════════════════════════════════════════════════════╣
   ║  READY (deep analysis):                                     ║
   ║    ✓ FORTRAN IV/77/90 — 12 rules, 5 capabilities, 4 targets║
   ║    ✓ TypeScript / JavaScript — 15 rules, 4 capabilities     ║
   ║                                                             ║
   ║  STUB (basic analysis only):                                ║
   ║    ○ COBOL — 0 rules, 0 capabilities                       ║
   ║    ○ C / C++ — 0 rules, 0 capabilities                     ║
   ║    ○ Python — 0 rules, 0 capabilities                      ║
   ║    ○ Java — 0 rules, 0 capabilities                        ║
   ║    ○ Ada — 0 rules, 0 capabilities                         ║
   ║    ○ RPG (AS/400) — 0 rules, 0 capabilities                ║
   ╚══════════════════════════════════════════════════════════════╝
   ```
   **Stop here. Do not proceed to analysis.**

4. Check if `$PROJECT_ROOT/.hulde-review/knowledge-graph.json` exists. If it does, read it and store as `$KNOWLEDGE_GRAPH`. If not, inform the user: "No knowledge graph found. Consider running `/hulde-review` first for architecture-level analysis. Proceeding with static and deep review only."

5. Get the current git commit hash:
   ```bash
   git rev-parse HEAD
   ```
   Store as `$COMMIT_HASH`.

6. Create the output directory:
   ```bash
   mkdir -p $PROJECT_ROOT/.hulde-review
   ```

7. Detect languages present in the project by scanning file extensions:
   ```bash
   find $PROJECT_ROOT -type f \( -name '*.ts' -o -name '*.tsx' -o -name '*.js' -o -name '*.jsx' -o -name '*.f' -o -name '*.f90' -o -name '*.for' -o -name '*.f77' -o -name '*.py' -o -name '*.go' -o -name '*.rs' -o -name '*.java' -o -name '*.c' -o -name '*.cpp' -o -name '*.cob' -o -name '*.cbl' -o -name '*.adb' -o -name '*.ads' -o -name '*.rpgle' -o -name '*.rpg' \) -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/dist/*' -not -path '*/build/*' | head -500
   ```
   Store the file list as `$SOURCE_FILES`.

8. **Match files to language profiles.** For each file in `$SOURCE_FILES`, call `getProfileForFile(filePath)`. Group files by profile. Track:
   - `$PROFILED_FILES` — Files with a matching profile
   - `$UNPROFILED_FILES` — Files with no matching profile (skip these)

9. **Check profile readiness** for each detected language:
   ```typescript
   const summary = getProfileSummary();
   ```
   Report to user:
   ```
   Language analysis capabilities:
     Deep analysis: Fortran, TypeScript (full rule sets + semantic analysis)
     Basic analysis: C (profile exists but rules not yet implemented)
     Not supported: <any files with no profile>
   ```
   **Warn** if any detected language uses a stub profile — these files will get universal rules only (large-file, long-function, etc.) but no language-specific deep analysis.

10. Parse `$ARGUMENTS` for options:
    - `--security-only` → `$SECURITY_ONLY = true`
    - `--legacy` → `$LEGACY = true`
    - `--strict` → `$STRICT = true`
    - `--language <id>` → `$LANGUAGE_FILTER = <id>` — filter `$SOURCE_FILES` to only this profile's files
    - `--deep` → `$FORCE_DEEP = true`
    - `--migration` → `$FORCE_MIGRATION = true`
    - Any path argument → `$SCOPE_PATH`

11. If `$SCOPE_PATH` is set, filter `$SOURCE_FILES` to only include files under that path.
12. If `$LANGUAGE_FILTER` is set, filter `$SOURCE_FILES` to only files matching that profile.

---

## Phase 1 — Static Analysis (per language profile)

For each file in `$SOURCE_FILES`:

1. Read the file content.
2. Get the file's language profile via `getProfileForFile(filePath)`.
3. Determine the language from the file extension:
   - `.ts` → typescript, `.tsx` → tsx, `.js` → javascript, `.jsx` → jsx
   - `.f`, `.for`, `.f77`, `.fpp` → fortran (fixed-format)
   - `.f90`, `.f95`, `.f03`, `.f08` → fortran (free-format)
   - `.py` → python, `.go` → go, `.rs` → rust, `.java` → java
   - `.c`, `.h` → c, `.cpp`, `.hpp`, `.cc` → cpp
   - `.cob`, `.cbl` → cobol, `.adb`, `.ads` → ada, `.rpgle`, `.rpg` → rpg

4. Build an `AnalysisContext` for each file:
   - For Fortran files, use the `FortranPlugin` to generate `StructuralAnalysis` and `CallGraphEntry[]`
   - For JS/TS files, use the `TreeSitterPlugin` or the basic structural analysis fallback
   - For other languages, use basic line-counting structural analysis

5. **Apply language-profile-aware rules:**
   - If the profile is **ready** (`getReadyProfiles()` includes it): apply ALL rules listed in `profile.staticRules`
   - If the profile is a **stub**: apply only universal rules (`large-file`, `long-function`, `too-many-params`, `deeply-nested`)
   - If the file has **no profile**: skip or apply universal rules only

6. **Run semantic capabilities based on profile:**
   - If `profile.semanticCapabilities.controlFlowAnalysis === true`: run GOTO/control flow tracing (e.g., `goto-chain-analysis` rule)
   - If `profile.semanticCapabilities.numericalAnalysis === true`: run numerical stability checks (e.g., `numerical-stability` rule)
   - If `profile.semanticCapabilities.memoryAnalysis === true`: run memory safety checks (future: buffer overflow, use-after-free)
   - If `profile.semanticCapabilities.concurrencyAnalysis === true`: run async/concurrency checks (e.g., `promise-leak` rule)
   - If `profile.semanticCapabilities.typeSystemAnalysis === true`: run type system checks (e.g., `type-assertion-abuse` rule)

7. Collect all `ReviewFinding` objects.

**If `$SECURITY_ONLY` is set**, filter findings to only `category === "security"`.
**If `$STRICT` is set**, upgrade all `severity === "medium"` findings to `"high"`.

**Gate check:** If >500 files, inform the user and suggest scoping with `--language` or a path argument. Proceed only if user confirms.

Store all findings as `$STATIC_FINDINGS`.

---

## Phase 2 — LLM-Powered Deep Review (enhanced with profile context)

Identify files that need deep review:
- **If `$FORCE_DEEP` is set:** ALL files get deep review (up to 20 files)
- Otherwise:
  - Files with >3 static findings from Phase 1
  - Files with `complexity === "complex"` in the knowledge graph (if available)
  - Files with any `critical` or `high` severity findings from static analysis

For up to 10 such files (20 if `--deep`), prioritized by finding count and severity, dispatch subagents for deep review. Run up to **3 subagents concurrently**.

For each file:

1. Get the file's language profile.
2. Build the LLM prompt by **injecting the profile's `deepReviewContext`**:

   > **File to review:** `<filePath>`
   >
   > **Language:** `<language>` (`<profile.name>`)
   >
   > **Language-specific context:**
   > ```
   > <profile.deepReviewContext>
   > ```
   >
   > **Static findings already detected:**
   > ```json
   > [list of static findings for this file]
   > ```
   >
   > **File content:**
   > ```
   > <file content>
   > ```
   >
   > **Instructions:** Follow the deep review prompt template. Focus on issues that the static analyzer cannot catch — semantic bugs, architectural smells, and language-specific pitfalls described in the language context above. Return findings as a JSON array of ReviewFinding objects.
   > Write output to: `$PROJECT_ROOT/.hulde-review/intermediate/deep-review-<fileIndex>.json`

3. For **legacy** language files (`profile.category === "legacy"`), also inject migration context:

   > **Migration targets for this language:**
   > ```json
   > <profile.migrationTargets>
   > ```
   >
   > **Additional instruction:** Identify specific migration blockers in this file and suggest which migration target is most suitable.

After all subagents complete, read each `deep-review-<N>.json` file and merge with `$STATIC_FINDINGS`. Deduplicate by checking if a deep review finding overlaps with an existing static finding (same file, similar line range, same category).

Store merged findings as `$ALL_FINDINGS`.

---

## Phase 3 — Migration Analysis (for legacy profiles only)

**Skip this phase if no legacy language files were detected AND `$FORCE_MIGRATION` is not set.**

If legacy language files are present OR `--migration` is set:

1. For each legacy language profile detected:
   - Use the `MigrationAnalyzer` from `@hulde-review/core` to analyze subroutines/modules
   - Use `profile.migrationTargets` to rank migration targets
   - Score each subroutine's migration readiness (1-5 scale)

2. Generate a phased migration plan:
   - Phase 1: Quick wins (readiness 1-2)
   - Phase 2: Core modernization (readiness 3)
   - Phase 3: Deep refactoring (readiness 4-5)
   - Phase 4: Validation and regression testing

3. Write the migration plan to `$PROJECT_ROOT/.hulde-review/migration-plan.json`.

4. Add migration-related findings to `$ALL_FINDINGS` (e.g., "This subroutine has 5 COMMON blocks — migration readiness score 4/5").

---

## Phase 4 — Architecture Review (if knowledge graph exists)

**Skip this phase if `$KNOWLEDGE_GRAPH` is not available.**

If the knowledge graph exists, analyze it for architecture-level issues:

1. **Circular dependencies:** Walk the edges of type `imports` and `depends_on`. If A→B→A exists, create a finding.
2. **Layer violations:** If layers are defined, check if any edges cross layers in unexpected ways.
3. **Orphaned modules:** Find nodes with zero incoming AND zero outgoing edges.
4. **God modules:** Find nodes with >15 connected edges (high fan-in + fan-out).

Generate architecture findings and merge with `$ALL_FINDINGS`.

---

## Phase 5 — Report Generation

1. Aggregate all findings from Phases 1-4.
2. Use the `ReportGenerator` from `@hulde-review/core/review/report-generator.js` to produce a `CodeReviewReport`:
   - Calculate composite risk score (0-100)
   - Estimate technical debt in hours
   - Group by severity and category
   - Generate executive summary text
   - Produce prioritized recommendations
   - Calculate per-language breakdown (using profile data)
3. **Include language profile readiness in the report:**
   - Which languages got deep analysis vs basic
   - Per-language breakdown uses profile names and industry context
4. Write the full report to `$PROJECT_ROOT/.hulde-review/review-report.json`.
5. Generate a human-readable Markdown report at `$PROJECT_ROOT/.hulde-review/review-report.md` with:
   - Header with project name, date, commit hash
   - **Language support summary** (deep vs basic vs unsupported)
   - Risk score with visual indicator
   - Executive summary
   - Findings table grouped by severity
   - Language breakdown (per-profile)
   - Migration plan summary (if Phase 3 ran)
   - Recommendations list
6. Clean up intermediate files:
   ```bash
   rm -rf $PROJECT_ROOT/.hulde-review/intermediate
   ```
7. Print a summary to the user:

   ```
   ╔══════════════════════════════════════════════════════════════╗
   ║  HULDE CODE REVIEW COMPLETE                                 ║
   ╠══════════════════════════════════════════════════════════════╣
   ║  Project: <projectName>                                     ║
   ║  Files analyzed: <totalFiles>                               ║
   ║  Risk Score: <riskScore>/100 [<riskLabel>]                  ║
   ║  Total Findings: <totalFindings>                            ║
   ║    Critical: <n>  High: <n>  Medium: <n>  Low: <n>          ║
   ║  Technical Debt: <hours> hours                              ║
   ╠══════════════════════════════════════════════════════════════╣
   ║  LANGUAGE ANALYSIS:                                         ║
   ║    Deep:  Fortran (12 rules), TypeScript (15 rules)         ║
   ║    Basic: C (universal rules only)                          ║
   ╠══════════════════════════════════════════════════════════════╣
   ║  TOP FINDINGS:                                              ║
   ║  1. <finding title> (<severity>) — <filePath>               ║
   ║  2. <finding title> (<severity>) — <filePath>               ║
   ║  3. <finding title> (<severity>) — <filePath>               ║
   ║  4. <finding title> (<severity>) — <filePath>               ║
   ║  5. <finding title> (<severity>) — <filePath>               ║
   ╠══════════════════════════════════════════════════════════════╣
   ║  EXECUTIVE SUMMARY:                                         ║
   ║  <executive summary>                                        ║
   ╠══════════════════════════════════════════════════════════════╣
   ║  Reports saved to:                                          ║
   ║    .hulde-review/review-report.json                         ║
   ║    .hulde-review/review-report.md                           ║
   ║                                                             ║
   ║  Run `/hulde-dashboard` to visualize findings in the graph  ║
   ╚══════════════════════════════════════════════════════════════╝
   ```

---

## Error Handling

- If a subagent dispatch fails during deep review, skip that file and continue. Log the failure.
- If structural analysis throws for a file, skip it and continue. Log the failure.
- If a language profile is a stub, warn and continue with universal rules only — never fail.
- ALWAYS save partial results — a partial report is better than no report.
- Report any skipped files or errors in the final summary.
- NEVER silently drop errors. Every failure must be visible in the final report.
