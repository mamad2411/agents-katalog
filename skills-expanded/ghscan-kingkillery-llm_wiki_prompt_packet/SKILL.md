---
description: create, refine, review, or retire reusable skills at expert level
---
Read `CLAUDE.md`, then read `LLM_WIKI_MEMORY.md` if present, `SKILL_CREATION_AT_EXPERT_LEVEL.md` if present, `.llm-wiki/config.json`, `wiki/index.md`, `wiki/skills/index.md`, and recent `wiki/log.md`.

Create or update a reusable skill from the current task, trajectory, or evidence:
- if the local skill MCP server is available, call `skill_lookup` before exploring
- for long tasks or expensive exploration, call `skill_reflect` or `skill_pipeline_run` first so the important context is captured as a reducer packet plus artifact refs
- call `skill_validate` before direct save when the candidate is non-trivial, likely duplicated, or needs explicit review
- use `skill_propose`, `skill_feedback`, or `skill_retire` for lifecycle operations
- search for existing related skills first
- write or update the skill page under `wiki/skills/active/`
- append reasoned review notes under `wiki/skills/feedback/` when the task is feedback-driven
- retire the skill into `wiki/skills/retired/` when evidence shows it is unsafe or the score should fall below the retirement threshold
- update `wiki/skills/index.md`
- append a `skill` entry to `wiki/log.md`

Skill requirements:
- optimize for learn-once, reuse-forever shortcuts
- include trigger, preconditions, fast path, failure modes, and evidence
- run a privacy gate before saving
- validate duplicates before saving, and merge deltas when overlap is strong
- for long tasks, capture a strong middle-manager reducer packet with an explicit `route_decision`
- prefer a 1-3 call reusable recipe over verbose narrative
- mark HTTP upgrade candidates explicitly, but do not claim them without evidence

Routing:
- use `pk-qmd` for repo-local evidence retrieval and prior skill lookup
- use `pk-qmd` first when the right prompt, note, file, or skill page is not known yet
- use `GitVizz` when repo topology or API context sharpens the reusable recipe
- use `brv` only for durable user or workflow preferences that materially affect the skill
- if `pk-qmd` and `brv` conflict, trust current source evidence

Return:
- stack/config used
- files read
- files changed
- what changed
- unresolved questions
