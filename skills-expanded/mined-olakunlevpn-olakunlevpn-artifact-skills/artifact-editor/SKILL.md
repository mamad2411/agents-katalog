---
name: artifact-editor
description: OUTPUT IS ALWAYS A `.html` FILE (never `.md`, never plain markdown) with working jQuery UI widgets and JavaScript wired up. Use this skill whenever the user asks for an interactive editor, triage board, kanban board, "thing I can drag around", feature flag panel, feature flag dashboard, prompt tuner, prompt playground, parameter panel, "let me adjust X live", "give me a UI to play with this", or any HTML artifact that the user is expected to manipulate (drag, sort, tweak sliders, toggle flags, edit and export). Pair with `artifact-css` for the underlying design system and `jQuery 4.0.0 + jQuery UI 1.14.2` for the interactivity (sortable, draggable, slider, datepicker, dialog, autocomplete widgets). Do NOT use for static dashboards that just display data — only when the user must change something and ideally export the result.
---

# artifact-editor

> ## OUTPUT CONTRACT
>
> **Produces ONE `.html` file. Not markdown. Not `.md`. Not plain text.**
>
> Editors are interactive HTML artifacts with real, working JavaScript. Sortables drag. Sliders slide. Dialogs open. Export buttons copy real JSON to clipboard. The file extension is `.html`, always — never a markdown description of "what the editor would do".
>
> Use the templates in `templates/`. Inline `artifact.css` inside `<style>` (Mode B — single-file portable) or `<link>` to it. Always load the jQuery 4.0.0 + jQuery UI 1.14.2 layer per `artifact-css/SKILL.md`.

---

Interactive HTML artifacts. The reader is also the writer. They drag cards, flip flags, slide ramps, edit prompts, and export the result as JSON, YAML, a Slack-paste, or a clipboard string.

Read `artifact-css/SKILL.md` first for the full OUTPUT CONTRACT, the design system, the page skeleton, and the **Interactivity layer** documenting the jQuery + jQuery UI loader pattern. Editor artifacts always opt-in.

## When to reach for this skill

- User says "build me a UI for X" with X being a data structure they want to manipulate.
- User wants a triage / planning board they can interact with.
- User wants to tune a feature-flag rollout interactively and copy the resulting config.
- User wants a prompt-tuning playground with sliders for temperature / top-p / max tokens.
- User wants a quick "design tool" or "config builder" they can ship as a single file.

Static reports and plans do NOT use this skill — they're read-only by design.

## Three templates

| Template | Use when |
|---|---|
| `templates/triage-board.html` | Kanban-style board with sortable cards across columns (Backlog / In flight / Done). LocalStorage persistence. JSON export. |
| `templates/feature-flag-panel.html` | Per-flag toggle + ramp slider + cohort filter + JSON config preview that updates live. |
| `templates/prompt-tuner.html` | Textarea for the prompt body, sliders for the numerical params, dropdowns for model + format, copy-to-clipboard export. |

Each template is a single-file HTML artifact, fully self-contained except for the CDN-loaded jQuery + jQuery UI.

## Widget cheat sheet

| jQuery UI widget | Used in |
|---|---|
| `sortable()` | Triage board columns. Drag cards within and between columns. |
| `draggable()` + `droppable()` | Alternative pattern when items move into static drop zones. |
| `slider()` | Feature flag ramp (0-100%) and prompt-tuner numeric knobs. |
| `dialog()` | Modal for the "Export" button — copy / download JSON. |
| `autocomplete()` | Tag filter on the triage board. |
| `datepicker()` | Schedule controls in feature-flag-panel (e.g. "ramp starts on…"). |

## Anatomy of an editor artifact

Six blocks. Use this order. Concrete shape varies per subtype.

1. **Header.** Eyebrow with what this tool does (`Tool · triage board`). h1 with the artifact title. `.lead` paragraph: one sentence describing what the user can change and how to export the result.
2. **Toolbar.** A `.row-between` strip at top: filter / search controls on the left, export button on the right. The export button opens a `dialog()` showing the current state serialized.
3. **Editor surface.** The main interactive area — the board, the panel, the form. This is where most of the JS wiring lives.
4. **Live preview.** A `.panel` (often collapsible) showing the current state as JSON or YAML. Updates on every change. Useful for the user to validate before exporting.
5. **Notes / constraints.** `.note` blocks calling out what's editable here vs what isn't, what's persisted vs what isn't, and any caveats about the export format.
6. **Export and reset.** Footer with the export action repeated and a "reset to defaults" link. The reset confirms via a `dialog()` before destroying state.

## LocalStorage persistence (when to enable)

| Template | Persist by default? |
|---|---|
| `triage-board.html` | **Yes** — board state survives reload. Reset button clears. |
| `feature-flag-panel.html` | **Yes** — flag configs survive reload. |
| `prompt-tuner.html` | **No** — every session starts clean. Users don't want stale prompts. |

Storage key pattern: `artifact-editor.<template-name>.v1`. Versioning the key prevents breakage if the schema changes in a later template release.

Always include the `?reset` URL hack:

```js
if (new URL(location).searchParams.has('reset')) {
  localStorage.removeItem(STORAGE_KEY);
  location.replace(location.pathname);
}
```

Saves a user from a corrupted local state.

## Export modal contract

Every editor includes an Export button that opens a `dialog()` with:

- A `<pre>` of the current state serialized (JSON 2-space indent, or YAML if the user explicitly asks).
- A "Copy to clipboard" button using `navigator.clipboard.writeText`.
- A "Download as .json" link using a `data:` or `Blob` URL.
- A "Close" button.

Never show the serialized state inline in the main page chrome — it's noisy. Modal is the right home.

## Fallback contract (no-JS)

Same as explainer — the page must remain readable:

- Sortable cards render as plain `<ul>` items in their starting positions.
- Sliders render as `<input type="range">` (HTML5 native) so they still adjust values, just without styled chrome.
- Dialogs degrade to inline `<details>`/`<summary>` blocks.
- LocalStorage usage is wrapped in `try { } catch {}` — private browsing / disabled storage doesn't crash the page.

Achieve this by writing semantic HTML first, then progressively enhancing.

## Voice and density rules

1. **Show the data.** The live preview block is the single most important block in an editor. Don't hide it behind a tab.
2. **Defaults must be sane.** A user who opens the artifact and immediately exports must get something useful. Never start with empty state.
3. **Disable, don't hide.** Controls that are unavailable in the current state are visibly disabled (greyed `.muted`), not hidden. Hidden controls confuse.
4. **Confirm destructive actions.** Reset, clear, delete-all — always via `dialog()` confirmation. Never one-click.
5. **No invented data.** If the template ships with sample cards / sample flags, label them clearly as samples in the export — never let a user accidentally ship sample data as if it were real.

## Common mistakes

- **No export.** An editor where you can change things but can't get them out is a toy. Always include export.
- **Persisting too much.** Persisting filter state? Yes. Persisting which dialog was last opened? No. Persist only the artifact's data, never UI ephemera.
- **Sortable with no drop hint.** Cards must visibly indicate where they'd drop on hover. jQuery UI's `placeholder` option handles this — use it.
- **Slider that doesn't show its current value.** Always pair a `.slider()` with a sibling `<output>` showing the current numeric value.
- **Dialog modal that locks the page on no-JS.** Use `<details>` fallback markup.

## Linting (skill-local)

Before shipping, check:

1. The artifact opens cleanly with JS disabled — content is fully readable.
2. The export modal copies real, current data — not a stale snapshot.
3. The reset button has a confirmation dialog.
4. LocalStorage write is wrapped in try/catch.
5. The page works in a private/incognito window where localStorage may throw.
6. All sliders pair with an `<output>` showing the value.

## After the artifact

Offer two derivatives:

1. The current state serialized as JSON, for paste into Slack or a config file.
2. A short "what to do with this" paragraph: what file to commit this to, what command to run with it, what reviewer to ping.
