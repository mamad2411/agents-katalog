---
name: tdd-with-feedback-loops
description: Implement features or fixes using test-first development with strict vertical slicing — one failing test, smallest passing change, then typecheck and lint and tests as the full feedback loop, then refactor. Use when implementing any non-trivial logic, when fixing bugs that need a regression test, or when working in unfamiliar code. Works equally well from a PLAN.md or directly from a clear user request. Skip for typo fixes, dependency bumps, or one-line changes.
---

# TDD with Feedback Loops

The rate of feedback is the speed limit. AI implementation goes wrong when it generates many lines of code before checking anything. This skill forces small steps with the full feedback loop after each one.

Test-first not because tests are the goal, but because tests force you to specify behavior before producing code. The cycle is:

> RED → GREEN → typecheck → lint → tests → REFACTOR → repeat

Not just RED-GREEN-REFACTOR. The full feedback loop runs every cycle, not at the end of the session.

## Process

For each behavior to implement:

1. **Write ONE failing test** that verifies one behavior through the public interface. Run it, confirm it fails for the *right reason* (not a syntax error, not a missing import — actually the behavior gap).
2. **Write the smallest code** that makes the test pass. No speculative features. No "while I'm here." If you find yourself writing more than ~20 lines, stop and split the test.
3. **Run the full feedback loop:** typecheck, lint, tests. All three must pass before continuing. If lint or typecheck breaks somewhere unrelated to your change, fix it now — don't accumulate breakage.
4. **Refactor only after green.** Improve naming, remove duplication, deepen modules. Run the feedback loop again after refactor.
5. **Move to the next test.** What did you learn from this cycle that changes what to test next?

Vertical slicing: one test → one implementation → one feedback loop → repeat. Never "write all tests then write all code" (horizontal slicing).

## Rules

- **Tests verify behavior through public interfaces.** A test that breaks when you rename an internal function but behavior is unchanged is testing implementation, not behavior. Rewrite it.
- **Confirm the test fails for the right reason** before writing implementation. A test that fails on a syntax error or missing import is not yet a useful test.
- **Never refactor while RED.** Get to GREEN first. Refactoring while broken loses the safety net.
- **Run typecheck and lint, not just tests.** AI-generated code frequently passes its own test while breaking types or lint in adjacent files. The full loop catches this.
- **Don't mock internal collaborators.** Mocking your own modules ties tests to implementation. Mock only the boundaries you don't own (HTTP, time, randomness, external services).
- **One test per cycle.** Writing two tests before implementing means you're committing to a structure before you've validated it. Slice vertically.
- **Minimal code per cycle.** If passing the test took 50 lines of new code, the test was too big. Split it.
- **No speculative features.** "While I'm here, I'll also add..." is how AI implementations balloon. The next test will tell you if more is needed.
- **Stop and ask if you don't know enough to write the test.** Tests written without understanding the behavior become tautologies — "function returns 5 when called with 5" tells you nothing. If neither the user's request nor any available SPEC/PLAN tells you what behavior to expect, ask the user.

## What good and bad tests look like

**Good test (behavior, public interface, durable):**

```typescript
test("user can checkout a cart with valid items", async () => {
  const cart = await createCart({ userId: "u1", items: [{ sku: "A", qty: 2 }] });
  const order = await checkout(cart.id);
  expect(order.status).toBe("placed");
  expect(order.totalCents).toBe(2000);
});
```

This test would survive any internal refactor of cart, order, or pricing modules. It describes capability.

**Bad test (implementation, internals, fragile):**

```typescript
test("checkout calls calculatePricing then createOrder then sendEmail", async () => {
  const calculatePricing = vi.spyOn(pricing, "calculatePricing");
  const createOrder = vi.spyOn(orders, "createOrder");
  const sendEmail = vi.spyOn(email, "sendEmail");
  await checkout("c1");
  expect(calculatePricing).toHaveBeenCalled();
  expect(createOrder).toHaveBeenCalledTimes(1);
  expect(sendEmail).toHaveBeenCalledTimes(1);
});
```

This test breaks when you rename `calculatePricing`, when you move pricing inline, when you batch emails — none of which change observable behavior. It tests *how* checkout works, not *what* it does.

## Pre-coding checklist

Before writing the first test, confirm:

- [ ] I know which public interface this behavior is exposed through. If unclear, ask the user briefly to confirm — or, for a multi-module change, consider `planning-by-modules` to design the surface first.
- [ ] I have a list of behaviors to implement, ordered (most foundational first).
- [ ] I know the build, test, lint, and typecheck commands. If `CONTEXT.md` (or similar) exists, check it; otherwise discover them from `package.json`/`Makefile`/`pyproject.toml` or ask the user.
- [ ] I have agreed with the user on which behaviors are critical to test versus nice-to-have. You can't test everything; focus on what matters.

## Per-cycle checklist

For each test:

- [ ] Test describes a behavior, not an implementation step
- [ ] Test uses only the public interface
- [ ] Test would survive an internal refactor
- [ ] Test fails for the right reason before implementation
- [ ] Implementation is minimal — no speculative features
- [ ] Typecheck passes after green
- [ ] Lint passes after green
- [ ] All tests pass after green (not just the new one)

## Anti-patterns to refuse

- **Horizontal slicing.** Writing all tests first, then all implementations. Refuse to do this even if asked. Vertical only.
- **Mocking your own modules.** If a test needs to mock another module you own, the seam is in the wrong place. Either expand the test scope or refactor the seam.
- **Tests that assert on internals.** Checking which functions were called, what private fields hold, or what database rows look like (instead of what the API returns) — all coupled to implementation.
- **Snapshot tests for complex objects.** They pass for the wrong reasons and fail for the wrong reasons. Assert on the specific behavior that matters.
- **Running tests but skipping typecheck and lint.** A green test with type errors is a half-passing change. The cycle isn't done.

## When you can't write a test first

Sometimes you genuinely don't know what the behavior should be until you try something. In that case:

1. Write a small spike (throwaway code) to learn what's possible. Don't commit it.
2. Discard the spike.
3. Now write the test based on what you learned, then implement.

Don't keep the spike code and retroactively write tests. The tests will follow the implementation's shape instead of driving it.

## Post-output instruction

After completing a session of TDD work, summarize:

> Implemented N behaviors via N RED-GREEN cycles. All tests, typecheck, and lint pass. New tests in: <files>. Remaining behaviors not yet implemented: <list> (drawn from PLAN.md if one exists, otherwise from the original request).
