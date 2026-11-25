---
name: shadcn-design-system
description: "Use this skill whenever the user is working with @sth87/shadcn-design-system, importing or using any of its components (Button, Dialog, DataTable, Sidebar, DatePicker, etc.), asking how to set up or configure the design system, customizing themes or tokens, using hooks like useDataTable, or building UI with this React + TypeScript component library. Also trigger when the user mentions shadcn-design-system, @sth87, or @dsui/design-system, even if they don't explicitly ask about a specific component."
---

# Design System Skill — @sth87/shadcn-design-system

## Quick Reference

| | |
|---|---|
| **Package** | `@sth87/shadcn-design-system` |
| **Internal alias** | `@dsui/design-system` |
| **React** | 18 / 19 |
| **Styling** | Tailwind CSS v4 + CSS custom properties |
| **Primitives** | Radix UI |
| **Motion** | `motion/react` (Framer Motion v11+) |
| **Icons** | `lucide-react` |
| **Table** | TanStack Table v8 |
| **Toasts** | Sonner |
| **URL State** | nuqs |
| **Storybook** | https://design-system-sth-kappa.vercel.app/ |

---

## 1. Installation & Setup

### 1.1 Install

```bash
npm install @sth87/shadcn-design-system
# or
pnpm add @sth87/shadcn-design-system
```

### 1.2 Tailwind v4 Configuration

```css
/* In your global CSS (v4 style) */
@source "../../node_modules/@sth87/shadcn-design-system/dist";
```

```js
// tailwind.config.js (v3 compat)
content: [
  "./src/**/*.{ts,tsx}",
  "./node_modules/@sth87/shadcn-design-system/dist/**/*.{js,mjs}"
]
```

Tailwind v3 — extend theme with CSS variable mappings:

```js
theme: {
  extend: {
    colors: {
      border: "hsl(var(--border))",
      input: "hsl(var(--input))",
      ring: "hsl(var(--ring))",
      background: "hsl(var(--background))",
      foreground: "hsl(var(--foreground))",
      primary: { DEFAULT: "hsl(var(--primary))", foreground: "hsl(var(--primary-foreground))" },
      secondary: { DEFAULT: "hsl(var(--secondary))", foreground: "hsl(var(--secondary-foreground))" },
      destructive: { DEFAULT: "hsl(var(--destructive))", foreground: "hsl(var(--destructive-foreground))" },
      muted: { DEFAULT: "hsl(var(--muted))", foreground: "hsl(var(--muted-foreground))" },
      accent: { DEFAULT: "hsl(var(--accent))", foreground: "hsl(var(--accent-foreground))" },
    },
    borderRadius: {
      lg: "var(--radius)",
      md: "calc(var(--radius) - 2px)",
      sm: "calc(var(--radius) - 4px)"
    },
  }
}
```

### 1.3 Global CSS Imports

Import all three in your root entry (`main.tsx`, `app/layout.tsx`, etc.):

```tsx
import "@sth87/shadcn-design-system/theme.css";     // design tokens (colors, radius, etc.)
import "@sth87/shadcn-design-system/index.css";     // component base styles
import "@sth87/shadcn-design-system/animation.css"; // animation keyframes
```

### 1.4 Component Imports

All exports are named exports from the package root:

```tsx
import {
  Button, Dialog, Input, Select, Tabs, DataTable,
  useDataTable, cn, toast, Toaster,
  BlurText, TypingText,
} from "@sth87/shadcn-design-system";
```

### 1.5 Toaster Setup

```tsx
import { Toaster } from "@sth87/shadcn-design-system";
// Add once at the app root
<Toaster position="top-right" richColors closeButton />
```

---

## 2. Reference Files

Load the relevant reference file when you need full props, types, or detailed examples. The index tables in Section 3 link directly to the relevant anchors.

| File | When to read | Contents |
|---|---|---|
| [references/theme-tokens.md](references/theme-tokens.md) | User asks about colors, dark mode, CSS variables, theming, or custom tokens | CSS design tokens, dark mode, theme switching, animation token table |
| [references/components-a-l.md](references/components-a-l.md) | User uses any component from Accordion to Label | Accordion → Label — full props + examples for 25 components |
| [references/components-m-z.md](references/components-m-z.md) | User uses any component from Marquee to Upload | Marquee → Upload — full props + examples for 26 components |
| [references/text-animation.md](references/text-animation.md) | User asks about text effects or animation components | 13 text animation components with usage examples |
| [references/utils.md](references/utils.md) | User calls `cn`, formatting helpers, or URL state utilities | `cn`, `animationClass`, `animationEffect`, `formatDate`, `dataTableConfig`, URL state parsers |
| [references/hooks.md](references/hooks.md) | User uses any hook from this library | 12 hooks including `useDataTable`, `useDebounceValue`, `useIntersectionObserver` |
| [references/types.md](references/types.md) | User needs TypeScript types or interfaces | All TypeScript types: `BasicColor`, `BasicAnimation`, `UploadFile`, `FilterVariant`, etc. |

---

## 3. Component Quick Index

### Components A–L → [references/components-a-l.md](references/components-a-l.md)

| Component | Import | Purpose |
|---|---|---|
| [Accordion](references/components-a-l.md#41-accordion) | `Accordion` | Collapsible FAQ sections |
| [Avatar](references/components-a-l.md#42-avatar) | `Avatar` | User photo or initials |
| [Badge](references/components-a-l.md#43-badge) | `Badge` | Status label / tag |
| [Breadcrumb](references/components-a-l.md#44-breadcrumb) | `Breadcrumb` | Navigation trail |
| [Button](references/components-a-l.md#45-button) | `Button`, `ButtonGroup` | Primary action / grouped buttons |
| [Calendar](references/components-a-l.md#46-calendar) | `Calendar` | Full calendar with date/range selection |
| [Carousel](references/components-a-l.md#47-carousel--carouselslide) | `Carousel`, `CarouselSlide` | Touch slider (Swiper.js) |
| [Checkbox](references/components-a-l.md#48-checkbox) | `Checkbox` | Binary toggle with label |
| [Collapsible](references/components-a-l.md#49-collapsible) | `Collapsible` | Single expandable section |
| [Command](references/components-a-l.md#410-command) | `Command`, `CommandDialog` | Command palette / spotlight search |
| [ContextMenu](references/components-a-l.md#411-contextmenu) | `ContextMenu` | Right-click action menu |
| [Cropper](references/components-a-l.md#412-cropper) | `Cropper` | Image crop with zoom/rotation |
| [DatePicker](references/components-a-l.md#413-datepicker--rangepicker--timepicker) | `DatePicker` | Date selection input |
| [RangePicker](references/components-a-l.md#413-datepicker--rangepicker--timepicker) | `RangePicker` | Date range selection |
| [TimePicker](references/components-a-l.md#413-datepicker--rangepicker--timepicker) | `TimePicker` | Time selection wheel |
| [Dialog](references/components-a-l.md#414-dialog) | `Dialog` | Modal overlay |
| [DropdownMenu](references/components-a-l.md#415-dropdownmenu) | `DropdownMenu` | Triggered action menu |
| [Glass](references/components-a-l.md#416-glass) | `Glass` | Frosted glass distortion filter |
| [ImageViewer](references/components-a-l.md#417-imageviewer) | `ImageViewer` | Lightbox with zoom/pan/rotation |
| [Input](references/components-a-l.md#418-input) | `Input` | Text input with label/error/prefix/suffix |
| [InputOTP](references/components-a-l.md#419-inputotp) | `InputOTP` | OTP / verification code input |
| [Interactive3DCard](references/components-a-l.md#420-interactive-3dcard) | `Interactive3DCard` | Mouse-tracked 3D tilt card |
| [Interactive3DMarquee](references/components-a-l.md#421-interactive3dmarquee) | `Interactive3DMarquee` | 3D perspective grid scroller |
| [InteractiveCursorFollow](references/components-a-l.md#422-interactivecursorfollow) | `InteractiveCursorFollow` | Custom cursor tracking |
| [Label](references/components-a-l.md#423-label) | `Label` | Form label with required/optional indicator |

### Components M–Z → [references/components-m-z.md](references/components-m-z.md)

| Component | Import | Purpose |
|---|---|---|
| [Marquee](references/components-m-z.md#424-marquee) | `Marquee` | Auto-scrolling content belt |
| [Masonry](references/components-m-z.md#425-masonry) | `Masonry` | Pinterest-style column layout |
| [Pagination](references/components-m-z.md#426-pagination) | `Pagination` | Page navigation control |
| [Popover](references/components-m-z.md#427-popover) | `Popover` | Non-modal floating panel |
| [QrCode](references/components-m-z.md#428-qrcode) | `QrCode` | QR code generator |
| [Radio](references/components-m-z.md#429-radio) | `Radio` | Radio group / button-group variant |
| [Rate](references/components-m-z.md#430-rate) | `Rate` | Star rating input |
| [Resizable](references/components-m-z.md#431-resizable) | `Resizable` | Drag-to-resize split panels |
| [ScrollArea](references/components-m-z.md#432-scrollarea) | `ScrollArea` | Custom-styled scrollable container |
| [Select](references/components-m-z.md#433-select) | `Select` | Dropdown value selector with search |
| [Separator](references/components-m-z.md#434-separator) | `Separator` | Divider line with optional label |
| [Sheet](references/components-m-z.md#435-sheet) | `Sheet` | Side drawer/panel |
| [Sidebar](references/components-m-z.md#436-sidebar) | `Sidebar` + 20 sub-components | Full application sidebar |
| [Skeleton](references/components-m-z.md#437-skeleton) | `Skeleton` | Loading placeholder shimmer |
| [Slider](references/components-m-z.md#438-slider) | `Slider` | Range / value input |
| [Stepper](references/components-m-z.md#439-stepper) | `Stepper` | Multi-step progress indicator |
| [Switch](references/components-m-z.md#440-switch) | `Switch` | Toggle switch |
| [DataTable](references/components-m-z.md#441-datatable) | `DataTable`, `DataTableColumnHeader`, etc. | TanStack Table v8 integration |
| [Tabs](references/components-m-z.md#442-tabs) | `Tabs` | Switchable content panels |
| [Textarea](references/components-m-z.md#443-textarea) | `Textarea` | Multi-line text input |
| [Toast](references/components-m-z.md#444-toast--toaster) | `toast`, `Toaster` | Notification toasts (Sonner) |
| [Toggle](references/components-m-z.md#445-toggle) | `Toggle` | Two-state toggled button |
| [Tooltip](references/components-m-z.md#446-tooltip) | `Tooltip` | Hover information popup |
| [Tour](references/components-m-z.md#447-tour) | `Tour` | Step-by-step feature walkthrough |
| [TreeSelect](references/components-m-z.md#448-treeselect) | `TreeSelect` | Hierarchical tree data selector |
| [Upload](references/components-m-z.md#449-upload) | `Upload` | File uploader with drag & drop preview |

### Text Animation → [references/text-animation.md](references/text-animation.md)

| Import | Effect |
|---|---|
| [`BlurText`](references/text-animation.md#blurtext) | Word-by-word blur entrance |
| [`RotatingText`](references/text-animation.md#rotatingtext) | Cycling word rotation |
| [`CircularText`](references/text-animation.md#circulartext) | Radial character ring |
| [`FlipWords`](references/text-animation.md#flipwords) | Vertical flip word list |
| [`GradientText`](references/text-animation.md#gradienttext) | Animated gradient fill |
| [`RollingText`](references/text-animation.md#rollingtext) | Slot-machine character roll |
| [`ShimmeringText`](references/text-animation.md#shimmeringtext) | Light sheen sweep |
| [`SplittingText`](references/text-animation.md#splittingtext) | Staggered character entrance |
| [`TextGenerateEffect`](references/text-animation.md#textgenerateeffect) | Word-by-word generation |
| [`TextHoverEffect`](references/text-animation.md#texthovereffect) | Cursor-following gradient trail |
| [`TextPressure`](references/text-animation.md#textpressure) | Variable font weight cursor response |
| [`TypingText`](references/text-animation.md#typingtext) | Classic typewriter + cycling |
| [`WritingText`](references/text-animation.md#writingtext) | SVG path draw-in animation |

---

## 4. Quick Recipes

### Minimal page with Button + Toast

```tsx
import "@sth87/shadcn-design-system/theme.css";
import "@sth87/shadcn-design-system/index.css";
import "@sth87/shadcn-design-system/animation.css";
import { Button, Toaster, toast } from "@sth87/shadcn-design-system";

export default function App() {
  return (
    <>
      <Button color="primary" onClick={() => toast.success("Hello!")}>Click me</Button>
      <Toaster position="top-right" />
    </>
  );
}
```

### DataTable (server-side + URL state)

```tsx
// Full docs: references/components-m-z.md#441-datatable  &  references/hooks.md#usedatatable
import { useDataTable, DataTable, DataTableColumnHeader } from "@sth87/shadcn-design-system";
import type { ColumnDef } from "@tanstack/react-table";

const columns: ColumnDef<User>[] = [
  { accessorKey: "name", header: ({ column }) => <DataTableColumnHeader column={column} title="Name" /> },
  { accessorKey: "email", header: "Email" },
];

function UsersPage({ data, pageCount, isLoading }) {
  const table = useDataTable({ data, columns, pageCount, enableSorting: true, syncWithUrl: true });
  return <DataTable table={table} pagination sticky loading={isLoading} />;
}
```

### Sidebar layout

```tsx
// Full example: references/components-m-z.md#436-sidebar
import { SidebarProvider, Sidebar, SidebarContent, SidebarMenu,
         SidebarMenuItem, SidebarMenuButton, SidebarInset, SidebarTrigger }
  from "@sth87/shadcn-design-system";

export default function Layout({ children }) {
  return (
    <SidebarProvider>
      <Sidebar collapsible="icon">
        <SidebarContent>
          <SidebarMenu>
            {navItems.map((item) => (
              <SidebarMenuItem key={item.href}>
                <SidebarMenuButton asChild tooltip={item.label}>
                  <a href={item.href}><item.icon /><span>{item.label}</span></a>
                </SidebarMenuButton>
              </SidebarMenuItem>
            ))}
          </SidebarMenu>
        </SidebarContent>
      </Sidebar>
      <SidebarInset>
        <header className="flex h-16 px-4 items-center gap-4 border-b">
          <SidebarTrigger />
        </header>
        <main className="p-6">{children}</main>
      </SidebarInset>
    </SidebarProvider>
  );
}
```

---

## 5. Integration Checklist

- [ ] `npm install @sth87/shadcn-design-system`
- [ ] Import `theme.css` in root entry
- [ ] Import `index.css` in root entry
- [ ] Import `animation.css` in root entry
- [ ] Configure Tailwind to scan `node_modules/@sth87/shadcn-design-system/dist/`
- [ ] Add `<Toaster />` to app root
- [ ] Install `nuqs` + wrap app in `<NuqsAdapter>` (only if using `syncWithUrl` with `useDataTable`)
- [ ] Wrap app in `<SidebarProvider>` (only if using the Sidebar component)
