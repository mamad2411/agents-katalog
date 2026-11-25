---
name: setup-workspace
description: Personalize this starter workspace. Interviews the user about their company, product, users, and preferences, then fills in CLAUDE.md and the context files and renames the example project. Use on first launch, or whenever the user wants to re-run onboarding.
---

# Setup workspace

Turn the template files into the user's own workspace through a short interview. The user answers in plain language; you do all the writing.

## How to run the interview

- Ask in rounds, one topic at a time, in this order: company, product, users, working and writing preferences, current projects. A few questions per round, not a wall of them.
- Plain questions a busy person can answer from memory: "What does your company sell, and to whom?", "Who do you picture when you make product decisions?", "What's a correction you find yourself giving on every AI draft?"
- Accept short answers and draft from them. Show what you wrote and ask for a yes or a fix before moving to the next topic. The user's words beat template language; keep their phrasing where it's clear.
- Skipping is fine. If the user doesn't know or doesn't care about a section, leave the template placeholder in place and move on. An honest placeholder beats invented content.

## What to fill

1. `CLAUDE.md` — replace the first line with who the user actually is (role, company). Keep the file short; it's a map, not a manual.
2. `context/company.md` — what the company does, how it's organized, competitors, vocabulary.
3. `context/product.md` — what the product is, positioning, current strategy, key metrics (names and where they live, not live numbers).
4. `context/users.md` — segments, primary persona, strongest findings.
5. `context/preferences.md` — writing preferences and working preferences in the user's own words. Replace the template examples with theirs; delete examples they don't want.
6. `projects/example-project/` — ask for the user's most active real project. Rename the folder to a short slug of it, fill `brief.md` from what they tell you, and seed `tasks.md` with their current next steps. If they'd rather start empty, leave the example in place.

## Finish

Show a short summary of every file you touched. Then suggest one concrete next move: give the workspace a real task, for example `/status-update` or a first draft the user owes someone. Remind them once: when they correct something you got wrong, `/file-feedback` makes the correction permanent.
