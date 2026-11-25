---
name: deevy-ui
description: How deevy's web UI (apps/web) is designed and built — the visual language for Humans, Agents and Gates, the navigation model, which shadcn registries and editor are used and why, and the test contracts a screen must keep. Load before touching anything under apps/web/src or apps/web/tests.
---

# deevy UI

deevy is project management where Humans and Agents are peers on the same Issues (CONTEXT.md). The UI's one
memorable idea: **you can always tell who is a Human and who is an Agent, and what is waiting on a Human.**
Everything else is quiet. This skill records the decisions of the 2026-09 redesign
(`docs/plans/ui-redesign.md`); each slice of that plan appends what it settled. Read `shadcn` (component
rules) and `frontend-design` (design process) beside it.

## Where things are

| You want                                 | Look at                                                                                                           |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| tokens, type, both themes                | `apps/web/src/index.css`, `/dev/tokens` on a dev instance                                                         |
| the frame, sidebar, top bar, member menu | `routes/shell.tsx`                                                                                                |
| ⌘K, shortcuts, `?`                       | `components/command-palette.tsx`, `lib/shortcuts.ts`, `components/shortcuts-sheet.tsx`                            |
| a list screen                            | `components/data-table.tsx`, `components/issue-filters.tsx`, `routes/issues/list.tsx`                             |
| the Issue, peek or page                  | `routes/issues/issue.tsx`, `components/side-peek.tsx`, `gate-controls.tsx`, `activity-stream.tsx`, `run-card.tsx` |
| the editor                               | `components/markdown-editor.tsx` (Tiptap, markdown in and out), `components/markdown.tsx`                         |
| Inbox, Board, Project                    | `routes/inbox.tsx`, `routes/projects/board.tsx` (`components/reui/kanban.tsx`), `routes/projects/*`               |
| a Settings page                          | `components/settings-page.tsx`, `routes/settings/*`, `settingsNav` in `routes/settings/layout.tsx`                |
| the chips and badges                     | `components/member-chip.tsx`, `state-badge.tsx`, `run-status.tsx`, `kbd-hint.tsx`                                 |
| everything outside the shell             | `App.tsx` (`SignInFrame`, `DevSignIn`)                                                                            |
| the accessible names tests rely on       | "Test contracts", at the end                                                                                      |

## Ground rules

- Vocabulary is CONTEXT.md's, in code, copy and tests: Member, Human, Agent, Sponsor, Workspace, Project,
  Issue, State, Gate, Run, Activity, Document, Event, Notification, Channel. "Board" is the column view of a
  Project, never a Project. Never "ticket", "task", "status", "user", "bot".
- **Base UI, not Radix.** `apps/web/components.json` is `"style": "base-mira"`. Custom triggers use
  `render={<Link … />}` (and `nativeButton={false}` on a Button that renders an anchor — without it Base
  UI warns on every render, which is what CI's stderr shows), never `asChild`. `nativeButton={false}`
  gives the anchor a button role, so navigation a test finds as a `link` (the not-found page's ways out) is
  a `<Link className={buttonVariants(…)}>` instead: a real link dressed as a button.
  Nothing under `apps/web` may import `@radix-ui/*`.
- Work from `apps/web` so the `shadcn` skill's `shadcn info` finds `components.json`. Add components with
  `pnpm dlx shadcn@latest add <item> --overwrite`; it rewrites `pnpm-workspace.yaml` and pins versions, so
  move new dependencies to the catalog and restore the file's comments.
- Markdown is the source of truth for Documents, descriptions and comments (Agents write it over MCP). An
  editor may render it richly; it stores markdown and never a second format.
- Every screen is verified in the browser through the stubbed dev instance (below), in both themes.

## Running the app without an OAuth App

`DEEVY_DEV_STUB_OAUTH=1` makes the Node server import `apps/web/scripts/stub-oauth.js` — the same stub the
acceptance walk and the Workers smoke prepend to their bundles — so the OAuth `code` is the email address and
the signed-out page offers "Sign in as this email". It stands in for the client pairs too, so an environment
that configures no provider still offers all four buttons: GitHub, Google, GitLab and one generic OpenID
Connect entry, which is what the signed-out screenshots show. Refused under `NODE_ENV=production`. The Worker
never has it. `health.ping` reports `devSignIn`, which is how the SPA knows to show the form.

```bash
# in .claude/launch.json as "dev:stub": the stubbed instance on its own database file
DEEVY_DEV_STUB_OAUTH=1 DEEVY_DATABASE_PATH=./data/stub.sqlite vp run -r --parallel dev
DEEVY_DATABASE_PATH=./data/stub.sqlite vp run server#seed        # a Workspace worth looking at
```

`vp run server#seed` (`apps/server/src/seed.ts`, a second `vp pack` entry) signs in the admin
(`DEEVY_ADMIN_EMAIL`) and `grace@<the admin's domain>` through the stub, creates the Agents `Planner` and
`Builder` sponsored by the admin, two Projects (`DEV` with the default six States, `OPS` with Todo/Doing/Done),
~35 Issues, Documents, comments with mentions, Runs in every status, Gate rulings, Links, a Slack Channel,
routing and a webhook — all through the operations, so the inbox and the Event log fill themselves. It
refuses a database that already has a Project unless `--force` (which removes the file). Sign in as either
Human with the dev form.

## Registries

Two hard constraints on anything added from a registry: **an open-source licence with no licence key**, and
**no `@radix-ui/*` import**. Run `pnpm dlx shadcn@latest view <item>` before `add` and read the imports.
Verified 2026-09-05:

| Namespace                                                          | Licence                 | Use                                                                                                 | Do not use                                              |
| ------------------------------------------------------------------ | ----------------------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| `@shadcn`                                                          | MIT                     | everything in `components/ui`; blocks `sidebar-07`, `sidebar-08`, `login-04` as starting points     | —                                                       |
| `@reui`                                                            | MIT (free items)        | `kanban`, `data-grid` — its `/r/{style}/{name}` URL returns the Base UI build for our style         | anything with a Pro badge; never set `REUI_LICENSE_KEY` |
| `@kibo-ui`                                                         | MIT                     | `kanban`, `list`, `table`, `avatar-stack`, `status` — compose our `ui/*` + dnd-kit / TanStack Table | `relative-time` (Radix), `gantt` for now                |
| `@diceui`                                                          | MIT                     | `sortable`                                                                                          | `mention` (Tiptap's extension does it), `data-grid`     |
| `@coss`                                                            | MIT for `apps/ui` items | pattern references: `p-command-1`, `p-group-23`, `style`                                            | as our theme                                            |
| Origin UI, Magic UI, Cult UI, Animate UI, Aceternity, shadcnblocks | mixed                   | —                                                                                                   | Radix or off-brief                                      |

Every adopted file starts with a comment naming the registry, item, date and licence. New npm dependencies
go through the catalog.

## Design language (the tokens in `apps/web/src/index.css`; chosen in round 2, slice A)

- **Type.** Inter (variable, `@fontsource-variable/inter`) for UI; JetBrains Mono
  (`@fontsource-variable/jetbrains-mono`) for Issue keys, `@handles`, Event kinds, API keys, seqs, shortcut
  hints. Self-hosted; no Google Fonts. Scale 12 / 13 / 14 / 16 / 20 / 28; tabular numerals on keys and
  times. Rows 32px compact, 40px comfortable; sidebar rows 28px; radius 8px (`--radius: 0.5rem`); the spacing
  unit is `--density: 0.2625rem`, 5% roomier than Tailwind's default — every spacing utility multiplies it.
  The families, radius, density and `--tracking` are variables `@theme inline` hands to the utilities, so a
  palette review retunes them from one block, as round 2 did with a dev-only switcher (since deleted).
- **Color slots.** `--human` (sky blue) for a Human Member; `--agent` (rose) for an Agent; `--gate` (amber)
  for a Gate State and anything waiting on a ruling; `--state-backlog|active|done` for other States;
  `--primary` (indigo) for the one action colour; cool blue-gray paper and ink — the base is tweakcn's
  _clean-slate_ preset (Apache-2.0), picked by Matt from six candidates and then six variations of it. Those
  three saturated slots are the only saturated colours on a screen besides `--primary` and `--destructive`.
  Round 3 (2026-09-06) chose them as indigo's neighbours — sky & rose, with amber the one warm colour, so a
  Gate jumps — from six analogous candidates. **Labels choose among eight swatches** (`lib/label-colors.ts`:
  sky, rose, amber, indigo, green, red, slate, violet; white text on each), never a free colour.
  A Label is `LabelBadge` (`components/label-badge.tsx`): the scope as a small pill inside the badge, then
  the name — `[[epic] Agent loop]`, never `epic: Agent loop` on screen; `solid` in Settings, `outline` on
  rows and cards. The badge names itself `labelText(label)` (`epic: Agent loop`), which is what a test reads.
  Both themes; a real System/Light/Dark toggle. Round 1's warm Plex look is history (`docs/plans/ui-redesign.md`).
- **Layout.** Full-bleed frame, 240px sidebar collapsing to 48px, edge-to-edge lists with a 40px filter bar,
  a side-peek of `min(92vw, max(56rem, 45vw))` — a share of the window rather than a fixed width, wide
  enough to be the page it shows, which since Provenance means the rail too — Issue page = main + an 18–22rem
  rail with the Gate ruling card always on top. Cards only for
  things that are cards (a Run, a Channel).
- **Motion** only in answer to an action. Nothing on load.

## Navigation and keyboard (slice 1)

Primary sidebar: Inbox (the only badge) · My Issues · My Agents' Issues · All Issues · Projects (listed) ·
Settings (own area with its own sidebar: Workspace / Work / Agents and delivery / You) · the Member's chip.
`⌘K` palette; `c` new Issue; `?` shortcuts; `g i/m/a/p/s` go to; `j`/`k`/`Enter`/`o`/`Esc` in lists;
`a`/`s`/`l`/`p` pickers on a focused Issue; `⇧A`/`⇧R` open the ruling card (never commit); `⌘Enter` is the
only submit key. `src/lib/shortcuts.ts` owns a scope stack: an open Sheet, Dialog or palette owns the keys.

## What slice 1 settled (tokens, frame, palette, shortcuts)

- **Sizes live in `components/ui`.** shadcn's `base-mira` is the compact style — 12px controls, 10px badges
  and kbd, 28px buttons. deevy resizes those files (button, input, textarea, native-select, select, label,
  table, badge, kbd, sidebar, dropdown-menu, command, dialog) to a 14px control size with 32px heights,
  drops `CommandDialog`'s `top-1/3 translate-y-0` so the palette keeps `DialogContent`'s own centring
  rather than sliding to the bottom of the window as its list fills, hides `CommandItem`'s unchecked tick
  instead of leaving it at `opacity-0` — it carries an `ml-auto` of its own, and two of those in one flex row
  split the free space, which stranded a row's trailing text mid-line (both 2026-09-11), and
  strips `avatar`'s inner `after:` border, since the kind ring (`MemberChip`) is the avatar's one edge, and
  paints fields (`input`, `textarea`, `select` trigger, `combobox` chips, `input-group`) `bg-card` in light —
  base-mira's `bg-input/20` read as disabled (Matt, 2026-09-06) — with `disabled:bg-muted` now meaning it;
  dark keeps `bg-input/30`, which reads as relief there. Search wells inside popovers (⌘K, a Combobox's
  list) keep the tint; the
  root stays 16px so 1rem is 16px everywhere. Scale: `text-xs` 12px for meta and badges, `text-sm` 14px for
  everything a person operates or reads in a row, `text-base` 16px for prose, `text-xl` 20px for a page
  title. A `shadcn add --overwrite` of one of those files brings the compact sizes back — re-apply them.
- **Theme is a class.** `next-themes` (`attribute="class"`, system default) sets `.dark` on `<html>`; tokens
  live on `:root` and `.dark`, never in a media query. The Member menu in the sidebar footer holds the toggle.
- **Shortcuts** go through `src/lib/shortcuts.ts` — `useShortcut("g i", …)`, `useShortcut("mod+k", …,
{ global: true })`, `useShortcutScope(name, active)` on anything modal — never a raw `keydown` listener.
  Plain letters are ignored while typing; `mod+…` is not. `Shortcut keys="…"` (`kbd-hint.tsx`) draws one.
- **Navigation.** The primary sidebar is `routes/shell.tsx`; the Settings area's nav is `settingsNav` in
  `routes/settings/layout.tsx`, shared with the palette so a page has one name everywhere. Settings routes are
  children of the `/settings` layout route, each declared with a literal path: a helper that takes `path:
string` erases the literal and every typed `to` in the app stops compiling.
- **Palette.** `components/command-palette.tsx` on `ui/command`. This shadcn version's `CommandDialog` puts
  its children straight into the Dialog, so the cmdk `<Command>` root is ours to add inside it. cmdk itself
  depends on `@radix-ui/react-dialog` and friends — the one sanctioned transitive Radix dependency, because
  it is what shadcn ships for Base UI projects too; nothing under `apps/web/src` imports Radix directly.
- **An empty list is an `Empty`, centred in the room the page leaves.** shadcn's `Empty › EmptyHeader ›
EmptyMedia variant="icon" + EmptyTitle + EmptyDescription`, with a lucide icon that says what kind of
  thing is missing (ClipboardList for Issues, SearchX for a search, FolderKanban, ScrollText, Inbox, Users,
  Tags, Webhook…). The kit's title is `text-base` and its description `text-sm` (one step up from
  base-mira). Height flows down so the `flex-1` Empty centres: the shell's page area is a flex column, and
  every page root (`SettingsPage`, `ProjectLayout`, the Issues home, Projects) is `flex flex-1 flex-col`;
  the Settings layout's content column too. `DataTable` takes `empty={{ icon, title, description }}`; a
  Settings list composes the parts itself. Inline notes inside a detail section ("No Runs yet") stay `<p>`
  (Matt, 2026-09-06). **The words say what emptied the list**: under a filter it is "No Issues match your
  filters" with a Clear filters button (`empty.action`), never "No Issues yet"; a built-in view names
  itself ("Nothing assigned to you"); the default Open view over an all-closed list says "No open Issues"
  (one `limit: 1` query, asked only then); the Inbox's Unread filter says "Nothing unread"; the Event
  log's filters say "No Events match your filters".
- **Nowhere is a page.** `routes/not-found.tsx` is the root route's `notFoundComponent` and what the Issue
  and Project pages render when the API says `NOT_FOUND` (`isNotFound`, which the QueryClient also uses to
  skip retries): inside the shell, `h1` "There is nothing here" or "There is no Issue DEV-999", the path or
  the API's message, then Go back / All Issues / Inbox.
- **Grouped buttons.** shadcn's rule: `ToggleGroup` for buttons that toggle a state (Inbox All/Unread, the
  filter bar's Any/Humans/Agents, Open/All, List/Board, Activity All/Comments/Changes), `ButtonGroup` for
  buttons that perform actions (a State's Move up/down in the Workflow editor); `Tabs` for views of one
  thing (the Documents on an Issue). Joined ToggleGroups are `variant="outline" spacing={0}`.
  A pressed Toggle is `bg-primary/10 text-primary` with a `border-primary/30` edge (`/20` fill in dark):
  the one "selected" language the sidebar, the Settings nav and the Tabs underline already speak; the kit's
  `bg-muted` was a 1% step off the page (Matt, 2026-09-06).
  Their corners, and half the kit's `data-horizontal:`/`data-open:`/`data-checked:` styling, depend on
  `@import "shadcn/tailwind.css"` in `index.css` (the `shadcn` package is in the catalog for that one
  stylesheet), as the base-mira style prescribes. Without it those variants match nothing and the kit
  silently degrades (square toggle corners, Tabs in a row) — which is how it shipped until 2026-09-06.
- **A select lists names, not chips.** A Member in a `SelectItem` or a `SelectValue` is `user.name` as text;
  the kind comes from the `SelectLabel` of the group it sits in (Humans / Agents), never from a `MemberChip`
  (Matt, 2026-09-06). And every `SelectItem` sits in a `SelectGroup` — the group carries the padding, so
  a stray item outside one renders flush left.
- **Destructive is for what does not undo.** Delete, Remove, Revoke, Archive are `variant="destructive"`
  (base-mira's tinted one, quiet enough for a table row). Suspend and Reinstate are `outline`: a suspension
  reverses, so it is not destructive (Matt, 2026-09-06). Reject is a Gate ruling, not a deletion, and keeps
  the ruling's own styling; Reset on a draft stays `ghost`.
- **Base UI menus.** A `DropdownMenuLabel` must sit inside a `DropdownMenuGroup` (or a radio group) or the
  menu throws the moment it opens. Make a menu's trigger the DOM button itself (`DropdownMenuTrigger
className={sidebarMenuButtonVariants(...)}`), not `render={<SidebarMenuButton/>}`: a `tooltip` there turns
  the button into a Tooltip wrapper and the click has nowhere to land. `tests/shell.test.tsx` opens the menu.
- **Layout facts.** shadcn's `SidebarInset` _is_ the `<main>` landmark — a page never renders another. Under
  768px the sidebar is a Sheet behind the trigger; review screens at ≥1280px. The New Issue dialog is owned
  by `NewIssueProvider` in the shell, so the button, the palette and `c` open the same one (`useNewIssue()`).
- **Live updates.** `lib/live.ts` maps an Event's `subjectType` to the query keys it may have changed
  (`keysFor`) and coalesces invalidations per 16ms; mutations invalidate by key, never `invalidateQueries()`
  bare. `QueryClient` has `staleTime: 5_000`.
- **jsdom stubs** live in `tests/setup.ts`: `matchMedia`, `ResizeObserver`, `scrollTo`, and
  `Element.prototype.scrollIntoView` (cmdk needs it).

## What slice 2 settled (Issues home, filters, peek)

- **`issues.list` is Workspace-wide when no `projectKey` is given** (newest change first, no cursor) and
  takes `q` — an Issue key, a number, or a word of the title. Its REST path is `/issues`, with everything as
  query parameters; MCP and RPC callers name it the same as before. One list per screen, never a fan-out.
- **Filters live in the URL** (`components/issue-filters.tsx`: `IssuesSearch`, `parseIssuesSearch`), so a
  view is a link and Back undoes a filter. **Every filter is the server's** (2026-09-06, #10): `issueFilterInput(search, myId, projectKey?)` turns the URL into
  the one `issues.list` input the Issues home, the Board and the palette send — `stateName` (a name, folded
  across Projects), `assigneeKind`, `unassigned`, `sponsorMemberId` for "my Agents", `assigneeMemberId`
  for `me` — and returns null while `me.get` has not said who "me" is. Nothing folds over the page in the
  browser any more: past 200 Issues that fold lied. The list holds `ISSUE_PAGE` (200) and the server says
  `hasMore`; the page then reads "Showing the first 200 Issues. Narrow the filters to see the rest." and
  the count is "200+".
- **`components/data-table.tsx`** is hand-rolled on `ui/table`: client sort per column, group rows that
  fold, skeleton, `Empty`, `aria-selected` on the keyboard row. No TanStack Table — it went to v9 with a new
  API and this list needs none of a grid. A row's accessible name is its text.
- **`components/side-peek.tsx`** renders the whole `IssuePage` in a right Sheet, keyed by `?peek=`. Base UI
  names the dialog from `SheetTitle` (`aria-labelledby` beats `aria-label`), so a test finds it by
  `/DEV-1/`. It pushes the `peek` shortcut scope; `o` opens the full page; `Esc` closes. Since 2026-09-11 it
  is `min(92vw, max(56rem, 45vw))` wide — 45% of a desktop window, 56rem floor, 92vw ceiling, and the whole
  window below `sm` — **resizable by its left edge** (`role="separator"` named `Resize the Issue panel`,
  arrow keys and `Home` as well as a drag; the width is remembered in `localStorage` and re-clamped when the
  window changes, `lib/peek-width.ts`). That expression is the floor a drag cannot go under, and is written
  in CSS so the first paint needs no JavaScript; `peekBounds().min` is the same number for the code that has
  to reason about it. Carries **no backdrop** (`showOverlay={false}`, a deevy prop on
  `ui/sheet.tsx`) and is **never modal**. The width is load-bearing: it keeps the Issue's own container over
  `@3xl`, so the peek is the page — two columns, rail on the right, sections in the same order — instead of
  the stacked, rail-first shape a narrower panel produced. The other two keep the list behind it lit,
  readable and, on the Board, still draggable; modal-except-on-the-Board was the old rule.
- **Keyboard on a list**: `j`/`k`/arrows move `aria-selected`, `Enter` peeks, `o` opens, `Esc` clears — bound
  by the page with `useShortcut`, not by the table.
- The sidebar has My Issues (`/?assignee=me`), My Agents' Issues (Sponsors only), All Issues (`/`) and
  Projects (`/projects`); `g m` / `g a` / `g p`. The palette searches Issues from two characters.

## The Issue view (chosen 2026-09-12)

`routes/issues/issue.tsx` is **Provenance**, picked from ten layouts in `docs/plans/issue-view.md`; the side
peek mounts the same component, so the two cannot drift. Its rules: the Documents are the subject and say
who wrote them, the rail is a column and not a gutter (`@3xl:grid-cols-[minmax(0,1fr)_minmax(18rem,22rem)]`),
and the Run feed lives in that rail beside the ruling it waits on rather than under the Documents, where a
long Run pushed the conversation off the screen. The nine rejected layouts are in that document with what
each of them paid for; read it before rearranging this page.

## What slice 3 settled (the editor)

- A page can hold more than one `role="status"` (what is saving, and what a Gate is waiting on), so a test
  names the one it means.
- **`components/markdown-editor.tsx`** is the one editor: markdown in, markdown out, `mode="block"`
  (Documents, descriptions) or `"inline"` (comments, notes, answers). **No Edit/Source switch** (2026-09-12):
  a pair of tabs above every Document, description and comment was a choice nobody was making and chrome on
  every reading of them. The plain `Textarea` underneath stays mounted and **hidden** — same `value`, same
  accessible name — because Tiptap is a ProseMirror view and jsdom has no layout to type into: a test asks
  for it with `{ selector: "textarea" }` and gets the markdown exactly as stored. `⌘Enter` submits
  (`onSubmit`). Nothing in the UI reaches it; if a Human ever needs the raw markdown again, the place for it
  is the Document's `⋯` menu, not a tab strip on every editor.
- **So are an Issue's title and description** (`inline-title.tsx`, `routes/issues/issue.tsx`): no Edit
  button, no form, no second copy of the words on screen. The title is a `contentEditable` `h1` rather than
  an input dressed as one — a heading's accessible name is its text, and an `<input>` inside it would take
  the title out of that name, which is how the page is found in every test. React must not own its children:
  the initial text is rendered once from a ref and a later server value is written in by hand, never while
  somebody is typing. `Enter` commits and gives up focus, `Escape` reverts, an empty title reverts rather
  than saving; a `committed` ref stops the blur that follows `Enter` from saving twice. The description is
  the same `MarkdownEditor` a Document uses, with the same transparent chrome, saving on blur and `⌘Enter`.
  One `useAutosave` serves both, and one `role="status"` beside the key says Saving…/Saved or offers Retry.
- **A Document is edited where it is read.** `IssueDocuments` has no read mode and no Save button: the
  editor is the view, `onBlur` (focus leaving the frame entirely) and `⌘Enter` write a version through
  `useAutosave`, and a `role="status"` line says Saving…/Saved or offers Retry. The editor there is passed
  `border-transparent bg-transparent` — a Document is the page, not a field on it, so it takes the page's
  own paper and ink; the input chrome stays for comments and notes, which are fields.
- Every write carries `baseVersion`, so a save landing on top of somebody else's is refused with a
  `CONFLICT` rather than quietly winning. Real simultaneous editing is `docs/plans/collaborative-documents.md`.
- **A Gate ruling pins what it ruled on.** Every decision records the version each Document stood at
  (`gate_decision_document`); the ruling reads "on spec v2", says so when the text has been written since,
  and the History dialog badges the version a Gate approved or rejected. An approval is about words, and the
  words keep moving.
- The byline names **every** Member who has written a version ("written by Ada and Planner · last edit 4d"),
  from `documents.versions`; older versions live behind a `⋯` (`More for <name>`) with History and Copy as
  Markdown, and History is a dialog that reads a version and can Restore it.
- **`components/tiptap-editor.tsx`** (lazy) is Tiptap 3.31 with `@tiptap/markdown` (GFM), StarterKit,
  `TableKit`, `TaskList`/`TaskItem`, lowlight code blocks, Placeholder. It emits `editor.getMarkdown()` only
  on a user transaction; a `value` changed from outside is loaded with `emitUpdate: false`, so an untouched
  load never re-serializes. `editorExtensions()` and `toMarkdown()` are exported so a test round-trips
  through a headless `Editor` with exactly the component's extensions.
- **Formatting is a bubble over the selection, never a strip above the text** (`BubbleMenu` from
  `@tiptap/react/menus`, block mode only). A Document, a description and a comment are read far more often
  than they are formatted, and a toolbar that is always there is chrome on every one of those readings. The
  bubble carries what a selection can _become_ — bold, italic, code, H1–H3, the three lists, quote, code
  block; what a Human _inserts_ — a table, a divider — is the `/` menu, because those are not things a
  selection turns into. It mounts only while something is selected, so a test with no layout never sees it:
  `Toolbar` is exported and tested as a component against a headless `Editor`, and the editor tests assert
  that nothing sits in the flow. Its accessible name is still `toolbar "Formatting"`.
- **Mentions are text.** `@` opens a `@tiptap/suggestion` popup (`role="listbox" aria-label="Mentions"`)
  fed by `useMentionables()` (`lib/mentions.ts`: Members and Teams by handle) and inserts `@handle ` as plain
  text — no Mention node, so markdown round-trips exactly and the server resolves handles as before. `/` at a
  line start opens the block menu (`aria-label="Commands"`) the same way — Heading 1–3, the three lists,
  table, code block, quote, divider. Both popups are `position: fixed` and belong to a **line**, not to the
  viewport: `popup()` keeps the suggestion's `clientRect` and re-places on `scroll` (captured, because the
  scroller is a pane or the peek rather than the window) and on `resize`. Without that the menu sits still
  while the words move. Two suggestion plugins need two
  `PluginKey`s or ProseMirror throws.
- **Highlighting is lowlight in both places**: `rehype-highlight` in `components/markdown.tsx`, the code
  block extension in the editor, colours from the palette in `index.css` (`.hljs-*`). Not shiki: its rehype
  plugin is async and `react-markdown` runs its pipeline synchronously. `proseClassName` is shared by the
  reader and the editor so switching does not reflow.
- **jsdom** needs `Range.prototype.getClientRects/getBoundingClientRect` and `document.elementFromPoint`
  stubbed for ProseMirror to mount (`tests/setup.ts`).

## What slice 4 settled (the Issue view)

- **One component, two shapes.** `routes/issues/issue.tsx` renders the Issue page and the peek. The root is
  `@container`; the grid is one column below `@3xl` (the 720px peek) and `minmax(0,1fr) 300px` above. In one
  column the rail comes first (`-order-1`), so the Gate ruling is still the first thing seen.
- **The Gate ruling card is the top of the rail, always** — `GateControls` inside `role="group"
aria-label="<State> Gate|State"`, with `data-focused` and a `role="status"` banner ("Waiting on your
  ruling…", button "Rule now") when `?gate=` names the current State. Then Assignee (a `Select` of
  `MemberChip`s, `aria-label="Assignee"`), `LabelPicker` (`role="group" aria-label="Labels"`, toggles named
  by label text), children, `IssueLinks` (lists named by kind, `Add a link`).
- **`components/activity-stream.tsx`** folds `comments.list` and `events.list` (subject issue) into one
  `<ol aria-label="Activity">` in time order, skipping `comment.*` Events; a filter All / Comments / Changes;
  the composer is the inline `MarkdownEditor` with `id="new-comment"` and `aria-label="Comment"`, button
  "Comment". The lists once named "Timeline" and "Comments" are gone; tests query within "Activity".
- **Mentions are the rich editor's own.** Tiptap's suggestion popup (`role="listbox" aria-label="Mentions"`)
  is the only one now; the textarea's parallel list went with the Source view it belonged to. What is ours
  is the candidate list, `useMentionables()`, and that is what the comments test asserts — the popup needs a
  ProseMirror view to open, which is the one thing jsdom cannot give it.
- **Sheet width.** shadcn's `SheetContent` sets `data-[side=right]:sm:max-w-sm`; to widen it, use the same
  variant chain (`data-[side=right]:sm:max-w-[720px]`) or the narrower class wins.

## What slice 5 settled (Runs)

- **`components/run-card.tsx`** exports `IssueRuns` (the section on an Issue) and `RunCard`. Each card is
  an `article` named by the Run id: the Agent's `MemberChip`, `RunStatus` (label "Waiting for approval"
  when the Run waits on a Gate), "started by <trigger>", elapsed time, the summary, and the Activity feed as
  `<ol aria-label="Activity of <id>">` with `li[data-kind]` per Activity — thought (muted italic), action,
  elicitation (gate hue), response (agent hue), error (destructive, mono), prompt (human hue). Feeds fold to
  the last three unless pinned or expanded.
- **The Run owed a Human comes first** (`data-pinned`), open, with a "Needs your answer" band and a plain
  `Textarea` named "Answer this Run" (⌘Enter sends) — a textarea, not the editor, because the runs test asks
  for one textbox and a reply to an Agent is a sentence. A Run waiting on a Gate shows "Open the Gate" and
  no answer box: the ruling card is the only place a Gate is decided (ADR-0004).
- `MarkdownEditor`'s markdown textarea is hidden with the HTML attribute, not a class, so it is never a
  second textbox to a role query while a label still finds it.

## What slice 6 settled (the Inbox)

- **Two panes** (`ui/resizable`, `orientation="horizontal"`, sizes in percent) above 1024px: the list on the
  left, the selected Notification's Issue on the right as the full `IssuePage` with `focusGate` when the
  kind is `gate_awaiting`, so the ruling card and its banner are in front. Below 1024px the preview is the
  `SidePeek`. The selection and the Unread filter ride in the URL (`?n=`, `?unread=1`).
- **Opening marks read** — reading is what was owed — and `e` / `⇧E` / `j` / `k` / `o` work on the list.
  Rows keep `Notifications for <key>` lists, `Mark read` (unread only, `stopPropagation` so it does not also
  open) and `Mark all read`; the kind glyph is coloured by what is owed (Gate, Agent, Human).
- **Search values are strings, both ways.** `router.tsx` gives the router a `parseSearch`/`stringifySearch`
  pair on `URLSearchParams`: the default JSON pair wrote `?open=%220%22` (shown as `open="0"`) for a
  string that looks like a number, and read a raw `?open=0` as the number 0 (2026-09-06). Every
  `parse*Search` still tolerates a number, so a hand-typed URL from before keeps working.
- **`Shortcut` hints are `aria-hidden`** (`data-slot="shortcut"`, `data-keys`), so a hint inside a button
  never joins its accessible name. Tests reach one by `data-slot`, never by label.

## What slice 7 settled (the Board)

- **`components/reui/kanban.tsx`** is `@reui/kanban` (Base UI build, MIT, header says so), edited once:
  `process.env.NODE_ENV` became `import.meta.env.DEV` because the browser tsconfig has no Node types. Registry
  files live under `components/<registry>/`, not `ui/`, so a re-add cannot clobber shadcn's own.
- **The Board** (`routes/projects/board.tsx`) gives the kanban `value` (a `Record<stateId, Issue[]>`) and an
  `onMove` callback, so it never applies a move itself: a card leaving a Gate column opens the ruling dialog
  ("Decide the <State> Gate on <key>", dialog with Approve/Reject) and anything else is `issues.move`.
  Columns are `KanbanColumn render={<section data-slot="board-column" aria-label={state.name}/>}` with the
  `StateBadge` header (the word "Gate" is `sr-only`: the amber diamond is the eye's, since 2026-09-06), `disabled` so columns do not reorder. A click on a card opens the
  peek (`?peek=`); the peek is `modal={false}` here and `onDragStart` closes it.
- **Filters** are the shared `IssueFilters` with `hideProject` and `nativeAssignee` — the Assignee is a plain
  `<select>` on the Board because its test drives it with a change event.
- **The frame is the viewport's height, and the page area is what scrolls** (2026-09-11). The sidebar
  wrapper is `h-svh overflow-hidden` (passed from `routes/shell.tsx`, not edited into the kit) and the div
  around the `Outlet` is `overflow-y-auto`. So the top bar and the sidebar stay put, a screen may ask for
  `h-full` and mean it, and `min-h-0` on every flex ancestor is what lets that height reach the bottom of a
  page. The Inbox's `h-[calc(100vh-2.75rem)]` became `h-full` with it.
- **A Project is configured in Settings, not on itself** (2026-09-11). `Settings › Work › Projects`
  (`routes/settings/projects.tsx`) is master–detail like Teams: `nav "Projects"` naming each by name and
  key, `article "<Project>"` beside it, `?project=<KEY>` in the URL, and `ProjectSettingsForm`
  (`routes/settings/project-settings.tsx`, moved from `routes/projects/`) as the pane. The Project's own
  tabs are the work alone — Issues, Board, Workflow — and `/projects/$key/settings` redirects into
  Settings, the way `settings/workflow` already redirected out of it. Creating a Project stays on
  `/projects`, which is where you go to start one.
- **A Project's header is its name, its description and its tabs** (2026-09-11). The Team that owns it is a
  column on the Projects list under a heading that says so; above the title it was a bare word naming
  nothing, so it is gone. `Archived` still shows there, because that is what the page has to say about
  itself before its name.
- **A Board spends no height on its own name.** The Project's Board tab has no `PageHeader`: the Project's
  name is the page's `h1`, the tab says Board, and its filters sit bare the way the Issues tab's do. The
  section also takes the page's bottom gutter back (`md:-mb-6 md:pb-2`, coupled to `p-6` in `shell.tsx`).
- **A Board is a frame from `md` up** (`components/issue-board.tsx`, 2026-09-11): the strip is `md:h-full`,
  a column `md:max-h-full`, and `KanbanColumnContent` is `md:min-h-0 md:flex-1 md:overflow-y-auto`, so the
  cards scroll and the headers, the counts and the Workflow do not. Below `md` every one of those is off and
  the Board grows with the page: the Project's chrome leaves about 300px on a phone, which is two cards.
- **The Board's sideways scroll is the Board's** (`components/issue-board.tsx`, 2026-09-08). The scroller is
  `relative`, because an absolutely positioned descendant is clipped by its containing block and not by
  whatever scrolls — without it the `sr-only` words a `StateBadge` and an avatar carry are laid out against
  the page and every column past the fold widens it. It wears `scrollbar-thin` (an `@utility` in `index.css`:
  `scrollbar-width` for Firefox, `::-webkit-scrollbar` for WebKit, the thumb in `--border`). **The wheel
  stays the browser's**: a listener that turned `deltaY` into `scrollLeft` shipped on 2026-09-08 and came
  off on 2026-09-11, because a Board is taller than the window at least as often as it is wider and the
  page could not be reached until the last column had gone by. Sideways is Shift and a wheel, a trackpad,
  or the bar.

## What slice 8 settled (the Project)

- **`/projects/$key` is a layout route** (`ProjectLayout`: header — key, Team, name, description; the
  `ul aria-label="Workflow"` strip of `StateBadge`s it carried went on 2026-09-06, since the Issues tab's
  groups and the Board's columns are the Workflow already — `nav aria-label="Project"` tabs) with children `/` (Issues: the Issues home `embedded` and `fixedProject`; the quick-add form went on
  2026-09-06, since the top bar's New Issue and `c` open the dialog with this Project already chosen), `board`, `workflow`, `settings`
  (`projects.update`/`archive`), and `settings/workflow` redirecting to `workflow`. The Issue filters and
  `?peek=` validate on the layout, so the tabs share them.
- **A tab writes its search with the router's `useNavigate()` and `to: "."`**, never the layout route's
  `useNavigate()`: a route's navigate takes its own path as `from`, and the Board lost `/board` the moment a
  peek opened.
- **`components/diceui/sortable.tsx`** is `@diceui/sortable` (MIT, dnd-kit) with `radix-ui`'s `Slot`
  replaced by Base UI's `useRender` (`@base-ui/react/use-render` + `merge-props`, the pattern
  `reui/kanban.tsx` uses): `asChild` hands the one child to `render`, so the child's own props win and
  refs merge through `useRender`'s `ref` list. The CLI had added `radix-ui` to the catalog, which the
  no-Radix rule forbids; a vendored `lib/slot.tsx` + `lib/compose-refs.ts` stood in until 2026-09-06 (#10).
  The Workflow editor's States are `SortableItem asChild` around each `<li>` with a "Drag <State>" handle;
  the "Move up/down" buttons stay for the keyboard and the tests. New draft States carry a `uid`.
- Under a Project the Workflow editor's heading is an `h2`: the Project's name is the page's `h1`.

## What slice 9 settled (Settings)

- **`components/settings-page.tsx`**: `SettingsPage` (the h1 via `PageHeader`, a description, the page's
  action on the right) and `SettingsSection` (a card with an optional title/description, `aria-label` for
  a landmark, `tone="danger"` for what suspends, revokes or archives). All eleven pages use them; their
  h1s and control names are unchanged.
- **Native selects stay in Settings** where a test drives them with a change event (schedules, routing
  rules, providers, approvers). Members and Agents tables show `MemberChip`s; the Sponsor is a chip.
- **An Agent is created with its first key**, and the dialog that made it is the only place that key is
  readable — the shape the invitation link already had. `agents.create` returns it (null where nothing can
  mint one), so an Agent made over the API is born connectable too.
- **Connecting is shown where the key is.** `ConnectAgent` (`components/connect-agent.tsx`, region
  `Connect an Agent`, `tablist "Coding agent"`) renders this deevy's endpoint and one tab per coding agent —
  Claude Code, OpenCode, Cursor CLI, Copilot CLI, `Anything else` — each with the file or the command it
  takes. It is mounted three times, and `issuedKey` is what differs: in the create dialog and beside a
  freshly issued key it writes that key into the command, because a key is readable once and no later screen
  can fill it in; standing on `/settings/agents/$memberId` it names the key instead. The recipes are data in
  `lib/mcp.ts` (which also owns `mcpEndpoint()`, read off the page), so a fifth is an entry there, and they
  follow the runtime's own (docs/harnesses.md). **A recipe only gets a `variable` where that client really
  expands one** — Claude Code `${VAR}`, OpenCode `{env:VAR}`; Cursor documents `${env:VAR}` and does not
  resolve it for a remote server, and the Copilot CLI documents none, so both fall back to the placeholder
  rather than to a reference deevy would be sent verbatim.
- **The Agent detail** has Projects and API keys (regions kept), a Schedule section (`Wake`), Recent Runs
  (`runs.list({ agentMemberId })`), a danger section to Suspend/Reinstate, and — for an admin — a
  `Change Sponsor` select in the header (`agents.setSponsor`). The Agents table keeps its own
  `Schedule for <name>` select, which its test drives.

## What the Settings rework settled (2026-09-07)

- **`SettingsRow` is one setting**: the label, one line of why, then the control, ruled off from the next.
  A page of cards each holding a single field spends more frame than it frames, so a tenth setting is a
  tenth row. Its `below` slot is for a form the row opens — across the row's whole width, never inside the
  control column, where it takes the width out of the label and turns a one-line hint into a sliver.
  `SettingsSection` is still the card, for a concern with several controls in it.
- **A Settings page lays itself out by its container, never by the window.** The content column is
  `@container`, so a page uses `@sm:`…`@3xl:` and not `sm:`…`xl:`: behind the sidebar and the Settings nav
  a 900px window leaves a form about 350px, and a viewport breakpoint says nothing about that.
  `SidebarInset` carries `min-w-0` for the same reason (a deevy edit in `ui/sidebar.tsx`) — without it a
  wide page pushes the whole app sideways rather than shrinking.
- **The Settings nav appears at `lg`, not `md`.** It is 224px beside a 256px sidebar, so at 768 the page
  was left 161px and most of the pages overflowed. Below `lg` the whole navigation is one Select
  (`combobox "Settings page"`) that names where you are without being opened and opens to all eleven pages
  in the four groups — not a strip of tabs scrolling sideways, which put MCP clients four swipes from
  General. The content column adds no padding of its own below `lg`: the shell already gives every page a
  gutter, and a second one spent a quarter of a 390px screen on margins.
- **Settings leaves the primary sidebar alone.** It used to fold it on the way in and unfold it on the way
  out; its own nav already reads as the second level.
- **Workspace › General opens with the Workspace**, not with a form about it: the mark, the name edited
  where it is read, `@slug`, the date, and counts taken from queries the shell has already run. The
  Allowlist is a row of chips on it (`/settings/allowlist` redirects), and one strip names what the
  instance has not set up while anything is unset, from lists the app already fetches, and renders nothing
  once nothing is.
- **Teams is master–detail** (`nav "Teams"` beside `article "<Team>"`), the shape the Workflow editor
  taught, with `?team=` naming the open one. It shows the Projects a Team owns, joined off `projects.list`
  which already carries each Project's Team.
- **A label element beats an `aria-label`** where a control can have a visible one: the Event log's filters
  name themselves Kind, Subject and Project on screen, and the `aria-label`s that would have shadowed them
  are gone. `getByLabelText` finds the same thing either way.
- **A log reads at 12px** and names its actors rather than drawing them — 300 rows of avatars is a column
  of noise. Which kind acted still shows, in the `--human` and `--agent` colours.

## What slice 10 settled (the Event log)

- **`events.list` takes `before` and `order`** (`asc` default, the stream's; `desc` for a log). The cursor
  is the last row's seq either way. `routes/settings/events.tsx` reads `order: "desc"`, pages back with
  `before`, filters by Project and subject on the server and by kind prefix on the page, and shows a row's
  payload as JSON when clicked. It is under Settings › Workspace › Event log; admins' reading.
- `DataTable` without groups is the plain table with a keyboard row; the Event log is its first flat use.

## What slice 11 settled (polish, mobile, the keyboard on screen)

- **Mobile is read-and-rule, and it falls out of the containers.** Do not add breakpoint-specific
  components: the Sidebar is a Sheet below 768px, the peek is full width below `sm`, the Inbox folds to one
  pane below 1024px, the Issue view stacks under `@3xl`, the Board scrolls horizontally. A new screen gets
  the same treatment by using the same containers; check it at 390px with `scrollWidth === innerWidth`,
  and clip any table cell that mixes text with chips (`min-w-0 overflow-hidden`; a `max-w-0` cell does
  not clip on its own, so chips paint over the next column).
- **The keyboard map lives in `components/shortcuts-sheet.tsx`** as data, shown by `?` and by the palette's
  Help group. Add a shortcut there when you add one to the app; the sheet is what a Human reads, so its
  wording is the app's, not the code's (`mod+enter` renders as ⌘↵ / Ctrl+↵ through `Shortcut`).
- **The palette knows the focused Issue from the URL**, `focusedIssue(pathname, search)` in
  `command-palette.tsx`: `/issues/KEY` first, else `?peek=`. Its group is Open full page (peek only), Copy
  key, Copy link. Actions that need a picker stay in the rail behind `a`/`s`/`l`/`p`.
- **Letters on an Issue reach the Issue in front.** `IssuePage`, `GateControls`, `LabelPicker`,
  `ParentPicker` and `IssueDocuments` take `shortcutScope` (default the page; the peek passes `"peek"`),
  and bind `a` (Assignee select, controlled `open`), `s` (State select, or the Gate's Note), `l` (focus the
  first Label), `p` (Parent Popover), `⇧A`/`⇧R` (Note focused, that ruling chosen, `⌘↵` commits it — the
  chosen button is the filled one, `data-ruling` says which), `[`/`]` (Document tabs). A picker opened by
  a key is a controlled Base UI popup, not a synthetic click. cmdk names its input from `<Command label>`,
  never from an `aria-label` on the input.
- **Screenshots** come from `vp run web#screens` (`apps/web/scripts/screens.ts`) against the seeded
  `dev:stub` instance, into `docs/screens/`; regenerate at milestones.
- **Live regions:** the Gate banner and the Run's "Needs your answer" band are `role="status"`. Nothing
  else announces; a new one needs a reason.
- **Everything outside the shell** (`SignedOut`, `NotAMember`, `Suspended`) renders in `SignInFrame`
  (`App.tsx`): the legend on the left is built from `MemberChip` and `StateBadge` with placeholder Members,
  so a token change shows up there too. **The sign-in buttons are `health.ping`'s `providers`**, one per
  entry in the order the server sent (`Sign in with <label>`); a deployment that configured none gets a line
  saying so and no button, and a provider is added by configuring one, never by editing `App.tsx`
  (docs/plans/sign-in.md). The dev form stays under them, only when `health.ping` reports `devSignIn`, and it
  signs in through the first provider that list carries rather than naming one, so a stubbed instance offering
  only Google still signs in; when the authorization URL carries an `id_token` nonce (an OpenID Connect
  provider does), the code it lands with is `email|nonce`.
- **An invitation link is answered outside the router.** `/invite/<token>` reaches somebody who is not a
  Member yet, and the router is only mounted for a Member — so `App.tsx` reads the token off the path on its
  first render and holds it in `sessionStorage` (`lib/invitation.ts`), the signed-out page says an invitation
  is waiting and no more (the token is a bearer; there is nothing to read without one), and `NotAMember`
  spends it through `invitations.accept` and re-reads `me.get`. A refusal is the operation's own message,
  since only it knows which address was invited. A Member who lands on the path is already in: the router's
  `/invite/$token` route drops the held token and redirects home (docs/plans/sign-in.md slice 8).
- **`ui/*` hygiene:** a `ui/*` file may sit unimported (it is the kit), but a dependency only an unimported
  file needs goes with the file. Removed in slice 11: `chart`, `carousel`, `calendar`, `input-otp`,
  `aspect-ratio`, `menubar`, `navigation-menu`, `slider`, `progress`, `radio-group`, `drawer`,
  `context-menu`, `hover-card`, `pagination`, `accordion`, and `recharts`, `embla-carousel-react`,
  `react-day-picker`, `input-otp` from the catalog. Add one back with `pnpm dlx shadcn@latest add`.

## What round 2 settled (Matt's critique of 2026-09-05; docs/plans/ui-redesign-2.md)

- **The theme** is clean slate: see "Design language" above. `--face-*`, `--radius`, `--density` and
  `--tracking` are the knobs; a candidate review is a dev-only switcher on `<html data-…>`, deleted after.
- **A rail section is named by `RailHeading`** (`components/rail-heading.tsx`, 2026-09-11): 12px, medium,
  muted — the size deevy sets metadata in. State, Assignee, Labels, Parent, Children and Links each spelled
  that out themselves and three had drifted to 14px, which is the size of a heading in the main column
  (Documents, Runs, Activity) and not of a label on the rail. Inside Links the per-kind headings keep 12px
  and lose the weight, so the section still leads.
- **A chip inside a sentence is `size="inline"`** (`member-chip.tsx`, 2026-09-11): the name is the size of
  the words either side of it and the mark beside it is the height of that line, so an Activity row reads as
  one sentence rather than as a badge followed by smaller text. **A size budgets for the kind ring**, which
  `ring-1 ring-offset-1` paints outside the box — 2px on every side, so `size-3.5` painted 18.7px on a 20px
  line. `inline` is `size-3` with `ring-offset-0`, which lands at 14.6. The ring classes are composed
  _before_ `style.avatar` for that reason: the size has the last word. `xs` and up stay what they were, for
  a chip that stands on its own in a row or a cell.
- **A timeline shows no avatars** (`nameOnly` on the chip, 2026-09-12): the Activity stream already carries
  a column of tone dots down its left edge, and a second column of pictures beside them is one more thing to
  read past on every line. The name alone, with an Agent's in the Agent colour and the kind still in the
  tooltip. Elsewhere — a byline, a Run header, a table — the avatar stays.
- **The tone dot is a bullet, centred on its line with `translate-y`, never `top`** (`lib/event-text.ts`):
  `size-2.5` over the kit's `size-4` — 10.5px at deevy's density, punctuation down the edge of the Activity
  rather than the first thing on every line — pushed 4.75px down, half the difference between it and the
  20px line box. The translate is not a style choice: the ReUI `Timeline` sets
  `group-data-[orientation=vertical]/timeline:top-0` on the indicator, and a variant beats a plain `top-*`
  wherever it sits in the class list. Change the size and measure the pair in the browser again.
- **A row of `items-baseline` wants children that have a baseline.** An `inline-flex items-center` button
  has none of its own, so the browser synthesises one from whatever is inside it: the folded "N steps"
  button pushed its own row 2.3px taller and its neighbours below both the button and the dot. An icon that
  belongs in a line of text goes _in_ the line — `inline size-3.5 align-[-0.1875em]` — not in a flex box
  beside it.
- **Wording lives in `lib/event-text.ts` and `lib/notification-text.ts`.** A screen never phrases an Event
  itself; new Event kinds get a case in `describeEvent` (with a unit test) and new payload fields carry
  names beside ids so the log reads without lookups. Activity is a ReUI `Timeline` rendered as the
  `ol aria-label="Activity"`; day rows are `li role="presentation"`.
- **Multi-select is a Base UI `Combobox multiple`** with `ComboboxChips`/`ComboboxChipsInput`, `items`,
  `itemToStringLabel`, `isItemEqualToValue`, and `removeLabel` on each chip (`label-picker.tsx` is the
  model; approvers reuse it). In a test: `fireEvent.change(input, …)` filters, `fireEvent.keyDown(input,
{ key: "ArrowDown" })` opens, then `screen.findByRole("option", …)` — the popup is portalled.
- **Selects are shadcn's, never native, composed directly from `ui/select`** — `Select` › `SelectTrigger` +
  `SelectValue`, then `SelectContent` › `SelectGroup` › `SelectItem`, with `SelectLabel` on a group that has
  a heading and `SelectSeparator` between a "none" item (Nobody, Never, Any, Nowhere) and the real choices.
  No wrapper over it: a page groups and separates as its options ask (the Event log's kinds by family, the
  State's Agents apart from Nobody). In that build the group carries the list's padding, so bare items sit
  flush against the popup edge. Base UI wants a real value for "none", so a page keeps a sentinel constant
  (`"__any"`, `"__none"`), never `""`. `ui/native-select.tsx` is gone. In a test, `pickOption(trigger, name)`
  from `tests/select.ts` drives one (ArrowDown opens, Enter on the highlighted option chooses — a click
  does not), and `selectedLabel(trigger)` reads it.
- **The Inbox** is one flat two-line list (`ul aria-label="Notifications"`): actor's name (no chip: the kind glyph on the left is enough) · verb · on KEY,
  the Issue title, the quote. `lib/notification-text.ts` phrases it from the joined Event, actor and
  comment; a checkbox per row and `x` select, a `toolbar "Selection"` marks several read.
- **Any Issue list is also a board.** `view=board` in the URL,
  `components/issue-board.tsx` for the board itself (`IssueBoard` is the connected one both the Project
  Board and the Workspace board render). Never build a second kanban.
- **A grouping is an object, and both shapes draw it** (`lib/groupings.tsx`, docs/plans/issue-views.md,
  2026-09-07). One `Grouping` buckets the rows, orders and names the buckets, and says what a drop into one
  means; the list renders the buckets as `DataGroup`s and the board renders the same buckets as columns.
  What ships is State, Assignee, Project and one per Label scope in use — a fifth is a new object in that
  file, never an edit to either view. Rules the model carries:
  - **`?group=` is any grouping's id** (`state`, `assignee`, `project`, `label:epic`) or `none`. The screen
    validates it against what it offers and falls back to State, so an old link still opens.
  - **Group by shows on a board too**, where the columns _are_ the grouping. "No grouping" is a list's
    choice alone: a board with no columns is not a board.
  - **A bucket's `plan` says what a drop means** — `move`, `assign`, `labels`, `gate`, `refused`. A bucket
    with no plan takes no cards and the board says why (grouping by Project). The board itself decides only
    what is true of every grouping; the Gate rule belongs to the State grouping, so reassigning a card that
    sits at a Gate is a reassignment, not a ruling.
  - **`keepWhenEmpty`** is how a board keeps a column nothing is in while the list drops the empty group.
  - **Group by a Label scope, never by a Label**: an Issue carries at most one Label per scope, so a scope
    divides the Issues exactly once each and a drop has one meaning.
  - **The table drops whatever column the groups already state** — by Assignee the Assignee column goes and
    State comes back.
  - A screen that is one Project's uses `projectStateGrouping` (its Workflow, unfolded, buckets by State
    id); a Workspace-wide one uses `stateGrouping` over `foldStates` (`lib/states.ts`), which folds States
    by name across Projects and resolves a drop to the card's own Project.
- **Forms save themselves** where a change is one field: `lib/autosave.ts` (`saveNow` on blur/Enter, a
  `role="status"` line: Saving · Saved · error + Retry). The Workflow editor is the exception — a rewrite with
  deletions keeps its explicit Save Workflow and counts unsaved changes in a sticky footer.
- **The Workflow editor is master–detail**: `ul "States"` on the left (drag handle, `Edit <State>` row
  button, unsaved dot), `form "<State>"` on the right with `StateFields` (`components/workflow-state-fields.tsx`),
  the template in the markdown editor, approvers in `components/approvers-picker.tsx`.
- **The top bar carries a breadcrumb** (`components/app-breadcrumb.tsx`, shadcn `ui/breadcrumb`, `nav
aria-label="breadcrumb"`): `crumbsFor(pathname, search, projectName)` is pure — Issues view by its filters,
  Projects › Project › tab, Projects › Project › KEY for an Issue, Settings › page. A new route gets a case there.
- **Lists are `DataTable`**, and a row opens on click (`onOpen`); the Projects list was the last raw table.
- **A page that lays out its own panes declares `staticData: { bleed: true }`** on its route; the shell
  reads it and adds no padding. Nothing else cancels the shell's `p-6`.
- **Tests drive Base UI popups with keys**: `ArrowDown` opens a Combobox or Select in jsdom, `Escape` closes
  it — and while one is open the rest of the page is inert, so close it before querying elsewhere.

## Test contracts

Tests in `apps/web/tests` query by role and accessible name, mock `lib/orpc` with
`tests/stub-client.ts` (shallow merge per namespace), and mount routes with
`createAppRouter(ctx, { initialEntries })` + `await act(() => router.load())`. Names a redesign keeps unless a
slice says otherwise: `Sign in with GitHub`; `New Issue` / `Create Issue` / `Add Issue`; `role=table` rows
`DEV-1 · title · Build · Ada Lovelace`; `role=region` per Board column named by State with visible `Gate`;
`Decide the Intent Gate on DEV-1`; `role=group` `… Gate` with `data-focused` for `?gate=`; `Note`, `Approve`,
`Reject`, `Gate decisions`, `State`; `tablist Documents`, `Body`, `More for <name>`, `Versions of <name>`, `Restore v<n>`;
`Notifications for DEV-1`, `Mark read`, `Mark all read`, `N unread`; `Comment` (textarea and button),
`listbox Mentions`; `article` named by Run id, `Answer this Run`, link `/gate/`; `Add a link`, lists
`Pull requests`/`Links`; `role=group Labels`; the settings h1s (`Workspace`, `Members`, `Agents`, …),
`Schedule for <name>`, `Grant a Project`, `Key name`, `Issue`, `Revoke DEV`, `Sponsored by`, `only time`;
`Approvers for <State>`, `Save Workflow`, list `States`. Slices 1, 2, 4 and 8 of the plan change names on
purpose and update the tests with them.

The grouping rework added: `combobox "Group by"` in `group "Filters"`, on the list **and** the board;
`region "<bucket>"` for a board column named by whatever it groups (`Unassigned`, `No epic`, a Project's
name, a State); `Group by <label>` as each option's text.

The Settings rework added: `combobox "Settings page"` (the compact nav below `lg`, whose classes the shell
test asserts as `lg:hidden` / `lg:flex`); `Who may join`, `Add rule`, `Stop allowing <value>` and the
`Match on` field behind it, whose value field is named by the kind chosen — `Domain`, `Organization login`,
`Group path` (Workspace › General); `Invited`, `Invite someone`, `Create invitation`, `list "Invitations"`
and `Revoke the invitation for <address>` beside it, with the link shown once in the dialog that made it and
never on a row; `nav "Teams"`, `article "<Team>"`,
`list "Members of <Team>"`, `Actions for <name>`, `Disband <Team>`; `Kind` / `Subject` / `Project` on the
Event log, now named by a `<label>` rather than an `aria-label`.

Round 2 added these names: `list "Notifications"` with `checkbox "Select <verb>"` and `toolbar "Selection"`
(Inbox); `button "List"` / `button "Board"` in `group "Filters"` and `region "<State>"` columns on the
Workspace board; `combobox "Labels"` with `button "Remove <label>"` chips; `button "Edit <State>"`,
`form "<State>"`, `combobox "Approvers for <State>"`, `textbox "Template for <State>"` (ask for the textarea) and the
`Save Workflow` / `Add State` / `Reset` footer in the Workflow editor; `status` on the Project settings form.
