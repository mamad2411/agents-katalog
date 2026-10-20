---
name: compose-ui-builder
description: Build a Jetpack Compose screen from a spec, mockup, or Figma description — covering state hoisting, previews, theming, accessibility, and responsive layout for phones/tablets/foldables. Use whenever the user asks to "build a screen", "implement this design", "turn this mockup into Compose", "make a Composable for X", or pastes a Figma link or screenshot and wants UI code. Also use for redesigning or restructuring existing Composables.
---

# Compose UI Builder

Translate a design into production-quality Compose code. Not a snippet generator — a structured pass through state, layout, theming, and a11y so the result holds up in code review.

## When to use

Triggers: "build this screen", "implement this design", "convert this mockup", "Compose code for…", screenshots/Figma links + "make this".

For tiny one-off Composables (a custom Button), just write it. Use this skill when the surface is a full screen or a non-trivial component.

## Process

### Phase 1: Understand the surface

Before writing code, get clarity on three things. Ask the dev only if not already obvious:

1. **States**: What does the screen look like when loading? Empty? Error? Content with one item vs. many? Refreshing?
2. **Inputs**: What ViewModel/state holder feeds this, or is it a leaf?
3. **Interactions**: Which actions navigate away, which mutate local state, which call back to the parent?

Sketch a `UiState` sealed interface (or data class with nullable fields, matching the project's style) covering each visual state before laying out pixels.

### Phase 2: Layer the implementation

Build top-down, not pixel-by-pixel:

1. **Stateful wrapper** — the entry point the nav graph calls. Hoists `UiState` from the ViewModel via `collectAsStateWithLifecycle()`. Routes events.
2. **Stateless screen** — `@Composable fun Screen(state: UiState, onEvent: (Event) -> Unit)`. No ViewModel reference. This is the testable, previewable unit.
3. **Section composables** — break the screen into named regions (`HeaderSection`, `ListSection`). Easier to read, easier to recompose only what changed.
4. **Leaf composables** — buttons, cards, rows. Pull from the design system if one exists; only build new leaves when the system doesn't cover it.

### Phase 3: Theming and tokens

Use the project's theme — `MaterialTheme.colorScheme`, `Typography`, `Shapes`. Don't hardcode colors or sizes. If the design uses tokens the project doesn't have yet, flag it and propose adding them to the theme rather than inlining values.

For spacing, use a consistent scale (the project likely has one — `Spacing.md`, `8.dp` increments, etc.). Match it.

### Phase 4: Previews

Add a `@Preview` for each meaningful `UiState`:

- Loading
- Empty
- Content (one item, many items)
- Error

Use `@PreviewParameter` with a provider when states share a Composable. Add dark-theme and font-scale previews for screens that ship to users.

### Phase 5: Accessibility

Walk through:

- Every clickable Composable has a meaningful semantic role and a `contentDescription` or `Modifier.semantics { }` when the visible text isn't enough.
- Touch targets ≥ 48.dp (`Modifier.minimumInteractiveComponentSize()` if needed).
- Color isn't the only signal for state (add icons, text, or borders too).
- Focus order makes sense with TalkBack — test by enabling it.
- Decorative icons get `contentDescription = null`; functional ones get a real label.

### Phase 6: Responsive layout

If the app targets tablets or foldables, branch on `WindowSizeClass`:

- Compact: single column.
- Medium/Expanded: two-pane or wider list, depending on what the design suggests.

If only phones are in scope, say so explicitly so the dev knows it's a deliberate skip, not an oversight.

## Output

A working screen file (or set of files) plus:

- The `UiState` definition.
- At least one preview per state.
- A short note on which tokens/components were reused vs. created.
- Any open questions about states the design didn't cover.

## Common pitfalls

- **ViewModel inside the stateless Composable.** Kills previews and testability. Always split stateful/stateless.
- **Hardcoded colors and dp values.** Looks fine until dark mode or a redesign.
- **One giant Composable.** If it scrolls off the screen, break it up — recomposition cost and readability both suffer.
- **Skipping previews because "I'll just run the app".** Previews catch state-specific layout bugs faster than any emulator.
- **`Modifier` parameter missing.** Every reusable Composable should accept a `modifier: Modifier = Modifier` as its first optional parameter so callers can position it.
