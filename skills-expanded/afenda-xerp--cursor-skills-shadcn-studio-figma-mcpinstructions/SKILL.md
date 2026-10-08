---
applyTo: "**"
---

# Upstream shadcn/studio Figma MCP notes (generic)

> **Afenda ERP:** Use [figma-mcp-afenda.md](./figma-mcp-afenda.md) instead — **no Figma Code Connect**; registry-first + `/ftc` + `@afenda/shadcn-studio` primitives + in-repo manifests.

# GitHub Copilot Instructions for shadcn/ui Project Figma MCP

## ⚠️ CRITICAL RULE - READ THIS FIRST ⚠️

**NEVER USE PURE TAILWIND CSS FOR UI COMPONENTS. ALWAYS USE SHADCN/UI COMPONENTS.**

This is a **shadcn/ui project**. Even if you receive code from external sources (Figma, designs, etc.) that uses pure Tailwind, you MUST convert it to use shadcn/ui components.

## Primary Framework & Component Library

This project uses **shadcn/ui** as the PRIMARY and ONLY component library. shadcn/ui components MUST be used over:

- ❌ Pure Tailwind CSS implementations
- ❌ Custom div/span with Tailwind classes
- ❌ Raw HTML elements

## Component Usage Guidelines

### 1. Always Check Available Components First

Before creating any UI element, check if a shadcn/ui component exists:

- Available components are in `/components/ui/` directory
- Common components: Button, Input, Dialog, Avatar, Badge, Accordion, Card, etc.
- If unsure, check the components directory or suggest adding the component via CLI

### 1.5 When Receiving Code from External Sources (Figma, Designs, etc.)

**MANDATORY CONVERSION PROCESS:**

When you get code from Figma MCP or any design tool:

1. **DO NOT use the code directly** - It will be pure Tailwind
2. **Analyze the design** - Identify what UI components it contains (cards, buttons, badges, tabs, etc.)
3. **Map to shadcn/ui components**:
   - Card layouts → `Card`, `CardHeader`, `CardContent`, `CardFooter`
   - Buttons → `Button` with appropriate variant
   - Badges/Pills → `Badge` component
   - Tabs → `Tabs`, `TabsList`, `TabsTrigger`, `TabsContent`
   - Any interactive element → Find shadcn/ui equivalent
4. **Extract only**: Text content, images, data, and layout structure
5. **Rebuild using shadcn/ui components** with the extracted content
6. **Use Tailwind ONLY for**: Spacing (px, py, gap, etc.), layout (flex, grid), and positioning

**EXAMPLE - WRONG vs RIGHT:**

❌ **WRONG** (Pure Tailwind from Figma):

```tsx
<div className="bg-white rounded-lg p-6 shadow-md">
  <button className="bg-blue-500 text-white px-4 py-2 rounded">Click me</button>
</div>
```

✅ **RIGHT** (shadcn/ui components):

```tsx
<Card>
  <CardContent className="p-6">
    <Button>Click me</Button>
  </CardContent>
</Card>
```

### 2. Installation Commands

**ALWAYS install missing shadcn/ui components before writing code.**

When a shadcn/ui component is needed but not available:

```bash
npx shadcn@latest add [component-name]
```

Examples:

- `npx shadcn@latest add accordion`
- `npx shadcn@latest add card`
- `npx shadcn@latest add button`
- `npx shadcn@latest add badge`
- `npx shadcn@latest add tabs`
- `npx shadcn@latest add sheet`

**Install components FIRST, then write the implementation.**

### 3. Import Pattern

Always use the established import pattern:

```tsx
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
```

### 4. Styling Approach

- Use shadcn/ui components with their built-in variants and props
- Leverage CSS variables defined in globals.css (--background, --foreground, --muted, etc.)
- Only add custom Tailwind classes for layout and spacing, not for core component styling
- Use `cn()` utility for conditional classes when available

### 5. Component Hierarchy Preference

1. **First Choice**: Use existing shadcn/ui components from `/components/ui/`
2. **Second Choice**: Install missing shadcn/ui components via CLI
3. **Third Choice**: Create custom components that extend shadcn/ui components
4. **FORBIDDEN**: Pure custom Tailwind components or raw HTML elements for UI components

**NEVER skip straight to Tailwind. ALWAYS try shadcn/ui first.**

## Specific Component Mappings

### Interactive Elements

- Buttons → `Button` component with variants (default, destructive, outline, secondary, ghost, link)
- Form inputs → `Input`, `Textarea`, `Select` components
- Modals/Popups → `Dialog`, `Sheet`, `Popover` components
- Dropdowns → `DropdownMenu` component

### Layout & Navigation

- Cards → `Card` component with CardHeader, CardContent, CardFooter
- Accordions → `Accordion` component with AccordionItem, AccordionTrigger, AccordionContent
- Tabs → `Tabs` component with TabsList, TabsTrigger, TabsContent
- Navigation → `NavigationMenu` component

### Data Display

- Tables → `Table` component with proper semantic structure
- Lists → Use `Command` component for searchable lists
- Badges/Tags → `Badge` component with variants
- Avatars → `Avatar` component with AvatarImage, AvatarFallback

### Feedback & Status

- Alerts → `Alert` component with AlertDescription
- Toasts → `Toast` components (install if needed)
- Progress → `Progress` component
- Skeleton loading → `Skeleton` component

## Code Generation Rules

### Always Include

1. Proper TypeScript types and interfaces
2. Error handling and loading states using shadcn/ui components
3. Accessibility attributes (already built into shadcn/ui components)
4. Responsive design using Tailwind breakpoints

### Never Do

1. Create custom button components when Button exists
2. Use raw HTML form elements instead of shadcn/ui form components
3. Implement custom modal/dialog logic when Dialog component exists
4. Create custom accordion logic when Accordion component exists

## Quality Checklist

Before finalizing ANY component, you MUST verify:

- [ ] ✅ Uses shadcn/ui components (NOT raw Tailwind div/button/etc.)
- [ ] ✅ Installed all required shadcn/ui components via CLI
- [ ] ✅ Follows established import patterns
- [ ] ✅ Uses proper TypeScript types
- [ ] ✅ Implements responsive design
- [ ] ✅ Maintains design system consistency
- [ ] ✅ Uses CSS variables for theming
- [ ] ✅ Includes proper accessibility features (built into shadcn/ui)
- [ ] ❌ NO pure Tailwind button/card/badge implementations
- [ ] ❌ NO code copied directly from Figma without conversion

**If you answered NO to any ✅ or YES to any ❌, STOP and refactor.**

## Design System Integration

- Follow the existing color palette defined in globals.css
- Use spacing tokens consistently (Tailwind spacing scale)
- Maintain typography hierarchy using Tailwind typography classes
- Respect the established border radius and shadow patterns

Remember: shadcn/ui components are designed to work together seamlessly. Always prioritize the component library ecosystem over custom implementations.
