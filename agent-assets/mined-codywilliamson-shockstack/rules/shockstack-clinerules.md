You are working in ShockStack, a convention-first monorepo template.

Tech: Astro 5, Vue 3, Tailwind 4, Better Auth, Drizzle ORM, optional .NET 10 backend.
Monorepo: Turborepo + pnpm workspaces.

Key paths:
- frontend/ — Astro 5 app
- backend/ — .NET 10 API (optional)
- packages/tokens/ — Style Dictionary design tokens

Commands: pnpm dev, pnpm build, pnpm test, pnpm tokens:build
Backend: dotnet build/test backend/ShockStack.slnx

Conventions:
- Conventional commits, pnpm only
- Tailwind 4 via @tailwindcss/vite
- CSS-first animations; JS motion allowed when CSS can't reasonably express it
- See docs/system/ for detailed docs
