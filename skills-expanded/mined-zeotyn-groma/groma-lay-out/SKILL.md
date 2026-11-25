---
name: groma-lay-out
description: Creates or completes docs/ - vision, concept, architecture, data model, glossary, risks, code style, MADR ADRs - additively during setup; sets up style tools; writes ADRs and doc updates inside a change. Use when a project lacks docs or ADRs, to set up documentation, or after groma-survey.
---

# groma-lay-out

Lay out the project's `docs/` tree: every mandatory slot filled, either by an existing file or by a new one from the templates.

**User language.** Talk to the user in the language of their latest message: questions, summaries, hints, warnings, escalations and the reasons for commands you print. Commands, paths, config keys and ids stay literal. Files you write, the findings report too, keep the language of their templates.

**Writes are additive.** Create a file only when its path does not exist. An existing file that covers a slot fills it; link to it instead of creating a second one. Proposed edits to existing files go into the findings report (`docs/_groma/`), never into the file.

Paths are relative to this skill folder unless they start with `<project>`.

## Inputs

Use whatever is available, in this order: survey results (from groma-survey in this session or the latest `<project>/docs/_groma/findings-*.md`), interview answers, `<project>/.groma/config.yaml`, the code itself. A missing input means more `Not yet documented.` sections, never invented content.

## Steps

1. **Inventory.** List every file under `<project>/docs/` and the root-level docs. Map each to a slot with [references/doc-slots.md](references/doc-slots.md). Done when each of the 9 slots is marked *filled by <path>* or *empty*.

2. **Fill empty slots.** For each empty slot, copy the template from [templates/docs/](templates/docs/) to the groma path and resolve every placeholder (rules in doc-slots.md):
   - vision, concept, glossary: from the interview or existing README; greenfield answers go here.
   - architecture: from the survey's code map, with real paths as evidence and a Mermaid context diagram. If the diagrams skill from the config (for example archify) is installed, offer an interactive diagram in addition.
   - data-model: from the survey's data-model draft, tags kept. No persistent data: `Not applicable: <reason>`.
   - risks: high and medium survey findings that are real risks or debt.
   - code-style: the tools table from the survey's "Code style draft" (brownfield) or from the tools chosen in the interview and set up below (greenfield), one row per tool with the config path linked and the check and fix commands from [references/code-style-tools.md](references/code-style-tools.md); a command the project already runs (`checked` line of `style-drift.sh`, for example `npm run lint`) replaces the table's check command. No tool: "None. Decided in the interview on <date>." whenever the interview asked (declined, or "document only"), "None found." only when no question was asked (update mode). Conventions from the survey draft, tags and paths kept; greenfield: "Not yet documented.". Decisions: links to the style ADRs. `sources`: the config files and the sampled source folders. The rules inside a config file are never copied into the doc. When an existing style guide fills the slot (patterns in doc-slots.md), create no file: link it in the index and put the tools table and the conventions into the findings report as a snippet for that guide.
   Set frontmatter `last_reviewed` to today, `status: draft`, `review_after_days` from `docs.review_after_days` (default 90), and `sources` to the code and config paths the doc describes. Never list other docs or paths inside change folders (`openspec/changes/`): they move on archive. Link the ADR instead.

3. **ADRs.** When `<project>/docs/adr/` has no `0001-*` or `0002-*` and no ADR exists anywhere else, create `0001-record-architecture-decisions.md` and `0002-adopt-groma-docs-structure.md` from `templates/docs/adr/`. When ADRs exist elsewhere, keep them there and number new ones after the highest found. Write `<project>/docs/adr/README.md` if absent, listing **every** ADR (groma's, proposed ones from the survey, and found ones with their path).

4. **Optional docs.** Create each slot listed in `docs.optional` from `templates/docs/optional/` (additive, same rules).

5. **Index.** If `<project>/docs/README.md` is absent, write it from the template: one row per slot pointing at the file that fills it (existing or new), plus one row per other doc found. If it exists, put the missing rows into the findings report as a snippet.

6. **Writing quality.** If `anti-ai-slop-writing` is listed under `skills.writing` and installed, apply its rules to every prose section you wrote.

7. **Verify.** Run `grep -rn "{{" <every file you created>`; it must print nothing. Done when every slot is filled and the list of created files is ready for the caller.

## Style setup

Runs when the interview chose style tools (the `groma` skill passes them), before the code-style slot is filled. Every tool is a row of [references/code-style-tools.md](references/code-style-tools.md).

1. **Config files.** For each chosen tool with a Template: copy `templates/code-style/<template>` to `<project>/<file name of the template>` only when that path does not exist (existing path: the template goes into the findings report as a snippet). Chosen templates that share a target file name (`.editorconfig` from EditorConfig and shfmt) become one new file, concatenated in table order. An empty Template column creates no file; when the tool lives inside an existing build file (Spotless), write the snippet from the table's Notes into the findings report and leave the build file unchanged.
2. **ADRs.** One ADR per chosen tool from [templates/adr-template.md](templates/adr-template.md), numbered after the highest existing ADR: title "Use <Tool> for <role>", `status: accepted` (the user decided in the interview), `evidence: [<config file>]`, the other options from the table as considered options, no `origin` line. Add each to `docs/adr/README.md`.
3. **Installs.** Each non-empty Install command goes through the consent flow of [references/install-consent.md](references/install-consent.md): ask first; on no, refusal or failure write it to `<project>/.groma/install.sh`. Never edit `package.json`, `pyproject.toml` or other manifests yourself; the install command does that after consent.
4. **Report.** Configs created, snippets, ADRs, installs run or pending. "document only" (brownfield default) and "none" skip all four steps; the code-style doc records the decision.

## ADR candidates from a change

Called during a change (by groma-loop, or when the user asks to record its decisions). Run:

```sh
sh scripts/docs-impact.sh --root <project> <change-dir>
```

For each `adr<TAB><change>#D<n><TAB><title>` line, write a new ADR from [templates/adr-template.md](templates/adr-template.md) into `<project>/docs/adr/`, numbered after the highest existing ADR: `status: proposed`, `origin: <change>#D<n>`, considered options from the decision's "Alternatives" paragraph, and `evidence` from the code the change touches. Add it to `docs/adr/README.md` as proposed. Each `impact` line names a doc to update in the change, or to exempt with a task line `Docs: <path> unchanged, because <reason>`. Doc updates and new ADRs here are authored work inside the user's change, like its code; the additive rule above covers setup writes only. Done when the report prints `summary<TAB>impact=0<TAB>adr=0`.

## Report

List created files, slots filled by existing files, and snippets you could not apply because the target existed.
