---
name: property-testing
description: >
  Property-based tests: fast-check with Vitest in TypeScript, Hypothesis with pytest in Python.
  Writes new property tests, exposes a property in code that seems to have none, reviews
  existing property tests for ones that assert nothing, and triages a failed property test into
  a wrong property, an ambiguous spec or a real bug. Use it when the owner asks for property
  tests or for inputs the existing tests miss: "write property tests for this parser", "find
  the edge cases this function misses", "test the invariants", "tests are green but prod breaks
  on odd input", "model-based test for this state machine or cache", "do these property tests
  check anything real", "my property test failed, is it a bug or a wrong property". Also use it
  on your own in test-first work when the function has an inverse, normalizes or sorts, does
  arithmetic over money or limits, parses data through a schema, or holds state. Not for binary
  fuzzing (libFuzzer, AFL), mutation testing, benchmarks or end-to-end UI tests.
metadata:
  version: "1.0.0"
---

# Property-based tests

An example test checks the inputs someone thought of. A property test states what must hold
for every input, lets the library generate hundreds of inputs it would take a person weeks to
think of, and when one breaks the statement, shrinks it to the smallest case that still breaks
it: not a list of three hundred elements but `[0]` with `n = 2`. That minimal case points at
the bug directly.

Property tests complement example tests, they do not replace them. One property test per
function that has a clear property; everything else stays example-based. Do not convert
existing example tests, do not add properties to glue code. Code with no property gets example
tests, and saying so is a valid outcome.

A green property test is not a proof. It says the generator found no counterexample in the
runs it made, over the domain you described; it does not say none exists. Its strength is
exactly the honesty of the generator. Report it that way: "no counterexample in a hundred
runs over inputs of this shape", never "correct for all inputs".

The method is the same in every language. The first part of this skill is the method; the two
sections at the end are the tooling for TypeScript and for Python. Read the method, then the
section for the project's language.

## When it fits

The shape of the function tells you both whether a property test is worth it and which
property to state.

| Shape of the function | Property to state |
| --- | --- |
| Has an inverse: serialize/parse, encode/decode, save/load, cursor encode/decode | Round-trip: back and forth returns the original |
| Normalizes, sorts, deduplicates, merges, brings to canonical form | Idempotence: applying twice equals once; plus invariants: length, membership, ordering |
| Arithmetic over money, quotas, limits, pagination | Invariants: totals preserved, never negative, no item lost or duplicated across pages; metamorphic: double the prices, the total doubles |
| Takes input from a human or an external system | Totality over the channel: everything the spec allows is extracted in full, everything else is rejected with the project's own error, nothing is crashed on or silently truncated |
| Parses external or stored data through a schema | Every generated valid value is accepted; round-trip through the schema; invalid input fails with the project's own error, never crashes |
| Builds state from a stream of events or messages | Order of arrival does not matter, duplicates do not matter; model-based against a simple reference |
| Holds state and takes a sequence of operations: queue, cache, run lifecycle | Model-based: the system agrees with a simple reference model after every step |
| Several async actors inside one process: jobs, sockets, concurrent writes | Race detection: the final state does not depend on the order in which operations complete |

It does not fit markup and layout, thin glue between libraries, anything that needs an external
service (that is an integration test), and functions with no statable property beyond "returns
something". Before concluding the shape is missing, check whether it is merely buried: a
calculation wrapped in I/O, a string built by concatenation, an in-place mutation each have a
property and no seam to assert it through. See `references/expose-a-property.md`.

## Choose the property

This is a checklist you run against the function yourself, not questions for the owner. Go
through it in order; the first line that matches the function names the property. A non-trivial
function usually matches two or three lines, and together those properties pin its contract
better than any list of examples.

1. **Is there an inverse?** Round-trip: `parse(serialize(x))` equals `x`.
2. **Does applying it twice equal applying it once?** Idempotence: `f(f(x))` equals `f(x)`.
3. **What must not change?** Invariant: same length, same multiset of elements, sum preserved,
   output ordered, every input point still covered.
4. **Does the order of operations matter?** Different paths, same destination: normalize then
   add equals add then normalize; for binary operations, commutativity, associativity, a
   neutral element; for event streams, any arrival order gives the same state.
5. **How does a known change of input change the output?** Metamorphic relation: append one
   element, the count grows by exactly one; scale every price by two, the total doubles.
6. **Is the answer hard to compute but easy to check?** Verify instead of recompute: tokens
   concatenated give back the text; the output is sorted and is a permutation of the input.
7. **Is there a slow but surely correct implementation, or the previous version?** Oracle:
   compare against it on every input.
8. **Is the function not obviously pure?** Determinism: `f(x)` equals `f(x)`. A tautology for
   a pure function, a real property for a serializer over sets or maps, for hashing, for
   anything that reads the clock or depends on iteration order.
9. **Nothing else?** The last resort: it does not crash on any input, and when it rejects, the
   error is the project's own error type with its code. Catch only the documented error and
   let everything else fail the test.

Properties differ in strength, weakest to strongest: no crash, type preserved, invariant,
idempotence, round-trip or oracle. Assert the strongest property the code supports. If all you
can find is "no crash", that alone rarely justifies a property test: either a small
rearrangement exposes something stronger (see `references/expose-a-property.md`), or the
honest report is that this code is a poor candidate. Rule out the first before settling for
the second.

## The two ways a property asserts nothing

- **Tautology.** `assert add(a, b) === a + b` restates the implementation; no bug they share
  can fail it. A property must constrain the function without recomputing it: use an
  independent oracle or a structural invariant. The exception is determinism (line 8 above),
  which looks like a tautology and is not when the function is not obviously pure.
- **Vacuity.** A precondition that discards nearly every generated input passes without
  exercising anything, and a self-contradictory one passes having run zero cases. A
  precondition that pins the input to a single value is an example test wearing a property's
  clothes. Push constraints into the generator so it produces valid inputs directly.

## Prove the property can fail

Before trusting a new property, plant a bug in the function: drop the last chunk, shift a
boundary by one, swap two branches. Run the test, see it go red with a counterexample, revert
the bug. A property that stays green with a bug in place is not a test; it is a green light
that lies. This step is not optional and takes a minute.

## Build the input by construction

The input is described by generators (arbitraries in fast-check, strategies in Hypothesis):
primitives, containers, choices among variants, transformations of a generated value into
another, and recursion for tree-like data such as JSON.

Build validity in, do not filter it out. A pair where the first is not greater than the second
comes from mapping a tuple through a sort, or from drawing the second value from a range that
starts at the first. Filtering is for the rare condition that cannot be expressed as a
generator, usually a relationship between two values already drawn; heavy filtering makes runs
slow and unstable, trips the library's health checks with a warning nobody reads in CI, and
hides the fact that the generator does not describe the domain.

**Generate from the boundary, not from the type.** For anything a human or an external system
sends, the domain is what the channel can carry, not what the handler wants to receive. A
free-text field can carry any string: three identifiers separated by commas, an identifier next
to a company name, plain words. A webhook can carry any JSON shape, any count of items, any
encoding. Describe that channel in the generator, embedding valid tokens into arbitrary
surroundings, and state the property as totality: everything the specification allows is
extracted in full (all three identifiers, not the first one), everything else is rejected with
the project's own error, and nothing crashes or is silently truncated. The generator that only
produces what the code expects finds nothing, and the first real user finds the rest.

**Every production incident becomes a pinned example.** The exact input that broke production
goes into the relevant property test as a permanent example, next to the generator, so the
case is checked on every run for as long as the test exists.

Pin the boundaries you already know about the same way: empty, a single element, all
duplicates, zero, a negative value, the maximum representable value. Random generation finds
them eventually; an explicit example finds them on every run and documents that you thought
about them.

Defaults that bite in both libraries: floating-point generators include `NaN` and infinities
unless told otherwise; plain string generators may not cover emoji and surrogate pairs, use the
full-unicode variant when the code meets real user text; dates carry time zones and pre-1970
values. Cap sizes (lengths, ranges) at what the domain actually allows, so that shrinking lands
on readable cases.

Money is generated as integers in minor units (cents, kopecks) and compared exactly. If the
code under test keeps money in floating point, generate integers anyway, convert at the edge,
and say in the report that comparison with a tolerance is a compromise forced by the code, not
the norm.

Domain objects come from the same generators mapped into the project's constructors. A
generator for a domain type is a shared test double: write it once and keep it where the
project keeps its shared test doubles, next to the type's contract, not copied into each test
file. Five slightly different generators for one type is the usual way property tests rot.

For a schema (zod, pydantic, a JSON schema), write the generator by hand to mirror the schema
and use the schema itself as the first property: every generated value passes validation. Do
not assume a generator-from-schema library works with the project's schema version; verify or
write by hand.

Verify the exact API against the library version installed in the project (its docs in the
installed package or the site for that version), not from memory. Names in the tooling
sections are the stable core; options and signatures move between majors.

## Order of arrival: streams, events, messages

State built from a stream is where production surprises cluster: message bubbles rendered out
of order, an update applied before the record it updates, a replay after reconnect doubling
entries. The reason is that the code was tested with events in the order the developer sent
them, and the network sends them in any order and sometimes twice.

The properties, for a reducer that folds events into state:

- **Any arrival order, same state.** Generate a valid sequence of events with their sequence
  numbers, then a permutation of it; folding the permuted sequence gives the same state as
  folding the original. This is line 4 of the checklist applied to streams.
- **Duplicates change nothing.** Folding the sequence with some events repeated (a reconnect
  replay) gives the same state as folding it once. Idempotence over delivery.
- **A snapshot plus deltas equals the full history.** For resync protocols: the state built from
  a snapshot at position k plus the events after k equals the state built from all events.
  Model-based testing fits here, with "a list ordered by sequence number" as the model.
- **Gaps are visible.** If the protocol has sequence numbers, a missing one is detected and
  reported, not papered over.

How to test it: when the reducer is synchronous, a permutation generator over the event array
is enough and runs fast. When delivery is asynchronous (promises, sockets, jobs), use the
scheduler in fast-check: it wraps the promises and reorders their resolution, so the property
"the final state is the same for every order" is checked against real async code. The
generator must produce realistic streams: interleaved sessions, bursts, a late event with a
low sequence number, the same event twice.

## Where property tests stop

Races between processes and containers are not property-testable: a container that starts
before a module it depends on has loaded, a gateway that has not yet received an account when
the backend first calls it. A test runs inside one process and controls nothing about how
services come up. Those failures are prevented by readiness contracts (a service counts as up
only when its readiness check answers, and dependants wait for that, not for the process to
exist), by bounded retries at the boundaries, and are caught by an integration test of the
startup itself.

What is property-testable is the in-process part: once the coordination logic is a function of
the sequence of readiness events (rearrangement 6 in `references/expose-a-property.md`), the
scheduler tests it for order
independence. Say in the report which part is covered by the property and which part is not,
and name the readiness contract or integration test that covers the rest. Never report a
cross-process race as "covered" because an in-process property passed.

## Stateful systems: model-based

For a queue, a cache, a run lifecycle, a resync protocol, test sequences of operations instead
of single calls. Describe each operation as a step that applies to both the real system and a
reference model and asserts they agree; the library generates random sequences of steps and
shrinks a failing sequence to the shortest one.

The model is a deliberately simple reference: a map, a list, a counter. It is not a second copy
of the system. When the system has a policy the model must know about (eviction in an LRU
cache, a limit that rejects), put that policy into the model, otherwise the two diverge at the
first eviction and the test reports a bug that is not there. Check invariants after every step,
not only at the end.

## Proportion, placement, dependency

One property is one test, named with the property in words: "merge keeps every input point
covered", not "property test 3". The test lives next to the code, under the project's own
naming convention. In test-first work the property is written before the implementation and
goes red first.

Run counts: the library default is right for a local run and for a shared, slow CI runner; a
property test runs the function a hundred times per run. Raise it only for a specific function,
in that test, with a comment saying why, or in a separate slow job if the project has one.
Never fix the seed permanently; that turns a property test back into an example test.

If the project already uses a property-testing library, write the tests in it; a second one is
not worth the property you wanted to write. If it uses none, adding one is a dependency
decision that belongs to the owner: offer it once, with the specific property you would write,
and take the answer either way.

## Where to look next

The sections above cover writing a new property test. Three other situations have their own
file; open the one that matches the task in front of you, not all three.

| Situation | File |
| --- | --- |
| The code seems to have no property to assert | `references/expose-a-property.md` |
| A property test failed: wrong property, ambiguous spec or real bug | `references/triage-a-failure.md` |
| Asked whether existing property tests check anything real | `references/review-existing-tests.md` |

## Pitfalls

- Restating the implementation in the property.
- Non-determinism inside the property that is not the thing under test: current time, random
  numbers, network calls. Fixed input must give a fixed verdict.
- A trivially true property, unaffected by any bug. Caught by the plant-a-bug step.
- Over-filtering where the generator should construct.
- A generator that describes what the code expects instead of what the channel can carry.
- Unbounded sizes, so the counterexample is unreadable and the run is slow.
- Converting example tests, or adding properties to code with no property.

## Before you report, check yourself

Long instructions get skimmed; these five are the ones that get dropped in practice.

- Every known boundary and every production incident is pinned as an explicit example next
  to the generator. A property test with no pinned examples is not finished.
- Generators for domain types live where the project keeps its shared test doubles, next to
  the type's contract. The test file holds properties, not hundreds of lines of scaffolding.
- Each property was shown to go red on a planted bug, and the report names which bug.
- The report says "no counterexample in N runs over inputs of this shape", names what the
  properties do not cover, and brings an open contract gap to the owner as a decision. A gap is
  not buried in the suite as an expected-failure test.
- One property test per function with a clear property; example tests untouched; no dependency
  added without the owner's word.

## TypeScript: fast-check with Vitest

- Plain `fc.assert(fc.property(...arbitraries, predicate))` inside an ordinary `it`;
  `fc.asyncProperty` when the predicate awaits. A promise returned from `fc.property` instead
  of `fc.asyncProperty` means the assertion never runs. No wrapper package: the Vitest binding
  is a 0.x package and adds nothing this method needs.
- Arbitraries: `fc.integer()`, `fc.nat()`, `fc.double()`, `fc.string()`, `fc.boolean()`,
  `fc.date()`, `fc.array()`, `fc.record()`, `fc.tuple()`, `fc.oneof()`, `fc.constantFrom()`,
  `.map()`, `.chain()`, `fc.letrec()` for recursion; `fc.shuffledSubarray()` and permutations
  built with `.chain()` for arrival-order properties. Rare exclusions: `fc.pre()`.
- Known boundaries, incidents and pinned counterexamples: the `examples` parameter of
  `fc.assert`. Replay: `seed` and `path` from the failure report, only while debugging.
- Model-based: commands with `check`, `run` and `toString`, generated by `fc.commands()`,
  executed by `fc.modelRun()` or `fc.asyncModelRun()`.
- Async order: `fc.scheduler()` wraps promises and reorders their resolution; the property is
  that the final state is the same for every order, or follows the documented conflict rule.

## Python: Hypothesis with pytest

- `@given(...)` with strategies from `hypothesis.strategies as st` on an ordinary test function;
  the assertion is a plain `assert`.
- Strategies: `st.integers()`, `st.floats(allow_nan=False, allow_infinity=False)`, `st.text()`,
  `st.booleans()`, `st.dates()`, `st.lists()`, `st.dictionaries()`, `st.tuples()`,
  `st.one_of()` or `a | b`, `st.sampled_from()`, `st.from_regex(..., fullmatch=True)`,
  `st.builds()` for domain objects, `.map()`, `@st.composite` for dependent values, `st.data()`
  for draws that depend on what the test already drew, `st.recursive()` for trees,
  `st.permutations()` for arrival-order properties, `st.binary()` against decoders for the
  error path. Rare exclusions: `assume()`.
- Known boundaries, incidents and pinned counterexamples: `@example(...)` on the test. Full
  determinism only while debugging: `@seed(...)`. The local example database replays known
  failures first on every run.
- Budget: `@settings(max_examples=..., deadline=...)`. The default deadline of 200 ms turns a
  slow machine into a failing test; set `deadline=None` for anything doing real work. A
  health-check warning means fix the strategy, not silence the check.
- Model-based: `RuleBasedStateMachine` with `@rule` steps, `@invariant` checks after every step,
  `Bundle` for entities created by one rule and consumed by another; expose it as
  `TestX = MyMachine.TestCase`.
- Worst-case search: `target(value)` steers generation towards inputs that maximize a measured
  quantity, for example run time, to find slow or oversized inputs. Hypothesis has no scheduler
  for reordering async completions; async arrival-order races are tested with fast-check only,
  synchronous reducers with `st.permutations()`.
