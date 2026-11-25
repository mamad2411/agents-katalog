---
name: heroui-all-components
description: >
  Catalog of all HeroUI v3 React components by category (Buttons, Forms,
  Overlays, Navigation, etc.). Use to pick the right component, map kebab doc
  paths to PascalCase exports, and open per-component docs. Keywords: HeroUI
  components, all components, Button Modal Select Accordion catalog, @heroui/react.
  Use when the user runs /heroui-all-components.
---

# HeroUI All Components (v3)

Explore the full library surface: **71** components (as of v3.0.x). More are on the way.

**Index:** https://heroui.com/en/docs/react/components  
**Source:** https://raw.githubusercontent.com/heroui-inc/heroui/refs/heads/v3/apps/docs/content/docs/en/react/components/index.mdx

## Apply the Skill

- Read `references/catalog.md` for the full categorized inventory + doc URLs.
- Prefer this skill to **discover / route** which component to use; then load `heroui-react` (or fetch MDX) for anatomy, props, and examples.
- Enforce compound composition and semantic variants via `heroui-composition-patterns` and `heroui-design-principles`.
- Styling/tokens: `heroui-styling`, `heroui-colors`, `heroui-dark-mode`, `heroui-animation-and-transitions`.

## Doc URL pattern

```text
https://heroui.com/docs/react/components/{kebab-name}
https://heroui.com/docs/react/components/{kebab-name}.mdx
```

| Export (PascalCase) | Doc slug (kebab) |
|---------------------|------------------|
| `Button` | `button` |
| `AlertDialog` | `alert-dialog` |
| `ButtonGroup` | `button-group` |
| `ColorSwatchPicker` | `color-swatch-picker` |
| `DateRangePicker` | `date-range-picker` |
| `InputOTP` | `input-otp` |
| `ProgressBar` | `progress-bar` |
| `RadioGroup` | `radio-group` |
| `ScrollShadow` | `scroll-shadow` |
| `ToggleButtonGroup` | `toggle-button-group` |

Import from `@heroui/react` (compound parts via dot notation or named exports).

## Categories (quick map)

| Category | When to use | Components (summary) |
|----------|-------------|----------------------|
| **Buttons** | Actions, toggles, close | Button, ButtonGroup, CloseButton, ToggleButton, ToggleButtonGroup |
| **Collections** | Menus / lists of options | Dropdown, ListBox, TagGroup |
| **Colors** | Color selection UI | ColorArea, ColorField, ColorPicker, ColorSlider, ColorSwatch, ColorSwatchPicker |
| **Controls** | Continuous / binary control | Slider, Switch |
| **Data Display** | Status chips, tables, badges | Badge, Chip, Table |
| **Date and Time** | Calendars & temporal fields | Calendar, RangeCalendar, DateField, DatePicker, DateRangePicker, TimeField |
| **Feedback** | Loading, progress, alerts | Alert, Meter, ProgressBar, ProgressCircle, Skeleton, Spinner |
| **Forms** | Inputs, labels, validation | Form, Fieldset, Label, Description, Input, InputGroup, InputOTP, TextField, TextArea, NumberField, SearchField, Checkbox, CheckboxGroup, RadioGroup, FieldError, ErrorMessage |
| **Layout** | Structure & chrome | Card, Separator, Surface, Toolbar |
| **Media** | People / images | Avatar |
| **Navigation** | Wayfinding & disclosure | Accordion, Breadcrumbs, Disclosure, DisclosureGroup, Link, Pagination, Tabs |
| **Overlays** | Floating layers | AlertDialog, Drawer, Modal, Popover, Toast, Tooltip |
| **Pickers** | Choose from options | Autocomplete, ComboBox, Select |
| **Typography** | Text primitives | Kbd, Typography |
| **Utilities** | Scroll affordances | ScrollShadow |

Full list with links: `references/catalog.md`.

## Work in This Order

1. **Intent** — action, form field, overlay, navigation, feedback, date, color, layout.
2. **Category** — pick row above (or catalog).
3. **Component** — prefer the most specific primitive (e.g. `SearchField` over bare `Input` + icon hacks when it fits).
4. **Docs** — fetch `…/components/{kebab}.mdx` or use `heroui-react` scripts / MCP.
5. **Compose** — compound parts; semantic variants; theme tokens.

## Decision Rules

### Buttons vs toggles vs links

| Need | Prefer |
|------|--------|
| Navigate | `Link` |
| One-shot action | `Button` |
| On/off in a toolbar | `ToggleButton` / `ToggleButtonGroup` |
| Grouped related actions | `ButtonGroup` |
| Dismiss control | `CloseButton` |

### Forms

- Prefer **named field components** (`TextField`, `NumberField`, `SearchField`, `DateField`) when they match the data type.
- Use `Form` + `Fieldset` + `Label` / `Description` / `FieldError` for structure and a11y.
- Choice: `Checkbox` / `CheckboxGroup`, `RadioGroup`, `Switch` (controls), `Select` / `ComboBox` / `Autocomplete` (pickers).

### Overlays

| Need | Prefer |
|------|--------|
| Confirm destructive / blocking | `AlertDialog` |
| Large panel | `Modal` or `Drawer` |
| Anchored lightweight content | `Popover` |
| Hover/focus hint | `Tooltip` |
| Transient message | `Toast` |

### Collections vs pickers

- **Select / ComboBox / Autocomplete** — form value selection (pickers).
- **ListBox / Dropdown / TagGroup** — list/menu patterns (collections); often composed inside pickers/menus.

### Refreshing the catalog

When docs drift, re-list via `heroui-react` skill:

```bash
node ~/.agents/skills/heroui-react/scripts/list_components.mjs
```

Or browse https://heroui.com/docs/react/components and the repo folders under `apps/docs/content/docs/en/react/components/(category)/`.

## Anti-Patterns

- Reaching for v2 component names/APIs (`HeroUIProvider`, visual variants only)
- Flat mega-props instead of compound anatomy from the component page
- Using `Button` for pure navigation without `Link` / router composition
- Inventing custom color pickers when Color* components exist
- Skipping FieldError/Description on forms that need validation messaging

## Reference Map

- Full catalog: `references/catalog.md`
- Index: https://heroui.com/en/docs/react/components
- meta pages (repo): `apps/docs/content/docs/en/react/components/meta.json`
- Sibling: `heroui-react` (install + per-component fetch), composition/styling/colors/dark-mode/animation skills
