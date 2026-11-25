---
name: groma-survey
description: Read-only survey of an existing repository - code map, docs and ADR harvest, stale docs, data model from migrations, code style and editorconfig drift, findings report. Use for brownfield onboarding, "what is in this repo", missing or outdated docs, or when /groma finds existing code.
---

# groma-survey

Survey an existing project like a surveyor walks a site before anyone builds: measure everything, move nothing.

**User language.** Talk to the user in the language of their latest message: questions, summaries, hints, warnings, escalations and the reasons for commands you print. Commands, paths, config keys and ids stay literal. Files you write, the findings report too, keep the language of their templates.

**Writes are additive.** Create files only at paths that do not exist yet, plus `.groma/` and `docs/_groma/`. Before every write, check the path; if it exists, record a finding instead. Pre-existing files stay byte-identical (the test suite checks this). Tools you run write there too: graphify's output goes to `<project>/.groma/graphify-out/` (step 2).

**Where you cannot ask** (you run as a subagent or headless), never wait for an answer: write the question as a finding marked `unconfirmed`, with what you would have asked and the default you assumed, and go on. This covers the schema dump offer (step 6) and every confirmation in the reference tables.

Paths below are relative to this skill folder unless they start with `<project>`.

**Map first, then targeted reads.** Steps 3 to 8 open only files that the code map (step 2), a reference table or a script output points to, never whole folders. Caps on files opened, per category:

| Category | Cap | Counts |
|---|---|---|
| code map | 15 | manifests, entry points and module files read beyond the map |
| ADRs | 50 | ADR files; read the frontmatter and title only. The highest ADR number comes from the file names of every ADR found, also past the cap |
| docs | 30 | Markdown docs; read the frontmatter and headings only |
| data model | schema and model files: no cap; migrations: 20 | schema and ORM model files (they define the entities) are read in full; migrations, newest first, only for drift |
| code style | 10 per top-level source folder | sampled files (step 7) |

Listing a tree and running a script open no file. At a cap, stop reading that category, mark it `capped` in the report's "Survey scope" and add a finding naming what stayed unread: `medium` for the data model (entities may be missing), `low` otherwise.

## Steps

1. **Detect.** Run `sh scripts/detect.sh <project>` (a copy of groma-detect's script, with its signals table in [references/signals.md](references/signals.md)). Done when you know the languages, manifests and history depth.

2. **Code map.** Use the discovery skill from `.groma/config.yaml` (`skills.discovery`, default graphify):
   - graphify installed: when `<project>/graphify-out/` already exists, read its report. Otherwise run graphify on `<project>` from `<project>/.groma/` as the working directory (graphify writes `graphify-out/` into its working directory), then read `<project>/.groma/graphify-out/GRAPH_REPORT.md` (god nodes, communities).
   - repomix chosen: `npx --yes repomix@1.18.1 --compress --output <project>/.groma/repomix.xml`, then read that file.
   - neither: read the tree, manifests and entry points; mark the code map `degraded`.
   Done when you can name the main modules, their dependencies, entry points and external systems, each with a path as evidence, and know which files each later step will open.

3. **ADR harvest.** Apply every row of [references/adr-sources.md](references/adr-sources.md). Done when every candidate location was checked and each ADR found has path, number, title, status, date.

4. **Docs harvest.** List every Markdown doc outside code folders (README, `docs/`, `doc/`, wiki folders, arc42 folders). Map each to a groma doc slot (vision, concept, architecture, data model, glossary, risks, code style, ADR) using [references/doc-slots.md](references/doc-slots.md).

5. **Freshness.** Run `sh scripts/freshness.sh <project>` (add `--docs <dir>` for docs outside `docs/`). Every `stale` line becomes a finding with its reason (dates, or the open ADR proposal). Every `broken` line becomes a finding with the listed paths and the action "fix `sources` in frontmatter"; a stale reason after `; ` on that line goes into the same finding. Done when every doc from step 4 has fresh, stale, broken or unknown.

6. **Data model.** Apply [references/data-sources.md](references/data-sources.md) top-down. Draft entities and relationships with `EXTRACTED`/`INFERRED` tags and source paths; record every disagreement between levels as drift. No sources and the project has a database: offer the dump script (where you cannot ask: an `unconfirmed` finding), never connect yourself.

7. **Code style.** Run `sh scripts/style-drift.sh <project>`. It reads [references/code-style-tools.md](references/code-style-tools.md) and runs no project tool.
   - Every `tool` line becomes a row of the tools table draft: tool, config path, check command, plus the fix command from the table. When a `checked` line exists for the tool, its command (`npm run lint`, `make lint`, the CI step) replaces the table's check command in the row: the doc shows what the project runs. A `note` line (table missing) becomes a low finding; the draft then says "style tools not detected (code-style-tools.md missing)".
   - Every `drift` line becomes a medium finding "`<property>` drift: <count> files" with the example paths and the action "run the formatter" (or "fix `.editorconfig`" when the code is consistent and the config is wrong).
   - Every `unchecked` line becomes a low finding with the action "add `<check command>` to CI or the scripts".
   - Conventions: for each top-level source folder, sample up to 10 files, preferring the most recently changed (`git log --name-only`). Infer at most 12 conventions in total for file and symbol naming, test location and naming, import style and error handling. Each line cites at least one file path, with a line number where it shows a specific construct. A convention read from configuration (test globs in `jest.config.*`, `pytest.ini`, `pyproject.toml`) is tagged `EXTRACTED`, everything else `INFERRED`. An area without a clear pattern reads "No consistent pattern found."
   - An existing style guide that matches the code-style slot in [references/doc-slots.md](references/doc-slots.md) (`CONTRIBUTING.md` with a style section, `STYLEGUIDE.md`, `docs/conventions.md`, ...) is listed under Docs found as `code-style`.
   Done when the report's "Code style draft" holds the tools table, the conventions and the drift and unchecked findings are in the findings table.

8. **Proposed ADRs.** When step 3 found **no** ADR anywhere, derive the decisions the code already shows: language and runtime, framework, persistence, API style, build and deployment, test approach. Write each as `<project>/docs/adr/NNNN-<kebab-title>.md` from [templates/adr-template.md](templates/adr-template.md) with `status: proposed`, `evidence: [paths]`, no `origin` line and "Derived by groma from existing code; confirm or reject." Numbering starts at 0003 (0001 and 0002 are the groma seed ADRs that groma-lay-out writes); when ADRs exist, propose only decisions that clearly lack one, numbered after the highest found (the report's ADR summary row names it).

9. **Report.** Fill [templates/findings.md](templates/findings.md) for `<project>/docs/_groma/findings-<YYYY-MM-DD>.md` (if taken: `-2`, `-3`, ...): keep its frontmatter, every heading and their order, and replace only the placeholders. A section with nothing to list keeps its table header and says `None found.` below it. Every finding has severity, evidence and one suggested action. Put proposed edits to existing files (for example a pointer line for an existing `CLAUDE.md`) under "Snippets for existing files". "Survey scope" holds one row per read-budget category with the files read. "Hand-off" holds at most ten lines: counts per severity, the top three findings, and what the docs step needs (data model source, existing docs that fill slots, proposed ADRs, the number of `unconfirmed` findings).
   - Inline or standalone: write the report to that path. Done when `sh scripts/report-check.sh <report>` exits 0 (the template's `generated_by` line, every template section with content, no template placeholder left, a hand-off of one to ten lines).
   - As a subagent: do not write the report file (Claude Code refuses report files from subagents, and a refused write repeats the report for nothing); the caller writes your reply's report and runs the check. Done when the report in your reply is the filled template, from its first `---` line to its last section.

## Severity guide

- **high**: no ADRs at all; architecture or data-model doc contradicts the code; data-model drift on a persisted field.
- **medium**: stale doc; mandatory doc missing; ADR without status; ADR proposed for too long; code that disagrees with `.editorconfig`.
- **low**: naming or formatting issues, missing frontmatter, broken `sources` in doc frontmatter, a style tool whose check runs nowhere.

## Hand-off

- As a subagent: reply with `report: <path>` on the first line (the free path from step 9), then the filled report exactly as it goes into the file, and nothing else: no summary before or after it. The caller writes it once, unchanged, and reads only its "Hand-off" section to go on.
- Inline or standalone: return the report path on the first line, then the report's "Hand-off" lines unchanged. When running standalone, also suggest `groma-lay-out` next to create the missing docs from this survey.
