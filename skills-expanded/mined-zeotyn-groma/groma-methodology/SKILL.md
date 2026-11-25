---
name: groma-methodology
description: Sets up a spec methodology (OpenSpec, Spec Kit, BMAD, GSD) and the m/c/f/s/r change naming with next-id and roadmap scripts. Use during /groma, when choosing or adding a methodology, or when creating, naming or checking changes and milestones.
---

# groma-methodology

Set up one spec methodology and the change naming convention. `docs/` stays the product truth; the methodology holds change work and points at `docs/`.

**User language.** Talk to the user in the language of their latest message: questions, summaries, hints, warnings, escalations and the reasons for commands you print. Commands, paths, config keys and ids stay literal. Files you write, the findings report too, keep the language of their templates.

## Steps

1. **Choose.** Use `methodology` from `<project>/.groma/config.yaml`. Not set: ask, recommended first:
   ```
   Spec methodology?
     ▸ openspec (recommended): light, change folders, built for existing code
       spec-kit: constitution and phase gates, good for teams
       bmad: full agile roles (PO, architect, ...)
       gsd: phases with fresh subagents per step
       none
   ```

2. **Initialize.** Read the chosen recipe in [methodologies.yaml](methodologies.yaml) and apply it as [references/methodologies.md](references/methodologies.md) describes: skip when already present, check prerequisites (`sh scripts/check-prereqs.sh`), ask before the init touches existing files, run the init command. On missing tools, refusal or failure: add the command to `<project>/.groma/install.sh`, mark `steps.methodology: pending` in the config, and continue.
   Done when the methodology folder exists or its command is pending in `.groma/install.sh`.

3. **Link to docs.** Append the recipe's `docs_link.append` to `docs_link.file`, only when this run created that file. For files that existed before, put the text into the findings report as a snippet.

4. **Convention.** Write `conventions.changes` into the config if missing (defaults in [references/conventions.md](references/conventions.md)). If the changes folder already holds changes, write their names to `<project>/.groma/conventions-baseline.txt` (only if that file is absent; a project that used the old `<type><NNN>-<slug>` names: follow "Migration" in [references/conventions.md](references/conventions.md) instead). Run `sh scripts/check-conventions.sh --root <project>`; it must print `conventions: ok`.

5. **Report.** Methodology state (initialized, already present, pending), where changes live, and how to create the next one:
   ```
   Next change id: sh <this skill>/scripts/next-change-id.sh c --root .
   ```

## Creating a change later

When the user asks for a new change, fix, spike or refactor in a groma project:

- **Outside a milestone:** get the id from `scripts/next-change-id.sh <type>` (`c`, `f`, `s`, `r`) and name the change `<id>-<slug>`, e.g. `c4-export-csv`.
- **Inside milestone N:** name it `m<N>-<slug>`; a spike, fix or refactor carries its type word: `m<N>-spike-<slug>`, `m<N>-fix-<slug>`, `m<N>-refactor-<slug>`. No id is needed. Then run `scripts/roadmap.sh --root <project>`, and again after archiving the change.
- **Spikes and refactors** (`s`, `r`, `m<N>-spike-`, `m<N>-refactor-`) carry no spec deltas: in OpenSpec add `skip_specs: true` to `.openspec.yaml`.
- A requested name in another form (`C004-Export`) becomes `c4-export`; tell the user. `d` is no type: docs belong to the change that causes them.

When the user plans a new milestone: it is not a change. Get its number from `scripts/next-change-id.sh m` and add a section from [templates/roadmap-section.md](templates/roadmap-section.md) to `<project>/docs/roadmap.md`. Create the file with a `# Roadmap` heading when it is missing; when it exists and groma did not write it, show the section and ask before adding it.
