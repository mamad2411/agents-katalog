---
name: groma-skills
description: Installs third-party skills the user picks from the groma catalog (design, writing, workflow, diagrams and more). Use during /groma, or when asked which skills to add or to change a project's skills.
---

# groma-skills

Offer the curated [catalog.yaml](catalog.yaml) one category at a time, record the picks, install them project-scoped for every configured agent.

**User language.** Talk to the user in the language of their latest message: questions, summaries, hints, warnings, escalations and the reasons for commands you print. Commands, paths, config keys and ids stay literal. Files you write, the findings report too, keep the language of their templates.

## Steps

1. **Load.** Read `catalog.yaml` and `<project>/.groma/config.yaml` (`agents`, `project.has_ui`, `skills`, `workflow`). Missing config: ask which agents the project uses (claude, copilot, gemini, cursor, codex) and whether it has a UI.

2. **Choose.** For each category in catalog order:
   - `condition: has_ui` and the project has no UI: record `none`, say "design: skipped, no UI".
   - Already answered in the config and the user did not ask to reconfigure: keep it.
   - Otherwise ask once, recommended option first, one line per option from its `description`:
     ```
     Writing style (pick any):
       ▸ anti-ai-slop-writing (recommended): human-sounding text, bans typical AI phrases
       ▸ i-have-adhd (recommended): action-first answers, one next action
         none
     ```
     `select: multi` accepts several picks; `select: single` exactly one.
   Done when every category has a recorded value.

3. **Record.** Write picks to `<project>/.groma/config.yaml`: `skills.<category>` for each category, the `workflow` category as top-level `workflow`. Then run `sh scripts/validate-config.sh <project>/.groma/config.yaml --catalog catalog.yaml`; fix every reported error.

4. **Install.** For each picked skill, build the commands for every configured agent from the templates in [agents.yaml](agents.yaml), following [references/install.md](references/install.md). Ask before an installer touches an existing file or installs outside the project. Run them; on refusal, missing permission or failure, write `.groma/install.sh` instead. Done when every pick is installed or listed in `.groma/install.sh`.

5. **Report.** Per skill: installed for which agents, or pending in `.groma/install.sh`, plus any `post_install` command the user must run inside the agent. Add the same list, with every command that ran or is pending, as a section `## Installs` to the current findings report (`<project>/docs/_groma/findings-<date>.md`; when this run has none, create it with the title `# groma findings, <date>` and that one section).

## Notes

- Skill repos change. When an install fails on the pinned `ref`, report it; do not switch to an unpinned version silently.
- Users can add their own entries to `catalog.yaml` in a fork; the validator checks them.
