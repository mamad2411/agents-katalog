---
name: settings-padding
description: "Rules and patterns for per-side padding settings — linked/unlinked toggle, 2×2 grid for individual controls, migration from a legacy single-value field, and s()-scaled CSS output. Use when adding padding controls to a component."
---

# Padding Settings — Usage Rule

## Rule

Padding follows a linked/unlinked pattern: a `Checkbox` toggles between a single "all sides" input and a 2×2 grid of individual per-side inputs.

- **Do** store four per-side fields (`paddingTop`, `paddingRight`, `paddingBottom`, `paddingLeft`) and a `paddingLinked` boolean in state.
- **Do** default `paddingLinked` to `true`.
- **Do** write a migration block in `common.js` that reads any legacy single-value field and fans it out to the four per-side fields.
- **Do** use `s()` on every numeric value in the CSS template string in `live.js`.
- **Do** gate the 2×2 grid behind `paddingLinked !== false` (not `=== true`) to handle `undefined` safely.
- **Do not** allow negative padding — clamp `min` at `0`.
- **Do not** skip the `Number(...)` cast when reading state values in `live.js` — they may arrive as strings.

> **Prefix fields with a meaningful noun when multiple elements need independent padding.** For example, use `cardPaddingTop` rather than plain `paddingTop` so one element's spacing does not clash with another.

---

## Patterns

### State fields — common.js

Add a migration block before `return`, then include the fields in the returned object.

```js
// Migration: per-side padding from legacy single padding field
const legacyPadding = getNumberValue(state && state.padding, 24);
const defaultPaddingTop =
  state && state.paddingTop != null
    ? getNumberValue(state.paddingTop, legacyPadding)
    : legacyPadding;
const defaultPaddingRight =
  state && state.paddingRight != null
    ? getNumberValue(state.paddingRight, legacyPadding)
    : legacyPadding;
const defaultPaddingBottom =
  state && state.paddingBottom != null
    ? getNumberValue(state.paddingBottom, legacyPadding)
    : legacyPadding;
const defaultPaddingLeft =
  state && state.paddingLeft != null
    ? getNumberValue(state.paddingLeft, legacyPadding)
    : legacyPadding;
```

Return object fields (inside `return { ... }`):

```js
paddingTop:    defaultPaddingTop,
paddingRight:  defaultPaddingRight,
paddingBottom: defaultPaddingBottom,
paddingLeft:   defaultPaddingLeft,
paddingLinked: state && state.paddingLinked != null ? Boolean(state.paddingLinked) : true,
```

---

### Editor controls — editor.js

Place this block inside the relevant `Section` (typically **Style** or **Design** tab).

```jsx
<div className="cmp-settings-subsection-heading">Padding (px)</div>
<SettingItem>
  <Checkbox
    label="Same for all sides"
    value={state.paddingLinked !== false}
    onChange={(v) => setState({ ...state, paddingLinked: v })}
  />
</SettingItem>
{state.paddingLinked !== false ? (
  <SettingItem>
    <Label content="All sides" />
    <NumberInput
      min={0}
      max={120}
      step={1}
      value={state.paddingTop}
      onChange={(val) => {
        const n = Number(val)
        setState({ ...state, paddingTop: n, paddingRight: n, paddingBottom: n, paddingLeft: n })
      }}
    />
  </SettingItem>
) : (
  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', boxSizing: 'border-box' }}>
    <SettingItem>
      <Label content="Top" />
      <NumberInput
        min={0}
        max={120}
        step={1}
        value={state.paddingTop}
        onChange={(val) => setState({ ...state, paddingTop: Number(val) })}
      />
    </SettingItem>
    <SettingItem>
      <Label content="Right" />
      <NumberInput
        min={0}
        max={120}
        step={1}
        value={state.paddingRight}
        onChange={(val) => setState({ ...state, paddingRight: Number(val) })}
      />
    </SettingItem>
    <SettingItem>
      <Label content="Bottom" />
      <NumberInput
        min={0}
        max={120}
        step={1}
        value={state.paddingBottom}
        onChange={(val) => setState({ ...state, paddingBottom: Number(val) })}
      />
    </SettingItem>
    <SettingItem>
      <Label content="Left" />
      <NumberInput
        min={0}
        max={120}
        step={1}
        value={state.paddingLeft}
        onChange={(val) => setState({ ...state, paddingLeft: Number(val) })}
      />
    </SettingItem>
  </div>
)}
```

> **`InputField` wrapper** — If the component already defines a local `InputField` helper, use it instead of bare `NumberInput`. It auto-generates Min/Max hint text below the input. Replace `<NumberInput .../>` with `<InputField type="number" .../>`.

---

### Live rendering — live.js

Compute safe numeric values inside the component function:

```js
const paddingTop = Number(state.paddingTop) || 0;
const paddingRight = Number(state.paddingRight) || 0;
const paddingBottom = Number(state.paddingBottom) || 0;
const paddingLeft = Number(state.paddingLeft) || 0;
```

Apply in the CSS template string (always wrap with `s()`):

```js
const styles = `
  .my-element {
    padding: ${s(paddingTop)}px ${s(paddingRight)}px ${s(paddingBottom)}px ${s(paddingLeft)}px;
  }
`;
```

**Responsive compact layout** — when a breakpoint adds extra vertical breathing room, adjust only the vertical axes:

```js
padding: ${s(paddingTop + extraVertical)}px ${s(paddingRight)}px ${s(paddingBottom + extraVertical)}px ${s(paddingLeft)}px;
```

---

## Quick reference

| Situation                                      | Pattern                                                                                               |
| ---------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| All sides equal                                | `paddingLinked: true` — single `NumberInput` writes all four fields simultaneously                    |
| Independent sides                              | `paddingLinked: false` — 2×2 grid, each input updates one field                                       |
| Guard against undefined `linkedFlag`           | Use `state.paddingLinked !== false`, not `state.paddingLinked === true`                               |
| Multiple padded elements (card, inner, etc.)   | Prefix state fields: `cardPaddingTop`, `innerPaddingTop`, etc.                                        |
| Legacy component with a single `padding` field | Add migration block: read legacy value into `legacyPadding`, default all four per-side fields from it |
| Extra vertical space at a compact breakpoint   | `${s(paddingTop + extraVertical)}px ${s(paddingRight)}px ${s(paddingBottom + extraVertical)}px ...`   |

---

## What not to do

```jsx
// ❌ Single padding field — no per-side control
<NumberInput
  value={state.padding}
  onChange={(padding) => setState({ ...state, padding })}
/>

// ❌ Linked check with === true — breaks when field is undefined
{state.paddingLinked === true && <NumberInput ... />}

// ❌ String interpolated directly without Number() cast — may produce 'NaNpx'
padding: ${state.paddingTop}px ${state.paddingRight}px ...

// ❌ s() omitted — breaks scaling in the Dot.vu editor preview
padding: ${paddingTop}px ${paddingRight}px ...

// ❌ Negative padding allowed
<NumberInput min={-20} ... />
```
