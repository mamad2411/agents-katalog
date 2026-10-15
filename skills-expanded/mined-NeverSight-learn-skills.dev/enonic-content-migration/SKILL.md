---
name: enonic-content-migration
description: Generates Enonic XP scripts for bulk content operations — creating, updating, querying, migrating, and transforming content using lib-content and lib-node APIs. Covers the query DSL (NoQL), aggregations, batch processing, task controllers for long-running operations, and export/import workflows. Use when writing bulk content creation, update, or deletion scripts, querying with NoQL syntax, migrating content between environments, running long-running task operations, or working with aggregations and paginated retrieval. Do not use for Guillotine GraphQL frontend queries, content type schema definitions, single contentLib.get() calls, or non-Enonic data migration tools.
license: MIT
metadata:
  author: webmaxru
  version: "1.1"
---

# Enonic Content Migration

## Procedures

**Step 1: Identify the Enonic XP project and operation scope**
1. Inspect the workspace for Enonic XP project markers: `build.gradle` with `com.enonic.xp` dependencies, `src/main/resources/` directory structure, or `gradle.properties` with `xpVersion`.
2. Execute `node scripts/find-enonic-targets.mjs .` to scan for Enonic XP project markers and existing content operation files when a Node runtime is available.
3. If no Enonic XP project is detected, stop and explain that this skill targets Enonic XP content operations only.
4. Determine the target XP version from `gradle.properties` or `build.gradle` to select the correct API surface.
5. Classify the requested operation:
   - **Bulk create**: Importing content from external sources (JSON, CSV, APIs).
   - **Bulk update**: Modifying existing content matching query criteria.
   - **Bulk delete**: Removing content matching query criteria.
   - **Migration**: Moving or transforming content between paths, sites, or environments.
   - **Query/Aggregation**: Retrieving and analyzing content with NoQL and aggregations.
   - **Long-running task**: Any operation processing more than ~100 items that needs progress reporting.

**Step 2: Select the API layer and context**
1. Read `references/migration-reference.md` for query DSL patterns, batch processing strategies, and branch handling rules.
2. Choose `lib-content` when the operation works with CMS content and needs publish/unpublish, content-type validation, and the content domain abstraction.
3. Choose `lib-node` when the operation needs low-level node manipulation, custom repositories, or bypasses content-type validation for raw data migration.
4. Determine the required context:
   - Use `lib-context` to run operations in `draft` branch for modifications and `master` branch for reading published content.
   - Use `lib-context` with `role:system.admin` principal when the operation requires elevated permissions.
5. If the operation processes more than ~100 items, wrap it in a task controller using `lib-task`. Read `references/migration-reference.md` section on task controllers for the pattern.

**Step 3: Build the query**
1. Construct the NoQL query string or DSL expression to match the target content.
2. For content-type filtering, use the `contentTypes` parameter on `contentLib.query()` or a `type` property comparison in node queries.
3. For date-range queries, use `instant()` or `dateTime()` functions and the `range()` query function.
4. For full-text search, use `fulltext()` with the appropriate field paths and operator (`AND`/`OR`).
5. For path-scoped operations, use `_path LIKE '/content/site-path/*'` to match descendants. Note: the `_path` property in NoQL queries includes the internal `/content/` prefix, but `hit._path` in results returns the content-domain path without it. Always prepend `/content/` when building queries from result paths.
6. Add `filters` for efficient post-query narrowing using `exists`, `notExists`, `hasValue`, or `boolean` combinations.
7. Add `aggregations` when the operation needs grouped statistics (term counts, date histograms, numeric ranges, stats).
8. Read `references/examples.md` for complete query and aggregation patterns.

**Step 4: Implement batch processing**
1. Use paginated retrieval with `start` and `count` parameters to avoid loading all results into memory.
2. Set `count` to a batch size between 50 and 200 depending on the complexity of per-item processing.
3. Loop until `result.hits.length === 0` or `start >= result.total`, incrementing `start` by the batch size each iteration.
4. For `contentLib.create()` in bulk, set `refresh: false` to avoid per-item index refresh; call a manual refresh after the batch completes.
5. For `contentLib.modify()`, use the editor callback pattern to safely transform each content item.
6. For `contentLib.publish()`, batch keys into groups of 50–100 to avoid timeout on large publish sets.
7. Track success and failure counts for reporting.
8. Read `assets/bulk-update.template.ts` for the reusable batch update controller template. Note: templates use TypeScript/ESM syntax (`import`, `const`, arrow functions); adapt to CommonJS JavaScript (`require()`, `var`, `function()`) for XP runtime deployment as `.js` files.

**Step 5: Handle branch operations and publishing**
1. Run content modifications in the `draft` branch context.
2. After modifications complete, publish changed items to `master` using `contentLib.publish()` with `sourceBranch: 'draft'` and `targetBranch: 'master'`.
3. Set `includeDependencies: false` when publishing bulk-updated items to avoid unintended dependency publishing.
4. For operations comparing draft and master state, use `repo.diff()` from `lib-node` with `target: 'master'` and `includeChildren: true`.

**Step 6: Wrap long-running operations in a task controller**
1. Use `taskLib.executeFunction()` for inline task functions or `taskLib.submitTask()` for named task descriptors.
2. Report progress using `taskLib.progress({ info, current, total })` at regular intervals during batch processing.
3. Read `assets/task-migration.template.ts` for the reusable task controller template with progress reporting.
4. Check for existing running instances with `taskLib.isRunning()` before starting a duplicate operation.
5. Use `taskLib.sleep()` for throttling between batches if the operation generates excessive load.

**Step 7: Validate and report results**
1. After the operation completes, log a summary: items processed, items created/updated/deleted, items failed, total duration.
2. For migration operations, verify target content exists by querying the destination path.
3. For publish operations, verify published state by querying the `master` branch.
4. If errors occurred, collect error details (content path, error message) into a structured report.

## Error Handling
* If `scripts/find-enonic-targets.mjs` finds no Enonic XP project, explain that the workspace does not contain an Enonic XP application.
* If a content operation fails with `contentAlreadyExists`, check whether the target exists and decide whether to update or skip. Read `references/troubleshooting.md` for duplicate handling patterns.
* If a query returns zero results, verify the query syntax, branch context, and property paths. NoQL string-format mismatches (e.g. missing `instant()` wrapper for date comparisons) are a common cause.
* If a task fails or times out, check `taskLib.get(taskId)` for state and progress details. Read `references/troubleshooting.md` for timeout and permission issues.
* If an `AccessDeniedException` occurs on publish or modify, ensure the context includes `role:system.admin` principals via `lib-context`.
