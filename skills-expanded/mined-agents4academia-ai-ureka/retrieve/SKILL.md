---
description: Find the knowledge-base notes relevant to a topic — BM25 seeds expanded by following relevant wikilinks — returned as a list of files with a one-line reason each
argument-hint: <query / topic> (e.g. "RLHF", "how ReAct reduces hallucination")
allowed-tools: Bash(sh .claude/src/pyrun:*), Read, Glob
---

Find the notes in the local knowledge base relevant to **$ARGUMENTS**. The base
spans four directories — `sources/` (objective paper text), `notes/` (personal
notes + annotations), `papers/` (paper pages), and `concepts/` (concept pages) —
and retrieval covers all four. It works in two parts: a Python BM25 search gives
**seed** notes (no LLM), then **you** expand from those seeds by reading each note
and following only the wikilinks that look relevant to the query. Return the
resulting set of relevant notes — a list of files, each with a one-sentence reason
it's relevant. Do not synthesise or merge their contents.

If **$ARGUMENTS** is empty, ask the user for a query, then continue.

## Steps

1. **Get seed notes.** Run the Python retriever (it builds/refreshes the index
   automatically; needs no API key):

   ```bash
   sh .claude/src/pyrun .claude/src/retrieve_cli.py --retrieve "$ARGUMENTS"
   ```

   Each output line is `<file path>\t<title>`. These seeds start your working
   set. (Optional: `-k N` for more/fewer seeds.)

2. **Expand by following relevant wikilinks.** Maintain a *relevant set* (notes
   you'll return) and a *frontier* of notes to examine, initialised to the seeds.
   While the frontier is non-empty:
   - Take a note off the frontier and `Read` it (skip if already visited).
   - Decide if it's relevant to **$ARGUMENTS**; if so, add it to the relevant set
     with a one-sentence reason why.
   - Look at the note's `[[wikilinks]]`. For each, judge whether *that linked
     note* is likely to hold material relevant to **$ARGUMENTS**. Only for the
     ones you judge relevant, resolve them to files and add any not-yet-visited
     notes to the frontier:

     ```bash
     sh .claude/src/pyrun .claude/src/retrieve_cli.py --resolve "tool use" "planning"
     ```

     Output is `<link>\t<path|NONE>`; skip `NONE` (no page yet — a knowledge-base
     gap) and skip notes already visited.
   - Keep the expansion focused: follow only genuinely relevant links, don't
     re-visit notes, and stop once nothing new and relevant is being found (in
     practice ~1–2 hops out from the seeds is plenty).

3. **Return the relevant set.** Present each note as a clickable file path with
   its one-line reason, e.g.

   ```
   - papers/instructgpt.md — defines the RLHF pipeline the query asks about
   - concepts/rlhf.md — followed from instructgpt's [[RLHF]] link; explains reward modelling + PPO
   - sources/zotero_instructgpt.md — primary annotation backing the pipeline details
   ```

   List the files only — do not synthesise, summarise, or merge their contents.

## Notes

- This skill needs **no Anthropic API key**: the Python side is pure BM25/lookup,
  and the wikilink-following judgement is done by you (Claude) reading the notes.
- It does not write or edit any files.
- Used directly when the user asks to find relevant notes, and as the gathering
  step for the `/concept` (synthesis) and `/ask` (question-answering) skills.
