---
name: design-to-component
description: Convert Figma designs into production-ready React components. Uses the Figma MCP to extract design specs, variants, design tokens, and layout — then scaffolds typed TypeScript components with proper prop interfaces. Triggers when a user shares a Figma URL or node ID and asks to implement, build, or convert a design.
disable-model-invocation: false
---

# Design to Component

Convert a Figma design into a typed, production-ready React component by extracting specs directly from the Figma MCP — no manual measurements or guesswork.

## When to Apply

Use this skill when:
- A user shares a Figma URL or node ID and says "implement this", "build this component", or "convert this design"
- Creating a new component and a Figma design exists as the source of truth
- Validating that an existing component matches its Figma spec
- Extracting design tokens (colors, spacing, typography) from a design into code

## Workflow

Follow these steps in order. Use the Figma MCP tools at each stage.

### Step 0 — Discover Project Conventions

Before touching any Figma tool, read `CLAUDE.md`, `README.md`, and any design system rules files (e.g. `.cursor/rules/`, `AGENTS.md`) to determine:

- **Styling approach**: CSS Modules, Tailwind, styled-components, vanilla CSS, or other
- **Token system**: CSS custom properties, Tailwind theme (`tailwind.config.js`), design token library, or none
- **Component conventions**: file structure, naming, existing UI components to reuse
- **Framework specifics**: Next.js App Router, Vite, CRA, etc. — affects import patterns

Pay close attention to `README.md` sections that document the project's CSS or design system structure — these are a primary source of truth for how tokens are named, where they live, and how they're used. If no such documentation exists, suggest the user add it to their README before or alongside this component, as it will make every future conversion more accurate.

If no rules exist and the project's approach is unclear, ask the user before generating code. Never assume a styling approach.

If the project uses the Figma MCP and has not yet generated design system rules, suggest running `figma_create_design_system_rules` once to produce a project-specific rules file they can save to `CLAUDE.md` or equivalent — this prevents the styling mismatch problem on every future component.

### Step 1 — Extract Design Metadata

Call `figma_get_metadata` with the node ID or URL to retrieve:
- Component name and description
- Node type (COMPONENT, COMPONENT_SET, FRAME, etc.)
- Size and layout constraints

Use the component name to determine the file name and export name.

### Step 2 — Extract Design Context

Call `figma_get_design_context` to get the full design spec:
- Layout mode (auto-layout direction, gap, padding)
- Fill colors, strokes, border radius
- Typography (font family, size, weight, line height)
- Effects (shadows, blur)
- Children and their hierarchy

Map layout mode to CSS:
- `HORIZONTAL` auto-layout → `display: flex; flex-direction: row`
- `VERTICAL` auto-layout → `display: flex; flex-direction: column`
- Fixed layout → `position: absolute` or `position: relative` with explicit sizing

### Step 3 — Extract Design Tokens

Call `figma_get_variable_defs` to retrieve variables bound to the node:
- Color variables → map to the project's token system (CSS custom properties, Tailwind theme key, design token variable, etc.)
- Spacing variables → map to gap/padding/margin values using the project's scale
- Typography variables → map to font-size, font-weight, line-height using the project's type scale

If no variables exist, extract raw values from Step 2 and treat them as fallbacks — always wrap them in the project's token reference where possible (e.g. `var(--color-primary, #0070f3)` or a Tailwind arbitrary value `bg-[#0070f3]`).

**Avoid over-tokenization:** Do not create a new token or config entry for every value you see. Slight Figma value differences (e.g. `#0071f4` vs `#0070f3`, `13px` vs `14px`) are almost always unintentional design drift — map them to the nearest existing token rather than minting new ones.

**When a value has no match:** If a Figma value genuinely doesn't correspond to any existing token, ask the user before creating a new one:
> "The design uses `[value]` which isn't in the token system. Should I map it to the nearest existing token (`[closest]`), create a new token, or use a raw/arbitrary value?"

### Step 4 — Identify Variants

If the node is a `COMPONENT_SET`, it has variants. Parse the variant properties from the metadata:
- Each variant property becomes a TypeScript prop
- Boolean variants → `prop?: boolean`
- Multi-value variants → `prop: 'value1' | 'value2' | 'value3'`
- Use a discriminated union if variants represent fundamentally different structures

Example: A button with `variant: Primary | Secondary | Destructive` and `size: SM | MD | LG` becomes:

```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'destructive';
  size?: 'sm' | 'md' | 'lg';
}
```

### Step 5 — Get Visual Reference

Call `figma_get_screenshot` to get a visual snapshot of the design. Keep this in context to validate the generated component visually.

### Step 6 — Scaffold the Component

Generate the component following these rules:

**File structure:**

Match the project's existing conventions (discovered in Step 0). A common layout:
```
ComponentName/
├── ComponentName.tsx      # Component implementation
├── ComponentName.module.css  # Only if using CSS Modules
└── index.ts               # Re-export
```
If the project uses a flat file structure or co-locates styles differently, follow that instead.

**Component template:**

Use the project's styling approach (discovered in Step 0). A generic starting point:
```typescript
interface ComponentNameProps {
  // Extracted from Figma variants and design context
  children?: React.ReactNode;
  className?: string;
}

export function ComponentName({ children, className }: ComponentNameProps) {
  return (
    <div className={className}>
      {children}
    </div>
  );
}
```
Fill in `className` using the project's styling method — CSS Modules reference, Tailwind utility string, styled-component, etc.

**Typing rules:**
- Always export a named interface (`ComponentNameProps`), never inline types
- Include `className?: string` for style overrides
- Include `children?: React.ReactNode` if the design has a content slot
- Extend `React.HTMLAttributes<HTMLDivElement>` (or the appropriate element) for native prop passthrough when the component is a simple wrapper

**Element selection:**
- Interactive elements (buttons, links) → `<button>` or `<a>`, never `<div>`
- Form inputs → native `<input>`, `<select>`, `<textarea>`
- Navigation → `<nav>`, `<ul>`, `<li>`
- Pure layout containers → `<div>` or `<section>`

**Variant implementation:**
Map each variant value to the appropriate style expression for the project's approach:
```typescript
// CSS Modules example
const variantClass = { primary: styles.primary, secondary: styles.secondary }[variant ?? 'primary'];

// Tailwind example
const variantClass = { primary: 'bg-blue-600 text-white', secondary: 'bg-transparent border border-gray-300' }[variant ?? 'primary'];
```
Use `clsx`, `cx`, or a similar utility if already present in the project. Fall back to `.filter(Boolean).join(' ')` only if no utility is available.

### Step 7 — Generate Styles

Use the styling approach established in Step 0. Do not introduce a new approach.

**CSS Modules / vanilla CSS**: Map Figma values to CSS properties. Reference project tokens as custom properties with raw value fallbacks:
```css
.root {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: var(--spacing-2, 8px);
  padding: var(--spacing-3, 12px) var(--spacing-4, 16px);
  background-color: var(--color-primary, #0070f3);
  border-radius: var(--radius-md, 6px);
  font-size: var(--text-sm, 14px);
  font-weight: 500;
  line-height: 1.4;
}
```

**Tailwind**: Map Figma values to utility classes. Use `tailwind.config.js` theme keys for colors and spacing. Don't create new properties or arbitrary values such as `bg-[#0070f3]`, `w-[42px]` unless absolutely necessary. If a value in Figma is slightly off from what's been set in `tailwind.config.js` use the version in the config file:
```tsx
<div className="flex flex-row items-center gap-2 px-4 py-3 bg-primary text-sm font-medium rounded-md" />
```

**styled-components / Emotion / CSS-in-JS**: Generate a styled component using the project's theme object:
```typescript
const Root = styled.div`
  display: flex;
  gap: ${({ theme }) => theme.spacing[2]};
  background: ${({ theme }) => theme.colors.primary};
`;
```

In all cases: never hardcode raw values where a project token exists, never introduce a styling method not already used by the project, and never silently create new tokens or config entries — ask the user first.

### Step 8 — Check Code Connect

Call `figma_get_code_connect_suggestions` to see if the component has existing Code Connect mappings. If mappings exist, follow the established prop naming conventions. If not, consider calling `figma_send_code_connect_mappings` to register the new component.

### Step 9 — Validate

After generating the component:
1. Ask the user to render the component in their app or Storybook
2. Compare against the `figma_get_screenshot` visual reference
3. Note any discrepancies in spacing, color, or typography
4. Adjust values iteratively

If a browser automation tool is available, use it to capture the rendered component and compare side-by-side with the Figma screenshot (e.g. `chrome_devtools_take_screenshot` via chrome-devtools MCP, `browser_screenshot` via browser MCP, or a Playwright screenshot command).

## Output Checklist

Before finishing, confirm:

- [ ] Component name matches Figma component name (PascalCase)
- [ ] All Figma variants are represented as TypeScript props
- [ ] Interactive elements use semantic HTML (not `<div>`)
- [ ] Design tokens are referenced via the project's token system (CSS variables, Tailwind theme, JS theme object), not hardcoded
- [ ] `className` prop is supported for external style overrides
- [ ] Component is exported from `index.ts`
- [ ] No inline styles (unless absolutely required for dynamic values)
- [ ] Accessibility: interactive elements have accessible labels

## Common Patterns

Before applying any pattern, read the project's `CLAUDE.md` and `README.md` to understand the conventions already in use — component structure, styling approach (CSS Modules, Tailwind, styled-components, etc.), naming conventions, and any established patterns. Adapt the examples below to match what the project already does.

### Icon + Label Button
```typescript
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  icon?: React.ReactNode;
  iconPosition?: 'left' | 'right';
}

export function Button({
  variant = 'primary',
  size = 'md',
  icon,
  iconPosition = 'left',
  children,
  className,
  ...props
}: ButtonProps) {
  return (
    <button
      className={[styles.root, styles[variant], styles[size], className]
        .filter(Boolean)
        .join(' ')}
      {...props}
    >
      {icon && iconPosition === 'left' && <span className={styles.icon}>{icon}</span>}
      {children}
      {icon && iconPosition === 'right' && <span className={styles.icon}>{icon}</span>}
    </button>
  );
}
```

### Card with Slots
```typescript
interface CardProps {
  header?: React.ReactNode;
  footer?: React.ReactNode;
  children: React.ReactNode;
  className?: string;
}

export function Card({ header, footer, children, className }: CardProps) {
  return (
    <div className={[styles.root, className].filter(Boolean).join(' ')}>
      {header && <div className={styles.header}>{header}</div>}
      <div className={styles.body}>{children}</div>
      {footer && <div className={styles.footer}>{footer}</div>}
    </div>
  );
}
```

### Compound Component (for complex designs with distinct sub-parts)
```typescript
export function Tabs({ children, className }: TabsProps) { ... }
Tabs.List = function TabsList({ children }: { children: React.ReactNode }) { ... };
Tabs.Tab = function Tab({ value, children }: TabProps) { ... };
Tabs.Panel = function TabPanel({ value, children }: TabPanelProps) { ... };
```
Use compound components when the Figma design has clearly named sub-components (e.g., Tabs/Tab, Menu/MenuItem, Accordion/AccordionItem).

## Figma MCP Tool Reference

| Tool | When to use |
|------|-------------|
| `figma_get_metadata` | First call — get component name, type, dimensions |
| `figma_get_design_context` | Extract layout, colors, typography, children |
| `figma_get_variable_defs` | Resolve design tokens bound to the node |
| `figma_get_screenshot` | Get visual reference for validation |
| `figma_get_code_connect_map` | Check existing prop mappings |
| `figma_get_code_connect_suggestions` | Get suggested prop mappings for a node |
| `figma_send_code_connect_mappings` | Register new component → Figma mapping |
