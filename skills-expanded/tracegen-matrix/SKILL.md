---
name: tracegen-matrix
model: claude-sonnet-4-6
effort: medium
description: >
  Requirement-to-code traceability generator — links every PRD requirement ID (User Stories,
  Non-Functional Requirements, Constraints) and bug code from a module's SPEC.md to the source
  code that implements it, and writes a per-application context/TRACEABILITY.md matrix. Resolves
  links primarily from the in-source CO2 traceability comments written by conductor-feature-develop
  and conductor-defect (e.g. `Implements: USHM00003`, `Bug fixes: [BUG-024]`), with a name-based
  source-scan fallback, and OPTIONAL precision enrichment from the codebase-memory knowledge graph
  when that MCP server is installed. Works fully WITHOUT codebase-memory. Takes an application name
  (mandatory), with optional version and module filters. Use when the user asks to "generate
  traceability", "update the traceability matrix", "link requirements to code", "regenerate
  TRACEABILITY.md", or when invoked as a sub-step by the feature/defect conductors after code or
  bug-fix changes.
---

# Tracegen — Traceability Matrix

Generate / update `<app_folder>/context/TRACEABILITY.md` — a per-application matrix linking every
PRD requirement ID (and bug code) to the source code that implements it. Two layers per module:
**module-level** (every ID of a module → that module's implementing code, complete coverage) and
**symbol-level** (specific ID → the specific file/symbol that implements it, where derivable).

This skill is **codebase-memory-OPTIONAL**. It resolves links from in-source traceability comments
and source scanning, and only uses the codebase-memory MCP for extra precision when present. It must
NEVER fail or produce an empty file just because codebase-memory is not installed.

## When to Use This Skill

- Automatically, as the final traceability step of `conductor-feature-develop` (after all modules
  for a version are implemented) and `conductor-defect` (after all bugs for a version are fixed).
- Manually, when a user asks to (re)generate or refresh the traceability matrix for an application.

## Prerequisites

- `<app_folder>/context/PRD.md` — tagged requirement IDs (run `util-ustagger` first if untagged).
- `<app_folder>/context/specification/<module>/SPEC.md` — per-module specs with a Traceability
  section listing the module's requirement IDs (and, for backends, the implementing package).
- Application source code under `<app_folder>/` (or the resolved `source:` path). If no source code
  exists yet, the skill still produces a forward-traceability stub (see Workflow step 6c).

## Version Gate

Before starting any work, resolve the application folder first (see Input Resolution), then check
`CHANGELOG.md` in the application folder (`<app_folder>/CHANGELOG.md`):

1. If `<app_folder>/CHANGELOG.md` does not exist, skip this check (first-ever execution).
2. If it exists, scan all `## vX.Y.Z` headings and determine the **highest version** via semantic
   version comparison.
3. If a `version:` argument was provided and the requested version **<** highest version → **STOP
   immediately**. Print: `"Version {requested} is lower than the current application version
   {highest} recorded in <app_folder>/CHANGELOG.md. Execution rejected."`
4. If no `version:` argument was provided (regenerating against the current state), skip the gate.

## Input Resolution

```
/tracegen-matrix <application> [version:<version>] [module:<module>] [source:<source-code-path>]
```

| Argument | Required | Description |
|----------|----------|-------------|
| `<application>` | Yes | Application name OR an already-resolved `<app_folder>` path. Matched against root-level application folders. |
| `version:<version>` | No | Single version (e.g. `version:v1.2.0`). Used for the Version Gate and to label the changelog row and the file header. Does NOT filter which IDs are linked — the matrix always reflects the full current PRD + code. |
| `module:<module>` | No | If provided, (re)generate ONLY that module's section in TRACEABILITY.md, preserving all other sections. If omitted, regenerate the whole file. |
| `source:<path>` | No | Path where source code resides. Defaults to `<app_folder>` (same convention as the conductors). |

### Application Folder Resolution

1. If `<application>` is already a path to an existing folder containing a `context/` subfolder,
   use it directly as `<app_folder>` (this is how the conductors pass it).
2. Otherwise, list root-level application folders; strip any leading `<number>_` prefix; match the
   provided name case-insensitively (accept snake_case, kebab-case, or title-case).
3. If no match is found, list available applications and **stop**.

### Auto-Resolved Paths

| Item | Resolved Path |
|------|---------------|
| PRD.md | `<app_folder>/context/PRD.md` |
| Specifications | `<app_folder>/context/specification/<module>/SPEC.md` |
| Develop tracking | `<app_folder>/context/develop/<module>/IMPLEMENTATION_MODULE.md` |
| Source code | `<source-code-path>/` (defaults to `<app_folder>/`) |
| Output | `<app_folder>/context/TRACEABILITY.md` |

## Resolution Strategy (codebase-memory is OPTIONAL)

Pick code references for each requirement ID using the following cascade. Combine the layers — do
not stop at the first that yields a hit.

1. **In-source traceability comments (PRIMARY — no MCP, deterministic).**
   `conductor-feature-develop` stamps every source file it creates with a top-of-file comment
   listing the requirement codes it implements, and `conductor-defect` appends bug codes:
   ```
   Implements: USHM00003, USHM00006
   NFR: NFRHM0003
   Constraints: CONSHM003
   Bug fixes: [BUG-024]
   ```
   For each requirement / bug code, scan the source tree for that exact code. Every file whose
   top-of-file comment contains the code is an implementer of it. Map file → symbol using the
   primary declared type/function in that file (class/interface/component name, usually = filename).
   - Recommended scan: ripgrep over source files, excluding `context/`, build output, dependencies,
     and tests — e.g. search the codes within the first ~20 lines / comment blocks of each file.

2. **Name-based source scan (FALLBACK — no MCP).**
   When a module's IDs produce NO comment hits (e.g. legacy code authored before the traceability-
   comment rule, as in pre-existing applications), resolve at module granularity instead:
   - Backend: read the module's `SPEC.md` `Package` (e.g. `my.app.module.foo`) and locate the
     matching source directory; collect its controller / service / repository / entity / mapper /
     DTO files.
   - Frontend: read the module's `SPEC.md` named pages/components/hooks/api and `Mockup Screens`,
     then locate the matching source files by name under the app's `src/`.
   Every ID of the module links to this resolved set (module-level layer).

3. **codebase-memory enrichment (OPTIONAL — only if the MCP is installed).**
   If the `codebase-memory` MCP tools (`search_graph`, `search_code`) are available in this session,
   resolve each matched file to its exact graph `qualified_name` for precise, navigable anchors, and
   use the graph to discover additional same-module symbols. If the MCP is NOT available, skip this
   step entirely and use **file-path references** instead (see Reference Format). The matrix content
   and structure are identical either way; only the anchor precision differs.

**Hard rule:** never invent a reference. A reference must come from a real comment hit, a real
source file located on disk, or (when present) a real codebase-memory node. If a specific symbol
cannot be resolved, leave the symbol-level cell as `—`; the module-level layer still covers it.

### Reference Format

- **codebase-memory present** → use the full graph `qualified_name` (exact node anchor).
- **codebase-memory absent** → use a repo-relative path with optional symbol suffix:
  `path/to/File.java#ClassName` (or `src/features/foo/pages/FooPage.tsx#FooPage`).

Record which mode was used in the file header so readers know how to interpret the anchors.

## Workflow

1. **Resolve inputs** — application folder, source path, optional version/module (Input Resolution).
   Apply the Version Gate.
2. **Detect capabilities** — record: (a) is the codebase-memory MCP available? (b) do source files
   carry in-source traceability comments? (sample a few known IDs). These two booleans select the
   active resolution layers and the Reference Format.
3. **Enumerate modules** — glob `<app_folder>/context/specification/*/SPEC.md`. If `module:` was
   provided, restrict to that module.
4. **Extract requirement IDs per module** — from each `SPEC.md` Traceability section: User Story,
   NFR, and Constraint IDs with their version tags. Also collect the module's `Package` (backend)
   or named components (frontend), and any `[BUG-XXX]` codes recorded for the module in PRD.md's
   `### Bug` section. Cross-check `<app_folder>/context/develop/<module>/IMPLEMENTATION_MODULE.md`
   when present for explicit ID→symbol hints.
5. **Resolve code references** — apply the Resolution Strategy cascade to build, per module:
   - the **module-level** set (the module's implementing files/symbols), and
   - **symbol-level** links for the specific IDs where a comment hit or SPEC/IMPLEMENTATION naming
     pins a specific file/symbol. Mark symbol-level links inferred when derived from naming rather
     than an explicit comment hit.
6. **Write TRACEABILITY.md** using the Output structure below.
   - a. Whole-file regeneration when no `module:` filter.
   - b. Single-module update when `module:` is given — replace only that module's `## <Module>`
     section, preserving every other section and the file header/summary (recompute the summary).
   - c. If NO source code exists for the app yet, still write the file: list every module's full ID
     inventory with all symbol cells `—`, plus the module's *intended* SPEC-named symbols as plain
     (non-anchor) references, and a prominent NOT-YET-IMPLEMENTED banner. This preserves forward
     traceability and is regenerated to real anchors once code exists.
7. **Changelog Append** — see below.
8. **Print a summary** — modules processed, total IDs linked (US/NFR/CON counts), symbol-level link
   count, resolution mode used (comments / name-based / graph-enriched), and any unresolved IDs.

## Output

A single file: `<app_folder>/context/TRACEABILITY.md`.

```markdown
# Traceability — <Application Display Name>

> **Purpose**: links every PRD requirement ID (User Stories, NFRs, Constraints) and bug code from
> `context/PRD.md` + `context/specification/*/SPEC.md` to the source code that implements it.
> **Resolution mode**: <in-source comments | name-based scan | graph-enriched> — anchors are
> <codebase-memory qualified_names | repo-relative file paths>.
> **Two layers**: _module-level_ — every ID of a module maps to that module's implementing code
> (complete); _symbol-level_ — specific ID → the specific file/symbol where derivable (partial,
> `(inferred)` when from naming rather than an in-source comment).
> **Maintenance**: regenerated by `tracegen-matrix` at the end of `conductor-feature-develop` and
> `conductor-defect`; re-run manually after significant code moves.

---

## <Module Name>  ·  prefix `<PFX>`  ·  package `<package or n/a>`

**Module-level code** (every ID below maps to these):
- `<reference>` — <role e.g. Controller / Page>
- `<reference>` — <role e.g. ServiceImpl / Hook>
- …

**Requirement links:**

| ID | Type | Ver | Symbol-level implementation |
|----|------|-----|-----------------------------|
| USHM00003 | US | v1.0.0 | `<reference>` |
| NFRHM0003 | NFR | v1.0.0 | — |
| CONSHM003 | CON | v1.0.0 | `<reference>` (inferred) |
| BUG-024 | BUG | v1.0.1 | `<reference>` |

---

(repeat per module)

## Summary
- Modules: <N>
- IDs linked: <N> (US <a>, NFR <b>, CON <c>, BUG <d>)
- Symbol-level links: <N>
- Resolution mode: <comments | name-based | graph-enriched>
- Unresolved: <short list or "none">
```

Type abbreviations: US = User Story, NFR = Non-Functional Requirement, CON = Constraint, BUG = bug
fix code.

## Changelog Append

After the matrix is successfully written, append an entry to `<app_folder>/CHANGELOG.md`:

1. If `<app_folder>/CHANGELOG.md` does not exist, create it with the standard CO2 changelog header.
2. Determine the version label: the `version:` argument if provided, else the highest version in
   the changelog, else `v1.0.0`.
3. Search for a `## {version}` heading. If it exists, append a new row; if not, insert a new section
   after the `---` below the header and before any existing `## vX.Y.Z` section (newest-first).
4. Row format: `| {YYYY-MM-DD} | {application_name} | tracegen-matrix | {module or "All"} | Regenerated TRACEABILITY.md — {N} IDs linked ({fine} symbol-level), mode: {resolution-mode} |`
5. **Never modify or delete existing rows.**

## Constraints

- **codebase-memory is OPTIONAL.** The skill MUST complete and produce a useful TRACEABILITY.md
  when the codebase-memory MCP is absent, using in-source comments and source scanning. Treat the
  graph purely as an enrichment for anchor precision.
- **Never fabricate a reference.** Every anchor must trace to a real in-source comment, a real file
  on disk, or a real graph node. Unresolved symbol-level cells are `—`.
- **Preserve unrelated sections.** With a `module:` filter, only that module's section may change.
- **Do not modify source code, PRD.md, SPEC.md, or any other artifact.** This skill only writes
  `TRACEABILITY.md` and appends one `CHANGELOG.md` row.
- **Preserve requirement tags verbatim.** Use the 9-character `util-ustagger` codes and `[BUG-XXX]`
  codes exactly as they appear; never reformat or invent codes.
- **Idempotent.** Re-running with the same inputs reproduces the same matrix (modulo newly added
  code or requirements).
