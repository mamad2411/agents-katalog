# AGENTS.md — Rotaris Desktop UI

These instructions apply to everything under `apps/rotaris/`. Repo-wide rules,
naming, ReqToCode, and commands live in the [root AGENTS.md](../../AGENTS.md) and
are not repeated here.

## Product scope

The desktop app is the primary user interface (see root AGENTS.md). Treat its UX
work as higher priority than TUI polish unless the user explicitly changes that.

- Keep PySide6 as the desktop host.
- Preserve the seven primary views: Overview, Workspace, Mission, Requirements, Git, Library, and
  Settings. Requirements (SWR-3301) sits between Mission and Git and shows the requirement board;
  it reads the engine's board projection and never derives a verdict of its own (SWR-3311).
- Target technical teams on Linux and Windows.
- Support a minimum window size of `1000×680` without clipping, overlap, or inaccessible actions.
- Apply WCAG 2.2 AA principles where they map to Qt desktop software.
- Design for mouse and desktop controls first. Keyboard shortcuts supplement visible controls;
  they do not replace them.
- Do not edit `src/rotaris_core/tui/` for Rotaris UX work. Shared backend changes are allowed only
  when Rotaris needs a real integration seam and the change does not amount to TUI polish.

## Architecture and ownership

- `src/rotaris/models/state.py`: framework-free UI data models.
- `src/rotaris/models/store.py`: observable UI state and mutation API. Views must not silently
  mutate store fields without emitting the corresponding signal.
- `src/rotaris/views/`: complete screens and cross-screen workflows.
- `src/rotaris/views/main_window.py`: application-level navigation, confirmations, notices, and
  service wiring. Keep leaf-widget behavior out of this file.
- `src/rotaris/widgets/`: reusable Qt primitives. Reuse these before adding one-off controls.
- `src/rotaris/theme/`: design tokens, the themes that fill them in, and the global QSS built
  from whichever is active (SWR-3700). Do not hard-code colors, radii, spacing or font sizes in
  views. Read a value with `from rotaris.theme import tokens` **inside** the method that paints
  or restyles — never in a class body, a module constant or a default argument, because those
  run at import, before the user has chosen a theme (SWR-3706). A widget that holds presentation
  itself (an inline stylesheet, a `QFont`, a colour cached for `paintEvent`) mixes in
  `rotaris.theme.manager.Themed` and implements `apply_theme`; a widget styled only by the
  global stylesheet needs nothing. Adding a theme is one file under `theme/palettes/`.
  The design system this implements is vendored at `docs/reference/rotaris-design-system/`.
- `src/rotaris/services/`: backend adapters and atomic desktop persistence.
- `tests/`: pytest-qt coverage for behavior, accessibility state, responsiveness, and backend
  wiring.

Use Qt signals for view-to-host intent and store signals for state-to-view updates. Keep backend
objects out of view code where a service or plain state model can provide the same boundary.

## UX standards

### Workflow clarity

Every workflow must make these states explicit when applicable:

1. Ready or first-run setup.
2. In progress.
3. Success.
4. Empty result.
5. Recoverable error with a concrete next action.
6. Unrecoverable error with copyable technical details.

Validate prerequisites before starting work. Provider, model, workspace, branch, path, and session
errors should be caught before an expensive operation where possible. Never fail silently.

Use persistent inline feedback for failures or completion states that matter after a toast expires.
Transient toasts are suitable only for low-risk acknowledgement. Preserve user input when an
operation fails.

### Actions and destructive changes

- Give each surface one clear primary action.
- Use precise action labels such as `Create worktree`, `Continue run`, or `Clear transcript`.
  Avoid vague labels such as `OK` when a specific verb fits.
- Explain why an unavailable action is disabled. Prefer nearby text or a tooltip over unexplained
  disabled controls.
- Confirm destructive or broad-impact actions and state exactly what will be affected.
- Offer undo when it is reliable and cheaper than confirmation.
- Protect unsaved settings with Save, Discard, and Cancel choices.
- Explicitly confirm permission-expanding settings such as access outside the workspace.

### Run and session workflows

- Normalize backend lifecycle values through `RunUiState`; do not render raw aliases directly.
- Keep the composer locked while a run is actively starting, running, pausing, or cancelling.
- Distinguish starting a run from continuing a completed or paused session.
- Show progress for pause, cancel, compression, refresh, and authentication operations.
- Cancellation confirmation must disclose live descendants that will also be cancelled.
- Preserve failed sessions, prompts, artifacts, and technical details for recovery.
- Rate-limit, quota, and authentication failures need provider-specific recovery actions.

### Workspace rules

- At widths below `1180px`, agent/todo and inspector panes are mutually exclusive overlay drawers.
  Opening a drawer must not increase the window minimum-size hint or shrink the transcript.
- Every compact drawer needs a visible close control and must close with Escape.
- Keep the transcript readable at `1000×680`; toolbar actions and composer controls must not clip.
- Preserve a reader's scroll position when new output arrives. Show a new-output control when the
  reader is away from the tail.
- Transcript search must expose match count plus previous and next navigation.
- Long reasoning blocks should be collapsible.
- Manual context compression and transcript clearing need progress or confirmation feedback.
- Todo editing must preserve backend task and phase IDs. Keep optimistic UI mutations synchronized
  with the live run or persisted session and recover cleanly when write-through is unavailable.
- Tool indicators must distinguish never used, previously used, and active now without relying on
  color alone.

### Empty, loading, and error states

- Do not leave blank cards, tables, panes, or tabs.
- Empty states should explain why the area is empty and what the user can do next.
- Loading states must prevent duplicate actions while keeping the rest of the window responsive.
- Error messages should contain a short human explanation. Put stack traces, provider payloads,
  and other diagnostics in copyable details.

## Accessibility

- Set `accessibleName` on icon-only, ambiguous, and custom controls.
- Set `accessibleDescription` when state, scope, or impact is not obvious from the name.
- Keep all workflows keyboard reachable with a visible focus indicator.
- Do not encode meaning with color alone; include text, glyph, label, or state description.
- Maintain at least 4.5:1 contrast for normal text and 3:1 for large text and interactive
  boundaries. Check both default and focused states. `theme.contrast_ratio` computes it;
  clearing `tokens().color.readable_ground` clears every ground text is painted on. Every
  built-in theme is swept for this, so a new palette has to clear it too.
- **Pick the token for the role, not the state.** A run state has two forms, and choosing
  wrongly is an accessibility defect rather than a style preference: `color.run` is the dot,
  ring segment or chart stroke (owes 3:1) and `color.run_text` is the word (owes 4.5:1). The
  design system paints a tag's text several steps lighter than the dot beside it for exactly
  this reason. Same for `wait`, `done`, `fail`, `info_state`/`info_text` and `idle`.
- Derive a colour variant by climbing towards white, not down towards the ground. On a dark
  theme the readable band runs upward, so a darker shade of a mid-tone token falls under
  4.5:1. `theme.raise_on` and `theme.raise_to_readable` do it correctly: hue and chroma are
  preserved and only lightness moves, upward, stopping at the floor.
- Use logical tab order. Hidden compact-pane controls must not remain in the active tab sequence.
- Give tables and lists meaningful accessible names and preserve explicit selection state.
- Keep text selectable or copyable when users may need it for debugging.
- Avoid hover-only actions. A hover-revealed action must also be keyboard focusable and discoverable
  through an accessible name or tooltip.

## Responsive and visual verification

For any layout or styling change, inspect at least:

- `1000×680`, compact drawers closed.
- `1000×680`, each compact drawer open.
- `1440×900`, all primary panes visible.
- One scaled display configuration when practical, especially for toolbar or dialog changes.

Check for clipped text, hidden buttons, unexpected horizontal scrolling, overlapping widgets,
minimum-size growth, stale focus rings, and unreadable secondary text. Offscreen screenshots are
useful, but behavioral pytest-qt assertions are still required.

## Implementation rules

- Reuse `make_button`, cards, feedback widgets, empty states, and theme tokens before creating new
  primitives.
- Keep user-visible strings specific, concise, and actionable.
- Keep expensive and synchronous backend work off the Qt event loop.
- Preserve atomic writes using a temporary file, flush/fsync where appropriate, and `os.replace`.
- Store desktop-only prompt conveniences under the workspace `.rotaris/` directory.
- Do not access private backend state from views. If unavoidable for orchestration integration,
  isolate it in `RunBridge` and cover it with a regression test.
- Programmatic shutdown and test teardown must not trigger interactive confirmation dialogs.
- Update all views that consume a changed store model; do not leave tuple/dict compatibility paths
  that silently discard identity or state.

## Testing and release gates

Test policy: [Product-Centred Test Strategy](../../docs/testing/test_strategy.md) and
[tests/AGENTS.md](../../tests/AGENTS.md). ReqToCode rules:
[root AGENTS.md](../../AGENTS.md#critical-rules--reqtocode-enforced-build-breaking) — they
apply here unchanged. For Rotaris requirements, the qualifying user-flow E2E boundary is
the real PySide6 desktop workflow with real internal store/service wiring; fake only
external systems.

Scoped gate commands (repo-wide forms are in [root AGENTS.md §Commands](../../AGENTS.md#commands)):

```bash
uv run ruff check apps/rotaris/src apps/rotaris/tests
uv run mypy apps/rotaris/src/rotaris
git diff --check
git status --short src/rotaris_core/tui
```

Add tests for each changed workflow, including the failure or cancellation path. For responsive
work, assert both compact and wide layouts. For service bridges, test the real state mutation or
persistence seam rather than only checking that a button emits a signal.

### Test levels

Every Rotaris test module declares its level with a module-level
`pytestmark = pytest.mark.<level>`; the markers are registered in the root and app
`pyproject.toml`. Select a level with `-m e2e`, `-m unit`, or `-m integration`.

- `unit` — a focused unit or a single widget primitive in isolation.
- `integration` — real collaboration across modules, persistence, or a UI/service seam.
- `e2e` — a productive flow driven through the window the user sees, faking only external
  systems such as LLM providers, OAuth, and the network. Reaching into a private method
  such as `window._submit_prompt` instead of clicking makes a test `integration`, whatever
  the file is named.

### Driving the UI in tests

Use `tests/ui_query.py` rather than reaching for a widget attribute. It finds controls by
accessible name — explicit `setAccessibleName` first, visible text as the fallback — and
refuses to drive a control that is hidden or disabled, so an unwired `clicked.connect` or a
control stranded in a collapsed drawer fails the test instead of passing it. This also makes
the accessible names Rotaris sets for screen readers load-bearing: break one and its tests
report the names that *are* reachable.

```python
from ui_query import click_by_name, find_by_accessible_name, settle, type_text

window.show_view("dashboard")
settle(qtbot)  # let deferred row deletions finish before querying
click_by_name(qtbot, window.dashboard, "+ New session", QPushButton)
```

Re-query after any action that rebuilds a pane; a reference captured earlier points at a
discarded row.

### Shared test support

Support modules sit beside the tests and are imported by name. Never import a helper from
another `test_*.py` module — that couples two suites and breaks collection when one is
refactored. If two modules need the same helper, it belongs in one of these:

- `tests/ui_query.py` — find and drive controls by accessible name.
- `tests/a11y.py` — contrast ratios and accessible-name sweeps over a live widget tree.
- `tests/fakes.py` — `FakeRunBridge`, `FakeCoordinatorBridge`, `FakeModelConfigService`,
  `FakeRunConfigService`. A fake records what the window asked for; anything that must
  behave rather than be observed belongs in a real object.
- `tests/run_wiring.py` — `ObserverHarness` plus real SDK event builders for the
  events → `_SessionObserver` → persisted session → store seam.

### Accessibility sweeps

`tests/test_accessibility_sweep.py` walks all seven primary views and fails when a control
has no accessible name or a label misses its WCAG AA ratio. A new view or control is
covered automatically, so adding a screen means fixing what the sweep reports rather than
writing new accessibility tests. Contrast is resolved from the widget's own stylesheet, its
ancestors, then the `objectName` defaults — which `a11y.py` now *derives* from
`theme.qss.object_styles`, the same table `build_qss` generates its rules from, rather than
keeping its own transcription (SWR-3706). A copy of that table drifts, and it fails in the
worst direction: the sweep goes on measuring against a colour the app stopped using and
reports everything as fine.

`test_theme_token_discipline.py` is the companion static check: it fails on a colour literal
outside `rotaris.theme` and on any token resolved at import time. That is what keeps the
property true as the app grows, rather than as a one-off audit.

Before completing a feature or bug fix:

- Verify no TUI files changed unless the user explicitly requested TUI work.
- Bump `apps/rotaris/pyproject.toml` and the root `pyproject.toml` as required by repository policy.
- Synchronize the matching editable package versions in `uv.lock`.
- Add or update a requirement record under the Rotaris epic
  `docs/requirements/2000-rotaris-desktop/` and satisfy ReqToCode per the root rules.
