---
name: jem-ui-components
description: Complete reference for using @jem-open/jem-ui components — props, variants, design tokens, setup, and common mistakes to avoid.
---

# jem-ui-components

Complete reference for AI agents consuming `@jem-open/jem-ui` in application projects. Covers every component's props, variants, and design tokens so you use the library correctly instead of recreating what already exists.

## Step 1 — Check prerequisites

Verify the consuming project is set up to use jem-ui.

**Check 1: Package installed**

Look for `@jem-open/jem-ui` in `package.json` dependencies or devDependencies.

If not found, install it:

```bash
npm install @jem-open/jem-ui
```

Peer dependencies required: `react@^18 | ^19`, `react-dom@^18 | ^19`, `tailwindcss@^3.4`.

**Check 2: Styles imported**

The app entry point (e.g. `layout.tsx`, `_app.tsx`, or `main.tsx`) must import jem-ui styles:

```typescript
import "@jem-open/jem-ui/styles.css"
```

If missing, add it.

**Check 3: Tailwind preset configured**

`tailwind.config.js` (or `.ts`) must include the jem-ui preset and content path:

```javascript
const jemPreset = require("@jem-open/jem-ui/tailwind-preset");

module.exports = {
  presets: [jemPreset],
  content: [
    "./src/**/*.{ts,tsx}",
    "./node_modules/@jem-open/jem-ui/dist/**/*.{js,mjs}",
  ],
};
```

If missing, add both the preset and the content path.

**Halt** if any check fails and cannot be auto-fixed.

---

## Step 2 — Identify needed components

Before writing any UI code, scan this catalog to find existing components that match your needs. Do not recreate components that already exist in the library.

All components are imported from `@jem-open/jem-ui`:

```typescript
import { ComponentName } from "@jem-open/jem-ui"
```

### Forms

| Component | Description |
|---|---|
| `Button` | Primary action button with 9 variants (default, primary, secondary, destructive, approve, outline, subtle, ghost, link), loading state, and icon slots |
| `IconButton` | Icon-only button with square/circle shapes |
| `Input` | Base text input |
| `InputField` | Input with label, description, helper text, and error state |
| `SearchInput` | Search input with built-in clear button |
| `Checkbox` | Standalone checkbox |
| `CheckboxWithLabel` | Checkbox with label and optional description |
| `CheckboxCard` | Card-style checkbox with label and description |
| `RadioGroup`, `RadioGroupItem` | Radio button group with items |
| `RadioGroupItemWithLabel` | Radio item with label and optional description |
| `RadioGroupCard` | Card-style radio item |
| `Select`, `SelectTrigger`, `SelectContent`, `SelectItem`, `SelectValue` | Composable dropdown select |
| `SelectField` | Select wrapper with label and description |
| `DatePicker` | Single date picker with calendar popover |
| `DateRangePicker` | Date range picker with two-month calendar |
| `Calendar` | Standalone calendar component |
| `Textarea` | Multi-line text input |
| `TextareaField` | Textarea with label, description, helper text, and error state |
| `Switch` | Toggle switch |
| `SwitchWithLabel` | Switch with label and optional description |
| `Label` | Form label (Radix-based, associates with inputs) |
| `Upload` | File upload with progress states (default, uploading, uploaded) |

### Navigation

| Component | Description |
|---|---|
| `Accordion`, `AccordionItem`, `AccordionTrigger`, `AccordionContent` | Collapsible content sections |
| `Tabs`, `TabsList`, `TabsTrigger`, `TabsContent` | Tabbed content with default and line variants |
| `Breadcrumb`, `BreadcrumbList`, `BreadcrumbItem`, `BreadcrumbLink`, `BreadcrumbPage`, `BreadcrumbSeparator` | Navigation breadcrumbs with chevron/slash separator |
| `Pagination`, `PaginationContent`, `PaginationItem`, `PaginationLink`, `PaginationPrevious`, `PaginationNext`, `PaginationEllipsis` | Page navigation controls |
| `Link` | Styled anchor with variant (default, muted) and size (xs, sm, base) options |

### Data Display

| Component | Description |
|---|---|
| `DataTable`, `DataTableColumnHeader` | Full-featured data table with TanStack Table integration, sorting, filtering, pagination |
| `Table`, `TableHeader`, `TableBody`, `TableRow`, `TableHead`, `TableCell`, `TableCaption`, `TableFooter` | Primitive table building blocks |
| `Tag` | Status tag with 13 variants (default, success, processing, pending, failed, drafted, outline, outline-navy, neutral, pink, pink-text, lime, purple) |
| `DismissibleTag` | Tag with dismiss (X) button |
| `CountTag` | Small count badge (pink circle with white number) |
| `Avatar`, `AvatarImage`, `AvatarFallback` | User avatar with image and fallback |
| `AvatarBadge` | Online/status indicator badge for Avatar |
| `AvatarGroup`, `AvatarGroupCount` | Stacked avatar group with overflow count |
| `Progress` | Progress bar |
| `Divider` | Horizontal/vertical separator with label option and 5 style variants |
| `Skeleton` | Loading placeholder with pulse animation |

### Feedback

| Component | Description |
|---|---|
| `Dialog`, `DialogTrigger`, `DialogContent`, `DialogHeader`, `DialogTitle`, `DialogDescription`, `DialogFooter`, `DialogClose` | Modal dialog with close button |
| `Drawer`, `DrawerTrigger`, `DrawerContent`, `DrawerHeader`, `DrawerBody`, `DrawerSection`, `DrawerFooter`, `DrawerTitle`, `DrawerClose` | Side drawer panel (right/left/top/bottom) |
| `DropdownMenu`, `DropdownMenuTrigger`, `DropdownMenuContent`, `DropdownMenuItem`, `DropdownMenuSeparator` | Context/action dropdown menu |
| `DropdownMenuCheckboxItem`, `DropdownMenuRadioGroup`, `DropdownMenuRadioItem` | Selection items within dropdown |
| `DropdownMenuSub`, `DropdownMenuSubTrigger`, `DropdownMenuSubContent` | Nested sub-menus |
| `Tooltip`, `TooltipProvider`, `TooltipTrigger`, `TooltipContent` | Hover tooltip with dark/light variants |
| `Popover`, `PopoverTrigger`, `PopoverContent` | Click-triggered popover |
| `Alert`, `AlertTitle`, `AlertDescription` | Alert message with 5 variants (default, success, warning, destructive, note) and auto icons |
| `EmptyState` | Empty state placeholder with icon, title, description, and action buttons |
| `EmptyStateNotFound`, `EmptyStateNoResults`, `EmptyStateNoData` | Pre-configured empty state variants |
| `Toaster` | Toast notifications — add once in root layout, trigger with `toast()` from sonner |

### Design Tokens

| Component | Description |
|---|---|
| `Icon` | Sized icon wrapper (xs/sm/md/lg/xl) for Lucide icons with accessibility label |
| `PrimaryLogo` | Primary JEM logo with 4 variant/color options and 4 sizes |
| `SecondaryLogoRound` | Round secondary logo with 2 variants and 4 sizes |
| `SecondaryLogoSquare` | Square secondary logo with 2 variants and 4 sizes |

### Utilities

| Export | Description |
|---|---|
| `cn` | Class name merger (clsx + tailwind-merge). **Use this for ALL class composition.** Never use template literals to combine Tailwind classes. |

---

## Step 3 — Use components correctly

Detailed reference for each component. Organized by category.

### Forms

#### Button

```typescript
import { Button } from "@jem-open/jem-ui"
```

**Props:** extends `React.ComponentProps<"button">`

| Prop | Type | Default | Description |
|---|---|---|---|
| `variant` | `"default" \| "primary" \| "secondary" \| "destructive" \| "approve" \| "outline" \| "subtle" \| "ghost" \| "link"` | `"default"` | Visual style |
| `size` | `"default" \| "xs" \| "sm" \| "small" \| "medium" \| "lg" \| "large" \| "icon" \| "icon-xs" \| "icon-sm" \| "icon-lg"` | `"default"` | Button size |
| `leftIcon` | `React.ReactNode` | — | Icon before label |
| `rightIcon` | `React.ReactNode` | — | Icon after label |
| `loading` | `boolean` | `false` | Shows loading spinner, disables button |
| `asChild` | `boolean` | `false` | Render as child element (use with links) |

**Example:**

```tsx
<Button variant="primary" size="medium" leftIcon={<Plus />}>
  Add item
</Button>
```

**asChild example (Button as link):**

```tsx
<Button asChild variant="outline">
  <a href="/settings">Settings</a>
</Button>
```

#### IconButton

```typescript
import { IconButton } from "@jem-open/jem-ui"
```

**Props:** extends `React.ComponentProps<"button">`

| Prop | Type | Default | Description |
|---|---|---|---|
| `size` | `"default" \| "small" \| "medium" \| "large"` | `"default"` | Button size |
| `shape` | `"square" \| "circle"` | `"square"` | Button shape |
| `icon` | `React.ReactNode` | — | Icon to display |

**Example:**

```tsx
<IconButton icon={<Trash2 />} shape="circle" aria-label="Delete item" />
```

Note: Always provide `aria-label` for accessibility since there is no visible text.

#### Input

```typescript
import { Input } from "@jem-open/jem-ui"
```

**Props:** extends `React.ComponentProps<"input">`

No additional props beyond standard HTML input attributes.

**Example:**

```tsx
<Input type="email" placeholder="Enter email" />
```

#### InputField

```typescript
import { InputField } from "@jem-open/jem-ui"
```

**Props:** extends Input props

| Prop | Type | Default | Description |
|---|---|---|---|
| `label` | `string` | — | Label text above input |
| `description` | `string` | — | Description below label |
| `helperText` | `string` | — | Helper text below input |
| `error` | `boolean` | `false` | Error state (red border, helper text turns red) |
| `icon` | `React.ReactNode` | — | Icon inside input |
| `button` | `React.ReactNode` | — | Button element inside input |

**Example:**

```tsx
<InputField
  label="Email"
  description="We'll never share your email"
  helperText={errors.email}
  error={!!errors.email}
  type="email"
  placeholder="name@example.com"
/>
```

#### SearchInput

```typescript
import { SearchInput } from "@jem-open/jem-ui"
```

**Props:** extends Input props

| Prop | Type | Default | Description |
|---|---|---|---|
| `onClear` | `() => void` | — | Called when clear (X) button is clicked |

Shows a search icon on the left and a clear (X) button when there is a value.

**Example:**

```tsx
const [query, setQuery] = useState("")

<SearchInput
  value={query}
  onChange={(e) => setQuery(e.target.value)}
  onClear={() => setQuery("")}
  placeholder="Search..."
/>
```

#### Checkbox

```typescript
import { Checkbox } from "@jem-open/jem-ui"
```

**Props:** extends `React.ComponentProps<typeof CheckboxPrimitive.Root>` (Radix)

Standard Radix checkbox props: `checked`, `onCheckedChange`, `disabled`, `name`, `value`.

**Example:**

```tsx
<Checkbox checked={agreed} onCheckedChange={setAgreed} />
```

#### CheckboxWithLabel

```typescript
import { CheckboxWithLabel } from "@jem-open/jem-ui"
```

| Prop | Type | Default | Description |
|---|---|---|---|
| `label` | `string` | required | Label text |
| `description` | `string` | — | Description below label |

Plus all Checkbox props.

**Example:**

```tsx
<CheckboxWithLabel
  label="Accept terms"
  description="You agree to our terms of service"
  checked={agreed}
  onCheckedChange={setAgreed}
/>
```

#### CheckboxCard

```typescript
import { CheckboxCard } from "@jem-open/jem-ui"
```

Same props as CheckboxWithLabel but renders as a card-style container.

**Example:**

```tsx
<CheckboxCard
  label="Email notifications"
  description="Receive email updates about your account"
  checked={emailNotifs}
  onCheckedChange={setEmailNotifs}
/>
```

#### RadioGroup / RadioGroupItem

```typescript
import { RadioGroup, RadioGroupItem } from "@jem-open/jem-ui"
```

**RadioGroup props:** extends `React.ComponentProps<typeof RadioGroupPrimitive.Root>` (Radix)
- `value`, `onValueChange`, `disabled`, `name`
- Layout: grid with gap-3

**RadioGroupItem props:** extends Radix RadioGroup.Item
- `value` (required)

**Example:**

```tsx
<RadioGroup value={plan} onValueChange={setPlan}>
  <RadioGroupItem value="free" />
  <RadioGroupItem value="pro" />
  <RadioGroupItem value="enterprise" />
</RadioGroup>
```

Also available: `RadioGroupItemWithLabel` (adds `label` and `description` props) and `RadioGroupCard` (card-style).

**RadioGroupItemWithLabel example:**

```tsx
<RadioGroup value={plan} onValueChange={setPlan}>
  <RadioGroupItemWithLabel value="free" label="Free" description="Basic features" />
  <RadioGroupItemWithLabel value="pro" label="Pro" description="All features" />
</RadioGroup>
```

#### Select (compound)

```typescript
import {
  Select, SelectTrigger, SelectContent, SelectItem, SelectValue
} from "@jem-open/jem-ui"
```

Composable compound component. Must be assembled from parts:

**Example:**

```tsx
<Select value={role} onValueChange={setRole}>
  <SelectTrigger>
    <SelectValue placeholder="Select role" />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="admin">Admin</SelectItem>
    <SelectItem value="editor">Editor</SelectItem>
    <SelectItem value="viewer">Viewer</SelectItem>
  </SelectContent>
</Select>
```

Also available: `SelectField` wraps Select with `label` and `description`:

```tsx
<SelectField label="Role" description="User's permission level">
  <Select value={role} onValueChange={setRole}>
    {/* ... same inner content */}
  </Select>
</SelectField>
```

Additional parts: `SelectGroup`, `SelectLabel`, `SelectSeparator`, `SelectScrollUpButton`, `SelectScrollDownButton`.

#### DatePicker

```typescript
import { DatePicker } from "@jem-open/jem-ui"
```

| Prop | Type | Default | Description |
|---|---|---|---|
| `date` | `Date` | — | Selected date |
| `onDateChange` | `(date: Date \| undefined) => void` | — | Date change handler |
| `placeholder` | `string` | — | Placeholder text |
| `disabled` | `boolean` | `false` | Disabled state |
| `label` | `string` | — | Label above picker |

**Example:**

```tsx
<DatePicker
  label="Start date"
  date={startDate}
  onDateChange={setStartDate}
  placeholder="Pick a date"
/>
```

#### DateRangePicker

```typescript
import { DateRangePicker } from "@jem-open/jem-ui"
```

| Prop | Type | Default | Description |
|---|---|---|---|
| `dateRange` | `DateRange` | — | Selected range `{ from?: Date, to?: Date }` |
| `onDateRangeChange` | `(range: DateRange \| undefined) => void` | — | Range change handler |
| `placeholder` | `string` | — | Placeholder text |
| `disabled` | `boolean` | `false` | Disabled state |
| `label` | `string` | — | Label above picker |

Shows 2 months side by side. Format: "LLL dd, y" (e.g. "Mar 09, 2026").

**Example:**

```tsx
<DateRangePicker
  label="Date range"
  dateRange={range}
  onDateRangeChange={setRange}
  placeholder="Select range"
/>
```

#### Calendar

```typescript
import { Calendar } from "@jem-open/jem-ui"
```

Standalone calendar component. Props extend React DayPicker. Usually used inside DatePicker — use DatePicker instead unless you need a custom calendar layout.

**Example:**

```tsx
<Calendar mode="single" selected={date} onSelect={setDate} />
```

#### Textarea / TextareaField

```typescript
import { Textarea } from "@jem-open/jem-ui"
```

**Textarea props:** extends `React.ComponentProps<"textarea">`. Min height: 115px. Resize disabled.

**TextareaField** adds form wrapper props:

| Prop | Type | Default | Description |
|---|---|---|---|
| `label` | `string` | — | Label text |
| `description` | `string` | — | Description below label |
| `helperText` | `string` | — | Helper text below textarea |
| `error` | `boolean` | `false` | Error state |

**Example:**

```tsx
<TextareaField
  label="Notes"
  helperText="Max 500 characters"
  placeholder="Enter your notes..."
/>
```

#### Switch / SwitchWithLabel

```typescript
import { Switch } from "@jem-open/jem-ui"
```

**Switch props:** extends Radix Switch. Key props: `checked`, `onCheckedChange`, `disabled`.

Checked: pink-900 background. Unchecked: slate-200.

**SwitchWithLabel** adds `label` and `description` props:

```tsx
<SwitchWithLabel
  label="Dark mode"
  description="Use dark theme across the app"
  checked={darkMode}
  onCheckedChange={setDarkMode}
/>
```

#### Label

```typescript
import { Label } from "@jem-open/jem-ui"
```

Radix-based label that properly associates with form inputs via `htmlFor`.

**Example:**

```tsx
<Label htmlFor="email">Email address</Label>
<Input id="email" type="email" />
```

Note: `InputField`, `TextareaField`, `SelectField`, `CheckboxWithLabel`, and `SwitchWithLabel` handle labeling automatically. Use `Label` only when building custom form layouts.

#### Upload

```typescript
import { Upload } from "@jem-open/jem-ui"
```

| Prop | Type | Default | Description |
|---|---|---|---|
| `state` | `"default" \| "uploading" \| "uploaded"` | `"default"` | Current upload state |
| `progress` | `number` | — | Upload progress (0-100), shown during "uploading" |
| `fileName` | `string` | — | Name of uploaded file |
| `title` | `string` | — | Title text in upload area |
| `description` | `string` | — | Description text in upload area |
| `maxSize` | `string` | — | Max file size text (e.g. "10MB") |
| `onSelectFile` | `() => void` | — | Called when user clicks to select file |
| `onRemoveFile` | `() => void` | — | Called when user removes uploaded file |
| `onSubmit` | `() => void` | — | Called when user submits uploaded file |

**Example:**

```tsx
<Upload
  state={uploadState}
  progress={uploadProgress}
  fileName={file?.name}
  title="Upload document"
  description="PDF, DOC, or DOCX"
  maxSize="10MB"
  onSelectFile={handleSelectFile}
  onRemoveFile={handleRemoveFile}
  onSubmit={handleSubmit}
/>
```

### Navigation

#### Accordion (compound)

```typescript
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from "@jem-open/jem-ui"
```

**Accordion props:** extends Radix Accordion.Root. Key props: `type` ("single" | "multiple"), `collapsible`, `value`, `onValueChange`.

**Example:**

```tsx
<Accordion type="single" collapsible>
  <AccordionItem value="item-1">
    <AccordionTrigger>Section 1</AccordionTrigger>
    <AccordionContent>Content for section 1</AccordionContent>
  </AccordionItem>
  <AccordionItem value="item-2">
    <AccordionTrigger>Section 2</AccordionTrigger>
    <AccordionContent>Content for section 2</AccordionContent>
  </AccordionItem>
</Accordion>
```

Trigger text turns pink on hover and when open. ChevronDown icon rotates.

#### Tabs (compound)

```typescript
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@jem-open/jem-ui"
```

**TabsList variants:**

| Variant | Description |
|---|---|
| `default` | Pink-100 background, white active tab |
| `line` | Border-bottom style, no background |

**TabsTrigger variants:** matches TabsList — use `variant="line"` on both for line style.

**Example (default):**

```tsx
<Tabs defaultValue="general">
  <TabsList>
    <TabsTrigger value="general">General</TabsTrigger>
    <TabsTrigger value="security">Security</TabsTrigger>
  </TabsList>
  <TabsContent value="general">General settings</TabsContent>
  <TabsContent value="security">Security settings</TabsContent>
</Tabs>
```

**Example (line variant):**

```tsx
<Tabs defaultValue="overview">
  <TabsList variant="line">
    <TabsTrigger variant="line" value="overview">Overview</TabsTrigger>
    <TabsTrigger variant="line" value="details">Details</TabsTrigger>
  </TabsList>
  <TabsContent value="overview">Overview content</TabsContent>
  <TabsContent value="details">Details content</TabsContent>
</Tabs>
```

#### Breadcrumb (compound)

```typescript
import {
  Breadcrumb, BreadcrumbList, BreadcrumbItem, BreadcrumbLink,
  BreadcrumbPage, BreadcrumbSeparator
} from "@jem-open/jem-ui"
```

**BreadcrumbSeparator** accepts `variant`: `"chevron"` (default) or `"slash"`.

**BreadcrumbLink** supports `asChild` for use with router links.

**Example:**

```tsx
<Breadcrumb>
  <BreadcrumbList>
    <BreadcrumbItem>
      <BreadcrumbLink href="/">Home</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbLink href="/settings">Settings</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbPage>Profile</BreadcrumbPage>
    </BreadcrumbItem>
  </BreadcrumbList>
</Breadcrumb>
```

#### Pagination (compound)

```typescript
import {
  Pagination, PaginationContent, PaginationItem,
  PaginationLink, PaginationPrevious, PaginationNext, PaginationEllipsis
} from "@jem-open/jem-ui"
```

**PaginationLink** props: `isActive` (boolean) — active page gets outline variant with border. `size` from Button.

**Example:**

```tsx
<Pagination>
  <PaginationContent>
    <PaginationItem>
      <PaginationPrevious href="#" />
    </PaginationItem>
    <PaginationItem>
      <PaginationLink href="#" isActive>1</PaginationLink>
    </PaginationItem>
    <PaginationItem>
      <PaginationLink href="#">2</PaginationLink>
    </PaginationItem>
    <PaginationItem>
      <PaginationEllipsis />
    </PaginationItem>
    <PaginationItem>
      <PaginationNext href="#" />
    </PaginationItem>
  </PaginationContent>
</Pagination>
```

#### Link

```typescript
import { Link } from "@jem-open/jem-ui"
```

| Prop | Type | Default | Description |
|---|---|---|---|
| `variant` | `"default" \| "muted"` | `"default"` | default is pink-900, muted is greyscale-text-caption |
| `size` | `"xs" \| "sm" \| "base"` | `"xs"` | Font size: 12px, 14px, 16px |

Plus standard anchor attributes.

**Example:**

```tsx
<Link href="/privacy" variant="muted" size="sm">Privacy Policy</Link>
```

### Data Display

#### DataTable (compound)

```typescript
import { DataTable, DataTableColumnHeader } from "@jem-open/jem-ui"
```

Uses TanStack React Table. Requires defining columns with `ColumnDef`.

| Prop | Type | Default | Description |
|---|---|---|---|
| `columns` | `ColumnDef<TData, TValue>[]` | required | Column definitions |
| `data` | `TData[]` | required | Data array |
| `filterColumn` | `string` | — | Column key to filter on |
| `filterPlaceholder` | `string` | — | Filter input placeholder |
| `showPagination` | `boolean` | `true` | Show pagination controls |
| `showToolbar` | `boolean` | `true` | Show toolbar with filter |
| `showRowsSelected` | `boolean` | `true` | Show selected row count |
| `toolbarChildren` | `React.ReactNode` | — | Extra toolbar content |

**DataTableColumnHeader** enables sorting. Use it in column header definitions.

**Example:**

```tsx
import { ColumnDef } from "@tanstack/react-table"

type User = { name: string; email: string; status: string }

const columns: ColumnDef<User>[] = [
  {
    accessorKey: "name",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Name" />,
  },
  {
    accessorKey: "email",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Email" />,
  },
  {
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => <Tag variant="success">{row.getValue("status")}</Tag>,
  },
]

<DataTable columns={columns} data={users} filterColumn="name" filterPlaceholder="Filter by name..." />
```

#### Table (compound)

```typescript
import {
  Table, TableHeader, TableBody, TableRow, TableHead, TableCell
} from "@jem-open/jem-ui"
```

Primitive table elements for custom table layouts. Use DataTable for most cases.

**Example:**

```tsx
<Table>
  <TableHeader>
    <TableRow>
      <TableHead>Name</TableHead>
      <TableHead>Status</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    <TableRow>
      <TableCell>Alice</TableCell>
      <TableCell>Active</TableCell>
    </TableRow>
  </TableBody>
</Table>
```

Additional parts: `TableCaption`, `TableFooter`.

#### Tag / DismissibleTag / CountTag

```typescript
import { Tag, DismissibleTag, CountTag } from "@jem-open/jem-ui"
```

**Tag variants:**

| Variant | Description |
|---|---|
| `default` | Navy-900 background |
| `success` | Green tones |
| `processing` | Blue-50 background |
| `pending` | Yellow-50 background |
| `failed` | Red-50 background |
| `drafted` | Grey tones |
| `outline` | Border only |
| `outline-navy` | Navy border |
| `neutral` | Neutral background |
| `pink` | Pink background |
| `pink-text` | Pink text, no background |
| `lime` | Lime background |
| `purple` | Purple background |

**Tag example:**

```tsx
<Tag variant="success">Active</Tag>
<Tag variant="pending">Pending review</Tag>
```

**DismissibleTag** adds `onDismiss` callback:

```tsx
<DismissibleTag variant="default" onDismiss={() => removeTag(id)}>
  Filter: Active
</DismissibleTag>
```

**CountTag** — small pink circle with white number:

```tsx
<CountTag>3</CountTag>
```

#### Avatar (compound)

```typescript
import { Avatar, AvatarImage, AvatarFallback } from "@jem-open/jem-ui"
```

**Avatar sizes:**

| Size | Dimensions |
|---|---|
| `sm` | 32px |
| `md` | 40px (default) |
| `lg` | 48px |

**Example:**

```tsx
<Avatar size="lg">
  <AvatarImage src="/user.jpg" alt="Jane Doe" />
  <AvatarFallback size="lg">JD</AvatarFallback>
</Avatar>
```

Note: Pass `size` to both `Avatar` and `AvatarFallback` to keep dimensions consistent.

**AvatarBadge** — online/status indicator (green dot, absolute positioned):

```tsx
<Avatar>
  <AvatarImage src="/user.jpg" alt="Jane Doe" />
  <AvatarFallback>JD</AvatarFallback>
  <AvatarBadge />
</Avatar>
```

**AvatarGroup / AvatarGroupCount** — stacked avatars:

```tsx
<AvatarGroup>
  <Avatar><AvatarFallback>AB</AvatarFallback></Avatar>
  <Avatar><AvatarFallback>CD</AvatarFallback></Avatar>
  <Avatar><AvatarFallback>EF</AvatarFallback></Avatar>
  <AvatarGroupCount>+5</AvatarGroupCount>
</AvatarGroup>
```

#### Progress

```typescript
import { Progress } from "@jem-open/jem-ui"
```

**Props:** extends Radix Progress. Key prop: `value` (0-100).

Height: 6px. Indicator: secondary-pink-900.

**Example:**

```tsx
<Progress value={65} />
```

#### Divider

```typescript
import { Divider } from "@jem-open/jem-ui"
```

| Prop | Type | Default | Description |
|---|---|---|---|
| `orientation` | `"horizontal" \| "vertical"` | `"horizontal"` | Direction |
| `variant` | `"default" \| "subtle" \| "strong" \| "primary" \| "secondary"` | `"default"` | Color style |
| `spacing` | `"none" \| "sm" \| "md" \| "lg"` | `"none"` | Margin around divider |
| `label` | `string` | — | Text label in center (horizontal only) |

**Example:**

```tsx
<Divider spacing="md" />
<Divider label="OR" variant="subtle" spacing="lg" />
```

#### Skeleton

```typescript
import { Skeleton } from "@jem-open/jem-ui"
```

Loading placeholder. Apply width/height via className.

**Example:**

```tsx
<Skeleton className="h-12 w-full" />
<Skeleton className="h-4 w-3/4" />
```

### Feedback

#### Dialog (compound)

```typescript
import {
  Dialog, DialogTrigger, DialogContent, DialogHeader,
  DialogTitle, DialogDescription, DialogFooter, DialogClose
} from "@jem-open/jem-ui"
```

**DialogContent** props:

| Prop | Type | Default | Description |
|---|---|---|---|
| `showCloseButton` | `boolean` | `true` | Show X button in top-right |

Max width: `max-w-md`. Border radius: `rounded-2xl`.

**DialogTitle** variants:

| Variant | Description |
|---|---|
| `default` | greyscale-text-title color |
| `error` | secondary-pink-900 color (use for destructive actions) |

**Example:**

```tsx
<Dialog>
  <DialogTrigger asChild>
    <Button>Open dialog</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Edit profile</DialogTitle>
      <DialogDescription>Make changes to your profile here.</DialogDescription>
    </DialogHeader>
    {/* Form content */}
    <DialogFooter>
      <DialogClose asChild>
        <Button variant="outline">Cancel</Button>
      </DialogClose>
      <Button variant="primary">Save</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

Also available: `DialogContact` (shows email link, default "support@example.com").

#### Drawer (compound)

```typescript
import {
  Drawer, DrawerTrigger, DrawerContent, DrawerHeader,
  DrawerBody, DrawerFooter, DrawerTitle, DrawerClose
} from "@jem-open/jem-ui"
```

**Drawer** props:

| Prop | Type | Default | Description |
|---|---|---|---|
| `direction` | `"right" \| "left" \| "top" \| "bottom"` | `"right"` | Side to open from |

**DrawerHeader** props: `showCloseButton` (default: true). Background: secondary-pink-50.

**DrawerContent**: max-w-[455px] for left/right, max-h-[80vh] for top/bottom.

**Example:**

```tsx
<Drawer direction="right">
  <DrawerTrigger asChild>
    <Button variant="outline">View details</Button>
  </DrawerTrigger>
  <DrawerContent>
    <DrawerHeader>
      <DrawerTitle>User Details</DrawerTitle>
    </DrawerHeader>
    <DrawerBody>
      {/* Detail content */}
    </DrawerBody>
    <DrawerFooter>
      <Button variant="primary">Edit</Button>
      <DrawerClose asChild>
        <Button variant="outline">Close</Button>
      </DrawerClose>
    </DrawerFooter>
  </DrawerContent>
</Drawer>
```

Also available: `DrawerSection` (groups content within DrawerBody), `DrawerDescription`.

#### DropdownMenu (compound)

```typescript
import {
  DropdownMenu, DropdownMenuTrigger, DropdownMenuContent,
  DropdownMenuItem, DropdownMenuSeparator
} from "@jem-open/jem-ui"
```

**DropdownMenuItem** props:

| Prop | Type | Default | Description |
|---|---|---|---|
| `inset` | `boolean` | `false` | Add left padding (align with items that have icons) |
| `variant` | `"default" \| "destructive"` | `"default"` | destructive shows red text |

**Example:**

```tsx
<DropdownMenu>
  <DropdownMenuTrigger asChild>
    <IconButton icon={<MoreHorizontal />} aria-label="Actions" />
  </DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuItem>Edit</DropdownMenuItem>
    <DropdownMenuItem>Duplicate</DropdownMenuItem>
    <DropdownMenuSeparator />
    <DropdownMenuItem variant="destructive">Delete</DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

Additional parts for selection: `DropdownMenuCheckboxItem`, `DropdownMenuRadioGroup`, `DropdownMenuRadioItem`.
Nested menus: `DropdownMenuSub`, `DropdownMenuSubTrigger`, `DropdownMenuSubContent`.
Grouping: `DropdownMenuGroup`, `DropdownMenuLabel`.
Keyboard shortcuts: `DropdownMenuShortcut`.

#### Tooltip (compound)

```typescript
import { Tooltip, TooltipProvider, TooltipTrigger, TooltipContent } from "@jem-open/jem-ui"
```

**TooltipContent** variants:

| Variant | Description |
|---|---|
| `dark` | Navy-900 background, white text (default) |
| `light` | Neutral-100 background, title text |

**Important:** Wrap your app or layout in `<TooltipProvider>` once. Tooltips won't render without it.

**Example:**

```tsx
// In layout.tsx — add once
<TooltipProvider>
  {children}
</TooltipProvider>

// In any component
<Tooltip>
  <TooltipTrigger asChild>
    <IconButton icon={<Info />} aria-label="More info" />
  </TooltipTrigger>
  <TooltipContent variant="dark">
    Additional information here
  </TooltipContent>
</Tooltip>
```

#### Popover (compound)

```typescript
import { Popover, PopoverTrigger, PopoverContent } from "@jem-open/jem-ui"
```

**PopoverContent** props: `align` (default: "center"), `sideOffset` (default: 4).

**Example:**

```tsx
<Popover>
  <PopoverTrigger asChild>
    <Button variant="outline">Options</Button>
  </PopoverTrigger>
  <PopoverContent align="start">
    {/* Popover content */}
  </PopoverContent>
</Popover>
```

Also available: `PopoverAnchor`, `PopoverHeader`, `PopoverTitle`, `PopoverDescription`.

#### Alert (compound)

```typescript
import { Alert, AlertTitle, AlertDescription } from "@jem-open/jem-ui"
```

**Alert variants** (each has an automatic icon):

| Variant | Icon | Description |
|---|---|---|
| `default` | Info | General information |
| `success` | CheckCircle2 | Success message |
| `warning` | AlertTriangle | Warning message |
| `destructive` | AlertCircle | Error message |
| `note` | Lightbulb | Note/tip |

| Prop | Type | Default | Description |
|---|---|---|---|
| `hideIcon` | `boolean` | `false` | Hide the automatic icon |

**Example:**

```tsx
<Alert variant="warning">
  <AlertTitle>Warning</AlertTitle>
  <AlertDescription>Your session will expire in 5 minutes.</AlertDescription>
</Alert>
```

#### EmptyState

```typescript
import { EmptyState } from "@jem-open/jem-ui"
```

**Variants:**

| Variant | Description |
|---|---|
| `default` | No background |
| `card` | greyscale-surface-subtle background |
| `bordered` | Border style |

**Sizes:** `sm` (max-w-sm), `md` (max-w-md, default), `lg` (max-w-lg)

**Props:**

| Prop | Type | Default | Description |
|---|---|---|---|
| `icon` | `"folder" \| "alert" \| "search" \| "file" \| "inbox" \| "users" \| React.ReactNode` | — | Icon to display |
| `title` | `string` | required | Title text |
| `description` | `string` | — | Description text |
| `primaryAction` | `{ label: string; onClick?: () => void; href?: string }` | — | Primary action button |
| `secondaryAction` | `{ label: string; onClick?: () => void; href?: string }` | — | Secondary action link |
| `footer` | `React.ReactNode` | — | Custom footer content |

**Example:**

```tsx
<EmptyState
  icon="search"
  title="No results found"
  description="Try adjusting your search or filters"
  primaryAction={{ label: "Clear filters", onClick: clearFilters }}
  variant="card"
/>
```

Pre-configured variants: `EmptyStateNotFound`, `EmptyStateNoResults`, `EmptyStateNoData`.

#### Toaster

```typescript
import { Toaster } from "@jem-open/jem-ui"
```

Add `<Toaster />` once in your root layout. Trigger toasts using `toast()` from the `sonner` package:

```tsx
// layout.tsx
import { Toaster } from "@jem-open/jem-ui"

export default function Layout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Toaster />
      </body>
    </html>
  )
}

// any component
import { toast } from "sonner"

toast.success("Changes saved")
toast.error("Something went wrong")
toast.info("New update available")
toast.warning("Disk space low")
```

Icons are pre-configured: success (PartyPopper), error (TriangleAlert), info (Bell), warning (TriangleAlert), loading (Loader2 spinning).

### Design Tokens (components)

#### Icon

```typescript
import { Icon } from "@jem-open/jem-ui"
```

**Sizes:**

| Size | Dimensions |
|---|---|
| `xs` | 12px |
| `sm` | 16px |
| `md` | 20px (default) |
| `lg` | 24px |
| `xl` | 32px |

| Prop | Type | Default | Description |
|---|---|---|---|
| `icon` | `LucideIcon` | required | Lucide icon component |
| `label` | `string` | — | Accessibility label |

**Example:**

```tsx
import { Icon } from "@jem-open/jem-ui"
import { Settings } from "lucide-react"

<Icon icon={Settings} size="lg" label="Settings" />
```

Re-exported Lucide icons available from `@jem-open/jem-ui`: X, Menu, Check, ChevronDown, ChevronUp, ChevronLeft, ChevronRight, Home, Settings, Calendar, Users, Info, CircleAlert, AlertTriangle, Bell, Edit, Trash2, Download, Upload, Copy, Plus, Minus, Search, Filter, Eye, EyeOff, ArrowUp, ArrowDown, ArrowLeft, ArrowRight, ExternalLink, MoreHorizontal, MoreVertical, RefreshCw, Loader2.

#### PrimaryLogo

```typescript
import { PrimaryLogo } from "@jem-open/jem-ui"
```

| Prop | Type | Default | Description |
|---|---|---|---|
| `variant` | `"bg-pink" \| "bg-white" \| "pink" \| "white"` | `"bg-pink"` | Color scheme |
| `size` | `"sm" \| "md" \| "lg" \| "xl"` | `"md"` | sm=24px, md=40px, lg=64px, xl=96px |

**Example:**

```tsx
<PrimaryLogo variant="bg-white" size="lg" />
```

#### SecondaryLogoRound

```typescript
import { SecondaryLogoRound } from "@jem-open/jem-ui"
```

| Prop | Type | Default | Description |
|---|---|---|---|
| `variant` | `"bg-pink" \| "bg-white"` | `"bg-pink"` | Color scheme |
| `size` | `"sm" \| "md" \| "lg" \| "xl"` | `"md"` | sm=32px, md=48px, lg=64px, xl=96px |

#### SecondaryLogoSquare

```typescript
import { SecondaryLogoSquare } from "@jem-open/jem-ui"
```

Same props as SecondaryLogoRound.

---

## Step 4 — Apply design tokens

Use these design tokens for consistent styling. Always prefer semantic tokens over raw color values.

### Colors — Semantic tokens

Use semantic tokens for all UI colors. These adapt correctly across themes.

| Category | CSS variable | Tailwind class | Purpose |
|---|---|---|---|
| Primary surface | `--primary-surface-default` | `bg-primary-surface-default` | Primary backgrounds (navy) |
| Primary surface | `--primary-surface-lighter` | `bg-primary-surface-lighter` | Lighter primary bg |
| Primary surface | `--primary-surface-subtle` | `bg-primary-surface-subtle` | Subtle primary bg |
| Primary surface | `--primary-surface-darker` | `bg-primary-surface-darker` | Darker primary bg |
| Primary border | `--primary-border-default` | `border-primary-border-default` | Primary borders |
| Primary border | `--primary-border-lighter` | `border-primary-border-lighter` | Lighter primary border |
| Primary border | `--primary-border-subtle` | `border-primary-border-subtle` | Subtle primary border |
| Primary border | `--primary-border-darker` | `border-primary-border-darker` | Darker primary border |
| Primary text | `--primary-text-label` | `text-primary-text-label` | Primary label text |
| Secondary surface | `--secondary-surface-default` | `bg-secondary-surface-default` | Secondary backgrounds (pink) |
| Secondary surface | `--secondary-surface-lighter` | `bg-secondary-surface-lighter` | Lighter secondary bg |
| Secondary surface | `--secondary-surface-subtle` | `bg-secondary-surface-subtle` | Subtle secondary bg |
| Secondary surface | `--secondary-surface-darker` | `bg-secondary-surface-darker` | Darker secondary bg |
| Secondary border | `--secondary-border-default` | `border-secondary-border-default` | Secondary borders |
| Secondary text | `--secondary-text-label` | `text-secondary-text-label` | Secondary label text |
| Error surface | `--error-surface-default` | `bg-error-surface-default` | Error backgrounds (red) |
| Error border | `--error-border-default` | `border-error-border-default` | Error borders |
| Error text | `--error-text-label` | `text-error-text-label` | Error label text |
| Warning surface | `--warning-surface-default` | `bg-warning-surface-default` | Warning backgrounds (orange) |
| Warning border | `--warning-border-default` | `border-warning-border-default` | Warning borders |
| Warning text | `--warning-text-label` | `text-warning-text-label` | Warning label text |
| Success surface | `--success-surface-default` | `bg-success-surface-default` | Success backgrounds (green) |
| Success border | `--success-border-default` | `border-success-border-default` | Success borders |
| Success text | `--success-text-label` | `text-success-text-label` | Success label text |
| Greyscale surface | `--greyscale-surface-default` | `bg-greyscale-surface-default` | Default page background |
| Greyscale surface | `--greyscale-surface-subtle` | `bg-greyscale-surface-subtle` | Subtle background |
| Greyscale surface | `--greyscale-surface-disabled` | `bg-greyscale-surface-disabled` | Disabled background |
| Greyscale border | `--greyscale-border-default` | `border-greyscale-border-default` | Default borders |
| Greyscale border | `--greyscale-border-disabled` | `border-greyscale-border-disabled` | Disabled borders |
| Greyscale border | `--greyscale-border-darker` | `border-greyscale-border-darker` | Darker borders |
| Greyscale text | `--greyscale-text-title` | `text-greyscale-text-title` | Page titles |
| Greyscale text | `--greyscale-text-body` | `text-greyscale-text-body` | Body text |
| Greyscale text | `--greyscale-text-subtitle` | `text-greyscale-text-subtitle` | Subtitles |
| Greyscale text | `--greyscale-text-caption` | `text-greyscale-text-caption` | Captions, hints |
| Greyscale text | `--greyscale-text-negative` | `text-greyscale-text-negative` | Inverted text (white) |
| Greyscale text | `--greyscale-text-disabled` | `text-greyscale-text-disabled` | Disabled text |

### Colors — Base palette

Use sparingly. Prefer semantic tokens above. Available for decorative/custom elements only.

| Palette | Tailwind prefix | Shades |
|---|---|---|
| Navy | `navy-` | 50, 100, 200, 300, 400, 500, 600, 700, 800, 900 |
| Pink | `pink-` | 50, 100, 200, 300, 400, 500, 600, 700, 800, 900 |
| Lime | `lime-` | 50–900 |
| Purple | `purple-` | 50–900 |
| Violet | `violet-` | 50–900 |
| Blue | `blue-` | 50–900 |
| Green | `green-` | 50–900 |
| Orange | `orange-` | 50–900 |
| Yellow | `yellow-` | 50–900 |
| Red | `red-` | 50–900 |
| Neutral | `neutral-` | 50–900, white, cream, black |

Usage: `bg-navy-100`, `text-pink-900`, `border-green-500`, etc.

### Spacing

| Token | Tailwind class | Value |
|---|---|---|
| none | `p-none`, `m-none`, `gap-none` | 0px |
| xxxxs | `p-xxxxs`, `m-xxxxs`, `gap-xxxxs` | 2px |
| xxxs | `p-xxxs`, `m-xxxs`, `gap-xxxs` | 4px |
| xxs | `p-xxs`, `m-xxs`, `gap-xxs` | 8px |
| xs | `p-xs`, `m-xs`, `gap-xs` | 12px |
| sm | `p-sm`, `m-sm`, `gap-sm` | 16px |
| md | `p-md`, `m-md`, `gap-md` | 24px |
| lg | `p-lg`, `m-lg`, `gap-lg` | 32px |
| xl | `p-xl`, `m-xl`, `gap-xl` | 48px |
| xxl | `p-xxl`, `m-xxl`, `gap-xxl` | 64px |
| xxxl | `p-xxxl`, `m-xxxl`, `gap-xxxl` | 96px |
| xxxxl | `p-xxxxl`, `m-xxxxl`, `gap-xxxxl` | 128px |

These tokens work with all Tailwind spacing utilities: `p-`, `px-`, `py-`, `m-`, `mx-`, `my-`, `gap-`, `space-x-`, `space-y-`, `w-`, `h-`, etc.

### Typography

**Font families:**
- `font-heading` — heading font (from `--font-family-heading`)
- `font-body` — body font (from `--font-family-body`)

**Font sizes:**

| Token | Tailwind class | Value |
|---|---|---|
| xxs | `text-xxs` | 10px |
| xs | `text-xs` | 12px |
| sm | `text-sm` | 14px |
| base | `text-base` | 16px |
| lg | `text-lg` | 18px |
| xl | `text-xl` | 20px |
| 2xl | `text-2xl` | 24px |
| 3xl | `text-3xl` | 30px |
| 4xl | `text-4xl` | 36px |
| 5xl | `text-5xl` | 48px |
| 6xl | `text-6xl` | 60px |
| 7xl | `text-7xl` | 72px |
| 8xl | `text-8xl` | 96px |
| 9xl | `text-9xl` | 128px |

**Font weights:**

| Weight | Tailwind class | Value |
|---|---|---|
| light | `font-light` | 300 |
| regular | `font-regular` | 400 |
| medium | `font-medium` | 500 |
| semibold | `font-semibold` | 600 |
| bold | `font-bold` | 700 |
| extrabold | `font-extrabold` | 800 |
| black | `font-black` | 900 |

### Border radius

| Token | Tailwind class | Value |
|---|---|---|
| none | `rounded-none` | 0px |
| xs | `rounded-xs` | 2px |
| sm | `rounded-sm` | 4px |
| md | `rounded-md` | 6px |
| lg | `rounded-lg` | 8px |
| xl | `rounded-xl` | 12px |
| 2xl | `rounded-2xl` | 16px |
| 3xl | `rounded-3xl` | 24px |
| 4xl | `rounded-4xl` | 32px |
| full | `rounded-full` | 100px |

---

## Step 5 — Avoid common mistakes

| Mistake | Why it's wrong | Correction |
|---|---|---|
| Building a custom button, input, or select component | jem-ui already provides these with consistent styling and accessibility | Check the catalog in Step 2 — the component likely exists |
| Using raw hex colors like `bg-[#062133]` or `text-[#ff697f]` | Bypasses the design system; breaks if tokens change | Use semantic tokens: `bg-primary-surface-default`, `text-secondary-text-label` |
| Merging classes with template literals: `` `${base} ${conditional}` `` | Tailwind classes can conflict (e.g. `p-4` and `p-2`); template literals don't resolve conflicts | Use `cn()` from `@jem-open/jem-ui`: `cn("p-4", isCompact && "p-2")` |
| Wrapping a Button in an anchor: `<a><Button>Click</Button></a>` | Nested interactive elements — accessibility violation, unexpected behavior | Use `asChild`: `<Button asChild><a href="/path">Click</a></Button>` |
| Writing `style={{ padding: '16px' }}` or `className="p-4"` | Bypasses design tokens; `p-4` is Tailwind default (16px) not jem-ui token | Use spacing tokens: `className="p-sm"` (16px via jem-ui token) |
| Hardcoding `#ff697f` for pink or `#062133` for navy | Raw hex breaks if the palette changes | Use `text-pink-500` or semantic `text-secondary-text-label` |
| Forgetting `TooltipProvider` wrapper | Tooltips silently won't render | Wrap your app or layout in `<TooltipProvider>` once |
| Adding `Toaster` in every page component | Creates duplicate toasts | Add `<Toaster />` once in the root layout |
| Using `<div onClick>` for clickable elements | Not keyboard accessible, no focus management, no semantic meaning | Use `<Button variant="ghost">` or the appropriate interactive component |
