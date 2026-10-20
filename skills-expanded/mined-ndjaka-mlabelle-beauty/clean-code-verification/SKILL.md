---
name: clean-code-verification
description: Use this skill when reviewing, refactoring, or finishing code in this project and the user asks for clean code, quality checks, verification, lint, TypeScript, unit tests, build, or a final audit before delivery.
---

# Clean Code Verification

## Workflow

1. Read the local project skills that apply:
   - `.agent/skills/project-context/SKILL.md`
   - `.agent/skills/architecture/SKILL.md`
   - `.agent/skills/component-generator/SKILL.md` for React components
   - `.agent/skills/booking-logic/SKILL.md` for booking behavior
   - `.agent/skills/database-rules/SKILL.md` for Supabase/database code
   - `.agent/skills/testing-rules/SKILL.md` before changing tests
2. Respect `AGENTS.md`: read the relevant Next.js docs in `node_modules/next/dist/docs/` before writing Next.js code.
3. Audit the changed files for the project rules below.
4. Fix issues before reporting success.
5. Run the full verification commands and summarize the result.

## Clean Code Checklist

Check components:
- Keep components focused and preferably under 150 lines.
- Extract repeated mobile/desktop blocks into shared components.
- Use `type` imports for types.
- Avoid inline React styles except inside email HTML strings.
- Use the shared `Button` component for CTA-style buttons.
- For backward navigation (like 'Back' buttons), use `useRouter().back()` from `next/navigation` instead of hardcoded `<Link href="/">` to preserve user flow context.
- Avoid `useEffect` for derived state when the URL, props, or memoized values can be the source of truth.

Check server/features:
- Keep `app/` routes thin: no direct Supabase calls and no business logic.
- Put Supabase reads in `features/*/queries.ts`, writes in `features/*/mutations.ts`, orchestration in `features/*/actions.ts`.
- Never trust client-provided duration, price, status, or availability.
- Revalidate booking availability on the server before inserting.
- Prefer database constraints for race-condition protection.
- Return user-friendly action errors; keep raw provider errors out of UI text.

Check database:
- Use explicit selected columns, not `.select('*')`.
- Preserve RLS.
- Add migrations for schema guarantees.
- Do not use raw SQL from application code; migrations are the right place for schema SQL.

## Required Commands

Run these before final delivery:

```bash
npm run lint -- --max-warnings=0
npx tsc --noEmit
npm test
npm run build
```

If one fails, fix the code and rerun the failing command. Final response must mention any command that could not be run.
