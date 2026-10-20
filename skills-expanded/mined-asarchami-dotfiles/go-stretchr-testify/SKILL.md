---
name: go-stretchr-testify
description: "testify assertions — assert vs require selection, mock expectations, argument matchers, call verification, suite lifecycle, Eventually, JSONEq, custom matchers. Use when writing tests or mocks with stretchr/testify, choosing between assert and require, setting up test suites, or reviewing existing testify code for misuse."
license: MIT
---

# stretchr/testify

**Leading word: assert.** Tests are executable specifications — every assertion constrains behavior and makes a failure self-explanatory. The discipline: choose the failure mode deliberately (require for preconditions, assert for verifications), state expectations as `(expected, actual)`, and verify every mock you install. testify complements `testing`; it never replaces `*testing.T`.

## Steps — write tests

1. **Choose `assert` vs `require` for each line.** `assert` records a failure and continues (see all failures at once); `require` calls `t.FailNow()`. Use `require` for preconditions where continuing would panic or mislead — setup, error checks — and `assert` for verifications. Never mix randomly.
   *Done when: every precondition uses `require` and every verification uses `assert`, with a stated reason per line.*

2. **Name the assertion objects `is` and `must`.** `is := assert.New(t)`, `must := require.New(t)` keep both failure modes reachable in one test.
   *Done when: assert and require both appear through named handles where the test needs them.*

3. **Write `(expected, actual)` in that order.** testify assumes this order; swapping produces backwards diff output.
   *Done when: every assertion passes the expected value first and the actual value second.*

4. **Assert errors by walking the chain.** `ErrorIs(err, sentinel)` / `ErrorAs(err, &target)` for wrapped errors, `NoError` for success, `ErrorContains` for message text — not `Equal(err, sentinel)`.
   *Done when: no wrapped-error comparison uses `Equal` on error values.*

5. **Poll async state with `Eventually` / `EventuallyWithT`.** Give a timeout and a tick interval; use `EventuallyWithT` for rich assertions inside the poll.
   *Done when: every asynchronous check polls with an explicit deadline instead of `Sleep` + one-shot assert.*

## Steps — write mocks

1. **Embed `mock.Mock` and record expectations.** Implement interface methods with `m.Called()`; declare expectations with `On(...)`.
   *Done when: every mocked method forwards through `Called()` and every expectation is declared before the code under test runs.*

2. **Match arguments deliberately.** `mock.Anything` where the value doesn't matter, `mock.AnythingOfType("T")` for type-only checks, `mock.MatchedBy(func)` for predicates. Constrain with `.Once()`, `.Times(n)`, `.Maybe()`, `.Run(func)`.
   *Done when: each expectation's matcher admits exactly the calls it should and rejects calls it shouldn't.*

3. **Verify every mock.** Call `AssertExpectations(t)` at the end of the test — otherwise unmet expectations pass silently.
   *Done when: no mock in the test runs without `AssertExpectations`.*

## Steps — set up suites

1. **Group related tests with shared setup.** Embed `suite.Suite`, initialize dependencies in `SetupTest`, tear down in `TearDownTest`; use `SetupSuite`/`TearDownSuite` for once-only work.
   *Done when: each suite's lifecycle covers the shared state it creates.*

2. **Add the launcher function.** `suite.Run(t, new(MySuite))` is required — without it, zero tests execute silently.
   *Done when: every suite has a launcher and `go test -run TestMySuite` executes its tests.*

3. **Mix failure modes via the suite.** `s.Equal(...)` behaves like `assert`; use `s.Require().NotNil(...)` where continuing would panic.
   *Done when: every guard in the suite goes through `s.Require()`.*

## Steps — review or audit

1. **Scan for `assert` used as a guard.** A test that continues after a failed precondition dereferences nil. *Done when: no `assert` guards a value the next line dereferences.*
2. **Check error assertions.** `Equal(sentinel, err)` on wrapped errors fails silently — replace with `ErrorIs`/`ErrorAs`. *Done when: every error assertion walks the chain.*
3. **Check pointer comparisons.** `Equal(ptr1, ptr2)` compares addresses — dereference or use `EqualExportedValues`. *Done when: no assertion compares pointer addresses where values are meant.*
4. **Run `testifylint`.** It catches wrong argument order and assert/require misuse. *Done when: testifylint reports nothing.*

## Reference

### Core assertions

```go
is := assert.New(t)

is.Equal(expected, actual)              // DeepEqual + exact type
is.EqualValues(expected, actual)        // converts to common type first
is.EqualExportedValues(expected, actual)
is.Nil(obj)                 is.NotNil(obj)
is.True(cond)               is.False(cond)
is.Empty(collection)        is.NotEmpty(collection)
is.Len(collection, n)
is.Contains("hello world", "world")     // strings, slices, map keys
is.Greater(actual, threshold)   is.Less(actual, ceiling)
is.Error(err)                   is.NoError(err)
is.ErrorIs(err, ErrNotFound)    // walks error chain
is.ErrorAs(err, &target)
is.IsType(&User{}, obj)         is.Implements((*io.Reader)(nil), obj)
```

### Advanced assertions

```go
is.ElementsMatch([]string{"b", "a", "c"}, result)   // unordered
is.InDelta(3.14, computedPi, 0.01)                  // float tolerance
is.JSONEq(`{"name":"alice"}`, `{"name": "alice"}`)  // ignores whitespace/key order
is.WithinDuration(expected, actual, 5*time.Second)
is.Regexp(`^user-[a-f0-9]+$`, userID)
is.Eventually(func() bool { ... }, 5*time.Second, 100*time.Millisecond)
is.EventuallyWithT(func(c *assert.CollectT) {
    assert.NoError(c, err)
    assert.Equal(c, "shipped", resp.Status)
}, 10*time.Second, 500*time.Millisecond)
```

### Suite lifecycle

```
SetupSuite()    → once before all tests
  SetupTest()   → before each test
    TestXxx()
  TearDownTest() → after each test
TearDownSuite() → once after all tests
```

### Mock reference

- **[Mock reference](./references/mock.md)** — defining mocks, argument matchers, call modifiers, return sequences, and verification

## Watch for

| Mistake | Fix |
| --- | --- |
| Forgetting `AssertExpectations(t)` | Verify every mock expectation at the end of the test |
| `is.Equal(ErrNotFound, err)` on wrapped errors | Use `is.ErrorIs` to walk the chain |
| Swapped argument order | Always write `(expected, actual)` |
| `assert` for guards | Use `require` — stop before the nil dereference |
| Missing `suite.Run()` | Add the launcher or zero tests run silently |
| Comparing pointers | Dereference or use `EqualExportedValues` |

## Cross-references

- → See `go-testing` for table-driven tests, fixtures, and CI
- → See `go-lint` for `testifylint` configuration
