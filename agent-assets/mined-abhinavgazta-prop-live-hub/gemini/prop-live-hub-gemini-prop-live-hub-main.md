# PropLive - Hyper-local Property Discovery

PropLive is a hyper-local property discovery and live-streaming platform, currently focused on Gurgaon. It leverages modern web technologies to provide a high-performance, interactive experience for property seekers and hosts.

## Tech Stack

- **Framework:** [TanStack Start](https://tanstack.com/start) (Full-stack React framework)
- **Routing:** [TanStack Router](https://tanstack.com/router) (Type-safe file-based routing)
- **State Management:** [TanStack Query](https://tanstack.com/query) (Data fetching and caching)
- **UI Components:** [Shadcn UI](https://ui.shadcn.com/) (Radix UI + Tailwind CSS)
- **Styling:** [Tailwind CSS v4](https://tailwindcss.com/)
- **Icons:** [Lucide React](https://lucide.dev/)
- **Maps:** [Leaflet](https://leafletjs.com/) with [React Leaflet](https://react-leaflet.js.org/)
- **Forms:** [React Hook Form](https://react-hook-form.com/) + [Zod](https://zod.dev/)
- **Deployment:** [Cloudflare Workers](https://workers.cloudflare.com/) via Wrangler

## Project Structure

- `src/routes/`: File-based routes (TanStack Router).
- `src/components/ui/`: Reusable UI components (Shadcn UI).
- `src/components/layout/`: Global layout components like `AppShell`.
- `src/components/map/`: Map-related components (Leaflet).
- `src/lib/`: Shared utilities and libraries.
- `src/hooks/`: Custom React hooks.
- `src/styles.css`: Global styles and Tailwind configuration.
- `wrangler.jsonc`: Cloudflare Workers configuration.

## Development Workflow

### Scripts

- `npm run dev`: Start the development server.
- `npm run build`: Build for production.
- `npm run lint`: Run ESLint for code quality.
- `npm run format`: Format code using Prettier.

### Conventions

- **Routing:** Always use file-based routing in `src/routes/`. Follow TanStack Router conventions for loaders and search params.
- **Components:** Prefer functional components with TypeScript. Use Shadcn UI components from `src/components/ui/` for consistency.
- **Styling:** Use Tailwind CSS utility classes. Avoid inline styles unless necessary for dynamic values. Leverage CSS variables defined in `src/styles.css`.
- **Types:** Maintain strict TypeScript typing across the codebase. Use Zod for runtime validation and schema definitions.

## Key Files

- `src/router.tsx`: Router instance creation.
- `src/routes/__root.tsx`: Root layout and provider setup.
- `src/server.ts`: Entry point for the Cloudflare Worker server.
- `src/start.ts`: Client-side hydration entry point.
