---
name: notebook-gardening
description: "Keep the agent's notebook true: find duplicates and contradictions, correct beliefs in place with their source, fade stale ones, and list for the Commander what to delete."
license: MIT
metadata:
  title: "Notebook Gardening"
  category: "Station"
  author: "StarNet"
---

The notebook is recalled into future runs automatically. A wrong belief in it is worse than a missing one: it gets repeated with confidence until someone notices. Gardening is a correction pass, not tidying for its own sake.

Know your reach. notebook.write corrects an entry in place (the old text is archived, out of active recall). notebook.feedback raises or sinks an entry's trust. Nothing you hold deletes an entry — forgetting is the Commander's, in the agent's Dossier, MEMORY tab. And your notebook is your own; another agent's notes are out of reach.

## Method
1. **Read it all (notebook.read with no query).** Note the count. For a large notebook, work one topic at a time with `query`.
2. **Sort each entry into one bucket:** keep, merge, correct, stale, or not memory. Not memory = task progress, completed-work logs, ids, facts that go stale within a week, or a procedure (procedures belong in a skill).
3. **Trace the source of anything doubtful.** recall_conversation finds where a belief came from in past dialogue: search with `query`, then read the moment in context with `around`. A belief with no traceable source and no confirmation is a candidate for sinking, not keeping.
4. **Merge duplicates into the best-worded entry.** Rewrite that one with notebook.write using `replaceId` and its exact current `previousBody`, so it carries the whole fact. Rate the redundant copies `unhelpful` with notebook.feedback so they rank below it, and list them for the Commander to forget.
5. **Correct wrong beliefs in place.** notebook.write with `replaceId` + the exact `previousBody`. Never add a second, contradicting entry with `distinct: true` — that leaves the wrong one active. If the tool says the memory changed since you read it, read it again and retry.
6. **Write facts, not orders, with their source.** "Commander prefers invoices as PDF (said in chat, 2026-09-12)" — declarative, dated, sourced. Not "Always send PDFs": an imperative is re-read later as a standing order.
7. **Scope it right.** Project requirements use `scope: stream`; only preferences that apply across projects are `global`. Pin only explicit, approved, reusable requirements.
8. **Sink the stale.** A belief that was true once but is not now: correct it if you know the new truth; otherwise rate it `unhelpful` so it fades from recall, and list it for review.
9. **Reward what held up.** An entry you checked and found accurate gets `helpful`.

## Rules
- **Never correct from inference alone.** A correction needs a source: the Commander's words, a file, a page, a tool result.
- **Never retry a refused write with new wording.** "Already known" means no write happened and none is needed.
- **Say "saved" or "updated" only after the tool confirms it.**
- Keep procedures out of the notebook; propose them as skills instead.

## Done means
No two active entries state the same fact, no active entry contradicts another, every corrected entry names its source, and the Commander has the list of entries to forget.

## Output
Counts before and after (kept · merged · corrected · sunk), each correction with its old wording, new wording and source, then the forget list with entry ids.

*Needs the NOTEBOOK (notebook.read / notebook.write / notebook.feedback, recall_conversation).*
