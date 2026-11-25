---
name: security-insights
description: >-
  Security Insights: SecurityInsights defines a schema that projects can use to report information about their security in a machine-processable way. Covers Security Insights. Use when publishing a SECURITY_INSIGHTS.yml file. Triggers: Security Insights.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Security Insights

The OpenSSF Security Insights specification: a YAML schema (`header`, `project` and `repository` objects) that a project publishes as `security-insights.yml` so tools and users can read its security contacts, vulnerability reporting, tooling and release details. Read from the specification repository at a pinned release tag.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Maintainer publishing a security-insights.yml file, or a tool author reading one.
- Target version: Security Insights (current); Security Insights 1.0 (legacy). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **`header.schema-version` (required).** "The version of the Security Insights schema being used."
2. **`header.url` (required).** "This should point to the canonical location where the file is hosted (e.g., a raw file URL in a version control system)."
3. **`project.vulnerability-reporting` (required).** "An object describing how security vulnerabilities can be reported and how they are handled by the project."
4. **`VulnerabilityReporting.reports-accepted` (required).** "Indicates whether this project currently accepts vulnerability reports."
5. **File location.** "Place your `security-insights.yml` file in the root of your repository or in your source forge directory (e.g. `.github/` or `.gitlab/`) to support automated detection"

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
- [ ] The file validates against the pinned 2.2.0 schema (`spec/schema.cue` at the same tag), and every required field quoted in `references/requirements.md` is present.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `security-txt`, `openssf-baseline`, `openvex`, `osv`, `yaml`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Security Insights schema 2.2.0](https://raw.githubusercontent.com/ossf/security-insights/v2.2.0/spec/schema.md): OpenSSF Specification, Release v2.2.0 (2026-01-31), checked 2026-10-06.
- [Security Insights CUE schema 2.2.0](https://raw.githubusercontent.com/ossf/security-insights/v2.2.0/spec/schema.cue): OpenSSF Specification, Release v2.2.0 (2026-01-31), checked 2026-10-06.
- [Security Insights README 2.2.0](https://raw.githubusercontent.com/ossf/security-insights/v2.2.0/README.md): OpenSSF Specification, Release v2.2.0 (2026-01-31), checked 2026-10-06.
- [Security Insights specification 1.0.0](https://raw.githubusercontent.com/ossf/security-insights/v1.0.0/specification.md): OpenSSF Specification (superseded), Release v1.0.0 (2023-10-02), checked 2026-10-06.
