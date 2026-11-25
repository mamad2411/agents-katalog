---
name: init-edu
description: Set up a learning project and student profile, preserving existing project instructions and settings. Run explicitly to onboard or update preferences.
disable-model-invocation: true
---

# Initialize Educational Environment

Before accessing education data, read `${CLAUDE_PLUGIN_ROOT}/references/education-data.md`. Resolve `<education-db>` using that contract. Current session ID: `${CLAUDE_SESSION_ID}`.

## 1. Inspect before changing files

Keep setup focused on learning. Use Claude Code's available file tools and host shell for setup and data operations. Do not ask the student to install jq, Python, packages, or a new shell, edit PATH, or run terminal diagnostics. Do not install tools automatically.

Hook reminders are an optional reinforcement of the project teaching instructions. Do not run `hooks/check-runtime.sh` as a required onboarding step, make lessons conditional on it, or label the student as being in "manual mode". That read-only check is available for requested troubleshooting when Bash is already usable. Never claim that hooks are active unless verified. A real file-access or save failure must still be explained plainly; do not hide it or weaken the data contract to finish setup.

Read the project `CLAUDE.md`, `.claude/CLAUDE.md`, `.claude/settings.json`, `.claude/claude-teacher.json`, and existing `<education-db>/student.json` and `dashboard.json`, when present.

- Preserve all unrelated instructions, settings, hooks, and student work. If a JSON file is invalid, report it and recover it before updating.
- Do not write setup files until the student has supplied the required onboarding and project answers. Honor supplied answers; do not ask again.
- If a profile exists, greet the student and ask whether to set up this project using it or update selected profile fields. Never delete the profile to edit it.
- If they want a full reset, direct them to `/claude-teacher:reset-edu`. Do not invoke or reproduce that manual-only skill automatically.

## 2. Onboard a new student

Ask only what is missing, one question at a time:

1. What would you like to learn or build?
2. Have you tried it before, or are you starting from scratch?

Accept "not sure" and choose a gentle introductory lesson. If the student already supplied the topic and level, proceed to setup. Default to clear, friendly explanations and examples; adapt from their responses.

Personalization is optional and can happen during later lessons or on repeat setup: preferred name, age, known subjects, learning preferences, frustrations, goals, interests, and ideal teacher style. Do not delay the first lesson for a questionnaire. Do not infer an age from the plugin's audience. Save unknown values as `null` or empty arrays and record only preferences the student actually supplied.

Save an object in `<education-db>/student.json` using the supplied information:

```json
{
  "name": null,
  "age": null,
  "level": null,
  "known_subjects": [],
  "learning_style": [],
  "frustrations": [],
  "goals": [],
  "interests": [],
  "teacher_persona": null
}
```

Use a number for an age supplied by the student and real `YYYY-MM-DD` dates for known deadlines. Adapt tone to their expressed preferences first. Store the personal profile in the global DB; do not copy personal information into a shared project file without their request.

## 3. Choose the project focus

Use the topic supplied above. Choose the learning type from the student's stated task; use `mixed` if it is unclear. Ask a follow-up only when it would change the first lesson:

- `project`: building something
- `subject`: studying a subject or field
- `exam-prep`: preparing for an exam, interview, or certification
- `mixed`: a mix or not sure yet

## 4. Initialize storage and the project marker

Create missing `<education-db>/{docs,topics,quizzes,sessions}`, project `.claude/`, and project `docs/` directories. Use quoted resolved paths, not a literal `<education-db>` shell token.

Merge `.claude/claude-teacher.json`, preserving unknown fields:

```json
{
  "schema_version": 1,
  "enabled": true,
  "learning_type": "subject",
  "topic": "the chosen topic",
  "initialized": "YYYY-MM-DD"
}
```

Keep the original `initialized` date on repeat setup. This marker activates hooks only in this project. Setting `enabled: false` pauses hook reminders.

## 5. Merge settings and migrate only owned hooks

If `.claude/settings.json` has no `outputStyle`, add `"outputStyle": "Explanatory"`. Preserve an existing output style and every other setting. Never add project hook registrations: the plugin already ships them.

For installations from 1.8.0 or earlier, inspect each handler in the existing `hooks` object. Remove a handler only when its command or args clearly reference this plugin's cache directory **and** one of these scripts:

- `session-start-load-db.sh`
- `inject-teach-context.sh`
- `stop-save-progress.sh`
- `post-code-review.sh`
- `post-quiz-motivate.sh`

Preserve other handlers in the same group, other groups/events, and all non-hook settings. Remove a group/event only if it became empty from removing owned handlers. Never remove the entire `hooks` block wholesale. Leave ambiguous entries unchanged and explain them.

## 6. Merge project instructions

Read `${CLAUDE_SKILL_DIR}/references/project-context.md`. Adapt it to the chosen type/topic and write it inside these exact markers in project `CLAUDE.md`:

```markdown
<!-- claude-teacher:start -->
[adapted project-context content]
<!-- claude-teacher:end -->
```

- If the file is absent, create it with that block.
- If one complete block exists, replace only that block. Preserve everything outside it byte-for-byte.
- If no block exists, append one after the existing content. For legacy teaching instructions, identify the old teaching section and merge without duplicating or removing unrelated guidance.
- If markers are duplicated or unbalanced, do not guess at a replacement boundary; report the ambiguity first.
- Respect project rules outside the block. The plugin's own developer guide is not runtime tutoring context.
- Always include the template's lesson-start, checkpoint, and lesson-ending instructions. They apply whether or not hooks run. On repeat setup, replace earlier plugin-owned "manual mode" notes inside the managed block with these instructions; preserve unrelated notes and real unresolved data-access problems.

## 7. Initialize the dashboard without resetting history

For a new DB, create `<education-db>/dashboard.json`:

```json
{
  "last_session": "YYYY-MM-DD",
  "current_topic": "the chosen topic",
  "total_quizzes": 0,
  "average_score": 0,
  "stats": {"new": 0, "weak": 0, "learned": 0, "solid": 0},
  "topics": {}
}
```

For an existing DB, merge only `last_session` and `current_topic`; preserve records and recalculate aggregates if necessary. Do not create a topic as learned merely because it was selected for study.

If project `memory/knowledge_gaps.md` already exists, preserve it and sync known states from the global DB. Do not create or overwrite an auto-memory index; this legacy mirror is optional.

Append one `session_start` setup event with a unique `event_id`, current time, `${CLAUDE_SESSION_ID}`, project path, topic, and learning type. Do not duplicate the event when retrying a save.

## 8. Confirm actual changes

Briefly confirm the topic and the first learning step. Explain that progress is kept in local files and that the student can say "save this" or "I'm done for today". Keep command lists and file inventories out of the normal welcome; provide exact paths or changes when requested or needed to resolve a problem. Mention unresolved data-access or migration issues clearly. Do not claim hooks saved data, settings loaded, or progress was saved unless verified.

Start the first learning step. Slash commands remain available as shortcuts, but the student does not need to learn them. If newly installed plugin components are not loaded, help reload them or restart Claude Code.
