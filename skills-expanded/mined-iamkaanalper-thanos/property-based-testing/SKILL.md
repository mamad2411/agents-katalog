---
name: property-based-testing
description: Property-based testing (PBT) patterns with fast-check (JS/TS), Hypothesis (Python), and gopter (Go). Generate random inputs, define invariants, shrink failures to minimal cases. Grok-native with Production Contract, hooks, compound, palace.
when-to-use: When testing pure functions, parsers, serializers, state machines, or any code where example-based tests miss edge cases. Pair with tdd-guide, test-enforcement, arbiter, mocksmith.
---

# Property-Based Testing (Grok Port)

Instead of hand-picking examples, define properties that must hold for ALL inputs in a domain. Frameworks generate hundreds/thousands of cases (including adversarial) and shrink failures to the smallest reproducible case. Grok-native: Production Contract, friction from "our tests looked good but missed the zero/empty/unicode case", compound to shared arbitraries, palace for "why PBT was required for this module".

## When to Use PBT
| Use Case             | Example Property |
|----------------------|------------------|
| Serialization        | `deserialize(serialize(x)) === x` |
| Sort                 | Output ordered AND same elements |
| Parser / Encoder     | Never crashes on valid input; roundtrips |
| State machine        | Invariants hold after any command sequence |
| Math / Financial     | Associativity, commutativity, bounds |
| API handler          | Never 500 on valid input (with generated payloads) |
| Data transform       | Output schema matches spec for any input |

When NOT to use: UI rendering (use visual), integration with external services (use contract), business scenarios that need specific stories (use example + BDD), oracle as complex as impl.

## fast-check (JS/TS)
```ts
import fc from 'fast-check';

test('sort is idempotent', () => {
  fc.assert(
    fc.property(fc.array(fc.integer()), (arr) => {
      const sorted = [...arr].sort((a, b) => a - b);
      expect(sorted).toEqual([...sorted].sort((a, b) => a - b));
    })
  );
});

test('JSON roundtrip', () => {
  fc.assert(fc.property(fc.jsonValue(), (v) => {
    expect(JSON.parse(JSON.stringify(v))).toEqual(v);
  }));
});
```

Custom arbitraries + adversarial:
```ts
const adversarialStringArb = fc.oneof(
  fc.constant(''), fc.constant('\0'), fc.constant('<script>alert(1)</script>'),
  fc.constant("Robert'); DROP TABLE users;--"), fc.unicodeString()
);
```

Stateful / model-based testing (cache vs Map model) is powerful for complex state.

## Hypothesis (Python)
```python
from hypothesis import given, strategies as st, settings

@given(st.lists(st.integers()))
def test_sort_preserves_length(xs):
    assert len(sorted(xs)) == len(xs)

@settings(max_examples=1000, deadline=None)
@given(st.dictionaries(st.text(), st.integers()))
def test_dict_roundtrip(d):
    import json
    assert json.loads(json.dumps(d)) == d
```

## gopter (Go)
```go
func TestSortIdempotent(t *testing.T) {
    properties := gopter.NewProperties(gopter.DefaultTestParameters())
    properties.Property("sort is idempotent", prop.ForAll(
        func(xs []int) bool {
            sorted := make([]int, len(xs)); copy(sorted, xs); sort.Ints(sorted)
            sortedTwice := make([]int, len(sorted)); copy(sortedTwice, sorted); sort.Ints(sortedTwice)
            return reflect.DeepEqual(sorted, sortedTwice)
        },
        gen.SliceOf(gen.Int()),
    ))
    properties.TestingRun(t)
}
```

## Shrinking (the killer feature)
When a property fails, the framework automatically shrinks the input to the smallest case that still fails. This tells you exactly which edge (zero, empty, unicode, negative, max-int, etc.) exposed the bug.

## Grok Integration (Production Contract)
- Primary: tdd-guide + test-enforcement (arbiter) + mocksmith (generate arbitraries for fixtures).
- Fire on_test or on_linter_friction when coverage passes but mutation or real bugs still slip through.
- Pre-Flight (recommended for pure logic, parsers, serializers, state machines): "Have we considered PBT for the core transformation? What invariants must hold for all inputs? Do we have custom arbitraries for domain types (email, money, order states)?"
- Ledger: for critical modules, record "PBT added, key properties: X,Y,Z, mutation score improved from 72% to 91%".
- Handoff: list of properties, custom arbitraries, "shrunk failures we had to fix", integration notes (how to run with fast-check/hypothesis in CI).
- Friction + compound: every "our 100% coverage tests missed the empty list + negative case" or "unicode in name broke the CSV export" → compound to "add PBT for all pure data transforms" rule or shared arbitrary library.
- Palace: "Required PBT + model-based for the cache + state machine layer because example tests never caught rebalance + concurrent set/delete races; rejected pure example tests after the 2025 incident".
- Claim-verification: Two-pass. Grep "fc.property" or "@given" → read_file actual test file + run the PBT suite (or at least see shrunk counterexample in history) → "Property 'sort idempotent' with adversarial inputs exists at tests/sort.pbt.ts:12 and last run found no counterexample ✓VERIFIED". Never claim "edge cases covered" without reading the properties + seeing the framework actually exercised the domain.
- Pair with: mutation-testing (PBT + mutation = very strong signal), test-enforcement, tdd-workflow, mocksmith, preflight, compound-learnings.

## When to Activate
- New pure functions, serializers, parsers, state machines, or complex data transforms.
- After coverage is green but you still feel nervous about edges.
- In TDD flows for algorithmic or protocol code (tdd-guide / arbiter).
- When mutation testing reveals weak assertions.
- Swarm Phase 2 (test-heavy tracks) + Phase 3.

See .grok/skills/mutation-testing/SKILL.md, test-enforcement, tdd (various), preflight. Run PBT in CI with enough examples; keep at least one "shrunk failure" as regression test. Production Contract: friction capture + ledger for PBT on critical logic.

PBT finds the bugs your brain didn't think to write a test for. Use it where the input space is large and the oracle is cheap.
