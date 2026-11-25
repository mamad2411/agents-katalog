---
name: feature
description: Create or revise a single Product feature file with a complete user story, Given/When/Then acceptance criteria, and an innovation-vs-implementation classification. Use when adding one feature to Product/Features/, or refining an existing feature, outside a full /innovate run.
allowed-tools: Read, Write, Edit, Glob, AskUserQuestion
---

# /feature — author one feature file (the atom)

You produce or revise exactly one file in `Product/Features/` that conforms to the feature schema. Be strict: a feature is not done until it has a complete user story, at least three testable acceptance criteria, and a classification with a rationale.

## Procedure

1. **Locate the product root.** Find `Product/Features/` from the current directory. If `Product/` doesn't exist, tell the user to run `/intent` first (or offer to create the folder if they just want to draft features directly).

2. **New or revise?**
   - *Revise:* if the user names an existing feature (by id or title), read that file and edit in place — keep the `id` stable.
   - *New:* scan `Features/F*.md`, find the highest `F<NNN>`, assign the next id. Filename = `F<NNN>-<kebab-slug>.md`.

3. **Gather the content.** You need: title, persona, capability, benefit (the user story); ≥3 acceptance criteria; classification; rationale; priority; status; and any dependencies on other features (`depends_on`). If the caller (e.g. `/innovate`) supplied these, use them. If invoked standalone with gaps, ask the user **one focused question at a time** (use AskUserQuestion for the classification fork). Do not invent a user story from nothing — ask.

4. **Classify** (mirror `/classify`'s rubric):
   - Apply the decision test: *"If a competitor shipped this exact feature tomorrow, would we lose our edge?"* → **innovation**. *"Would every competitor's product have this too?"* → **implementation**.
   - Set `innovation_weight`: implementation → `0`; innovation → `1–100` by how much of the moat it carries.
   - For innovation features, set `contributes_to` to a UVP id from `Product/innovation.md` (read it if present). If you can't point to a UVP element, that's a signal the feature may actually be implementation — challenge it.
   - Write a one-sentence `classification_rationale`.

5. **Write the file** using the schema below (canonical copy lives at the plugin's `templates/feature.md`). Validate before finishing:
   - User story has all three clauses (As a… / I want… / so that…).
   - ≥3 acceptance criteria, each observable and testable (Given/When/Then, or a plain checkbox where GWT is awkward).
   - `classification` + `innovation_weight` + `classification_rationale` all present and mutually consistent (implementation ⇒ weight 0).

6. **Refresh the index.** Note that `Product/features-index.md` is now stale; offer to run `/classify` (regenerates the ranked index) or `/product-status`.

## Schema (reproduce exactly)

```markdown
---
id: F00N
title: Short feature name
classification: innovation | implementation
innovation_weight: 0-100        # implementation = 0; innovation = 1-100
classification_rationale: One sentence.
contributes_to: UVP-x           # innovation features only
priority: must | should | could | wont
status: proposed | validated | building | done
risk_retired:
created_by_stage: ideation | innovation | manual
depends_on: [F00X]              # optional, structured — features this builds on
---

## User story
As a **<persona>**, I want **<capability>**, so that **<benefit>**.

## Acceptance criteria
- [ ] **Given** <context>, **when** <action>, **then** <result>.
- [ ] ...
- [ ] ...

## Notes & open questions
- ...
```
