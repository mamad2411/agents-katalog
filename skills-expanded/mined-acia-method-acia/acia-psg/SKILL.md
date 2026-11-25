---
name: acia-psg
description: Generates a Project Structure Guide by autonomously exploring and understanding the workspace. Triggered by requests such as "Create a Project Structure Guide," "Generate a Context Index," "Create a PSG," "Update the PSG," "Generate a PSG," "Organize the folder structure," or "Analyze the workspace structure." Not used for README generation, skill definition creation, or general document creation.
license: MIT
metadata:
  version: "1.0.0"
---

# Project Structure Guide Generation Skill

## Overview

Explores the workspace and generates a Project Structure Guide (PSG) that enables AI to understand the project's asset layout (what is where) and inter-asset dependencies. A PSG is a structural map; it does not include operational procedures such as build steps, deployment steps, or execution commands.

## Absolute Rules

CRITICAL — The following are the highest-priority rules across this entire skill:

1. **Strict output format**: PSG output to files must follow the "Output Specification" section of this file
2. **Prohibited content in output file**: Validation results, auto-correction logs, checklist OK/NG statuses, correction loop progress, additional suggestions, and remark messages (such as "next suggestion" or "if you'd like") must NOT be included in the output file. These are only to be reported in the final chat response
3. **Confirmation gate compliance**: No file creation or updates may occur until the user has responded with the output destination
4. **Continuous execution flow**: After user confirmation in Step 4, work autonomously through Step 5 verification and final report. Do not output intermediate reports to the chat

## Output Specification

### Output Template

```markdown
<!-- PSG:START -->

## Project Structure Guide (PSG)

### Overview

{short description}

### Context Index

{table}

### Navigation Guide

{bullet points}

<!-- PSG:END -->
```

| Section | Required | Description |
|---------|:--------:|-------------|
| Overview | Recommended | A short sentence capturing the nature of the project |
| Context Index | Required | Category-based folder path table |
| Navigation Guide | Recommended | Supplementary information to assist Context Index exploration |

### Notation Rules (Common to All Sections)

IMPORTANT: The following apply to all descriptions in Overview, Context Index, and Navigation Guide.

#### Placeholder Rules

Generalize attribute information of the same type that exists in parallel at the same hierarchy level (path elements where multiple instances exist under the same naming convention) using `{name}` format. Single fixed paths must NOT be placeholder-ized.

**Prohibited format**: `{name1,name2}` format and `{name1|name2}` format (formats containing commas or pipes within braces) must NOT be used. Only single-token `{name}` format is valid.

#### Prohibited Notation

| Prohibited Notation | Example | Alternative |
|---------------------|---------|-------------|
| Wildcards | `sqlMap-*.xml` | `sqlMap-{id}.xml` (use placeholder) |
| Ellipsis | `...` | List all items |
| Pseudo-names | `xxx` | `{name}` format placeholder or concrete name |
| Example notation | `(e.g.: pathname)` | State the concrete path directly |
| Abbreviated enumeration | `etc.`, `and so on` | Enumerate all items |
| Table structure breaking | `{a\|b}`, `pathA\|pathB` | `{name}` format placeholder. Split multiple values into rows or use a single token |

### Overview Specification

- A short sentence (1-2 sentences) that captures the nature of the project
- Only list major technology stacks. Do not be verbose
- Summarize from metadata if available; otherwise infer from structure

### Context Index Specification

**Table format** (fixed 3 columns):

| Category | Folder Path | Role |
|----------|-------------|------|
| {classification name} | {folder path} | {role within the project} |

#### Folder Path Constraints

| Constraint | Description |
|------------|-------------|
| Trailing slash required | Folder paths must always end with `/` (including when ending with a placeholder) |
| Ellipsis prohibited | `...` must NOT be used. Use placeholders (`{package}` and similar formats) for consolidation only |
| One path per row | The same path must not be assigned to multiple rows |
| Path column purity | Only path strings. Do not include parenthetical annotations, separators (`,`, `/`, `<br>`) for listing multiple paths, or descriptive text |
| Parallel variant consolidation | Parallel variants with the same structure must be consolidated into one row using placeholders |
| Source root priority | When actual source roots exist, do not include corresponding compiled output folders |

#### Category Constraints

| Constraint | Description |
|------------|-------------|
| Content-based | AI determines classification names based on folder contents (folder-level judgment is sufficient; detailed per-file analysis is unnecessary) |
| One row per category | No duplicate category rows may exist. If roles differ, use different categories |
| Module boundary preservation | Information belonging to different modules must not be consolidated into the same category. Prefix category names with the module name |
| No subsections | `####` must NOT be used within Context Index. Always use a single flat table |

#### Aggregation and Granularity Criteria

IMPORTANT: Criteria for determining category granularity. AI judges based on subfolder lists and file counts as input data.

**Principle**: Subfolders are consolidated into the parent category's role description. They become independent categories only when the following conditions are met:

| Classification | Condition | Action |
|---------------|-----------|--------|
| Core layer | Folders handling the project's primary separation of concerns (layers such as input handling, business logic, data access, data definition) | Independent category regardless of count |
| Support layer | Folders supporting core layers (elements such as exception handling, configuration, utilities) | Independent category when **4 or more** items exist. Below that, consolidate into parent with mention in role description |
| Other | Subfolders not matching either of the above | Consolidate into parent category |

#### Role Constraints

| Constraint | Description |
|------------|-------------|
| Summary-level description | Describe the role that assets within the folder path serve in the project at a summary level |
| Exploration-based content | Describe based on contents actually confirmed during exploration |
| No path structure description | Do not append subdirectory naming patterns or parallel structures in parentheses to the role column. Express parallel structures using `{name}` placeholders in the folder path column |

#### Exclusion Constraints

| Constraint | Description |
|------------|-------------|
| Exclusion targets | Build artifacts, dependency modules, and caches are generally not included in the Context Index |
| AI skill definition exclusion | AI skill definitions such as `.github/skills/`, `.agent/skills/`, `.cursor/skills/` are always excluded from the Context Index (only exclusion notes in Navigation Guide are permitted) |
| Exclusion notes | Build artifact locations and AI skill definition locations are noted in the Navigation Guide |

### Navigation Guide Specification

Describe information that assists Context Index exploration in **bullet point** format. If there is no useful information, the section itself may be omitted.

**Content to describe**:

- Dependencies between categories
- Module composition information (for multi-module projects)
- Intra-category navigation assistance (identification methods when different file types coexist at the same path)
- Naming conventions and ID patterns
- Exclusion folder notes (build artifact locations, AI skill definition locations)

#### Attribution Rules for Context Index and Navigation Guide

| Nature of information | Belongs to | Test |
|-----------------------|-----------|------|
| **What is where** — folder existence, layout, role | Context Index | Is this information a structural description of folder layout? |
| **How they connect** — dependencies between categories, correspondence through naming conventions | Navigation Guide | Is this exploration assistance between already-placed categories? |
| **How to operate** — build steps, deployment steps, execution commands, setup steps | Outside PSG scope | Is this an operational procedure rather than asset layout? |

When the Navigation Guide requires folder layout explanations, it is a sign of insufficient splitting in the Context Index.

**Constraints**:

- **Consistency with Context Index**: Reference category names and folder paths accurately
- **Separation from Overview**: Information about the project's nature or technology stack belongs in the Overview
- **Exclusion of operational procedures**: Build commands, deployment steps, DB initialization steps, and setup steps are not included in the PSG. Command examples and code blocks are also not to be included

## Execution Steps

### Step 1: Understand the Workspace

1. Use `list_dir` to confirm the root structure
2. Check the following metadata files in priority order to understand the project's purpose:
   - `README.md` / `README.txt`
   - `AGENT.md` / `.github/copilot-instructions.md`
   - Project definition files (build definitions such as `package.json`, `pom.xml`) description fields
3. Retain the project's purpose, major technology stack, and module composition (single/multi) as working notes

**Completion criteria**: Root structure and project purpose are understood.

### Step 2: Folder Exploration

1. **Exclusion judgment**: Exclude build artifacts, dependency modules, caches, IDE settings, and VCS folders
   - Judge based on AI's general knowledge. When in doubt, refer to [exclusion-patterns.md](./references/exclusion-patterns.md)
   - AI skill definitions (`.github/skills/`, `.agent/skills/`, `.cursor/skills/`) are also excluded from the Context Index
2. **Exploration**: Recursively explore analysis target folders to the necessary depth using `list_dir`
   - Stop when reaching architecture layer folders (folders representing design roles)
   - Stop when there are no more subfolders
   - Maximum 10 levels deep
   - **Symmetry principle**: All child folders of the same parent folder must be explored to the same depth. Do not explore specific folders deeper/shallower than others
3. **For large workspaces**: If there are many modules, confirm the analysis scope with the user

**Completion criteria**: All target folder structures are understood, with subfolder lists and file counts recorded for each folder.

### Step 3: Category Classification

1. Classify each folder into categories
   - **Judgment approach**: Folder name -> file extensions -> check file headers if necessary -> infer from parent folder, in that order
   - Judge based on AI's general knowledge. No special rule references needed
   - Group folders with the same role into the same category
2. **Aggregation/granularity judgment**: Follow the aggregation and granularity criteria in the output specification to determine whether each subfolder should be independent or consolidated
3. **Traversal of organization namespace hierarchies**: Traverse through package hierarchies that start with organization domains (reverse-domain packages such as `jp/`, `com/`, `org/`) and set the category path at the architecture layer folder
4. If there are folders that cannot be classified, confirm with the user

**Completion criteria**: All target folders have been assigned a category.

### Step 4: Guide Generation

1. **Overview**: Generate a short description from Step 1 information
2. **Context Index**: Output Step 3 classification results as a table with "Category / Folder Path / Role"
3. **Navigation Guide**: Output category relationships, composition supplements, and essential information as bullet points from exploration results
4. **User confirmation**: Confirm the output destination with the user
5. **Use question tool**: Use the `ask_questions` tool (or `AskUserQuestion` in Claude Code) to present output destination candidates (candidates: `.github/copilot-instructions.md`, `AGENT.md`, `CLAUDE.md`, Other) to the user for selection (if the tool is unavailable, ask directly)

**Confirmation gate** (Absolute Rule #3):
- No file creation or updates may occur until the user has responded with the output destination
- When unconfirmed, return only the "output destination confirmation question" and suspend the generation process
- Do not automatically save to a default output destination

**Completion criteria**: The complete Project Structure Guide including all sections with `<!-- PSG:START -->` to `<!-- PSG:END -->` markers has been generated at the user-confirmed output destination.

### Step 5: Verification

Check the following in priority order and auto-correct any issues. Verify all MUST items and confirm they pass before proceeding to SHOULD items.

#### MUST — Structure & Content

| ID | Check | Expected |
|----|-------|----------|
| S1 | PSG heading structure has 1 `##` (Project Structure Guide) + 1-3 `###` (Context Index is required; Overview and Navigation Guide are recommended) | Compliant |
| S2 | Context Index is a 3-column table format (Category, Folder Path, Role) — bullet lists and 4+ columns are non-compliant | Compliant |
| S3 | PSG text starts with `<!-- PSG:START -->` and ends with `<!-- PSG:END -->` | Compliant |
| S4 | Residual `etc.`, `and so on`, `...`, `(e.g.:`, `xxx` | 0 found |
| S5 | `####` (subsections) within Context Index | 0 found |
| S6 | `|` characters in cell content not used as column delimiters | 0 found |
| S7 | All folder paths end with trailing `/` | Compliant |

#### SHOULD — Quality

| ID | Check | Expected |
|----|-------|----------|
| Q1 | `*` (wildcards) in path strings | 0 found |
| Q2 | No concrete names of parallel instances that should be placeholder-ized remain | 0 found |
| Q3 | `{xxx,yyy}` format or `{xxx|yyy}` format (invalid placeholders) | 0 found |
| Q4 | No multiple paths listed in a single Context Index path column cell | 0 found |
| Q5 | The terminal folder name of every Context Index folder path is an architecture layer name (a name representing a design role) | Compliant |
| Q6 | No folder structure explanations have leaked into Navigation Guide (folder layout descriptions belong to Context Index) | Compliant |
| Q7 | Aggregation/granularity criteria have been properly applied for splitting/consolidation | Compliant |

**Auto-correction**: AI automatically performs: trailing `/` completion on paths, duplicate row removal, exclusion omission correction, placeholder-ization of concrete instances, rewriting of prohibited terms, and replacement of `|` within table cells with `{name}` placeholders or row splitting.
**Correction loop**: If issues remain, correct and re-verify (up to 3 times). If unresolvable, report to the user.

**Verification result output** (Absolute Rules #2 and #4):
- The final chat response must include a concise pass/fail (OK/NG) for each verification item
- If auto-corrections were performed, include correction details and re-verification results
- Verification results and auto-correction information must NOT be written into the output file body
- If verification results are not reported, the task is considered incomplete

## Updating an Existing Guide

1. Identify the range from `<!-- PSG:START -->` to `<!-- PSG:END -->`
2. Identify newly added, deleted, or moved folders
3. Update only the differences (preserve existing classifications)
4. Confirm with the Step 5 verification checklist

## Output Examples

For complete output examples, see [output-examples.md](./references/output-examples.md).

## Performance Notes

IMPORTANT: Quality takes priority over speed.

- The verification step (Step 5) must NOT be skipped
- Confirm each Step's completion criteria before proceeding to the next Step
- When uncertain, confirm with the user before proceeding
