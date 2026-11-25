---
name: documenting-appian
description: >
  Generates complete technical documentation for Appian applications from
  XML exports (project root = app folder): inventory, architecture, data model,
  integrations, security, deployment, health analysis, and Mermaid diagrams
  (BPMN flowchart, ER, sequence, state, C4, block-beta, pie, etc.).
  Includes Python automation scripts for each documentation phase.
  Triggers when the task involves documenting, analyzing, auditing, inventorying,
  or diagramming any aspect of an Appian export — including process models,
  CDTs, record types, connected systems, or groups — even without explicitly
  mentioning "technical documentation" or "Mermaid."
  Also activates for health checks, dead code analysis, export diffs/changelogs,
  and import customization file (ICF) generation.
  NOT for Java/Spring/Quarkus projects (use documenting-paas instead).
compatibility: "Python 3.8+ (stdlib only, no pip install required)."
---

# Skill: documenting-appian

## Source of truth

Project root (`.`) — the open project folder **is** the exported Appian application (**read-only** for documentation tasks).
See [references/appian-export-format.md](references/appian-export-format.md) for folder names and parsing notes.

## Goal

Create/update auditable, navigable technical documentation in `docs/`, based **only** on evidence from the project root (`.`).

## Expected outputs

| File | Content |
|------|---------|
| `docs/README.md` | Index + maintenance guide |
| `docs/01-appian-overview.md` | Purpose, scope, naming conventions, complexity metrics |
| `docs/02-appian-glossary.md` | Domain glossary |
| `docs/03-appian-inventory.md` | Object inventory table + `pie` chart |
| `docs/04-appian-architecture.md` | Architecture, entry points, flows (Mermaid) |
| `docs/05-appian-navigation.md` | Site pages → object mapping + `block-beta` |
| `docs/06-appian-data.md` | Record types, data stores, CDTs + `erDiagram` |
| `docs/07-appian-integrations.md` | Web APIs, connected systems + `sequenceDiagram` + `C4Context` |
| `docs/08-appian-security.md` | Group hierarchy `flowchart` + role map matrix |
| `docs/09-appian-deployment.md` | Packaging, ICF template, risks, checklist |
| `docs/appian-import-customization-template.properties` | ICF with actual UUIDs |
| `docs/10-appian-i18n.md` | Translation sets/strings |
| `docs/11-appian-interfaces.md` | Interfaces, expression rules, constants |
| `docs/12-appian-health.md` | Dead code, dependency graph + `stateDiagram-v2` |
| `docs/process-models/` | BPMN `flowchart` diagram per Process Model (PM) |

## Progress tracking (MANDATORY)

Copy this checklist before starting. Update after every phase. Resume from here if interrupted.

```
Documentation Progress ([S] = script, [M] = manual/agent):
- [ ] Phase A: build_uuid_index.py → _uuid-index.json  |  [M] 01-appian-overview.md
- [ ] Phase B: generate_inventory.py → 03-appian-inventory.md  |  [M] 02-appian-glossary.md
- [ ] Phase C: generate_navigation.py → 05-appian-navigation.md  |  pm2mermaid.py (batch ALL PMs)  |  [M] 04-appian-architecture.md
- [ ] Phase D: parse_cdts.py → 06-appian-data.md  |  extract_integrations.py → 07-appian-integrations.md
- [ ] Phase E: extract_role_maps.py → 08-appian-security.md
- [ ] Phase F: extract_translations.py → 10-appian-i18n.md  |  generate_deployment.py → 09-appian-deployment.md + ICF
- [ ] Phase G: analyze_health.py → 12-appian-health.md  |  [M] 11-appian-interfaces.md  |  validate_docs.py → README.md quality  |  [M] README.md
- [ ] Phase H: Wiki published + HTML exported (via wiki-html-publisher)
```

## Scripts (13)

> **Terminology**: "PM" = Process Model, "CS" = Connected System, "CDT" = Custom Data Type, "ICF" = Import Customization File.

All scripts live in `scripts/` (Python 3.8+, stdlib only, no pip install). Run from the project root (the Appian app folder).

| Script | Phase | Output | Auto-generated diagrams |
|--------|-------|--------|------------------------|
| `build_uuid_index.py` | A | `_uuid-index.json` | — |
| `generate_inventory.py` | B | `03-appian-inventory.md` | `pie` |
| `generate_navigation.py` | C | `05-appian-navigation.md` | `block-beta` |
| `pm2mermaid.py` | C | `process-models/*.md` | `flowchart` (BPMN) |
| `parse_cdts.py` | D | `06-appian-data.md` | `erDiagram` (partial) |
| `extract_integrations.py` | D | `07-appian-integrations.md` | `sequenceDiagram` + `C4Context` |
| `extract_role_maps.py` | E | `08-appian-security.md` | `flowchart` (roles) |
| `extract_translations.py` | F | `10-appian-i18n.md` | — |
| `generate_deployment.py` | F | `09-appian-deployment.md` + ICF | — |
| `analyze_health.py` | G | `12-appian-health.md` | `stateDiagram-v2` |
| `validate_docs.py` | G | Quality section → `README.md` (`--fix` auto-corrects Mermaid) | — |
| `list_process_models.py` | utility | stdout (quick ref) | — |
| `diff_exports.py` | utility | `appian-changelog.md` | — |

Shared modules (not standalone): `cli_common.py`, `app_info.py`, `xml_helpers.py`, `constants.py`, `node_classifier.py`, `parser.py`, `mermaid_builder.py`, `mermaid_validator.py`.

`pm2mermaid.py` uses its own argparse (not `cli_common.make_parser()`). See [references/script-details.md](references/script-details.md#pm2mermaidpy--divergent-cli) for its CLI flags and batch usage.

**Quick start**: see [references/bash-commands.md](references/bash-commands.md) for full pipeline commands (Bash + PowerShell) and BPMN batch generation. Run `build_uuid_index.py` first — all other scripts depend on it.

Scripts output to **final document files**. Review and enrich with narrative, cross-references, and additional diagrams rather than regenerating.

**Feedback loop**: If `validate_docs.py` reports issues, fix and re-run until clean. Use `--fix` to auto-correct Mermaid syntax issues.

## Diagram types (9)

| Type | Use case | Auto-generated by | Style reference |
|------|----------|-------------------|-----------------|
| `flowchart` + Palette B | PM (BPMN) diagrams | `pm2mermaid.py` | [references/type-mapping.md](references/type-mapping.md) |
| `flowchart` + Palette A | Dependency graphs, security hierarchy | `extract_integrations.py`, `extract_role_maps.py` | [references/legend.md](references/legend.md) |
| `architecture-beta` | High-level system architecture | Manual | [references/style-architecture-beta.md](references/style-architecture-beta.md) |
| `sequenceDiagram` | Integration flows (per CS) | `extract_integrations.py` | [references/style-sequence-diagram.md](references/style-sequence-diagram.md) |
| `stateDiagram-v2` | Entity lifecycle | `analyze_health.py` | [references/style-state-diagram.md](references/style-state-diagram.md) |
| `erDiagram` | CDT data model | `parse_cdts.py` (partial) | [references/style-er-diagram.md](references/style-er-diagram.md) |
| `block-beta` | Site navigation map | `generate_navigation.py` | [references/style-block-beta.md](references/style-block-beta.md) |
| `C4Context` | System context | `extract_integrations.py` | [references/style-c4-diagram.md](references/style-c4-diagram.md) |
| `pie` | Object distribution | `generate_inventory.py` | Mermaid built-in |

For the **decision tree** on which diagram type to use, palettes, and detailed syntax/examples per type, see [references/legend.md](references/legend.md).

### PM diagram rules

- **ALL** PMs get a diagram (complete + detailed). Simplified view is an ADDITION for >50 nodes, never a replacement.
- `pm2mermaid.py` handles parsing, shape mapping, validation, and auto-fix.
- After batch run, enhance: click links for subprocesses, edge labels on XOR gateways, dotted links for error paths. See [references/type-mapping.md](references/type-mapping.md#post-script-enhancement-rules).
- >30 nodes → `flowchart TD` + `subgraph`. >50 nodes → simplified + detailed views.
- Always validate Mermaid syntax. Use `mermaid_validator.py --fix` for existing docs.

## Phase details & references

| Reference | Content |
|-----------|---------|
| [references/phases.md](references/phases.md) | Detailed instructions per phase |
| [references/templates.md](references/templates.md) | Skeleton Markdown for agent-written docs |
| [references/deployment-risks.md](references/deployment-risks.md) | Deployment risks and ICF template |
| [references/script-details.md](references/script-details.md) | Detailed script documentation + output examples |
| [references/mermaid-validator-checks.md](references/mermaid-validator-checks.md) | Validator checks, severities, auto-fix behavior |
| [references/appian-export-format.md](references/appian-export-format.md) | Export folder names, file formats, parsing notes |
| [references/wiki-publishing.md](references/wiki-publishing.md) | Phase H wiki page mapping and publishing instructions |

## Authoring conventions

- **Output language**: match the primary language of the application (Spanish-first → write in Spanish, keep English technical terms as-is). Keep exact Appian object names unchanged.
- **Traceability**: every document ends with `## Evidencias` enumerating consulted file paths.
- **No secrets**: mask credentials, API keys, tokens, internal hostnames. Connected System URLs are OK if already in the export description.
- **Cross-references**: always use resolved names (not just UUIDs). Link between docs.
- **Naming conventions**: document the prefix convention observed (e.g., `RC_`, `CDT_`, `DS_`, `WA_`, `CS_`, `RT_`).
- **Unverifiable facts**: `TODO(unknown)`. Unresolvable references: `TODO(unresolved-ref: <id>)`.

## Error handling

If a script exits with code **2** (path not found) or **3** (data error), check stderr, fix the cause (e.g., missing `_uuid-index.json` → run `build_uuid_index.py` first), and re-run. All scripts are idempotent.

## Phase H: Wiki publishing + HTML export

**DELEGATED** to the **`wiki-html-publisher`** skill. After Phases A–G and validation, invoke it.
See [references/wiki-publishing.md](references/wiki-publishing.md) for wiki page mapping and detailed instructions.

---

## Definition of Done

- `docs/README.md` links to all other documents
- UUID cross-reference index built and used throughout
- Complete inventory covers all detected object types (XML + XSD)
- Domain glossary with business acronyms and definitions from CDT descriptions
- Data model: Data Stores (JNDI + autoUpdateSchema), Record Types, field-level CDTs, `erDiagram`
- Site navigation map with all pages and target objects
- Architecture: Web APIs table (HTTP method + URL alias), ALL flow categories in indented-text
- Integrations: payloads, CS env URLs, dependency diagram, `sequenceDiagram`, `C4Context`
- Security: group hierarchy diagram (color-coded) + cross-object role map matrix
- ICF template with actual UUIDs
- Deployment: JDBC table, application-specific risks, specific checklist naming actual objects
- BPMN diagram for **every PM**: validated, color-styled, `classDef`, legend link, `## Evidencias`
- Dead code analysis + expression references included
- TODO resolution pass completed
- `validate_docs.py` executed; results in `docs/README.md`
- No secrets in documentation
