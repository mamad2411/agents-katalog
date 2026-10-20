---
description: Scaffold a new template under templates/ and wire it into CLAUDE.md if needed.
argument-hint: "<template-name>"
when_to_use: Use when the user wants to add a new kind of source that doesn't fit the built-in templates (source-summary, paper-summary, concept, entity, synthesis, output, stub). Typical examples: voice memos, meeting transcripts with distinct structure, interview notes, bookmark collections. Triggered by phrases like "add a new template", "I want a template for X", "create a voice-memo template".
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Wiki New Template

Scaffold a new template file in `templates/` and (if needed) teach `/wiki-ingest` when to use it. Arg (`$ARGUMENTS`): the new template's base name (e.g. `voice-memo-summary`, `meeting-minutes`).

## Step 1 — Validate the name

- Kebab-case, ASCII only, no spaces/underscores/uppercase.
- Must not collide with existing templates: `source-summary`, `paper-summary`, `concept`, `entity`, `synthesis`, `output`, `stub`.
- Suggest the suffix `-summary` if the template describes source material, `-page` if it describes a wiki page type. Optional — user's call.

## Step 2 — Pick the starting point

Ask the user which existing template is closest in shape to what they want:

- `source-summary.md` — for new kinds of source material (articles, transcripts, interviews, notes)
- `paper-summary.md` — for new kinds of structured reference material (academic papers, legal briefs, specifications, standards with page citations)
- `concept.md` — for new kinds of compiled wiki pages about ideas
- `entity.md` — for new kinds of compiled wiki pages about people/orgs/tools

Copy the chosen starter as `templates/{name}.md`.

## Step 3 — Customise together

Walk the user through the frontmatter fields in the copy. For each, ask:

- Does this field apply to the new type? (yes → keep, no → delete)
- Are there new fields unique to this type? (add them with sensible defaults)
- What's the one-line purpose of this template? (update the `summary` comment if present)

Then walk the body sections. Same logic — keep what applies, drop what doesn't, add what's missing.

## Step 4 — Wire it into INGEST (only if this is a source-material template)

If the new template maps to source material (not a wiki-page type), `/wiki-ingest` needs to know when to use it. Three ways to wire this, in order of preference:

1. **By `raw/` subfolder** (cleanest): create `raw/{subfolder}/` and ask the user to drop files there. Update `CLAUDE.md` → INGEST step 2b's template-selection rule with a new line: *"Use `templates/{name}.md` for anything in `raw/{subfolder}/`."*
2. **By filename pattern** (if subfolder split is overkill): add a rule under INGEST step 2b matching the pattern (e.g. "files starting with `meeting-` use `templates/meeting-minutes.md`").
3. **By explicit user-on-ingest** (if the template is rare): skip CLAUDE.md wiring. User will tell Claude which template to use when running `/wiki-ingest` on that file.

Default: ask the user which approach they want. Don't pick silently.

## Step 5 — If creating a new `raw/` subfolder

- `mkdir raw/{subfolder}`
- Touch `raw/{subfolder}/.gitkeep`
- Update `raw/_index.md` with a one-line description of the new subfolder.
- Commit none of this — let the user decide when to commit.

## Guardrails

- Never modify the 7 shipped templates — only create new ones.
- Never duplicate an existing template's name.
- If the user describes a template shape that's >80% identical to an existing one, push back — ask if they actually need a new template or if they just need to use the existing one with different frontmatter values.

## Reporting

- New template path: `templates/{name}.md`
- Starting template used: (source-summary | paper-summary | concept | entity)
- CLAUDE.md wired? (yes/no/deferred)
- New `raw/` subfolder created? (path or n/a)
