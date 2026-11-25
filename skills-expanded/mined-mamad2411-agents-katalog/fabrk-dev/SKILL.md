# Fabrk Boilerplate - Cursor IDE Rules

## Primary Instructions
Read CLAUDE.md in the project root for comprehensive AI agent instructions.

## Quick Reference

### File Structure
- src/app/ - Next.js App Router (pages, API routes, layouts)
- src/components/ - React components organized by feature
- src/lib/ - Utilities, services, and configurations
- prisma/ - Database schema

### Code Style
- TypeScript strict mode
- Functional components with hooks
- Server components by default, "use client" when needed
- Tailwind CSS with design tokens from globals.css
- **Terminal aesthetic**: rounded-none, font-mono, no hardcoded colors

### Naming Conventions
- kebab-case for files: user-profile.tsx
- PascalCase for components: UserProfile
- camelCase for functions: getUserProfile

### Component Pattern
```tsx
"use client"; // Only if client-side interactivity needed

import { mode } from "@/design-system";
import { cn } from "@/lib/utils";

interface Props {
  // Props definition
}

export function ComponentName({ prop }: Props) {
  return (
    <div className={cn(mode.radius, mode.font)}>
      {/* Implementation */}
    </div>
  );
}
```

### API Route Pattern
```ts
import { NextResponse } from "next/server";
import { auth } from "@/lib/auth";

export async function GET() {
  const session = await auth();
  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }
  // Implementation
}
```

### Environment Variables
```ts
import { env } from "@/lib/env";

// ✓ GOOD
const key = env.server.DATABASE_URL;

// ✗ BAD
const key = process.env.DATABASE_URL;
```

### Design System (Terminal Aesthetic)
- **No rounded corners**: Use `rounded-none` everywhere
- **Monospace font**: Use `font-mono` for all UI text
- **Design tokens only**: NO hardcoded colors (bg-white, text-gray-500, #hex)
- **8-point grid**: Spacing in multiples of 4px
- **Mode tokens**: Import from `@/design-system` for consistent styling

```tsx
import { mode } from "@/design-system";

// GOOD
<Button className={cn(mode.radius, mode.font, "text-xs")}>
  > SUBMIT
</Button>

// BAD - will fail pre-commit
<Button className="rounded-lg bg-purple-500">
  Submit
</Button>
```

### Testing
- npm test - Run Vitest unit tests
- npm run test:e2e - Run Playwright E2E tests
- Tests in *.test.ts or *.test.tsx files

### Common Commands
- npm run dev - Start development server (auto-kills port 3000)
- npm run build - Production build
- npm run lint - ESLint + hex color scan
- npm run type-check - TypeScript validation
- npm run scan:hex - Detect hardcoded colors

### Pre-Commit Hooks
Git commits automatically check:
- TypeScript compilation
- ESLint with auto-fix
- Prettier formatting
- No hardcoded colors
- No console.log statements
