---
name: property-based-testing
description: Writes property-based tests with generators, invariants and shrinking for parsers, serializers and pure logic where example tests miss edge cases.
---

# Property based testing

Find a rule that must always hold, then let a generator attack it.

## Steps

1. Pick the library already in the project, or the standard one for the language (fast-check, Hypothesis, jqwik, gopter or rapid, proptest). Do not add a second.
2. Write the property in one plain sentence before any code. Good shapes:
   - round trip: `decode(encode(x)) == x`
   - idempotence: `normalize(normalize(x)) == normalize(x)`
   - invariant: output length, sum or sort order is preserved
   - oracle: the fast version equals a naive, obviously correct version
   - no crash: arbitrary input returns a value or a documented error, never an unhandled exception
3. Build generators for the domain, not raw strings: valid records, boundary numbers (0, -1, max, NaN), unicode, empty and huge collections. Constrain with filters sparingly, since heavy filtering wastes runs.
4. Run at least 200 cases locally and more in CI. Keep the seed printed on failure.
5. When a property fails, use the shrunk counterexample: decide whether the code or the property is wrong, fix it, and keep the counterexample as a plain example test.

## Rules

- A property must not recompute the implementation. That proves nothing.
- Never swallow the library's seed or disable shrinking.
- Keep each property to one rule.

## Report

The properties added, the generators, any bug found with its shrunk input, and the run count used.
