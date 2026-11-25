---
name: use-vector-memory
description: >
  Meaning-search over text you store — and the choice between it and the knowledge graph. Load it when
  the owner says "find by meaning", "search that isn't exact-match", "answer from our documents", when
  you are about to add a search box over prose, or when a search returns nothing useful and you cannot
  see why. The functions already exist in this project (`lib/fractera/vectors.ts`); what nobody
  guesses is that half of the failures here are not code — they are a document stored whole instead of
  in pieces, or the wrong tool chosen for the shape of the answer.
---

# use-vector-memory

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

The door and the credential are in `use-data`. This is about storing text so it can be found by
meaning.

---

## 1. It is already written — use it

`lib/fractera/vectors.ts`: **`remember`**, **`recall`**, **`forget`**, **`vectorStatus`**. Server-side,
through the one door. Do not write HTTP calls of your own to `/vectors` — the helper is the same call
with the mistakes already removed.

🔒 **Nothing in this repository calls them yet** (checked 2026-08-23: zero imports of
`lib/fractera/vectors` outside the helper itself). The helper is written and the store answers — but
you will be the first caller, so budget a minute to look at what `recall` actually returns instead of
assuming a shape. The neighbouring map skill states the same thing about itself; this one did not,
and a cold run pointed that out.

Storage lives in the SAME database as your rows, so a record can point back at the row it describes
through `refTable` / `refId`. That link is what turns "a passage matched" into "this product matched".

## 2. 🔒 Vector memory or the knowledge graph — decided by the SHAPE of the answer

| The answer is… | Tool | What you get back |
|---|---|---|
| in ONE passage, and you will show it | **vectors** (`recall`) | passages with a score — you do the writing |
| spread across MANY documents, and must be composed | **graph** (`ask`, `use-agentic-rag`) | a written answer |

**Cost decides the rest.** Storing a vector is one cheap embedding call. Loading a document into the
graph makes the model read every chunk to extract entities and relations. Asking is cheap in both.

Choosing the graph for "find me the paragraph about returns" buys slowness and nothing else; choosing
vectors for "what does our policy say about refunds across these twelve documents" gives twelve
disconnected passages and no answer.

## 3. 🔒 Long text must be split before storing — this is the usual failure

One vector for forty pages finds nothing well: the embedding averages everything the document says
until it says nothing in particular. A few hundred to a thousand characters per piece works.

The split is yours to make, and it should follow meaning — a section, a paragraph, a product
description — not a fixed character count that cuts sentences in half.

## 4. `collection` is the only filter a search has

So choose it as the thing you will want to search WITHIN: `docs`, `products`, `tickets`. It cannot be
narrowed later by anything else — there is no `where` clause on top of a `recall`. One collection for
everything means every search competes with every unrelated text you ever stored.

## 5. Facts that change how you use it

- **The embedding model and its size are the platform's, not yours** — ask `/capabilities`
  (`vectors.model`, `vectors.dims`) rather than assuming. Vectors stored with one model are not
  comparable with another's; changing the model means re-storing everything.
- **You may pass your own `embedding`** to `remember` — then no model is called at all. That is the
  path for text you already embedded elsewhere, and for tests that must not spend money.
- **Nothing here needs a key of its own.** The OpenAI key lives in the data service, not in your slot.
  A store that fails because no key is configured is an owner-level problem — say so plainly instead
  of building a fallback that hides it.
- **`vectorStatus`** tells you whether the store answers at all, and how it indexes. A project that
  never stored anything returns an empty, healthy store — that is not a fault.

## 6. What NOT to build

- A second store of your own: a table of texts plus your own similarity in JavaScript. It exists, it
  is indexed, and it is in the same database.
- A cache of embeddings in the repository. They belong to the data layer and go stale with the model.
- Exact-match search through vectors. If the user types an article number, that is a `WHERE` clause —
  meaning-search will find something similar and be wrong with confidence.

## 7. Before you call it done

1. Stored in pieces, not whole documents; `collection` named after what you will search within.
2. `recall` run against real stored text — and read: the top hit should be the passage you expect, not
   merely *a* passage.
3. `refTable` / `refId` set when the text describes a row, so the result can be turned into a link.
4. Say in the step which tool you chose and why, in one line — the choice between vectors and the
   graph is the decision here; the code is not.
