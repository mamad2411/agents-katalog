# Alexandria

A single-user desktop personal knowledge system: daily lists, notes,
design canvases ("Blueprints"), a kanban for
feedback planning, and two visualizations of activity. All data lives
on-device. (The original single shared canvas — the "Alexandria" map —
was removed in Sprint 40; Blueprints superseded it.)

> The product is named **Alexandria** (after its centerpiece canvas).
> The macOS bundle identifier is still `com.alertmedia.bigpicture` — it
> was deliberately *not* renamed because it resolves the on-disk SQLite
> path; changing it would orphan existing data. The "bigpicture" string
> survives only in that identifier / DB path, never in the UI.

> If you are a Claude session being onboarded to continue development:
> read this file end-to-end, then skim `documentation/SPRINT*.md`
> chronologically (1 → 13). The sprints are the *why* — this file is
> the *map*.

## Stack

- **Frontend**: SvelteKit + `adapter-static` (SPA, **no SSR**), Svelte 5
  with runes (`$state` / `$derived` / `$effect`), Tailwind CSS v4,
  TypeScript. CSR-only is enforced by `src/routes/+layout.ts`.
- **Backend**: Rust + Tauri 2, `sqlx` against SQLite. The DB file lives
  at `~/Library/Application Support/com.alertmedia.bigpicture/todos.db`
  on macOS. Migrations run automatically at startup via
  `sqlx::migrate!("./migrations")`.
- **Canvas / visualization libs**: `@xyflow/svelte` (Alexandria + the
  feedback connectors). ("The Mirror" — the former Visualization —
  renders on a plain `<canvas>`, no chart lib; Sprint 46.)

Bundle ID: `com.alertmedia.bigpicture`. Window has transparent
`titleBarStyle` + macOS sidebar vibrancy (see `tauri.conf.json`).

## Dev commands

```bash
pnpm install                         # once
pnpm tauri dev                       # full app (Tauri window + frontend)
pnpm dev                             # frontend only (browser, no IPC)
pnpm build                           # frontend production build
npx svelte-check --tsconfig ./tsconfig.json   # frontend type check
cd src-tauri && cargo check          # backend type check
cd src-tauri && cargo test --lib     # backend tests (see "Known quirks")
```

Run `pnpm tauri dev` once before committing to ensure migrations apply
to your local DB.

## Repo layout

```
src/
  app.css                       # Tailwind + global rules; imports xyflow CSS
  app.html
  lib/
    components/
      Sidebar.svelte                 # left rail; search + Today/Backlog/Add +
                                     #   unified drag-reorderable Pinned list (Sprint 49)
      Welcome.svelte                 # home view; Today card + Jump-back-in +
                                     #   contribution calendar (Sprint 48)
      HelpModal.svelte               # `?` shortcuts modal
      AddEntityModal.svelte          # "+ Add" picker from sidebar
      ListView/NoteView/ArticleView.svelte  # (WorkflowView removed — Sprint 50)
      LibraryView.svelte             # "Library" — unified browser for all
                                     #   entities (Sprint 47; replaced
                                     #   SummaryView + the Blueprints/Feedback/
                                     #   Storyboards index views)
      MirrorView.svelte              # "The Mirror" — canvas data-portrait (Sprint 46)
      MapTextNode / MapCommentNode / MapTitleNode  # decorative canvas nodes,
                                     #   now used ONLY by Blueprints (the
                                     #   Alexandria map was removed, Sprint 40)
                                     # (BlueprintsView removed — Sprint 47)
      BlueprintView / BlueprintEditor / BlueprintCardNode
                                     # (FeedbackBoardsView removed — Sprint 47)
      FeedbackBoardView.svelte       # kanban columns + DnD
      FeedbackCardPanel.svelte       # card detail slide-in
      ActivityView.svelte            # Kandinsky weekly grid
      MarkdownEditor.svelte          # click-to-edit / blur-to-save md editor
      IdChip.svelte
    stores/
      app.svelte.ts                  # SINGLE AppStore class — view + data + actions
      theme.svelte.ts                # light/dark/system
    ipc.ts                           # all types + Tauri `invoke` wrappers
                                     # (garden.ts removed in Sprint 46)
  routes/
    +layout.ts                       # exports `ssr = false`
    +layout.svelte
    +page.svelte                     # dispatches the view by app.view

src-tauri/
  src/
    commands/
      lists.rs todos.rs tags.rs notes.rs articles.rs pins.rs
      map.rs feedback.rs search.rs export.rs images.rs blueprints.rs mod.rs
    db/
      mod.rs                         # pool setup + sqlx::migrate!()
      models.rs                      # ALL serde structs (serde camelCase)
    error.rs markdown.rs lib.rs main.rs
  migrations/                        # 0001-… monotonic, auto-applied
  Cargo.toml tauri.conf.json

documentation/
  SPRINT1.md … SPRINT12.md           # decision log — read these to onboard
```

## Architecture (request → response → render)

```
UI event in a *.svelte component
  → calls app.someAction(args)        (src/lib/stores/app.svelte.ts)
    → app.* awaits an IPC fn          (src/lib/ipc.ts)
      → Tauri invoke "snake_case_cmd" (camelCase args ↔ snake_case auto-converted)
        → commands/<domain>.rs        (returns Result<Model, AppError>)
          → sqlx against SQLite
  → store mutates its $state          (e.g. this.notes = [...this.notes, new])
  → Svelte components re-render reactively
```

`app.view` is a discriminated string. `routes/+page.svelte` is a giant
`{#if/:else if}` over the view names. To add a new top-level
destination, add a string to the union, add a `route` case, add a
sidebar button.

Current view values: `home · list · note · index ·
mirror · feedback · feedback-board · activity · flashdeck ·
blueprints · blueprint · storyboards · storyboard · passwords`.

UI labels diverge from internal names where renames happened — the
internal name stays to avoid touching every callsite. The six primary
destinations live in `TopNav.svelte`, an icon cluster in a reserved top
toolbar row of the main column (Sprint 17/18), not the sidebar; shortcuts
unchanged:

| Internal | UI label             | Shortcut |
|----------|----------------------|----------|
| home     | Home (also logo)     | ⌘1       |
| blueprints| (no toolbar icon)   | ⌘2 (Sprint 47 — TopNav button removed; ⌘2 still opens the Library pre-filtered to Blueprints) |
| index    | Library              | ⌘3 (Sprint 47 — Library; `blueprints`/`feedback`/`storyboards` views now also render `LibraryView` pre-filtered, and the Library hub icon is active for all of them) |
| mirror   | The Mirror           | ⌘4 (Sprint 46 — replaced the Garden/Visualization) |
| feedback | (no toolbar icon)    | ⌘5 (Sprint 47 — TopNav button removed; ⌘5 still opens the Library pre-filtered to Boards) |
| activity | Activity             | ⌘6       |
| flashdeck| Flash Deck           | ⌘7       |
| passwords| Passwords            | ⌘8 (Sprint 41 — encrypted site-password vault) |

`TopNav.svelte` also hosts the **back** button (`app.back()`, ⌘[) —
backed by `app.navStack`, a history stack each `select*`/`open*`/`goHome`
pushes to — plus the theme toggle and the sidebar-tint picker. The
sidebar is now search + pinned items + footer only.

The toolbar row also shows the **current section label** and a **"Search ⌘K"**
pill. **⌘K opens `CommandPalette.svelte`** — the global finder: searches every
entity (client-side over loaded store state) + lists all destinations (with
descriptions) + quick actions. It's the primary way to navigate/search; the
sidebar box is todos-only. `FormattingHelp.svelte` (the in-app markdown
reference) opens from the editors' "Aa" button, Help, and the palette. First-run
shows a dismissible "Start here" card on Home (Sprint 21).

## Svelte 5 patterns we follow

- **All state in the store class.** `app` is a singleton. Components
  read from it and call its actions; they don't hold their own data.
- **`$state` vs `$state.raw`.** Default to `$state`. Use `$state.raw`
  for arrays bound to xyflow (`bind:nodes={flowNodes}`,
  `bind:edges={flowEdges}`) — the deep proxy can swamp the main thread
  during xyflow's high-rate updates. We trigger reactivity by
  *reassigning* the variable, not by mutating it.
- **`$effect` only for side effects / sync.** Avoid using it for
  derivations — use `$derived` instead.
- **Modal pattern**: a child component takes an `onClose` prop and
  renders a full-screen overlay-button + a dialog (see
  `AddEntityModal.svelte`, `FeedbackCardPanel.svelte`).

## Subtle / non-obvious patterns (READ BEFORE EDITING A CANVAS)

> NOTE (Sprint 40): the Alexandria `MapEditor` was removed. The canvas
> patterns below now live in **`BlueprintEditor.svelte`**, which was
> originally copied from MapEditor and carries the same subtleties (single
> combined `$effect`, `$state.raw`, identity caches, `markerEnd`, the
> decorative-endpoint `onConnect` rule). Read them as applying to
> BlueprintEditor; the `MapNodeCard` SVG note is historical (Blueprint
> cards are HTML `BlueprintCardNode`).

### The canvas reactive sync is a SINGLE effect

There's exactly one `$effect` that reassigns BOTH `flowNodes` AND
`flowEdges`. Having two separate effects caused xyflow to drop edges on
node-only mutations (Sprint 12). The effect also maintains
`flowNodeCache` / `flowEdgeCache` Maps so unchanged items keep the same
JS object identity across rebuilds — xyflow's internal reconciler
short-circuits on identity, which keeps the canvas stable.

If you add a new field to map nodes/edges, update `sameNode` /
`sameEdge` to compare it, or refs will go stale.

### Feedback kanban uses pointer events, not HTML5 drag-and-drop

HTML5 DnD is unreliable in WKWebView (Tauri's macOS webview). The
kanban uses `pointerdown` / `pointermove` / `pointerup` +
`setPointerCapture`, a 5-pixel movement threshold to distinguish click
from drag, `document.elementFromPoint` to find the target column, and
a floating ghost card at the cursor. See `FeedbackBoardView.svelte`.

### `MapNodeCard` (entity cards) is SVG, not HTML

xyflow zooms via `transform: scale()` on the viewport, which makes
HTML inside look pixelated on WKWebView at non-1.0 zoom. `MapNodeCard`
renders its body as inline SVG so it stays crisp at any zoom.
`MapTextNode` / `MapCustomNode` / `MapTitleNode` are HTML because they
need editable text — we accept some pixelation there.

### Today's list is never auto-created

`app.init()` does NOT call `listToday()` (Sprint 11). The only path to
creation is the sidebar's "Create today's list" button. Reason:
opening the app on a weekend shouldn't silently make an empty list.

### `MapNode.width` / `height` persistence

`map_nodes` has nullable `width` / `height` REAL columns. NULL ⇒ use
the renderer's default. After `NodeResizer.onResizeEnd`, the new
dimensions are persisted via `app.resizeMapNode(id, w, h)` and
re-read on every flowNode rebuild (Sprint 12).

### `markerEnd` on every edge

`toFlowEdge` in MapEditor sets `markerEnd: { type:
MarkerType.ArrowClosed, width: 18, height: 18 }`. Missing this hides
the direction arrows.

### Connections reject decorative kinds

In `onConnect`, edges are rejected if either endpoint is `text`,
`comment`, or `title`. `custom` IS connectable. The check lives in
`MapEditor.svelte`'s `onConnect`.

### IndexView → SummaryView → LibraryView

The old free-text index doc is preserved in the `index_doc` table but
not surfaced anywhere. `app.view = "index"` renders `LibraryView.svelte`
(Sprint 47 — the unified entity browser). The `blueprints`, `feedback`,
and `storyboards` view values also render `LibraryView` (with a different
`initialKind` prop), so those four destinations are one consolidated
view; only the entity *editors* (`blueprint`/`feedback-board`/
`storyboard`) remain distinct.

### "The Mirror" is a single `<canvas>` (Sprint 46)

`MirrorView.svelte` draws everything imperatively (bars + orbs) on one
canvas via `requestAnimationFrame`, with its own camera (wheel-zoom /
drag-pan in world coords) and a hand-rolled easing/stagger build
animation — no chart lib, no d3-force, CSP/offline-clean. Data comes
from the backend `get_mirror` command (`app.mirror`); orb radius is a
global `log(1+mass)` normalisation so types compare fairly. Bars are
contiguous & centered; orbs beeswarm (notes above, other types below).
Clicking an orb navigates to its entity. The Garden (`GardenView` +
`garden.ts`, d3-force) it replaced was deleted.

## Database

### Migrations

Files in `src-tauri/migrations/0001_…sql` … `0024_…sql`, monotonically
numbered, applied at startup. To add one:

1. Create `00NN_<short_name>.sql`.
2. Use plain `ALTER TABLE` when possible.
3. **CHECK constraint changes require recreating the table** (SQLite
   limitation). Pattern: `PRAGMA defer_foreign_keys = ON;` →
   `CREATE TABLE foo_new (...)` → `INSERT INTO foo_new SELECT …` →
   `DROP TABLE foo` → `ALTER TABLE foo_new RENAME TO foo`. If any other
   table FKs to it, rebuild that one too in the same migration (we do
   this in 0006, 0008, 0010 for `map_nodes` / `map_edges`).

### Tables (high-level)

- `lists` + `todos` + `tags` + `todo_tags`: daily todo plumbing. A single
  **backlog** (Sprint 29) is a sentinel list flagged `is_backlog = 1`
  (migration `0020`, additive column; `date = ''`, get-or-created lazily by
  `lists::backlog`) holding unscheduled tasks; it reuses all todo plumbing and
  is excluded from the daily surfaces (`list_all` / `stats` / `daily_stats` all
  filter `is_backlog = 0`). Tasks move between a daily list and the backlog via
  `move_todo(id, targetListId)` — "Send to backlog" / "Pull to today" per-row
  actions in `TodoRow`/`ListView`; the sidebar shows a pending-count entry.
- `workflows` + `workflow_steps`: REMOVED in Sprint 50 (migration `0026`
  drops both). The workflow entity is gone — replaced by a ```workflow
  markdown block (numbered step chain; `renderWorkflow` in markdownit.ts).
- `notes`: markdown bodies, day-attached (have a `date`), pinned/archived.
  (The `articles` entity was REMOVED in Sprint 51 — migration `0027` drops
  the table; powered markdown absorbed its "wrap other entities" role, so
  it was just a note. The `{{kind:id}}` embed feature + `EmbedBlock` went
  with it — notes never embedded.)
- `index_doc`: legacy single-row markdown summary, preserved for data
  safety but unused in UI.
- `map_nodes` + `map_edges`: **REMOVED in Sprint 40** (migration `0021`
  drops both). The Alexandria master-map canvas is gone; Blueprints
  replaced it. Historical description of what they held: `kind` was one of
  `note · article · workflow · feedback_board · text · comment · custom ·
  title`. The first four reference an existing entity via `entity_id`;
  the last four are decorative (entity_id = 0, content holds text). A
  partial unique index `(kind, entity_id) WHERE kind NOT IN (text,
  comment, custom, title)` enforces one-position-per-entity.
- `feedback_boards` + `feedback_columns` + `feedback_cards` +
  `feedback_card_comments`: kanban. Columns are **per-board, user-editable
  rows** (Sprint 19 — no longer a hardcoded CHECK); a new board seeds four
  defaults in `create_board`. Cards reference `column_id` and carry a
  nullable `color`. Boards have `pinned` (sidebar) + `archived`.
  `#tag`s in board/card titles render as badges (`$lib/badges.ts`).
- `blueprints` + `blueprint_nodes` + `blueprint_edges`: the Blueprints
  section (Sprint 22) — multiple standalone design canvases. Node `kind` is
  `card · text · comment · title · frame`; cards carry `title`/`description`
  (markdown)/`color` and a nullable `image_url` (Sprint 24 — a pasted image
  card, `add_image_card`), decoratives + `frame` use `content` (frame = its
  label). A `frame` (Sprint 24, migration `0019` recreated the table to widen
  the `kind` CHECK) is a labeled resizable rectangle rendered behind cards
  (zIndex 0 vs 1) to group a diagram — visual only, doesn't own its contents.
  No entity references, no partial unique index. Edges persist `source_handle`/`target_handle`
  (`t|r|b|l` — cards have four connection points, loose connection mode)
  plus a `label`. Canvas mutations touch the parent's `updated_at`.
- `flashcards` + `flashcard_categories`: the Flash Deck (Sprint 20). One global
  deck; a card has a markdown `body`, optional `image_url` (else generative art),
  `emoji` + `color` accents, optional `category_id` (ON DELETE SET NULL), and a
  manual `position`. Categories ("suits") carry a color + icon. Generative card
  art is a seeded flat-geometric SVG (`$lib/cardArt.ts`); `FlashCard.svelte` is
  the front, `FlashCardPanel`/`FlashStudyView` add a front↔back flip.
  `{{flashcard:id}}` embeds + `flashcard:id` links like other entities.
- Mermaid: there is **no diagram entity/table** (the Sprint 14 `diagrams`
  table was removed in Sprint 16 — migration `0011` created it, `0012`
  drops it). Mermaid now lives **only** as inline ```` ```mermaid ````
  fences in note/article markdown bodies: `$lib/markdownit.ts` emits a
  `.mermaid-block` placeholder and `hydrateMermaidBlocks` renders it to
  SVG via `$lib/mermaid.ts` (`renderMermaid`, dynamic-imports mermaid).
- All entity tables have `pinned` (sidebar visibility) and `archived`
  (Summary's archive tab) booleans.
- `vault_meta` + `secrets`: the **Passwords vault** (Sprint 41, migration
  `0022`). `vault_meta` (single row `id=1`) holds the Argon2id `salt` + a
  `verifier` blob (a constant encrypted with the derived key) — the master
  password is NEVER stored. `secrets(id, title, password_enc, …)` keeps the
  title **plaintext** (list browsable while locked) and the password
  encrypted as `nonce‖ciphertext` (XChaCha20-Poly1305). The derived key
  lives only in `AppState.vault_key` (backend memory, zeroized on lock);
  see `commands/secrets.rs`. No entity-table conventions apply here.
- `storyboards` + `storyboard_pages` + `storyboard_nodes` + `storyboard_edges`:
  **Storyboards** (Sprint 43, migration `0024`) — a sequence of pages, each a
  tiny canvas + a markdown note. Cloned-and-simplified from Blueprints with a
  **pages** layer: `storyboard_pages(position, note)` are the ordered slides;
  nodes/edges belong to a **page** (`page_id`). Node `kind` is `box · icon ·
  header · comment` (box/icon connectable + 4 handles; header/comment reuse
  `MapTitleNode`/`MapCommentNode`). `get_storyboard` returns
  `{storyboard, pages, nodes, edges}` (all pages at once; the editor filters by
  `currentPageId`). Autosave per mutation; canvas edits touch the storyboard's
  `updated_at`, note edits the page's. `commands/storyboards.rs`,
  `StoryboardEditor.svelte` (reuses the combined-`$effect` sync + identity
  caches + presenter pattern), reached via the command palette + `storyboard:id`
  entity link. v1 has Present (slideshow); PNG export is a fast-follow.
- `checkins`: the **camera check-ins** gallery (Sprint 42, migration `0023`).
  `checkins(id, list_id →lists ON DELETE SET NULL, path, created_at)` — one
  webcam GIF per today's-list creation (opt-in). `path` is the GIF's file in
  the images dir; the frontend captures + encodes the GIF client-side
  (`$lib/checkin.ts` via `getUserMedia` + `gifenc`), saves bytes through
  `save_image`, then records the row. `commands/checkins.rs`.

### Tauri command conventions

- Backend function name = command name (snake_case).
- Register in `src-tauri/src/lib.rs` `tauri::generate_handler![]`.
- Frontend `invoke("snake_case_cmd", { camelCaseArgs })`; Tauri does
  the case conversion. **Don't** send snake_case from JS or args go
  missing.
- All models use `#[serde(rename_all = "camelCase")]` so JS sees
  `createdAt`, `entityId`, etc.

## Known quirks

- **xyflow zoom pixelation** on HTML node bodies in WKWebView is
  unavoidable for HTML content; we mitigate by using SVG inside
  `MapNodeCard` and capping `fitViewOptions.maxZoom = 1`. Text /
  custom / title nodes accept some softness on zoom.
- **`cargo test`** can fail with `failed to read plugin permissions:
  …bigpicture_app/…` referencing a stale build cache path. `cargo
  clean` inside `src-tauri/` fixes it. The bug is in the cached Tauri
  build script, not in our code.
- **`map_nodes` / `map_edges` were dropped in Sprint 40** (migration
  `0021`); the paragraph below is historical (those tables no longer exist).
- **Migrations 0006 / 0008 / 0010** recreate `map_nodes` (and
  `map_edges` to refresh the FK). If you alter `map_nodes`'s CHECK
  again, follow the same pattern.

## When developing

- **Plan first for non-trivial changes.** Write a SPRINT doc in
  `documentation/` before coding the feature. Existing sprints are the
  template — keep them honest about tradeoffs.
- **Test the round trip.** After any DB or IPC change: cargo check +
  svelte-check + manually load the affected view.
- **Don't try to fix xyflow zoom pixelation with CSS** — we've tried
  every CSS hint over multiple sprints (Sprint 9-11 history). The only
  fix is SVG content. Take the tradeoff.
- **Treat the sprint docs as the deep context source.** Each sprint
  records why a feature is shaped the way it is. Read the relevant
  ones before changing related code.

## Quick wins for a fresh Claude session

1. Read this file (you're doing it).
2. Skim `documentation/SPRINT*.md` in order; bias toward 9–12 for
   anything canvas / kanban / activity-related.
3. Open `src/lib/stores/app.svelte.ts` and `BlueprintEditor.svelte`. These
   two files encode most of the architectural choices.
4. Run `pnpm tauri dev` once to confirm migrations apply cleanly on
   your machine.

Last updated: end of Sprint 67 (Per-block editing · section jumper · note-styling refresh — three
threads for big notes, all frontend (no DB/IPC/migration). (1) PER-BLOCK EDITING: hover a block in a
note preview → a pencil (right margin) → an in-place textarea over just that block, seeded with its
raw markdown, Save (⌘↩) splices it back & commits (Esc cancels). Enabled by SOURCE RANGES on every
block: `addLineNumbers` stamps `data-line`+`data-end-line` (start + exclusive end from `token.map`) on
regular blocks, and a `withSourceRange()` wrapper on the fence rule injects the same into every
powered/code block's outer element. New `replaceLinesInSource(src,start,end,text)` splice helper
(sibling of toggleTaskInSource). MarkdownEditor: `previewWrap` (relative) hosts the pencil+overlay;
`onPreviewMove` finds the block via `closest("[data-line][data-end-line]")`; notes only (`!readOnly`),
preview only. Pencil is in the RIGHT margin (`right:-1.75rem`) to avoid colliding with a block's own
top-right controls (📷/GIF) + progress steppers, with HOVER-INTENT (240ms hide delay cancelled by the
pencil's mouseenter) so it doesn't vanish mid-reach. (2) SECTION JUMPER: replaced the always-on
floating heading column (it overlapped the note) with an on-demand "≡ Sections" button above the Edit
FAB (bottom-right) → a popover of h1–h3 (indented), click to smooth-scroll; shown for ≥2 headings,
hidden while split/block-editing. (3) NOTE STYLING (all theme-accent-driven): headings → SERIF display
face (`ui-serif`→system New York/Iowan, h1 hairline rule; scoped); inline `code` → a copyable BADGE
(`code_inline`→`<code class="md-badge" data-code=…>`+ always-visible copy button; `installInlineCopy`
delegated copies the exact text); plain `>` (no `[!TYPE]`) → a SOFT NOTE card (`blockquote:not(.callout)`,
accent bar+tint+quote glyph); CALLOUTS redesigned to rounded tinted panels w/ a left bar + per-type ICON
(`CALLOUT_ICON` map → note info · tip bulb · important star · warning/caution triangle · comment bubble);
SUBLISTS step ●→○→▪ and 1.→a.→i. (bullet under a number stays a bullet) with accent `::marker`; TASK
checkboxes use `accent-color:var(--accent)`. Specificity fixes: scoped `ul/ol{list-style}` was beating
app.css nested rules (→ all lists showed the top marker) so list-style moved wholesale to app.css; a
generic `.md-badge-copy svg{display:block}` beat the check-hide rule (→ both icons showed) so it was
removed. Files: `markdownit.ts`, `MarkdownEditor.svelte`, `app.css`. Mocked up in three Artifact rounds
first. svelte-check + build pass; DOM/interaction bits need a live webview run. Deferred: per-list-item
editing, surgical single-block re-render, and the un-taken style ideas (link chips, divider, rhythm).
See documentation/SPRINT67.md. — earlier: Sprint 66 (Voice notes per todo list — an on-demand audio note recorded per
list, the audio sibling of the Sprint 42 camera check-ins (near-1:1 reuse; simpler because
`MediaRecorder` returns a finished blob — no encoding lib). CAPTURE `src/lib/voicenote.ts`
`startVoiceRecording()` → `getUserMedia({audio})` + `MediaRecorder`, feature-detects the container
(WKWebView `audio/mp4`→m4a · Chromium webm/opus via `isTypeSupported`); returns
`{label, stop(), cancel()}` where `stop()` resolves `{bytes, ext, durationMs}` and `label` is the
active mic's device name (empty until permission granted). BACKEND migration `0029_voice_notes.sql`
(`voice_notes(id, list_id→lists ON DELETE SET NULL, path, duration_ms, created_at)`),
`commands/voice_notes.rs` (add/list/delete; delete removes the file; 2 tests), `VoiceNote` model,
registered in lib.rs; bytes saved through the existing `save_image` command (files land in the images
dir). STORE `voiceNotes` (loaded in init) + `recordingListId`/`recordingMicLabel`/`recordingStartedAt`
+ `startVoiceNote`/`stopVoiceNote`/`cancelVoiceNote`/`deleteVoiceNote`; one recording at a time, NO
opt-in toggle (recording is explicit consent, unlike the camera's ambient capture), MULTIPLE notes per
list (append). UI `ListView`: a mic button (→ red "Stop m:ss" while recording this list), a recording
banner (pulse + live `m:ss` timer via a 250ms `$effect` interval from `recordingStartedAt` + the
selected mic label, "default mic" fallback), and a per-list player list (`<audio controls>` + duration
+ delete, newest first; hidden for Backlog). `NSMicrophoneUsageDescription` added to Info.plist. ipc
`addVoiceNote`/`listVoiceNotes`/`deleteVoiceNote` + `voiceNoteSrc` (convertFileSrc). Deferred:
waveform, max-duration cap, an ActivityView gallery tab, transcription. svelte-check + cargo check + 2
tests + build pass; the real WKWebView `MediaRecorder` capture / container / `<audio>` playback / mic
prompt need a live `pnpm tauri dev` run (same caveat as the camera check-ins). See
documentation/SPRINT66.md. — earlier: Sprint 65 (Check-in polish · animated canvas tints · theme accent · shortcut
cleanup — a UX/theming grab-bag. (1) CAMERA CHECK-INS: `captureCheckinGif` now shows a small
non-invasive live PREVIEW (bottom-right, mirrored) with a 3→2→1 COUNTDOWN so you can frame yourself,
and burns a DATE STAMP into each frame (`checkinStamp(new Date())` → "Thursday · Aug 14, 2026", drawn
after the mirror transform); the gallery gained a per-GIF DOWNLOAD button (native Save As →
`read_binary_file` + `save_binary_file`; the opener-plugin open-folder/reveal path was blocked by
scope so it was dropped). (2) THREE ANIMATED CANVAS TINTS — `SidebarFx.svelte`, a hand-rolled
`<canvas>`+rAF loop (no lib, like the Mirror/aurora) in the same `z-index:-1` backdrop slot:
**glitter** (drifting twinkling dots + shimmer), **fireworks** (starbursts w/ trailing gravity
sparks), **meteor** (starfield + shooting-star streaks). New `SIDEBAR_TINTS` entries w/ an `fx` field
+ `base`; `theme.sidebarFx` (light-only, like aurora) renders it in the Sidebar; reduced-motion → one
static frame; `{#key}` remounts on switch. (3) SCREENSAVER: Focus mode fills its stage with the
selected tint's canvas fx when it's an fx tint (`theme.selectedFx`, works in light AND dark since the
stage is always dark), else the aurora backdrop; plus a prominent accent-filled **Enter Focus** button
in the sidebar footer. (4) THEME ACCENT: each tint contributes an `accent` (`tintAccent`; hue tints
derive it, others explicit) published as `--accent` on `<html>` (both modes); new `.btn-accent`
(app.css: `var(--accent)` fill, white text, `color-mix` hover) swept across ALL primary CTAs (sidebar
Add/Enter-Focus, Home new-list, Library +New, AddEntityModal, note Edit FAB, Storyboard Save PNG,
Flash Deck, Passwords, feedback Save) — so buttons follow the tint (Fireworks=red, Meteor=blue, …).
The TopNav toolbar also recolors (hub pills + active icon + split-active use `--accent`); selection
row highlights left blue by design. (5) SHORTCUTS trimmed to a Stream-Deck set — ⌘1 Home · ⌘2 Add ·
⌘3 Mirror · ⌘4 Activity · ⌘5 Passwords · ⌘6 Screensaver · ⌘7 Split view · ⌘8 Random theme; removed
⌘F/⌘[/⌘\\/⌘N/⌘E/⌘⇧C/T/B/N/S + old ⌘2/3/5/7 view-nav (still reachable via TopNav + palette); kept
⌘K/Esc/?/Enter/Tab. HelpModal, CommandPalette hints, and TopNav tooltips updated to match; the TopNav
**Focus icon was removed** (now in the sidebar). (6) Removed the sidebar **build/commit** footer
(`__APP_COMMIT__*`). Frontend + one backend command, no migration; svelte-check + cargo check + build
pass; the preview/stamp/save-dialog + canvas anims + toolbar recolor need a live webview run. See
documentation/SPRINT65.md. — earlier: Sprint 64 (Reference list blocks — two powered-markdown blocks that render a
list of internal entity links as a distinct "related items" component instead of the generic blue
link-chips. Both parse the same body (one `[label](kind:id)` per line, an optional `- `/`* `/`1. `
list marker tolerated; labels are authored inline so they render SYNCHRONOUSLY like list/files/stats,
no store/IPC — unlike the async `{{board N}}` embed). `parseEntityLinks` resolves each `kind:id` to a
color + kind label + icon (note blue · blueprint violet · board teal · list green · storyboard pink ·
flashcard amber; external `https://` → globe/gray/hostname). ```links [title] (`renderLinks`) → a
bordered `.md-links` list w/ a `blockHeader` (title default "References" + count) and one `<a
href="kind:id">` row each: a kind-colored icon TILE (color via `--lc` set inline so the CSS is
kind-agnostic) + ellipsised label + uppercase kind word + a hover ↗; PNG-copyable. ```linkchips
[title] (`renderLinkChips`) → the same links as compact "see also" pills (colored dot + label,
optional small title); no PNG. NAVIGATION: the anchors reuse MarkdownEditor's `onPreviewClick` →
`navigateEntity`, and `board` became a first-class entity link there (added to the regex +
`navigateEntity`→`openFeedbackBoard`; previously boards were reachable in markdown only via the embed).
GOTCHA: the Sprint 23 chip rule `a:not(.md-card)` boxed every anchor blue — extended its opt-out to
`a:not(.md-card):not(.md-link-row):not(.md-linkchip)` (any future block rendering its own anchors must
add itself). Slash "Reference list"/"Reference chips" (Lists & ideas) + FormattingHelp; mocked up 4
options as an Artifact first (rows + chips chosen). Frontend-only, no backend/migration; svelte-check
+ build pass; anchor clicks need a live webview run. See documentation/SPRINT64.md. — earlier:
Sprint 63 (Split view — a read-only REFERENCE pane beside the editable main
pane. `+page.svelte` toolbar split button (`app.toggleSplit`) turns the main content area into a
horizontal flex with a draggable divider (`splitFraction` 0.25–0.82, pointer-capture); left = the
app as-is (global selection/sidebar/nav/palette unchanged), right = `SecondaryPane`. Store:
`splitOpen` + `splitRef {kind:note|blueprint|board, id, title}` (null while open → picker) +
toggleSplit/openSplitRef/closeSplit. SecondaryPane empty state = a picker (search + "Recently
edited" notes/blueprints/boards by updatedAt); reference renders note + board via the SAME
`MarkdownEditor` in a new `readOnly` mode (identical output — the fix for a style mismatch that came
from a bare `md.render`; board = its `{{board N}}` embed), blueprint via a static fit-to-width SVG
overview (`get_blueprint` → cards at saved positions + edges, no xyflow). Header: open-in-main /
Change / ✕. `readOnly` prop on MarkdownEditor: preview only — `startEditing` no-ops, edit
buttons/FAB hidden, `data-md-sections` persist hook dropped, source-mutating clicks ignored (links
still navigate). The floating heading outline hides while split is open (`!app.splitOpen`). Only
note/blueprint/board; read-only by design. svelte-check + build pass; content loads via IPC (needs
a live webview run). See documentation/SPRINT63.md. — earlier: Sprint 62 (Embed a feedback board in a note — `{{board N}}` on its own line
renders a READ-ONLY mini-kanban of board N. Since a synchronous fence can't reach the store/IPC,
`addBoardEmbeds` is a core rule that turns a paragraph of just the marker into a placeholder
`<div class="md-board-embed" data-board="N">`; `hydrateBoardEmbeds(el)` (exported, called from
MarkdownEditor's hydration `$effect` + MutationObserver, guarded per-placeholder via
`data-rendered`) fetches `listFeedbackBoards`/`listFeedbackColumns`/`listFeedbackCards` and fills
`boardEmbedHtml` — header (title + card count) + columns (name + count) + card chips (title +
`cardAccent` rail + comment count). Kanban look: tinted board area, transparent columns, white
cards, columns `flex:1 1 0` to fill width; 📷 PNG button. Clicking the embed header opens the board
(`app.openFeedbackBoard` via `onPreviewClick`). Boards now show an id chip in the board header
(`IdChip` gained a `board` kind that displays+copies `{{board N}}`). Slash "Embed a board" (Lists &
ideas) + FormattingHelp; the interim ```board fence was removed. svelte-check + build pass; board
content loads via IPC so it needs a live webview run. See documentation/SPRINT62.md.
— earlier: Sprint 61 (Blueprint block · collapsible-section overhaul · task notes.
NEW ```blueprint [title] (`renderBlueprint`): the Blueprint import DSL rendered inline as a small
static diagram that LOOKS like the Blueprints canvas — `Name: desc [- color]` → a card, `A -> B
-> C` → edges (auto-create nodes); longest-path (Kahn) left→right layout; a DOT-GRID scene
(`.md-bp-scene`, `min-width:100%` fills the block) with HTML cards (left accent bar + shadow +
bold centered title + 2-line desc, like `BlueprintCardNode`) over an SVG edge layer (animated
dashed arrows, pinned top-left so viewBox maps 1:1 to card px); connection-handle dots on the card
border where edges attach; per-card `- <color>`; PNG copy, NO GIF. Slash "Blueprint (diagram)"
(Charts & visuals) + FormattingHelp. COLLAPSIBLE SECTIONS restyled + made PERSISTENT: single card
w/ a DARK BAR header (small centered Oswald title + chevron); the open/closed status now lives in
the SOURCE — `## >` collapsed / `## >>` open — each `<summary>` has a `data-section` index and
`toggleSectionInSource` flips the marker (mirrors `toggleTaskInSource`); MarkdownEditor's preview
is `[data-md-sections="persist"]` and handles the click (flip+save) while the global
`installSectionToggle` bails there (ephemeral toggle stays for read-only surfaces) — so expand →
edit → back keeps it open (survives restart). TASK NOTES (`Inspector.svelte`): the description uses
the notes locked floating-edit (`floatingEdit` + new `floatingContained` prop anchoring the FAB to
the modal via `absolute` vs `fixed`); modal widened `max-w-2xl`→`max-w-4xl`. ```list gained an
optional ` — description` row per idea. svelte-check + build pass. See documentation/SPRINT61.md.
— earlier: Sprint 60 (Workflow card · slash categories · ```list block —
(1) ```workflow [title] (`renderWorkflow`) now renders in a CARD (`.md-workflow-block`) with a
fence-info header defaulting to "Workflow" + step count, a per-step hover, and a 📷 PNG copy
button (via `withImgCopy`, no GIF). (2) SlashMenu commands gained a `cat` field + are grouped
under headers in menu order (Basic · Lists & ideas · PR blocks · Charts & visuals) via a
`.slash-cat` header rendered on category change; filter/keyboard nav unchanged. (3) NEW ```list
(`renderList`) — a non-workflow list of ideas styled like the files block (container card, rows
split by a hairline, colored left rail). Per line `idea [— description] [- <color>]`: trailing
` - <color>` (NAMED_COLORS) tints the rail (default gray), optional ` — `/` -- `/` # ` adds a
muted description row; title+desc take inline markdown; hover tints the row; NO export buttons.
Slash "List of ideas" (Lists & ideas) + FormattingHelp row. svelte-check + build pass. See
documentation/SPRINT60.md. — earlier: Sprint 59 (Backend PR blocks — four more powered-markdown blocks in
`$lib/markdownit.ts`, each with a header from the FENCE INFO (shared `blockHeader`→`.md-bhead`,
not a `heading:` body line), a PNG copy button, and a GIF export button where there's motion.
```terminal [title] [animated] (`renderTerminal`): console window, fence info = title bar, `$`
lines are commands, `animated` streams lines in. ```tree [title] (`renderTree`): file/dir tree
(2-space indent = depth; a trailing ` - new` [green] / ` - edit` [amber] legend tags the file,
no line counts), a line ending `pulse` breathes its TEXT. ```flow [title] (`renderFlow`): linear pipeline, `Name: sublabel` per line, ≤4
horizontal / 5+ auto-vertical; a plain marker glides the path and each node hover-highlights
(border+tint+lift) as it arrives, synced via per-node `--fdelay`. ```compare [title]
(`renderCompare`): before/after split by `---`, each an inset code panel, crossfading. GIF ENGINE
rewritten (`installGifSave`) — general multi-frame STATE-DRIVEN capture: freeze live CSS via
`.md-cap`, drive each frame from JS (flow marker interp + `.on` node / compare layer opacity /
terminal line reveal / pulse+tree `--capop`), rasterize each with html-to-image `toCanvas`, encode
a looping GIF (gifenc). WKWebView robustness unchanged (white pad, inline opaque bg, zeroed inner
margin, content-box oversized canvas, fonts.ready + warm-up); native save + browser-download
fallback (clipboards can't carry animation → SAVE not copy). PNG path (`installBlockImageCopy`)
unchanged, on every block. ALSO refined ```files: no more `+N/-N` counts — the status renders as
a colored word label (`new`/`edit`/`delete`/`rename` via `--st`) and the per-file note is black.
Slash (Terminal/File tree/Flow/Before-after) + FormattingHelp + demo rewritten as a backend PR. svelte-check + build pass; GIF save + image clipboard write still need a
live webview run. See documentation/SPRINT59.md. — earlier: Sprint 54 (PR / code-doc markdown blocks — a family of powered-markdown
blocks in `$lib/markdownit.ts` for writing PR descriptions / code findings, all synchronous/
CSS-only (render in note previews + blueprint cards) and copy-as-image-able. ```files
(`renderFiles`): one file per line `<A|M|D|R> path [+adds] [-dels] [pulse] [— note]` — status
colors the row (left rail `--st` + chip), path = dimmed `dir/` + bold filename (plain mono text,
NO pill — a pill left a gap in the copied image on mono-font substitution), a header sums
`N files changed` + total `±lines`, note = description row w/ inline markdown. ```stats
[theme] (`renderStats`): `Label: value` → metric cards (`+N`/`−N` green/red); optional `heading:`
→ header bar + metric count in a panel. ```spec [theme] (`renderSpec`): `Label: value` sheet,
theme-tinted neutral key column, values take inline markdown (`md.renderInline`); optional
`heading:` → header bar + field count. ```cards: optional `heading:`/`desc:` first block →
header bar + card count in a panel. SHARED: `blockHeader()`→`.md-bhead` GitHub-style header
(files/stats/spec/cards). SURFACE THEMES (stats/spec only): a fence keyword → `.md-theme-*`
class (`surfaceThemeClass`) setting CSS vars (`--surf/--ink/--line/--head-bg/--card-base/
--neutral/--pos/--neg`); themes github (DEFAULT) · light · dark · midnight · slate. NO accent
color (tried + removed as noisy) — blocks are theme-only. PER-ITEM `pulse`: trailing `pulse` on
a stat card / spec row / file row (`peelPulse`) → `.md-pulse` neutral breathing overlay+ring
(currentColor, reduced-motion-safe). COPY-AS-IMAGE: files/stats/spec/cards wrap in `.md-block`
(`withImgCopy`) + hover 📷; `installBlockImageCopy` (delegated capture-phase, like
`installCodeCopy`) rasterizes via html-to-image `toBlob` 2× and copies a PNG (native Tauri
`copy_image_to_clipboard`, else `navigator.clipboard.write`; both dynamic-imported). WKWebView
robustness: WHITE padding (blends into a light PR), force every opaque bg inline before capture
(foreignObject drops CSS bg), zero the inner block's margin (equal padding across block types),
`content-box`+oversized canvas (no clip), `await document.fonts.ready` + a warm-up pass. SAVE AS
GIF: a files/stats/spec block with a `pulse` item also shows a "GIF" button (`installGifSave`) —
clipboards can't carry animation, so it SAVES a looping GIF (native dialog; browser fallback =
download) to drag into a PR: rasterize a clean base ONCE (live pulse hidden via a temp
`.md-nopulse` class), then composite the breathing overlay over each `.md-pulse` rect per frame on
a canvas (1 raster + compositing, not N) and encode ~20 frames with `gifenc` (infinite loop, same
`0.18→1` ease as the CSS). Slash
(Changed files/Stat cards/Spec sheet) + FormattingHelp + `pr-blocks-demo.md`. svelte-check +
build pass; the image CLIPBOARD WRITE still needs a live webview run to verify. See
documentation/SPRINT54.md. — earlier: Sprint 55 (Collapsible toggle sections — a heading whose text
starts with `>` (e.g. `## > Roadmap`) becomes a `<details>` section COLLAPSED by
default, body = every block down to the next same-or-higher heading. `addCollapsibleSections`
in `$lib/markdownit.ts` is a core rule (after `line_numbers`) that wraps toggle headings
with `section_open`/`section_body_open`/`section_close` marker tokens (level-stack close
rule; strips the `>` from the heading's inline content + first text child); render rules
emit `<details><summary>…</summary><div class="md-section-body">…</div></details>`.
`installSectionToggle()` is a capture-phase delegated click listener (like `installCodeCopy`)
that owns the toggle — `preventDefault`+`stopPropagation` so it never trips a surface's
click-to-edit, flips `details.open` (a link inside the heading still navigates).
`.md-section*` CSS (disclosure triangle `::before` rotates when open). Opt-in by the marker
→ plain headings/existing notes untouched; nested toggles nest. Slash "Toggle section" +
FormattingHelp row. See documentation/SPRINT55.md.
(Sprint 54 numbering note: SPRINT54.md now consolidates the whole PR-blocks feature; the old
per-pass docs 53/56/57/58 were folded into it.)
— earlier: Sprint 52 (Home visual — added a "Your activity" **ridge** + a
dark Today card in `Welcome.svelte`. The ridge is a full-width canvas band, one bar
per day spanning your history so far (first activity → today, capped ~52 weeks),
height = tasks that day (from `app.dailyStats`),
fixed Magma gradient, centered mirror-style; animates in on mount (rAF + per-bar
stagger, reduced-motion-safe), and the whole card is a button that opens the Mirror
(⌘4). Shown only when ≥1 day has tasks; sits BELOW the contribution calendar. The Today card's
surface + text **follow the sidebar tint** — it uses `var(--sidebar-bg)`/`--sidebar-border`
+ `class:dark={theme.isSidebarDark}` (same mechanism as the Sidebar), so the tint picker
customizes it too (Ink default → black card; a colored tint tints the card; inner controls use
light/dark Tailwind variants that respond to the local `.dark`). Frontend-only, no backend/store
change. Picked from a
4-option mockup (mini-Mirror / aurora / generative art / calendar-as-hero). svelte-
check + build pass. See documentation/SPRINT52.md. Also (post-52 fixes): camera
check-ins now fire from `createHomeToday`/`createFocusToday` too (they created lists
without calling `maybeCaptureCheckin` — the Home "Create today's list" button was
silently skipping the capture); and ListView gained a **camera button** to
take/replace a list's check-in on demand (`app.captureListCheckin(listId)` — captures
a GIF, deletes the list's existing check-ins, adds the new one; ignores the opt-in
toggle since the click is explicit consent). Also: `addHomeTodo` now syncs `this.todos`
when the same list is open (the Home Today card + list view are separate arrays and
`select()` short-circuits, so adding on Home didn't show in the list until a reload).
Also: the note editor (MarkdownEditor with `floatingEdit`) now has a **LOCKED edit
mode** — blur only SAVES the draft and stays in edit mode (so switching windows/apps
never renders or scroll-jumps behind your back, and you resume editing on return); you
leave edit mode explicitly via a **Done** FAB (toggle of the preview's Edit FAB).
Non-note MarkdownEditor surfaces keep the classic click-outside-to-preview. — earlier:
Sprint 51 (Removed the Article entity — powered markdown
(link cards + entity links) absorbed its "wrap other entities" role, so articles
were just notes; the author migrated them into notes manually. Full-stack removal
mirroring Sprint 50: migration `0027_drop_articles.sql` (DROP `articles`); deleted
`commands/articles.rs` (+ mod/8 handlers) and models `Article`/`ArticleSummary`;
`WeeklyActivity` lost its `articles` count and `activity_stats`/`get_mirror` stopped
querying articles (mirror test now expects 2 today-entities). Frontend: deleted
`ArticleView`, `ArticleEditor`, and **`EmbedBlock`** (the sole `{{…}}` transclusion
surface — gone with articles; notes never embedded), removed the article slice from
the store (state, `article` view/NavLoc, all `*Article*` methods, the quick-article
feature `quickArticleId`/`toggleQuickArticle`/`openQuickArticle`/⌘⇧A, nav switches),
and the `article` kind everywhere — Library, Sidebar pins, AddEntityModal,
CommandPalette, EntityLinkPicker, IdChip, MarkdownEditor (entity-link regex +
navigate), markdownit CARD_ENTITY, Welcome (empty-state + Jump-back-in), MirrorView
(type/hue/navigate/copy), HelpModal (⌘⇧A), `+page` (view/label/dispatch/shortcut).
`ActivityView`'s Kandinsky weekly cell now shows 2 figures (notes·lists) not 3.
Embeds + `{{…}}` are gone (old embeds/`article:` links are inert — acceptable).
90 cargo tests + svelte-check + build all pass. See documentation/SPRINT51.md.
— earlier: Sprint 50 (Removed the Workflow entity; added a ```workflow
markdown block. The author doesn't create workflows, so the full CRUD entity was
retired. NEW BLOCK: `renderWorkflow` in `$lib/markdownit.ts` (synchronous fence) —
one step per non-empty line, `` `backtick` `` segments → tag badges; numbered blue
bullets joined by a connector line (`.md-workflow` CSS), matching the old entity's
style. Slash command "Workflow (steps)" + FormattingHelp row. REMOVAL (full-stack):
migration `0026_drop_workflows.sql` drops `workflow_steps`+`workflows`; deleted
`commands/workflows.rs` (+ mod/handler regs) and models `Workflow`/`WorkflowSummary`
/`WorkflowStep`; `WeeklyActivity` lost its `workflows` count (Activity view now
shows 3 figures — notes·articles·lists — not 4). Frontend: deleted `WorkflowView`
(+ the unused legacy `IndexView`), removed the workflow slice from the store (state,
`workflow` view value/NavLoc, all `*Workflow*` methods, nav switches), and the
`workflow` kind everywhere it was woven — Library, Sidebar pins, AddEntityModal,
CommandPalette, EntityLinkPicker, IdChip, EmbedBlock (`{{workflow:id}}`),
MarkdownEditor/ArticleEditor (entity-link + embed regex + navigate), placeholders,
Welcome empty-state, `+page` (view/label/dispatch). Kept the `workflow` concept
icon in `storyIcons.ts` (used by the Storyboard icon picker — unrelated). 95 cargo
tests + svelte-check + build all pass. See documentation/SPRINT50.md. — earlier:
Sprint 49 (Sidebar redesign + drag-to-reorder pins — the
7 near-identical pinned blocks (Workflows/Articles/Notes/Blueprints/Storyboards/
Boards/Flashcards) collapsed into ONE unified "Pinned" list: a flat, single-
header list where a type-colored icon conveys kind (no per-type headers / repeated
pin stars), hover reveals an unpin ✕, active entity highlighted. **Drag to
reorder** is pointer-based (HTML5 DnD is unreliable in WKWebView — same reason the
kanban uses pointer events): `pointerdown` + setPointerCapture, 5px click-vs-drag
threshold, live insertion index from non-dragged rows' midpoints, `animate:flip`
slides the rest, dragged row lifts; on drop the order persists. PERSISTENCE
(full-stack): migration `0025_pin_order.sql` (`pin_order(kind, entity_id,
position)`), `commands/pins.rs` `get_pin_order`/`set_pin_order` (wholesale-replace
tx, self-heals; models `PinOrder`/`PinKey`; 1 test; registered as
`get_pin_order_cmd`/`set_pin_order_cmd`), ipc `getPinOrder`/`setPinOrder`, store
`pinOrder` (`"kind:id"→position`) + `loadPinOrder()` (in init) + `reorderPins`
(optimistic then persist); sidebar sorts by it, unordered pins fall to the end.
Today's-list card gained a mini progress bar; ＋ Add icon rotates on hover; entrance
uses `$lib/anim` `reveal` (staggered, reduced-motion-safe). Search/brand-edit/
commit popover/aurora/collapse/today-detection unchanged. 108 cargo tests +
svelte-check + build all pass. See documentation/SPRINT49.md. — earlier:
Sprint 48 (Home, redesigned — `Welcome.svelte` rewritten to
lead with action, not counts. OUT: the Articles/Notes/Blueprints counter cards,
the Library/Mirror quick-nav cards, and the per-kind bucket list (all redundant
with the toolbar + Library). IN: (1) a time-aware **greeting** + a header New-list
button (creates today's list, or "Open today's list" if one exists); (2) a
**Today card** — today's list as checkable tasks + progress bar + inline "Add a
task", with a **Backlog pill** (pending count → Backlog); empty state = "＋ Create
today's list" CTA + backlog line; (3) **Jump back in** — the 6 most-recently-touched
notes/articles/blueprints/boards/storyboards (type colour+icon + "edited Xago"),
click to resume. KEPT the contribution **calendar** + day-detail panel + first-run
Start-here card. Store gained a self-contained Home-Today slice (`homeListId`/
`homeTodos` + `loadHomeToday`/`createHomeToday`/`toggleHomeTodo`/`addHomeTodo`,
mirroring Focus); `Welcome` loads it on mount + via a guarded `$effect` (handles
the async-init race). New `$lib/anim.ts` `reveal` action (Web Animations API:
staggered fade-up, reduced-motion-safe) drives the entrance — same no-dependency,
hand-rolled approach as the Mirror (NOT anime.js); reusable. Frontend-only, no
backend/migration. svelte-check 0/0, build clean. See documentation/SPRINT48.md.
— earlier: Sprint 47 ("The Library" — consolidated four list views into
one. Summary + the Blueprints/Feedback/Storyboards index views were the same
"list of entities with open/pin/archive/delete" (the dedicated ones just added
"+ New"). New `LibraryView.svelte` unifies them: a toolbar (title · search · sort
recent/A–Z/type · grid⇄list · "+ New" → existing `AddEntityModal`) + HORIZONTAL
filter chips (`All · Pinned │ Notes · Articles · Blueprints · Boards ·
Storyboards · Workflows · Flash cards │ Archived`, colour dot + live count) —
chips instead of a second left rail so it coexists with the app sidebar. Cards
(or list rows): type colour+icon, title (`#tag` badges for boards/flashcards),
meta = updated date + type-native metric (nodes/pages/cards/steps, straight off
the existing summaries), pin toggle, hover actions (rename [blueprint/board/
storyboard only] · archive · delete; restore/delete under Archived); Pinned
surfaces to the top. Reuses ALL existing store actions — NO backend/ipc/store
change. Low-risk wiring: the four view values (`index`/`blueprints`/`feedback`/
`storyboards`) + their open methods/shortcuts/TopNav icons are KEPT; they now
render `LibraryView` with a different `initialKind` (index→all, blueprints→
blueprint, feedback→board, storyboards→storyboard), so ⌘3 = Library and ⌘2/⌘5
open it pre-filtered; entity editors untouched. The now-redundant TopNav
**Blueprints + Feedback icon buttons were removed** (⌘2/⌘5 shortcuts still route
to the pre-filtered Library; the Library hub icon lights up for index/blueprints/
feedback/storyboards). TopNav "Summary"→"Library";
section labels/palette/Help/Welcome/Sidebar copy updated. REMOVED SummaryView/
BlueprintsView/FeedbackBoardsView/StoryboardsView. Daily Lists dropped from the
browse (they live in Home). Prototyped as an approved mockup. svelte-check 0/0,
build clean. See documentation/SPRINT47.md.
— earlier: Sprint 46 ("The Mirror" — replaced the Visualization/Garden.
A data-portrait of the whole corpus on one time axis: centered contiguous **bars**
= todo lists (height & Magma-gradient colour = task count), **orbs** = every
artifact (notes float above, articles/blueprints/boards/storyboards below), sized
by a global `log(1+mass)` normalisation, placed at creation time, beeswarmed,
each a **click-through link** to its entity (+ hover tooltip). Zoom/pan (scene
wider than the window), a time-lapse build animation, light/dark, reduced-motion
safe — all on ONE `<canvas>` in `MirrorView.svelte` (no chart lib/d3; hand-rolled
camera + easing; CSP/offline-clean). Backend `get_mirror` (`commands/search.rs`,
models `MirrorPoint{kind,id,title,createdAt,mass}`/`MirrorList{id,date,tasks,done}`
/`MirrorData`) computes per-type mass in SQL (notes/articles = `length(body)`;
blueprint = nodes+edges; board = cards+comments; storyboard = nodes+pages) + the
lists terrain (archived+backlog excluded); 1 test. ipc `getMirror`; store
`openMirror`/`invalidateMirror` (in refreshLists) + `mirror`/`mirrorLoading` state,
view `garden`→`mirror` (⌘4, TopNav/palette/Welcome/Help updated). Bars pick one
of six magnitude ramps (Magma/Ember/Sunset/Ocean/Viridis/Forest) at RANDOM per
open (+ a 🎨 shuffle button); the five orb/type colours are DERIVED as a
complement (opposite hue) of the active ramp so a shuffle re-themes the whole
scene at once (HSL helpers in-component). The info/legend panel is collapsible
(collapsed by default) so it never blocks the view. REMOVED
`GardenView.svelte` + `garden.ts` + the garden store slice + `buildGraph` (no DB
change — Garden owned no tables). Prototyped as an approved Artifact mockup first.
107 cargo tests + svelte-check + build all pass. See documentation/SPRINT46.md.
— earlier: Sprint 45 (Note editor "stay where you were" — two
long-note fixes in `MarkdownEditor`, both powered by a new source-line map.
`$lib/markdownit.ts` `addLineNumbers` is a core rule (`line_numbers`, pushed
last) that stamps each top-level block token with `data-line="<0-based source
line>"` via the default `renderToken` (custom fences ignore attrs → no line,
inert on all non-note surfaces). (1) **Scroll-to-edited**: `commit()` records
`pendingScrollLine` = caret's source line at blur; an `$effect` keyed on
`previewEl` (undefined→defined on the edit→preview swap) scrolls the block with
the largest `data-line ≤` that line into view (center), so leaving the editor no
longer jumps to the top. (2) **Floating Edit FAB** (new `floatingEdit` prop,
NoteView passes it): hides the inline top-right + bottom Edit buttons and shows a
single pill FAB fixed bottom-right (`fixed bottom-6 right-6 z-20`), always
reachable while reading; a plain preview click does nothing (reading stays
uninterrupted). Helper `lineAtOffset` for the scroll restore. Notes only;
Articles/other surfaces keep the inline buttons. No dep/backend/migration.
svelte-check 0/0, build clean. See documentation/SPRINT45.md. — earlier:
Sprint 44 (Icons in powered markdown — the curated
Storyboard icon set (Lucide concept line icons + Devicon brand logos, from
`$lib/storyIcons.ts`) is now usable INLINE in notes/articles via a `:name:`
shortcode. `addIconShortcodes` in `$lib/markdownit.ts` adds an inline rule
BEFORE `emphasis` that fires only when `:([a-z0-9][a-z0-9-]*):` resolves to a
known icon via new helper `iconByShortcode` (flat concept key, then `b:` brand
prefix) — an unknown `:x:` is left as plain text, so URLs/times (`10:30`) are
never mangled. Renders `<span class="md-icon md-icon-{kind}">` with
`iconInlineSvg` (concepts stroked with `currentColor` so they tint with text;
brand logos keep their colors); `.md-icon` CSS = `1.05em` inline box. New
`IconPicker.svelte` (Concepts/Logos tabs + search, inserts the shortcode),
reused by both `MarkdownEditor`/`ArticleEditor` (each got `iconPickerOpen`,
`openIconPicker`, `insertIcon`, an Insert-icon toolbar button, the
`commit()` blur-guard extended, and the `SlashMenu` `onIcon` wire); `SlashMenu`
gained an `/icon` command. Grew the icon set ~63→82 for PM work: concepts
ticket/kanban/todo/backlog/pull-request/comment/flag/bell/calendar/bookmark/
check/tag + logos jira/confluence/trello/slack/figma/gitlab/bitbucket
(`scripts/gen-story-icons.mjs` lists updated to match; generated file stays
self-contained/offline). FormattingHelp gains a `:name:` row + an "Icons"
section. No dep/backend/migration. svelte-check 0/0, build clean. See
documentation/SPRINT44.md. — earlier:
Sprint 43 (Storyboards — a new canvas entity for TINY
diagrams: a sequence of pages, each a mini-canvas + a powered-markdown note,
flipped like slides and built to present. Clone-and-simplify of Blueprints (NOT a
shared refactor — Blueprints is the flagship): reuses the combined nodes+edges
`$effect` sync + identity caches + `$state.raw` + `ConnectionMode.Loose` +
presenter pattern, and the decorative `MapTitleNode`/`MapCommentNode` for
header/comment. New: a **pages** layer (`storyboard_pages(position, note)` — the
markdown note lives per page) and a **minimal node kit** — `box`/`icon`
(connectable, new `StoryBoxNode`/`StoryIconNode` with 4 t/r/b/l handles) +
`header`/`comment` (decorative). Migration `0024` (4 tables; nodes/edges scoped
to `page_id`); `commands/storyboards.rs` (~25 commands, get_storyboard returns
`{storyboard,pages,nodes,edges}`, 4 tests); full ipc + store slice (state holds
ALL pages, editor filters by `currentPageId`). `StoryboardsView` (index) +
`StoryboardView` (Provider wrapper) + `StoryboardEditor` (toolbar w/ 4 add
buttons + Present · canvas · per-page MarkdownEditor note · filmstrip w/ add/
delete/reorder). Present = in-place slideshow (←/→/Esc, read-only canvas). Edge
labels editable (floating input). Reached via palette + AddEntityModal +
Summary "Storyboards" section + pinned-sidebar section + `storyboard:id` IdChip/
markdown link; no ⌘-digit (all taken). Autosave per mutation. **PNG export**
shipped (crop-rectangle, reuses `composeCropPng`/`buildEdgeLayerSvg`) — the
toolbar "Export image" button; Present was dropped. **Icon nodes** use a curated
set — Lucide concept icons (tinted line SVGs) + Devicon brand logos — from
`$lib/storyIcons.ts` (generated by `scripts/gen-story-icons.mjs`; the icon field
stores a key or freeform emoji), with a Concepts/Logos picker popover. Also fixed
a pre-existing timezone-flaky test (`activity_stats` now inserts with localtime).
106 cargo tests + svelte-check + build all pass. See documentation/SPRINT43.md.
— earlier: Sprint 42) Camera check-ins — "lolcommits for todo lists":
creating a today's list snaps a ~1s webcam GIF (OPT-IN, default off). `newList`
fires `maybeCaptureCheckin` (fire-and-forget); `$lib/checkin.ts`
`captureCheckinGif` uses webview `getUserMedia` + `gifenc` (new dep) to encode
~10 mirrored 240×180 frames, saved via `save_image` → `add_checkin(path,listId)`.
Migration `0023` `checkins(id, list_id →lists ON DELETE SET NULL, path,
created_at)`; `commands/checkins.rs` (add/list/delete, delete also removes the
file; 2 tests). Gallery = a "Check-ins" tab in `ActivityView` (grid + delete +
the opt-in toggle & privacy note); store `checkins`/`capturingCheckin`; theme
`checkinsEnabled` persisted. `+page.svelte` shows a red "📸 Capturing…" pill.
`src-tauri/Info.plist` adds `NSCameraUsageDescription`. Local-only, never
uploaded. IMPORTANT: the camera capture itself is UNTESTED without a real
`pnpm tauri dev` run (WKWebView `getUserMedia` + macOS prompt). See
documentation/SPRINT42.md. — earlier:
Sprint 41) Passwords vault — a tiny encrypted site-password
keeper at ⌘8. Entry = {title, password}; titles plaintext (browsable while
locked), password encrypted. Master password → Argon2id key (crates: `argon2`,
`chacha20poly1305` XChaCha20-Poly1305, `zeroize`); key lives ONLY in
`AppState.vault_key` (`tokio::sync::Mutex<Option<[u8;32]>>`, zeroized on lock),
never crosses IPC except a plaintext password via `reveal_secret`. Master
password never stored — `vault_meta` keeps salt + a verifier blob; `secrets`
holds `password_enc` = nonce‖ct. Migration `0022`; backend `commands/secrets.rs`
(vault_status/setup/unlock/lock, list/add/update/reveal/delete_secret, +4 crypto
tests). `PasswordsView.svelte` (setup/locked/unlocked states, generator, reveal/
copy-with-20s-clipboard-clear/delete); store `vaultInitialized/vaultUnlocked/
secrets` + `touchVault` idle-lock (~5min, wired to global key/pointer listeners)
+ lock on quit (process death drops the key). TopNav icon + palette + HelpModal.
Honest scope: protects data at rest, not a live-unlocked compromised machine. See
documentation/SPRINT41.md. — earlier:
Sprint 40) Removed the Alexandria canvas — the original
single shared `map` view. Blueprints (standalone design canvases) superseded it
and is the daily driver, so it's gone: deleted `MapView`/`MapEditor`/
`MapNodeCard`/`MapCustomNode`/`AddToMapPalette`, the whole map store slice +
`*Map*` actions, the ipc map types/wrappers, `commands/map.rs` (+ handler regs +
`MapNode/MapEdge/MapState` models), and the `map` view/label/keybinding.
Migration `0021_drop_master_map.sql` DROPs `map_edges`+`map_nodes` (data
intentionally discarded). **Blueprints promoted**: now owns ⌘2 + a TopNav toolbar
icon (was ⌘8/no icon; ⌘8 now unbound). KEPT `MapTextNode`/`MapCommentNode`/
`MapTitleNode` — still used by `BlueprintEditor` — with their `app.*` store
fallbacks changed to no-ops (Blueprints always passes its own
`onCommitContent`/`onResizeEnd`). App name/bundle id unchanged. 96 cargo tests +
svelte-check + build all pass. See documentation/SPRINT40.md. — earlier:
Sprint 39) Contribution graph in Focus mode — a GitHub-style
52-week activity heatmap below the today's-list block on the aurora screensaver.
Counts a COMBINED per-day activity: todos on that day's list (by list date —
ALL tasks, not just completed; changed Sprint 44) + notes/articles/blueprints
CREATED that day (by `created_at`), archived+backlog excluded.
Backend `get_activity_stats` (`commands/search.rs`, model `ActivityDay{date,count}`)
UNION ALLs four per-day GROUP BYs and sums (test:
`activity_stats_combines_todos_and_entities`); store `activityStats` loaded in
init/refreshLists + refreshed in `enterFocus`. `FocusMode.svelte` `contrib`
(`$derived.by`) builds Sun→Sat week columns from a `date→count` map, keyed off
`todayKey`=`isoLocal(now)` (a string) so it rebuilds only at midnight, not every
clock tick. 5-level green scale (`.cg-l0…4`, `levelFor` 0/1-2/3-4/5-6/7+), today
outlined, future cells hidden, "Less→More" legend + "N contributions in the last
year" caption. Todo completions update live via refreshLists. The Home
(`Welcome.svelte`) calendar — already a GitHub-style weekly grid — now colors
PAST/today cells by the SAME combined `activityStats` count on the SAME 5-level
green scale (`levelFor`), so Home and Focus read identically; future cells keep
their planning role (clickable future-empty/future-planned), plus today ring +
month labels. Legend became a Less→More green ramp. See documentation/SPRINT39.md.
— earlier:
Sprint 38) Lettering — a ```lettering fence renders a big,
centered, uppercase display-type banner (bundled Oswald) for announcements,
distinct from headings. `renderLettering` in `$lib/markdownit.ts` joins non-empty
lines with `<br>`; optional color/gradient from the shared vocabulary tints the
text — a gradient becomes gradient text via `.md-lettering-grad`
(`background-clip:text`). `.md-lettering` = Oswald 700, centered, uppercase,
`clamp(2rem,6vw,3.4rem)`. CSS-only/synchronous. Slash command "Lettering (big
title)" + FormattingHelp row + showcase. See documentation/SPRINT38.md. — earlier:
Sprint 37) Per-cell treemap colors — each ```treemap
`Label: value` line can now carry, after the value: a color/gradient name
(recolors that square, per-cell gradients get their own `<defs>`), `highlight`/
`accent` (AUTO distinct color from `TM_AUTO_ORDER`, cycling + skipping the base
color), and/or `animated`. `renderTreemap` resolves each cell's fill via
`namedSvgFill`, collects all defs into `defs[]`, and `TMData` gained a resolved
`fill?`. Explicit name > highlight > base color. Slash snippet + FormattingHelp +
showcase updated. See documentation/SPRINT37.md. — earlier:
Sprint 36) Unified color + gradient vocabulary — one shared
palette across every customizable markdown element. `$lib/markdownit.ts` defines
`NAMED_COLORS` (red/orange/amber/green/teal/blue/violet/pink/gray/black, 600-level)
+ `NAMED_GRADIENTS` (sunset/ocean/forest/dusk/candy, matches ```cards) once, with
resolvers `isNamedFill`, `namedBackground` (CSS bg for HTML: marquee/progress) and
`namedSvgFill` (→ `{fill,def}` for SVG: chart/treemap — gradients need a
`<linearGradient>` def since SVG `fill` can't take `linear-gradient()`; unique ids
via `svgGradSeq`). Now charts (bar/line accent) and treemap and progress ALL accept
the full solid+gradient set (charts gained black+gradients); donut keeps its own
auto categorical `CHART_PALETTE`. Progress fill switched to the `background`
shorthand so its barber-pole stripes moved to a `::after` overlay. Removed
`CHART_NAMED`/`MARQUEE_COLORS`/`MARQUEE_GRADIENTS`. FormattingHelp gains a shared
"Colors & gradients" section. See documentation/SPRINT36.md. — earlier:
Sprint 35) Treemaps in markdown — a ```treemap fence
renders a single-color squarified treemap (area ∝ value), inspired by the xray
LOC treemap but simplified to one flat color. `renderTreemap` in
`$lib/markdownit.ts` uses `d3-hierarchy` (new dep: `hierarchy`/`treemap`/
`treemapSquarify`) over a fixed 1000×600 viewBox (SVG scales responsively);
Oswald labels (the bundled face) auto-fit per cell + optional value sub-label.
One `Label: value` per line; fence info options `treemap [color] [animated]`
(color reuses `MARQUEE_COLORS`, default blue; `animated` pulses all cells), and a
per-line `- animated` suffix pulses just that cell (`.md-treemap-pulse` /
`@keyframes md-tm-pulse`, reduced-motion safe). White cell text. CSS-only/
synchronous like the other fences. Slash command "Treemap" + FormattingHelp row.
See documentation/SPRINT35.md. — earlier:
Sprint 34) Interactive progress counter — a ```progress
fraction bar `n/d` renders −/+ steppers that rewrite the numerator in the
markdown source and save, exactly like task checkboxes (`toggleTaskInSource`).
New exports `stepProgressInSource(src,index,delta)` (finds the Nth integer-frac
line inside a ```progress fence, clamps 0..d, preserves label/den/trailing
color) + `countProgressStepsInSource`. Steppers render only when the fence is
rendered with `env.progressInteractive` — set by `MarkdownEditor` (notes) and
`ArticleEditor` (articles); read-only surfaces (blueprint cards, flash cards)
show a static bar. Per-render stepper index lives on `env.progressSteps`
(document-ordered); `ArticleEditor` offsets per-segment via
`countProgressStepsInSource` like it does task indices. Percent/bare bars stay
static. See documentation/SPRINT34.md. — earlier:
Sprint 33) Progress bars in markdown — a ```progress fence
renders one labeled bar per `Label: value` line; value as `4/10` (→ its %),
`60%`, or a bare `0–100`, with an optional trailing color word (reuses
`MARQUEE_COLORS`, default blue). CSS-only/synchronous like the other custom
fences: `renderProgress` in `$lib/markdownit.ts` emits a label+readout header and
a track/fill bar (fill width+color inline; track uses `color-mix(currentColor
12%)` so it's theme-safe). Chosen as the simple authored option over
auto-from-checkboxes / a stored per-note % field. Slash command "Progress bars" +
FormattingHelp row. See documentation/SPRINT33.md. — earlier:
Sprint 32) Marquee banner — a ```marquee fence renders a
right→left scrolling colored bar for flagging important notes or as a bold
divider. CSS-only (no hydration): `renderMarquee` in `$lib/markdownit.ts` emits
the text twice in a `.md-marquee-track` that animates `translateX(0→-50%)`
infinitely for a seamless loop; options (`marquee <color> <speed>`) ride in the
fence INFO STRING — not `key:value` lines — so the banner text can contain
colons. Background = solid `MARQUEE_COLORS` (600-level, white text) OR a
`MARQUEE_GRADIENTS` preset (sunset/ocean/forest/dusk/candy, shared with ```cards),
inline `style` to dodge Tailwind purge; default blue; speeds slow/normal/fast
(26/16/9s). `app.css` `.md-marquee*` has hover-pause + a reduced-motion fallback
(single centered static label). Options are documented in-app in FormattingHelp's
"Marquee banner" section; slash command "Marquee banner". See
documentation/SPRINT32.md. — earlier:
Sprint 31) Sidebar app-brand mark — retired the stale
Lists/Todos/Streak counters from the sidebar footer (the app outgrew daily-todo
metrics; `getStats` still powers Home) and replaced them with an editable
**app-brand label**: Oswald, uppercase, `0.14em` tracking, default "Alert Media
Engineering Toolbox". A hover pencil does inline edit (Enter/blur save, Esc
cancel, blank resets). Lives in the theme store (`brandLabel` / `setBrandLabel`
/ `DEFAULT_BRAND`, persisted to `localStorage` `brandLabel`), so it sits next to
`sidebarTint`; the label inherits the footer color so it adapts to every tint +
dark mode. Oswald is **bundled offline** (no CDN in the Tauri webview):
`static/fonts/oswald-{latin,latin-ext}.woff2` (variable woff2 subsets, one file
per subset covers all weights) + two `@font-face` blocks at the top of
`app.css`; `adapter-static` copies them to `build/fonts/`. Shortcuts + build
popover unchanged. See documentation/SPRINT31.md. — earlier:
Sprint 30) Charts in markdown — a ```chart fence renders an
inline bar / donut / line chart, rendered as SVG synchronously in
`$lib/markdownit.ts`'s fence rule (like ```cards, unlike async ```mermaid — so
it works in blueprint cards too, no dependency, CSP-safe). DSL mirrors ```cards:
`type: bar|donut|line` + `title:` + `color:` config lines, then `Label: number`
data lines (order preserved; negatives/non-numbers dropped). `renderChart` →
`renderBarChart`/`renderDonutChart`/`renderLineChart`. Series colors are a fixed
mid-tone palette baked into the SVG; structural ink (axis text, gridlines, donut
center total) uses `currentColor` so it follows the theme. Styles under
`.md-chart` in `app.css`. Slash menu gains "Bar chart"/"Donut chart"; a "Charts"
section added to `FormattingHelp`. See documentation/SPRINT30.md. — earlier:
Sprint 29) Backlog — a single durable list for unscheduled
tasks, separate from the day-to-day carry-over flow. Stored as a sentinel list
`is_backlog = 1` (migration `0020`, additive `ALTER`; `date = ''`, get-or-created
by `lists::backlog`) so it reuses all todo plumbing; excluded from the daily
surfaces (`list_all`/`stats`/`daily_stats` filter `is_backlog = 0`). New
`move_todo(id, targetListId)` re-parents a todo (append to target order),
powering manual "Send to backlog" (daily → backlog) and "Pull to today" (backlog
→ today's list, created if needed — explicit action, cf. Sprint 11) per-row
actions in `TodoRow`. Sidebar gets a "Backlog" entry with a pending-count badge
(`backlogPending`); `ListView` branches on `app.selected.isBacklog` (title
"Backlog", no date/pin/delete/export chrome); command palette adds "Backlog".
No auto-sweep, one global backlog, not pinnable/archivable. See
documentation/SPRINT29.md. — earlier: Sprint 28) Focus mode — a full-screen aurora "screensaver"
overlay showing today's list for distraction-free task focus. Entered via a
sparkles icon in `TopNav` or the command palette's "Enter Focus mode"; exited
with the ✕ or Esc. `FocusMode.svelte` renders the Sprint 23 aurora backdrop
(colors from `theme.sidebarAurora`, else a default palette), a live clock +
long date, and today's todos as big checkable rows (completed dim + strike);
empty state offers "Create today's list". It's an overlay driven by
`app.focusMode`, NOT a `view` — so it never disturbs the nav stack or the open
entity. Focus keeps its own todo state (`focusTodos`/`focusListId`/
`focusListTitle` + `enterFocus`/`exitFocus`/`toggleFocusTodo`/`createFocusToday`
in the store) loaded via `listTodos`; toggling syncs `this.todos` only when the
same list is open behind it, then `refreshLists()`. Today's-list only, no
auto-create (Sprint 11), no new global shortcut (webview reserves too many). See
documentation/SPRINT28.md. — earlier: Sprint 27) Blueprint diagram importer — an "Import" button
on the blueprint canvas opens a textarea for a mermaid-like DSL: `Name: desc`
lines become cards, `A -> B` lines become edges (undefined names auto-create).
`parseImport` + `layoutImport` (longest-path/Kahn's top-down layering) +
`doImport` in `BlueprintEditor.svelte` create real connected cards via the
existing store actions (no backend change); placed right of existing content,
bottom→top edge handles, viewport pans to the result. See
documentation/SPRINT27.md. — earlier: Sprint 26) Slash command menu — type `/` at line-start or
after a space in the note/article editors to open a Notion-style command popup
AT THE CARET (Heading/list/checklist/quote/callout/code/table/diagram/cards/
divider/link/image); filter by typing, ↑↓/Enter/Tab/Esc. `SlashMenu.svelte`
(shared) attaches capture-phase key handlers to the textarea and positions via
a mirror-div caret measurement; snippet commands replace the `/query`, Link/
Image call the editors' pickers. Editor toolbars slimmed to icon-only +
tooltips. See documentation/SPRINT26.md. Also (Sprint 25) added card `filled:
true` (bold darker fill) + `color: black`, and fixed the card hover picking up
the link-chip purple. — earlier: Sprint 25) Link cards — a ```cards markdown fence renders
a responsive grid of clickable tiles (title/desc/link/color/icon per card,
separated by `---`) for building dashboard notes/articles. `renderCards` in
`$lib/markdownit.ts` emits the grid HTML directly; card `<a>` links reuse the
editors' existing `onPreviewClick` anchor handling (entity nav + external open);
styled in `app.css` under `.md-cards` (solid hue tints via a `--h` var +
gradient presets sunset/ocean/forest/dusk/candy). "Insert cards" button in both
editors. See documentation/SPRINT25.md. Also markdown polish: bigger h1, rounded
tables + tinted header + row hover, better code blocks, aligned task checkboxes;
wider note/article columns (max-w-4xl); task detail is now a modal reusing the
notes MarkdownEditor. — earlier in this session, Sprint 24:) Blueprints as a presentation & documentation
surface — all four items scoped to the Blueprints section. **Presenter view**:
a toolbar toggle (Esc to exit) that hides authoring chrome, swaps the backdrop
to a theme-aware stage gradient, and spotlights whatever node the cursor is
over (all others dim) — pure CSS via `.bp-presenting` + `:has(...:hover)`, no
node rebuilds, `drop-shadow` not `transform:scale()` because xyflow owns the
node's inline translate. **Icon-only toolbar**: every cluster button is now an
icon with its name in a `title` tooltip. **Copy PNG to clipboard**:
`composeCropPng` returns the Blob; the crop bar offers Save PNG + Copy
(`navigator.clipboard.write`). **Paste images** (Approach A — image on a card,
not a new node kind): migration `0018` adds nullable `blueprint_nodes.image_url`
(additive ALTER, no CHECK rebuild); `add_image_card`/`add_blueprint_image_card`;
`BlueprintCardNode` renders the image with an optional caption; a window-level
`onpaste` in `BlueprintEditor` saves clipboard images via `save_image` and drops
a card at the cursor. IMPORTANT export subtlety: asset-protocol images can taint
html-to-image's capture — `inlineImagesForCapture` swaps each `<img>` src for a
`data:` URI during capture and restores after. Two things need a live test:
image clipboard copy, and PNG export/copy of a blueprint containing a pasted
image. Plus a UX pass: Home counters are now Articles/Notes/Blueprints (Lists &
Tasks dropped — they live in the calendar) with quick-nav cards to Summary &
Visualization; the **sidebar shows pinned Blueprints**; **Summary** swapped its 8
overflowing tabs for a left section rail + an "All" union view, collapsing the
seven duplicated row blocks into one normalized `Row` + `{#snippet entityRow}`;
and more sidebar background tints. See documentation/SPRINT24.md.)

Sprint 23 (Markdown upgrades. **Task checkboxes**:
`- [ ] / - [x]` render as clickable checkboxes that persist by flipping the
marker in the source (`addTaskLists` + `toggleTaskInSource` in
`$lib/markdownit.ts` — renderer index and source-scan index must stay in
sync; ArticleEditor offsets per-segment indices via `countTasksInSource` +
`data-seg` wrappers); done tasks strike through. **Syntax highlighting**:
highlight.js core with hand-registered languages (Elixir first), GitHub-ish
`.hljs-*` palette in `app.css`; also fixed the per-line background strips on
fenced code — the inline-code pill CSS now scopes to `:not(pre) > code` in
MarkdownEditor/ArticleEditor/EmbedBlock. **Note outline**: MarkdownEditor's
`outline` prop (passed by NoteView) shows a floating right-side h1–h3
navigator on xl screens. **Link chips**: rendered markdown links display as
button-like chips in all markdown surfaces. **Aurora sidebar tints**: three
animated gradient surfaces (aurora/nebula/ember) — `Tint.aurora` colors +
`Tint.base`, blurred drifting blobs + feTurbulence noise rendered by
Sidebar.svelte behind an `isolate`/`z-index:-1` layer; reduced-motion safe.
See documentation/SPRINT23.md.)

Sprint 22 (Blueprints — a new ⌘8 section of standalone
design canvases for planning software. Migration `0017` (`blueprints` +
`blueprint_nodes` + `blueprint_edges`), `commands/blueprints.rs`, full
ipc/store wiring, views `blueprints` (index modeled on the feedback boards
list) + `blueprint` (editor). `BlueprintEditor.svelte` copies MapEditor's
architecture (single $effect syncing nodes+edges together, identity caches,
$state.raw) — same subtleties apply. `BlueprintCardNode.svelte` is an HTML
card (title-dominant, markdown description via the shared markdownit factory
— mermaid fences deliberately not hydrated inside cards, color from
`$lib/cardColors.ts`, NodeResizer, four handles `t|r|b|l` with
ConnectionMode.Loose; edges persist their handle ids). The Map* decorative
nodes (text/comment/title) are shared: they now accept optional
`onCommitContent`/`onResizeEnd` callbacks in node `data`, defaulting to the
map store actions. Edge labels are editable here (click an edge → floating
input). PNG export: "Export PNG" enters a crop-rectangle mode (pre-fit to
`getNodesBounds`, pointer-drag move/resize), rasterizes the region with
`html-to-image` (new dep) via `getViewportForBounds` at 2× on a flat
theme-aware background, saves through the native dialog +
`save_binary_file`. Follow-ups in the same sprint: no TopNav icon (list
lives in a Summary "Blueprints" tab, creation in AddEntityModal; ⌘8 + the
palette still open the index view); edges are animated dashed lines; cards
auto-size to their text (no default node height — a persisted NodeResizer
height still wins) with centered titles; inline code in descriptions
(`` `like this` ``) renders as an accent-tinted badge pill (CSS-only,
`:not(pre) > code`); the exported PNG is composed on a canvas — flat
theme-aware background + phase-aligned dot grid + 48px margin + rounded
hairline border ("card style") + the blueprint title in the bottom-left
corner. IMPORTANT export subtlety: xyflow edges are zero-sized
`overflow: visible` SVGs that WKWebView clips inside html-to-image's
foreignObject — so `BlueprintEditor` excludes `.svelte-flow__edges` from
the DOM capture and rebuilds the edge layer itself (`buildEdgeLayerSvg`
serializes the edge paths' `d` into one viewBox'd SVG with an arrow
marker, composited under the nodes). `blueprint:id` is a first-class entity
link (MarkdownEditor/ArticleEditor regex + navigate, EntityLinkPicker,
IdChip — shown in Summary, the blueprints index, and the editor's top-left
chip). TopNav renders Home + Summary as always-tinted icon "hub" buttons
ahead of a divider (PRIMARY array in `TopNav.svelte`). Deferred: sidebar
pinned section, an Alexandria `blueprint` map kind.)

Sprint 21 (UX hardening — no new features. Added a global
**command palette** (⌘K, `CommandPalette.svelte`) that searches every entity +
lists all destinations & quick actions (client-side, no backend); a visible
"Search ⌘K" pill + the current **section label** in the toolbar; sidebar search
relabeled "Search todos". Refreshed `HelpModal` (⌘K/⌘7/⌘[/⌘\ + Tab + per-section
descriptions) and added `FormattingHelp.svelte` (in-app markdown reference) via an
"Aa" button in the editors. A dismissible first-run "Start here" card on Home; a
Map/Alexandria empty-state hint. Esc now closes the feedback/flashcard panels.
Frontend-only; `svelte-check`/`build` clean.)

Sprint 20 (Flash Deck — a single global deck of flashcards
as a first-class entity. Migration `0016` (`flashcards` + `flashcard_categories`),
`commands/flashcards.rs` (cards + category CRUD, reorder, nullable-field setters),
full ipc/store wiring. New view `flashdeck` (⌘7, `TopNav` icon). UI: a responsive
deck grid with pointer-DnD reorder, generative geometric card art
(`$lib/cardArt.ts`, seeded SVG — chosen over a fluid "Refik Anadol" variant the
user rejected), `FlashCard` front + `FlashCardPanel` (front↔back flip + edit:
title/body via `MarkdownEditor`, category/color/emoji pickers, image upload) +
`FlashStudyView` (shuffle/flip/next-prev study mode). Categories are color/icon
"suits". Surfaced in AddEntityModal, a Summary "Cards" tab, sidebar pinned
section, and `{{flashcard:id}}` embeds / `flashcard:id` links. Canvas node
deferred. `#tag` badges work in card titles.)

Sprint 19 (Feedback boards leveled up + markdown polish +
sidebar collapse. Boards: per-board custom columns (`feedback_columns` table,
migration 0013; `create_board` seeds 4 defaults; rename/add/delete in
`FeedbackBoardView`), card color (`color` col + `$lib/cardColors.ts` picker in
`FeedbackCardPanel`), `#tag` badges in board/card titles (`$lib/badges.ts` +
`TagBadges.svelte`), quick-add (Enter adds & keeps the input open),
`user-select:none` while dragging, board `pinned` → sidebar + Summary "Boards"
tab + Alexandria canvas node (`feedback_board` map kind, migration 0014).
Markdown (`$lib/markdownit.ts` + global CSS in `app.css`): `{color|text}`,
`==highlight==`, `> [!NOTE|TIP|WARNING|COMMENT]` callouts, distinct table
headers, nested-list bullets, Tab inserts spaces (no blur), `lheading` disabled
(no stray heading from `----`), word counter, broken entity links flash instead
of erroring. Sidebar: collapse toggle (⌘\) for full-width reading. Lists: one
active list per day — `create` is idempotent per date + partial unique index
(migration 0015), fixing the stale/duplicate today's-list bug.

Sprint 18 (UI follow-ups — the top nav menu moved from a
floating overlay into a reserved 44px toolbar **row** at the top of the main
column (`+page.svelte`: main column = toolbar row + scroll area), so it no
longer overlaps a view's own top-right controls; full-bleed views switched
`h-screen`→`h-full` and padded views `min-h-screen`→`min-h-full` to fit the
reduced scroll area. Added a "Last updated <timestamp>" footer to note/article/
workflow views (`$lib/format.ts` `formatTimestamp`, `mt-auto` pins it to the
bottom). Added dark sidebar tints (ink/graphite/navy/forest/wine) — when a
`dark` tint is active the sidebar adds a local `dark` class so its content flips
to light text regardless of app theme (`theme.isSidebarDark`)).

Sprint 17 (UI polish — moved the six nav destinations out
of the sidebar into a floating top-right icon bar (`TopNav.svelte`) to free
sidebar space; added a back button + `app.navStack` history (⌘[); made the
sidebar footer stick to the bottom and the app shell fixed-height
(`h-screen overflow-hidden`, only the main column scrolls) so the footer no
longer drifts on long notes; clickable build-hash → commit message/date popover
(vite injects `__APP_COMMIT_MESSAGE__`/`__APP_COMMIT_DATE__`); customizable
sidebar tint via CSS vars `--sidebar-bg`/`--sidebar-border` set by the theme
store (`SIDEBAR_TINTS`, persisted, light/dark-aware); fixed mermaid leaving
orphan "Syntax error in text" nodes stacked at the page bottom — `renderMermaid`
now removes them in a finally).

Sprint 16 (Remove the Diagram entity — Sprint 15's inline
```` ```mermaid ```` fences made the standalone Sprint 14 entity redundant, so
it's gone: deleted `commands/diagrams.rs`, `DiagramView`/`DiagramEditor`, the
`Diagram`/`DiagramSummary` models + ipc types + store actions, the `diagram`
view, the Summary tab, the AddEntityModal option, sidebar pinned section, the
`{{diagram:id}}` embed + `diagram:id` link plumbing, and the EntityLinkPicker
option. DB: kept `0011_diagrams.sql`, added `0012_drop_diagrams.sql`
(`DROP TABLE`) — additive so existing DBs don't fail sqlx's applied-migration
checksum. No data migration (the DB had zero diagrams/embeds). Inline mermaid
fences stay; the editors' "Insert diagram" button now inserts a fence).

Sprint 15 (Inline ```mermaid fences — write a fenced `mermaid` block anywhere
you write markdown (notes, articles) and it renders inline, GitHub-style.
Client-only: a shared `$lib/markdownit.ts` factory adds a markdown-it `fence`
rule that emits a `.mermaid-block` placeholder, then `hydrateMermaidBlocks`
swaps in the SVG via a MutationObserver — `{@html}` re-renders on edit/commit
wipe manual injection, so a one-shot effect isn't enough. Source+theme cache +
last-good-render on syntax errors).

Sprint 14 (Diagrams — Mermaid diagrams-as-code as a first-class entity.
REMOVED in Sprint 16; see above. Was: `diagrams` table + `commands/diagrams.rs`,
`DiagramView`/`DiagramEditor`, PNG export, `{{diagram:id}}` embeds.)

Sprint 13 (Alexandria rename — identifier kept; planning calendar with
clickable future days; markdown editor polish — explicit Edit button,
auto-growing textarea via `$lib/autosize`, table insert, entity links).
