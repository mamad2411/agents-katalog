---
name: util-usanalyzer
model: claude-sonnet-4-6
effort: medium
description: >
  Analyze PRD.md files for quality issues: incomplete sentences, non-existent references,
  cross-module inconsistencies, contradictory requirements, duplicate roles, design system
  validation, architecture principle violations, and process flow coverage gaps. Validates
  bi-directional coverage between User Stories/NFRs and High Level Process Flows — detects
  modules not covered by any process flow and process flow steps not covered by any User
  Story or NFR. Adds inline [TODO] annotations directly into the PRD.md file for each
  issue found.
  Trigger on keywords: "analyze user story", "analyze user stories", "check user story quality",
  "validate user stories", "find user story issues", "audit user stories", "review user stories",
  "check requirements quality", "find inconsistencies", "find contradictions".
  Accepts an application name as input (e.g., `/util-usanalyzer mainapp`,
  `/util-usanalyzer "Main App"`).
---

# Util US Analyzer

Analyze PRD.md files for quality issues and add `[TODO]` annotations for each issue found.

## Input Resolution

This skill requires one mandatory argument: `<application>`.

| Argument | Required | Description |
|----------|----------|-------------|
| `<application>` | Yes | Application name — matched against root-level application folders |
| `<module>` | No | Optional module name to limit analysis to a single module |

### Application Folder Resolution

1. List root-level application folders that may have a numeric prefix (e.g., `1_hub_middleware`, `2_hc_adapter`) or no prefix (e.g., `mainapp`)
2. Strip the leading `<number>_` prefix from each folder name if present (e.g., `1_hub_middleware` -> `hub_middleware`)
3. Match the provided application name **case-insensitively** against the stripped folder names
4. Accept `snake_case`, `kebab-case`, or title-case input (e.g., `hub_middleware`, `hub-middleware`, `Hub Middleware` all match `1_hub_middleware`)
5. If no match is found, list all available application names and **stop**

### Auto-Resolved Paths

| File | Resolved Path |
|------|---------------|
| PRD.md | `<app_folder>/context/PRD.md` |

Example invocations:
- `/util-usanalyzer mainapp`
- `/util-usanalyzer "Main App"`
- `/util-usanalyzer mainapp module:Home`

## Workflow

### 1. Read and Parse PRD.md

Read the entire PRD.md file and parse its structure:
- Identify all module sections (delimited by `## <Module Name>` headers under `# System Module` or `# Business Module`)
- Within each module, identify subsections: `### User Story`, `### Non Functional Requirement`, `### Constraint`, `### Reference`, `### Test`, `### Bug`
- Record line numbers for every item for precise TODO annotations
- Parse the following top-level extended sections if they exist:
  - `# Design System` — extract referenced file paths and any inline declarations
  - `# Architecture Principle` — extract all declared architectural patterns and principles
  - `# High Level Process Flow` — extract all process flow entries (inline or external file references). For external references (e.g., `- Flow Name: Refer to [file.md](path/to/file.md) for the high level process flow`):
    - Extract the flow name (text before the colon)
    - Extract the referenced file path from the markdown link
    - Resolve the path relative to PRD.md's location
    - Read the external file and parse its `# Process/System Flow` section (ordered steps) and `# Statuses` section (per-application status tables)
    - If the external file does not exist, flag the reference line as `BAD_REF` and skip further analysis of that flow

### 2. Collect All Roles

Scan the entire document and collect every role mentioned in user stories (the part after "As a" / "As" and before the comma or "I want"). Build a normalized role registry mapping each unique role to its canonical form and the line numbers where it appears.

### 3. Collect All Cross-References

Scan the entire document for:
- References to other modules (e.g., mentions of `Batch Job`, `Audit Trail`, `Headcount`, etc.)
- References to external documents or sections (e.g., `[PROJECT.md](../PROJECT.md)`)
- References to pages, sections, or features by name within user stories, NFRs, constraints

Build a registry of all outbound references per module.

### 4. Run Analysis Checks

**Skip empty modules entirely.** If a module has no content in any of its subsections (User Story, Non Functional Requirement, Constraint, Reference are all empty — no bullet items), skip that module completely. Do not flag empty sections or run any checks on empty modules.

Execute the following checks in order. For each issue found, record the line number, issue category, and a description.

#### 4.1 Incomplete User Stories

Check every top-level bullet under `### User Story` sections:
- Must follow the Agile format: **"As a [role], I want [feature] so that [benefit]"** or **"As [role], I want [feature] so that [benefit]"**
- Flag items missing "I want" clause
- Flag items missing "so that" clause (benefit/justification)
- Flag items that appear to be truncated or end abruptly (e.g., ending with a colon but no sub-bullets, or trailing whitespace with no content)
**Exception:** User stories that end with a colon (`:`) followed by sub-bullets describing the detail are acceptable — they provide the "what" through their sub-items. Only flag these if the sub-bullets are missing.

#### 4.2 Non-Existent References

For each reference found in step 3:
- If it references an external file (e.g., `[PROJECT.md](../PROJECT.md)`), verify the file exists at the resolved path relative to the PRD.md location
- If it references a module by name (e.g., backtick-quoted `Batch Job`), verify that module exists as a `## <Module>` section in the document
- If it references a page or feature (e.g., "redirect to the Headcount list page"), verify that the referenced module exists

#### 4.3 Cross-Module Inconsistencies

For each module, check:
- If a user story, NFR, or constraint mentions a feature/entity from another module (e.g., "Headcount Fulfillment Status"), verify that feature is actually defined in the referenced module
- If a user story mentions navigating to another module's page (e.g., "redirect to the Sub Project details page"), verify that view/page is described in the target module's user stories
- If an NFR or constraint references a concept from another module (e.g., "using `Batch Job`"), verify the referenced module defines that concept

#### 4.4 Contradictory Requirements

Compare requirements within the same module and across modules:
- Look for NFRs or constraints that directly contradict each other (e.g., one says "will be automatically deleted" while another says "will not be automatically deleted")
- Look for user stories that grant permissions contradicted by constraints (e.g., a user story allows editing but a constraint says the data is read-only)
- Look for status values or enums defined differently in different places (e.g., status list in user story differs from status list in constraint)
- Look for contradictions between NFR and Constraint sections within the same module (e.g., Sub Project NFR says it has status values but Constraint says it will not have status)

#### 4.5 Duplicate Roles

Using the role registry from step 2:
- Identify roles that are semantically similar but named differently (e.g., "Project Manager" vs "PM", "user" vs "User", "staff" vs "Staff")
- Check the `## Role` module's constraint section for the canonical role list
- Flag any role used in user stories that doesn't match the canonical list
- Flag inconsistent capitalization of the same role (e.g., "a user" vs "a User")

#### 4.6 Design System Reference Validation

If a `# Design System` section exists in PRD.md:
- Extract the referenced file path (e.g., from `[DESIGN_SYSTEM.md](reference/DESIGN_SYSTEM.md)`)
- Resolve the path relative to PRD.md's location
- Verify the referenced file actually exists at the resolved path
- If the file does not exist, flag as `BAD_REF`
- If the design system file exists, read it and extract declared UI component patterns, layout conventions, and interaction patterns. Then:
  - Cross-reference User Stories that describe UI behavior (e.g., "view dashboard", "search for", "view details") with the design system's declared patterns
  - If a User Story describes a UI interaction or component that directly contradicts a design system declaration (e.g., user story says "popup modal" but design system prohibits modals in favor of inline expansion), flag as `CONTRADICTION`
  - Only flag clear contradictions — do not flag User Stories that simply omit UI detail, as implementation choices belong in the specification phase

#### 4.7 Architecture Principle Consistency

If an `# Architecture Principle` section exists in PRD.md:
- Extract declared architectural patterns (e.g., "stateless", "event-driven", "document based database", "message driven", "monolithic", "container based", "file storage using GridFS")
- Cross-reference with User Stories, NFRs, and Constraints across all modules:
  - If architecture declares "stateless" but a User Story or NFR implies server-side session storage, flag as `ARCH_VIOLATION`
  - If architecture declares "document based database" but a User Story, NFR or constraint references SQL joins, foreign key enforcement, or relational schema concepts, flag as `ARCH_VIOLATION`
  - If architecture declares "event-driven" inter-module communication but a User Story or NFR describes synchronous direct calls between modules, flag as `ARCH_VIOLATION`
  - If architecture declares "message driven" processing but a User Story, NFR or constraint implies synchronous external API polling for message processing, flag as `ARCH_VIOLATION`
  - If architecture declares a specific file storage mechanism (e.g., "GridFS in MongoDB") but an NFR or constraint describes a different file storage approach (e.g., local filesystem, S3), flag as `ARCH_VIOLATION`
  - If architecture declares "monolithic" design but a User Story or NFR describes deploying separate microservices, flag as `ARCH_VIOLATION`
  - If architecture declares a specific framework/technology (e.g., "Spring Boot", "JTE template engine") but an NFR or constraint references an incompatible technology, flag as `ARCH_VIOLATION`
- Also check Test sections: if test instructions reference infrastructure or tooling that contradicts architecture principles (e.g., test setup assumes a relational DB when architecture declares document-based), flag as `ARCH_VIOLATION`
- Only flag clear, unambiguous contradictions — patterns that directly oppose the stated architectural principle

#### 4.8 Process Flow Coverage and Consistency

If a `# High Level Process Flow` section exists in PRD.md:

##### 4.8.1 Parse and Resolve Process Flows

- Each process flow entry in the `# High Level Process Flow` section may be:
  - **Inline**: A named subsection (e.g., `## Recruitment Agent Sync`) with ordered steps as bullet items directly in PRD.md
  - **External reference**: A bullet item referencing an external file (e.g., `- Recruitment Agent Sync: Refer to [ra_sync.md](path/ra_sync.md) for the high level process flow`)
- For external references:
  - Extract the flow name (text before the colon)
  - Extract the referenced file path from the markdown link
  - Resolve the path relative to PRD.md's location
  - Read the external file and parse its `# Process/System Flow` section (ordered numbered steps) and `# Statuses` section (per-application status tables)
  - If the file does not exist, flag as `BAD_REF` and skip further analysis of that flow
- For each successfully parsed flow, build a flow registry containing:
  - Flow name (e.g., "Recruitment Agent Sync", "Job Demand", "Candidate Registration")
  - All numbered steps with their descriptions
  - Application-relevant steps (steps that mention the current application name — inferred from the root folder name, e.g., "Hub Middleware")
  - Application-specific statuses from the status table (if defined)

##### 4.8.2 Flow → Module Coverage (Forward Check)

For each process flow that has application-relevant steps:
- **Module existence**: Match the flow name to a module under `# System Module` or `# Business Module`. If no module with a matching name exists, flag the flow entry line in the `# High Level Process Flow` section as `FLOW_COVERAGE` with description: "Process flow '<flow name>' has steps for this application but no corresponding module exists in PRD"
- **Step-to-NFR coverage**: For each application-relevant step in the flow, verify the corresponding module has an NFR that describes the behavior:
  - **Message consumption**: If a step describes consuming/listening to messages from a queue, the module must have an NFR describing message queue consumption (e.g., "listen to incoming messages from ... via message queue"). If missing, flag the module's first NFR line as `FLOW_COVERAGE` with description: "Process flow '<flow name>' step <N> describes message consumption but no NFR in module '<module>' covers this behavior"
  - **Message publishing/forwarding**: If a step describes publishing messages to a queue (forwarding to another system), the module must have an NFR describing message publishing. If missing, flag as `FLOW_COVERAGE`
  - **Acknowledgement publishing**: If a step describes publishing acknowledgement messages, the module must have an NFR describing acknowledgement behavior. If missing, flag as `FLOW_COVERAGE`
  - **Data recording**: If a step describes recording/storing messages in the database, the module must have an NFR describing data storage/recording. If missing, flag as `FLOW_COVERAGE`
  - **Error/failure paths**: If the flow describes error or failure paths (e.g., "response with error if validation failed"), the module must have an NFR or constraint handling that error condition. If missing, flag as `FLOW_COVERAGE`
- **Cross-entity extraction**: If a flow step implies the application extracts or creates entities managed by other modules (e.g., Job Demand processing that extracts Employer and Recruitment Agent data), verify there is an NFR in either the flow's primary module or the target module describing this extraction. If missing, flag as `FLOW_COVERAGE`

##### 4.8.3 Module → Flow Coverage (Reverse Check)

For each module under `# System Module` or `# Business Module`, scan its NFRs for any of the following message-processing behaviors:
- Listening to / consuming messages from a message queue
- Publishing messages to a message queue
- Publishing acknowledgement messages to a message queue
- Processing incoming messages from external systems via message queue

If any NFR describes such behavior, verify that:
- There is a corresponding process flow in the `# High Level Process Flow` section whose name matches or covers this module
- OR the module's message-processing NFR explicitly references another module's process flow (e.g., an NFR says "updated from Job Demand messages" — this is covered by the Job Demand flow)

If no process flow covers the module's message-processing behavior (directly or via cross-reference), flag the first message-processing NFR in the module as `FLOW_COVERAGE` with description: "Module '<module name>' has message-processing NFRs (e.g., <NFR_ID>) but is not covered by any High Level Process Flow"

**Exceptions — do NOT flag these modules:**
- Modules whose NFRs only describe internal asynchronous processing (e.g., event listeners triggered within the application, scheduled tasks, internal Spring events) without external message queue interaction
- Modules whose NFRs explicitly state they receive data as a side effect of another module's message processing (e.g., "Employer information will be extracted from the incoming Job Demand message") — these are indirectly covered by the parent flow

##### 4.8.4 User Story ↔ Process Flow Alignment

For each module that is covered by a process flow (either directly or indirectly):
- **Data availability check**: If a User Story describes viewing, searching, or managing data (e.g., "search for Employer"), verify that the data referenced in the User Story is delivered to the application by at least one process flow. If a User Story references an entity or data type that no process flow delivers, flag the User Story as `FLOW_COVERAGE` with description: "User story <US_ID> references '<entity/data>' but no process flow delivers this data to the application"
- **Contradiction check**: If a User Story implies manual creation or modification of data that a process flow says is only received via message queue (read-only from the application's perspective), and no constraint explicitly permits manual override, flag as `CONTRADICTION`
- **Completeness check**: If a process flow delivers data to the application (e.g., Candidate Registration messages) but the corresponding module has NO User Stories for viewing or managing that data, flag the module's `### User Story` section as `FLOW_COVERAGE` with description: "Process flow '<flow name>' delivers data to this application but module '<module>' has no User Stories for viewing or managing this data"

**Exception**: Modules that are purely system/infrastructure modules (e.g., Authentication, Audit Trail) or modules that only store data as a side effect of another module's processing and have their own explicit User Stories are not required to have a 1:1 User Story for every piece of flow-delivered data.

##### 4.8.5 NFR ↔ Process Flow Status Coverage

For each process flow that defines application-specific statuses in its status table:
- Each status should correspond to a behavior described by an NFR in the relevant module
- If a status is defined in the flow's status table for the application but no NFR in the corresponding module describes the behavior that triggers that status (e.g., status `PROCESSED` implies message processing, status `SC_ACKNOWLEDGED` implies publishing acknowledgement), flag the module's first NFR as `FLOW_COVERAGE` with description: "Process flow '<flow name>' defines status '<STATUS_CODE>' for this application but no NFR in module '<module>' describes the behavior triggering this status"
- Conversely, if an NFR describes a status-producing behavior (e.g., "publish acknowledgement message") but the process flow's status table does not include a matching status for the application, flag the NFR as `FLOW_COVERAGE` with description: "NFR <NFR_ID> describes behavior that should produce a status but process flow '<flow name>' does not define a corresponding application status"

##### 4.8.6 Test Section ↔ Process Flow Alignment

For modules covered by a process flow:
- If the `### Test` section defines test data or test configuration, verify it is consistent with what the process flow describes
- If test instructions reference message structures, queue names, or external system interactions, they should be consistent with the process flow's description. If a test references a message type or system interaction not present in any process flow, flag as `FLOW_COVERAGE`
- Do not flag empty Test sections — test completeness is not the concern of this check

##### 4.8.7 Reference Section ↔ Process Flow Alignment

For modules covered by a process flow:
- If the `### Reference` section references message structure documents (e.g., `[Job Demand Message](path/to/MESSAGE_JOB_DEMAND.md)`), verify the referenced message type aligns with what the process flow says the application receives
- If a Reference points to a message structure for a recruitment step that has no process flow defined, flag as `FLOW_COVERAGE` with description: "Reference <REF_ID> points to message structure for '<message type>' but no process flow is defined for this recruitment step"

### 5. Insert TODO Annotations

For each issue found, insert a `[TODO]` annotation in the PRD.md file:

**Placement rules:**
- Insert the `[TODO]` as a new line **immediately above** (before) the problematic line, at the **same indentation level** as the problematic line
- If the issue relates to a section-level problem (e.g., empty section, cross-module inconsistency), insert the `[TODO]` as a top-level bullet above the first item after the version tag line

**Format:**
```
- [TODO] <CATEGORY>: <description> (line <N>)
- <the problematic line stays unchanged below>
```

**Categories:**
| Category | Code |
|----------|------|
| Incomplete User Story | `INCOMPLETE` |
| Non-Existent Reference | `BAD_REF` |
| Cross-Module Inconsistency | `CROSS_MODULE` |
| Contradictory Requirement | `CONTRADICTION` |
| Duplicate Role | `DUP_ROLE` |
| Architecture Violation | `ARCH_VIOLATION` |
| Process Flow Coverage Gap | `FLOW_COVERAGE` |

**Examples:**
```markdown
- [TODO] INCOMPLETE: User story is missing content after the colon — no sub-bullets describing what the dashboard shows. Add the dashboard items or remove the trailing colon. (line 25)
- As Management Team, I want to be able to view the dashboard showing:
- [TODO] INCOMPLETE: User story is missing "so that [benefit]" clause. Add the business justification. (line 304)
- [TODO] INCOMPLETE: Possible typo — "be to manage" should likely be "be able to manage". (line 304)
- As Super Admin, I want to be to manage divisions
```

### 6. Output Summary

After inserting all TODOs, print a summary table:

```
## Analysis Summary for <Application Name>

| Category              | Count | Modules Affected                  |
|-----------------------|-------|-----------------------------------|
| Incomplete            | X     | Home, Division, ...               |
| Bad Reference         | X     | ...                               |
| Cross-Module          | X     | ...                               |
| Contradiction         | X     | ...                               |
| Duplicate Role        | X     | ...                               |
| Arch Violation        | X     | ...                               |
| Flow Coverage         | X     | ...                               |
| **Total**             | **X** |                                   |

### Details by Module

#### <Module Name>
- [INCOMPLETE] line X: <brief description>
- [BAD_REF] line Y: <brief description>
...
```

## Important Rules

- **NEVER remove, modify, or delete existing content.** Only add new `[TODO]` annotation lines.
- **NEVER modify existing tags** (e.g., `[USHM00003]`, `[v1.0.0]`). These are immutable identifiers.
- Preserve all existing content, formatting, and indentation exactly.
- Each TODO must reference the specific line number where the issue was found for easy navigation.
- Be precise and actionable in TODO descriptions — state what the issue is AND what needs to be done to fix it.
- Do not flag stylistic preferences — only flag genuine quality issues that could lead to implementation ambiguity.
- If a module filter is provided, only analyze that module but still check cross-module references involving it.
- Do not insert duplicate TODOs — if the same issue applies to multiple lines, annotate each line individually but do not repeat the same TODO on the same line.
- Tables, blank lines, version tags (e.g., `[v1.0.0]`), and section headers are never annotated.
- When checking for contradictions, consider the full context — an NFR in one module may intentionally override a general rule stated elsewhere. Only flag clear, unambiguous contradictions.
- When checking roles, the canonical role list is defined in the `## Role > ### Constraint` section under the Role module. Roles not in this list should be flagged.
