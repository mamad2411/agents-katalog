---
name: frontend-page
description: Create a full frontend page following the 4-layer architecture (Page -> Container -> Component) with strict separation of concerns.
author: Antigravity
---

# Create Frontend Page

This skill guides you through creating a new frontend page in the application, enforcing the **4-layer architecture**:

1.  **Page (Server)**: Entry point/Route definition.
2.  **Container (Client/Server)**: Smart component handling logic and state.
3.  **Hook (Logic)**: Separated logic for the container.
4.  **Component (UI)**: Pure presentational components.

> **Template vs Examples**: Reference implementations live in `examples/frontend/`. See `examples/frontend/containers/product/` for a full working container example.

## Prerequisites

- **App**: `apps/frontend` (or similar)
- **Tech Stack**: Next.js 16 (App Router), React 19, Tailwind CSS 4 + CSS Modules.
- **State Management**: `use-immer` (mandatory for complex state).
- **HTTP**: `ky` via `useApi` hook.

## Step 1: Identify Project Patterns

Before creating files, verify:

1.  **Routing Structure**: Check `app/` (e.g., `app/(screens)/(authenticated)` or `app/[locale]`).
2.  **Existing Containers**: Check `src/containers` for naming/structure consistency.

## Step 2: Create Page (Server Layer)

**Location**: `app/(screens)/(authenticated)/[feature-name]/page.tsx`  
(Adjust based on routing structure found in Step 1)

**Role**: Server Component that imports and renders the Container.

```tsx
import "server-only";
import [FeatureName]Container from "@/containers/[feature-name]";

export default function [FeatureName]Page() {
  return <[FeatureName]Container />;
}
```

## Step 3: Create Container (Smart Component)

**Location**: `src/containers/[feature-name]/`

**Structure**:

1.  `types.ts`: Define Props and State interfaces.
2.  `use-[feature-name].ts`: **Logic Hook** (State, Effects, Handlers).
3.  `[feature-name].tsx`: **View Component** (UI only, uses Hook).
4.  `index.ts`: Exports.
5.  `[feature-name].module.css`: (Optional) CSS Module styles.

### 3.1 Define Types (`types.ts`)

```typescript
import type { ComponentPropsWithoutRef } from "react";

// Container Props
export interface [FeatureName]ContainerProps extends ComponentPropsWithoutRef<"div"> {
  // e.g. id?: string;
}

// Hook Return Interface
export interface Use[FeatureName]Return {
  state: {
    isLoading: boolean;
    data: any[]; // Replace with specific type
  };
  handlers: {
    onAction: () => void;
  };
}
```

### 3.2 Implement Logic Hook (`use-[feature-name].ts`)

Encapsulate ALL logic here.

```typescript
import { useCallback, useEffect } from "react";
import { useImmer } from "use-immer";
import type { [FeatureName]ContainerProps, Use[FeatureName]Return } from "./types";

export default function use[FeatureName](props: [FeatureName]ContainerProps): Use[FeatureName]Return {
  const [state, setState] = useImmer({
    isLoading: false,
    data: [],
  });

  const handleAction = useCallback(() => {
    // Logic here
  }, []);

  return {
    state: {
      isLoading: state.isLoading,
      data: state.data,
    },
    handlers: {
      onAction: handleAction,
    },
  };
}
```

### 3.3 Implement View Component (`[feature-name].tsx`)

Purely presentational. Connects hook to UI.

```tsx
"use client";

import { memo } from "react";
import clsx from "clsx";
import use[FeatureName] from "./use-[feature-name]";
import styles from "./[feature-name].module.css"; // Only if using CSS modules
import type { [FeatureName]ContainerProps } from "./types";

function [FeatureName]Container(props: [FeatureName]ContainerProps) {
  const { className, ...rest } = props;
  const { state, handlers } = use[FeatureName](props);

  return (
    <div className={clsx("flex flex-col gap-4", className)} {...rest}>
      {/* UI Content */}
      {state.isLoading ? "Loading..." : "Content"}
    </div>
  );
}

export default memo([FeatureName]Container);
```

### 3.4 Export (`index.ts`)

```typescript
export { default } from "./[feature-name]";
export type { [FeatureName]ContainerProps } from "./types";
```

## Step 4: Create Shared Hooks (If Needed)

**Location**: `src/hooks/[hook-name]/`

Use for reusable API calls or shared logic across multiple containers.

**Structure**:

- `[hook-name].ts`
- `types.ts`
- `index.ts`

```typescript
// src/hooks/[hook-name]/[hook-name].ts
import { useCallback, useState } from "react";
import useApi from "../use-api";

export default function use[HookName]() {
  const api = useApi();
  // ... implementation
}
```

## Step 5: (Optional) Create UI Components

**Location**: `src/components/ui/[component-name]/`

Use for reusable UI elements. Follow the same 3-4 file structure (`tsx`, `types.ts`, `index.ts`) if complex.

## Golden Rules (XML)

```xml
<golden-rules>
  <rule id="no-export-star">
    <title>Do Not Use export *</title>
    <description>
      Never use `export * from [path]` in index.ts or any re-export file.
      Always use explicit `export type { ... }` for type-only re-exports.
    </description>
    <bad-example>export * from "./types";</bad-example>
    <good-example>export type { [FeatureName]ContainerProps } from "./types";</good-example>
    <rationale>
      `export *` pollutes the namespace, makes types hard to trace,
      and can cause circular dependency issues. Explicit `export type`
      ensures only intended types are exposed and improves IDE autocomplete.
    </rationale>
  </rule>
</golden-rules>
```

## Rules & Conventions

1.  **Files**: Kebab-case (`user-profile.tsx`).
2.  **Components**: PascalCase (`UserProfileContainer`). Always use named functions (`function UserProfileContainer() {}`) for components, never arrow functions.
3.  **State**: Always use `useImmer` for objects/arrays.
4.  **No `any`**: Use strict types from `shared-types` or local definitions.
5.  **Imports**: Use absolute paths (`@/components/...`, `@/hooks/...`).
6.  **Separation**: Logic in `use-[name].ts`, View in `[name].tsx`.
