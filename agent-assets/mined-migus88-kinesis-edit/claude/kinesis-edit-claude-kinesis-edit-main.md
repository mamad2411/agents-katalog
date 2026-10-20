# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A modern, cross-platform replacement for the Kinesis SmartSet keyboard-configuration app (the legacy app is written in Pascal and unsupported). Target stack: **C# with Avalonia UI**. Primary platform is **macOS** — develop Mac-first — but Windows and Linux must also work.

**Current status.** The UI-free domain layer `KinesisEdit.Core` is essentially complete — device data, the runtime keyboard/macro model, the v-Drive services, and parsers/serializers for every in-scope file format (the one gap is Advantage2's position-based profile naming, issue #37). The app on top is in active development: **two boards have real editors** — the Freestyle Edge RGB (remaps, macros, lighting, settings) and the Savant Elite2 (its seven pedals) — and every other device opens a placeholder until its board picture is authored (issues #39–#42), which also gates the TKO edge-LED tab (#40) and the Advantage 360 indicator editor (#41). Diagnostics and Troubleshoot are #46.

**What exists module by module, and which doc covers it, is [`docs/app/README.md`](docs/app/README.md) — start there, not here.** This file deliberately does not restate it: a status narrative maintained in prose is the one thing every feature branch has to edit, so it collided constantly and went stale between collisions.

The solution lives at `src/KinesisEdit.sln` (Avalonia app `KinesisEdit`, UI-free domain library `KinesisEdit.Core`, xUnit tests `KinesisEdit.Core.Tests` for Core and `KinesisEdit.Tests` for the app layer); see `docs/app/solution-structure.md` for the layout and dependency rules. From the repo root:

- Build: `dotnet build src/KinesisEdit.sln`
- Test: `dotnet test src/KinesisEdit.sln`
- Run the app: `dotnet run --project src/KinesisEdit`

Implementation is planned and tracked in GitHub issues — see the epic ([#1](https://github.com/migus88/kinesis-edit/issues/1)) and its ordered sub-issues. There is no in-repo planning document.

**A UI redesign is in flight.** Everything described above was built to mimic the legacy app; a design handoff now supersedes its look and, in places, its behavior. `docs/design/` holds that handoff and is the **authoritative design reference** — read `docs/design/README.md` before touching any view, style or user-facing string. The redesign has its own epic and phased child issues in GitHub; a design decision there beats the current implementation unless the issue says otherwise.

Its foundation has landed: the **design system** — colour/shape/type/motion tokens in `src/KinesisEdit/Themes/`, the shared style layer in `src/KinesisEdit/Styles/`, embedded IBM Plex Sans/Mono, the reduce-motion switch, a Fluent control-alias layer that puts the base controls on the palette, the icon and device-art system, and the control-theme layer in `src/KinesisEdit/Themes/ControlThemes/` — plus the **headless UI test harness** that guards it. The screens are being rebuilt on it issue by issue; what each rebuilt screen now does is recorded in that screen's own doc under `docs/app/`, not here.

**Read `docs/app/design-system.md` before writing any view or style.** It is the redesign's foundation spelled out in the app — the token registry, the type scale, geometry, the motion budget, the icon catalog, the `ControlTheme` registry and every deliberate deviation from the handoff with its reason — and it also documents **how to test UI work in this repo** (headless rendering, frame capture, what each suite guards). Parts of the UI remain in the pre-redesign layout; that doc's **Known gaps** section lists which.

**Two rules from that layer bind every view and style you write:** name a class (`Classes="primaryAction"`), and let a one-setter bridge in `Styles/` point it at a `ControlTheme`; and **never name a template part outside `Themes/ControlThemes/`** — a `/template/` selector anywhere else is a bug and fails a test.

## Repository layout

- `specs/` — Standalone specification of the legacy SmartSet apps, devices, and on-device file formats. This is the **authoritative domain reference** for the rebuild; do not modify it casually. Start with `specs/README.md` for the reading order and mental model.
- `docs/app/` — Agent-first documentation of the new app's modules (see "Documentation rules" below). **[`docs/app/README.md`](docs/app/README.md) is its index**: which doc answers which question, plus the module inventory for Core and the app layer. Go there rather than listing the modules here.
- `docs/design/` — The design handoff for the UI redesign, and the **authoritative design reference** for anything visual or user-facing. `README.md` (index, reading order, the mockup id map, and the design laws that cut across every screen), `handoff.md` (the handoff verbatim: design tokens, per-screen specs, Avalonia implementation notes), `mockups.md` (agent-first distillation of all 20 mockups — read this instead of the HTML), `KinesisEdit.dc.html` + `support.js` (the mockup canvas, for pixel-level reference in a browser). Do not modify it casually; it is a delivered artifact.
- `docs/guides/` — Coding conventions and other guides.
- `src/` — Source code of the new app.

## Domain model (the big picture)

Read `specs/README.md` first — but the core mental model is:

A SmartSet app is **a file editor with a keyboard-shaped UI**. Each programmable Kinesis device mounts a small FAT volume (the "v-Drive") containing plain-text config files (`layouts/layoutN.txt`, `lighting/ledN.txt`, settings); the keyboard's **firmware** parses those files — there is **no USB/HID configuration protocol**. The app therefore consists of:

1. Drive discovery (find the mounted v-Drive by volume label + marker files). Implemented in `KinesisEdit.Core.VDrive` (see `docs/app/vdrive.md`).
2. Parsers/serializers for the text file formats. The `lighting/ledN.txt` engine (RGB, TKO, Advantage360) is implemented in `KinesisEdit.Core.Lighting` (see `docs/app/lighting.md`), the settings files (spec 08) in `KinesisEdit.Core.Settings` (see `docs/app/settings.md`), the layout/macro files (specs 04, 06) in `KinesisEdit.Core.Layouts` (see `docs/app/layout-files.md`), and the Savant Elite2 pedal file `active/pedals.txt` (spec 12) in `KinesisEdit.Core.SavantElite` (see `docs/app/savant-elite.md`).
3. An in-memory model per keyboard (layers → keys → remaps/macros), implemented in `KinesisEdit.Core`: the static foundation — device catalog, key-token registry, layer geometries (see `docs/app/domain-data.md`) — plus the editable runtime model built on it, `KeyboardLayout`/`KeyboardLayer`/`KeyboardKey`/`Macro` (see `docs/app/keyboard-model.md`). Device limits are reported by `Validate()`, never enforced.
4. Keystroke capture feeding that editing: real keypresses with left/right modifiers distinguished, swallowed while recording a remap or macro. Implemented in `KinesisEdit.Core.Input` (see `docs/app/keystroke-capture.md`); the keyboard editor owns the single subscription and routes each keystroke to exactly one consumer — an **armed key-inspector panel** (which is where a macro is recorded now), an open feature panel, or a listening key.
5. A per-device visual keyboard UI for editing that model. The app shell that hosts it — window, device dashboard, the Settings and Help screens the other two nav pills go to, device detection (manual — nothing polls), notifications, the per-user preference store behind the theme/motion pickers and the window's remembered geometry (see `docs/app/host-preferences.md`), and the `IShellChrome` hand-off that lets an editor draw the window's one 46 px bar itself — is implemented in `KinesisEdit` (see `docs/app/app-shell.md`); the keyboard editor on top of it — the visual-geometry layer in `KinesisEdit.Core.Geometry.Visual`, one device-agnostic keyboard control, the editor shell's toolbar/tab bar/Demo Mode bar, the click-then-press remap workflow, the lighting tab and the capability-driven settings panel — is implemented for the **Freestyle Edge RGB** (see `docs/app/keyboard-editor.md`), together with the non-modal **key inspector rail** that replaced two of spec 11's dialogs, and the three that are still modal plus layout/led import hosted over it (see `docs/app/feature-dialogs.md`, backed by `KinesisEdit.Core.Transfer` plus `TapAndHoldPrecheck`/`MacroDelayTokens`/`KeySearchCatalog` in Core), and the **Savant Elite2** has its own pedal editor (see `docs/app/savant-elite.md`). Other devices need only their board picture authored (issues #39–#42), which also unblocks the TKO edge-LED tab (#40) and the Advantage360 indicator editor (#41) with its Multimodifier and Select Macro dialogs; diagnostics/troubleshoot are #46.
6. Save/sync/eject handling so the firmware reloads the files. The file I/O and eject services are implemented in `KinesisEdit.Core.VDrive` (see `docs/app/vdrive.md`); the save orchestration on top — load/edit/save/**import**/eject for one numbered profile, tying the layout/lighting/settings engines and v-Drive I/O together — is implemented in `KinesisEdit.Core.Profiles` for the numbered-profile devices (FS Edge/Pro, Edge RGB, TKO, Advantage360; Advantage2's position-based naming is issue #37) — see `docs/app/profiles.md`. The Savant Elite2 is outside that orchestration: it has one live file and no profiles, and saves through `KinesisEdit.Core.SavantElite` with no eject (see `docs/app/savant-elite.md`).

Facts that shape the architecture (details in `specs/README.md` and the numbered docs):

- **Three config-file dialects**, one per device generation — Legacy (Advantage2, SE2 pedal), Gen1 (Freestyle Edge/Pro, Edge RGB, TKO), Gen2 (Advantage360). Each needs its own parser/serializer; the key-token tables in spec 05 plus the grammars in specs 04 and 06 are the interoperability-critical heart of the system.
- **Parsing is case-insensitive; saving regenerates the whole file.** Unparseable lines are collected and shown to the user, not silently dropped.
- **Read tolerantly, write the current dialect** — devices in the field contain files written by older firmware/app versions.
- **Feature availability is firmware-gated** by comparing device version files against hard-coded minimums (spec 09 has the gate table).

## Custom commands

- `/feature <issue-number | issue-url | description>` — drives a feature end to end: fetches `origin`, resolves or creates the GitHub issue, creates an isolated git worktree under `.claude/worktrees/` branched from `origin/main` (the shared checkout is never touched, so multiple sessions can work concurrently), **then researches and asks clarifying questions inside that worktree** — the shared checkout is routinely several merges stale, so research against it studies a tree that no longer exists — proposes a split when the spec is too large for one reviewable PR, records the spec on the issue, implements via subagents (Workflow orchestration with adversarial review when ultracode is enabled), re-syncs with `origin/main`, verifies the doc and test-coverage updates, checks the rendered screens for UI work, runs the unit tests the change can actually affect — the whole suite whenever the app layer moved, and all of them must pass before a PR is opened — and opens a PR. When the user reports the PR merged, the worktree and branch are removed. Defined in `.claude/commands/feature.md`.
- `/clean-worktree [all]` — removes finished worktrees: by default only those whose branch is merged into `origin/main` and that have no uncommitted changes; `all` force-removes every worktree after user confirmation. Defined in `.claude/commands/clean-worktree.md`.

## Testing rules (important)

Everything is covered by unit tests. Concretely:

- Every feature creates unit tests for the code it adds and maintains the tests of the code it touches. Tests are part of the change, not a follow-up.
- The full unit-test suite must pass (`dotnet test` once the solution exists) before a pull request is opened. A feature with failing or missing tests is incomplete and must not reach the PR stage. **One exception, and it is a narrow one:** when `git diff origin/main -- src/ global.json .editorconfig` is empty, the branch compiles to a tree byte-identical to `origin/main` — which CI has already proved green — so the suite cannot distinguish the two and has nothing to catch. Run that command rather than reasoning about the diff: merging `origin/main` into a docs-only branch adds source and tests to it, yet adds nothing to verify, because they arrive from the green tree. Note the skip and its reason in the PR body; CI still runs on the PR regardless.
- CI runs the unit-test suite on every pull request targeting `main`; a red suite blocks the merge (workflow scoped in issue #3).
- **UI is testable too, and must be tested.** `KinesisEdit.Tests` runs a headless Avalonia harness (`Avalonia.Headless.XUnit` + `Avalonia.Skia`) that boots the real `App` and renders real pixels with **no display attached** — `dotnet test` covers views, styles and tokens like anything else. Use `[AvaloniaFact]`/`[AvaloniaTheory]`, not `[Fact]`/`[Theory]`. See `docs/app/design-system.md` § "Testing UI work in this repo" for the harness, the ad-hoc frame-capture technique and what each suite guards. **Do not add golden-image comparisons** — that is a deliberate refusal, documented there.
- **A green suite is not evidence the screen is right.** A test asserts what is true of the control you wrote; a frame shows what is true of the screen the user gets. During #86 a hatched LED strip landed on every key cap of the Keys tab with ~1700 tests passing — every assertion about the cap was correct, and the mistake was visible only on the board. Nothing but a frame caught it. So: **any change that alters what a screen looks like is verified by capturing that screen offscreen, in both theme variants, and looking at the frame** — not only by rendering the control in a harness. The capture harness is throwaway; delete it before committing.

## Documentation rules (important)

Documentation here is **agent-first**: the aim is that AI agents read `docs/app/` instead of source code to understand how a domain works, dipping into source only for particulars. Therefore:

- Every developed module must have a doc in `docs/app/`. Keep it token-efficient: sufficient for an agent to understand the domain, not a prose-heavy tutorial.
- **A feature's behavior is documented in its module's doc — and only there.** When implementing a feature, maintain the relevant `docs/app/` doc as part of the change. Touch this CLAUDE.md only for things that are genuinely repo-wide: a **new module** (one row in `docs/app/README.md`, and here only if the mental model changed), a changed build/test command, a new custom command, or a new rule that binds every feature.
- **Do not describe what a feature does in CLAUDE.md or `README.md`.** Both files used to carry a running prose narrative of everything the app could do. Every feature branch had to append a clause to the same paragraph, so they conflicted on every concurrent PR, cost a merge resolution each time, and went stale in between — while duplicating what the module's own doc already said better. A change that "needs" a sentence there almost always needs it in `docs/app/<module>.md` instead. `README.md` describes the project to a newcomer, not the changelog; git history and the GitHub issues are the changelog.
- **A new module means a new row in [`docs/app/README.md`](docs/app/README.md)** — both its routing entry and its inventory entry. That file is the index agents route through; a doc missing from it is a doc nobody finds. Keep it a router: it must not acquire descriptions of behavior, or it becomes the paragraph it replaced.
- `docs/design/` is a delivered artifact, not a maintained module doc — read it, don't rewrite it. Record what the app actually does in `docs/app/`, including any deliberate deviation from the design and why.

## Design rules (important)

Anything visual or user-facing is governed by `docs/design/` — see `docs/design/README.md` for the reading order and the laws that cut across every screen. In short: never hardcode a color in a view (every color is a named token defined for both themes); mono type is reserved for values that exist verbatim in a config file; advisories are amber and never block; features a device lacks are not rendered at all rather than disabled; nothing ejects implicitly; and the motion budget is fixed and small.

**`docs/app/design-system.md` is how those laws are actually spelled in the app** — the token registry (every role, both themes), the type-scale classes, the geometry resources, the four-status vocabulary, the motion budget and its reduce-motion aliases, the Fluent control-alias layer, the icon and device-art catalog, the control-theme registry, and every deliberate deviation from the handoff with its reason. Read `docs/design/` for *what* the design is and `docs/app/design-system.md` for *which key to name*. A hex literal anywhere outside `src/KinesisEdit/Themes/` is a bug and fails a test — and inside `Themes/`, the three geometry dictionaries carry no colour either. A `/template/` selector outside `src/KinesisEdit/Themes/ControlThemes/` is a bug and fails a test too: paint a control through its `ControlTheme`, never by reaching into somebody else's template.

## Code style

Follow `docs/guides/Coding Conventions.md`. Non-negotiables:

- Clean code, SOLID principles. No god classes — classes with thousands of lines are explicitly unwanted.
- PascalCase for types/methods/properties; camelCase for locals/parameters; `_camelCase` for private fields. No public fields — expose state through properties.
- Allman braces; always use braces, never single-line statements.
- Member ordering within a file: constants → static members → properties → events → fields → constructors → public methods → private methods → `Dispose` → nested types.
