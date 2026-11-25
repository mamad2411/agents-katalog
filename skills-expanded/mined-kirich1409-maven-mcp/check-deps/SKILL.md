---
name: check-deps
description: >-
  Use when the user asks to "check deps", "check dependencies",
  "outdated dependencies", "update dependencies", "are my deps up to date", "scan for updates",
  "find outdated libraries", "upgrade dependencies", or wants to know which Maven/Gradle
  dependencies have newer versions available. Resolves the Gradle project via gradlew and
  reports available updates.
---

# Check Dependencies

Scan the current project and report which dependencies have newer versions available, then
apply the updates the user confirms. Prefer the plugin MCP tools — they use project-declared
repositories, version classification, and OSV hydration already implemented in the server.

## Step 1 — Audit via MCP (preferred)

Call **`audit_project_dependencies`** with:

- `projectPath` — project root (default: cwd)
- `includeVulnerabilities` — `true` by default; set `false` if the user only wants updates
- `productionOnly` — `true` by default; set `false` to include test-scoped deps

This single call resolves production dependencies through the project's Gradle wrapper
(one invocation), merges build-file provenance (catalogs, module paths, plugin DSL), looks
up latest versions against project repos, and optionally queries OSV. Requires `gradlew` at
the project root.

Alternatively, when you only need the declared list first:

1. `scan_project_dependencies` → extract coordinates
2. `compare_dependency_versions` with `{groupId, artifactId, currentVersion}` per entry
3. `get_dependency_vulnerabilities` for versioned coordinates (optional)

Do **not** hand-parse `maven-metadata.xml` or POST to OSV yourself while MCP tools work.

## Step 2 — Build the report

From the audit / compare results, only include entries where an upgrade is available
(`upgradeType` ≠ `none`, or `latestVersion` ≠ `currentVersion`). Group by `source.kind`:

- **catalog-library** / **catalog-plugin** — alias, current → latest, upgrade type, catalog file, usages
- **module-direct** — module, file, artifact, current → latest, configuration; flag catalog drift
- **plugins-dsl** — split settings `pluginManagement` vs root/module `plugins {}`
- **buildscript-classpath** — artifact, current → latest, file; note legacy style
- **gradle-resolved** — Gradle-resolved direct dependency with no matching build-file provenance

When `resolvedBy: "gradle"` is present on the scan/audit result, versions are Gradle-resolved
(effective versions from BOM/platform/constraints), not regex-guessed from build files.

**Terminal branch — nothing outdated and no vulnerabilities:**

> All dependencies up to date.

Stop — do not continue to edit steps.

**Vulnerabilities:** after upgrade tables, add a **Vulnerabilities** section for every entry
with non-empty `vulnerabilities`. Use server fields (`id`, `severity`, `summary`,
`fixedVersion`, `malicious`) — do not re-derive severity from a raw querybatch response.
Sort CRITICAL → HIGH → MEDIUM → LOW → unknown. Omit the section when empty.

Surface `resolvedFrom.viaPublicFallback` when true (coordinate missing from declared repos).
Surface `deadRepositoryHints` from the scan/audit when present (e.g. `jcenter()`).

## Step 3 — Confirmation

Present the full report and **ask before making any edits**. Default proposal: update
catalog entries first. Ask separately for non-catalog groups. Flag every MAJOR upgrade
explicitly.

Do not call `compare_upgrade_closure` in step 1 or step 2. The audit stays direct.

## Closure preview — after confirm, before any edit

After the user confirms a concrete set, and before editing a build file, preview that
batch once with **`compare_upgrade_closure`**. Do not diff graphs yourself. Do not union
several deps.dev calls. The pre-edit and post-edit hooks do not call this tool.

`fromVersion` is the audited current version. `toVersion` is the version the user just
confirmed. Pass `projectPath` when the project is not the working directory. Leave
`substitution` unset (`exact`) unless the user accepts the retry below.

1. **Drop rows that this tool does not compare.** Print an explicit `not closure-checked`
   line for each dropped row, name the coordinate, and do not send it. Do not later
   describe that line as `advisory: none`.

   Always drop a Gradle plugin marker: `artifactId` ends with `.gradle.plugin` and
   `groupId` is that plugin id.

   **Gradle configuration names** (`gradlew` exists). The `runtimeClasspath` predicate
   applies only here. Also drop a row when no `usages[].configuration` is a production
   runtime classpath. Read every usage, not only the first `configuration`. A usage
   counts only when all of these hold: it is not a test configuration (the name starts
   with `test`, or matches `[a-z]Test`), it is not `classpath`, it is not `compileOnly`,
   it is not `compileClasspath` and does not end with `CompileClasspath`, and the name
   is `runtimeClasspath` or ends with `RuntimeClasspath`. The Java plugin name
   `runtimeClasspath` does not end with `RuntimeClasspath` (the leading `r` is
   lowercase); the equality arm is required. Keep a row that has at least one such
   usage. Dropped rows include buildscript-only classpath and a plugin coordinate that
   is not a marker and is not on that classpath (AGP and KGP included).

   **No `gradlew`.** Do not apply the `runtimeClasspath` predicate. Maven `compile` is
   stored as `implementation` and Maven `runtime` as `runtimeOnly`; neither is
   `runtimeClasspath`, and a row with either usage stays in the batch. Still drop,
   as `not closure-checked` and not as `none`:
   - test scopes (`testImplementation`, a name that starts with `test`, or matches
     `[a-z]Test`) and `compileOnly` / `provided`;
   - `classpath`, including a row whose usages are only `classpath` (buildscript
     classpath);
   - a non-marker plugin coordinate that is only on `classpath` or plugin DSL
     (`source.kind` `plugins-dsl` or `buildscript-classpath`, and no usage is
     `implementation` or `runtimeOnly`).
   Do not print `implementation` or `runtimeOnly` as `not closure-checked`. Do not
   send a dropped row, and do not later call it `none`.

   If no library upgrade remains, do not call. Print the not-closure-checked lines
   only. An empty `upgrades` list is rejected; do not quote that error as `unknown`.

2. **No `gradlew`** (Maven project, or Gradle files without a wrapper). Do not call
   the tool once per coordinate. `auto` would select deps.dev.
   - Exactly one library upgrade left: one call with `graphSource: "depsdev"`.
   - More than one: say "a batch closure needs a Gradle wrapper" and do not call.
   - If that audit row has `isPlatform` or `managedBy`, add the BOM caveat on this
     call. The server has no `isPlatform` input; do not pass one. An empty
     public-graph diff is not "no coordinate change" for a platform or a managed
     row: deps.dev does not show versions that BOM moves elsewhere.

3. **`gradlew` exists and at least one library upgrade remains.** One call. Omit
   `graphSource` (`auto`). At most 20 library upgrades. The server rejects a longer
   list; it does not truncate. If more than 20 remain, send majors first
   (`upgradeType` `major`), then rows whose direct audit entry already has
   `vulnerabilities`. Say the rest were `not closure-checked`. Do not loop.

4. **Render that single result.** Lead with `advisory`, `graphSource`, `diffReliable`,
   and every `not closure-checked` line from the split. Then the block for `advisory`.
   Do not re-rank. A decision row is specified under [Decision row](#decision-row).
   Do not paraphrase a CVE `summary`. Skip a field only when the payload omitted it.

   The upgraded coordinate is not in `vulnerabilities.introduced` / `remaining` /
   `fixed`. Its introduced, remaining, and fixed rows are `targets[].vulnerabilityDelta`;
   keep that relation. `targets[].vulnerabilities` is `relation: target` only. Do not
   relabel a delta row `target`, and do not use the target list to fill introduced,
   remaining, or fixed. Other coordinates come from the closure buckets.

   Render every CVE decision row in those lists, whatever `advisory` is. A `stop`
   result still shows a non-MAL HIGH CVE. A `review` result still shows `fixed` and
   `MEDIUM`/`LOW` rows. `advisory` only chooses the action; it does not hide rows.

   - **`stop`** — do not edit. Also call out each `MAL-` id in `targets[].vulnerabilities`,
     `targets[].vulnerabilityDelta`, and `vulnerabilities.introduced` / `remaining` /
     `uncompared`, including `path` when present. If the same id is in both the
     target list and the delta, one row, and the relation is the delta's. Do not
     edit. Do not call an `uncompared` `MAL-` "introduced".
   - **`review`** — one decision row per introduced id from `vulnerabilityDelta` and
     from `vulnerabilities.introduced` (include an id with no severity; do not drop
     it), per `relation: target` at `CRITICAL`/`HIGH` only when that id is not
     already in `vulnerabilityDelta`, and per remaining `CRITICAL`/`HIGH` from
     `vulnerabilityDelta` and from `vulnerabilities.remaining`, still labeled
     remaining. Then license rows whose `verdict` is `violation`, and every matrix
     reason that is set: `diffReliable` false, `fixesIncomplete`, a target not
     `landed`, `rewroteVersionless`, `capabilityUnavailable`. When
     `compare_versions(safeUpgrade.version, toVersion) > 0`, say the confirmed
     direct version does not clear every known CVE and name that candidate. That
     compare is `compare_versions`: numeric segments, then stability class, qualifier
     presence, prerelease ordinals, then a lexical tie-break. Not text order (`1.10`
     is above `1.9`). An RC and a final release that share a numeric core are not equal. Ask
     again before editing. Writing that higher version is a new confirm and a new
     preview, not an in-place edit of this result.
   - **`info`** — `added` / `changed` / `removed` counts and the first rows, then
     a decision row for each remaining `MEDIUM`/`LOW`, each `fixed` id, and each
     introduced `MEDIUM`/`LOW`, from `vulnerabilityDelta` and from the closure
     buckets. License rows whose `verdict` is `review` or `ok`. Do not call the
     bump safe. Those rows are in addition to the full CVE list above, not instead of it.
   - **`unknown`** — the closure was not compared. Quote `error`. Do not fill the
     gap, and do not describe empty buckets as "no change".
   - **`none` after a compare** (`diffReliable: true`, and the target has a
     `vulnerabilities` list, empty when nothing came back) — no coordinate change
     outside the target, then that target OSV result (`relation: target`). Quote
     the non-guarantee note from `notes`. Do not say safe. On a deps.dev platform
     or `managedBy` row, do not use that closure sentence: an empty public-graph
     diff is not "no coordinate change".
   - **`none` from all-identity** (`vulnerabilities` omitted on the target, not
     `[]`) — nothing was requested to change and the current coordinate was not
     re-queried. Do not say the graphs were compared. Do not invent an empty OSV
     result. Do not say safe.

   `targets[].safeUpgrade` is one extra line on the direct coordinate, labeled
   advisory: `fixesAllKnown` and `version`, or `fixesAllKnown: false` plus
   `reason`. It is not a row per CVE. Do not present it as the version to write.

   If `landed` is false, you may offer one retry of that coordinate with
   `substitution: "module"`. The server does not launch that second pair. Do not
   send it unless the user accepts. An accepted retry is a new preview, not an edit.

`stop` ends the edit. `review` waits for the new answer. `info`, compared `none`,
all-identity `none`, and `unknown` do not mean safe; they also do not by themselves
cancel a set the user already confirmed. Step 5 stays a build check. This preview
is not a build.

### Decision row

One CVE, in this order. Same row as `/upgrade-closure`. Do not paraphrase `summary`.

1. `relation` — introduced, remaining, fixed, uncompared, or target.
2. `vulnerableNode` as `groupId:artifactId:version`.
3. `id`, linked with `url`. When `url` is empty, use `https://osv.dev/vulnerability/{id}`.
4. `severity`, or `severity unknown` when hydration left it off.
5. `summary`, or the id alone when `summary` is empty.
6. `fixedVersion`, or `fix unknown` when it was omitted.
7. `clearedBySelection`: `selected version is at or above the fix`, `selected version is still below the fix`, or omit this clause when there is no `fixedVersion`. For `relation: fixed`, say the bump no longer selects the vulnerable version.
8. `path` as an arrow chain (`g:a:v → g:a:v`) when present. When `pathOmitted` is present, say the middle was shortened and the leaf is the vulnerable node.
9. When the node is not the target and `clearedBySelection` is false: this coordinate is not the line being edited; clearing it needs a constraint or a higher root, and this preview does not propose that pin.

## Step 4 — Edit pass

Apply only the groups the user confirms, after the preview above. Touch only version values:

- Catalog — `[versions]` or inline version in `[libraries]` / `[plugins]`
- Module direct / Plugin DSL / Buildscript — inline version string in the build file
- pom.xml — `<version>` inside the matching `<dependency>`

### Catalog-aware edits (`catalog_entry`, #288)

Gradle has **no** built-in command to update `gradle/libs.versions.toml`. Before adding
or renaming catalog aliases, call **`catalog_entry`**:

- **Upgrade existing alias** — `mode: "generate"` with the same alias + new `version` and
  the current `catalogToml`. Prefer the returned `suggestedDiff` (usually a single
  `[versions]` key bump). Do not rewrite the whole file.
- **Add a library/plugin** — `mode: "generate"` with `coordinate` + `kind`. Use the
  returned `alias` / `accessor` / `suggestedDiff` as-is (kebab-case alias, reserved-segment
  safe, `libs.x` or `alias(libs.plugins.x)`).
- **Sanity-check before/after** — `mode: "validate"` with `catalogToml` and, when editing
  build scripts, `buildContent`. Fix any `violations` (reserved aliases, invalid first
  subgroups, `id(libs.plugins.x)` misuse, `libs` inside `subprojects {}` / `buildscript {}`).

Hard rules when editing catalogs by hand:

- Default catalog path is exactly `gradle/libs.versions.toml`.
- Plugins: `alias(libs.plugins…)` — never `id(libs.plugins…)`.
- Do not use reserved aliases (`extensions` / `class` / `convention`) or first segments
  `bundles` / `versions` / `plugins` (e.g. `versions-foo` is invalid; `versionsFoo` or
  `foo-versions` is fine).

## Step 5 — Build verification

After every edit pass:

- **Gradle:** `./gradlew build` (or a faster resolve check when a full build is slow)
- **Maven:** `mvn dependency:tree`

Surface failures immediately. Attempt trivial fixes; otherwise revert that entry and note
"manual upgrade required". **Never report "versions updated" without a passing build.**

## Constraints and non-goals

- Major version bumps require explicit per-entry confirmation.
- Step 1 stays direct: `audit_project_dependencies` is first-level production dependencies, not the closure. The closure preview runs only after confirm, for the library batch, and is not a safety verdict.
- The write hooks do not call `compare_upgrade_closure`. Do not add that call.
- This skill does not auto-select unstable/pre-release versions (server uses prefer-stable).
- Gradle resolution in step 1 needs `gradlew`. Maven projects are in scope: `audit_project_dependencies` still returns their rows, and the no-wrapper preview is one deps.dev call, or no call when the batch is larger or no library upgrade remains.

## Fallback (MCP unavailable only)

If MCP tools cannot be called: Glob/Read build files, extract GAVs, fetch public
`maven-metadata.xml` (Central / Google / Plugin Portal), classify versions, and optionally
POST OSV `/v1/querybatch` then hydrate via `GET /v1/vulns/{id}`. State clearly that
project-private repos, plugin-marker→implementation resolution, and server-side cache are
skipped. Do not reconstruct a closure diff on this path, and do not treat
`mvn dependency:tree` or `./gradlew dependencies` as an OSV result.
