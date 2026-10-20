# Page Development

## Purpose
Creates route pages that compose components, hooks, and usecases without containing raw API calls or business logic.

## Role
Frontend Developer

## Phase
Development

## Triggered By
New route/page needed (from UI/UX `user-flow-definition`).

## Inputs
- `user-flow-definition` from UI/UX Designer

## Process
Pages location: `modules/{feature}/pages/`. Consumed by file-based router — do NOT manually register routes.

### Page Responsibilities
- Layout composition (which components go where)
- Route parameters reading (`useParams`, `useSearchParams`)
- Page-level error boundary (error state for the whole page)
- Loading states at page level

### Page NEVER Contains
- Raw Apollo Client calls (goes through usecase or hook)
- Business logic (goes in usecase)
- Database access or API endpoint strings

### Page Composition Pattern
```typescript
// modules/{feature}/pages/{Feature}Page.tsx
export const {Feature}Page = () => {
  const { data, loading, error } = use{Feature}()  // hook or usecase

  if (loading) return <LoadingState />
  if (error) return <ErrorState error={error} />

  return (
    <PageLayout>
      <{Feature}Component data={data} />
    </PageLayout>
  )
}
```

## Outputs
Implemented page component wired to file-based router.

## Quality Gates
- [ ] No raw Apollo calls in page components
- [ ] No business logic in page components
- [ ] Loading and error states handled
- [ ] Route auto-registered by file-based router (not manual)

## References
- `.claude/skills/ui-ux-designer/user-flow-definition/SKILL.md`
- `.claude/skills/frontend-developer/hook-development/SKILL.md`
- `.claude/skills/frontend-developer/usecase-development/SKILL.md`
