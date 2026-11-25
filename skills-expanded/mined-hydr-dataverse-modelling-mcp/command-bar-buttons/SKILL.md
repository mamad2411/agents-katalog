---
name: command-bar-buttons
description: Add, change or remove a button on a Dataverse / Dynamics 365 table command bar — classic RibbonDiffXml (ribbon_get, ribbon_add_button, ribbon_remove_button) or modern commands in the appaction table (command_*). Covers which mechanism to pick, how the ribbon is really stored, the failures that return success while the button silently never appears, and a deployed button change that never reaches the users (ribbon_diagnose, ribbon_sync_unmanaged_layer, ribbon_refresh_client_metadata). Use when the user wants a button, ribbon or command bar entry on a table, form or grid, when a button they added is missing, mislabelled or vanishes on row selection, or when users still get the old behaviour after a deployment.
version: 1.0
---

# Buttons on a Dataverse command bar

Two mechanisms exist and picking the wrong one costs a day. Full reference, all of it verified
against a live org: `${CLAUDE_PLUGIN_ROOT}/docs/tools/buttons-classic-vs-modern.md`. Read it before
the first write — the summary below is a router, not a substitute.

## Pick the mechanism first

**Does visibility depend on what is selected in a grid?**

- **Yes → classic ribbon.** `SelectionCountRule` is entity-bound and self-contained. Tools:
  `ribbon_get`, `ribbon_add_button`, `ribbon_remove_button`. One limit to plan around: a `Minimum`
  above 1 is **not enforced** — the button is enabled on a single selected row too, so the lower bound
  has to be re-checked in the handler and server-side.
- **No → either works.** Modern commands are Microsoft's direction; classic stays versionable as XML.

The modern equivalent of a selection rule is a Power Fx formula, and that formula must live in a
canvas component library. **No API can create one** — only the Command Designer opened *from an app*,
which turns a table-level button into an app dependency that has to be dragged through every
environment. That is the whole argument for classic here, and it is on merit, not nostalgia.

**Classic ribbons still render.** An `appactionmigration` row with `ismigrated = True` does not mean
classic `RibbonDiffXml` is ignored. Both mechanisms render side by side on the same table.

## Before you write

- There is **no Web API that writes a ribbon**. `ribbon_add_button` does a solution round-trip
  internally. Do not hand-roll it — steps 4, 5 and 8 of that round-trip are load-bearing in
  non-obvious ways.
- **A non-empty `<CustomActions>` import replaces the entire collection.** An import naming only your
  new button deletes every other one. `ribbon_add_button` re-sends the existing nodes and reports
  `lostCustomActionIds`; a hand-built import has no such guard.
- An **empty** `<CustomActions />` removes nothing. Deletion goes through `ribbon_remove_button`,
  which deletes the stored `ribbondiff` / `ribboncommand` / `ribbonrule` rows.
- **`ribbondiff` holds more than CustomActions.** Localized captions live there too, as `<LocLabel>`
  nodes with `difftype = 3`, and they belong in `<LocLabels>` — not in `<CustomActions>`, where the
  importer rejects them with *"Missing Location Attribute … for CustomAction element with
  Id=….LabelText"*. `ribbon_get` returns them separately (`customActions` / `locLabels` /
  `otherDiffs`), and `ribbon_remove_button` deletes a button's label rows with it — an orphaned one
  breaks the next add on that table. Any table that has seen the Ribbon Workbench has such rows.

## Failures that return success

Each of these logs nothing and leaves you with a missing or wrong button. Check them first when
something does not appear:

1. **Invalid `fontIcon`** (e.g. `$clientsvg:Money`) — modern command never renders. `command_create`
   validates; `command_list_icons` prints the known-good set.
2. **A caption the client cannot resolve** — and a *literal* `LabelText` is one: it is stored and read
   back perfectly, and the Unified Interface draws no button at all. A `$LocLabels:` reference without
   its `<LocLabel>` node renders the raw token instead. The configuration that works is a `<LocLabel>`
   node plus a reference, which is what `ribbon_add_button` now writes — pass the caption as `label`.
   Watch `captionLanguageCode` in the result: a caption under a language the org does not use is just
   as invisible as no caption. It defaults to the language the table's other buttons use.
3. **~~`ModernImage="$webresource:….svg"`~~** — this was in the list and is wrong. Six buttons on
   `invoice` carry such a reference and all of them render; the disappearance came from the caption
   (point 2). The rejection has been removed from the tool.
4. **A `Location` that does not exist** — nothing renders. `ribbon_get` with `includeLocations=true`
   lists the valid ones.
5. **Grid modern command with `visibilitytype = 0`** — vanishes as soon as rows are selected. The most
   common "my button disappeared" report.
6. **Wrong app.** Custom commands do not render in `d365default`. Check in a real app.
7. **An unmanaged ribbon layer on the target overrides the deployment.** Every managed import of the
   command is stored and never takes effect. It cannot be removed — `RemoveActiveCustomizations` refuses
   ribbons (`0x8004f059`) — only overwritten with `ribbon_sync_unmanaged_layer`.
8. **The client keeps receiving the old command.** Database and compiled ribbon are right; publishing
   the ribbon, the table, the app or everything does not rebuild what `GetClientMetadata` serves. A
   change to the table's own metadata does: `ribbon_refresh_client_metadata`.

## Users still get the old behaviour after a deployment

Go through the levels in this order and stop at the first that is wrong. `ribbon_diagnose` does all
three and names the failing level:

1. **Stored** — does an unmanaged (`Active`) layer differ from every managed copy?
   → `ribbon_sync_unmanaged_layer` with `sourceSolution` = the managed solution that holds the intended
   version. Run it with the default `dryRun=true` first and read the plan.
2. **Compiled** — does `RetrieveEntityRibbon` show the stored version? → publish the table.
3. **Delivered** — does each app's client receive the compiled version?
   → `ribbon_refresh_client_metadata`, then have the users reload.

**Never edit a ribbon directly on a staging or production environment** (Ribbon Workbench, a manual
import). That is how the unmanaged layers in point 1 come about, and they cannot be taken back. Before
and after deploying a ribbon change to such an environment, run `ribbon_scan_unmanaged_layers` there:
any command under `commandsOverridingManaged` will ignore the deployment.

`solution_remove_active_layer` is for other components. On a table it removes the table's unmanaged
properties, but not its unmanaged ribbon.

## Verifying — the part that actually costs the time

Separate **stored** from **drawn**. `ribbon_get` answers the first; only a browser answers the second.
Never let one stand in for the other. In between sits **delivered** — what the server hands the
client — which `ribbon_diagnose` reads per app, so a stale server cache shows up without a browser.

- **Read the whole command bar.** Do not filter for the caption you expect — a mislabelled button is
  exactly the case you would then miss. This once produced the conclusion that classic ribbons no
  longer worked at all, when the button had been rendering the whole time as `LabelText`.
- **Compare against a reference button you know works — on the same table.** If yours is missing and
  the reference renders, the fault is in your definition. If neither renders, you are in the wrong app.
  The table matters: comparing an `invoice` button against `sample_purchaseorder`, where literal captions
  work fine, sends you through Location, TemplateAlias, Sequence and cache while the cause is the label.
- **Searching the compiled ribbon for your CustomAction id always fails.** `RetrieveEntityRibbon`
  returns the ribbon with the diff already applied — it contains no `<CustomAction>` elements at all.
  Search for the button id and the caption.
