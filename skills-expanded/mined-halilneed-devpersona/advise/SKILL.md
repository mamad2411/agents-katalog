---
name: advise
description: Turn the persona profile built from local coding-agent history into concrete suggestions — new agent skills worth authoring, coding-habit improvements, and architecture recommendations. Use when the user asks what skills they should create, how to improve their workflow, prompts, or code habits, says "suggest skills for me", "bana skill öner", "ne geliştirmeliyim", "önerilerin neler", or runs /devpersona:advise, optionally with a focus argument (skills | code | architecture). Requires a persona card from devpersona:analyze and builds it first if missing. Not for the profile itself — that is devpersona:analyze.
---

# Persona-based suggestions

Convert the persona card into actionable advice. Ground every suggestion in
observed evidence — cite the number, memory file, or pattern it comes from.
A suggestion without evidence does not go in the report.

**Language rule: write every user-facing output in the language the user is speaking with you.**

## Step 0 — Load the persona

Read `~/.claude/persona/persona.md` and `~/.claude/persona/stats.json`.
If either is missing or `stats.json` is older than 7 days, first run the full
procedure in the `analyze` skill of this plugin, then continue.

If the user passed an argument (`skills`, `code`, or `architecture`), produce only
that section. Otherwise produce all three.

## Section 1 — Skill suggestions

Find **repeated manual routines** in the evidence and propose turning each into a
agent skill. Sources of repetition:

- `commands` counts (e.g. `dotnet test` appearing 40× across projects → a test-run-and-triage skill)
- session titles that describe the same task type again and again
- memory files that record the same kind of gotcha repeatedly
- prompt samples where the user types near-identical instructions

For each suggestion (max 4, ranked by observed frequency) give a ready-to-use draft:

```markdown
### <n>. <skill-name> — seen <N>× in <evidence>
---
name: <kebab-case>
description: <What it does>. Use when <concrete triggers the user actually types>.
---
<5–10 line body sketch: the steps the skill would encode>
```

Point the user at the official docs (https://code.claude.com/docs) for where to put
the skill (`~/.claude/skills/<name>/SKILL.md` for personal use).

## Section 2 — Coding-habit suggestions

Derive 2–4 suggestions from patterns like:

- high `errors / toolCalls` ratio in a project → what kind of errors repeat (check
  prompt samples and memory files for the cause) and what habit would prevent them
- `denials` count → friction with permissions worth configuring away
- test-related commands rare or absent while build commands are frequent
- very long sessions (`largestSessions`) → suggest checkpoint/commit habits
- one-sided tool usage (e.g. no Grep/Glob, everything by manual paths)

Each suggestion: **observation (with number) → why it costs something → the new habit.**

## Section 3 — Architecture suggestions

From `languages`, `commands`, and memory files, infer the stacks actually in use and
give 2–3 recommendations at the architecture level: recurring structural pain visible
in the evidence (e.g. migrations breaking, dual environments, config drift),
patterns that fit the observed stack, and one "next investment" the history justifies.

Do not recommend technologies the evidence doesn't touch. If the history shows too
little architectural signal, say so honestly instead of padding.

## Closing

End with a short "start here" line naming the single highest-value suggestion,
and remind the user the analysis was fully local.
