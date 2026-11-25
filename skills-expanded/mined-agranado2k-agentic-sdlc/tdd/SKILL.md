---
name: tdd
description: Test-driven development with red-green-refactor loop. Use when user wants to build features or fix bugs using TDD, mentions "red-green-refactor", wants integration tests, or asks for test-first development.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
metadata:
  phase: tester
---

# Test-Driven Development

> **Project context — read these first, they are the parts this file cannot know:**
>
> - **Test runner, tiers, and conventions**: `constitution/local-engineering.md`. It names the command that runs the suite, the file-naming convention the runner actually collects, and which tier a given behavior belongs in. A test written to a convention your runner does not collect **silently never runs** — that is the single most expensive mistake available here, so check before you write the first file.
> - **What counts as source, and what counts as its paired test**: `scripts/guards.config.sh`. Those two regexes are the machine-readable version of "this change needed a test", and everything below is the procedure that keeps you on the right side of them. Keep them in step with your runner's include globs: a tree the runner covers but the guards' policy file doesn't is silently un-guarded.
> - **Code craft**: `constitution/shared-code-craft.md`. The portable rules the GREEN and refactor steps are held to. The review's standards axis reads with that file open; write with it open too.
> - **Domain language**: `docs/domain-glossary.md`. Assertions and test names use those names. Do not invent local aliases inside test files — a second name for one concept is a distinction waiting to be invented.
> - **Decision records**: `docs/adr/`. Respect the ones covering the area you're touching; a test that contradicts a binding decision is a finding, not a green.
> - **The enforcement layer**: `.githooks/pre-push` runs `scripts/tdd-pairing-guard.sh`, which blocks a push whose source changes carry no test changes; `scripts/tdd-pairing-guard-ci.sh` runs the same rule over the pull request, so a local bypass only defers the failure. **This skill provides the *procedure*; the hook and the workflow provide the *enforcement*.** They are not a substitute for each other: the guard checks that a test file moved, never that the test is any good.
>
> Shared invariant §3 is the reason all of this exists: the test suite **is** the signal an agent optimizes for, so it is the specification, not an afterthought — and the testing infrastructure is the ceiling on how correct any agent's output can be.
>
> The rest of this file is universal advice, adapted from the upstream skill named at the bottom.

---

## Philosophy

**Core principle**: Tests should verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't.

**Good tests** are integration-style: they exercise real code paths through public APIs. They describe _what_ the system does, not _how_ it does it. A good test reads like a specification - "user can checkout with valid cart" tells you exactly what capability exists. These tests survive refactors because they don't care about internal structure.

**Bad tests** are coupled to implementation. They mock internal collaborators, test private methods, or verify through external means (like querying a database directly instead of using the interface). The warning sign: your test breaks when you refactor, but behavior hasn't changed. If you rename an internal function and tests fail, those tests were testing implementation, not behavior.

A test that cannot fail is worse than no test: it converts an unknown into a false "verified" (shared invariant §3).

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Anti-Pattern: Horizontal Slices

**DO NOT write all tests first, then all implementation.** This is "horizontal slicing" - treating RED as "write all tests" and GREEN as "write all code."

This produces **crap tests**:

- Tests written in bulk test _imagined_ behavior, not _actual_ behavior
- You end up testing the _shape_ of things (data structures, function signatures) rather than user-facing behavior
- Tests become insensitive to real changes - they pass when behavior breaks, fail when behavior is fine
- You outrun your headlights, committing to test structure before understanding the implementation

**Correct approach**: Vertical slices via tracer bullets. One test → one implementation → repeat. Each test responds to what you learned from the previous cycle. Because you just wrote the code, you know exactly what behavior matters and how to verify it.

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
  ...
```

## Workflow

### 1. Planning

When exploring the codebase, use `docs/domain-glossary.md` so that test names and interface vocabulary match the project's language, and respect the decision records in `docs/adr/` covering the area you're touching.

Before writing any code:

- [ ] Confirm with user what interface changes are needed
- [ ] Confirm with user which behaviors to test (prioritize)
- [ ] Identify opportunities for [deep modules](deep-modules.md) (small interface, deep implementation)
- [ ] Design interfaces for [testability](interface-design.md)
- [ ] List the behaviors to test (not implementation steps)
- [ ] Get user approval on the plan

Ask: "What should the public interface look like? Which behaviors are most important to test?"

**You can't test everything.** Confirm with the user exactly which behaviors matter most. Focus testing effort on critical paths and complex logic, not every possible edge case.

### 2. Tracer Bullet

Write ONE test that confirms ONE thing about the system:

```
RED:   Write test for first behavior → test fails
GREEN: Write minimal code to pass → test passes
```

This is your tracer bullet - proves the path works end-to-end.

### 3. Incremental Loop

For each remaining behavior:

```
RED:   Write next test → fails
GREEN: Minimal code to pass → passes
```

Rules:

- One test at a time
- Only enough code to pass current test
- Don't anticipate future tests
- Keep tests focused on observable behavior

Record each step as you take it — after the test ran, never before: `sh scripts/trace.sh emit kind=tdd.cycle outcome=red|green|refactor data.test='<the test name>' reason='<the behavior this test pins, one line>' || :`. One event per RED, per GREEN and per refactor step (the next section's), so a cycle is readable later without the transcript. The trace is written here and never read (the kit's ADR-0008); unconfigured, the call is a silent no-op.

### 4. Refactor

After all tests pass, look for [refactor candidates](refactoring.md):

- [ ] Extract duplication
- [ ] Deepen modules (move complexity behind simple interfaces)
- [ ] Apply SOLID principles where natural
- [ ] Consider what new code reveals about existing code
- [ ] Run tests after each refactor step

**Never refactor while RED.** Get to GREEN first.

And keep the refactor out of the behavior commit (shared invariant §10) — a refactor-only pass is its own commit, with the suite green before and after.

## Checklist Per Cycle

```
[ ] Test describes behavior, not implementation
[ ] Test uses public interface only
[ ] Test would survive internal refactor
[ ] Code is minimal for this test
[ ] No speculative features added
```

---

*Adapted from `engineering/tdd` in [mattpocock/skills](https://github.com/mattpocock/skills) — MIT, see `.agents/skills/LICENSE-mattpocock-skills.md`. The project-context prelude above is this kit's; the four sidecars are verbatim; `deep-modules.md`'s two diagrams are redrawn as fenced diagram-language blocks, since craft rule §10 forbids character art
