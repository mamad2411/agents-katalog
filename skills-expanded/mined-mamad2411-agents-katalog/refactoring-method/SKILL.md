---
name: refactoring-method
description:
  This skill should be used when improving the design of existing code without
  changing its observable behaviour, applying the two hats (adding function
  versus refactoring, never both at once), understanding why and when to refactor,
  working through the rule of three, applying preparatory, comprehension, or
  litter-pickup refactoring, working under a test net with small
  behaviour-preserving steps, or deciding when not to refactor. Use it whenever
  the situation involves cleaning up or improving code structure, however it is
  phrased: "clean this up", "improve this design", "refactor this", "this code
  is messy", "this is hard to read", "I want to make this easier to change",
  "can we simplify this", or "this needs a rework", even when Fowler is not
  named. Use alongside `code-smells` for diagnosis and `refactoring-catalog`
  for move mechanics. Composable with your own conventions.
---

# Refactoring Method

Refactoring is the discipline of improving the internal structure of existing
code without changing its observable behaviour. Fowler's second edition
(with Kent Beck, 2018) is the definitive treatment. This skill covers the
method: the definition, the two hats, why and when to refactor, the test net,
and the mechanics of small steps.

## Definition

Fowler gives two forms (Fowler, *Refactoring*, 2nd ed., 2018, Chapter 2):

- **Noun.** A refactoring is a specific change made to the internal structure
  of software to make it easier to understand and cheaper to modify, without
  changing its observable behaviour.
- **Verb.** To refactor is to restructure software by applying a series of
  refactorings without changing its observable behaviour.

The constraint is strict: the visible input-output contract of the code does
not change. If behaviour changes, the move is not a refactoring; it is a bug
fix or a feature addition. The definition keeps the word precise and the
practice safe.

## The two hats

Kent Beck's metaphor divides development time into two modes
(Fowler, *Refactoring*, 2nd ed., 2018, Chapter 2). When **adding function** you are writing
new behaviour: you write new tests for the intended behaviour, which start
failing until you implement the feature, while existing tests stay green. When **refactoring** you are changing only structure: no new
tests, and every existing test must stay green after every step.

You can wear only one hat at a time. Switching hats is fine and frequent.
Know which hat you are wearing at each moment. Mixing the two in a
single step conceals the source of any test failure: you cannot tell whether
a regression came from the structural change or from the new behaviour. The
resolution is to undo everything and restart with a clear separation.

## Why refactor

Refactoring pays off in four ways (Fowler, *Refactoring*, 2nd ed., 2018, Chapter 2):

1. **Design.** Code designed once drifts without maintenance. Refactoring keeps
   the design aligned with the current problem.
2. **Readability.** Code is read far more than it is written. Improving names,
   extracting small functions, and removing duplication reduces the cognitive
   load of the next reader.
3. **Bug detection.** Restructuring forces a close reading. Bugs hiding in
   tangled code surface when you tease it apart.
4. **Speed.** Well-factored code is easier to extend. The short-term cost of
   refactoring is recovered in reduced friction on all subsequent changes.

The **Design Stamina Hypothesis** captures the long-term case: neglecting design
trades long-term productivity for a short-term burst. Projects that invest in
good design sustain higher velocity for longer. The payoff line is typically
reached within weeks, not months (Fowler, *Refactoring*, 2nd ed., 2018, Chapter 2; see also
https://martinfowler.com/bliki/DesignStaminaHypothesis.html).

## When to refactor

### The rule of three (Don Roberts)

The first time you do something, just do it. The second time, do it again but
notice the duplication. The third time, refactor (Fowler, *Refactoring*, 2nd ed., 2018,
Chapter 2). The rule keeps premature abstraction in check while giving
duplication a bounded lease.

### Opportunistic refactoring

Most refactoring should arise during other work, not be scheduled separately
(Fowler, *Refactoring*, 2nd ed., 2018, Chapter 2). The three opportunistic modes:

- **Preparatory.** Before adding a feature, refactor the code into a structure
  that makes the feature easy to add. Fowler: "The best time to refactor is
  just before I add a new feature." The refactoring is justified by the work
  it enables, not as an end in itself.
- **Comprehension.** While understanding a piece of code, move that
  understanding into the code: rename a variable, extract a well-named
  function, clarify a condition. The next reader inherits your understanding
  rather than reconstructing it.
- **Litter-pickup.** If you encounter something messy during other work and
  fixing it takes a minute, fix it now. If it takes longer, note it and come
  back. The camp-site rule: leave the code a little better than you found it.

### Planned refactoring

Reserve planned refactoring sessions for areas so entangled that opportunistic
moves cannot make a dent. Keep sessions bounded: a clear scope, a time limit,
and a specific target state. A team doing opportunistic refactoring consistently
rarely needs large planned sessions.

### Long-term refactoring

Large architectural changes, such as moving a subsystem across a boundary or
splitting an overgrown module, take weeks or months to complete. The key
constraint throughout is that the code must remain deployable at every point
during the transition. Branch by Abstraction provides the technique: grow a
new structure in parallel with the old, use a flag to control which is live,
and remove the old once the new is stable (Fowler, *Refactoring*, 2nd ed.,
2018, Chapter 2). For the full treatment of this and the other
when-to-refactor categories, see `references/refactoring-method.md`.

## The test net as prerequisite

Refactoring without tests is guesswork. The test suite is the mechanism by
which each small step is verified safe (Fowler, *Refactoring*, 2nd ed., 2018, Chapter 2).
Before refactoring any piece of code, confirm that tests cover the behaviour
you intend to preserve and that they all pass.

If the code lacks tests, apply the `legacy-code` skill first to establish a
characterization test net via seams and enabling points. Return here once the
bar is green. For the general TDD loop and writing tests for new behaviour,
defer to `test-driven-development`; this skill covers the refactoring steps
that follow a green bar.

## Mechanics in small steps

Move in the smallest step the transformation allows
(Fowler, *Refactoring*, 2nd ed., 2018, Chapter 1). After each step:

1. Compile (if the language requires it) and run the full test suite.
2. If all tests pass, commit or checkpoint and proceed to the next step.
3. If any test fails, undo the step immediately; diagnose before proceeding.

Reversibility is the point. Any failing test points to the one small change
just made, not to an accumulation of unrelated edits.

A typical sequence of moves:

1. **Extract Function** or **Extract Variable** to pull out a well-named piece.
2. **Rename** (variable, function, parameter) for clarity.
3. **Inline Variable** or **Inline Function** to remove an indirection that
   adds no information.
4. **Move Function** or **Move Field** to place code near the data it operates
   on.
5. **Replace Temp with Query** to remove mutable temporaries.
6. **Split Phase** to separate two concerns across a clear intermediate data
   structure.

For the complete catalogue of named moves with mechanics and TypeScript
examples, see the sibling skill `refactoring-catalog`.

## When not to refactor

- **Code you are about to rewrite.** If a section is scheduled for deletion
  or complete replacement, refactoring it first adds cost with no benefit.
- **Code you are not touching.** Opportunistic refactoring applies when you are
  already in the neighbourhood. Do not seek out unrelated code to improve.
- **Under a hard deadline.** When time genuinely runs out, defer the
  refactoring and record the debt explicitly. A half-refactored function is
  harder to read than either the original or the finished version.

## Guardrails

- **Never refactor without a test net.** A structural change with no tests in
  place is not a refactoring; it is a structural change with unknown
  consequences.
- **One hat at a time.** If a refactoring exposes a bug, stop. Note the bug,
  restore the green bar, and address it through a separate cycle with its own
  test. Do not fix bugs as a side-effect of refactoring.
- **Small steps, not large ones.** A change that takes more than a few minutes
  without a green bar is a change waiting to go wrong. Decompose it.
- **Do not use refactoring to explore unfamiliar code.** If you do not yet
  understand the code well enough to know what to extract, use comprehension
  refactoring to read and annotate first, then refactor from understanding.
- **Track performance separately.** Refactoring can change performance on hot
  paths. Measure before and after; do not sacrifice readability for speculative
  performance gains without measurement.

## Relationship to other skills

- **`code-smells`**: the catalogue of symptoms that signal the need for
  refactoring, each pointing to the refactoring moves that address it
  (Beck and Fowler, *Refactoring*, 2nd ed., 2018, Chapter 3). Use it to
  diagnose which move to apply; use this skill for the method and mechanics.
- **`refactoring-catalog`**: the complete set of named moves with condensed
  mechanics and TypeScript examples. This skill is the method; that one is
  the toolbox.
- **`test-driven-development`**: the red-green-refactor loop, of which
  refactoring is the third step. The two skills compose: TDD governs when to
  write code; this skill governs how to improve it once the bar is green.
- **`testing-strategy`**: self-testing code is the prerequisite for safe
  refactoring; `testing-strategy` decides the shape and balance of that test
  suite.
- **`legacy-code`**: when the code to be refactored has no tests, that skill
  covers how to get it under test first via seams and characterization tests.
  Return to this skill once the test net is in place.
- **`clean-code`**, **`solid-principles`**, **`simplicity-principles`**: the
  destination properties refactoring works toward. Refactoring is the
  mechanism; those skills name the target qualities.
- **`simple-design`**: Beck's four rules of simple design are what the refactor
  step aims at. This skill is the method; `simple-design` is the priority-ordered
  target the mechanics drive the code toward.
- **`object-calisthenics`**: its nine rules are drills whose moves this skill
  owns (Extract Function, guard clauses, Encapsulate Collection, Hide Delegate)
  and whose target smells it catalogues (Primitive Obsession, Message Chains).
  That skill is the exercise; this one is the mechanics.

## Adapt to your context

This skill stays generic on purpose. Your team may have preferred naming
conventions for extracted functions, agreed limits on step size before
committing, or specific moves to avoid in certain contexts. Declare those in
your own `CLAUDE.md` or a higher-priority skill, which overrides this
baseline. This skill does not impose them.

## Reference

For a condensed, TypeScript-annotated walk through Fowler's chapter-1
theatrical-players example showing the full sequence of small refactorings
with the test net called out at each step, plus extended notes on the two
hats and the full when-to-refactor taxonomy, read
`references/refactoring-method.md`.
