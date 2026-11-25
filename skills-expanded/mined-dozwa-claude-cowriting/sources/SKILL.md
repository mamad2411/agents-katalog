---
name: sources
description: Literature help: search papers, check the author's Zotero library and Obsidian notes, verify DOIs, write marked source notes. Use when the author needs sources or wants citations checked.
---

# Sources

Depending on the request:

- **Find literature**: use a connected paper-search tool (e.g. Consensus) or web search. Report each hit as `Authors (Year). Title. Venue. DOI/URL` plus 1–2 lines "AI summary – read the original". Never present a reference you did not see in a tool result.
- **Check the library**: `python3 "${CLAUDE_PLUGIN_ROOT}/tools/zotero_search.py" "<query>"` searches the running Zotero (local API) or falls back to the bibliography files under `literature/` (BibTeX, CSL JSON, RIS, PubMed `.nbib`). Tell the author which hits they already own.
- **Verify citations**: `python3 "${CLAUDE_PLUGIN_ROOT}/tools/verify_refs.py"` checks every bibliography file under `literature/` (BibTeX, CSL JSON, RIS, PubMed `.nbib`) against Crossref: each DOI, and for entries without one a title lookup whose DOI is shown as a suggestion. Report MISMATCH / NOT FOUND / NO DOI entries; a suggested DOI is for the author to check, not verified.
- **Find unsupported claims**: scan the manuscript for claims without citation and list them with location.
- **Obsidian**: if a vault is configured, search it (Grep) for the author's notes on the topic and cite them as `[[note]]`.

Notes you write go to `notes/ai/sources-<topic>.md` (and, if configured, the vault's AI notes folder) with frontmatter `ai_generated: true`. Never write text for the manuscript, and never paste abstracts as manuscript text.
