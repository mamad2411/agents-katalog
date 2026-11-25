---
name: subagent-manager
description: "Profile subagent management via `subagent.profile.*` and `subagent.run`. Use when listing, inspecting, creating, editing, deleting, or executing custom subagents."
---

# subagent-manager

Purpose: manage profile-local subagent descriptors stored as markdown files under `profiles/<profile_id>/subagents/<name>.md`.

## Workflow
1. Always inspect existing profile subagents first with `subagent.profile.list`.
2. Before create/edit/delete, return a short summary of existing subagents from list payload:
   - `name`
   - `summary`
3. If user asks to inspect one subagent, call `subagent.profile.get`.
4. If user asks to create or edit a subagent, call `subagent.profile.upsert` with:
   - `name`: normalized slug that matches `^[a-z0-9][a-z0-9-]*$`.
   - `markdown`: complete subagent definition.
5. If user asks to remove a subagent, call `subagent.profile.delete`.
6. If user asks to execute a subagent, call `subagent.run` and then `subagent.wait` / `subagent.result`.

## Rules
- Intent routing:
  - If user says "сделай через субагента", treat it as explicit request to use this workflow.
  - In this case, do not skip the initial `subagent.profile.list` + short summary step.
- Use this skill before any direct file operation for custom subagents.
- Keep subagent markdown language aligned with user input language.
  - If user wrote in Russian, write markdown in Russian.
  - If user wrote in English, write markdown in English.
  - If user provides markdown text, preserve that language/style unless asked to rewrite.
- Never attempt nested subagent spawning from a running subagent.
- Name normalization is mandatory when user gives non-latin or mixed name:
  - Lowercase input.
  - Transliterate Cyrillic to Latin (`а->a`, `б->b`, `в->v`, `г->g`, `д->d`, `е->e`, `ё->e`, `ж->zh`, `з->z`, `и->i`, `й->y`, `к->k`, `л->l`, `м->m`, `н->n`, `о->o`, `п->p`, `р->r`, `с->s`, `т->t`, `у->u`, `ф->f`, `х->h`, `ц->ts`, `ч->ch`, `ш->sh`, `щ->sch`, `ы->y`, `э->e`, `ю->yu`, `я->ya`, drop `ъ`/`ь`).
  - Replace spaces and `_` with `-`.
  - Remove all chars outside `[a-z0-9-]`.
  - Collapse repeated `-`, trim leading/trailing `-`.
  - Ensure length `1..128`.
  - If already used and user asks to create a new one, append numeric suffix (`-2`, `-3`, ...).
  - Report final slug used in the result text.
- Runtime routes the correct skill automatically; do not send `skill_name`.
