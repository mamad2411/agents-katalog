---
name: tableau
description: Build and edit Tableau dashboards as code via .twb workbooks - schema-correct XML generated from a compact spec, validated against Tableau's official XSD before anyone opens it. Use when the team's BI tool is Tableau and a dashboard, sheet, or data connection needs building, fixing, or reviewing.
---

# Tableau - .twb Authoring & Validation

Owner: `dashboard-developer`, with `tableau-validator` for the validation gate and `analytics-engineer` for the data layer. Args describe the work, e.g. `/tableau build the exec revenue dashboard`.

A `.twb` is plain XML. That makes a Tableau dashboard an ordinary code artifact - spec'd, built, diffed, reviewed, and version-controlled like everything else the team ships. Since February 2026 Tableau publishes [official XSD schemas](https://github.com/tableau/tableau-document-schemas) for the format, explicitly as a reference for agents to build and validate against. Work it as code, not as a GUI you can't reach.

## Procedure

1. **Check this is the right path.** This skill applies when `{{BI_TOOL}}` is Tableau, or the user explicitly asked for Tableau. If the team's tool is Power BI, Looker, Excel, or nothing yet, stop and return to `/build-dashboard` - none of the guidance below transfers. If `{{BI_TOOL}}` is still an unfilled placeholder, ask which tool the team uses before building anything.

2. **Detect what you can actually do.** Read `references/tooling-tiers.md` and run the detection commands. State the tier before you start. Tier 1 needs only Python and the free Tableau Public app; it is the honest default and it is enough to build a complete, correct dashboard. Never install anything yourself - recommend, state the licence cost, let the user decide.

3. **Spec before building.** Do not re-derive requirements here - `/build-dashboard` steps 1-4 own the audience, the 1-3 questions, the metrics (which must already exist in `knowledge/metrics-catalog.md`), the filters, and the layout sketch. This skill owns implementation only. If there's no `dashboards/<name>/SPEC.md` yet, go write one first.

4. **Build the data layer first.** Every sheet reads from a mart or summary table - no heavy logic in the workbook (`standards/tableau-standards.md`). Decide the connection per `references/connections.md`: a CSV exported from the mart (portable, driver-free) or a live warehouse connection with custom SQL. **Targeting Tableau Public means an extract** - it is extract-only and cannot open a live connection, so use `extract=True` and ship a `.twbx`. Tableau Desktop needs neither. **One grain per workbook.** Most broken Tableau dashboards are a grain problem wearing a chart's clothing - if revenue is monthly and tickets are per-ticket, you cannot put both in one flat extract without duplicating one of them.

5. **Write the spec, not the XML.** You author a Python dict and `scripts/twb_builder.py` emits schema-correct XML. A worksheet is 150-250 lines of order-sensitive boilerplate; the builder owns that so you don't. The spec format is `references/workbook-spec.md`; the six chart recipes are `references/chart-recipes.md`. Chart choice, colour, layout, and decluttering come from `standards/dashboard-standards.md` - that file is the single source of truth for design and this skill does not restate or override it.

6. **Ship a build script, not a workbook.** Every dashboard folder gets a `build.py` that regenerates both the extract and the `.twb` from source. A workbook someone once saved is not reproducible; a script that rebuilds it is (`CLAUDE.md` principle 3).

7. **Validate before anyone opens it.** Run the checker:
   ```bash
   python .claude/skills/tableau/scripts/validate_twb.py dashboards/<name>
   ```
   Fix every ERROR. Triage WARNs, don't ignore them. For anything stakeholder-facing, hand off to `tableau-validator` for an independent pass.

8. **Reconcile, then ship.** Open the workbook in Tableau Desktop or Tableau Public and confirm it renders - **validation proves the files are well-formed, only Tableau proves the dashboard works.** Cross-check every displayed number against an independent direct query, saved in `dashboards/<name>/checks/`. Screenshot into `dashboards/<name>/`, update the `dashboards/README.md` inventory. Publishing to Server/Cloud for a broad audience -> confirm with the user first.

9. **Record what you learned.** New source quirks -> `knowledge/data-sources.md`. Methodological choices (exclusions, LOD semantics, fiscal handling) -> `knowledge/decision-log.md`. Anything materially off-trend you noticed while reconciling -> the Observations section there too.

## Hard rules

- **XSD-valid does not mean it opens.** Tableau says so directly: the schemas do not cover "connection attributes, calculated field contents, and references to workbook elements". The validator's semantic layer covers much of that gap, but a human opening the file is still the last gate. Never report a dashboard as working because validation passed.
- **Write every file as UTF-8 without BOM, with LF endings.** On Windows, PowerShell's `Set-Content`, `Out-File`, and `>` all add a BOM. Write from Python with `encoding="utf-8", newline="\n"` - `write_twb()` already does.
- **Never hand-edit a `.twbx`.** It is a zip archive, and the official schema explicitly does not cover packaged workbooks. Work the `.twb` and ship the data alongside it.
- **Never invent a metric definition in a calculated field.** Calculated fields are for presentation logic. A metric defined in a workbook is invisible to the catalog and to every other workbook, which is exactly how two dashboards start disagreeing. Route conflicts to `metrics-steward`.
- **Never edit the vendored XSD** in `schemas/`. It stays byte-identical to upstream so `/upgrade` can diff it against a new Tableau release. The two shim files beside it are ours and are documented in place.
- **Close Tableau before regenerating a workbook it has open.** It does not watch the filesystem and will overwrite your rebuild from its in-memory copy on the next save.

---

> Created by Colin Beck — https://www.linkedin.com/in/beckcolin/
