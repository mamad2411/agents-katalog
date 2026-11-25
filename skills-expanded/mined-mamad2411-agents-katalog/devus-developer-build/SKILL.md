# Devus – AI Coding Rules
# These rules are automatically picked up by Cursor, Copilot, and similar AI assistants.

## Tech Stack
- React 18 + TypeScript (strict off, noImplicitAny off)
- Vite 5 bundler, Bun package manager
- Tailwind CSS 3.4 + tailwindcss-animate
- Framer Motion 12 for animations
- Supabase (via Lovable Cloud) for backend
- React Router 6, React Query 5, Zod 3

## Project Structure
```
src/
  components/          # Reusable UI components (PascalCase.tsx)
  components/ui/       # shadcn/ui primitives – do NOT edit unless adding variants
  components/dashboard/ # Dashboard-specific components
  contexts/            # React Context providers
  hooks/               # Custom hooks (use-kebab-case.ts)
  integrations/supabase/ # Auto-generated – NEVER edit client.ts or types.ts
  lib/                 # Utilities, static data, type definitions
  pages/               # Route-level page components
supabase/
  functions/           # Deno edge functions
  config.toml          # Auto-managed – do NOT edit
```

## Critical Rules

### Imports
- Always use `@/` path alias (e.g., `import { Button } from "@/components/ui/button"`)
- Never use relative paths like `../../`

### Design System – MANDATORY
- All colors MUST use HSL CSS variables from `src/index.css`
- Use semantic Tailwind classes: `bg-primary`, `text-foreground`, `border-muted`, etc.
- NEVER hardcode hex/rgb/hsl values in components (e.g., no `text-white`, `bg-black`, `#ff0000`)
- Custom colors must be added to `tailwind.config.ts` referencing CSS vars
- Fonts: Sora (display), Inter (body), JetBrains Mono (code)

### Components
- Named exports only (`export const MyComponent = ...`)
- One component per file, filename matches component name
- Use shadcn/ui primitives from `src/components/ui/` as building blocks
- Animations via Framer Motion (`motion.div`, `AnimatePresence`)

### State Management
- Auth state: `useAuth()` hook from `@/contexts/AuthContext`
- Server state: React Query (`useQuery`, `useMutation`)
- Static tool catalog: `@/lib/data.ts` – update here when adding tools
- Tool types: `@/lib/types.ts`

### Supabase / Backend
- Import client: `import { supabase } from "@/integrations/supabase/client"`
- NEVER edit `src/integrations/supabase/client.ts` or `types.ts`
- NEVER edit `supabase/config.toml` or `.env`
- Edge functions go in `supabase/functions/<name>/index.ts` (Deno runtime)
- Always add RLS policies to new tables
- User roles must be in a separate `user_roles` table, never on profiles

### Dependencies
- Use `bun add <package>` to install
- Verify docs/version with Context7 MCP before adding new packages
- Do not duplicate functionality already provided by installed packages

### Testing
- Vitest for unit tests in `src/test/`
- Test files: `*.test.ts` or `*.test.tsx`

### Do NOT
- Create files in `src/integrations/supabase/` beyond what exists
- Use `localStorage` for auth/role checks
- Store API keys in source code
- Use anonymous Supabase signups
- Modify shadcn/ui base components unless adding new variants
