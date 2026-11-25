---
name: modelgen-nosql
model: claude-opus-4-8
effort: xhigh
description: >
  Extract NoSQL document models from Agile user stories using Domain-Driven Design (DDD) principles.
  Produces Mermaid class diagrams showing document structure (embedded vs referenced), JSON schema
  examples per collection, and detailed model documentation per module. Use this skill whenever the
  user asks to extract a NoSQL module model, NoSQL document model, NoSQL schema, collection design,
  or document structure from user stories. Also trigger when the user provides user stories grouped
  by module and asks for NoSQL data modeling, document-oriented design, or embed-vs-reference analysis.
  Even if the user says "design my NoSQL collections" or "what documents do I need", this skill applies
  if the input contains structured Agile user stories with module groupings. Do NOT use this skill for
  RDBMS or relational schema extraction â€” use the modelgen-relational skill for that.
  Also trigger when the user says "update the model" or "upgrade the model" to
  incrementally evolve an existing NoSQL document model based on changes in PRD.md.
  Accepts an application name (mandatory), version (mandatory), and optional module argument
  (e.g., `/modelgen-nosql hub_middleware v1.0.3` or `/modelgen-nosql hub_middleware v1.0.3 module:Location Information`).
---

# NoSQL Model Generator

Extract document-oriented NoSQL models from Agile user stories following a systematic DDD methodology.
This skill is database-agnostic and produces generic document models applicable to MongoDB, Couchbase,
DynamoDB, Firestore, CosmosDB, or any document-oriented NoSQL store.

## When to Use

Trigger this skill when the user asks to:
- Extract a NoSQL module model or document model
- Design NoSQL collections or document structures from user stories
- Perform embed-vs-reference analysis on entities
- Generate document schemas from requirements
- Update an existing NoSQL document model based on story changes
- Upgrade the model to a new version
- Detect and fix outdated/invalid model elements

Do NOT use for RDBMS/relational schema extraction â€” use the modelgen-relational skill for that.

## Version Gate

Before starting any work, resolve the application folder first (see Input Resolution below), then check `CHANGELOG.md` in the application folder (`<app_folder>/CHANGELOG.md`):

1. If `<app_folder>/CHANGELOG.md` does not exist, skip this check (first-ever execution for this application).
2. If `<app_folder>/CHANGELOG.md` exists, scan all `## vX.Y.Z` headings and determine the **highest version** using semantic versioning comparison.
3. Compare the requested version against the highest version:
   - If requested version **>=** highest version: proceed normally.
   - If requested version **<** highest version: **STOP immediately**. Print: `"Version {requested} is lower than the current application version {highest} recorded in <app_folder>/CHANGELOG.md. Execution rejected."` Do NOT proceed with any work.

## Input Resolution

The skill requires mandatory `<application>` and `<version>` arguments, with an optional `module:` argument.

### Argument Syntax

| Argument | Required | Description |
|----------|----------|-------------|
| `<application>` | Yes | Application name â€” matched against root-level application folders |
| `<version>` | Yes | Version label (e.g., `v1.0.3`). Used for version-filtered generation. |
| `module:<name>` | No | Limit generation to a single module |

| Format | Example | Meaning |
|--------|---------|---------|
| App + version | `/modelgen-nosql hub_middleware v1.0.3` | All modules, version-filtered |
| App + version + module | `/modelgen-nosql hub_middleware v1.0.3 module:Location Information` | Single module, version-filtered |
| Module quoted | `module:"Location Information"` | Quoted form (equivalent) |
| Module snake_case | `module:location_information` | Converted to title-case for matching |

### Application Folder Resolution

1. List root-level application folders that have a numeric prefix (e.g., `1_hub_middleware`, `2_hc_adapter`)
2. Strip the leading `<number>_` prefix from each folder name (e.g., `1_hub_middleware` -> `hub_middleware`)
3. Match the provided application name **case-insensitively** against the stripped folder names
4. Accept `snake_case`, `kebab-case`, or title-case input (e.g., `hub_middleware`, `hub-middleware`, `Hub Middleware` all match `1_hub_middleware`)
5. If no match is found, list all available application names and **stop**

### Auto-Resolved Paths

| File | Resolved Path |
|------|---------------|
| PRD.md | `<app_folder>/context/PRD.md` |
| Output directory | `<app_folder>/context/model/` |

### Module Matching Rules

1. Match the specified module name **case-insensitively** against modules in PRD.md
2. Convert `snake_case` input to title-case for matching (e.g., `location_information` â†’ `Location Information`)
3. If no module matches, **stop and report available module names** before doing any file writes
4. Exactly one module must match â€” partial or ambiguous matches are rejected with suggestions

### Module-Filtered Generation Mode

When a `module:` argument is provided, the skill operates in **module-filtered mode**:

| Aspect | Full Generation | Module-Filtered |
|--------|-----------------|-----------------|
| Per-module files (model.md, document-model.mermaid, schemas.json) for **target module** | Generate | Generate / overwrite |
| Per-module files for **other modules** | Generate | **SKIP â€” leave untouched** |
| Root `MODEL.md` | Generate full file | **Partial update** â€” only the target module's row in the Modules table, its Table of Contents section, and its Assumptions Summary row are updated. All other module sections remain untouched. |
| Cross-Module Dependencies in MODEL.md | Generate | Update only rows where source or target is the filtered module |
| Update History in MODEL.md | Generate | Append new entry scoped to the target module |

**Module filter is additive, not destructive:** When `module:` is specified, only the named module's content files are written/overwritten. All other module files remain untouched. If the target module does not exist in PRD.md, stop and report available module names before doing any file writes.

**First-time module generation:** If the output directory does not yet contain files for the target module (e.g., generating a new module into an existing model), create the module subdirectory and files normally, then update MODEL.md to include the new module.

### Version Filtering (with or without module)

When a version argument is provided (with or without `module:`):

1. Only process user stories from versions **up to and including** the specified version
2. Stories from later versions are excluded from extraction
3. Version comparison uses the ordering present in PRD.md (versions appear in document order, earlier = lower)
4. The generated model reflects the state of the system at the specified version

When combined with `module:`, both filters apply: only stories in the target module at or below the target version are processed.

---

## Update Mode

This section defines the **incremental update** workflow for evolving an existing NoSQL document
model when user stories change across versions. Use this mode instead of full regeneration when
working with a previously generated model.

### Update Mode Triggers

Activate update mode when the user says:
- "update the model"
- "upgrade the model"

The user must provide a **new version identifier** for the update (e.g., "1.1.0", "v2", "Sprint-4").

### Update Mode Input Contract

| Element | Description |
|---------|-------------|
| **Existing Model Directory** | Path to previously generated output (must contain MODEL.md + module subdirectories with model.md, document-model.mermaid, and schemas.json) |
| **Updated PRD.md** | The updated user story file with changes (additions, modifications, removals) |
| **New Version** | Version label for this update (e.g., "1.1.0", "v2") |

### Update Mode Processing Workflow

#### Phase U1: Baseline Loading

- Read all existing model files (MODEL.md, per-module model.md, document-model.mermaid, schemas.json)
- Build an inventory of current collections, embedded documents, fields, references, enums with their source story traceability tags

#### Phase U2: Change Detection (Diff Analysis)

- Parse the updated PRD.md
- Compare against source story references in existing model files
- Classify changes into:
  - **ADDED** â€” New stories not referenced by any existing model element
  - **MODIFIED** â€” Stories whose text has changed (same tag, different content)
  - **REMOVED** â€” Stories referenced in the model but no longer present in PRD.md
  - **UNCHANGED** â€” Stories with no changes

#### Phase U3: Staleness & Validity Check

For each existing model element (collection, embedded document, field, reference, enum value), check:
- **Orphaned elements**: Source stories entirely removed â†’ flag for removal
- **Partially orphaned**: Some source stories removed but others remain â†’ flag for review
- **Stale fields**: Source story text changed such that the field inference no longer holds â†’ flag for update
- **Stale references**: Relationship patterns changed â†’ flag for re-evaluation
- **Stale embed decisions**: Access patterns or cardinality changed â†’ flag embed-vs-reference re-evaluation
- **Stale enums**: Qualifier terms changed or removed â†’ flag for update
- **Contradictions**: New stories contradict existing model assumptions â†’ flag

Produce a **Staleness Report** table:

| Element Type | Element Name | Module | Status | Reason | Affected Stories | Action |
|---|---|---|---|---|---|---|
| Collection | orders | Order Mgmt | ORPHANED | All source stories removed | [US-010] | REMOVE |
| Field | priority | orders | STALE | Source story US-005 modified | [US-005] | UPDATE |
| Embed Decision | address in orders | Order Mgmt | STALE | Access pattern changed | [US-012] | REVIEW |

Status values: `ORPHANED`, `STALE`, `CONTRADICTED`, `VALID`
Action values: `REMOVE`, `UPDATE`, `REVIEW`, `KEEP`

#### Phase U4: Incremental Extraction

- For ADDED stories: run the full 8-phase extraction pipeline (existing Phases 1â€“8)
- For MODIFIED stories: re-extract affected model elements, compare with existing, merge
- Re-evaluate embed-vs-reference decisions for any affected collections
- Apply new version tag to all new/modified elements

#### Phase U5: Model Merge

- Integrate new/updated elements into existing model
- Remove ORPHANED elements (after confirmation or auto-removal if clearly orphaned)
- Update version annotations on modified elements
- Preserve unchanged elements with their original versions
- Regenerate index recommendations for affected collections

#### Phase U6: Output Regeneration

- Regenerate all output files (document-model.mermaid, schemas.json, model.md, MODEL.md) with merged model
- Add a **Changelog** section to each module's model.md and to the root MODEL.md

---

## Reference Documents

Before processing any input, read both reference documents:

```
Read references/model-extraction-methodology.md
Read references/nosql-design-guide.md
```

- **model-extraction-methodology.md** â€” Defines Phases 1â€“4 (linguistic analysis, entity
  identification, attribute extraction, relationship detection) and appendices (verb heuristics,
  NFR impact map). Reused from the RDBMS skill.
- **nosql-design-guide.md** â€” Defines the document-specific design principles: embed-vs-reference
  decision framework, DDD-to-document classification, access pattern analysis matrix, field
  conventions, NFR adaptations, and all output format conventions with examples.

---

## Input Contract

The user MUST provide the following structured input. If any required element is missing,
ask the user to supply it before proceeding. Do NOT infer modules from story content.

### Required Input

| Element | Description |
|---------|-------------|
| **Module List** | Explicit list of module names (bounded context candidates) |
| **User Stories** | Agile-format stories, each tagged with a **module** and a **version**. Format: "As [role], I want to [action] [object] so that [purpose]" |
| **NFRs per Module** | Non-functional requirements (security, performance, compliance, etc.) |

### Optional Input

| Element | Description |
|---------|-------------|
| **Module Prefix Overrides** | A 3-character prefix per module to override auto-generation. Format: `Module Name: XXX`. |
| **External Reference Files** | Supporting documents (Markdown, CSV, Excel, PDF, JSON, text, YAML, XML) for additional context. |
| **Access Patterns** | Descriptions of how the application reads and writes data. Critical for embed-vs-reference decisions. If not provided, inferred from user stories and flagged as assumptions. |
| **Constraints** | Technical or business constraints affecting the model |
| **Glossary** | Domain-specific term definitions (ubiquitous language) |
| **Existing Data Model** | Current-state model for migration or extension scenarios |

### Input Format Example

```markdown
## Module: User Management

### Version: 1.0

- US-001: As an HR Admin, I want to create employee records so that new hires are registered.
- US-002: As an HR Admin, I want to assign departments to employees so that org structure is maintained.

### Version: 1.1

- US-005: As an HR Admin, I want to update employee contact info so that records stay current.
- US-006: As an HR Admin, I want to assign roles to employees so that permissions are controlled.

#### NFRs
- NFR-EM-001: All entities must support soft delete for compliance.
- NFR-EM-002: Audit trail required for all write operations.

#### Access Patterns (optional)
- AP-001: Employee profile is always read with department name and assigned roles.
- AP-002: List employees by department with pagination (up to 500 per department).
```

The version tag is freeform (e.g., `1.0`, `v2`, `Sprint-3`). Preserved exactly as provided.

### Module Prefix Generation Rules

Each module gets a 3-character uppercase prefix for collection names in shared-database deployment.

**Auto-generation:** Multi-word â†’ first letter of each word ("User Management" â†’ `USM`).
Single-word â†’ first 3 characters ("Billing" â†’ `BIL`). Collisions resolved by alternate
letters or numeric suffix.

**Scope:** Prefix appears in **collection names in diagrams and JSON schemas** only
(e.g., `usm_employees`). The `model.md` uses clean PascalCase names.

**Override:** User can supply 3-character uppercase overrides per module.

### Input Validation Rules

1. **Requirement tagging is mandatory.** Before processing, scan the input PRD.md file and verify that ALL top-level bullet items under User Story, Functional Requirements, Non Functional Requirement, Constraint, and Reference sections have a tag code (e.g., `[USHM00003]`, `[NFRHM0003]`, `[CONSHM003]`, `[REFHM0003]`). If ANY item is missing a tag, **stop immediately** and invoke the `co2-skills:util-ustagger` skill on the file to tag all untagged items. Only resume model extraction after all items are tagged. These tag codes will be used as the `Source Story` reference throughout the model output.
2. **Module-story binding is mandatory.** Stop and ask if stories lack module assignment.
3. **Version tag is mandatory.** Stop and ask if stories lack version tags.
4. **Story format check.** Flag deviations but attempt to parse.
5. **At least one NFR per module.** Prompt for confirmation of defaults if missing.
6. **Output directory is auto-resolved.** The output directory is automatically resolved to `<app_folder>/context/model/`. Auto-create if the path doesn't exist.

---

## Processing Workflow

When no `module:` argument is provided, process ALL modules in a single pass. When a
`module:` argument is provided, process ONLY the target module â€” skip all other modules
entirely. Each module is independent â€” do not model cross-module references. Flag
potential cross-module dependencies in assumptions.

### Version Tracking

Process stories in version order. Annotate every model element with the version that
introduced it. New fields added in later versions carry the later version; the collection
retains its original version.

### Pre-Processing: External Reference Files

If provided, read external files before Phase 1. They supplement â€” not replace â€” user stories.
Every collection must trace to a user story. Reference-only entities go in assumptions.
Set Source to `REFERENCE` with filename in Source Story when a field comes from a reference file.
On conflicts, prefer user stories and flag the discrepancy.

### Phase 1: Linguistic Analysis

Parse each user story per the methodology reference (Section 3). Extract subjects, verbs,
direct/indirect objects, purpose clauses, qualifiers. Decompose compound stories.

### Phase 2: Entity Identification â†’ Document Classification

Classify extracted nouns using the methodology reference (Section 4.2), then apply the
**DDD-to-document classification** from the NoSQL design guide. Key principle: aggregate
roots become collections; entities within aggregates become embedded documents; value objects
are always embedded; M:N join entities become arrays of references unless data-rich.

### Phase 3: Access Pattern Analysis (NoSQL-Specific)

For each collection candidate, run through the **Access Pattern Analysis Matrix** from
the NoSQL design guide. If the user provided access patterns, use them directly. If not,
infer from user stories (especially purpose clauses) and flag each inference as an assumption.

### Phase 4: Embed vs Reference Decision

Apply the **Embed vs Reference Decision Flowchart** from the NoSQL design guide to every
relationship. Record each decision with rationale in the Document Design Decisions table.
Default to embedding; only promote to a separate collection when criteria are met.

### Phase 5: Field Extraction

Derive fields from four sources in priority order: explicit mention, operation inference,
NFR requirements, domain convention. Use **document-specific field conventions** from the
NoSQL design guide (`_id`, `_audit`, `_version`, `ISODate`, etc.).

Source types: `EXPLICIT`, `OPERATION_INFERENCE`, `NFR`, `CONVENTION`, `REFERENCE`, `ASSUMPTION`.

### Phase 6: Cross-Cutting Concerns

Map NFRs to document model impact using the **NFR Adaptation** table in the NoSQL design guide.

#### Phase 6a: Architecture Principle Integration

If PRD.md contains an `# Architecture Principle` section, read it and apply to model decisions:

- **Document DB confirmation**: If architecture explicitly confirms "document based database" or "MongoDB", gain higher confidence in embed-vs-reference decisions â€” favor embedding more aggressively for frequently co-read data.
- **Consistency model**: If architecture mentions "eventual consistency", flag denormalization assumptions with lower severity in the Assumptions table. Rationale entries in the Document Design Decisions table (Section 4) should reference the architecture principle (e.g., "DENORMALIZE: architecture allows eventual consistency â€” stale reads acceptable").
- **Event-driven**: If architecture mentions "event-driven" or "domain events", generate event collection schemas alongside data collections. Add event payload document types and event store collection if applicable.
- **CQRS hints**: If architecture mentions "CQRS" or "command query separation", consider separate read/write collection patterns and note them in the Collection Catalog.
- **Monolithic**: If "monolithic" with "modular architecture", model cross-module references as soft references (ObjectId fields without formal FK enforcement) and note this in Cross-Module Dependencies.

If the `# Architecture Principle` section is absent, skip this sub-phase and proceed with existing behavior.

#### Phase 6b: Process Flow Integration

If PRD.md contains a `# High Level Process Flow` section, read it and apply to model decisions:

- **Entity lifecycle states**: If a process flow describes status transitions (e.g., "Received â†’ Validated â†’ Enriched â†’ Active"), cross-reference with enum extraction from Phase 2. Ensure all states from flows appear in the corresponding collection's status enum. Add any missing states.
- **Access patterns from flows**: Process flow steps that describe queries (e.g., "system queries job demands by corridor and status") directly inform the Access Pattern Analysis (Phase 3) and index recommendations (Section 9). Record each flow-derived access pattern.
- **Intermediate collections**: If a flow describes staging or temporary data (e.g., "incoming message stored before validation"), verify that corresponding staging collections exist. If not, create them.
- **Domain events from flows**: Each "publishes", "sends", or "triggers" step should be checked against the Domain Events table (Section 10). Add any flow-derived events not already captured.

If the `# High Level Process Flow` section is absent, skip this sub-phase.

### Phase 7: Output Generation

Produce three deliverables per domain (see Output Specification below).

### Phase 8: Validation

Run quality gates as self-review. Fix issues before presenting output.

---

## Changelog Append

After all model files are successfully generated, append an entry to `CHANGELOG.md` in the application folder (`<app_folder>/CHANGELOG.md`):

1. Read `<app_folder>/CHANGELOG.md`. If it does not exist, create it with:
   ```markdown
   # Changelog

   - This file tracks all skill executions by version for this application.
   - The highest version recorded here is the current application version.
   - Skills MUST NOT execute for a version lower than the highest version in this file.

   ---
   ```
2. Search for a `## {version}` heading matching the current version.
3. If the section **exists**: append a new row to its table.
4. If the section **does not exist**: insert a new section after the `---` below the context header and before any existing `## vX.Y.Z` section (newest-first ordering), with a new table header and the first row.
5. Row format: `| {YYYY-MM-DD} | {application_name} | modelgen-nosql | {module or "All"} | Generated NoSQL document models |`
6. **Never modify or delete existing rows.**

## Output Specification

For each module, produce exactly **three files** in a kebab-case subdirectory, plus one
**root-level summary file**:

```
/output-dir/
â”œâ”€â”€ MODEL.md                          # Root summary and table of contents
â””â”€â”€ {module-name}/
    â”œâ”€â”€ document-model.mermaid        # Mermaid class diagram
    â”œâ”€â”€ schemas.json                  # JSON schema examples with sample documents
    â””â”€â”€ model.md                      # Full model documentation
```

### 1. Document Structure Diagram: `document-model.mermaid`

A Mermaid **class diagram** showing collections, embedded documents, and references.
Follow all conventions from the **Output Format Conventions** section of the NoSQL design guide:
stereotypes (`<<collection>>`, `<<embedded>>`, `<<enum>>`), composition vs association arrows,
prefixed collection names, and camelCase fields. Include version and prefix comments at top.

### 2. JSON Schema Examples: `schemas.json`

A JSON file with an example document per collection, following the format in the NoSQL design
guide. Each collection entry includes: `description`, `exampleDocument` (realistic sample data
showing all fields, embedded documents, arrays), and `indexes` (recommended indexes from
access patterns). Include `_meta` block with domain, prefix, and versions.

### 3. Model Documentation: `model.md`

```markdown
# NoSQL Document Model: {Module Name}

## 1. Module Prefix Map
| Module | Prefix | Auto-Generated | Override |

## 2. Collection Catalog
| Collection | DDD Type | Bounded Context | Document Type | Key Fields | Source Stories | Version |
(Document Type: Root Collection, Supporting Collection, Event Collection, Audit Collection)

## 3. Base Document Specification
(Audit, soft delete, versioning fields common to all documents)

## 4. Document Design Decisions
| Parent | Child | Decision | Rationale | Access Pattern | Source Story | Version |
(Decision: EMBED, EMBED_ARRAY, REFERENCE, DENORMALIZE_AND_REFERENCE)
This is the most critical table â€” records every embed-vs-reference decision with reasoning.

## 5. Field Detail (one subsection per collection)
### 5.x {Collection Name}
| Field | Type | Nullable | Constraints | Source | Source Story | Version |
Source values: EXPLICIT, OPERATION_INFERENCE, NFR, CONVENTION, REFERENCE, ASSUMPTION.
Type values: String, Number, Boolean, ObjectId, ISODate, Object, Array<Type>, enum name.

## 6. Embedded Document Definitions (one subsection per embedded type)
### 6.x {Embedded Document Name}
| Field | Type | Nullable | Description | Source Story | Version |

## 7. Enum Definitions (one subsection per enum)
### 7.x {Enum Name}
| Value | Description | Source Story | Version |

## 8. Reference Catalog
| Source Collection | Target Collection | Reference Field | Denormalized Fields | Cardinality | Business Rule | Source Story | Version |

## 9. Index Recommendations
| Collection | Field(s) | Index Type | Rationale | Source Story | Version |
(Index Type: unique, single, compound, text, ttl)

## 10. Domain Events
| Event Name | Trigger Story | Aggregate | Payload Fields | Version |

## 11. Bounded Context Summary
| Context | Collections | Description |

## 12. Assumptions and Ambiguities
| Story ID | Collection / Field | Assumption Made | Clarification Needed | Version |

## 13. Changelog

### Version {new-version} (from {previous-version})

#### Added
| Element Type | Name | Description | Source Stories |
|---|---|---|---|

#### Modified
| Element Type | Name | Change Description | Previous | New | Source Stories |
|---|---|---|---|---|---|

#### Removed
| Element Type | Name | Reason | Former Source Stories |
|---|---|---|---|

#### Flagged for Review
| Element Type | Name | Issue | Recommendation |
|---|---|---|---|
```

### 4. Root Summary: `MODEL.md`

After generating all per-module files, produce a single `MODEL.md` in the **root output directory**.
This file serves as the entry point and table of contents for the entire model extraction output.

#### Document Structure

```markdown
# NoSQL Document Model Summary

> Generated from {total story count} user stories across {module count} modules.

## Modules

| # | Module | Prefix | Collections | Embedded Docs | References | Versions | Stories |
|---|--------|--------|-------------|---------------|------------|----------|---------|

(One row per module. Collections = count of root collections. Embedded Docs = count of
embedded document types. References = count of cross-collection references. Versions =
comma-separated list of versions included. Stories = count of source stories for that module.)

## Table of Contents

### {Module Name} (`{prefix}`)

> {One-line summary: e.g., "Manages employee records, departments, and role assignments."}

- **Model Documentation:** [{module-kebab}/model.md](./{module-kebab}/model.md)
- **Document Structure Diagram:** [{module-kebab}/document-model.mermaid](./{module-kebab}/document-model.mermaid)
- **JSON Schemas:** [{module-kebab}/schemas.json](./{module-kebab}/schemas.json)
- **Collections:** {comma-separated collection names in lower_snake_case with prefix}
- **Key Design Decisions:** {2â€“3 most significant embed-vs-reference decisions in natural language}

(Repeat for each module, in the same order as the Modules table.)

## Cross-Module Dependencies

| Source Module | Target Module | Dependency | Noted In |
|---------------|---------------|------------|----------|

(List any cross-module dependencies flagged in assumptions tables. If none, state "No
cross-module dependencies were identified.")

## Assumptions Summary

| Module | Count | Critical |
|--------|-------|----------|

(Count = total assumptions for that module. Critical = count of assumptions marked as
needing clarification. Links to the respective module's Assumptions and Ambiguities section.)

## Update History

| Version | Date | Modules Affected | Added | Modified | Removed | Flagged |
|---|---|---|---|---|---|---|
```

---

## Constraints

1. **No module inference.** Module-to-story mapping must be provided by the user.
2. **Modules are independent.** No cross-module references. Flag dependencies in assumptions.
3. **Concise output.** Final consolidated output only â€” no intermediate analysis.
4. **Traceability.** Every element must reference its originating user story or NFR.
5. **Ambiguity transparency.** Record all assumptions, especially around access patterns
   and embed-vs-reference decisions.
6. **Document-first thinking.** Default to embedding. Only promote to a separate collection
   when a clear "reference when" criterion is met, justified in Document Design Decisions.

---

## Quality Gates (Self-Review)

Before presenting output, verify:

- [ ] Every user story maps to at least one collection or embedded document
- [ ] Every collection has at least one source user story
- [ ] Every collection has `_id` and audit fields
- [ ] Every embed-vs-reference decision is recorded with rationale
- [ ] Every access pattern (provided or inferred) is addressed
- [ ] Every state-change verb has a corresponding enum
- [ ] Every NFR has been analyzed for document model impact
- [ ] No embedded array is unbounded without justification
- [ ] No document likely exceeds typical size limits (flag if > 1MB estimated)
- [ ] Denormalized fields are identified with their source collection
- [ ] Index recommendations cover all query patterns
- [ ] Naming is consistent (camelCase fields, lower_snake_case collections with prefix)
- [ ] Mermaid class diagram is syntactically valid
- [ ] JSON schema examples are valid JSON with realistic sample data
- [ ] All ambiguities are recorded with proposed defaults
- [ ] Root `MODEL.md` is generated with correct links to all module subdirectories
- [ ] `MODEL.md` module statistics (collection count, embedded doc count, story count) match actual output

### Update Mode Quality Gates

When running in update mode, additionally verify:

- [ ] All removed stories have their model elements addressed (removed or re-sourced)
- [ ] All modified stories have their model elements re-evaluated
- [ ] No orphaned elements remain without explicit KEEP justification
- [ ] Embed-vs-reference decisions re-evaluated for affected collections
- [ ] Changelog accurately reflects all changes
- [ ] Version annotations are correct (new elements get new version, unchanged keep original)
- [ ] MODEL.md Update History is current

### Module-Filtered Mode Quality Gates

When running with a `module:` argument, additionally verify:

- [ ] Only the target module's files were written/overwritten
- [ ] Other module subdirectories were not modified
- [ ] MODEL.md was partially updated (only target module rows/sections changed)
- [ ] If target module is new, MODEL.md includes the new module in the Modules table and Table of Contents
- [ ] Module matching was case-insensitive and unambiguous
