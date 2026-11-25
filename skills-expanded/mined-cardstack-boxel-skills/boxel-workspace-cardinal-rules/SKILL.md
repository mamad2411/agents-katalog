---
name: boxel-workspace-cardinal-rules
description: Silent-failure traps in Boxel card authoring — rules that pass lint and often indexing, then corrupt the realm index, crash at render, or drop data with no error (DateField vs DateTimeField formats, external URLs in relationship links, and more). Check every card and field against this list before finishing.
boxel:
  kind: skill
---

# Boxel cardinal rules — silent-failure traps

Rules discovered the hard way in a downstream Boxel workspace: each one passes lint and
often passes indexing too, then breaks silently — corrupting the realm's index,
crashing at render, or dropping data with no error. Check every card/field you write
against this list before finishing an issue.

The numbers below are local to this file. The `boxel` skill carries a separate Cardinal
Rules table with its own numbering, and that is the one a bare "Cardinal Rule N"
citation in `index.md`, `CLAUDE.md`, or `AGENTS.md` refers to — several of those numbers
are past the end of this list and do not name a rule here.

## 1. DateField vs DateTimeField value format

`DateField` values are `YYYY-MM-DD` (no `T`). `DateTimeField` values are full ISO
datetimes (`2026-07-16T14:30:00.000Z`, with `T`). Putting a datetime string in a
`DateField` (or vice versa) passes lint and indexes fine, then **crashes at render**
with `RangeError: Invalid time value` when a user actually opens the card. Naming
convention to follow when picking the field type: a `*At` suffix (`createdAt`,
`publishedAt`) means `DateTimeField`; a `*Date`/`*On` suffix or bare `dob` means
`DateField`.

## 2. Never put an external URL in `relationships.<field>.links.self` — and never a realm URL in a string field

If a `linksTo`/`linksToMany` field's JSON `links.self` points at a URL the indexer
can't parse as a card (an external website, an image CDN URL, anything not a card
resource), **the failed parse poisons the JSONB write and rolls back the WHOLE
REALM's indexing transaction** — every other file in the same push silently fails to
index too, with no error pointing at the actual bad file. For an external image/URL,
use the pair pattern instead: `linksTo(ImageDef)` (or a similar file/media field) +
`contains(UrlField)` as two separate fields, never one relationship pointing straight
at an external URL.

**The rule cuts both ways.** If a field's value is the URL of a card instance or a
realm file — an absolute realm URL, a relative path like `../Theme/foo`, or any URL
a realm serves — model it as `linksTo` / `linksToMany` (a `FileDef` subtype for
files), never as a `StringField` or `UrlField` attribute. The string version writes
fine, indexes fine, and even renders as a clickable link — then rots silently: the
index never invalidates the referrer when the target changes, broken-link
diagnostics can't see it, `<@fields.X />` can't render the target, and queries can't
traverse it. When the target moves or is deleted, nothing reports the dangling
reference. Two carve-outs where a string is correct: a `FileDef` subtype's own
`id`/`url`/`sourceUrl` descriptor fields hold the realm file URL as strings by
design, and a curated public path routed via `hostRoutingRules` (a nav target like
`/about`) is a routed path, not a resource identifier. Everything else `UrlField`
holds should be an external (non-realm) URL. Details:
`boxel/references/base-field-catalog.md` "Realm-resource URLs — always a
relationship, never a string".

## 3. `linksToMany` JSON uses indexed top-level keys, never an array

Correct:

```json
"relationships": {
  "items.0": { "links": { "self": "../foo" } },
  "items.1": { "links": { "self": "../bar" } }
}
```

Wrong (rejected outright — "instance ... is not a card resource document"):

```json
"relationships": {
  "items": { "links": { "self": ["../foo", "../bar"] } }
}
```

## 4. Never inline media or binary bytes in card JSON

No `data:` URIs, `blob:` URIs, base64, or raw media bytes in any JSON string field or
attribute. Store media as a realm file linked via `linksTo(FileDef)` (or a FileDef
subtype: `ImageDef`, `CsvFileDef`, etc.) instead — never embed the bytes directly in
the instance JSON.

## 5. Card searches are capped, and empty until the realm is known

A card search with no `realms` targets the card's own realm; before that realm is
known it searches nothing, so don't treat the empty first result as an answer. A card
search is capped at 100 rows and 2 realms, and asking for more returns *nothing*, not
a trimmed page — `boxel/references/query-systems.md` "Limits and ceilings".

## 6. Query-filter shape: `type` selects instances, `on` only scopes predicates

To select every instance of a type, filter on `{ type: <ref> }` directly — never wrap
it in `{ on: <ref> }` alone (`on` only scopes _other_ predicates like `eq`/`contains`;
a bare `{ on: ref }` with nothing else matches nothing). Build refs with a `codeRef()`
helper, not a manually-constructed object.

## 7. Don't push more than ~30 files through one atomic batch to a fresh realm

Large atomic pushes (30+ files via a single bulk-write endpoint) can report success
while silently dropping some files' indexing jobs. For bulk kit/asset installs, push
in smaller batches and verify each batch's expected file count actually shows up in a
realm search before pushing the next batch.

## 8. NEVER curl / HTTP-GET a base card's module reference to inspect it

Base card modules are addressed by the canonical `@cardstack/base/` prefix
(`@cardstack/base/theme`, `@cardstack/base/card-api`,
`@cardstack/base/cards/structured-theme`, etc.). Those are **loader-resolved module
references, not fetchable HTTP resources** — there is no URL to GET. The older URL
spelling `https://cardstack.com/base/...` still resolves at runtime, but do not write it
and never fetch it: `cardstack.com` is a marketing site, so a direct GET or a realm op
(`_mtimes`, `boxel file read`) against `cardstack.com/base/...` returns a generic
Webflow **404 HTML page** (`data-wf-domain=... %%PUBLISH_URL_REPLACEMENT%%`), NOT the
card. Do not keep retrying it — that page will never become the schema. To learn a base
card's fields/shape, use the **`get_card_schema` tool** (it resolves through the realm
server), or read an existing instance of that card already in the target realm. Same
rule for any published `*.boxel.site` / `*.boxel.build` URL: those are Webflow-published
sites, not realms — never point realm operations at them.

Also: many base cards are **default exports**, so the schema ref is `name: "default"`,
NOT the class name. The base **Theme** card is the default export of
`@cardstack/base/theme` (the module is `export default Theme`) — query it as
module `@cardstack/base/theme`, name `default` (querying `#Theme` fails).
`StructuredTheme` is likewise the default export of `base/structured-theme`. When a
`get_card_schema` call fails with "named export is a CardDef", retry with `name:
"default"` before assuming the card is unreachable — do NOT fall back to curling a URL.

## 9. Never call `serializeCard(model)` from a render getter

Serializing the card's own model inside a template-facing getter (isolated/embedded
component code) can appear to work, then fails in two environment-dependent ways:
in prerender it throws during render (instance-error 500, the card drops out of
prerendered listings), and in interactive sessions it raises the deterministic
IDResolver error `conflicting instance id in store` — the serialize path re-registers
the instance under a conflicting local id. When a template needs a JSON:API-shaped
view of the card, reconstruct the shape from `@model` fields instead of calling
`serializeCard`.

## 10. `linksTo` fields never appear in `attributes` — not even as `null`

A `linksTo` field is serialized under `relationships`, keyed by its field path — for a
linksTo nested inside a contained field, a dotted key: `"cardInfo.theme": { "links":
{ "self": "../Theme/foo" } }`. An empty link is `{ "links": { "self": null } }`, or
omit the key entirely. Writing `"cardInfo": { "theme": null }` (or any value for the
link) into `attributes` passes lint and writes successfully — then **every read of the
instance throws** `linkTo field 'theme' cannot deserialize non-relationship value null`
until the raw JSON is repaired by hand.

## 11. Any function a template *calls* must be an arrow-function property, never a class method

When a template calls a component function — as a helper (`{{if (this.isActive
note) ...}}`) or via `{{fn}}` — Glimmer invokes the plain function **without
binding `this`**. A class body is always strict mode, so inside a class *method*
`this` is `undefined` and the first property access throws — **during render**,
which poisons Ember's renderer beyond recovery: the whole application freezes
and only a page reload brings it back. The code passes lint, often passes
prerender (the crash can hide behind interaction-dependent branches), and event
handlers wired with `{{on}}` mask the pattern because the same mistake there
merely breaks one handler instead of the app. Write every template-invoked
function as an arrow property:

```ts
// wrong — crashes the app at render
isActive(note: string) { return this.activeNotes.has(note); }
// right
isActive = (note: string) => this.activeNotes.has(note);
```

Getters are safe: the template reads them off `this` (`{{this.safeTitle}}`,
`{{#if this.showComments}}`), so they never lose their receiver — the trap is
only functions the template detaches and calls. `@action` methods also bind
correctly and are safe in call position; arrow properties are the convention
in this repo.

## 12. No `:global()` in a card's CSS

Card code is compiled with `:global` turned off (to stop a card's styles from
escaping its scope). The compiler only warns, on the server, and leaves
`:global(...)` in the output; the browser rejects the selector as invalid, and
**an invalid selector drops the whole rule, so every other selector in the same
comma-separated list goes with it**:

```css
/* both selectors are dropped; .plain loses its style too */
.wrap td :global(button.x), .plain { color: var(--primary); }
```

The card compiles, lint passes, the correctness check passes, and the styles
never apply. The host's and the component libraries' own CSS uses `:global`;
card code cannot copy it. Use instead:

- **A class on the element or component.** A class on a component that passes
  `...attributes` through (Pret UI and boxel-ui controls, and a linked or
  compound field invocation such as `<@fields.link class='…' />`) lands on its
  root and is reachable with a plain scoped selector. Pret UI's own styles are
  in cascade layers, so that rule wins without extra specificity. A class on
  `Select` lands on its wrapper, so reach its trigger with
  `:deep(.pretui-selecttrigger)`. A boxel-ui component is restyled through
  its knobs, not a rule on its classes. A primitive leaf field
  (`<@fields.title class='…' />` on a `StringField`) renders bare text, so the
  class lands nowhere; wrap it in an element of your own.
- **`:deep()`** for DOM you neither render nor can put a class on (the
  internals of a component or a host shell). It compiles to a scoped ancestor
  and an unscoped descendant, which the browser accepts.

Grep for `:global(` before finishing any card.

## 13. Build every `Intl` formatter once, at module scope — never per call

Each `new Intl.DateTimeFormat(…)` holds roughly 15–30 KB of ICU memory **outside
the JavaScript heap**. The garbage collector does not count that memory, so it
feels no pressure to free it. A date formatter built inside a function that
runs per row, per render, grows the browser tab by hundreds of MB per second
while the JS heap stays small: the render times out, the tab is killed, and a
prerender of the card can take down every other card rendering beside it. In
Chrome, 200,000 constructions grew a tab from 34 MB to 5.8 GB; one shared
formatter doing the same 200,000 calls grew it by nothing. The other
formatters (`Intl.NumberFormat`, `RelativeTimeFormat`, `Collator`,
`PluralRules`, `ListFormat`) hold less memory, but each construction still
costs about 40 `format` calls. Lint passes, sample data renders fine, and the
card fails only once real data piles up.

Inside a getter, `computeVia`, helper, loop, `map` / `filter` / `sort` /
`reduce` callback, or any function a template calls (or one called from it),
never:

- construct an `Intl` formatter (`new Intl.DateTimeFormat(…)`, or the same
  call without `new`);
- call `toLocaleString` / `toLocaleDateString` / `toLocaleTimeString` with
  options, or `localeCompare` with options. Each such call builds a formatter
  or collator internally and throws it away. That costs CPU on every call
  (about 30 times a shared formatter's `format`) rather than memory, but
  per row and per render it adds up the same way.

Build each formatter once at module scope. When the locale, time zone or
currency comes from the data, cache formatters in a module-level `Map` keyed by
the options:

```ts
// wrong — a new formatter for every row, on every render
const dayKey = (d: Date, timeZone: string) =>
  new Intl.DateTimeFormat('en-CA', { timeZone, year: 'numeric', month: '2-digit', day: '2-digit' }).format(d);

// wrong — rebuilds a formatter internally on every call
const dayLabel = (d: Date) => d.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });

// right — module scope: one formatter for the whole module
const dayLabelFormat = new Intl.DateTimeFormat('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
const dayLabel = (d: Date) => dayLabelFormat.format(d);

// right — options vary with the data: one formatter per time zone, ever
const dayKeyFormats = new Map<string, Intl.DateTimeFormat>();
function dayKey(d: Date, timeZone: string) {
  let format = dayKeyFormats.get(timeZone);
  if (!format) {
    format = new Intl.DateTimeFormat('en-CA', { timeZone, year: 'numeric', month: '2-digit', day: '2-digit' });
    dayKeyFormats.set(timeZone, format);
  }
  return format.format(d); // YYYY-MM-DD in that time zone
}

// right — sorting by a locale-aware compare: one collator, not one per comparison
const byName = new Intl.Collator('en', { sensitivity: 'base' });
people.sort((a, b) => byName.compare(a.name, b.name));
```

Safe on any path:

- `toLocaleString()`, `toLocaleDateString()`, `toLocaleTimeString()` and
  `localeCompare(other)` with no options and at most one fixed locale
  (`n.toLocaleString()`, `d.toLocaleDateString('en-US')`,
  `a.localeCompare(b)`), which reuse a cached formatter or collator. A locale
  that changes from row to row defeats that cache, so build those formatters in
  a module-level `Map` as above.
- The `formatDateTime`, `formatCurrency`, `formatNumber` and
  `formatRelativeTime` helpers, which cache their formatters.

For a card that formats dates, numbers or currency, grep for `Intl.`,
`toLocale` and `localeCompare` before finishing. Every hit is at module scope,
inside a module-level cache, or a safe call from the list above.
