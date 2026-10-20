# Unit Test Writing

## Purpose
Writes unit tests following TDD workflow for UseCases and Repositories.

## Role
Backend Developer

## Phase
Development (write BEFORE implementation — part of `tdd-workflow`)

## Triggered By
`tdd-workflow` step 6.

## Inputs
- Pseudo code / planned classes from `tdd-workflow`

## Process
Tools: Vitest (bun test compatible). Framework: Arrange-Act-Assert (AAA) pattern.

### Test File Locations
- UseCase tests: `apps/servers/{service}/src/usecases/{Operation}UseCase.test.ts`
- Repository tests: `apps/servers/{service}/src/repositories/{Entity}Repository.test.ts`

### Mocking Strategy
- Mock: external gRPC clients, Kafka broker, Redis (use `vi.mock`)
- Real: business logic inside UseCase/Repository

Coverage target: ≥ 80% new code (SonarQube gate).

### Test Structure Per UseCase
```typescript
describe('{Operation}UseCase', () => {
  // Arrange: setup mocks and dependencies

  it('should {expected behaviour} when {condition}', async () => {
    // Arrange: specific test data
    // Act: call the UseCase
    // Assert: verify outcome
  })

  it('should throw {error} when {invalid condition}', async () => {
    // Test error paths
  })

  it('should handle {edge case}', async () => {
    // Test edge cases from AC
  })
})
```

## Outputs
Unit test suite per UseCase/Repository, written before implementation.

## Quality Gates
- [ ] Tests written before implementation
- [ ] Happy path tested
- [ ] Error paths tested
- [ ] Edge cases from AC tested
- [ ] All mocks properly cleaned up between tests

## References
- `.claude/skills/backend-developer/tdd-workflow/SKILL.md`
- `.claude/skills/backend-developer/component-integration-test-writing/SKILL.md`
