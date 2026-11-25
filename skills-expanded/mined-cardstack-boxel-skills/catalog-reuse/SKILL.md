---
name: catalog-reuse
description: >-
  MANDATORY before writing any `.gts`. Boxel ships a curated catalog; search it before you author. Classify what you need, then apply the matching reuse operation: a **Spec** when you need building blocks (a CardDef to link, a FieldDef to contain, a component or command to import — catalog modules import directly, so this is the default), an **instance** when the content already exists (point a relationship at it), a **Listing** when the user wants a bundle of their own to keep and change (install or remix it; apps ship as app Specs, never Listings). Build new only for confirmed gaps. For UI primitives inside a `.gts` template, use boxel-ui-component-discovery instead.
boxel:
  kind: skill
  tools:
    - codeRef:
        module: '@cardstack/boxel-host/tools/run-realm-code'
        name: default
---

# Catalog Reuse

Boxel ships a **curated catalog**: apps, cards and fields as definitions you
reference where they live, components, commands, themes, assets, and Listings
packaged for installation — real, tested parts other people finished and
shipped.

**First classify what kind of thing you need. Then apply the reuse operation for
that kind.** Everything below is that one idea, made operational.

## Non-negotiable rules

1. **Never author before searching.** By the time you write the first line of
   any `.gts`, a catalog query must already have returned.
2. **Never treat a Spec as the reusable object.** A Spec is an index entry. You
   reuse what its `ref` names, or an instance from its `linkedExamples` — never
   the Spec itself.
3. **Never conclude a gap after one failed query.** Broaden once (step 5) before
   declaring anything missing.
4. **Never pass over a suitable result without recording why.** Every hit is
   adopted, or refused in writing naming what mismatched. A Listing you answered
   by referencing its parts counts as adopted — say which parts, and move on.
   A second hit that ships an export you already took is refused as a
   duplicate, not taken as well: two hits that ship the same module export are
   one decision.
5. **Never copy what you can reference.** Catalog modules import directly, so a
   definition can be used without taking a copy of it. Install or remix a
   Listing when the user wants their own bundle — and when you do take a copy,
   take it through `install` or `remix`, never by hand.
6. **Prove it at the end.** For everything you authored from scratch, be able to
   name the reuse option above it and why it was unusable. "I didn't look" means
   it needs replacing.

Reading design or pattern references is not a substitute for searching: they
tell you how to build well, not whether to build at all.

## Required workflow

1. **Enumerate** every card, field, component, command, app, theme, and asset
   the brief implies, in plain language. A noun that names an entity — "the
   venue we booked", "the supplier", "the workshop" — is one of those cards:
   enumerate the entity itself and search for it. Spelling it out as the two or
   three attributes you would otherwise type is how a card-sized need gets
   searched for as nothing at all. This holds when the brief reaches the entity
   only through its attributes — "the supplier's payment terms", "the venue's
   capacity" — a possessive names the entity as surely as a bare noun does, and
   what it owns is the card's business, not yours to re-declare.
2. **Search Specs** for each enumerated need, and reference what you find.
   One `matches` term per need. A search for the whole deliverable ("a service
   desk", "a support app") is not a search for its parts and does not replace
   one.
3. **Search Listings only when the user asked to own something**, and be able
   to quote the words that asked — "our own", "a copy we can change",
   "independent of theirs". No such words, no Listing search. That a Listing
   exists and fits is not a reason to install it: nobody asked for a copy.
4. **Search instances** when a need is content-shaped — a particular author,
   theme, config, image, or a sample to start from.
5. **Evaluate** each hit against the need; broaden once before calling anything
   a gap.
6. **Build only confirmed gaps**, and record them. When a catalog definition
   answers the brief, the build is an instance of it, not a design pass.
7. **Self-audit** before finishing.

Step 2 is the default because a catalog definition can be referenced where it
lives. Step 3 hands the user a copy — a separate thing to own, which cannot be
re-attached to the catalog later — so it answers a stated wish for their own
bundle, not a match in the search results.

### One card: one search run, then write

When the user asks for a single card with a few fields of its own, and not an
app, a card family or a page, the workflow takes one read-only run, and the
next run writes.

1. **Search in one script.** Search Specs for the entity the card is, and put
   the broadened query of step 5 (`OR` alternates, no `specType`) in the same
   script, so the broadening costs no turn of its own. Return
   `{ url, ref, specType, cardTitle }` for each hit, and the `readMe` of the
   top two or three. The card's own attributes (a first name, a headline) are
   not needs of their own: the search for the entity covers them.
2. **Decide from the `readMe`.** Adopt a hit by its `ref` (link, contain or
   extend, as in the Parts table), or refuse it naming the mismatch. Read
   source only where the reading budget below says the chosen operation needs
   it.
3. **Write in the next run.**

A control in the card's template is `boxel-ui-component-discovery`'s search,
not a second catalog search.

## Reuse strategy: classify, then operate

**You may import catalog modules directly.** `@cardstack/catalog/` is a
registered import prefix, so a catalog module imports straight into your `.gts`
across realms — you do not have to copy the file in. That is why referencing is
the default and copying is the exception.

Every search here is a search over card instances — `Spec` and `Listing` are
ordinary card types, and so is `Author`. What differs is what a hit **denotes**.

| You need | Anchor on | A hit denotes | Operation |
|---|---|---|---|
| parts to build with | `Spec` | a module export, named by `ref` | link · contain · extend · import |
| content that exists | the card type itself | the instance | point a `linksTo` / `linksToMany` at it · or copy and edit |
| a bundle of their own | `Listing` | an installable bundle | `install` to hand it over as-is · `remix` when they will diverge from it |

Nothing exports a Listing, so no CodeRef names one: **a Spec query can never
return a Listing, and a Listing query can never return a bare definition.**
Different anchors, because they describe different kinds of thing.

**A Listing that fits is not a Listing you have to take.** What it bundles are
Specs, and referencing those answers the same need without handing over a copy —
the parts arrive wired to the catalog instead of forked from it. Choosing the
parts over the bundle is not passing over a suitable result; it is taking the
same result by the binding that keeps working.

### Parts: what each `specType` entitles you to

Take the target from the hit's `ref` (module + name) and wire **that**.

| `specType` | The export is | How you wire it |
|---|---|---|
| `card` | a **CardDef** | `linksTo` / `linksToMany` as a field · `extends` to specialize · `adoptsFrom` in an instance |
| `field` | a **FieldDef** | `contains` / `containsMany` · `extends` to specialize |
| `component` | a Glimmer component | import into your template's markup |
| `command` | a Command | import and invoke, or run through your session's command mechanism |
| `app` | an **AppCard** (the app's root CardDef) | import or `extends` it through `@cardstack/catalog/…` and link its `linkedExamples` instance; the cards it composes are `card` Specs of their own |
| `file` | an asset | an **instance** → use the instance anchor |

**How you declare the wiring is `boxel`'s call, not this skill's.** Its
Cardinal Rules own CardDef-vs-FieldDef and `contains` vs `linksTo`. Here you
decide *which* catalog unit answers the need; go there for how to write it.

`specType` crosses these rows — five values name module exports, `file` is an
instance.

Within parts, prefer more whole over less: a card over a field, a field over
hand-rolled markup. This is not a queue — a need that *is* a field starts at the
field. What it forbids is hand-building a part when a bigger unit contains it.

### Content: two different instance searches

- **Catalog instances — this is reuse.** Anchor on the card type and search the
  catalog. A hit is something to point a relationship at, or to copy and edit.
- **Your own realm — this is a self-check.** Same tool, your realm. It answers
  "have I already built this?", not "has the catalog?", and does **not** satisfy
  step 2 or 3.

`linkedExamples` on a Spec hit is the direct route from a definition to the
instances the catalog ships for it. Check it before authoring instances by hand.
A search entry does not carry it. Read the Spec with `realm.cards.get(url)`,
where `url` is the entry's `url`, in a run in the catalog (see *Read catalog
source in a run in the catalog* below). The answer's `relationships` lists each
example as `linkedExamples.0`, `linkedExamples.1`, and so on.

**Declaring a relationship and filling it are different steps.** You declare
`@field author = linksTo(Author)` from a Spec hit's `ref` (parts); you fill it by
pointing `relationships.author` at an existing `…/Author/jane.json` you found by
searching instances (content). Same keyword, different step.

## Search mechanics

**Transport.** Use whichever search you actually have — the queries below are
identical either way.

- **`realm.entries.search(query, { realms, scope, limit })` in a
  `run-realm-code` script**, in an assistant room. This skill declares the
  `run-realm-code` tool; the sandbox rules for the script are in
  `source-code-editing`. For parts, pass `realms: ['@cardstack/catalog/']` (its
  full `https://` URL works too): without `realms` the search also reads every
  workspace the user can read, and a definition or policy from another
  workspace is not a catalog part. Pass your own realm's URL for the
  self-check below. A realm is a realm root such as `…/catalog/`: a module folder inside
  it (`…/catalog/<app-folder>/`) is not a realm, and one such URL fails the
  whole search. To narrow to one app, `matches` its name (or, for instances,
  anchor `on` its type). Put all the searches of a step in one script. The
  realm calls of a run go one at a time, also in `Promise.all`, and a run has
  55 seconds, so put at most five searches in one script and split more across
  runs. It answers `{ entries, total, truncated, incomplete }`.
  Each entry is `{ url, kind, ref, specType, cardTitle, cardDescription, name,
  readMe }`, with the fields at the top level, not under `attributes`. An entry
  does not carry the card's other fields or its links.
- **`npx boxel search --realm <realm-url> --query '<filter-json>' --json`**,
  where you have a shell instead. Here `--realm` is required and repeatable, so
  the catalog realm has to be passed explicitly; your environment guidance names
  its URL.

Card-search tools are a different thing again: they fetch live instances to
attach, open, or patch.

**Filter shape.** Card-rooted: an `on` type anchor plus `every` / `eq` /
`matches`, bare field names. Never hand-write `item.`-prefixed paths.

```json
{
  "filter": {
    "on": { "module": "@cardstack/base/spec", "name": "Spec" },
    "every": [{ "eq": { "specType": "field" } }, { "matches": "address" }]
  },
  "sort": [{ "by": "_matchRelevance", "direction": "desc" }]
}
```

`specType` is advisory and sometimes absent, so the broadened retry drops it —
this is the form to reach for when the constrained query returns nothing:

```json
{
  "filter": {
    "on": { "module": "@cardstack/base/spec", "name": "Spec" },
    "matches": "address OR postal OR location"
  }
}
```

For Listings the anchor is
`{ "module": "@cardstack/catalog/catalog-app/listing/listing", "name": "Listing" }`;
for content, the card type itself.

**`scope`** is `'cards' | 'files' | 'all'` and selects card-instance rows vs file
rows. It is orthogonal to which type you anchor on — Specs, Listings and Authors
are all card instances. Use `'files'` for assets.

**Three query rules that decide outcomes:**

- **The query is the first argument**, never `realm.entries.search({ query })`
  or a bare string: both are refused, the first with `unknown field in query:
  query`. Anchor Spec searches `on: Spec`, or you get instances and Listings
  and read an example to find the definition it adopts from.
- **`matches` ANDs its words.** `"person author"` means *person AND author*.
  One concept per query; spell alternatives as `"person OR author"`. Keep an
  `OR` set to terms of comparable specificity — one generic word swamps it
  (`"game OR card OR gambling"` against a catalog of cards returns everything).
  An empty result from a multi-word `matches` is a malformed query, not a gap.
- **`_matchRelevance`** scores 0–1, best first, and is appended for you when the
  filter carries a positive `matches`. Read the scores, do not just take rank 1:
  a flat spread of low scores means the query was too broad. The sort is only
  valid alongside `matches` — requesting it on a `type`-only filter is rejected.

Deeper query semantics: `boxel/references/query-systems.md`,
`boxel/references/spec-usage.md`.

## Evaluating hits

Read each hit's `specType`, `cardTitle`, `cardDescription`, and `readMe`. A text
match is a candidate, not a decision. The `readMe` is the source of truth — it
carries the API contract, and `realm.entries.search` returns it in full on each
entry, so judging needs no follow-up read. `cardDescription` is often empty, so `readMe`
and `ref` are usually what settle it. Judging on the title alone is how a Spec
that answered the need gets discarded.

Keep what a script returns small: everything it returns stays in the
conversation for every later turn. Return `{ url, ref, specType, cardTitle }`
for each hit, and the `readMe` only of the few hits you are choosing between.
Ask for `limit: 10` per term; a need that ten best-first hits do not answer
needs a better term, not a longer list.

**Read catalog source in a run in the catalog.** A `run-realm-code` script
reads and writes only the realm the tool's `realm` argument names
(`boxel-environment/references/workflows-and-orchestration.md` → *Multi-Realm
Operations*). That is the tool's argument, not the script's `realm` global,
which stays the API. Every `realm.fs` path resolves against that realm, and
`realm.fs.readText` takes a path only — a second argument such as `{ realm }`
is ignored, so a catalog path read from a run in your workspace answers
`File not found`. A run can read a realm that the user can only read.

1. **Search and read in one run in the catalog.** Set the tool's `realm`
   argument to the catalog's full `https://` URL, never the
   `@cardstack/catalog/` prefix, which the argument refuses.
   `realm.entries.search` reaches every realm from any run, so the search fits
   in the same script: search, pick the hit and the operation you will use
   (link, contain, instantiate, import, call, extend), then read only what that
   operation needs (the reading budget below), with paths relative to the
   catalog root.
2. **Write in the next run, in your own workspace**, importing the catalog
   module by its `@cardstack/catalog/…` path.

```js
// run-realm-code with realm: '<catalog https:// URL>'
let spec = { module: '@cardstack/base/spec', name: 'Spec' };
let found = await realm.entries.search(
  { filter: { on: spec, every: [{ eq: { specType: 'card' } }, { matches: 'contract' }] } },
  { limit: 10 },
);
let contract = await realm.fs.readText('cards/legal/contract.gts');
return {
  hits: found.entries.map(({ url, ref, cardTitle }) => ({ url, ref, cardTitle })),
  contract,
};
```

**Reading budget.** Everything a read returns stays in the conversation, so a
catalog module you read is paid for again on every later turn. Read catalog
source in a `run-realm-code` script, never with `readRealmFile`, which returns
the whole file and cannot slice it. Most reuse needs no source at all. What
each operation needs, in the order of the Parts table:

| Operation | Read |
|---|---|
| link a card type (`linksTo` / `linksToMany`) | nothing: the hit's `ref` is the contract |
| link an existing instance | nothing; `realm.cards.get(url)` if you need its values |
| contain a field (`contains`) | nothing: the hit's `ref` and `readMe` |
| instantiate a catalog type (`adoptsFrom`) | one of the Spec's `linkedExamples`, for the value shapes: a `YearField` holds `{ value: … }`, an `AmountWithCurrency` holds `{ amount, currency: { code } }`; a bare number or code indexes as null |
| import a component, call a command | the `readMe` |
| extend without changing behaviour | the `readMe` |
| extend and change a field the catalog reads | the declaration, and every place that reads the field — usually two modules |

Return windows, not files. Search the text for the name and return the lines
around each match:

```js
let src = await realm.fs.readText('cards/legal/approval-rule.gts');
let windows = [];
for (let at = src.indexOf('minValue'); at >= 0; at = src.indexOf('minValue', at + 1)) {
  windows.push(src.slice(Math.max(0, at - 300), at + 900));
}
return { windows: windows.slice(0, 6) };
```

Never cut from the top (`src.slice(0, 6000)`): the member sits past the cut
and you read the file again. Take every window you need from a file in one
run, and read each file once. When every need has a disposition, the next run
writes.

A catalog import without an extension (`./utils/format`) may be a `.ts` file
rather than `.gts`. On `File not found`, run `realm.fs.list` on that folder (it
lists one level) and read the name it returns instead of guessing again.

**If a need returns nothing, broaden once** before concluding a gap: re-query
with two or three alternates joined by `OR`, and drop the `specType` constraint.
Each answer carries a `total`, the number of matches. When `truncated` is
`true`, more entries match than the answer holds; the search does not page, so
narrow the query first, and raise `limit` (at most 50) only to see more
titles. When `incomplete` is `true`, a
realm did not answer, and an empty answer is not yet a gap. The catalog is a corpus of app-specific parts, not a standard library, so
"nothing fits" is often correct — but it is a verdict you record, never one you
take silently.

**Then disposition every hit**: adopted, or refused naming what actually
mismatched — the fields it lacks, the design rule it breaks. Reading a hit and
then authoring your own is a refusal, not a reuse: record it as one, naming
why the hit itself could not be linked, installed, or copied.

Before you say a catalog card lacks an action, look in its formats (`edit`,
`isolated`): an action often lives there, and a subclass or an instance
inherits it.

## Edge cases

- **Whole apps** ship as app Specs (`specType: "app"`), not Listings. Use one
  by reference like any other part: import its module through
  `@cardstack/catalog/…` and link its example instance. The catalog's Listings
  are cards, fields, themes and components, so an app has no bundle to install;
  when the user wants an app of their own, build from the app's Specs.
- **Themes** are instances — link one through `cardInfo.theme`, or copy and edit
  when it must diverge.
- **Files, images, fonts, icons** are instances too — search with
  `scope: 'files'` and `linksTo` what you find.
- **Referencing beats installing; installing beats re-typing.** Hand-writing
  code that already exists costs a large multiple of any reuse and drifts from
  the original. Visual or naming differences are never a reason to skip reuse —
  reference and restyle. When the user wants their own bundle, install rather
  than re-type, and remix when the bundle they own will diverge from the
  catalog's. `catalog-listing` has the mechanics. Changing behavior is not
  asking to own a copy: a new rule or a new scale of values is a
  specialization (see the change-request bullet below), not a remix.
- **Reuse *from a user realm* does mean copying.** User realms have no import
  prefix and literal realm URLs are lint-banned. This restricts user realms, not
  the catalog — catalog modules import directly.
- **Reuse the model, own the look.** A reused catalog card keeps its fields,
  computeds and operations, not necessarily its stock look; restyle it with the
  lowest step that works and record the route in the disposition:
  [`restyle-reused-card.md`](references/restyle-reused-card.md).
- **A change request goes through the same workflow, and is built in that
  reply.** When a later message changes what you built — a scale of values the
  catalog's field does not carry, an extra field, a new rule — list the changed
  parts, then search, evaluate and settle each one. The user's message is the
  go-ahead: state any assumption in one line and build, rather than describing
  the change and asking whether to make it. Take the lightest route that
  makes the change real, and write it now. When the catalog keeps the rule in
  a card, add an instance of that card: a contract that needs a new sign-off
  threshold is a new `ApprovalRule` instance with its own `minValue` and
  `requiredRoles`, like the catalog's `vendor-over-100k`, with no new field or
  code. Link or contain a different catalog part when one fits. Extend only
  when behaviour must change, and then:
  1. In your realm, write a definition that `extends` the catalog one (or calls
     the factory its Spec ships) and overrides only what changed. Redeclaring
     an inherited `@field` replaces it in the subclass. For a field a factory
     builds, call the same factory with the new values:

     ```gts
     import { contains, field } from '@cardstack/base/card-api';
     import { markDefinition } from '@cardstack/base/mark-definition';
     import { statusField } from '@cardstack/catalog/fields/status/status';
     import { Shipment } from '@cardstack/catalog/<shipment-module>';

     export const OurStageField = markDefinition(
       statusField({
         options: [{ value: 'Packed' }, { value: 'At hub' }, { value: 'Delivered' }],
       }),
     );

     export class OurShipment extends Shipment {
       @field stage = contains(OurStageField);
     }
     ```

     An exported definition made by a call is wrapped in `markDefinition`
     (`boxel/references/enumerations.md`).

     A catalog readMe that calls a vocabulary "hardcoded" describes the
     catalog's own module, not what your subclass can declare.
  2. Code in the catalog definition that reads the field you changed — a
     lookup table keyed on its values, a badge colour, a sort — is part of that
     override, not a reason to stop. Override the members that read it, or
     build the field and name which catalog behaviour still uses the old
     values.
  3. Point the instances you made at the new definition (`meta.adoptsFrom`)
     and show one, so the user sees the change.
  4. Check the rule before the reply claims it. A field, option or factor you
     add changes nothing until catalog code reads it: a computed that reads
     the catalog's own field class never sees the value on yours. Search the
     catalog module for the field name to find what reads it. If a rule card
     carries the rule, the data route above is the change; if only code reads
     it, override that member. Every number in the reply then comes from the
     index (`realm.cards.get` in the next run) or is marked as one you typed.

  Read the module that declares the changed field and the one that reads it,
  then write in your next turn. A turn of reading with no write after the plan
  is clear is the failure this bullet exists to prevent; so is going looking
  for a Listing to remix, which the change request did not ask for.

  When part of the request is beyond the platform (a timer that has to fire
  with nobody watching, say), build the parts within reach — the field, the
  rule as a computed or a command someone runs — and name the limit. Naming a
  limit never replaces building the rest: a change-request reply that writes
  nothing is unfinished.
- **Base-realm imports are the baseline, not the target.** Importing from the
  base realm and `@cardstack/boxel-ui` is what every card already does. This
  skill is about what you add on top.

## Self-audit before finishing

Re-read what you built. For everything you authored from scratch:

- Which reuse operation did I answer it with — part, instance, or Listing?
- Did I copy anything I could have referenced? An install or a remix should
  trace back to something the user asked to own.
- If I authored instance JSON, did I check whether the catalog already ships one?
- Does every refusal name its mismatch, and is every real gap recorded?
- If this reply answers a change request, did it write the change? Explaining
  why the catalog part doesn't fit is the start of the work, not the end.
- Does every number my reply states come from the index or from a catalog
  computation, or did I type it? Did I read anything the operation I chose
  didn't need?

And of what you said: did I end on a question the workflow had already
answered?

If the honest answer to any of these is "I didn't look", that thing needs
replacing with its catalog equivalent. Only then is it done.

## Related

- `boxel-ui-component-discovery` — the specialized front-end for UI primitives;
  use it whenever the task is writing template UI. This skill is the general form.
- `catalog-listing` — install / remix / update mechanics for Listings.
- `boxel/references/enumerations.md` and
  `boxel-patterns/patterns/organize-atomic-field-factory` — fields built by a
  factory, and how a usage overrides its defaults.
- `boxel` — CardDef / FieldDef authoring, query syntax.
