---
name: create-test-for-pr-comment
description: >
  For every GitHub PR review comment being fixed, add a focused regression test whose
  title matches the review subject (including P1/P2 priority), proves the failure mode
  before or after the fix, and lives next to the owning package tests. When the user
  pastes chatgpt-codex-connector / "New review comment on pull request" / !P1|!P2 Badge
  blocks, do NOT only write tests — auto-launch workflow name=fix-pr-comments with
  args.paste=full message (pairs with fix-pr-comments). Also use for /create-test-for-pr-comment
  alone when only tests are requested.
---

# Create Test for PR Comment

**Rule:** every actionable PR review comment that changes code gets **one named regression test** before the fix is considered done. No “fixed” without a test title you can cite on the PR reply.

## When to run

- User pastes one or more review comments (Codex, human, bot) → **prefer full `fix-pr-comments` workflow** with `args.paste` (tests are a step inside it, not a substitute)
- User runs `/create-test-for-pr-comment` only (tests without ship)
- While addressing PR feedback (`/fix-pr-comments`, `gh-address-comments`)

## Inputs

Collect for each comment:

| Field | Source |
|--------|--------|
| Priority | `P1` / `P2` badge or body |
| Subject | Bold title after the badge (e.g. `Reject nullable unique columns as mutation identities`) |
| Path / line | Review anchor (`path`, `line`) |
| Failure mode | What breaks if the bug remains |
| Fix surface | Module under test |

Skip only pure nits (typos, comment-only, already covered by an existing identically titled test).

## Naming convention (required)

Mirror the review subject so replies can cite it:

```text
P1: <exact review subject>
P2: <exact review subject>
```

Examples:

```ts
// packages/athena-js — node:test
test('P1: Reject nullable unique columns as mutation identities', async () => { ... })

// apps/web — vitest
it('P2: Preserve global FK order when grouping by schema', async () => { ... })
```

If the suite already uses a looser title, **rename** to this form when touching that area.

## Placement

| Change lives in | Prefer |
|-----------------|--------|
| `packages/athena-js` Cloudflare / D1 | `packages/athena-js/test/cloudflare-review-regression.test.ts` (or domain-specific `cloudflare-*.test.ts`) |
| Studio progressive DDL | `apps/web/app/lib/__tests__/ddlJob.test.ts` or `ddlProgressive.test.ts` |
| Scaffold / create-athena-app | `packages/create-athena-app/test/*.test.ts` |
| Other package | Existing test layout for that package; create `*-review-regression.test.*` if none |

Prefer **one regression file per PR theme** over scattering one-off names when the PR is large (see Athena PR #508 pattern).

## What the test must do

For each comment, encode the **original found case** from the review body (not a generic happy path).

1. **Reproduce the review scenario** with minimal fixtures (payloads, mocks, PRAGMA rows, SQL catalog mocks).
2. **Assert the corrected contract** (SQL shape, order, error code, type surface, phase order).
3. **Assert the anti-pattern is gone** when useful (`doesNotMatch`, `not.toContain`, rejected error code).
4. Stay **fast and hermetic** — no live network, no real D1/Postgres unless the suite already does.

## Red → green (required before “fixed”)

Order is non-negotiable:

```
1. Derive original case from the review (failure mode + minimal fixture)
2. WRITE the regression test first (title P?: <subject>)
3. RED  — run that test against current production code → must FAIL
4. FIX  — implement the production change
5. GREEN — run the SAME test → must PASS
6. Confirm the review failure mode is gone
```

- If the test **passes before the fix**, it does **not** cover the original case — rewrite and re-run red.
- Do **not** implement the production fix before red has failed for the right reason.
- If the bug is already fixed on the branch: temporarily re-expose the bug (local revert of the fix lines or call the old path), prove red, restore fix, prove green.

The `fix-pr-comments` workflow records `red_failed_as_expected` and `green_passed` per comment.

### Patterns by bug class

**Compiler / pure function**

```ts
test('P1: Preserve resource_id filters on D1 deletes', () => {
  const compiled = compileD1Delete({ /* review scenario */ })
  assert.match(compiled.sql, /"resource_id"/)
  assert.doesNotMatch(compiled.sql, /"id" = \?/)
})
```

**Runtime / transport with mocks**

```ts
test('P1: Reject partial unique indexes as mutation identities', async () => {
  const db = mockD1WithPartialUnique()
  await assert.rejects(
    () => resolveD1BoundedIdentityColumn(db, 'users'),
    (e) => e instanceof D1SqlCompileError && e.code === 'bounded_mutation_no_unique_identity',
  )
})
```

**Ordering / multi-object export**

```ts
it('P2: Preserve global FK order when grouping by schema', async () => {
  const entries = await fetchTablesDdlJob(...)
  const names = entries.map((e) => `${e.table.table_schema}.${e.table.table_name}`)
  expect(names.indexOf('b.parent')).toBeLessThan(names.indexOf('a.child'))
})
```

**Phase / pipeline order**

```ts
it('P2: Emit functions before table defaults that call them', async () => {
  // record phases in mocks, then:
  expect(phases.indexOf('functions')).toBeLessThan(phases.indexOf('relations'))
})
```

## Workflow (do this for every comment)

```
1. List comments → number them
2. For each actionable comment:
   a. Draft test title = "P?: <subject>"
   b. Write regression test for the ORIGINAL found case (before production edits)
   c. RED: run test → must fail while bug present
   d. Implement fix
   e. GREEN: run same test → must pass; issue gone
3. Commit tests + fix together when possible
4. PR reply cites: tip SHA, what changed, red→green, Proof: `<file>` — **P?: subject**
```

### Commit message fragment

```text
test: lock PR #N review regressions (P1 resource_id, P2 global FK order, …)
```

### PR reply template

```markdown
Fixed on tip <sha>.

<one sentence what changed>

Proof: `<test-file>` — **P1: <exact subject>**.
```

## Anti-patterns

- Fix without a test
- Fix **before** writing/running the red test
- Test that is green on buggy code (false coverage)
- Test title unrelated to the review subject
- Only testing the happy path when the review was about a failure mode
- Giant integration tests that hide the contract
- Claiming “covered by existing suite” without a title match or assertion that pins the bug
- Skipping red when “already fixed” without temporary re-exposure

## Checklist before “done”

- [ ] One test per actionable comment, encoding the original found case
- [ ] Titles match review subjects (`P1:` / `P2:`)
- [ ] Red run failed as expected before (or via temporary re-expose of) the fix
- [ ] Green run passed after the fix
- [ ] Relevant suite run is green
- [ ] PR reply can name file + test title + red→green
- [ ] Tests committed with or immediately after the fix

## Related skills

- `/fix-pr-comments` — implement fixes, commit, push, reply
- `gh-address-comments` — discover PR threads
- Domain skills (e.g. athena-js, progressive DDL) for *where* to put fixtures

See `references/title-mapping.md` for title → test-file conventions used on Athena PR #508.
