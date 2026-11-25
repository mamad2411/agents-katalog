# Usecase Development

## Purpose
Creates the business logic layer between pages/hooks and Apollo Client.

## Role
Frontend Developer

## Phase
Development

## Triggered By
Complex business logic needed beyond simple data fetching.

## Inputs
- Story business logic requirements

## Process
Frontend UseCases live in `modules/{feature}/usecases/`. No fixed class form — unlike the backend UseCase pattern. These are React hook functions (`use` prefix) since they use React hooks.

### When to Create a Usecase (vs Just a Hook)
- Multiple Apollo operations need coordination
- Complex state transitions (multi-step forms, wizards)
- Business logic beyond simple data display
- Transformation between API data shape and UI data shape

### Pattern
```typescript
// modules/{feature}/usecases/use{Operation}.ts
export const use{Operation} = () => {
  const [mutate, { loading, error }] = useMutation({MUTATION})
  const { data } = useQuery({QUERY})

  const execute = async (input: {InputType}) => {
    // business logic here
    await mutate({ variables: { input } })
    // post-mutation actions
  }

  return { execute, loading, error, data }
}
```

## Outputs
Implemented usecase consumed by pages.

## Quality Gates
- [ ] Business logic in usecase (not in page or component)
- [ ] Uses generated types from packages/api/
- [ ] Returns stable interface for consuming components

## References
- `.claude/skills/frontend-developer/hook-development/SKILL.md`
- `.claude/skills/frontend-developer/page-development/SKILL.md`
