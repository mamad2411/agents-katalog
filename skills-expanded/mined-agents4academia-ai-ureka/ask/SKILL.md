---
description: Answer a question from the knowledge base — retrieve relevant notes, synthesize a cited answer, and flag gaps (optionally searching the web for what's missing)
argument-hint: <question> (e.g. "how does ReAct reduce hallucination?")
allowed-tools: Read, Glob, Bash(sh .claude/src/pyrun:*), WebSearch, WebFetch
---

Answer **$ARGUMENTS** using the local knowledge base. Retrieve the relevant notes,
synthesize an answer grounded in them with inline citations, and be explicit when
the base doesn't have enough to answer.

If **$ARGUMENTS** is empty, ask the user for their question, then continue.

## Layout

Knowledge-base I/O is at the repo root, across `sources/` (objective paper text),
`notes/` (personal notes), `papers/` (paper pages), and `concepts/` (concept pages).

## Steps

1. **Retrieve.** Use the **`/retrieve`** skill to gather the notes relevant to the
   question across the whole base: get BM25 seeds, then expand by following relevant
   wikilinks.

   ```bash
   sh .claude/src/pyrun .claude/src/retrieve_cli.py --retrieve "$ARGUMENTS"
   sh .claude/src/pyrun .claude/src/retrieve_cli.py --resolve "<linked topic>" ...
   ```

   `Read` each relevant file.

2. **Synthesize an answer.** Answer the question directly and concisely in your own
   words, grounded **only** in the retrieved files. Cite each claim inline with a
   relative link to the file it came from, e.g.
   `ReAct grounds reasoning in tool observations, cutting hallucination ([ReAct](papers/react.md))`.
   Distinguish objective findings (`sources/`, `papers/`) from the user's own notes
   (`notes/`) where it matters. Where the answer is mathematical, give the relevant
   equations/derivations rather than vague prose (the **Page conventions** in
   `.claude/AGENTS.md` cover this). Format note: answers print to the terminal, which does
   **not** render LaTeX, so use plain readable notation (e.g. `sqrt(d_k)`) in the
   reply; only switch to LaTeX (`$ ... $` / `$$ ... $$`) if the user asks to save the
   answer into a page.

3. **Flag gaps.** If the base doesn't fully answer the question, say so plainly and
   name what's missing — e.g. "no source in the base covers X". If it would help,
   use `WebSearch`/`WebFetch` to identify what the missing material is (a paper,
   a method, a result) and suggest the user ingest it via `/paper`. Clearly mark any
   web-derived information as **not from the knowledge base** and do not present it
   as a cited base answer.

## Wrap up

End with a short **Sources** list (the base files you cited) and, separately, any
**gaps** found — so the user can fill them with `/paper` or `/concept`.
