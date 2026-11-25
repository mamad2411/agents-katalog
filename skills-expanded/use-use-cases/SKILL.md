---
name: use-use-cases
description: >
  Mode `cases` — the order in which work is allowed to start when the owner has switched it on: a case
  he confirmed, then a queue of numbered steps, and every step naming the case it serves. Load it when
  `PLATFORM-CONFIG.mode` is `cases`, when the owner says "add a case" / "what are we building next" /
  "decompose this", and before opening any step in a product that has a dossier. Two things you cannot
  guess: a case is confirmed ONLY by the owner and nothing in your reach can confirm one, and the
  decomposition step is found by its `kind`, never by matching its title — the title is a sentence
  somebody will reword.
---

# use-use-cases

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

**The mode answers one question: what gives you the right to write the first line?** In `classic` the
answer is "he asked". Here it is a **confirmed case**, and everything below is the machinery that keeps
that honest.

---

## 1. Where the two entities actually live

| | Cases | Steps |
|---|---|---|
| What it is | content a person confirmed | the state of a queue |
| Home | the product dossier — `PRODUCTS-CONFIG/<id>.json`, array `cases[]` | table `development_steps` (declared in `lib/db/index.ts`), mirrored in the dossier's `steps[]` |
| A case carries | `slug`, `title`, `summary`, `confirmed`, `confirmedAt`, `updatedAt` | `number`, `product_id`, `title`, `status`, `importance`, `kind`, `cases`, `plan`, `result` |
| Asked of it | "what are we building" | "what is open for this product" |

🔒 **The step NUMBER is server-wide and permanent.** Not per product: the dossier lists a product's steps
by number as a table of contents, and a number that only means something inside one product would make
that list unreadable. Closing a step never renames or renumbers it — completion is a column
(`status`), not a rename.

🔒 **`product_id = 'platform'` is a legal value, not a placeholder.** Theme, languages, the offline
cache belong to the whole server; forcing a product id onto them would be a field that lies.

## 2. The flow, and why it has two entrances

```
intake — the panel's Quiz writes questions and answers into the dossier
      │
      │  🔒 the OWNER confirms a case  (confirmed: true)
      ▼
a DECOMPOSITION step appears           kind: "decomposition", one per product
      │  created by the panel at confirmation time;
      │  created by the agent at session start if it is missing
      ▼
you execute it: read the confirmed cases, write the ordered queue
      the FIRST step is always the minimal working skeleton —
      architecture on disk, doors present, navigation walking on stubs
      ▼
development → analysis (the owner decides what is finished)
```

**Two independent paths to one state, both idempotent.** The panel creates the step because that is
where the owner acts and the queue must exist even if no agent is ever opened. You create it because a
mechanism that depends on the other path having run is a mechanism that silently does nothing.

🔒 **Find it by `kind`, never by title.** `WHERE product_id = ? AND kind = 'decomposition'`. A lookup
that matches a sentence survives exactly until somebody rewords the sentence.

## 3. 🔒 Rules that decide whether the mode means anything

- **Only the owner confirms.** There is no tool to confirm a case — by construction, not by omission.
  An unconfirmed case is the model's guess about his business, and building on it is the expensive kind
  of wrong: it looks finished.
- **Editing a confirmed case returns it to draft.** Green must mean "he approved *this* text", not "he
  approved something that used to be here". The panel does this; do not work around it.
- **A step names the cases it serves** (`cases: string[]`). A step serving none is work nobody ordered.
  `platform` steps are the one exception.
- **A step's title is 6–12 words** — the service refuses anything else. A title is a promise, not a
  paragraph.
- **The stage only moves forward.** Backwards is the owner's decision, made in the panel.
- **The phase is derived, not typed:** `intake` → `decomposition` → `development` → `analysis` come out
  of the dossier itself — the questions answered, the cases confirmed, the statuses of the steps — so it
  cannot drift from the truth. Details of the dossier: `use-products-config`.

## 4. 🔒 The closing question is not "does it work"

Green gates and a live page answer "does it work". They cannot answer **"is this what was ordered"** —
only the case can. So closing a step, name its case and say what promised in it is now true. A feature
that works perfectly and answers no case is work the owner did not ask for, and it is the most
expensive thing this mode exists to prevent.

## 5. The boundary with the other two skills

| Skill | Owns |
|---|---|
| `use-use-cases` (this) | the right to start: cases, their confirmation, the queue born from them |
| **`build-product-with-owner`** | **the PATH once a case is confirmed**: the pact with the owner, the four decisions before the first route, the furniture, the size of an iteration, the prototype line |
| `use-development-steps` | how a step is CARRIED — session handover in `current-steps.md`, the group, the closing report |
| `use-products-config` | the dossier itself: record, phases, the pages plan, what belongs to which product |

They are not alternatives. The table is the queue the owner sees in the panel; `current-steps.md` is
what survives a context reset. Neither replaces the other, and neither is derived from the other.

## 6. Before you say the mode is being followed

1. The case you are building against is `confirmed: true` in the dossier — quote its slug.
2. The step exists in the queue and names that slug.
3. The first step of a new product is a skeleton that RUNS, not a folder of intentions.
4. Nothing was confirmed, moved backwards, or reworded by you on the owner's behalf.
