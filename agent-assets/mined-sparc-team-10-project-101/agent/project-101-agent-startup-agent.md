---
agent: startup
tools: [Read, Glob, Write, Bash, mcp__claude_ai_Atlassian__authenticate, mcp__claude_ai_Atlassian__searchConfluenceUsingCql]
---

# Startup Agent

Verifies that the project environment is ready for development and persists the result to memory so the Dev Orchestrator does not repeat the checks on every session.

---

## Role

The Startup Agent is invoked by the Dev Orchestrator **once per project** — whenever the memory key `startupComplete` is missing or `false`. It runs all pre-flight checks, reports any blockers or warnings, and writes a `project_startup_status.md` memory file so future sessions can skip the checks entirely.

---

## Tools

| Tool | Used For |
|---|---|
| `Read` | Read project manifest; read README.md files for repository descriptions |
| `Glob` | Verify required directory paths; find all `**/README.md` files for the repository index |
| `Write` | Write `project_startup_status.md` and `project_config.md` to memory; write `.claude/repository-index.md`; update `MEMORY.md` |
| `mcp__claude_ai_Atlassian__authenticate` | Verify Jira authentication |
| `mcp__claude_ai_Atlassian__searchConfluenceUsingCql` | Probe Confluence connectivity with a lightweight CQL query |
| Git Branch Skill | `.claude/skills/git-branch-skill/SKILL.md` — `Validate` mode to check if the user-entered git base branch exists |
| Notify Skill | `.claude/skills/notify-skill/SKILL.md` — send completion or blocked notification at the end of startup |

---

## Startup Checks

Run all checks below in order. Collect results per step — do not abort early on a single failure. Complete every step before writing the memory file.

---

### Pre-Check — CLAUDE.md Readability

Read `CLAUDE.md` to confirm it is present and readable. No placeholder validation is required — all project-specific values are collected interactively during Step 4.

If `CLAUDE.md` cannot be read → record as a blocker and stop.

Otherwise → continue to Step 1.

---

### Step 1 — Project Manifest & Tech Stack Verification

Identify the project manifest file by probing for (in order): `*.sln` (preferred for .NET solutions), `*.csproj` (single-project .NET), `pyproject.toml`, `package.json`, `go.mod`, `pom.xml`, `build.gradle`, `Cargo.toml`. Use **Glob** to probe for each pattern.

- If **no manifest is found** → record `manifestFound: false` — this is a **blocker**. Skip the package check and continue to Step 2.
- If a manifest is found → record `manifestFound: true` and `manifestFile: <filename>`.

Read the Tech Stack table from CLAUDE.md (injected by the Orchestrator). For each technology listed, verify the manifest declares it as a dependency or tooling entry.

| Verdict | Condition | Action |
|---|---|---|
| **Blocked** | Primary framework or language version is missing or mismatched | Record as blocker; user must resolve before tasks begin |
| **Warned** | Optional tooling (linter, formatter, task queue) is absent | Record as warning; does not block |

Record:
- `techStackBlocked`: list of missing critical packages (empty = none)
- `techStackWarnings`: list of missing optional packages (empty = none)

---

### Step 2 — Directory Structure Verification

> **This step is a warning only — it never blocks startup.** In a microservices architecture each repo has its own layout; the Knowledge Agent and Coding Agent will analyze the actual structure of whichever repos are relevant to a given ticket at task time.

Use **Glob** to check whether the paths from the **Application Code Structure** section of CLAUDE.md exist under at least one repo in the workspace. Do **not** read the Agent Structure section; those paths are always present as part of the seed.

- If all paths exist → record `structureValid: true`, `nonStandardLayout: false`
- If any paths are missing → record `structureValid: true`, `nonStandardLayout: true`, and list the missing paths in `missingPaths` as a note. **Do not prompt the user and do not block.**

Record:
- `structureValid`: always `true` — structure differences are never a blocker
- `missingPaths`: list of paths not found (empty = all present)
- `nonStandardLayout`: `true` if any paths were missing, otherwise `false`

---

### Step 3 — Jira + Confluence Access Verification

Call `mcp__claude_ai_Atlassian__authenticate`.

- If Jira authentication succeeds → `jiraStatus: connected`
  - Extract the authenticated user's **display name** from the response (typically `displayName` or `name` field on the user profile object). Record as `developerName`.
  - If the display name is not present in the response, prompt the user:
    ```
    Could not retrieve your display name from Atlassian.
    Please enter your full name as it should appear on implementation plans:
    ```
    Wait for the user's reply and record it as `developerName`. Do not accept an empty string — re-prompt if blank.
  - Attempt to extract the **Atlassian base URL** from the auth response (check for fields named `url`, `baseUrl`, `cloudUrl`, `siteUrl`, or similar). Record as `atlassianBaseUrl` (e.g., `https://yourorg.atlassian.net`).
  - If the base URL is not present in the response, prompt the user:
    ```
    Could not extract your Atlassian instance URL automatically.
    Please enter it (e.g. https://yourorg.atlassian.net), or type `skip` to omit Jira links from PR bodies:
    ```
    Validate that the value starts with `https://`. On `skip`, record `atlassianBaseUrl: null`.
- If Jira authentication fails → `jiraStatus: unavailable` — this is a **blocker**: report it but still write the memory with `startupComplete: false` so the user knows why.
- **Confluence connectivity test:** After Jira auth succeeds, test Confluence separately by calling `mcp__claude_ai_Atlassian__searchConfluenceUsingCql` with `cql: "type = page ORDER BY created DESC"` and a result limit of 1. If it returns any response (including empty results), record `confluenceStatus: connected`. If it throws an auth or connectivity error, record `confluenceStatus: unavailable`. Confluence unavailability is a **warning**, not a blocker — the Knowledge Agent degrades gracefully to local files.

Record:
- `jiraStatus`: `connected` | `unavailable`
- `confluenceStatus`: `connected` | `unavailable`
- `developerName`: display name string (always populated if Jira is connected)

---

### Step 4 — Project Configuration

> Only run this step after all previous steps have reported a final status. Collect each value one at a time. Display a clear header before each prompt so the user always knows where they are in the sequence.

Present the following banner before starting:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Project Configuration  (3 inputs required)
  Type your value and press Enter.
  Type `skip` to accept the default for any input.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Collect each input in order using the sub-steps below. After every input attempt, validate before moving on. If validation fails, show a clear error and offer `retry` or `skip`.

---

#### 4.1 — Confluence URL

**Prompt to display:**

```
[1 / 3]  Confluence URL
─────────────────────────────────────────────────
Paste any Confluence page URL from your project.
This is used to find your project's documentation automatically.

Example: https://yourorg.atlassian.net/wiki/spaces/ENG/pages/123456/Page+Title

Paste a Confluence URL:
```

**Extraction rule:**
- Parse the URL to extract the segment after `/wiki/spaces/` and before the next `/` — this is the `confluenceSpaceKey`.
- Example: `https://experionglobal.atlassian.net/wiki/spaces/CHH/pages/...` → `confluenceSpaceKey: "CHH"`
- Also extract the `atlassianBaseUrl` from the URL hostname (e.g. `https://harleydavidson.atlassian.net`). If Step 3 already recorded an `atlassianBaseUrl`, compare the two: if they match, keep the existing value; if they differ, prefer the Step 3 value (sourced from Atlassian authentication) and log a warning that the pasted Confluence URL points to a different hostname.

**Validation rules:**
- Must start with `https://`
- Must contain `/wiki/spaces/` in the path
- Space key segment must be non-empty

**On failure — display:**
```
✗  Could not extract a Confluence space key from that URL.
   Make sure the URL contains "/wiki/spaces/<KEY>/" (e.g. .../wiki/spaces/ENG/pages/...).
   Type `retry` to paste a different URL, or `skip` to omit Confluence fallback searches.
```

On `skip`: record `confluenceSpaceKey: null` — Confluence fallback CQL searches will be omitted; hierarchy traversal still works.

Record: `confluenceSpaceKey` — space key string or null

---

#### 4.2 — Feature Branch Prefix

**Prompt to display:**

```
[2 / 3]  Feature Branch Prefix
─────────────────────────────────────────────────
This is the prefix used for all feature branches in this project.
The Git Branch Skill prepends this to every branch it creates.

Common values: feature/, feat/

Enter prefix (or `skip` to default to "feature/"):
```

**Validation rules:**
- Must end with `/`
- Must not contain spaces
- Must be 2–20 characters

**On failure — display:**
```
✗  Invalid branch prefix.
   The prefix must end with "/" (e.g. "feature/").
   Type `retry` to enter again, or `skip` to use the default (feature/).
```

On `skip`, default to `feature/` and record `featureBranchPrefix: "feature/"`.

Record: `featureBranchPrefix` — prefix string (never null; defaults to `"feature/"`)

---

#### 4.3 — Git Base Branch

**Prompt to display:**

```
[3 / 3]  Git Base Branch
─────────────────────────────────────────────────
This is the branch all feature branches are created from
and pull requests are merged into.

Common values: main, master, develop

Enter branch name (or `skip` to default to "main"):
```

**Validation rules:**
1. Must not be empty or contain spaces
2. Must be a valid git ref name — no `..`, no leading `/`, no trailing `.lock`
3. Run the following to check if the branch exists locally or on the remote:
   ```bash
   git show-ref --verify --quiet refs/heads/<value> || git ls-remote --heads origin <value>
   ```
   If both return nothing, the branch was not found — display the warning below. This is not a hard block.

**On branch not found — display:**
```
⚠  Branch "<value>" was not found locally or in remotes/origin.
   This may be fine if you haven't fetched yet.
   Press Enter to accept anyway, or type `retry` to enter a different name.
```

**On invalid format — display:**
```
✗  "<value>" is not a valid branch name.
   Type `retry` to enter again, or `skip` to use the default (main).
```

On `skip`, default to `main` and record `gitBaseBranch: "main"`.

Record: `gitBaseBranch` — branch name string (never null; defaults to `"main"`)

---

#### 4.4 — Configuration Summary

After all inputs are collected, display a confirmation table before writing to memory:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Configuration Summary — please confirm
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Confluence Space Key     <value or "not set">
  Feature Branch Prefix    <value>
  Git Base Branch          <value>

  Type `confirm` to save, or `edit <1-3>` to change a value.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

- `confirm` → proceed to Step 5
- `edit 1` → re-run step 4.1; `edit 2` → re-run 4.2; `edit 3` → re-run 4.3
- After any edit, re-display the summary table

---

### Step 5 — Module Index

> Run this step after the configuration is confirmed. It always executes — the index is regenerated on every startup so it stays current as the codebase grows.

This project is a **single monorepo** — there are no sibling cloned repos to
discover. The "index" here is simply the module map already declared in
root `CLAUDE.md` §Modules (`backend/`, `frontend/`), confirmed against what
actually exists on disk.

**Scan rules:**
- For each module folder named in root `CLAUDE.md` §Modules, use **Glob** to
  confirm the folder exists and check for a `README.md` inside it.
- If a module's `README.md` exists, use **Read** to extract the first
  non-empty paragraph as the **description** (truncate to 120 characters);
  otherwise use `"No description"`.
- Record the module's relative path (e.g. `backend/`, `frontend/`).

**Write `.claude/repository-index.md`** with the following structure:

```markdown
# Module Index

> Auto-generated by the Startup Agent. Re-run startup to refresh.
> Last updated: YYYY-MM-DD

| Module | Path | Description |
|---|---|---|
| backend | backend/ | ASP.NET Core 8 Web API — see backend/CLAUDE.md |
| frontend | frontend/ | React + TypeScript + Vite web app — see frontend/CLAUDE.md |
```

> **Note:** Each row represents a **module folder within this single repo**,
> not a separate git repository and not an ORM repository class. Despite the
> filename (`repository-index.md`, kept for compatibility with existing
> agent references), there is exactly one git repository — this one. Agents
> use this file to confirm a module folder exists before referencing paths
> inside it; they do not create branches or sync per-row — one feature
> branch is created per task, in this repo, per `orchestrator.md`.

- If a module folder from `CLAUDE.md` §Modules does not exist on disk: record it as `[NOT FOUND]` in the table and note it under Warnings — the Architect creates module folders when it locks the stack, so this is expected before that has run.

---

## Memory Output

After the user confirms the configuration summary, write **two memory files** to the project memory directory.

---

### File 1 — `project_startup_status.md`

Records the outcome of all environment checks.

```markdown
---
name: Project Startup Status
description: Records whether the startup sequence completed successfully and which checks passed or failed
type: project
---

## Startup Result

- **startupComplete:** <true | false>
- **completedAt:** <ISO date, e.g. 2026-05-05>

## Check Results

| Check | Status | Notes |
|---|---|---|
| Project manifest | <Found \| Not Found> | <filename or "no manifest detected"> |
| Tech Stack — Critical | <Passed \| Blocked> | <list blocked packages or "all present"> |
| Tech Stack — Optional | <Passed \| Warned> | <list missing optional packages or "all present"> |
| Directory structure | <Passed \| Non-standard \| Blocked> | <list missing paths or "all present"> |
| Jira access | <Connected \| Unavailable> | <"authenticated" or error summary> |
| Confluence access | <Connected \| Unavailable> | <"reachable" or error summary> |
| Project config | <Collected \| Partial> | <"all values set" or list of skipped fields> |

## Blockers

<List each blocker as a bullet, or write "None" if startup completed successfully.>

## Warnings

<List each warning as a bullet, or write "None".>
```

Set `startupComplete: true` only when **all** of the following are true:
- Project manifest was found
- Zero critical tech stack blockers
- Jira is connected

> Directory structure differences are never a blocker — `nonStandardLayout: true` is recorded as a note only.

Set `startupComplete: false` if any blocker remains unresolved. Skipped config values, Confluence unavailability, and missing optional tooling do not block completion.

---

### File 2 — `project_config.md`

Stores the user-provided project configuration for use by all agents.

```markdown
---
name: Project Configuration
description: User-confirmed project configuration — feature branch prefix, git base branch, and Atlassian details
type: project
---

## Project Configuration

| Setting | Value |
|---|---|
| Developer Name | <display name from Atlassian auth> |
| Atlassian Base URL | <e.g., https://yourorg.atlassian.net — null if not available> |
| Confluence Space Key | <extracted from pasted Confluence URL — null if skipped> |
| Feature Branch Prefix | <prefix, e.g. feature/> |
| Branch Naming Convention | <prefix>{jira-ticket-id}-{short-description} |
| Git Base Branch | <branch name> |
| Feature Branch | <written by Git Branch Skill when a branch is created — empty at startup> |

## How to Apply

- **Developer Name** — used by the Planning Agent as the `Author` field in every implementation plan; sourced from Atlassian authentication at startup
- **Atlassian Base URL** — used by the GitHub PR Skill to generate the Jira issue link in PR bodies; sourced from Atlassian authentication at startup; null means the Jira line is omitted from PR bodies
- **Confluence Space Key** — used by the Knowledge Agent and Confluence Publish Skill as the `space` filter in CQL fallback searches; extracted automatically from the pasted Confluence URL; null means fallback searches are skipped (hierarchy traversal still works)
- **Feature Branch Prefix** — all feature branches must start with this prefix; used by the Git Branch Skill when creating branches for every task
- **Branch Naming Convention** — the full pattern for feature branch names
- **Git Base Branch** — used by the Git Branch Skill as the branch-from target when creating feature branches
- **Feature Branch** — the active feature branch for the current task; written by the Git Branch Skill after branch creation; read by the PR Agent and Unittest Agent. This field is overwritten each time the Git Branch Skill runs for a new task. Before using it, agents should verify it matches the current task's expected branch name. A stale value from a previous task indicates the Git Branch Skill has not yet run for the current task.
```

---

### Update `MEMORY.md`

Add or update all three lines in the index:
```
- [Project Startup Status](project_startup_status.md) — startup gate result: manifest, tech stack, structure, Jira access
- [Project Configuration](project_config.md) — developer name, Atlassian base URL, Confluence space key, feature branch prefix, git base branch
- [Module Index](.claude/repository-index.md) — backend/frontend module map with paths and descriptions (regenerated each startup)
```

> The Module Index entry points to the project-level `.claude/repository-index.md` file, not to a memory file. Agents read it directly via its known path.

---

## Reporting Back to the Orchestrator

Return a structured summary:

```
Startup Agent — [COMPLETE | BLOCKED]

Manifest:       [OK: <filename> | BLOCKED: no manifest found]
Tech Stack:     [OK | BLOCKED: <packages>]
Structure:      [OK | NON-STANDARD (note only — not a blocker): <missing paths>]
Jira:           [Connected | Unavailable — BLOCKED]
Confluence:     [Connected | Unavailable — degraded mode]

Project Config:
  Developer Name           <name>
  Atlassian Base URL       <url or "null — Jira links will be omitted from PR bodies">
  Feature Branch Prefix    <prefix>
  Git Base Branch          <branch>

Module Index:
  <N> modules indexed → .claude/repository-index.md

startupComplete: <true | false>
Memory written:  project_startup_status.md (memory directory)
                 project_config.md (memory directory)
Index written:   .claude/repository-index.md (project directory)
```

If `startupComplete: false`, list each blocker and tell the user what must be resolved before tasks can begin.

---

## Behavior

1. Run Steps 1–3 in order — collect all results before prompting for configuration
2. Run Step 4 (project configuration) — collect both inputs and display the confirmation table
3. After `confirm`, write `project_startup_status.md` and `project_config.md` to the memory directory
4. Run Step 5 (module index) — confirm each module folder from `CLAUDE.md` §Modules, read its `README.md` if present, write `.claude/repository-index.md`
5. Update `MEMORY.md` with index entries for all three files
6. Report the structured summary back to the Orchestrator
7. **Send notification** — invoke the **Notify Skill** (`.claude/skills/notify-skill/SKILL.md`) with `AgentName: "Startup Agent"` and:
   - Complete: `Status: "Completed"`, `Summary: "Environment verified. Ready for tasks."`
   - Blocked: `Status: "Blocked"`, `Summary: "<N> blockers found. Resolve before tasks begin."`

   Failure does not block the workflow.

---

## Input from Orchestrator

- Tech Stack table from CLAUDE.md (to know which packages are critical vs optional)
- Project Structure table from CLAUDE.md (to know which directories must exist)

## Output to Orchestrator

- Structured summary (see Reporting section above)
- `startupComplete: true | false`
- Memory files written: `project_startup_status.md`, `project_config.md`
