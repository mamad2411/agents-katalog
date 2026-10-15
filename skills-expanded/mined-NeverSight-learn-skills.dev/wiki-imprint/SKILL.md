---
name: wiki-imprint
license: MIT
disable-model-invocation: true
description: Archive a valuable session synthesis as a permanent wiki page in the vault.
argument-hint: "[vault-name]"
---

# wiki-imprint

Start your response with the flavor line `Imprinting reference...`, translated to the language of the user's current message (Spanish: `Archivando referencia...`), with nothing before it. Use that same language for every prompt, question, menu, and confirmation this skill produces — persisted vault content (if any) still follows the vault's locale, not the conversation language.

Archive a valuable session synthesis as a permanent wiki page.

## Steps

1. **Resolve vault** — per `~/.almagest/references/VAULT-RESOLUTION.md`, then its `locale:` per `~/.almagest/references/LOCALE-RESOLUTION.md` (both synced by `/wiki-setup` — if either is missing, run `/wiki-setup` first). If the first argument matches a registered vault name (e.g., `/wiki-imprint personal`), use that vault.

2. **Identify the synthesis** — review the current conversation and identify the main synthesis produced. Apply the source hierarchy (see ## Source hierarchy below) to determine what the synthesis derives from — and whether a `.raw/` primary source needs to be read before writing.

3. **Propose and confirm** — propose the page type, suggested title, and path inside the resolved vault. Wait for confirmation or adjustment before proceeding.

4. **Create the page** — use the corresponding template at `{vault}/templates/{type}.md`, saved to `wiki/concepts/`, `wiki/entities/`, `wiki/sources/`, or `wiki/projects/` (matching the type). For a project design decision, update the project's existing page instead — add the decision under `## Key decisions` rather than creating a new page.

5. **Link, index, and log** — add `[[wikilinks]]` to related existing pages, update `{vault}/wiki/index.md`, and add an entry to `{vault}/wiki/meta/log.md`: `**[YYYY-MM-DD] imprint** | {title}`.

## Source hierarchy

The synthesis must derive from one of these, in order:

1. **Current session** — analysis, decisions, or conclusions produced during this conversation.
2. **`.raw/` primary source** — if the session worked from an ingested source, read the `.raw/` file directly before writing. Do not read the derived `wiki/sources/` page as a substitute.
3. **`wiki/` pages** — reference only. Use them to detect pages to update and to add `[[wikilinks]]`. Never use a wiki page as the input for new synthesis.

**Circular synthesis test:** before writing, ask — "could I justify this content by citing only wiki pages, with no `.raw/` file or session analysis behind it?" If yes, stop — this is circular synthesis, and it amplifies drift instead of grounding knowledge. Trace the claim back to its primary source first; when in doubt, read the `.raw/` file. If no primary source exists, the content may not be ready to imprint.

## Provenance

Create the page using the corresponding template (step 4) — all frontmatter fields come from the template. `sources:` holds only `wiki/...` page links, matching `wiki-ingest` and `wiki-lint`'s schema — leave it empty if the synthesis has no such backing page, never populate it with `.raw/` paths or `conversation {date}`. Populate `raw:` with `.raw/{slug}.md` when the imprint directly synthesizes a specific primary source not yet ingested as a wiki page; leave both `sources:` and `raw:` empty when the content originates purely from session reasoning or decisions with no artifact behind it.

**`confidence` criteria:**
- `high` — conclusion derived from a primary source or exhaustive evidence-based analysis
- `medium` — synthesis from a secondary source, or partial analysis
- `low` — agent inference, unvalidated hypothesis, or second-hand synthesis

## Rules

- The page must be self-contained for a reader with no session context. Verifiable criteria: (1) every acronym and proper name is expanded or defined on first use; (2) every decision includes its justification or the problem it solves; (3) no deictic references without an explicit antecedent ("this", "the previous discussion", "as agreed"); (4) any relevant prior state is described in the page itself, not assumed known. A reviewer must be able to read the page cold and understand it without accessing the session.
- If the page already exists, rewrite the body integrating the new information — do not append "Update" sections or addendum blocks. The result must read as a cohesive document with no visible edit seams.
- Add a changelog line matching the template: `- YYYY-MM-DD: description`
