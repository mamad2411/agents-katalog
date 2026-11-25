---
name: conductor-defect
model: claude-opus-4-8
effort: high
description: >
  Fix bugs reported by humans from a BUG.md file. Takes an application name (mandatory),
  version (optional â€” supports single version, comma-separated list, "all", or omit for all),
  and module (optional), resolves the context folder automatically from root-level application
  folders. When multiple versions are provided (or "all"/omitted), versions are processed
  SEQUENTIALLY in ascending semver order â€” all bugs from version N are fully resolved before
  version N+1 begins. Tags untagged bugs, creates a BUG_MASTER.md tracking checklist, then
  fixes each bug one at a time: reproduce with Playwright, write a test spec, plan the fix,
  apply the fix, verify, and update related artifacts (mockups, specifications, module models,
  user stories). Integrates with Ralph Loop to ensure all bugs are fully fixed across sessions.
  Use this skill when the user asks to "fix bugs", "fix bug", "start bug fixing", "resolve bugs
  from BUG.md", "bug fix session", or any request to systematically fix bugs from a BUG.md file.
  Also trigger when user says "resume bug fixing" to continue from where a previous session left
  off using BUG_MASTER.md progress file.
---

# Bug Fixer

Fix bugs reported by humans one at a time, tracked via BUG_MASTER.md and per-bug BUG_FIX_PLAN.md.

## Ralph Loop Integration (INTERNAL â€” FULLY AUTOMATIC)

This skill internally manages Ralph Loop. The user does NOT need to invoke `/ralph-loop` or know
about Ralph Loop at all. The skill handles starting, iterating, and completing the loop transparently.

### Internal Auto-Start Mechanism

When this skill is invoked (e.g., `/conductor-defect hub_middleware version:v1.0.4`), the
**very first action** â€” before reading any files, before Phase 0, before ANYTHING â€” is to
silently start Ralph Loop by invoking the Skill tool internally:

```
Skill(skill: "ralph-loop:ralph-loop", args: "<original-user-invocation-with-all-args> --completion-promise \"ALL BUGS RESOLVED\" --max-iterations 50")
```

**Construction rule**: Take the EXACT text the user typed (e.g., `/conductor-defect hub_middleware
version:v1.0.4 module:location-information`) and pass it as the `args` value, appending the
`--completion-promise` and `--max-iterations` flags.

| User types | Ralph Loop args |
|------------|----------------|
| `/conductor-defect hub_middleware` | `/conductor-defect hub_middleware --completion-promise "ALL BUGS RESOLVED" --max-iterations 50` |
| `/conductor-defect hub_middleware version:v1.0.4` | `/conductor-defect hub_middleware version:v1.0.4 --completion-promise "ALL BUGS RESOLVED" --max-iterations 50` |
| `/conductor-defect hub_middleware version:v1.0.3,v1.0.4` | `/conductor-defect hub_middleware version:v1.0.3,v1.0.4 --completion-promise "ALL BUGS RESOLVED" --max-iterations 50` |
| `/conductor-defect hub_middleware version:all` | `/conductor-defect hub_middleware version:all --completion-promise "ALL BUGS RESOLVED" --max-iterations 50` |
| `/conductor-defect hub_middleware version:v1.0.4 module:location-information` | `/conductor-defect hub_middleware version:v1.0.4 module:location-information --completion-promise "ALL BUGS RESOLVED" --max-iterations 50` |

**Skip if already active**: If `.claude/ralph-loop.local.md` already exists, Ralph Loop is
already running (this is a resumed iteration). Do NOT re-invoke â€” proceed directly to Phase 0.

**BLOCKING**: Do NOT proceed with ANY work until Ralph Loop is confirmed active (either freshly
started or already running from a previous iteration).

### How It Works (Transparent to User)

1. User invokes `/conductor-defect` with their arguments â€” they never see or interact with Ralph Loop
2. This skill silently starts Ralph Loop with the conductor-defect prompt as the loop body
3. On each iteration, the agent reads BUG_MASTER.md to find the next unresolved bug
4. The agent fixes one or more bugs until context runs out or all bugs are resolved
5. When the agent tries to exit, Ralph Loop re-feeds the same prompt automatically
6. The next iteration resumes from where the last one left off (tracked in BUG_MASTER.md)
7. When ALL bugs are resolved, the agent outputs the completion promise to exit the loop
8. The user only sees bug-fixing progress â€” Ralph Loop is an invisible persistence layer

### Completion Promise

When ALL bugs in BUG_MASTER.md have a terminal status (`FIXED`, `CANNOT_REPRODUCE`, or
`HIGH_IMPACT`), output the following promise tag to signal Ralph Loop that bug fixing is done:

```
<promise>ALL BUGS RESOLVED</promise>
```

**CRITICAL**: Only output this promise when EVERY bug in BUG_MASTER.md has a terminal status.
Do NOT output the promise prematurely. Do NOT output it to escape the loop.

### Iteration Awareness (Internal)

At the START of every iteration (including the first), the agent MUST:
1. Check if Ralph Loop is already active (if `.claude/ralph-loop.local.md` exists, skip re-invoking)
2. If NOT active, silently invoke Ralph Loop as described above
3. Read BUG_MASTER.md to determine what is already resolved
4. Find the FIRST bug with status `NEW` or `IN_PROGRESS`
5. If that bug has a BUG_FIX_PLAN.md, read it to find the last incomplete step
6. Resume from exactly that point â€” do NOT re-fix already-resolved bugs
7. If ALL bugs have terminal status, output the completion promise and stop

## Inputs

The skill expects these arguments:

```
/conductor-defect <application> [version:<version>] [module:<module>]
```

| Argument | Required | Example | Description |
|----------|----------|---------|-------------|
| `<application>` | Yes | `hub_middleware` | Application name to locate the context folder |
| `version:<version>` | No | `version:v1.0.4` or `version:v1.0.3,v1.0.4` or `version:all` | Filter bugs by version. Supports single version, comma-separated list, `all`, or omit for all versions. Multiple versions are processed sequentially in ascending semver order |
| `module:<module>` | No | `module:location-information` | Filter bugs by module |

### Input Resolution

The application name is matched against root-level application folders:
1. Strip any leading `<number>_` prefix from folder names
2. Match case-insensitively
3. Accept snake_case, kebab-case, or title-case input
4. If no match found, list available applications and stop

### Auto-Resolved Paths

| File | Resolved Path |
|------|---------------|
| BUG.md | `<app_folder>/context/BUG.md` |
| PRD.md | `<app_folder>/context/PRD.md` |
| Bug Tracking Output | `<app_folder>/context/bug/` |
| Module Models | `<app_folder>/context/model/` |
| HTML Mockups | `<app_folder>/context/mockup/` |
| Specifications | `<app_folder>/context/specification/` |

### Argument Combinations

| Provided | Behavior |
|----------|----------|
| `<application>` only | All versions (sequential, ascending semver), all modules |
| `<application>` + `version:v1.0.4` | Single version, all modules |
| `<application>` + `version:v1.0.3,v1.0.4` | Multiple versions (sequential, ascending semver), all modules |
| `<application>` + `version:all` | All versions (sequential, ascending semver), all modules |
| Any above + `module:<module>` | Same as above, filtered to specific module |

### Version Resolution

The `version:` argument supports four forms:

| Form | Example | Behavior |
|------|---------|----------|
| Single version | `version:v1.0.3` | Process only v1.0.3 |
| Comma-separated list | `version:v1.0.1,v1.0.2,v1.0.3` | Process each version sequentially in ascending semver order |
| Explicit all | `version:all` | Discover all versions from BUG.md, process sequentially in ascending semver order |
| Omitted | _(no version arg)_ | Same as `version:all` |

#### Version Discovery

When `version:all` or omitted:
1. Scan BUG.md for all `[vX.Y.Z]` version tags across all module sections
2. Collect unique versions
3. Sort in ascending semantic version order (v1.0.0 < v1.0.1 < v1.1.0 < v2.0.0)
4. This becomes the ordered version list for sequential processing

#### Sequential Version Processing Rule

**Versions are ALWAYS processed one at a time, in ascending semver order.** All bugs from
version N must be fully resolved (terminal status: `FIXED`, `CANNOT_REPRODUCE`, or `HIGH_IMPACT`)
before ANY bug from version N+1 is started. This ensures:
- Bug fixes from earlier versions are in place before later version bugs are addressed
- The codebase is progressively stabilized version by version
- Each version's fixes build on a stable foundation from prior versions

### Context Folder Structure (Expected)

```
<app_folder>/context/
  BUG.md                     # Bug reports grouped by module, optionally versioned
  PRD.md              # User stories (for recording bug fixes)
  bug/                       # Bug tracking folder (BUG_MASTER.md + per-module subfolders)
    BUG_MASTER.md            # Master checklist (created by this skill)
    <module-slug>/           # Per-module folder
      <BUG-XXX>/             # Per-bug folder (named by bug tag)
        screenshot_*.png     # Reproduction screenshots
        BUG_TEST_SPEC.md     # Test spec for verification
        BUG_FIX_PLAN.md      # Fix plan with checklist
  model/                     # Module models (updated if fix involves model changes)
  mockup/                    # HTML mockups (updated if fix involves UI changes)
  specification/             # Technical specifications (updated if fix involves logic changes)
```

## Pre-Requisite: Project Information from CLAUDE.md (MANDATORY)

**CLAUDE.md is automatically loaded into context** at the start of every session. It contains
project details, infrastructure paths, credentials, and configuration. You do NOT need to read
it manually â€” the information is already available in your context.

**Before executing ANY tool command** (Maven build, Spring Boot run, database CLI, Keycloak CLI,
Playwright test, npm start, etc.), use the following from CLAUDE.md (already in context):

- **JDK path** â€” Use the exact `JAVA_HOME` path specified in CLAUDE.md
- **Maven path** â€” Use the exact Maven binary path specified in CLAUDE.md
- **Database credentials** â€” Host, port, username, password
- **Keycloak configuration** â€” Host, admin credentials, CLI path
- **Any other infrastructure details** â€” Ports, URLs, connection strings

**WHY**: CLAUDE.md contains the actual system paths, credentials, and configuration for the
developer's machine. Every shell command MUST use the values from CLAUDE.md.

## BUG.md Format

The BUG.md file follows a hierarchical structure mirroring the module structure in CLAUDE.md:

- **Top-level groups** are H1 headers: `# Common`, `# System Module`, `# Business Module`
- **Modules** are H2 headers under their respective group (e.g., `## UI/UX Standards` under `# Common`,
  `## User` under `# System Module`, `## Employer` under `# Business Module`)
- Under each module, bugs are listed as top-level bullet items. Each bug may optionally have a version
  tag (e.g., `[v1.0.4]`) on the line immediately before the bug items for that version.

```markdown
# Common

## UI/UX Standards
[v1.0.4]
- Bug description here
  - Priority: High
  - Steps to Reproduce:
    1. Step 1
    2. Step 2
  - Expected Result: ...

[v1.0.5]
- Another bug for a different version

---

# System Module

## User
[v1.0.5]
- Bug description here

---

## Notification

---

## Activities

---

## Audit Trail

---

## Document Management

---

# Business Module

## Location Information

---

## Corridor

---

## Recruitment Step

---

## Employer

---

## Recruitment Agent

---

## Industrial Classification

---

## Occupation Classification

---

## Job Demand
[v1.0.6]
- Bug description here

---

## Candidate Registration
```

### Version Filtering Logic

- Version tags appear as `[vX.Y.Z]` on their own line within a module section
- When a single `version:` filter is provided, only include bugs that appear AFTER the matching
  version tag and BEFORE the next version tag or module header
- When a comma-separated list is provided (e.g., `version:v1.0.3,v1.0.4`), include bugs from
  each listed version. Bugs are grouped by version for sequential processing
- When `version:all` or version is omitted, discover ALL `[vX.Y.Z]` tags in BUG.md, collect
  bugs from every version, and group them by version for sequential processing
- **Sequential processing**: Regardless of how versions are specified (list, all, omitted),
  when multiple versions are resolved, bugs are processed version-by-version in ascending
  semver order. All bugs from version N must reach terminal status before version N+1 begins

### Module Filtering Logic

- Module headers are H2 (`## Module Name`) under their parent group (H1) in BUG.md
- The parent groups (`# Common`, `# System Module`, `# Business Module`) are NOT modules themselves
  â€” they are organizational headers
- When `module:` filter is provided, only include bugs under the matching H2 module section
- Module matching: convert filter value to title case for matching (e.g., `location-information`
  matches `## Location Information`, `ui-ux-standards` matches `## UI/UX Standards`)
- When no `module:` filter is provided, include ALL modules across all groups

## Bug Tagging Convention

Bug tags follow the format: `BUG-XXX` where `XXX` is a zero-padded running number with interval
of 1, starting from `001`.

- Tag format: `BUG-001`, `BUG-002`, `BUG-003`, ...
- Tags are inserted as `[BUG-XXX]` at the start of the bug description (after the `- `)
- Only tag bugs that do NOT already have a `[BUG-XXX]` tag
- Scan the entire BUG.md to find the highest existing tag number before assigning new ones
- Continue numbering from the highest existing number + 1

Example before tagging:
```markdown
- Table formatting in document management is not consistent...
```

Example after tagging:
```markdown
- [BUG-001] Table formatting in document management is not consistent...
```

## Version Gate

Before starting any work, check `CHANGELOG.md` in the application folder (`<app_folder>/CHANGELOG.md`):

1. If `<app_folder>/CHANGELOG.md` does not exist, skip this check (first-ever execution for this application).
2. If `<app_folder>/CHANGELOG.md` exists, scan all `## vX.Y.Z` headings and determine the **highest version** using semantic versioning comparison.
3. Apply the gate based on the version argument form:
   - **Single version**: If requested version **<** highest version â†’ **STOP immediately**. Print: `"Version {requested} is lower than the current application version {highest} recorded in <app_folder>/CHANGELOG.md. Execution rejected."`
   - **Comma-separated list**: Check the **lowest** version in the list. If lowest **<** highest version â†’ **STOP immediately**. Print: `"Version {lowest} in the provided list is lower than the current application version {highest} recorded in <app_folder>/CHANGELOG.md. Execution rejected."`
   - **`version:all` or omitted**: Skip this check â€” when processing all discovered versions, historical versions are expected to be present in the source file.

## PRD.md Extended Sections

When fixing bugs, check PRD.md for the following extended sections and use them as diagnostic context:

### Design System

If PRD.md contains a `# Design System` section referencing a `DESIGN_SYSTEM.md` file:
- When fixing UI bugs (wrong color, incorrect styling, layout issues), consult the design system to determine the **correct** appearance before applying a fix
- The design system is the authoritative source for visual expectations

### Architecture Principle

If PRD.md contains an `# Architecture Principle` section:
- Use architectural patterns for root cause analysis context
- If a bug reports "data inconsistency between modules" and architecture declares "event-driven", focus on fixing event handling (retry, idempotency) rather than adding direct cross-module DB queries
- If architecture declares "stateless" and a bug relates to session state, the fix should ensure no server-side session storage

### High Level Process Flow

If PRD.md contains a `# High Level Process Flow` section:
- **Trace the bug against the process flow** to identify which step is failing
- This provides systematic root cause analysis: Was the message received? Validated? Stored? Was the ACK step reached? Which step failed?
- The process flow serves as a step-by-step debugging guide for message-driven bugs

---

## Workflow

### Phase 0: Resume Check (Runs Every Ralph Loop Iteration)

This phase runs at the START of every iteration, including the first.

0. **Ensure Ralph Loop is active (INTERNAL â€” silent)** â€” Check if `.claude/ralph-loop.local.md`
   exists. If it does NOT exist, silently invoke Ralph Loop using the Skill tool as described
   in the "Internal Auto-Start Mechanism" section above. The user should NOT be informed about
   this step â€” it is an internal implementation detail. If the file already exists, skip this step.

1. **Use project information from CLAUDE.md (already in context)** â€” extract JDK path, Maven path, database credentials,
   and all infrastructure details. These values are required for every subsequent tool command.

2. Check if `<app_folder>/context/bug/BUG_MASTER.md` exists

3. If it exists, read it and determine the current state:
   - **Resolve the version list** using the Version Resolution rules (same as Phase 1)
   - Read the **Version Processing Order** table from BUG_MASTER.md
   - **New version detection**: Compare the resolved version list against the versions tracked
     in the Version Processing Order table. If BUG.md contains versions that are NOT yet in
     the Version Processing Order table (and those versions have bugs matching the module filter):
     - These are **new versions added since the last run**
     - Add them to the Version Processing Order table with status `NEW`
     - Tag any untagged bugs for these new versions (same as Step 1.2)
     - Add new version sections with their bug tables to BUG_MASTER.md
     - Update the Summary table counts
     - Resume processing from the first new version
   - Scan the Version Processing Order table for the FIRST version with status != `COMPLETED`
   - If ALL versions are `COMPLETED` (and therefore all bugs have terminal status) â†’
     output `<promise>ALL BUGS RESOLVED</promise>` and stop
   - Otherwise, within the active version section, find the FIRST bug with status `NEW` or
     `IN_PROGRESS`
   - Read its `BUG_FIX_PLAN.md` (if exists) for detailed progress
   - Resume from the last incomplete step within that version

4. If it does not exist, proceed to Phase 1 (fresh start)

### Phase 1: Pre-Implementation â€” Analyze, Tag, and Create Master Checklist

#### Step 1.1: Read, Resolve Versions, and Filter BUG.md

1. Read `<app_folder>/context/BUG.md`
2. **Resolve the version list** using the Version Resolution rules:
   - Single version â†’ `[v1.0.4]`
   - Comma-separated â†’ parse and sort ascending by semver â†’ `[v1.0.3, v1.0.4]`
   - `all` or omitted â†’ scan BUG.md for ALL `[vX.Y.Z]` tags, deduplicate, sort ascending â†’ `[v1.0.1, v1.0.2, v1.0.3, ...]`
3. Apply module filter if provided
4. For each resolved version, identify all bugs that match the filter criteria
5. Count the total bugs per version and overall

#### Step 1.2: Tag Untagged Bugs

1. Scan the ENTIRE BUG.md for existing `[BUG-XXX]` tags to find the highest number
2. For each untagged bug (matching the filter), assign the next `[BUG-XXX]` tag
3. Write the updated BUG.md with new tags applied
4. **IMPORTANT**: Only tag bugs that do NOT already have a tag. Never modify existing tags.

#### Step 1.3: Create BUG_MASTER.md

Create `<app_folder>/context/bug/BUG_MASTER.md` with this structure:

```markdown
# Bug Master â€” <Application Name>

**Started**: <date>
**Context**: <app_folder>/context
**Resolved Versions**: <comma-separated sorted version list, e.g., "v1.0.3, v1.0.4, v1.0.5">
**Module Filter**: <module or "All">
**Status**: IN PROGRESS

---

## Version Processing Order

| # | Version | Bug Count | Status | Started | Completed |
|---|---------|-----------|--------|---------|-----------|
| 1 | v1.0.3 | 3 | NEW | - | - |
| 2 | v1.0.4 | 5 | NEW | - | - |
| 3 | v1.0.5 | 2 | NEW | - | - |

> **Processing Rule**: All bugs from version N must reach terminal status before version N+1 begins.

---

## v1.0.3

### <Module Name>

| Code | Description | Status | Remark |
|------|-------------|--------|--------|
| BUG-001 | Short description of the bug | NEW | |
| BUG-002 | Short description of the bug | NEW | |

---

### <Another Module>

| Code | Description | Status | Remark |
|------|-------------|--------|--------|
| BUG-003 | Short description of the bug | NEW | |

---

## v1.0.4

### <Module Name>

| Code | Description | Status | Remark |
|------|-------------|--------|--------|
| BUG-004 | Short description of the bug | NEW | |

---

## Summary

| Status | Count |
|--------|-------|
| NEW | X |
| IN_PROGRESS | 0 |
| FIXED | 0 |
| CANNOT_REPRODUCE | 0 |
| HIGH_IMPACT | 0 |
| **Total** | **X** |
```

**IMPORTANT â€” Single version shortcut**: When only a single version is resolved (either
explicitly provided or only one version exists in BUG.md), the BUG_MASTER.md still uses
the same structure above but with only one version section. The Version Processing Order
table will have a single row.

**IMPORTANT â€” Version-first organization**: Bugs are grouped by version (H2), then by
module (H3) within each version. This ensures the version-sequential processing order
is visually clear and easy to track.

**Status Values:**
- `NEW` â€” Bug has been tagged but not yet worked on
- `IN_PROGRESS` â€” Bug is currently being investigated/fixed
- `FIXED` â€” Bug has been fixed and verified
- `CANNOT_REPRODUCE` â€” Bug could not be reproduced via Playwright
- `HIGH_IMPACT` â€” Fix would potentially break other working functionalities; deferred

### Phase 2: Implementation â€” Fix Each Bug (Version by Version, One at a Time)

Process bugs **version by version** in the order defined in the Version Processing Order table:

1. Find the FIRST version in the Version Processing Order table with status != `COMPLETED`
2. Update that version's status to `IN_PROGRESS` and record the start date
3. Within that version section, find the FIRST bug with status `NEW` or `IN_PROGRESS`
4. Fix that bug using Steps 2.1â€“2.8 below
5. After fixing, check if ALL bugs in the current version have terminal status:
   - If YES â†’ mark the version as `COMPLETED` in the Version Processing Order table, record
     completion date, and move to the NEXT version (step 1)
   - If NO â†’ find the next `NEW` bug in the same version and continue
6. Repeat until ALL versions are `COMPLETED`

For each bug with status `NEW` in BUG_MASTER.md (within the current version), in order:

#### Step 2.1: Initialize Bug Folder

1. Update BUG_MASTER.md: set the current bug's status to `IN_PROGRESS`
2. Create folder: `<app_folder>/context/bug/<module-slug>/<BUG-XXX>/`
3. This folder will contain all artifacts for this specific bug

#### Step 2.2: Reproduce the Bug with Playwright

1. Read the bug description from BUG.md (including reproduction steps and expected result)
2. Write a Playwright script to reproduce the bug â€” save the script file in the bug folder:
   `<app_folder>/context/bug/<module-slug>/<BUG-XXX>/reproduce.spec.ts`
3. In the Playwright script, use **explicit screenshot paths** pointing to the bug folder.
   Do NOT rely on Playwright's default screenshot location. Use `page.screenshot()` with an
   absolute or project-relative path:
   ```typescript
   await page.screenshot({
     path: '<app_folder>/context/bug/<module-slug>/<BUG-XXX>/screenshot_reproduce.png',
     fullPage: true
   });
   ```
4. Run the Playwright script: `npx playwright test <path-to-script> --config=<playwright-config>`

**CRITICAL**: Screenshots MUST be saved to `<app_folder>/context/bug/<module-slug>/<BUG-XXX>/`.
Do NOT save screenshots in the application source folder, test output folder, or Playwright's
default results directory. The bug folder in the application's `context/` folder is the single source of truth for all
bug artifacts.

**IF able to reproduce:**
- Update BUG_MASTER.md remark: "Reproduced successfully"
- Proceed to Step 2.3

**IF NOT able to reproduce:**
- Update BUG_MASTER.md: set status to `CANNOT_REPRODUCE`, add remark with details
- Save the screenshot showing the current (non-buggy) state to the bug folder
- Move to the next bug

#### Step 2.3: Write Test Spec

Create `<app_folder>/context/bug/<module-slug>/<BUG-XXX>/BUG_TEST_SPEC.md`:

```markdown
# Test Spec â€” <BUG-XXX>

**Bug**: <Short description>
**Module**: <Module Name>
**Reproduced**: Yes

---

## Pre-Conditions

- <List any required state, data, or login credentials>

## Steps to Verify Fix

1. <Step-by-step instructions to verify the bug is fixed>
2. <Navigate to...>
3. <Assert that...>

## Expected Result After Fix

- <What the user should see when the bug is fixed>

## Playwright Verification Script

```typescript
// Playwright test to verify the fix
test('<BUG-XXX>: <description>', async ({ page }) => {
  // Steps to verify...

  // IMPORTANT: Save screenshots to the bug folder, NOT the source folder
  await page.screenshot({
    path: '<app_folder>/context/bug/<module-slug>/<BUG-XXX>/screenshot_fixed.png',
    fullPage: true
  });
});
```
```

#### Step 2.4: Analyze and Plan the Fix

1. Analyze the bug in detail â€” read relevant source code, templates, configurations
2. Determine the root cause
3. Plan how to fix it
4. Assess impact on other functionalities

Create `<app_folder>/context/bug/<module-slug>/<BUG-XXX>/BUG_FIX_PLAN.md`:

```markdown
# Fix Plan â€” <BUG-XXX>

**Bug**: <Short description>
**Module**: <Module Name>
**Root Cause**: <What is causing the bug>
**Impact Assessment**: <Low/Medium/High â€” does fixing this affect other features?>

---

## Fix Checklist

- [ ] 1. <First change to make>
- [ ] 2. <Second change to make>
- [ ] 3. Verify fix with BUG_TEST_SPEC.md
- [ ] 4. Update artifacts (mockups/specs/models/user stories)

---

## Files to Modify

| File | Change Description |
|------|-------------------|
| `path/to/file.jte` | Fix table styling |
| `path/to/file.java` | Update method logic |

---

## Fix Log

### Step 1: <description>
<timestamp> - Started
- Changes made: ...
- Result: ...
```

**IF the fix potentially affects other working functionalities (HIGH_IMPACT):**
- Update BUG_MASTER.md: set status to `HIGH_IMPACT`, add remark explaining the risk
- Record the analysis in BUG_FIX_PLAN.md
- Do NOT apply the fix
- Move to the next bug

**IF safe to fix:**
- Proceed to Step 2.5

#### Step 2.5: Apply the Fix

1. Make the code changes as planned in BUG_FIX_PLAN.md
2. **Annotate the fix in source (MANDATORY)** â€” On EACH method, block, or template region
   modified by the fix, leave a `[BUG-XXX]` marker comment using the language's native
   comment style:
   - Java method: prepend a Javadoc line `* [BUG-XXX] <one-line description>` (or extend
     the existing Javadoc if the method already has one)
   - PHP / TypeScript / JavaScript: same pattern with PHPDoc / JSDoc
   - Blade template: `{{-- [BUG-XXX] <description> --}}` immediately above the changed block
   - JTE template: `@* [BUG-XXX] <description> *@` immediately above the changed block
   - HTML / SQL: `<!-- [BUG-XXX] <description> -->` / `-- [BUG-XXX] <description>`
   - YAML / `.env` / `.properties`: `# [BUG-XXX] <description>` above the changed key

   Example (Java service method):
   ```java
   /**
    * [BUG-024] Trim leading whitespace from corridor code before lookup.
    */
   public Corridor findByCode(String code) { ... }
   ```

   The marker enables `git blame` and IDE search to trace any modified line back to
   BUG.md without consulting BUG_FIX_PLAN.md.
3. **Append to top-of-file traceability comment (if present)** â€” If the modified file
   already carries a top-of-file traceability comment (from `conductor-feature-develop`'s
   code-level traceability rule), append the `[BUG-XXX]` code to its `Bug fixes:` line,
   creating the line if it does not yet exist. Use the `USHM#####` / `NFRHM####` /
   `CONSHM###` / `REFHM####` codes already present in the file â€” do NOT change them:
   ```java
   /**
    * Implements: USHM00003, USHM00006
    * NFR: NFRHM0003
    * Bug fixes: [BUG-024]
    */
   public class CorridorService { ... }
   ```
4. Update BUG_FIX_PLAN.md: check off completed items, log changes in the Fix Log section

#### Step 2.6: Verify the Fix

1. Run the verification from BUG_TEST_SPEC.md (Playwright test)
2. Capture post-fix screenshot using an explicit path in the Playwright script:
   ```typescript
   await page.screenshot({
     path: '<app_folder>/context/bug/<module-slug>/<BUG-XXX>/screenshot_fixed.png',
     fullPage: true
   });
   ```
   Do NOT save screenshots in the application source folder â€” always use the bug folder under `<app_folder>/context/`.

**IF verified (test passes):**
- Update BUG_MASTER.md: set status to `FIXED`
- Update BUG_FIX_PLAN.md: mark all checklist items as completed
- Proceed to Step 2.7

**IF NOT verified (test fails):**
- Log the failure in BUG_FIX_PLAN.md
- Go back to Step 2.4 to re-analyze and re-plan
- Apply a different fix approach

#### Step 2.7: Update Related Artifacts

Analyze the fix to determine which artifacts need updating:

**A. UI Fix â†’ Update Mockups**

If the fix changed the visual appearance (HTML/CSS/layout changes in JTE templates):
1. Navigate to `<app_folder>/context/mockup/` and find the relevant module screens
2. Update the HTML mockup files to reflect the fix
3. Log the mockup changes in BUG_FIX_PLAN.md

**B. Code Logic Fix â†’ Update Specifications**

If the fix involved code logic changes (service layer, controller logic, validation):
1. Navigate to `<app_folder>/context/specification/<module-slug>/`
2. Update the SPEC.md to reflect the changed behavior
3. Log the specification changes in BUG_FIX_PLAN.md

**C. Module Model Fix â†’ Update Models**

If the fix involved module model changes (new/removed fields, collection changes):
1. Navigate to `<app_folder>/context/model/<module-slug>/`
2. Update `model.md`, `schemas.json`, and `document-model.mermaid` as needed
3. Log the model changes in BUG_FIX_PLAN.md

**D. Record in PRD.md**

If the bug fix is NOT already documented in PRD.md:
1. Open `<app_folder>/context/PRD.md`
2. Find the specific module section
3. Look for a `### Bug` section (positioned AFTER the `### Reference` section)
4. If the `### Bug` section does NOT exist, create one after `### Reference`
5. Add the version tag on the line immediately after the `### Bug` header, using the bug's
   version from BUG.md (e.g., `[v1.0.3]`). This follows the same format as all other sections
   in PRD.md (User Story, Non Functional Requirement, Constraint, Reference) where the
   version tag `[vX.Y.Z]` appears on its own line directly after the `###` header.
6. Add a new bullet point with the bug tag and fix description after the version tag:
   ```markdown
   ### Bug
   [v1.0.3]
   - [BUG-001] Fixed table formatting inconsistency between document management and location information screens
   ```
7. If the `### Bug` section already exists:
   - Check if the bug's version tag already appears in the section
   - If the version tag already exists, append the new bug fix bullet point under that version
   - If the version tag does NOT exist, add the new version tag and bullet point after the
     last existing entry (following the same multi-version pattern used in other sections):
     ```markdown
     ### Bug
     [v1.0.3]
     - [BUG-001] Fixed table formatting inconsistency
     [v1.0.4]
     - [BUG-003] Fixed another issue
     ```

#### Step 2.8: Record Summary in BUG_MASTER.md

1. Update the bug's `Remark` column with a brief summary of what was fixed
2. Include chain effects (what other artifacts were updated)
3. Update the Summary table counts
4. Move to the next bug with status `NEW`

### Phase 3: Completion

After all bugs have been processed (every bug has a terminal status):

1. Update BUG_MASTER.md:
   - Set top-level `**Status**:` to `COMPLETED`
   - Update all Summary table counts
2. **Regenerate the traceability matrix** so the new `[BUG-XXX]` source markers (Step 2.5) and any
   code changes are reflected in the requirement-to-code links:
   ```
   Skill(skill: "co2-skills:tracegen-matrix", args: "<app_folder> version:<highest-version-processed>")
   ```
   - If a `module` filter was active for this run, pass it through: append ` module:<module>`.
   - It updates `<app_folder>/context/TRACEABILITY.md` and appends its own `CHANGELOG.md` row.
   - This does **not** require the codebase-memory MCP — `tracegen-matrix` resolves links from the
     in-source traceability / `[BUG-XXX]` comments, with a name-based source-scan fallback.
3. Append entries to `CHANGELOG.md` in the application folder (`<app_folder>/CHANGELOG.md`) â€” **one entry per version processed**:
   - Read `<app_folder>/CHANGELOG.md`. If it does not exist, create it with context header.
   - For EACH version in the resolved version list (ascending order):
     - Search for a `## {version}` heading matching this version.
     - If the section **exists**: append a new row to its table.
     - If the section **does not exist**: insert a new section after the `---` below the context header and before any existing `## vX.Y.Z` section (newest-first ordering), with a new table header and the first row.
     - Row format: `| {YYYY-MM-DD} | {application_name} | conductor-defect | {module or "All"} | Fixed {count} bugs ({list of BUG codes for this version}) |`
   - **Never modify or delete existing rows.**
4. Output the Ralph Loop completion promise: `<promise>ALL BUGS RESOLVED</promise>`

## Critical Rules

1. **CLAUDE.md is the source of truth for all tool commands** â€” CLAUDE.md is automatically
   loaded into context. Use the exact JDK path, Maven path, database credentials,
   and all other infrastructure details from CLAUDE.md. NEVER hardcode or guess paths.

2. **One bug at a time** â€” Fix bugs sequentially. Complete all steps for one bug before moving
   to the next. Never work on multiple bugs simultaneously.

3. **BUG_MASTER.md is the master checkpoint** â€” Ralph Loop uses BUG_MASTER.md to determine
   which bugs have been fixed and which are pending. Always keep it up to date. For detailed
   status of each bug, refer to the BUG_FIX_PLAN.md in each bug's folder.

4. **Never skip reproduction** â€” Always attempt to reproduce the bug with Playwright first.
   If it can't be reproduced, mark it as `CANNOT_REPRODUCE` and move on.

5. **HIGH_IMPACT defers, not blocks** â€” If a fix would break other features, mark it as
   `HIGH_IMPACT` and move to the next bug. Do not attempt risky fixes.

6. **Track everything** â€” Every action should be logged in BUG_FIX_PLAN.md so that any
   future session (or Ralph Loop iteration) can understand what was done and what remains.

7. **Preserve existing tags** â€” Never modify or remove existing `[BUG-XXX]` tags in BUG.md.
   Only add new tags to untagged bugs.

8. **Update artifacts faithfully** â€” When a fix changes UI, logic, or models, update the
   corresponding mockups, specifications, and module models. Keep all artifacts in sync.

9. **Context window awareness** â€” If approaching context limits, save progress to
   BUG_MASTER.md and BUG_FIX_PLAN.md. Ralph Loop will resume from where you left off.

10. **Ralph Loop discipline â€” NEVER stop prematurely** â€” After fixing one bug, IMMEDIATELY
    check for the next `NEW` bug and start it. Do NOT stop "to let the user review". The only
    valid reasons to stop within an iteration are: (a) context window approaching limit,
    (b) all bugs resolved (output promise), or (c) an unrecoverable error requiring user input.

11. **Auto-start Ralph Loop (INTERNAL)** â€” The FIRST action MUST be to silently check if Ralph
    Loop is active (`.claude/ralph-loop.local.md` exists). If not, silently invoke it using the
    Skill tool. The user should NEVER be asked to start Ralph Loop manually â€” this is an internal
    implementation detail handled entirely by the skill. Do NOT mention Ralph Loop to the user.

12. **NO creative alternatives for 3rd party applications (CRITICAL)** â€” Use the EXACT methods,
    connection strings, CLIs, and credentials described in `CLAUDE.md`. NEVER use Docker
    containers, alternative databases, or different CLIs than what CLAUDE.md specifies.

13. **Screenshots MUST be saved in the bug folder (CRITICAL)** â€” All Playwright screenshots
    (reproduction, verification, fixed) MUST be saved to
    `<app_folder>/context/bug/<module-slug>/<BUG-XXX>/` using explicit `page.screenshot({ path: ... })`
    calls. NEVER save screenshots in the application source folder, Playwright's default test-results
    directory, or any other location. The Playwright script files themselves should also be saved in
    the bug folder, not in the source tree.

14. **Spring Boot `app:` namespace for new configuration (CRITICAL)** â€” When a bug fix
    introduces a new configuration value in a Spring Boot application, that value MUST be
    added under the top-level `app:` key in `application.yml`. NEVER place new
    application-specific keys at the YAML root (e.g., top-level `notification:`,
    `batch-job:`, `audit-trail:`) and NEVER place them under Spring framework namespaces
    (`spring.*`, `server.*`, `management.*`, `logging.*`, `springdoc.*`).

    **Grouping:**
    - Cross-cutting values (version, CORS, shared security, shared messaging, shared
      object-storage) sit directly under `app.*` with no module prefix.
    - Per-module values MUST be grouped under `app.<module-kebab-case>.*`, one block
      per module. If the module does not yet have an `app.<module>` block, create one.

    **Binding:** bind every new `app.*` value via a `@ConfigurationProperties` record in
    the owning module's `config` subpackage. If a record already exists for that module,
    extend it rather than creating a second one. NEVER introduce `@Value("${app....}")`
    injections as a shortcut. Use kebab-case in YAML.

    **If the bug fix touches code that currently reads configuration from a root-level
    YAML key or a framework namespace, relocate the config under `app:` as part of the
    fix** â€” do not leave the violation in place. Update the `application.yml`, the Java
    `@ConfigurationProperties` prefix, any `@Value` references, and any tests that use
    `@TestPropertySource` or `@SpringBootTest(properties = ...)`. See SPECIFICATION.md
    section "Application-Specific Configuration (`app:` namespace)" for the rules.

15. **Code-level bug traceability is MANDATORY** â€” Every method, block, or template region
    modified by a bug fix MUST carry a `[BUG-XXX]` marker comment using the language's
    native comment style (Javadoc / PHPDoc / JSDoc / `{{-- --}}` / `@* *@` / `<!-- -->` /
    `#`). When a modified file already carries a top-of-file traceability comment from
    `conductor-feature-develop`, append the `[BUG-XXX]` code to its `Bug fixes:` line
    (creating the line if it does not yet exist). See Step 2.5 for the exact comment
    formats per language.

    **Why**: `git blame` and IDE search must surface the originating bug for any fix line
    directly, without consulting BUG_FIX_PLAN.md (which is a transient tracking file).
    PRD.md's `### Bug` section captures **what** was fixed; the in-source `[BUG-XXX]`
    marker captures **where** â€” both are required for end-to-end traceability.
