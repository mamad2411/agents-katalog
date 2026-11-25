---
name: context-md
description: Seed a CONTEXT.md glossary for a repo that already has code, by mining its own vocabulary. Use for "bootstrap a glossary", "this repo needs a CONTEXT.md", "seed the domain model".
disable-model-invocation: true
---

# Seed a CONTEXT.md

`/domain-modeling` writes `CONTEXT.md` lazily, one term at a time, as a design session settles them. That works from day one and does nothing for a repo with 40,000 lines and no glossary. This skill seeds one from the vocabulary the repo already uses, then hands maintenance back.

## The one failure that matters

A glossary of terms Claude would use is worse than no glossary. It reads plausible, it gets loaded into every session, and it quietly teaches the agent a second vocabulary that nobody on the project speaks. Every rule below exists to stop that.

**Every entry is sourced.** A term earns a row only with a citation to where the repo already uses it: a file path, an identifier, a memory-file line. No citation, no row. If you find yourself writing a definition before finding a use, delete it.

## 1. Mine

Run all of these before writing anything.

- **Identifiers.** The nouns in exported function, type, table and module names, ranked by how often they appear across files. A word used in three modules is domain language; a word used once is a local variable.
- **Directory names.** `src/<name>/` is usually a domain term someone already committed to.
- **The project memory file.** `~/.claude/projects/C--Users-skf-s/memory/project_<repo>.md` holds the words Keith uses in prose. These outrank the code when the two disagree: the glossary records what the humans say.
- **README and existing docs.** The terms already explained to a reader.
- **Recent commit subjects.** `git log --format=%s -200`, for what the work is currently called.

## 2. Find the collisions

The mining pass gives a word list. The value is in the disagreements, so look for them explicitly:

- **One thing, two words.** Code says `entry`, memory says `memory`, README says `note`. Pick one and record which the others map to.
- **One word, two things.** `session` as the agent conversation and `session` as the DB row. Both keep a name; neither keeps the bare word.
- **Code disagrees with prose.** The memory file says the store decays entries; the code has no decay path. That is not a glossary entry, it is a question. Ask it.

## 3. Draft, cap, show

Cap the first pass at **15 terms**. A repo does not have 60 domain words, and a long glossary is not read. Take the terms that appear in the most places and carry the most collision.

Use the format in `~/.claude/skills/domain-modeling/CONTEXT-FORMAT.md`. Glossary only: no implementation detail, no architecture, no roadmap, no spec. If a line explains how something works rather than what it is called, it belongs in `ARCHITECTURE.md`.

Show Keith the draft as a table (term, definition, where it came from, what it replaces), then write the file in the same turn. He owns the words; you found the candidates. Terms he rejects afterwards are dropped, not renamed.

## 4. Write and hand off

Write `CONTEXT.md` at the repo root and commit it alone, so the diff is reviewable.

Then stop maintaining it here. Every later change goes through `/domain-modeling`, which updates it inline the moment a term settles. Do not re-run this skill on a repo that already has a `CONTEXT.md`: a second seeding pass overwrites settled human decisions with fresh guesses, which is the failure at the top of this file wearing a different hat.

Where a term surfaced a decision that is hard to reverse, surprising without context, and a real trade-off, offer one ADR under `docs/adr/`. All three tests, or no ADR.
