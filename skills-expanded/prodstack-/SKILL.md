# prodstack — Cursor/Windsurf Rules

## Architecture
- Backend: Convex. All data access goes through Convex queries/mutations/actions.
- Auth: @convex-dev/auth. Always use requireAuthUserId(ctx) in Convex functions.
- Admin: requireAdminUser(ctx) for admin-only Convex functions.
- Routing: protected routes defined in utils/constants.ts, enforced by middleware.ts.

## Code conventions
- Use cn() from @/lib/utils for all Tailwind class merging.
- Use shadcn/ui components from @/components/ui — never raw HTML equivalents.
- Use react-hook-form + zod for all forms.
- Use sonner toast() for all user feedback.
- All Convex functions must call requireAuthUserId or requireAdminUser.
- Never hardcode user IDs — always derive from ctx.

## File naming
- Convex functions: convex/<tableName>.ts (e.g. convex/users.ts)
- Route pages: app/(authenticated)/<route>/page.tsx
- Components: components/<name>/index.tsx or components/ui/<name>.tsx

## Imports
- Use @/ path alias for all imports from project root.
- Import Convex API from @/convex/_generated/api.

## Testing
- Run before committing: pnpm typecheck && pnpm test && pnpm build
- Convex unit tests: convex/__tests__/*.test.ts (uses convex-test)
- Frontend tests: app/**/__tests__/*.test.tsx (uses @testing-library/react)
- E2E: pnpm e2e (requires running Convex + Next.js dev servers)

## Themes
- CSS vars in app/globals.css — do not hardcode colors in components.
- Use Tailwind semantic tokens (bg-background, text-foreground, etc.).
- Theme presets: neutral (default), ocean, forest — set via data-theme on html.
