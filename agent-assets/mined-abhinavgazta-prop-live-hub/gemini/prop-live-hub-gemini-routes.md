# Routes

This directory uses [TanStack Router](https://tanstack.com/router) for file-based routing. Routes are automatically discovered and code-generated into `src/routeTree.gen.ts`.

## Core Concepts

- **File-based Routing:** Each `.tsx` file in this directory (excluding `__root.tsx`) represents a route.
- **Root Route (`__root.tsx`):** Defines the base layout, global providers (QueryClientProvider), and error/notFound components.
- **Index Route (`index.tsx`):** The home page route (`/`).

## Adding a New Route

1. Create a new `.tsx` file in `src/routes/` (e.g., `settings.tsx`).
2. Define the route using `createFileRoute`:

```tsx
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/settings")({
  component: SettingsComponent,
  loader: async () => {
    // Fetch data before the route renders
  },
});

function SettingsComponent() {
  return <div>Settings Page</div>;
}
```

3. The dev server will automatically update `src/routeTree.gen.ts`.

## Loaders and Data Fetching

- Use the `loader` function to fetch data required for a route.
- Access loader data in the component using `Route.useLoaderData()`.
- For complex data fetching, integrate with **TanStack Query** by passing the `queryClient` through the route context.

## Search Parameters

- Define and validate search parameters using Zod schemas in the route definition.
- Access them using `Route.useSearch()`.

## Navigation

- Use the `Link` component from `@tanstack/react-router` for internal navigation.
- Use the `useNavigate` hook for programmatic navigation.
- Both are fully type-safe based on your defined routes.
