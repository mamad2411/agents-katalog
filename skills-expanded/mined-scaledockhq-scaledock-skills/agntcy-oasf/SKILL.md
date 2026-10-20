---
name: agntcy-oasf
description: >-
  Open Agentic Schema Framework (OASF): describe AI agents, their skills and domains in standard records. Covers OASF 1.1.0, OASF 1.2 (track preview). Use when describing agent capabilities with OASF. Triggers: OASF.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.1"
  kind: standard
---

# Open Agentic Schema Framework

The Open Agentic Schema Framework (OASF) from AGNTCY is a schema system for describing AI agents in records annotated with skills, domains and modules. This skill quotes the OASF repository at the v1.1.0 tag (README, the `record` object, the base skill, domain and module classes, the class metaschema and the contribution guide's schema conventions), plus the README and changelog of the main development line.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Record publisher (agent author or registry), record consumer or validator, or schema extension author.
- Target version: OASF 1.1.0 (current); OASF 1.2 (preview, posture: track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Schema Versioning and Immutability.** "Once a schema version is released, no changes to that version of the schema are expected, except for non-breaking fixes such as documentation updates or minor bug corrections."
2. **record.version (required).** "The version of the record. Values MAY conform to a specific versioning schema."
3. **record.schema_version (required).** "Version of the OASF schema."
4. **record.created_at (required).** "Includes the creation timestamp."
5. **record.skills (required).** "List of skills associated with this record."
6. **base_module.name (required).** "The name as a unique identifier of the module."
7. **base_module.data (required).** "The data associated with the module."
8. **class.schema.json category.** "If true, indicates this class is a category (organizational structure) and should not be used as an actual value."
9. **Adding or Modifying an `attribute`.** "Attribute names must be a valid UTF-8 sequence."
10. **Adding or Modifying an `attribute`.** "Attribute names must be all lowercase."
11. **Defining an `object`.** "All objects in OASF must extend a base definition of `object` or another existing object."
12. **Versioning.** "OASF does **not** follow semantic versioning."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Every record sets `name`, `version`, `schema_version`, `description`, `authors`, `created_at` and `skills`, the attributes `record.json` marks required.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `a2a`, `mcp`, `open-agent-spec`, `agent-skills`, `json-schema`, `semver`.

- `dns-aid` for discovering agents through DNS records: `npx skills add ScaleDockHQ/scaledock-skills --skill dns-aid`.
- `agent-network-protocol` for the Agent Network Protocol and its agent descriptions: `npx skills add ScaleDockHQ/scaledock-skills --skill agent-network-protocol`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [OASF README (v1.1.0)](https://raw.githubusercontent.com/agntcy/oasf/v1.1.0/README.md): Release, Tag v1.1.0, commit f510be0, 2026-07-10, checked 2026-10-06.
- [OASF record object (v1.1.0)](https://raw.githubusercontent.com/agntcy/oasf/v1.1.0/schema/objects/record.json): Release, Tag v1.1.0, commit f510be0, 2026-07-10, checked 2026-10-06.
- [OASF base skill class (v1.1.0)](https://raw.githubusercontent.com/agntcy/oasf/v1.1.0/schema/skills/base_skill.json): Release, Tag v1.1.0, commit f510be0, 2026-07-10, checked 2026-10-06.
- [OASF base domain class (v1.1.0)](https://raw.githubusercontent.com/agntcy/oasf/v1.1.0/schema/domains/base_domain.json): Release, Tag v1.1.0, commit f510be0, 2026-07-10, checked 2026-10-06.
- [OASF base module class (v1.1.0)](https://raw.githubusercontent.com/agntcy/oasf/v1.1.0/schema/modules/base_module.json): Release, Tag v1.1.0, commit f510be0, 2026-07-10, checked 2026-10-06.
- [OASF class metaschema (v1.1.0)](https://raw.githubusercontent.com/agntcy/oasf/v1.1.0/schema/metaschema/class.schema.json): Release, Tag v1.1.0, commit f510be0, 2026-07-10, checked 2026-10-06.
- [OASF Contribution Guide (v1.1.0)](https://raw.githubusercontent.com/agntcy/oasf/v1.1.0/CONTRIBUTING.md): Release, Tag v1.1.0, commit f510be0, 2026-07-10, checked 2026-10-06.
- [OASF README (main)](https://raw.githubusercontent.com/agntcy/oasf/a2c7e161a9b8534da921dfb029b9e6523609c5f7/README.md): Development, main at commit a2c7e16, 2026-10-06, schema 1.2.0-dev, checked 2026-10-06.
- [OASF Changelog (main)](https://raw.githubusercontent.com/agntcy/oasf/a2c7e161a9b8534da921dfb029b9e6523609c5f7/CHANGELOG.md): Development, main at commit a2c7e16, 2026-10-06, schema 1.2.0-dev, checked 2026-10-06.
