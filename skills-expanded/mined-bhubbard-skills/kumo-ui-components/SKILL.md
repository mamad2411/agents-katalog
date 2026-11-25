---
name: kumo-ui-components
description: Reference guide for all 34+ Kumo UI components (@cloudflare/kumo). Covers import patterns, the Components vs Blocks distinction, and practical recipes for Button, Dialog, Input, Select, Combobox, Table, Toast, and more. Trigger when building React UI with Kumo components.
---

# Kumo UI Components

Kumo UI (`@cloudflare/kumo`) provides 34+ accessible React components built on Base UI primitives. Components handle keyboard navigation, focus management, and ARIA attributes automatically.

---

## 1. Installation

```bash
pnpm add @cloudflare/kumo react react-dom @phosphor-icons/react
```

---

## 2. Components vs Blocks

**Components** — Exported from the package index. Import directly:
```tsx
import { Button, Input, Dialog } from "@cloudflare/kumo";
```

**Blocks** — Large complex patterns NOT exported from the package. Must be scaffolded into your source:
```bash
npx @cloudflare/kumo add PageHeader     # → src/components/kumo/PageHeader.tsx
npx @cloudflare/kumo add ResourceList
npx @cloudflare/kumo add DeleteResource
```

---

## 3. Full Component Catalog

Available via `npx @cloudflare/kumo ls`:

| Component | Import Name | Description |
|---|---|---|
| Accordion | `Accordion` | Expandable content sections |
| Alert | `Alert` | Inline status messages |
| Alert Dialog | `AlertDialog` | Confirmation dialogs requiring explicit user action |
| Autocomplete | `Autocomplete` | Text input with filtered suggestion dropdown |
| Avatar | `Avatar` | User/entity avatar with image or initials fallback |
| Badge | `Badge` | Status indicators, labels, and tags |
| Banner | `Banner` | Page-level status announcements |
| Breadcrumbs | `Breadcrumbs` | Hierarchical navigation trail |
| Button | `Button` | Primary interactive trigger |
| Card | `Card` | Surface container for grouped content |
| Checkbox | `Checkbox` | Binary selection control |
| Clipboard Text | `ClipboardText` | Copyable text with click-to-copy behavior |
| Cloudflare Logo | `CloudflareLogo` | Official Cloudflare brand mark |
| CodeHighlighted | `CodeHighlighted` | Syntax-highlighted code block |
| Collapsible | `Collapsible` | Show/hide content with animation |
| Combobox | `Combobox` | Searchable dropdown with free-text entry |
| Command Palette | `CommandPalette` | Global search + action launcher |
| Date Picker | `DatePicker` | Calendar-based date selection |
| Dialog | `Dialog` | Modal overlay with focus trap |
| Dropdown | `Dropdown` | Contextual action menu |
| Empty | `Empty` | Empty state placeholder with icon + message |
| Flow | `Flow` | Vertical layout with consistent spacing |
| Grid | `Grid` | Responsive grid layout |
| Icon Button | `IconButton` | Icon-only button with accessible label |
| Input | `Input` | Text input field |
| Input Area | `InputArea` | Multi-line textarea |
| Input Group | `InputGroup` | Input with leading/trailing addons |
| Label | `Label` | Form field label |
| Layer Card | `LayerCard` | Elevated card with primary/secondary sections |
| Link | `Link` | Accessible anchor element |
| Loader | `Loader` | Spinner/loading indicator |
| Menu Bar | `MenuBar` | Horizontal application menu |
| Meter | `Meter` | Progress/percentage bar |
| Number Input | `NumberInput` | Numeric input with increment/decrement |
| Pagination | `Pagination` | Page navigation controls |
| Popover | `Popover` | Non-modal overlay anchored to a trigger |
| Radio | `Radio` | Radio button group |
| Search Field | `SearchField` | Search-specific input with clear button |
| Select | `Select` | Dropdown selection control |
| Sensitive Input | `SensitiveInput` | Password-style input with show/hide toggle |
| Sidebar | `Sidebar` | Collapsible side navigation |
| Skeleton Line | `SkeletonLine` | Loading placeholder line |
| Slider | `Slider` | Range slider control |
| Switch | `Switch` | Toggle on/off control |
| Table | `Table` | Data table with sorting support |
| Table of Contents | `TableOfContents` | Auto-generated page anchor nav |
| Tabs | `Tabs` | Tabbed content panels |
| Tag Group | `TagGroup` | Selectable/removable tag set |
| Text | `Text` | Styled text with variant support |
| Toast | `Toast` | Non-blocking notification toasts |
| Toolbar | `Toolbar` | Horizontal action bar |
| Tooltip | `Tooltip` | Hover-triggered contextual info |

---

## 4. Common Component Recipes

### Button

```tsx
import { Button } from "@cloudflare/kumo";

// Variants: "primary" | "secondary" | "danger" | "ghost"
<Button variant="primary" onClick={handleSubmit}>Save Changes</Button>
<Button variant="secondary">Cancel</Button>
<Button variant="danger" onClick={handleDelete}>Delete</Button>
<Button variant="primary" disabled>Loading...</Button>

// With icon (Phosphor Icons)
import { PlusCircle } from "@phosphor-icons/react";
<Button variant="primary" icon={<PlusCircle />}>Add Item</Button>
```

### Input & Form Fields

```tsx
import { Input, Label, InputGroup, InputArea } from "@cloudflare/kumo";

// Basic input
<Label htmlFor="name">Display Name</Label>
<Input id="name" placeholder="Enter name..." value={name} onChange={e => setName(e.target.value)} />

// Input with prefix/suffix
<InputGroup>
  <InputGroup.Prefix>https://</InputGroup.Prefix>
  <Input placeholder="example.com" />
  <InputGroup.Suffix>.workers.dev</InputGroup.Suffix>
</InputGroup>

// Textarea
<InputArea rows={4} placeholder="Enter description..." />
```

### Select

```tsx
import { Select } from "@cloudflare/kumo";

<Select
  value={region}
  onChange={setRegion}
  placeholder="Select region..."
>
  <Select.Option value="us-east">US East</Select.Option>
  <Select.Option value="eu-west">EU West</Select.Option>
  <Select.Option value="ap-south">AP South</Select.Option>
</Select>
```

### Combobox (Searchable Select)

```tsx
import { Combobox } from "@cloudflare/kumo";

<Combobox
  value={selected}
  onChange={setSelected}
  placeholder="Search workers..."
  items={workers.map(w => ({ value: w.id, label: w.name }))}
/>
```

### Dialog (Modal)

```tsx
import { Dialog, Button } from "@cloudflare/kumo";
import { useState } from "react";

export function ConfirmDialog() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <Button variant="primary" onClick={() => setOpen(true)}>Open Dialog</Button>
      <Dialog open={open} onClose={() => setOpen(false)}>
        <Dialog.Title>Confirm Action</Dialog.Title>
        <Dialog.Description>
          This action cannot be undone. Are you sure?
        </Dialog.Description>
        <Dialog.Footer>
          <Button variant="secondary" onClick={() => setOpen(false)}>Cancel</Button>
          <Button variant="danger" onClick={handleConfirm}>Delete</Button>
        </Dialog.Footer>
      </Dialog>
    </>
  );
}
```

> **Tailwind v4 required**: Add `@source "../node_modules/@cloudflare/kumo/dist/**/*";` to your CSS — otherwise Dialogs won't center correctly.

### Table

```tsx
import { Table } from "@cloudflare/kumo";

<Table>
  <Table.Head>
    <Table.Row>
      <Table.Header>Name</Table.Header>
      <Table.Header>Status</Table.Header>
      <Table.Header>Requests</Table.Header>
    </Table.Row>
  </Table.Head>
  <Table.Body>
    {workers.map(worker => (
      <Table.Row key={worker.id}>
        <Table.Cell>{worker.name}</Table.Cell>
        <Table.Cell><Badge variant="success">Active</Badge></Table.Cell>
        <Table.Cell>{worker.requests.toLocaleString()}</Table.Cell>
      </Table.Row>
    ))}
  </Table.Body>
</Table>
```

### Toast Notifications

```tsx
import { Toast, useToast } from "@cloudflare/kumo";

export function App() {
  const { toast } = useToast();

  return (
    <>
      <Button onClick={() => toast({ title: "Saved!", description: "Changes saved successfully.", variant: "success" })}>
        Save
      </Button>
      <Toast.Viewport />
    </>
  );
}
```

### Tabs

```tsx
import { Tabs } from "@cloudflare/kumo";

<Tabs defaultValue="overview">
  <Tabs.List>
    <Tabs.Trigger value="overview">Overview</Tabs.Trigger>
    <Tabs.Trigger value="analytics">Analytics</Tabs.Trigger>
    <Tabs.Trigger value="settings">Settings</Tabs.Trigger>
  </Tabs.List>
  <Tabs.Content value="overview"><OverviewPanel /></Tabs.Content>
  <Tabs.Content value="analytics"><AnalyticsPanel /></Tabs.Content>
  <Tabs.Content value="settings"><SettingsPanel /></Tabs.Content>
</Tabs>
```

---

## 5. Blocks (CLI-Scaffolded)

Blocks are complex UI patterns that you scaffold locally and then modify:

```bash
# List available blocks
npx @cloudflare/kumo ls

# Scaffold into src/components/kumo/
npx @cloudflare/kumo add PageHeader
npx @cloudflare/kumo add ResourceList
npx @cloudflare/kumo add DeleteResource
```

Blocks depend on standard Kumo components and are designed to be customized for your app's specific requirements.

---

## 6. Accessibility (Base UI)

All interactive components wrap Base UI primitives which automatically handle:
- **Keyboard navigation** — Arrow keys, Enter, Space, Escape
- **Focus management** — Focus trapping in Dialogs/Modals, focus return on close
- **ARIA attributes** — `aria-expanded`, `aria-controls`, `role`, `aria-label` applied correctly
- **Screen reader announcements** — Dynamic content changes announced via live regions

You do not need to add these manually. If you override component markup, ensure you preserve the ARIA structure.
