---
name: shadcn-component-scaffolding
version: "1.0"
description: >
  shadcn/ui CLI usage, component installation, and composition patterns with file ownership philosophy.
  PROACTIVELY activate for: (1) adding shadcn/ui components via CLI, (2) composing multi-part components, (3) customizing component variants.
  Triggers: "shadcn", "add component", "components.json"
group: ui
core-integration:
  techniques:
    primary: ["structured_decomposition"]
    secondary: []
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# shadcn/ui Component Scaffolding

## Overview

shadcn/ui is a collection of re-usable components that you copy into your project. Unlike traditional component libraries, you own the code.

## CLI Usage (MANDATORY)

**ONLY way to add components**:

```bash
npx shadcn-ui@latest add button dialog card
```

**Why CLI only**:
- Resolves dependencies automatically
- Updates components.json
- Installs peer packages
- Ensures correct configuration

## Component Composition

Most shadcn/ui components are composed of multiple parts:

```tsx
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from '@/components/ui/card';

function ProfileCard({ user }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{user.name}</CardTitle>
        <CardDescription>{user.email}</CardDescription>
      </CardHeader>
      <CardContent>
        <p>{user.bio}</p>
      </CardContent>
      <CardFooter>
        <Button>Edit Profile</Button>
      </CardFooter>
    </Card>
  );
}
```

## File Ownership

After installation, the component source code is in your project at `src/components/ui/[component].tsx`. You can:
- Modify the code freely
- Add custom variants
- Change styling
- Extend functionality

## Common Components

### Button

```tsx
import { Button } from '@/components/ui/button';

<Button>Default</Button>
<Button variant="destructive">Delete</Button>
<Button variant="outline">Cancel</Button>
<Button variant="ghost">Menu Item</Button>
<Button size="sm">Small</Button>
<Button size="lg">Large</Button>
```

### Dialog

```tsx
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';

<Dialog>
  <DialogTrigger asChild>
    <Button>Open Dialog</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Are you sure?</DialogTitle>
      <DialogDescription>
        This action cannot be undone.
      </DialogDescription>
    </DialogHeader>
    <DialogFooter>
      <Button variant="outline">Cancel</Button>
      <Button>Continue</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

### Form Components

```tsx
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

<div className="space-y-2">
  <Label htmlFor="email">Email</Label>
  <Input id="email" type="email" placeholder="Enter email" />
</div>

<Select>
  <SelectTrigger>
    <SelectValue placeholder="Select option" />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="option1">Option 1</SelectItem>
    <SelectItem value="option2">Option 2</SelectItem>
  </SelectContent>
</Select>
```

## Anti-Patterns

- `npm install @shadcn/ui` - Not distributed as package
- Manually copying from website - Bypasses dependency checks
- Importing from non-existent package

**Always use**: `npx shadcn-ui@latest add [component]`

## Customization

After installation, customize in `src/components/ui/[component].tsx`:

```tsx
// Add a new variant to button.tsx
const buttonVariants = cva(
  "inline-flex items-center justify-center ...",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground ...",
        destructive: "bg-destructive text-destructive-foreground ...",
        // Add your custom variant
        success: "bg-green-600 text-white hover:bg-green-700",
      },
      // ...
    },
  }
);
```

---

**Related Skills**: `tailwind-utility-styling`, `typescript-prop-definition`
