---
name: chakraui-components
description: Build UI with Chakra UI v3 components. Use when the user mentions Chakra UI, asks about Chakra components (Button, Dialog, Table, Menu, Tabs, Input, etc.), needs form elements, overlays, navigation, or data display components. Also use when implementing layouts (Flex, Grid, Stack), typography (Text, Heading), or any React component styling with Chakra. Triggers for phrases like "how do I make a dialog", "create a form", "add a menu", "show a table", or when code contains @chakra-ui/react imports.
---

# Chakra UI v3 Components Skill

## Quick Reference

### Component Categories

| Category | Components | Reference |
|----------|------------|-----------|
| **Layout** | Box, Flex, Grid, Stack, Container, Center, AbsoluteCenter, SimpleGrid, Wrap, Bleed, Float | [layout-components.md](references/layout-components.md) |
| **Typography** | Text, Heading, Em, Mark, Highlight, Blockquote, Code, Prose | [typography-components.md](references/typography-components.md) |
| **Forms** | Input, Button, Select, Checkbox, Radio, Slider, Switch, Field, Fieldset, Textarea, Rating, Editable | [form-components.md](references/form-components.md) |
| **Data Display** | Table, Badge, Tag, Avatar, Card, Stat, DataList, List, Status, Progress | [data-components.md](references/data-components.md) |
| **Overlay** | Dialog, Drawer, Popover, Tooltip, Toast | [overlay-components.md](references/overlay-components.md) |
| **Navigation** | Menu, Tabs, Breadcrumb, Pagination, Steps, TreeView | [navigation-components.md](references/navigation-components.md) |
| **Feedback** | Alert, Spinner, Skeleton, Collapsible | [feedback-components.md](references/feedback-components.md) |

### Common Props

Most Chakra UI components share these common props:

| Prop | Values | Description |
|------|--------|-------------|
| `size` | `xs`, `sm`, `md`, `lg`, `xl` | Component size |
| `variant` | `solid`, `outline`, `subtle`, `ghost`, `surface`, `plain` | Visual style |
| `colorPalette` | `gray`, `red`, `green`, `blue`, `teal`, `pink`, `purple`, `cyan`, `orange`, `yellow` | Color theme |
| `disabled` | `boolean` | Disable interaction |
| `loading` | `boolean` | Show loading state |

### Import Patterns

```tsx
// Named imports from @chakra-ui/react
import { Button, Dialog, Table } from "@chakra-ui/react"

// Compound components pattern
import { Dialog } from "@chakra-ui/react"
<Dialog.Root>
  <Dialog.Trigger />
  <Dialog.Content>
    <Dialog.Header>
      <Dialog.Title />
    </Dialog.Header>
    <Dialog.Body />
    <Dialog.Footer />
  </Dialog.Content>
</Dialog.Root>
```

### Compound Component Pattern

Many Chakra UI v3 components use compound components:

```tsx
// Dialog
<Dialog.Root>
  <Dialog.Trigger />
  <Dialog.Backdrop />
  <Dialog.Positioner>
    <Dialog.Content>
      <Dialog.Header>
        <Dialog.Title />
      </Dialog.Header>
      <Dialog.Body />
      <Dialog.Footer />
      <Dialog.CloseTrigger />
    </Dialog.Content>
  </Dialog.Positioner>
</Dialog.Root>

// Table
<Table.Root>
  <Table.Header>
    <Table.Row>
      <Table.ColumnHeader />
    </Table.Row>
  </Table.Header>
  <Table.Body>
    <Table.Row>
      <Table.Cell />
    </Table.Row>
  </Table.Body>
</Table.Root>

// Tabs
<Tabs.Root>
  <Tabs.List>
    <Tabs.Trigger />
  </Tabs.List>
  <Tabs.Content />
</Tabs.Root>
```

### Common Component Patterns

#### Button Variants
```tsx
<Button variant="solid">Solid</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="subtle">Subtle</Button>
<Button colorPalette="blue">Blue Button</Button>
<Button loading>Loading</Button>
```

#### Form Field with Label
```tsx
<Field.Root>
  <Field.Label>Email</Field.Label>
  <Input type="email" />
  <Field.ErrorText>Invalid email</Field.ErrorText>
</Field.Root>
```

#### Card Layout
```tsx
<Card.Root>
  <Card.Header>
    <Heading size="md">Title</Heading>
  </Card.Header>
  <Card.Body>
    <Text>Content</Text>
  </Card.Body>
  <Card.Footer>
    <Button>Action</Button>
  </Card.Footer>
</Card.Root>
```

#### Status Badge
```tsx
<Badge colorPalette={status === 'success' ? 'green' : status === 'error' ? 'red' : 'yellow'}>
  {status}
</Badge>
```

#### Loading Spinner
```tsx
<Spinner size="sm" colorPalette="blue" />
<Spinner size="lg" />
```

### Portal Usage

Overlay components require Portal for proper z-index management:

```tsx
import { Portal } from "@chakra-ui/react"

<Dialog.Root>
  <Dialog.Trigger asChild>
    <Button>Open</Button>
  </Dialog.Trigger>
  <Portal>
    <Dialog.Backdrop />
    <Dialog.Positioner>
      <Dialog.Content>...</Dialog.Content>
    </Dialog.Positioner>
  </Portal>
</Dialog.Root>
```

### asChild Pattern

Use `asChild` to compose with custom elements:

```tsx
// Button as link
<Button asChild>
  <a href="/dashboard">Dashboard</a>
</Button>

// Dialog trigger as custom component
<Dialog.Trigger asChild>
  <IconButton aria-label="Open settings">
    <SettingsIcon />
  </IconButton>
</Dialog.Trigger>
```

## Best Practices

1. **Use compound components** for complex components like Dialog, Table, Tabs
2. **Use Portal** for overlay components to ensure proper stacking context
3. **Use colorPalette** instead of hardcoded colors for themeable components
4. **Use semantic tokens** like `bg.muted`, `fg.subtle` for dark mode support
5. **Provide loading states** for async actions
6. **Use Field.Root** for form inputs with labels and error messages
7. **Use size prop** consistently across components for visual harmony

## Detailed References

- **[layout-components.md](references/layout-components.md)** - Box, Flex, Grid, Stack, Container, Center, AbsoluteCenter, SimpleGrid, Wrap, Bleed, Float
- **[typography-components.md](references/typography-components.md)** - Text, Heading, Em, Mark, Highlight, Blockquote, Code, Prose
- **[form-components.md](references/form-components.md)** - Input, Button, Select, Checkbox, Radio, Slider, Switch, Field, Fieldset, Textarea, Rating, Editable
- **[data-components.md](references/data-components.md)** - Table, Badge, Tag, Avatar, Card, Stat, DataList, List, Status, Progress
- **[overlay-components.md](references/overlay-components.md)** - Dialog, Drawer, Popover, Tooltip, Toast
- **[navigation-components.md](references/navigation-components.md)** - Menu, Tabs, Breadcrumb, Pagination, Steps, TreeView
- **[feedback-components.md](references/feedback-components.md)** - Alert, Spinner, Skeleton, Collapsible

## Full Reference

- **[llms-components.txt](references/llms-components.txt)** - Full reference of all Components without any sacrifices! "very large File 55000+ lines".
