---
description: Vitest, Playwright, fixtures — no live keys, do not delete tests
globs: "**/*.{test,spec}.{ts,tsx}"
alwaysApply: false
---

# Tests

- Vitest for `packages/*` (compiler, receipts, caps, branching, Zod IPC, adapters).
- Playwright for critical renderer flows when the wave’s UAT requires it.
- Adapter tests: recorded/fixture streams only. Never commit keys or call real providers in unit tests.
- New contract without a test is not done (compiler, receipts, spend caps, branching, import idempotency).

```ts
// ❌
it("streams", async () => { await openai.chat.completions.create(...) })

// ✅
it("writes interrupted receipt on abort", async () => {
  const stream = fixtureStream("partial-then-abort");
  await expect(runChat(stream, { abort: true })).resolves.toMatchObject({
    status: "aborted",
    receipt: { outputTokens: expect.any(Number) },
  });
});
```

Never delete or skip tests to get a green run. Fix the code or the fixture.
