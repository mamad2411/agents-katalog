---
name: web-artifacts-builder
description: Create sophisticated Claude.ai HTML artifacts using React, Tailwind CSS, and shadcn/ui components. Use when building complex web artifacts that need state management, routing, component libraries, or modern frontend tooling bundled into a single self-contained HTML file for sharing.
---

# Web Artifacts Builder

Create sophisticated Claude.ai HTML artifacts using modern frontend technologies: React 18 + TypeScript + Vite + Tailwind CSS + shadcn/ui components.

## Technology Stack

- **React 18** + TypeScript
- **Vite** (build tool)
- **Parcel** (bundling to single HTML)
- **Tailwind CSS 3.4.1**
- **shadcn/ui** (40+ pre-installed components)

## Workflow

### 1. Initialize Project

```bash
bash scripts/init-artifact.sh my-artifact-name
cd my-artifact-name
```

This sets up: React + TypeScript via Vite, Tailwind CSS, 40+ shadcn/ui components, path aliases (`@/`), Parcel bundling support.

### 2. Develop the Artifact

Edit the React components in `src/`:

```typescript
// src/App.tsx
import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export default function App() {
  const [count, setCount] = useState(0)

  return (
    <Card className="w-full max-w-md mx-auto mt-8">
      <CardHeader>
        <CardTitle>My Artifact</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-center text-2xl mb-4">{count}</p>
        <Button onClick={() => setCount(c => c + 1)} className="w-full">
          Increment
        </Button>
      </CardContent>
    </Card>
  )
}
```

### 3. Bundle to Single HTML

```bash
bash scripts/bundle-artifact.sh
```

This:
- Installs dependencies
- Configures Parcel with path aliases
- Builds without source maps
- Inlines all assets into a single self-contained HTML file

### 4. Share the Artifact

The output is a single `artifact.html` file that can be directly shared in Claude.ai.

## Available shadcn/ui Components

Accordion, Alert, AlertDialog, AspectRatio, Avatar, Badge, Button, Calendar, Card, Carousel, Checkbox, Collapsible, Command, ContextMenu, Dialog, Drawer, DropdownMenu, Form, HoverCard, Input, Label, Menubar, NavigationMenu, Pagination, Popover, Progress, RadioGroup, ResizablePanels, ScrollArea, Select, Separator, Sheet, Skeleton, Slider, Switch, Table, Tabs, Textarea, Toast, Toggle, Tooltip

## Design Guidelines

Avoid:
- **Excessive centered layouts** — feels like a PowerPoint slide
- **Purple gradients** on everything — overused AI aesthetic
- **Uniform rounded corners** — `border-radius: 8px` on every element
- **Inter font** as the only typeface — use something with character

Do instead:
- Asymmetric layouts with intentional whitespace
- Custom color schemes defined in Tailwind config
- Varied corner radii (some sharp, some round)
- Thoughtful typography pairing

## Example: Data Dashboard

```typescript
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const data = [
  { month: 'Jan', value: 40 },
  { month: 'Feb', value: 65 },
  { month: 'Mar', value: 48 },
]

export function Dashboard() {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">Analytics</h1>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="value" stroke="#d97757" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
```

## Path Aliases

```typescript
// Use @/ instead of relative paths
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
```
