---
name: configure-agent-guidance
description: Install, update, or remove reusable guidance sections in a global or project AGENTS.md. Use when the user explicitly asks to configure persistent agent guidance, install one of this skill's AGENTS.md templates, choose whether guidance applies across projects or only to the current project, or maintain a previously installed section.
---

# Configure Agent Guidance

Manage reusable `AGENTS.md` sections from [templates](templates/) without scripts or a separate configuration file.

## Choose the section and scope

Discover available sections by listing the Markdown files directly under `templates/`. Read only the template or templates the user selects.

Before writing, determine whether the user wants the selected guidance installed globally or in the current project. If the user has not already made that choice explicit, ask them. Use the Codex home `AGENTS.md` for global guidance: `$CODEX_HOME/AGENTS.md` when `CODEX_HOME` is set, otherwise `~/.codex/AGENTS.md`. Use the repository-root `AGENTS.md` for project guidance.

Inspect the target before changing it. If an `AGENTS.override.md` at the same level would prevent the target `AGENTS.md` from taking effect, explain that conflict and ask the user whether to use the override file or continue with the ordinary file.

## Apply a section

Preserve every part of the target file outside the selected template's `agent-foundry:begin` and `agent-foundry:end` comments.

When both matching boundary comments are absent, append the complete template with a blank line separating it from existing content. Before appending, check for an unmarked section with the same heading; if one exists, ask whether to replace it or leave it unchanged instead of creating a duplicate.

When exactly one matching managed block exists, leave it unchanged if it already matches the template. Otherwise, show the material difference and ask before replacing the block, since the user may have customized it.

Stop without writing if a boundary is missing, duplicated, reversed, or nested incorrectly. Explain the malformed structure so the user can decide how it should be repaired.

For removal, delete only the selected managed block and collapse the blank lines left at its former boundary. Never remove an unmarked section without explicit confirmation.

After a successful change, report the target file and affected section. Remind the user that newly written `AGENTS.md` guidance is normally picked up when a new Codex run or task starts.

After completing the requested operation, compare every well-formed `agent-foundry` managed block identifier in the target with the current template filename stems. If any managed section is no longer provided, leave it unchanged and ask whether the user wants it removed.
