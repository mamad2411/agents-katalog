---
name: use-agentic-rag
description: >
  The knowledge graph — documents in, written answers out. Load it when the owner wants the site to
  answer questions from company documents, when an answer must be composed across many files, before
  loading anything large into it, and when the base answers "unavailable" or answers nothing useful.
  Two things decide everything here and neither is visible from the code: loading is expensive while
  asking is cheap, so what you load is a budget decision; and the graph is built in the BACKGROUND,
  so a question asked right after loading honestly sees nothing.
---

# use-agentic-rag

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

The door and the credential are in `use-data`; the choice between this and passage search is in
`use-vector-memory` §2.

---

## 1. It is already written — use it

`lib/fractera/knowledge.ts`: **`ask`**, **`learn`**, **`knowledgeDocuments`**, **`knowledgeReady`**.

They go through `/service/rag/*` — the data service forwards to the engine on the server's loopback.
The engine is not published to the internet and its key is injected by the proxy: **you never hold
it**, and a project cloned onto a laptop reaches the same base with no second address and no second
port.

## 2. 🔒 Loading is expensive, asking is cheap — and that is the whole planning problem

`learn` makes the model read every chunk of the document to extract entities and relations. Once per
document, and it is the dominant cost of the whole feature. `ask` walks the graph that already exists.

**Therefore: load what will actually be asked about.** Loading "everything we have, just in case" is
how this feature becomes expensive without becoming useful. When the owner asks for the whole archive,
that is the moment to say the cost out loud — before the run, not in the invoice.

## 3. 🔒 The graph is built in the background

`learn` returns as soon as the document is ACCEPTED. Ask a question a second later and the honest
answer is "nothing found" — the graph is still being built.

So: never chain "load → ask" in one request and treat the empty answer as a defect. If the product
needs to show progress, the engine has a pipeline status of its own (`/service/rag/documents/pipeline_status`
through `dataFetch`), and `knowledgeDocuments` lists what it holds.

## 4. Modes of `ask`

| mode | Leans on | Take it when |
|---|---|---|
| `hybrid` (default) | named things **and** themes | you do not have a reason to choose another — this is the right default |
| `local` | specific entities | the question names a thing: a product, a person, a document |
| `global` | themes across the corpus | the question is about the whole: "what do our policies say about…" |
| `naive` | plain retrieval, no graph | you want to compare against a baseline, or the graph is empty |

The engine also accepts `mix` and `bypass`, and many knobs (`top_k`, rerank, references, streaming) —
`dataFetch("/service/rag/query", …)` reaches them all. Take that path only when the four above are not
enough, and say why.

## 5. The engine is bigger than the helper

Behind `/service/rag/*` sits a full API — around forty routes: documents (`text`, `texts`, `upload`,
`scan`, paginated listing, status counts, delete, reprocess), the graph itself (labels, entities,
relations, create / edit / merge), streaming query, and an ollama-compatible chat surface.

**Reach it with `dataFetch`, not with a new address.** Ask `/capabilities` for the proxy prefix rather
than trusting this list — a route list in a document is stale the moment the engine is upgraded.

🔒 **Deletion is ASYNCHRONOUS, and `200` is not proof of it.** The engine answers `deletion_started`
and does the work in the background: the document is still in the list a moment later, and that is not
a failure. Verify by asking for the list again and finding it gone — never by the status code.

🔒 **Delete by the document's ID, not by its name.** A name is what a person typed; the id is what the
engine indexed. Deleting by name looks like it worked — it returns the same cheerful `deletion_started`
and removes nothing. Both facts were bought on 2026-08-23, in a run that reported success twice.

## 6. "Unavailable" is a normal state, not a failure

`ask` returns `{ available: false }` when the base is switched off, and that is correct for a project
that does not use it. Show the product's own empty state — **never** invent an answer, and never hide
the fact with a cheerful fallback. `knowledgeReady` answers the question directly when you need it
before rendering.

The same applies to an empty graph: a base that was never loaded answers nothing, and that is not a
bug to work around.

## 7. Before you call it done

1. You chose the graph over vectors for a stated reason (`use-vector-memory` §2).
2. What you loaded is what will be asked about — and the owner knows the cost if it is large.
3. You did not measure the base immediately after loading; you waited for the background build.
4. The "unavailable" and "found nothing" paths are visible in the product, in the user's language, and
   are not disguised as an answer.
