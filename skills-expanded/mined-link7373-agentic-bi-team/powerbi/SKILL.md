---
name: powerbi
description: Build and edit Power BI dashboards as code via PBIP projects — semantic model in TMDL, report pages and visuals in PBIR, theme JSON, deterministic validation, and publishing. Use when the team's BI tool is Power BI and a dashboard, measure, or model needs building, fixing, or reviewing.
---

# Power BI — PBIP Authoring & Validation

Owner: `dashboard-developer`, with `powerbi-validator` for the validation gate and `analytics-engineer` for the data layer. Args describe the work, e.g. `/powerbi build the exec revenue dashboard`.

A PBIP project is plain text — TMDL for the model, JSON for the report. That makes a Power BI dashboard an ordinary code artifact: spec'd, built, diffed, reviewed, and version-controlled like everything else the team ships. Work it as code, not as a GUI you can't reach.

## Procedure

1. **Check this is the right path.** This skill applies when `{{BI_TOOL}}` is Power BI, or the user explicitly asked for Power BI. If the team's tool is Tableau, Looker, Excel, or nothing yet, stop and return to `/build-dashboard` — none of the guidance below transfers. If `{{BI_TOOL}}` is still an unfilled placeholder, ask which tool the team uses before building anything.

2. **Detect what you can actually do.** Read `references/tooling-tiers.md` and run the detection commands. State the tier you're working in before you start — it determines whether you can bulk-format, publish, or only author files. Never install anything yourself; recommend, and say what the licence costs are, then let the user decide.

3. **Spec before building.** Do not re-derive the requirements here — `/build-dashboard` steps 1–4 own the audience, the 1–3 questions, the metrics (which must already exist in `knowledge/metrics-catalog.md`), the filters, and the layout sketch. This skill owns implementation only. If there's no `dashboards/<name>/SPEC.md` yet, go write one first.

4. **Build the model layer.** Star schema, one dedicated date table, marts as the source — no heavy transformation inside Power BI (`standards/powerbi-standards.md`). Author TMDL per `references/semantic-model-tmdl.md`; write measures per `references/dax-patterns.md`, named **exactly** as `knowledge/metrics-catalog.md` names them. A measure whose name or logic drifts from the catalog is a defect, not a variation — route conflicts to `metrics-steward`.

5. **Build the report layer.** Pages and visuals per `references/pbir-visuals.md`. Chart choice, colour, layout, and decluttering come from `standards/dashboard-standards.md` — that file is the single source of truth for design and this skill does not restate or override it. Name every page and visual folder in `[A-Za-z0-9_-]` only; anything else is silently discarded by Desktop (`references/gotchas.md`).

6. **Set the theme once.** Encode the palette, semantic status colours, and typography in a theme file rather than formatting visuals individually (`references/theme-json.md`). Theme-first is what makes the design standard hold across every page without hand-editing each visual — and what makes a rebrand a one-file change.

7. **Validate before anyone opens it.** Run the checker:
   ```bash
   python .claude/skills/powerbi/scripts/validate_pbip.py dashboards/<name>
   ```
   Fix every ERROR — those either block Desktop from opening or cause pages and visuals to vanish silently. Triage WARNs, don't ignore them. At Tier 2+, also run `pbir validate`. For anything stakeholder-facing, hand off to `powerbi-validator` for an independent pass.

8. **Reconcile, then ship.** Open the project in Power BI Desktop and confirm it renders — validation proves the files are well-formed, only Desktop proves the report works. Cross-check every displayed number against an independent direct query, saved in `dashboards/<name>/checks/`. Screenshot into `dashboards/<name>/`, update the `dashboards/README.md` inventory. Publishing to a broad or external audience → confirm with the user first (`references/publishing.md`).

9. **Record what you learned.** New model quirks or source oddities → `knowledge/data-sources.md`. Methodological choices (exclusions, measure semantics, fiscal handling) → `knowledge/decision-log.md`. Anything materially off-trend you noticed while reconciling → the Observations section there too.

## Hard rules

- **Write every file as UTF-8 without BOM.** A BOM anywhere in the project — including the gitignored `.pbi/localSettings.json` — stops Desktop opening it entirely. On Windows, `Set-Content -Encoding utf8`, `Out-File`, and `>` in PowerShell 5.1 all add one; write from Python with `encoding="utf-8"` instead.
- **Never hand-edit a `.pbix`.** It is a binary. Convert to PBIP, or work through Desktop.
- **Never generate a `.platform` file.** Its `logicalId` is assigned by Fabric; a hand-written one corrupts the Git link. Missing is a warning, not something to fix.
- **Never rewrite a DAX measure silently.** Surface the change and the reason.
- **Restart Desktop after external edits.** It does not watch the filesystem and will overwrite your work from its in-memory copy.

---

> Created by Colin Beck — https://www.linkedin.com/in/beckcolin/
