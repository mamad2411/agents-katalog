# React Build Rules

Rules and patterns for translating Figma designs into React/TypeScript view-layer components in Nitro. Read alongside [SKILL.md](../SKILL.md) (the process orchestrator), [REFERENCE.md](./REFERENCE.md) (shared lookups), and [component-intelligence.md](./component-intelligence.md) (playbook-builder behavior, MCP guide, component recognition).

---

## Component-specific rules

These supplement the universal translation rules in [SKILL.md](../SKILL.md) Step 6.

### 1. DatePicker requires `pickerId`

Flatpickr needs a DOM id. Without it: `document.querySelector(...) is null` — crashes the React tree.

```tsx
<DatePicker onChange={handleDate} pickerId="purchase-date" />
```

### 2. `htmlOptions` — avoid entirely, never on form components

**Always prefer Playbook props over `htmlOptions`.** Do not use `htmlOptions` for styling when a Playbook prop exists (e.g., use `background="light"` not `htmlOptions={{ style: { backgroundColor: "..." } }}`).

If `htmlOptions` is absolutely unavoidable (no Playbook prop exists), add a comment explaining why. **Never apply `htmlOptions` to these components** — they pass unknown props to the DOM, causing React warnings:

| Component | Use instead |
|-----------|------------|
| `TextInput` | Playbook props: `width`, `marginBottom`, etc. |
| `Textarea` | Playbook props only (`marginBottom` not supported) |
| `Select` | Playbook props only |

### 3. Content area `maxWidth`

**Every content column must be checked for maxWidth.** The spec now emits `dimensions` on all layout nodes (not just FIXED), so you always have width data.

**When the spec includes `maxWidth`:** Use it directly — playbook-builder already mapped the effective width to a token.

**When the spec omits `maxWidth`:** Check `dimensions.width` on the content column. If it exceeds ~1240px and the column contains form fields, the page needs a manual maxWidth constraint. See [component-intelligence.md](./component-intelligence.md) → "Form pages without maxWidth" for the heuristic table.

| Spec width | Token |
|-----------|-------|
| ~480px | `"sm"` |
| ~720px | `"md"` |
| ~960px | `"lg"` |

Add `margin="auto"` when `maxWidth` is present.

```tsx
<Flex margin="auto" maxWidth="md" orientation="column" width="100%">
  {/* form content */}
</Flex>
```

### 4. Select — use `options` prop exclusively

**Never use `<option>` children.** They bypass Playbook styling, rendering a borderless unstyled input.

```tsx
// CORRECT
<Select
  label="Territory"
  onChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
    handleChange("territory", e.target.value)
  }
  options={[
    { value: "", text: "All Territories" },
    ...territoryOptions.map(o => ({ value: o.value, text: o.label })),
  ]}
  value={formData.territory}
/>

// WRONG — unstyled, no border
<Select label="Territory" onChange={handleChange}>
  <option value="">All Territories</option>
</Select>
```

### 5. `textAlign` on containers — skip it

Figma's `textAlign: center` on frames means "center children" (layout). CSS `text-align` cascades to all descendant text, misaligning input labels and body text. Apply `textAlign` only to `Title`, `Body`, `Caption`, `Detail`.

### 6. Component `text` exceptions

| Component | Spec `text` | Use instead |
|-----------|------------|-------------|
| `Timestamp` | Display text — ignore | `timestamp={new Date()}` |
| `Avatar` | Layer name — ignore | `name="Full Name"` |

### 7. Component prop gotchas

These are **Playbook component behaviors** documented in `.cursor/rules/playbook-components.mdc`. During Figma builds, watch for these spec-to-code translation mistakes:

- **Pill / Badge** — `text` prop is **required**. Use `text="Review"`, never JSX children `<Pill>Review</Pill>`. See `playbook-components.mdc` → Pill, Badge.
- **`requiredIndicator` vs `required`** — The spec emits `requiredIndicator`. Use that, not `required` (different behavior). See `playbook-components.mdc` → TextInput, Textarea.
- **SectionSeparator** — Renders at zero width by default. Always add `width="100%"`. See `playbook-components.mdc` → SectionSeparator.

---

## Explicit event handler types

**All inline event handlers MUST have explicit type annotations.** Never use bare `e =>`.

| Component | `onChange` signature |
|-----------|-------------------|
| `TextInput` | `(e: React.ChangeEvent<HTMLInputElement>) => void` |
| `Textarea` | `(e: React.ChangeEvent<HTMLTextAreaElement>) => void` |
| `Select` | `(e: React.ChangeEvent<HTMLSelectElement>) => void` |
| `DatePicker` | `(dateString: string, dateArray: Date[]) => void` |
| `Typeahead` | `(selected: Array<{ label: string; value: string }>) => void` |

```tsx
// CORRECT
onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleChange("name", e.target.value)}

// WRONG — implicit type
onChange={e => handleChange("name", e.target.value)}
```

---

## Lint rules

### JSX prop ordering

ESLint enforces `react/jsx-sort-props` — **all JSX props in A-Z order**. The spec outputs props alphabetically; preserve that and insert handlers (`onChange`, `onClick`) in order.

```tsx
// CORRECT
<Button onClick={handleClick} text="Submit" variant="primary" />

// WRONG — fails CI
<Button variant="primary" text="Submit" onClick={handleClick} />
```

### One component per file

`react/no-multi-comp` — each `.tsx` exports one React component. Extract sub-components into separate files.

### No console statements

`no-console` — use a noop for placeholder handlers:

```tsx
// eslint-disable-next-line @typescript-eslint/no-empty-function
const noop = () => {}
```

---

## Verify wiring

**Do not generate wiring files.** The component's entrypoints, barrel exports, routes, controllers, and views are the developer's responsibility — they either already exist (Path A) or are created by nitro-web's generator (Path B).

**Read-only checks:** Confirm these files exist before building. If any are missing, tell the user what's needed so they can create or generate them.

| File | What to check |
|------|--------------|
| `app/javascript/entrypoints/<component>/index.ts` | Has `nitroReact.register(...)` for the app |
| `app/javascript/index.ts` (or `index.tsx`) | Exports the app |
| `config/routes.rb` | Has a route for the page |
| `app/controllers/` | Has a controller that renders the view |

If files are missing, tell the user: "These wiring files are needed for the page to render. You can create them manually or run the component generator."

---

## Code patterns

```tsx
import React from "react"
import { Card, Flex, Title, Body, TextInput, Select } from "playbook-ui"

<Card padding="md" width="100%">
<Flex flex="1" orientation="column">
<TextInput label="GL Code" placeholder="00-00-0000" required />
<Flex gap="md" orientation="row">
  <Card flex="2" padding="md">{/* left column */}</Card>
  <Flex flex="3" orientation="column">{/* right column */}</Flex>
</Flex>
<Flex background="light">
```

---

## Mock data

### Typed data contracts (`types.ts`)

Every form field appears in `FormData`. Add JSDoc noting the backend endpoint.

```typescript
/** TODO: Wire to backend endpoint */
export type FormData = {
  itemName: string
  territory: string
  cost: string
}

export type SelectOption = { value: string; text: string }
```

### Mock data (`mockData.ts`)

Import types. Use realistic values from the Figma spec text — not "test" or "lorem ipsum". Select options: 3-5 realistic entries.

```typescript
import { FormData, SelectOption } from "./types"

// TODO: Replace with data from backend
export const initialFormData: FormData = {
  itemName: "",
  territory: "",
  cost: "",
}

// TODO: Replace with data from backend
export const territoryOptions: SelectOption[] = [
  { value: "east", text: "Eastern" },
  { value: "west", text: "Western" },
]
```

State management, form submission, and button handlers are the developer's responsibility. Use `// TODO: Wire form state and submission` in component files where handlers are needed.

---

## Format and lint

```bash
npx prettier --write app/javascript/YourAppName/
yarn lint
```

Key Prettier rules: `arrowParens: "avoid"` (write `item =>` not `(item) =>`), `semi: false`.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `document.querySelector(...) is null` | `DatePicker` missing `pickerId` | Add `pickerId="unique-id"` |
| `htmlOptions` warning on DOM element | `htmlOptions` on `TextInput`/`Textarea`/`Select` | Remove; use Playbook props |
| `marginBottom` warning on DOM element | `marginBottom` on `Textarea` | Remove — unsupported |
| Content area too wide | Missing `maxWidth` | Add token + `margin="auto"` |
| Input labels center-aligned | `textAlign="center"` on container | Remove from `Card`/`Flex` |
| Select without border | `<option>` children instead of `options` prop | Use `options={[{ value, text }]}` |
| 500 — entrypoint not found | Missing Vite entrypoint | Create `entrypoints/<component>/index.ts` |
| Blank page | Export mismatch | Verify export matches `render_app("AppName")` |
| 500 in Milano / CI build | Missing `tsconfig.json` | Add extending root |
| Module not found | Missing `package.json` | Create it; run `yarn install` |
| Page outside Nitro shell | Missing layout | Add `layout "nitro_theme/application"` to controller |

