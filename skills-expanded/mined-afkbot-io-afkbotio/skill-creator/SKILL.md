---
name: skill-creator
description: "Profile skill management via `skill.profile.*` and `skill.marketplace.*`. Use when listing, inspecting, creating, editing, deleting, or installing custom skills. Every skill must keep `name` and `description` in YAML frontmatter because AgentLoop summaries are built from that metadata."
aliases: skill-manager, skills-manager, skill-profile
triggers:
  - skill marketplace
  - marketplace skills
  - install skill
  - list skills
  - search skills
  - маркетплейс скиллов
  - маркет плейс скиллов
  - маркет плейс навыков
  - установи скилл
  - список скиллов
  - список навыков
  - какие навыки есть
  - покажи навыки
  - найди скилл
tool_names:
  - skill.profile.list
  - skill.profile.get
  - skill.profile.upsert
  - skill.profile.delete
  - skill.marketplace.list
  - skill.marketplace.search
  - skill.marketplace.install
preferred_tool_order:
  - skill.profile.list
  - skill.marketplace.list
  - skill.marketplace.search
  - skill.marketplace.install
  - skill.profile.upsert
  - skill.profile.delete
---
# skill-creator

Purpose: manage profile-local skills stored as markdown files under `profiles/<profile_id>/skills/<name>/SKILL.md`.

## Workflow
1. Always inspect skills first with `skill.profile.list`, `scope=all`.
   - For generic requests like "какие навыки есть" or "покажи навыки", never use `scope=profile` unless the user explicitly asked for only profile-local skills.
2. Before create/edit/delete, return a short summary of existing skills from list payload:
   - `name`
   - `summary`
3. If user asks to inspect one skill, call `skill.profile.get`.
4. If user asks to create or edit a skill, call `skill.profile.upsert` with:
   - `name`: normalized slug that matches `^[a-z0-9][a-z0-9-]*$`.
   - `markdown`: complete skill body in markdown.
5. If user asks to remove a skill, call `skill.profile.delete`.
6. If user asks to browse marketplace skills, call `skill.marketplace.list`.
7. If user asks to search/filter marketplace skills, call `skill.marketplace.search`.
8. If user asks to install a marketplace skill, call `skill.marketplace.install`.

Marketplace defaults:
- If user did not provide a source, use the default curated marketplace source.
- Prefer `skill.marketplace.list` before install when the user asks to browse.
- Prefer `skill.marketplace.search` when the user already provided a query.
- If user names a skill directly, install it without asking for a raw marketplace URL first.

## Rules
- Intent routing:
  - If user says "сделай через скилл", treat it as explicit request to use this workflow.
  - In this case, do not skip the initial `skill.profile.list` + short summary step.
- Use this skill before any direct file operation for custom skills.
- Every created or updated skill must use canonical `SKILL.md` structure with YAML frontmatter at the top.
- Frontmatter must always contain:
  - `name`: the normalized skill slug.
  - `description`: the full trigger description used later in AgentLoop summaries.
- Prefer adding machine-readable routing metadata when the skill orchestrates tools or integrations:
  - `triggers`: extra phrases for implicit routing.
  - `tool_names`: tools that should stay visible when this skill is selected.
  - `app_names`: integration apps allowed for this skill.
  - `preferred_tool_order`: tool order the agent should follow.
  - `requires_env`: runtime env prerequisites, for example `AFKBOT_CREDENTIALS_MASTER_KEYS`.
- Keep `SKILL.md` focused on workflow and routing. When a skill needs larger runnable examples, templates, or implementation helpers, prefer adjacent `scripts/` and `references/` files instead of growing one huge markdown file.
- If a skill uses sibling `scripts/` or `references/`, mention the exact relative paths in `SKILL.md` and keep the markdown concise about when to load them.
- Put the trigger conditions and use cases into `description`, not only into the body.
- Keep the body concise and action-oriented after the frontmatter.
- Keep skill markdown language aligned with user input language.
  - If user wrote in Russian, write markdown in Russian.
  - If user wrote in English, write markdown in English.
  - If user provides markdown text, preserve that language/style unless asked to rewrite.
- Avoid duplicating a skill name when user intent is to edit existing content.
- For destructive changes, restate target skill name before deletion.
- Name normalization is mandatory when user gives non-latin or mixed name:
  - Lowercase input.
  - Transliterate Cyrillic to Latin (`а->a`, `б->b`, `в->v`, `г->g`, `д->d`, `е->e`, `ё->e`, `ж->zh`, `з->z`, `и->i`, `й->y`, `к->k`, `л->l`, `м->m`, `н->n`, `о->o`, `п->p`, `р->r`, `с->s`, `т->t`, `у->u`, `ф->f`, `х->h`, `ц->ts`, `ч->ch`, `ш->sh`, `щ->sch`, `ы->y`, `э->e`, `ю->yu`, `я->ya`, drop `ъ`/`ь`).
  - Replace spaces and `_` with `-`.
  - Remove all chars outside `[a-z0-9-]`.
  - Collapse repeated `-`, trim leading/trailing `-`.
  - Ensure length `1..128`.
  - If already used and user asks to create a new one, append numeric suffix (`-2`, `-3`, ...).
  - Report final slug used in the result text.

## Canonical Skill Template

Use this shape for all created skills:

```md
---
name: example-skill
description: "Short but complete trigger description. Explain what the skill does and when it should be used."
aliases:
  - optional-alias-1
  - optional-alias-2
triggers:
  - optional extra trigger phrase
tool_names:
  - exact.tool
app_names:
  - optional-app
preferred_tool_order:
  - exact.tool
requires_env:
  - OPTIONAL_RUNTIME_ENV
---

# Example Skill

Use this skill when the task matches the description above.

## Workflow
1. Do the first deterministic step.
2. Do the second deterministic step.
3. Return the result in the requested format.

## Rules
- Keep secrets out of normal chat if the skill touches credentials.
- Mention the exact tools, files, or APIs the skill should use.
```

Notes:
- `aliases` is optional.
- `triggers`, `tool_names`, `app_names`, `preferred_tool_order`, and `requires_env` are optional but strongly recommended for tool-using skills.
- Larger skills may also rely on sibling `scripts/` and `references/` directories for progressive disclosure. Keep only the minimum routing/workflow summary in `SKILL.md`.
- AgentLoop skill summaries are derived from `description`, so do not leave it vague.
- If the user provides legacy markdown without frontmatter, rewrite it into this canonical format before saving.
- Runtime routes the correct skill automatically; do not send `skill_name`.
