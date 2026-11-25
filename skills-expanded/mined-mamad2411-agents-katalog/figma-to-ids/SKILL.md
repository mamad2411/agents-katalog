---
name: figma-to-ids
description: >
  Translate Figma design properties and structures into IDS (Iress Design System)
  component implementations. Use when the user provides Figma designs, mentions
  Figma MCP, asks to convert a design to code, or references Figma component
  names, variants, or auto-layout properties.
license: Apache-2.0
compatibility: React 18+, TypeScript, @iress-oss/ids-components@beta
metadata:
  author: iress
  version: "1.0"
---

# Skill: Figma to IDS Translation

## Purpose

Translate Figma design properties and structures into IDS (Iress Design System) component implementations. This skill helps AI agents interpret Figma design metadata (from tools like Figma MCP or exported design specs) and produce accurate IDS code.

## Figma MCP Setup

AI agents need a Figma MCP server to read Figma files directly. Without one, you can still use this skill by pasting exported design specs or Figma component descriptions manually.

### Setup

1. **Get a Figma personal access token** — In Figma, go to *Settings → Account → Personal access tokens* and create a token with **File content (Read-only)** scope.

2. **Add the MCP server to your agent config.** The exact location depends on your tool:

   | Tool | Config file |
   | --- | --- |
   | **Kiro CLI** | `~/.kiro/settings/mcp.json` (global) or `.kiro/settings/mcp.json` (workspace) |
   | **Cursor** | `.cursor/mcp.json` |
   | **Claude Code** | `.claude/mcp.json` or `~/.claude/mcp.json` |
   | **VS Code (GitHub Copilot)** | `.vscode/mcp.json` |

   Example configuration (using the community [`figma-developer-mcp`](https://github.com/nicholasgriffintn/figma-developer-mcp) server):

   ```json
   {
     "mcpServers": {
       "Figma": {
         "command": "npx",
         "args": ["-y", "figma-developer-mcp", "--stdio"],
         "env": {
           "FIGMA_API_KEY": "<your-figma-token>"
         }
       }
     }
   }
   ```

   For Kiro CLI, you can also add it via the command line:

   ```bash
   kiro-cli mcp add --name Figma --command npx --args "-y figma-developer-mcp --stdio" --env "FIGMA_API_KEY=<your-figma-token>"
   ```

3. **Verify** — Ask your agent to fetch data from a Figma file URL. It should return frame and component information.

## Process

1. **Analyse Figma structure** — Identify frames, auto-layout, and component instances
2. **Map components** — Match Figma component names/variants to IDS components
3. **Extract tokens** — Convert Figma design values to IDS design token references
4. **Generate code** — Produce clean, minimal React/TypeScript with proper IDS imports. Use the fewest components possible — check whether parent components already handle layout before adding `IressInline`/`IressStack` wrappers. Never wrap a single child in a layout component.
5. **Verify output** — Check that all imports resolve, no raw HTML is used where IDS components exist, grid layouts use responsive `span` values, and no common anti-patterns are present (disabled buttons, slot attributes, redundant textStyle)

> **Important:** IDS v6 is currently in beta. Install with the `@beta` tag:
>
> ```bash
> npm install @iress-oss/ids-components@beta
> npm install @iress-oss/ids-tokens@beta  # if using tokens directly (e.g. cssVars or CSS vars import)
> ```

## Figma → IDS Mapping

When mapping Figma components to IDS, read [references/component-mapping.md](references/component-mapping.md) for the full Figma component → IDS component mapping table.

When converting Figma design values (colours, spacing, radius, typography) to IDS tokens, read [references/token-mapping.md](references/token-mapping.md).

For neutral text colours, treat `colour.neutral.90` as a backwards-compatible
alias of `colour.neutral.80` (both resolve to `#141F4D`). Prefer
`colour.neutral.80` in new IDS implementations, but handle either token name
when translating older Figma files.

## Translation Examples

### Figma: Login Form Frame

**Figma structure:**

- Frame: Auto-layout vertical, gap 16px, padding 24px
  - Text: "Log In" (Heading H2)
  - Input: "Email" (Text Input)
  - Input: "Password" (Password Input)
  - Button: "Sign in" (Primary)
  - Text: "Forgot password?" (Link)

**IDS implementation:**

```tsx
import {
  IressStack,
  IressText,
  IressField,
  IressInput,
  IressButton,
  IressLink,
  IressCard,
} from '@iress-oss/ids-components';

function LoginForm() {
  return (
    <IressCard p="lg">
      <IressStack gap="md">
        <IressText element="h2">Log In</IressText>
        <IressField label="Email" htmlFor="email" required>
          <IressInput id="email" type="email" />
        </IressField>
        <IressField label="Password" htmlFor="password" required>
          <IressInput id="password" type="password" />
        </IressField>
        <IressButton mode="primary" type="submit">
          Sign in
        </IressButton>
        <IressLink href="/forgot-password">Forgot password?</IressLink>
      </IressStack>
    </IressCard>
  );
}
```

### Figma: Alert Banner

**Figma structure:**

- Frame: Fill `#EBF9F5`, border-radius 12px, padding 16px
  - Auto-layout horizontal, gap 8px
  - Icon: "check_circle"
  - Text: "Your changes have been saved" (Body MD)

**IDS implementation:**

```tsx
import { IressAlert } from '@iress-oss/ids-components';

// IressAlert already handles the layout, icon, and styling
<IressAlert status="success">Your changes have been saved</IressAlert>;
```

> **Key insight:** IDS components encapsulate their styling. Don't recreate layout/colours from Figma — use the component's props (like `status`) and let IDS handle the visual treatment.

### Figma: Status Modal (Danger Confirmation)

**Figma structure:**

- Modal frame with danger icon in header
  - Heading: "Delete record?"
  - Body text: "This action cannot be undone."
  - Footer: Two buttons (Cancel, Delete)

**IDS implementation:**

```tsx
import { IressModal } from '@iress-oss/ids-components';

// Status modals use the `status` prop — the icon, colours, and button status are handled automatically.
// Use `actions` instead of `footer` for opinionated action buttons.
<IressModal
  status="danger"
  heading="Delete record?"
  actions={[{ children: 'Cancel', mode: 'tertiary' }, { children: 'Delete' }]}
  show={isOpen}
  onShowChange={setIsOpen}
>
  This action cannot be undone.
</IressModal>;
```

> **Key insight:** When `status` is set on `IressModal`, the `footer` prop is not available — use `actions` instead. Each action button automatically inherits the modal's status. Size is restricted to `sm` (default) or `md`.

### Figma: Data Table

**Figma structure:**

- Frame: Table with header row and data rows
  - Header: ["Name", "Email", "Status", "Actions"]
  - Rows: data with tag in Status column, button in Actions

**IDS implementation:**

```tsx
import { IressTable, IressTag, IressButton } from '@iress-oss/ids-components';
import type { TableColumn } from '@iress-oss/ids-components';

interface User {
  name: string;
  email: string;
  status: string;
  id: string;
}

const columns: TableColumn<User>[] = [
  { key: 'name', label: 'Name' },
  { key: 'email', label: 'Email' },
  {
    key: 'status',
    label: 'Status',
    format: (value) => <IressTag>{value}</IressTag>,
  },
  {
    key: 'actions',
    label: 'Actions',
    format: (_, row) => (
      <IressButton mode="tertiary" icon="edit">
        Edit
      </IressButton>
    ),
  },
];

function UsersTable({ users }: { users: User[] }) {
  return <IressTable caption="Users" rows={users} columns={columns} />;
}
```

> **Key insight:** `IressTable` is data-driven — pass `rows` and `columns` props instead of composing sub-components. Use the `format` function on columns to render custom cell content like tags or buttons.

## Responsive Layout

**Always produce responsive output**, even when Figma only provides a single desktop frame. IDS uses a 12-column grid with 6 breakpoints — every translation should consider how the layout adapts to smaller screens.

### Responsive Design Principles

When no mobile Figma frames are provided, apply these principles:

1. **Identify the primary task** — Determine what the user is trying to accomplish on the page (e.g. filling a form, reviewing data, making a decision). The mobile layout should prioritise this task.
2. **Stack multi-column layouts** — Any side-by-side columns should stack to full-width (`span={{ xs: 12, md: ... }}`) on mobile.
3. **Relocate secondary content** — Move supplementary UI (filters, sidebars, secondary actions, metadata panels) into an `IressSlideout` or collapsible section on mobile so the primary task remains front and centre.
4. **Simplify dense layouts** — Tables with many columns, multi-panel dashboards, and wide forms should adapt: hide non-essential columns with `hideBelow`, collapse sections, or switch to a card-based layout on mobile using `useBreakpoint`.
5. **Preserve all functionality** — Never remove features on mobile. Use `IressSlideout`, `IressModal`, expandable sections, or `IressTabSet` to keep functionality accessible without cluttering the mobile view.

### Breakpoints

| Breakpoint | Screen width    |
| ---------- | --------------- |
| `xs`       | 0 – 575px       |
| `sm`       | 576px – 767px   |
| `md`       | 768px – 1023px  |
| `lg`       | 1024px – 1279px |
| `xl`       | 1280px – 1599px |
| `xxl`      | 1600px+         |

### Responsive Props

Many props accept a `ResponsiveProp` — either a single value or an object keyed by breakpoint:

```tsx
// Single value (all breakpoints)
<IressCol span={6} />

// Responsive — full-width on mobile, half on medium+
<IressCol span={{ xs: 12, md: 6 }} />
```

Props that support responsive values: `span`, `offset`, `gap`, `gutter`, `rowGap`, `p`, `px`, `py`, `pt`, `pr`, `pb`, `pl`, `m`, `mx`, `my`, `mt`, `mr`, `mb`, `ml`, `width`, `srOnly`, `hideFrom`, `hideBelow`.

### Figma Multi-Viewport → Responsive Columns

When Figma provides separate mobile and desktop frames for the same layout:

**Figma mobile (xs):** Single column stack
**Figma desktop (md+):** Two-column sidebar layout

```tsx
<IressRow gutter={{ xs: 'sm', md: 'lg' }}>
  <IressCol span={{ xs: 12, md: 4 }}>
    <Sidebar />
  </IressCol>
  <IressCol span={{ xs: 12, md: 8 }}>
    <MainContent />
  </IressCol>
</IressRow>
```

### Figma Desktop-Only → Inferred Responsive Layout

When Figma only provides a desktop frame with a sidebar + main content area, infer the mobile layout:

```tsx
import { useState } from 'react';
import {
  useBreakpoint,
  IressSlideout,
  IressButton,
  IressStack,
  IressRow,
  IressCol,
} from '@iress-oss/ids-components';

function Page() {
  const { breakpoint } = useBreakpoint();
  const isMobile = breakpoint === 'xs' || breakpoint === 'sm';
  const [filtersOpen, setFiltersOpen] = useState(false);

  return (
    <>
      {isMobile ? (
        // Mobile: primary content first, secondary content in slideout
        <IressStack gap="md">
          <IressButton
            mode="secondary"
            icon="filter_list"
            onClick={() => setFiltersOpen(true)}
          >
            Filters
          </IressButton>
          <MainContent />
          <IressSlideout
            heading="Filters"
            show={filtersOpen}
            onShowChange={setFiltersOpen}
          >
            <FilterPanel />
          </IressSlideout>
        </IressStack>
      ) : (
        // Desktop: side-by-side layout as designed in Figma
        <IressRow gutter="lg">
          <IressCol span={3}>
            <FilterPanel />
          </IressCol>
          <IressCol span={9}>
            <MainContent />
          </IressCol>
        </IressRow>
      )}
    </>
  );
}
```

### Responsive Visibility

Use `hideFrom`/`hideBelow` CSS props directly on any component:

```tsx
<IressButton hideBelow="md">Desktop action</IressButton>
<IressText hideFrom="lg">Mobile only text</IressText>
```

For conditional rendering based on breakpoint (e.g. rendering entirely different components), use the `useBreakpoint` hook:

```tsx
import { useBreakpoint } from '@iress-oss/ids-components';

function Navigation() {
  const { breakpoint } = useBreakpoint();
  const isMobile = breakpoint === 'xs' || breakpoint === 'sm';

  return isMobile ? <MobileNav /> : <DesktopNav />;
}
```

## Best Practices

1. **Minimise component nesting** — Use the fewest components possible. Every wrapper must earn its place. Before adding `IressInline` or `IressStack`, check whether the parent already handles layout (e.g. `IressCard` has `heading` and `footer` props; `IressModal` has `actions`; `IressButtonGroup` handles horizontal button layout). Don't wrap a single child in a layout component.
2. **Use IDS components, not raw elements** — IDS components encapsulate correct spacing, colours, border radius, and accessibility
3. **Don't recreate component internals** — If Figma shows a button with specific padding/radius, use `IressButton` with the right `mode` — the styling is built in
4. **Map Figma gap/padding to spacing tokens** — Divide pixel value by 4 to get the token number, then use the full token: 16px → `"spacing.4"`, 24px → `"spacing.6"`. Alias tokens (`"xs"`, `"sm"`, `"md"`, `"lg"`, `"xl"`) are also valid. Never use bare numbers like `gap="4"`.
5. **Prefer semantic props over manual styling** — Use `status="danger"` instead of `bg="colour.system.danger.fill"`
6. **Use IressField for all form inputs** — It provides the label, hint, and validation layout
7. **Respect responsive patterns** — Use `hideFrom`/`hideBelow` props or the `useBreakpoint` hook for responsive visibility; use responsive `span` on `IressCol` for adaptive grid layouts
8. **Always make grid layouts responsive** — When translating Figma multi-column layouts, use responsive `span` values (e.g. `span={{ xs: 12, md: 6 }}`) so columns stack on mobile
9. **Check the component docs** — Read the specific component doc for detailed props and patterns (`node_modules/@iress-oss/ids-components/.ai/components/`)

## Common Mistakes

### Unnecessary layout wrappers

Don't add `IressInline` or `IressStack` when it adds no value. Every Figma auto-layout frame does NOT need its own layout wrapper — check the IDS component first.

```tsx
// ❌ Unnecessary nesting — IressStack wrapping a single child
<IressStack gap="md">
  <IressInline gap="sm">
    <IressButton mode="primary">Save</IressButton>
    <IressButton mode="secondary">Cancel</IressButton>
  </IressInline>
</IressStack>

// ✅ Single group of buttons only needs IressInline
<IressInline gap="sm">
  <IressButton mode="primary">Save</IressButton>
  <IressButton mode="secondary">Cancel</IressButton>
</IressInline>
```

**Rule of thumb:** When Figma shows an auto-layout frame, check if the corresponding IDS component already provides that layout before adding a wrapper. Components like `IressModal` (with `actions`) and `IressButtonGroup` already handle their internal layout. For `IressCard`, use the `heading` and `footer` props to structure content — but note the `footer` slot does not auto-layout its children, so use `IressInline` inside `footer` when you need horizontal button layout.

### Other common anti-patterns

For the full list of common anti-patterns (disabled buttons, redundant textStyle, legacy slot attributes, raw HTML, hardcoded values), read the Common Mistakes guide at `node_modules/@iress-oss/ids-components/.ai/guides/foundations-common-mistakes.md` (requires `@iress-oss/ids-components` to be installed).

**Figma-specific addition:** When Figma shows named content areas ("prepend", "append", "footer"), map them to the corresponding **React prop**, not to a `slot` attribute. When Figma shows a greyed-out or disabled button state, do not use `disabled` — see the guide for alternatives.
