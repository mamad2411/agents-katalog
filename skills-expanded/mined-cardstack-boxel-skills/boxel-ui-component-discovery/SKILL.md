---
name: boxel-ui-component-discovery
description: MANDATORY before writing any UI in a `.gts` template, including a quick fix to an existing card (turning a styled span or div into a button, wiring a dead control, a design-review fix) and the reuse search design-review runs for each gap. Search the catalog for a component Spec and reuse it — Pret UI first, boxel-ui only where Pret UI has no equivalent yet. Fall back to raw HTML only when no matching spec exists, and surface the gap when you do.
boxel:
  kind: skill
  tools:
    - codeRef:
        module: '@cardstack/boxel-host/tools/run-realm-code'
        name: default
---

# Boxel UI Component Discovery

## Mandatory rule

Before you write any UI in a `.gts` template — anything you'd describe
as a UI primitive (button, input, dropdown, modal, tooltip, pill, menu,
accordion, …) — **you must first search the catalog for an existing
component Spec and reuse it.** The catalog holds two component
libraries:

- **Pret UI** — the spec's `ref.module` starts with
  `@cardstack/pretui/components/`. This is the default for every
  control and display primitive.
- **boxel-ui** — the spec's `ref.module` is
  `@cardstack/boxel-ui/components`. Use one only when no Pret UI spec
  covers the primitive (layout shells such as `CardContainer` and
  `FittedCard`, `KanbanPlane`, `FilterList`, …).

Tell the two libraries apart by `ref.module`. When both libraries
match, use the Pret UI one. To see which boxel-ui components a Pret UI
component replaces, use the replacement table in
`boxel-ui-guidelines/references/use-boxel-ui-components.md`.

- A matching spec exists → import it via its `ref` and follow
  its documented API (step 3 says where that lives for each library). No raw `<button>`, `<input>`,
  `<textarea>`, `<select>`, `<details>`, etc. Visual styling — even
  unconventional aesthetics — is never a reason to drop down to raw
  HTML. Restyle it in the order of
  [`restyle-component.md`](references/restyle-component.md): theme tokens, documented
  attributes and CSS variables, then (Pret UI only) a CSS rule of your own.
- No spec matches → write minimal idiomatic HTML and record the gap
  where your workflow keeps notes (tell the user, or note it on the
  task you are working), so the gap is visible. Don't invent a
  `@cardstack/pretui/components/…` or `@cardstack/boxel-ui/components`
  import that wasn't in the search results — names not present in the catalog don't exist for your
  purposes.

This rule is intentionally not a fixed HTML→component mapping. The
catalog's inventory changes over time and the spec readMe is the source
of truth for what's available and what each component is called.

## Procedure

1. **Enumerate first.** Before any search, read the brief and your
   planned template and list every UI primitive it implies — in plain
   language ("button", "dropdown", "tag-style indicator", "expandable
   section") — **and every structure**: app frame, navigation, panel
   layout, KPI or stat, chart, table, empty and loading state. The
   partial-compliance failure mode is "agent finds one match, uses it,
   hand-rolls everything else" — enumerating up front prevents it.
   Dashboards and tools hand-roll their frame when only primitives are
   searched.

   | App type | Search terms (not component names; the catalog decides) |
   |---|---|
   | Dashboard, admin | app shell, sidebar, dashboard grid, stat, chart, data table |
   | Data tool, back-office | data grid, filter set, form layout, split panes |
   | Mobile app | bottom nav, sheet, tabs |
   | Landing page | hero split, cta band |

   Give every structure hit a disposition in the reply: adopted, or
   refused with a reason (for example, on a consumer app: "four
   destinations, so top tabs per `layout-gravity.md`"). On an admin,
   dashboard or back-office surface the sidebar is not optional: it is
   the shell `surface-types.md` sets, so adopt the app shell or name the
   catalog Spec that replaces it.

2. **Query the catalog once, broadly.** Use the catalog realm for the
   environment you are working against — take it from your context if
   one is provided, otherwise list the realms available to your session
   (`npx boxel realm ls` from a CLI session) or ask; do not invent a host.

   ```json
   {
     "filter": {
       "on": { "module": "@cardstack/base/spec", "name": "Spec" },
       "eq": { "specType": "component" }
     }
   }
   ```

   Run the filter through your session's search transport. Write it
   card-rooted (`on`/`type` anchors, bare field names) like every other
   card query — the transport translates it to the search endpoint's
   wire form itself; never hand-write `item.`-prefixed paths.

   - **From a CLI session**, `npx boxel search --realm <catalog-realm-url>
     --query '<filter-json>' --json` returns the full inventory (well
     over 100 specs across both libraries) in one call. Match each item in your enumeration to a result
     by reading `attributes.cardTitle` and `attributes.cardDescription`.
   - **In an assistant room, search in one `run-realm-code` script**
     with `realm.entries.search(query, { realms, scope: 'cards', limit })`.
     This skill declares the `run-realm-code` tool. The sandbox rules
     for the script are in `source-code-editing`. Pass `realms` with only
     the catalog realm: without it, the search also reads every
     workspace the user can read, and a component Spec that a user
     wrote in a workspace is not a catalog component. The catalog realm
     is `@cardstack/catalog/`, or the catalog URL from your context.
     Run one query per enumerated item, all in the same script. The
     realm calls of a run go one at a time, also in `Promise.all`, and
     a run has 55 seconds. If a run with many items stops at that
     limit, split the items across two runs. Add
     `{ "matches": "<the item's plain-language name>" }` beside the
     `specType` constraint, and return only what you will use. Each
     entry is `{ url, kind, ref, specType, cardTitle, cardDescription,
     name, readMe }`. The fields are at the top level, not under
     `attributes`, and `readMe` is the full readMe. An entry does not
     carry the spec's other fields or its links (for example the
     `writeup` link of a Pret UI spec):

     ```js
     const items = ['button', 'text input', 'dropdown', 'modal'];
     const found = {};
     for (const item of items) {
       const { entries, total, truncated, incomplete } =
         await realm.entries.search(
           {
             filter: {
               on: { module: '@cardstack/base/spec', name: 'Spec' },
               every: [{ eq: { specType: 'component' } }, { matches: item }],
             },
           },
           { realms: ['@cardstack/catalog/'], scope: 'cards', limit: 10 },
         );
       found[item] = {
         total,
         truncated,
         incomplete,
         specs: entries.map((e) => ({
           title: e.cardTitle,
           description: e.cardDescription,
           ref: e.ref,
           readMe: e.readMe,
         })),
       };
     }
     return found;
     ```

     Check `total`, `truncated` and `incomplete` for each item before
     you choose. `total` is how many specs match. `truncated` is `true`
     when more specs match than the answer holds; a search returns at
     most 50 entries and does not page. Then the Pret UI spec can be
     one of the specs you did not see, so raise `limit` (at most 50) or
     narrow the query, and search again before you choose a boxel-ui
     spec or declare a gap. `incomplete` is `true` when a realm did not answer;
     search again before you declare a gap. The script above returns
     each spec's `readMe`, so step 3 needs no second search for a
     boxel-ui spec.

   Narrow with `contains` on the title or `matches` (full-text over the
   readMe) if a query is noisy. See `boxel/references/query-systems.md`
   for full query syntax.

3. **Read each chosen spec's API.**
   - **Pret UI:** the `readMe` holds only the import line. The
     contract (args, accessibility, theming knobs) is the component's
     write-up, the `<name>.md` file beside the module. Worked examples
     are in `<name>.usage.gts`. Read the write-up before you use the
     component. The search entry does not carry its path, so make the
     path from `ref.module`: for `@cardstack/pretui/components/button`
     the write-up is `components/button.md` in the Pret UI realm. Read it
     in a second `run-realm-code` run with `realm` set to the Pret UI
     realm's full `https://` URL; `realm` refuses the `@cardstack/pretui/`
     prefix. A run can read a realm
     that the user can only read. Read all the write-ups you need in
     that one run. If the run is refused, choose from the spec's
     `readMe` and `cardDescription`, and tell the user that you could
     not read the write-up:

     ```js
     const writeups = {};
     for (const p of ['components/button.md', 'components/select.md']) {
       writeups[p] = await realm.fs.readText(p);
     }
     return writeups;
     ```
   - **boxel-ui:** the `readMe` has the Import line, the API
     table (arg / type / required / default / options / description),
     an example snippet, and CSS variables. It comes in the search
     entry; no second read is needed.

4. **Use the components.** Translate each `ref` to an
   import line directly (the readMe gives you the exact statement).
   Copy an example as a template and substitute your own args following
   the contract or API table. Never carry boxel-ui arg names (`@kind`,
   `@as`, `@size='extra-small'`) onto a Pret UI component. Required args must be
   present; defaults are listed for every optional arg.

## A component that does not fit the app's look

The component supplies behaviour and accessibility; the app's theme and Look supply the style. Restyle through its theme tokens, documented attributes and CSS variables, then, for a Pret UI component, a CSS rule of your own, judged from a capture. The steps: [`restyle-component.md`](references/restyle-component.md).

## Self-audit before finishing

Re-read your finished template. For each interactive or form-shaped
HTML element it contains, ask: would I have searched the catalog for
this if I were writing it from scratch? If yes, did I? Replace any raw
HTML primitive that has a spec'd equivalent, and any boxel-ui component
that has a Pret UI replacement, re-run lint/parse, and
only then call it done. Raw `<input>` / `<select>` / `<details>` lint
and parse clean — only this audit catches them.

## Related

- `catalog-reuse` — the general form of this discipline: search the
  catalog for an existing card, field, command, app, or asset before
  building one. This skill is the specialized front-end for UI
  primitives in a `.gts` template; reach for it whenever the task is
  writing template UI.
