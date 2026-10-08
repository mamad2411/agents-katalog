---
type: gotcha
context: Writing or reading pipeline JSON files that assign a skill to a task
keywords: [procedure, skill, pipeline json, session field, rename]
---

## What

The pipeline JSON key for assigning a skill to a task was renamed from `"procedure"` to `"skill"`. The corresponding TypeScript session field `session.procedure` was also renamed to `session.skill`.

Old (archived pipelines in `pipelines/done/`):

```json
{ "procedure": "review-arch-skill" }
```

Current:

```json
{ "skill": "review-arch" }
```

## Do

- Use `"skill"` as the key when writing new pipeline JSON files
- Read `session.skill` in TypeScript code when accessing the assigned skill on a session

## Don't

- Don't use `"procedure"` as a key in new pipeline JSON — the runtime reads `"skill"` and will silently ignore `"procedure"`
- Don't reference `session.procedure` in TypeScript — the field no longer exists under that name
