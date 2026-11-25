---
name: demoable-visually-testable-ui-components
description: Guides frontend UI component design toward explicit, deterministic, controllable visual states, reusable fixtures, and visual testability. Use whenever creating, changing, refactoring, reviewing, or testing frontend components, UI state, design primitives, Storybook stories, visual regression tests, or product demos.
---

# Rules for Demoable and Visually Testable UI Components

## 1. Every component must be renderable from explicit state

A component should not require the entire application to exist before it can render.

Prefer:

```svelte
<DocumentToolbar
  mode="reading"
  selection={selection}
  annotationCount={3}
  canAnnotate={true}
/>
```

over:

```svelte
<DocumentToolbar />
```

where `DocumentToolbar` internally reads:

* route state
* global stores
* authentication
* current document
* selection state
* permissions
* network cache

A component should ideally be describable as:

```text
UI = render(props)
```

This makes it possible to reproduce any visual state directly.

---

## 2. Separate visual state from application state

Application state may be complicated:

```ts
{
  user,
  organization,
  document,
  permissions,
  subscription,
  annotations,
  websocketStatus,
  ...
}
```

The component usually does not need all of that.

Give it a small view model:

```ts
type AnnotationToolbarViewModel = {
  visible: boolean;
  selectedText: string;
  canComment: boolean;
  canAskAI: boolean;
  anchor: {
    x: number;
    y: number;
  };
};
```

Then transform application state into that model outside the component.

```text
Application state
       ↓
   adapter
       ↓
UI ViewModel
       ↓
 component
```

This is one of the most important rules.

---

## 3. Prefer controlled components

Important state should be controllable from the outside.

Instead of:

```svelte
<Popover />
```

where the popover decides internally whether it is open, support:

```svelte
<Popover open={true} />
```

Likewise:

```svelte
<Select value="pdf" open={true} />
```

```svelte
<Tooltip visible={true} />
```

```svelte
<AnnotationComposer
  state="typing"
  text="@Curie explain this"
/>
```

The production component may still provide an uncontrolled convenience API, but there should always be a controlled path.

This allows a test to say:

```text
render toolbar
popover = open
selection = active
cursor = hovering
```

without performing five mouse interactions first.

---

## 4. Treat meaningful UI states as named states

Avoid building complicated visual behaviour around dozens of unrelated booleans.

Bad:

```ts
{
  loading: false,
  selected: true,
  toolbarVisible: true,
  aiLoading: false,
  annotationOpen: true,
  inputFocused: true
}
```

Better:

```ts
type AnnotationState =
  | "idle"
  | "selecting"
  | "selected"
  | "composer"
  | "submitting"
  | "completed";
```

Then additional data belongs beside the state:

```ts
type AnnotationViewModel = {
  state: AnnotationState;
  selection?: Selection;
  draft?: string;
};
```

Named states naturally become:

```text
Storybook stories
Visual snapshots
Demo checkpoints
Playwright fixtures
Documentation examples
```

---

## 5. Every important state should have a fixture

For example:

```text
fixtures/
  reader/
    empty.ts
    document-loaded.ts
    text-selected.ts
    annotation-open.ts
    ai-query-typing.ts
    ai-response.ts
```

Each fixture should be deterministic.

```ts
export const textSelectedFixture = {
  document: sampleDocument,
  selection: {
    text: "The restricted three-body problem...",
    start: 143,
    end: 187
  },
  annotation: {
    state: "selected"
  }
};
```

Then all environments reuse it:

```text
Production debugging
Storybook
Demo
Playwright
Screenshot regression
Design review
```

---

## 6. Fixtures must contain data, not behaviour

A fixture should describe the world.

Good:

```ts
{
  status: "loading",
  progress: 0.64
}
```

Avoid:

```ts
{
  simulateLoading: async () => ...
}
```

Fixtures should be serializable whenever practical.

Ideally:

```ts
JSON.stringify(fixture)
```

works.

That gives you powerful capabilities later:

```text
?fixture=annotation-open
```

or even:

```text
/demo/reader?state=ai-response
```

---

## 7. Time must be injectable

Animations and asynchronous UI often become impossible to snapshot because they depend on wall-clock time.

Avoid components implicitly depending on:

```ts
Date.now()
setTimeout()
Math.random()
requestAnimationFrame()
```

where possible.

For something such as:

```svelte
<RelativeTime timestamp={...} />
```

allow:

```svelte
<RelativeTime
  timestamp={timestamp}
  now={fixedNow}
/>
```

For demos, animation progress can even become explicit:

```svelte
<SelectionAnimation progress={0.73} />
```

Production can derive `progress` from time.

Tests can freeze it at `0.73`.

---

## 8. Animation state should be separable from component state

Think of animation as:

```text
State A
   ↓ transition
State B
```

rather than animation being the state itself.

For example:

```svelte
<AnnotationPopover open={true} />
```

CSS handles:

```text
opacity
transform
scale
```

You should be able to disable transitions globally:

```css
[data-visual-test] * {
  animation-duration: 0s !important;
  transition-duration: 0s !important;
}
```

Or deliberately freeze a transition when testing the animation itself.

---

## 9. Components should support animation checkpoints

For important product interactions, define explicit checkpoints.

For example:

```ts
type ReaderDemoCheckpoint =
  | "document"
  | "cursor-enter"
  | "selection-half"
  | "selection-complete"
  | "toolbar-open"
  | "composer-open"
  | "prompt-entered"
  | "response";
```

Your demo can move through them:

```text
document
   ↓
cursor-enter
   ↓
selection-half
   ↓
selection-complete
   ↓
toolbar-open
   ↓
composer-open
```

Visual regression can render those exact same checkpoints independently.

This is significantly more reliable than:

```text
start animation
sleep 1850 ms
take screenshot
```

---

## 10. Demo orchestration must live outside product components

Do not put:

```ts
if (demoMode) {
  await sleep(700);
  selectParagraph();
  await sleep(300);
  openToolbar();
}
```

inside `Reader`.

Instead:

```text
Reader
Selection
AnnotationToolbar
Cursor
AIComposer
```

remain ordinary components.

Then create:

```text
ReaderDemoController
```

which orchestrates them.

For example:

```svelte
<Reader
  document={fixture.document}
  selection={scene.selection}
/>

<AnnotationToolbar
  state={scene.toolbar}
/>

<FakeCursor
  position={scene.cursor}
/>
```

The fake cursor should not even need to exist in the production application.

---

## 11. Build demos by composition, not by adding demo flags

Avoid APIs like:

```svelte
<Reader
  demoMode={true}
  fakeSelection={true}
  fakeCursor={true}
  marketingVersion={true}
/>
```

That pollutes production components.

Instead compose:

```svelte
<DemoViewport>
  <Reader {...readerState} />
  <DemoCursor {...cursorState} />
  <DemoSelection {...selectionState} />
</DemoViewport>
```

Production:

```svelte
<Reader {...realReaderState} />
```

Shared components remain clean.

---

## 12. Avoid hidden environmental dependencies

A visual component should not unexpectedly depend on:

```text
window dimensions
localStorage
cookies
current URL
locale
current timezone
network
user agent
feature flags
random IDs
system fonts
```

If one matters visually, expose it.

For example:

```svelte
<Date value={date} locale="en-GB" timezone="Europe/Warsaw" />
```

rather than silently reading browser state.

Determinism is the foundation of visual regression.

---

## 13. Network state must have visual models

Never make Storybook or visual tests depend on a real API.

Represent network state explicitly:

```ts
type AsyncData<T> =
  | { state: "idle" }
  | { state: "loading" }
  | { state: "success"; data: T }
  | { state: "error"; error: UIError };
```

Now every network state becomes testable:

```text
Document/loading
Document/loaded
Document/error
Document/reconnecting
```

---

## 14. Error and empty states are first-class states

Don't create only:

```text
HappyPath.stories.ts
```

Create:

```text
Empty
Loading
Partial
Overflow
PermissionDenied
Error
Offline
SlowNetwork
LongText
HugeNumber
MissingAvatar
```

These states are often where visual regressions actually happen.

---

## 15. Stable dimensions are part of component contracts

For demos and screenshots, layout stability matters enormously.

Avoid layout shifting because:

```text
avatar hasn't loaded
font hasn't loaded
image hasn't loaded
response hasn't arrived
```

Reserve space.

For example:

```css
.avatar {
  width: 32px;
  height: 32px;
}

.document-preview {
  aspect-ratio: 4 / 5;
}
```

A component's geometry should be as predictable as its data.

---

## 16. Build a deterministic demo viewport

Marketing demos should run inside a controlled canvas.

For example:

```svelte
<DemoViewport
  width={1200}
  height={760}
  scale="contain"
>
  <ReaderDemo />
</DemoViewport>
```

The demo always thinks it has:

```text
1200 × 760
```

The website can scale that viewport responsively.

This means the same fixture can produce:

```text
Marketing demo
Story
Visual regression snapshot
Documentation screenshot
Launch image
```

---

## 17. Test components at canonical viewport sizes

Define a small set rather than arbitrary dimensions.

For example:

```ts
export const viewports = {
  mobile: [390, 844],
  tablet: [768, 1024],
  desktop: [1440, 900],
  demo: [1200, 760]
};
```

Every component does not need every viewport.

Specify which matter.

---

## 18. Give visual states stable addresses

A UI state should ideally be directly navigable.

For example:

```text
/__ui/reader/text-selected
/__ui/reader/annotation-open
/__ui/library/empty
/__ui/library/loading
```

or:

```text
/__ui/reader?fixture=annotation-open
```

This is extremely useful.

Someone reporting a visual bug can send:

```text
/__ui/reader?fixture=annotation-open
```

instead of:

> Log in, open this paper, select paragraph three, click annotate...

---

## 19. Use semantic visual selectors

For automated interaction, expose stable semantics.

Prefer:

```html
<button aria-label="Add annotation">
```

or:

```html
<div data-ui="annotation-toolbar">
```

Avoid testing against:

```text
:nth-child(4)
.bg-gray-200
.absolute.left-4
```

Tests should survive CSS refactors.

---

## 20. Separate interaction tests from visual tests

Visual tests should answer:

> Does this state look correct?

Interaction tests should answer:

> Can the user reach this state correctly?

Don't require every visual screenshot to reproduce the whole interaction.

For example:

### Interaction test

```text
drag selection
→ toolbar appears
```

### Visual tests

Directly render:

```text
selection-complete
toolbar-open
composer-open
```

These two test categories complement each other.

---

## 21. Visual regression should snapshot state, not timing

Bad:

```ts
await page.waitForTimeout(1700);
await expect(page).toHaveScreenshot();
```

Good:

```ts
await page.goto(
  "/__ui/reader?checkpoint=toolbar-open"
);

await expect(page).toHaveScreenshot();
```

Even better:

```ts
await page.waitForSelector(
  '[data-checkpoint="toolbar-open"]'
);
```

The screenshot becomes deterministic rather than dependent on machine performance.

---

## 22. Demo state should be serializable when possible

If this:

```ts
{
  scene: "toolbar-open",
  document: "three-body",
  selection: "paragraph-2"
}
```

can be represented in a URL:

```text
/demo/reader
?scene=toolbar-open
&document=three-body
&selection=paragraph-2
```

you gain an extremely powerful debugging system.

State can be:

* bookmarked
* shared
* reproduced in CI
* used by designers
* loaded into Storybook
* captured automatically

---

## 23. Components should expose intent, not implementation

Prefer:

```svelte
<Button importance="primary">
```

rather than:

```svelte
<Button blue shadow large>
```

Prefer:

```svelte
<Annotation state="selected">
```

rather than:

```svelte
<Annotation yellowBackground borderWidth={2}>
```

The fixture should describe the product state.

The design system decides how that state looks.

This makes visual regression useful during design-system changes.

---

## 24. Design primitives must behave identically everywhere

Marketing demos should preferably use the same:

```text
Button
Tooltip
Popover
Avatar
Input
Card
Typography
Icon
Menu
```

as the actual application.

Do not make a parallel "marketing design system".

The demo may use simplified application composition, but primitives should remain shared.

Otherwise the showcase slowly stops representing the product.

---

## 25. Make component states observable

For debugging and automated demos, components can expose their meaningful state:

```html
<div
  data-ui="annotation"
  data-state="composer-open"
>
```

Not every internal detail.

Only semantic states.

This makes it trivial for Playwright to wait for:

```ts
page.locator(
  '[data-ui="annotation"][data-state="composer-open"]'
);
```

---

# Architectural principle

The application should ideally have three layers:

```text
┌───────────────────────────────┐
│ Application                   │
│ API, auth, routing, stores    │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│ UI State / View Models        │
│ deterministic + serializable │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│ Visual Components             │
│ props → pixels               │
└───────────────────────────────┘
```

A fourth layer can orchestrate presentation:

```text
                    ┌── Production interaction
View Models → UI ───┼── Storybook
                    ├── Visual regression
                    ├── Marketing demo
                    └── Documentation
```

The visual components should not care which environment is rendering them.

# Litmus test

For every significant component, ask:

> Can I render every meaningful visual state of this component by supplying data, without clicking anything, making a network request, authenticating, or waiting for time to pass?

If the answer is yes, the component is probably well structured.

If not, identify which hidden dependency prevents it.
