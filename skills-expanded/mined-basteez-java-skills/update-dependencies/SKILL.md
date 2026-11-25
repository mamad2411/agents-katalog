---
name: update-dependencies
description: Check all dependencies in a Java project for newer stable versions and known CVEs, then update build files automatically.
disable-model-invocation: true
allowed-tools: Read Edit Glob Grep WebFetch Bash(mvn *) Bash(./gradlew *) Bash(gradlew.bat *)
---

# Update Dependencies

## Purpose

This skill checks all dependencies in a Java project (Maven or Gradle) for newer stable versions and known security vulnerabilities (CVEs), then updates the build files automatically — applying safe minor/patch updates directly, auto-updating high/critical CVEs to safe versions, and flagging major version bumps and medium/low CVEs for developer review.

## Prerequisites

- A Java project with a `pom.xml` (Maven) or `build.gradle`/`build.gradle.kts` (Gradle) in the project root
- Network access (the skill queries Maven Central and OSV.dev APIs)

## Usage

```
/update-dependencies
```

No arguments needed. Run from your project root.

### Expected Output

The skill produces a summary report after processing:

```
## Dependency Update Summary

### Updated Dependencies (3)
| Dependency | Old Version | New Version | Reason |
|-----------|------------|------------|--------|
| com.fasterxml.jackson.core:jackson-databind | 2.14.0 | 2.14.3 | Newer patch version |
| org.slf4j:slf4j-api | 2.0.5 | 2.0.9 | Newer minor version |
| org.apache.logging.log4j:log4j-core | 2.17.0 | 2.17.2 | CVE-2021-44832 (CVSS 6.6) + newer patch |

### Flagged for Review (1)
| Dependency | Current | Available | Reason |
|-----------|---------|-----------|--------|
| org.springframework:spring-core | 5.3.28 | 6.1.2 | Major version bump |

### CVE Findings (1)
| Dependency | CVE | Severity | CVSS | Status |
|-----------|-----|----------|------|--------|
| log4j-core 2.17.0 | CVE-2021-44832 | Medium | 6.6 | Resolved → 2.17.2 |

### Up to Date: 12 dependencies
### Skipped: 1 (private repository)
```

---

## Instructions

You are updating dependencies for a Java project. Follow each step below in order.

### Workflow Overview

1. **Detect** — Identify the build tool (Maven or Gradle) and all build files
2. **Extract** — Parse all dependencies, plugins, and BOM imports with their version sources
3. **Ecosystem Check** — Detect managed ecosystems (Spring Boot + Spring Cloud, etc.) and resolve compatible versions
4. **Lookup** — Check each non-ecosystem dependency for the latest stable version via Maven Repository metadata
5. **CVE Check** — Query OSV.dev for known vulnerabilities on current versions
6. **CVE Verify** — Re-check CVEs on target versions to avoid updating into vulnerable versions
7. **Decide** — Apply the update decision matrix (auto-update, flag, or skip)
8. **Update** — Edit build files at version source locations
9. **Verify** — Compile and run tests; roll back if the build breaks
10. **Report** — Output a formatted summary of all changes, flags, and warnings

---

### Step 1: Build Tool Detection

Scan the project root for build files:

- Look for `pom.xml` (Maven)
- Look for `build.gradle` or `build.gradle.kts` (Gradle)

**If both Maven and Gradle files exist**: Ask the user which build tool to use. Wait for their response before continuing.

**If neither exists**: Inform the user that no supported build file was found and **stop**.

**Multi-module detection**:
- **Maven**: Check for `<modules>` element in the root `pom.xml`. If present, list all child module directories.
- **Gradle**: Check for `settings.gradle` or `settings.gradle.kts` in the project root. If present, extract all `include` entries to identify subproject directories.

Record the build tool type and a list of all build files to process (root + child modules).

---

### Step 2: Dependency Extraction

Read all detected build files and extract every dependency, plugin, and BOM import. For each, record the groupId, artifactId, current version, and where the version is defined (the **version source**).

For detailed Maven and Gradle extraction patterns (property references, BOM imports, version catalogs, multi-module traversal, and general extraction rules), see [reference/build-patterns.md](reference/build-patterns.md). Read that file now to understand all supported version source formats before proceeding.

---

### Step 3: Ecosystem Compatibility Check

Before looking up individual dependency versions, detect whether the project belongs to a managed ecosystem where dependencies have cross-version compatibility constraints. In these ecosystems, you **cannot** update dependencies independently — you must respect the compatibility matrix.

#### Detection

Check the extracted dependencies and BOMs for known ecosystem markers:

| Ecosystem | Detection Signal |
|-----------|-----------------|
| Spring Boot | Parent POM `spring-boot-starter-parent` or BOM `spring-boot-dependencies` |
| Spring Cloud | BOM `spring-cloud-dependencies` or any `spring-cloud-*` dependency |
| Quarkus | BOM `quarkus-bom` or `quarkus-universe-bom` |
| Jakarta EE | BOM `jakarta.platform:jakarta.jakartaee-bom` |

#### Spring Boot + Spring Cloud Compatibility

If both Spring Boot and Spring Cloud are detected:

1. **Determine the target Spring Boot version** first (via maven-metadata.xml as in Step 4)
2. **Resolve the compatible Spring Cloud version** by fetching the Spring Initializr metadata:
   - Fetch `https://start.spring.io/actuator/info`
   - Parse the JSON response: navigate to `bom → spring-cloud → mappings`
   - Each mapping entry has a `compatibilityRange` (Spring Boot version range) and a `version` (compatible Spring Cloud version)
   - Find the mapping whose `compatibilityRange` includes the target Spring Boot version
   - Use that mapping's `version` as the target Spring Cloud version
3. **Lock all Spring Cloud dependencies** to the resolved compatible version. Do NOT look up Spring Cloud dependency versions individually via maven-metadata.xml — use only the version from the compatibility matrix.

**Example**: If Spring Boot is being updated to 3.5.x, and the Initializr metadata says Spring Cloud `2024.0.x` is compatible with Boot `3.5.x`, then update the `spring-cloud-dependencies` BOM to `2024.0.x`.

#### Other Managed Ecosystems

For Quarkus and Jakarta EE BOMs: update the BOM version via maven-metadata.xml, but **skip individual version lookups** for all dependencies managed by that BOM. The BOM controls their versions.

#### General Rule

When a dependency is managed by an ecosystem BOM, do NOT look up its version individually in Step 4. Only the BOM version should be updated. Mark all BOM-managed dependencies as `ecosystem-managed` and skip them during version lookup.

---

### Step 4: Version Lookup

For each extracted dependency that is **not** ecosystem-managed (see Step 3), look up the latest stable version.

**Maven Repository Metadata** (primary — always up to date):
- Fetch `https://repo1.maven.org/maven2/{groupId with dots replaced by slashes}/{artifactId}/maven-metadata.xml`
  - Example: for `org.springframework.boot:spring-boot-starter-parent` → `https://repo1.maven.org/maven2/org/springframework/boot/spring-boot-starter-parent/maven-metadata.xml`
- Parse the XML response:
  - `<release>` tag contains the latest release version
  - `<versions><version>` list contains all published versions (use this for pre-release filtering if `<release>` points to a pre-release)
- This is the repository's source of truth and reflects newly published versions immediately, unlike the Solr search index which can lag behind.

**Gradle Plugin Portal** (for Gradle plugins not found on Maven Central):
- Query: `https://plugins.gradle.org/plugin/{pluginId}`
- Extract the latest version from the page

**Pre-release version filtering**: Check the `<release>` version against pre-release patterns (case-insensitive, with optional numeric suffix):
- `-SNAPSHOT`
- `-alpha` / `-Alpha` / `-ALPHA`
- `-beta` / `-Beta` / `-BETA`
- `-RC` / `-rc`
- `-M` (milestone, e.g., `-M1`, `-M2`)
- `-CR` (candidate release)

If the `<release>` version is a pre-release, walk the `<versions>` list in reverse order and pick the first version that does NOT match any pre-release pattern.

**Version comparison**: Parse versions as `major.minor.patch` (tolerating additional segments like qualifiers):
- If `latestMajor > currentMajor` → classify as **major** update
- If `latestMinor > currentMinor` (same major) → classify as **minor** update
- If `latestPatch > currentPatch` (same major.minor) → classify as **patch** update
- If versions are equal → classify as **none** (already up to date)
- For non-semver versions (e.g., date-based like `20230301`) → classify as **unknown** and flag for review

Record for each dependency: `latestStableVersion`, `updateType` (major/minor/patch/none/unknown).

---

### Step 5: CVE Check (Current Version)

For each dependency, check the **current** version for known security vulnerabilities.

**OSV.dev API**:
- Use web fetch to POST to `https://api.osv.dev/v1/query` with body:
  ```json
  {
    "version": "<currentVersion>",
    "package": {
      "name": "<groupId>:<artifactId>",
      "ecosystem": "Maven"
    }
  }
  ```
- Parse the response for vulnerabilities. For each vulnerability, record:
  - **ID**: The vulnerability identifier (e.g., `CVE-2021-44228`, `GHSA-xxxx`)
  - **Severity**: Based on CVSS score — LOW (0.1–3.9), MEDIUM (4.0–6.9), HIGH (7.0–8.9), CRITICAL (9.0–10.0)
  - **CVSS score**: Extract from `severity[].score` (look for `CVSS_V3` type first, fall back to `CVSS_V2`)
  - **Fixed version**: Extract from `affected[].ranges[].events[]` where `type` is `FIXED`
  - **Description**: Brief summary from the `summary` or `details` field

If the API returns no vulnerabilities, the dependency is clean for this version.

If the API call fails (network error, timeout), report the dependency as "CVE check failed" and continue processing other dependencies.

---

### Step 6: CVE Verification (Target Version)

For each dependency that will be updated (has a newer minor/patch version, or a CVE-driven update), check the **target** (latest stable) version for CVEs using the same OSV.dev API query but with the target version.

**Decision logic based on target version CVE results**:

- **Target version has no CVEs**: Safe to proceed with the update
- **Target version has high/critical CVE (CVSS >= 7.0)**: Do **NOT** auto-update. Flag with warning: "Latest version also has known high/critical vulnerability — no safe version available. Manual review required."
- **Target version has only medium/low CVEs (CVSS < 7.0)**: Proceed with the update but note the remaining CVE in the report

---

### Step 7: Update Decisions

For each dependency, apply this decision matrix:

| Condition | Action |
|-----------|--------|
| Newer minor/patch version, no CVE on current or target | **Auto-update** to latest stable |
| Newer major version, no CVE | **Flag for review** — do NOT auto-update |
| Current version has CVE with CVSS >= 7.0, target is clean | **Auto-update** to latest safe version |
| Current version has CVE with CVSS >= 7.0, target also has high/critical CVE | **Flag for review** — warn "no safe version available" |
| Current version has CVE with CVSS >= 7.0, target has only medium/low CVE | **Auto-update** but note remaining CVE in report |
| Current version has CVE with CVSS < 7.0, no version update needed | **Flag for review** — medium/low CVE, inform developer |
| Major version bump AND current has high/critical CVE, target is clean | **Auto-update** — security overrides major-bump caution |
| Private/unresolvable dependency (not found on Maven Central) | **Skip** and report separately |
| Already at latest stable version, no CVE | **Report as up to date** |
| Already at latest stable version, has CVE | **Flag for review** — warn "current version is latest but has known CVE" |
| Malformed version string | **Skip** and report separately |
| Version lookup failed (network error) | **Skip** and report separately |

---

### Step 8: Apply Updates

For each dependency marked for auto-update, edit the build file to change the version.

**Critical rules**:
1. **Update at the version source** — edit the property definition, `ext` variable, version catalog entry, or BOM version. Do NOT edit `${...}` reference sites or individual dependency declarations that use a shared property.
2. **Preserve file formatting** — maintain existing indentation, spacing, line endings, and comments. Do not reformat or reorganize the file.
3. **One edit per version source** — if multiple dependencies share a property (e.g., `spring.version`), update the property once. Do not make duplicate edits.

---

### Step 9: Build Verification

After applying all updates, verify the project still compiles and tests pass. **This step is mandatory — never skip it.**

**1. Run compilation**:
- **Maven**: `mvn compile -q` (quiet mode to reduce noise)
- **Gradle**: `./gradlew compileJava --quiet` (or `gradlew.bat` on Windows)

**2. If compilation succeeds, run tests**:
- **Maven**: `mvn test -q`
- **Gradle**: `./gradlew test --quiet`

**3. If compilation OR tests fail**:
- Read the build output to identify which updated dependency caused the failure
- **Roll back the failing update(s)**: revert the version in the build file to its original value
- Re-run compilation and tests after each rollback to confirm the project is green again
- Move rolled-back dependencies from the "Updated" list to the "Flagged for Review" list with the reason: "Update caused build/test failure — reverted to {originalVersion}. Error: {brief error description}"
- If multiple updates were applied and it's unclear which one caused the failure, roll back all updates, then re-apply them one at a time, running the build after each to isolate the breaking update(s)

**4. If compilation and tests pass**: All updates are confirmed safe. Proceed to the summary report.

**Note**: If the project did not compile or pass tests *before* the skill ran (pre-existing failures), inform the user and still proceed with the report — but note that pre-existing build issues were detected.

---

### Step 10: Summary Report

After all updates are verified (or rolled back), output a formatted summary report with these sections:

#### Section 1: Updated Dependencies
List all dependencies that were auto-updated.

```
### Updated Dependencies ({count})
| Dependency | Old Version | New Version | Reason |
|-----------|------------|------------|--------|
| groupId:artifactId | x.y.z | x.y.w | Newer patch/minor version |
```

If no dependencies were updated, show: `### Updated Dependencies: None`

#### Section 2: Flagged for Review
List all dependencies flagged for developer review.

```
### Flagged for Review ({count})
| Dependency | Current | Available | Reason |
|-----------|---------|-----------|--------|
| groupId:artifactId | x.y.z | a.b.c | Major version bump / Medium CVE / No safe version / Build failure (reverted) |
```

If none flagged, show: `### Flagged for Review: None`

#### Section 3: CVE Findings
List all CVEs found across all dependencies.

```
### CVE Findings ({count})
| Dependency | CVE | Severity | CVSS | Status |
|-----------|-----|----------|------|--------|
| artifactId x.y.z | CVE-XXXX-XXXXX | High | 8.1 | Resolved → a.b.c / Flagged / No safe version |
```

If no CVEs found, show: `### CVE Findings: None`

#### Section 4: Skipped
List dependencies that could not be processed.

```
### Skipped ({count})
- `groupId:artifactId` — reason (private repository / lookup failure / malformed version)
```

If none skipped, show: `### Skipped: None`

#### Section 5: Up to Date
Count of dependencies already at the latest stable version with no CVEs.

```
### Up to Date: {count} dependencies
```

---

Now detect the build tool and begin processing dependencies for this project.
