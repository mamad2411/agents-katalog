---
name: use-translations
description: >
  Where a translatable string is allowed to live, how many languages it owes, and who checks. Load it
  before adding ANY user-visible string, before creating a dictionary, when a gate says a dictionary is
  short of languages, when the owner says "translate this" or "why is this page English", and before
  promising him a translation run. Three storage forms exist and they are not interchangeable; the
  number of languages is decided by WHAT the thing is, not by how important it feels; and the guard
  only checks the dictionaries somebody registered by hand — which is how two dictionaries stood
  outside it for weeks while looking perfectly healthy.
---

# use-translations

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

**A string is never written where it is used.** Everything below is about choosing its home, its
language count, and its guard — three decisions taken before the string exists, because moving one
afterwards means touching every file that reads it.

---

## 1. 🔒 Three forms, and they are not interchangeable

| Form | Looks like | Belongs to | Guarded by |
|---|---|---|---|
| **dictionary** | one file, `lang → { key: string }` | interface words: buttons, labels, empty states, errors | `check:i18n`, if registered |
| **language cell** | a folder, one file per language (`_data/en.ts`, `ru.ts`) | the CONTENT of an authored page: a post, a legal page, the home page | `check:i18n` via its own list, if registered |
| **object column** | an `i18n` column in the row itself (`lib/products/localize.ts` reads it) | the content of a thing somebody created: a product, a category | nothing — the person who made the object owns its languages |

Choosing wrong is expensive in one direction: interface words inside a language cell get copied into
every page that shows the same button, and they drift. Page prose inside a dictionary turns a file
meant for short labels into a document nobody can review.

🔒 **`lang === "ru" ? … : …` is not a third option.** It cannot be exported, cannot be counted by a
gate, and is found by the person least expecting it — a visitor on the language you never opened.

## 2. 🔒 How many languages — decided by WHAT it is

| The thing | Languages | Why |
|---|---|---|
| a **reusable** part of the product — appears anywhere the owner switches a language on | **82** | it shows up in a new language the same minute it is enabled, with nobody editing anything. Arriving there in English means that part is broken in every new market at once |
| words of **one page or one widget** | **10** | the page set; a widget belongs to one route and never appears by itself |
| content of an object | whoever created it | not our decision at all |

Cookie consent is the sharpest case of the first row: consent shown in a language the visitor does not
read is not a rough edge, it is **consent that did not happen**.

🔒 **Fewer than the row says is legal ONLY as a written debt** — a line in
`development-docs/TRANSLATION-DEBT.md` **and** the honest number in `scripts/check-i18n.mjs`. Two
dictionaries carry `2` today and both are written down. A number that lies to look finished is worse
than the debt: the next session reads the gate as truth.

## 3. 🔒 The guard checks only what somebody registered

`scripts/check-i18n.mjs` holds two hand-written lists — dictionaries and language cells. A file not on
a list is not checked at all, and nothing says so out loud.

**This is not an oversight to fix with a folder walk.** A walk would silently adopt files nobody
decided about, and the decision — how many languages this thing owes — is exactly what must be made
consciously. The cost is real and was paid: two dialog dictionaries already carried 82 languages while
standing outside the guard, so they could have been cut to ten and no gate would have noticed.

**Therefore: registering a new dictionary is part of the same commit as the dictionary.** Not a
follow-up task.

🔒 `check:i18n` does NOT run in `prebuild`. It and `check:types` are the two you run yourself
(`use-code-shape` §2).

## 4. Translating a lot at once — the owner's route, not yours

Translating page prose by hand is paid for in context on every iteration. The project has a pair of
scripts for handing the work to an external model:

```
node scripts/i18n-export.mjs <dict> --langs uk,cs,sk    → storage/i18n/<dict>.request.json
node scripts/i18n-import.mjs <dict> <answer.json>       → writes back, only if every check passes
```

Three limits worth knowing BEFORE you promise anything:

- **Only registered dictionaries, and only JSON ones.** `DICTS` in the export script lists them; a
  `.i18n.ts` dictionary is not among them. Wrong name → the script prints what it does know and stops.
- **There is no default language list.** `--langs` is mandatory; without it the script refuses rather
  than guessing a set.
- **The import does not trust the model, and that is its whole point.** It refuses a missing key, a
  changed placeholder (`{roles}` translated as `{роли}` breaks the page silently in exactly the
  language nobody opens) and an answer that is not an object of languages. Nothing is written until
  every check passes.

🔒 **A translation run is the owner's decision, not a chore you start.** Proposing one for strings he
did not ask about spends his money on work nobody ordered — and mid-development those strings will be
rewritten anyway.

## 5. When to translate at all

**Develop in the default language; translate when the thing is finished.** During construction the
same string is rewritten several times, and every rewrite pays for the translation again.

That rule has a second half, and forgetting it is what makes it dangerous: the postponed translation
disappears from view together with the step. Write the debt down the same day, in
`TRANSLATION-DEBT.md`, or in a month nobody can say which routes are still single-language.

## 6. Machine strings are never translated

Ids, slugs, enum values, `data-*` attributes, config keys, product names in the do-not-translate list
(`Fractera`, `GitHub`, `OpenAI`, `Next.js`, …). A translated identifier does not look wrong — it looks
like a working page until something searches by it.

## 7. Before you call it done

1. `npm run check:i18n` — nobody runs it for you, and it is not in `prebuild`.
2. The new dictionary is registered in `scripts/check-i18n.mjs` **in this commit**, with the number of
   languages it owes.
3. Any shortfall is a line in `TRANSLATION-DEBT.md`, and the gate's number matches reality.
4. Open the page in a language you did NOT write — the second one is enough. An untranslated string
   shows itself instantly there and never in the language you were building in.
