---
name: code-smells
description:
  This skill should be used when a piece of code has a structural problem
  and you need to name what is wrong and which refactoring fixes it,
  recognising the bad smells catalogued by Beck and Fowler (Refactoring,
  2nd ed., 2018). Use it whenever the situation involves a structural
  suspicion about code, however it is phrased: "this smells",
  "duplicated code", "this function is too long", "too many parameters",
  "this class does everything", "feature envy", "magic values everywhere",
  "hard to change without breaking things", "this is messy",
  "every change breaks something else", "this class knows too much about
  another", or any variant that signals a code quality concern, even when
  Fowler is not named. Composable with your own conventions.
---

# Code smells

Chapter 3 of Fowler's *Refactoring*, co-authored with Kent Beck
(Fowler, *Refactoring*, 2nd ed., 2018, Chapter 3), names 24 bad smells:
patterns that signal structural problems without prescribing an exact fix.
A smell is a hint, not a rule; context determines whether and how to act.
The sections below group the 24 smells into five pedagogical families.
These groupings are an organising aid; they are not Fowler's own structure.

## Bloaters

Code that has become hard to understand, through size or obscurity.

- **Mysterious Name.** A name (function, variable, field, or class) that
  does not reveal what it does or holds. Remedies: Change Function
  Declaration (Rename Function), Rename Variable, Rename Field.
- **Long Function.** A function long enough that its full logic is hard to
  hold in one reading. Remedies: Extract Function, Replace Temp with Query,
  Decompose Conditional, Replace Conditional with Polymorphism, Split Loop.
- **Long Parameter List.** A function with so many parameters that each
  call site is hard to read and easy to misinvoke. Remedies: Replace
  Parameter with Query, Preserve Whole Object, Introduce Parameter Object,
  Remove Flag Argument, Combine Functions into Class.
- **Large Class.** A class carrying too many responsibilities, too many
  fields, or too many methods. Remedies: Extract Class, Extract Superclass,
  Replace Type Code with Subclasses.
- **Data Clumps.** The same cluster of data items appearing together in
  multiple places (as fields, parameter lists, or local variables). Remedies:
  Extract Class, Introduce Parameter Object, Preserve Whole Object.
- **Primitive Obsession.** Using primitive values (strings, numbers, booleans)
  where a small domain object would enforce constraints and communicate intent.
  Remedies: Replace Primitive with Object, Replace Type Code with Subclasses,
  Introduce Parameter Object, Replace Conditional with Polymorphism,
  Combine Functions into Class.

## Object-orientation abusers

Code that misuses or sidesteps object-oriented mechanisms.

- **Repeated Switches.** The same conditional logic duplicated across several
  places so that adding a case requires changes everywhere. Remedy: Replace
  Conditional with Polymorphism.
- **Temporary Field.** A field set only under special circumstances and empty
  the rest of the time, creating null checks and confusion throughout the
  class. Remedies: Extract Class, Introduce Special Case.
- **Refused Bequest.** A subclass that ignores or overrides most of what it
  inherits, suggesting the hierarchy is wrong. Remedies: Push Down Method,
  Push Down Field, Replace Subclass with Delegate.
- **Alternative Classes with Different Interfaces.** Two classes doing similar
  things with different method signatures that prevent substitution. Remedies:
  Change Function Declaration, Move Function, Extract Superclass.

## Change preventers

Structural forces that make a single logical change cascade into many edits.

- **Divergent Change.** A class that must be opened for several unrelated
  reasons, each requiring a different set of functions to change. Remedies:
  Split Phase, Move Function, Extract Function, Extract Class.
- **Shotgun Surgery.** A single logical change that requires small edits
  scattered across many different classes. Remedies: Move Function, Move Field,
  Combine Functions into Class, Combine Functions into Transform, Inline
  Function.
- **Global Data.** Data reachable from anywhere in the codebase with no
  access control, so any code can change it. Remedy: Encapsulate Variable.
- **Mutable Data.** Shared mutable state that can be altered from many places,
  producing unexpected side effects at a distance. Remedies: Encapsulate
  Variable, Split Variable, Separate Query from Modifier, Remove Setting
  Method, Replace Derived Variable with Query, Combine Functions into Class,
  Change Reference to Value.

## Dispensables

Code that adds no value and should be removed or simplified.

- **Duplicated Code.** The same code structure appearing in more than one
  place, so bugs must be fixed in every copy. Remedies: Extract Function,
  Slide Statements, Pull Up Method.
- **Lazy Element.** A function or class that does so little it does not
  justify the indirection. Remedies: Inline Function, Inline Class,
  Collapse Hierarchy.
- **Speculative Generality.** Abstractions added for anticipated future needs
  that have never materialised. Remedies: Collapse Hierarchy, Inline
  Function, Inline Class, Change Function Declaration, Remove Dead Code.
- **Loops.** A loop that performs a transformation or filter where a pipeline
  expresses intent more directly. Remedy: Replace Loop with Pipeline.
- **Data Class.** A class with only fields and accessors and no real
  behaviour of its own. Remedies: Encapsulate Record, Remove Setting Method,
  Move Function, Extract Function, Split Phase.
- **Comments.** Comments that explain what the code does rather than why,
  compensating for code that is not self-explanatory. Remedies: Extract
  Function, Change Function Declaration, Introduce Assertion.

## Couplers

Excessive or inappropriate dependencies between classes.

- **Feature Envy.** A function more interested in the data of another class
  than its own class. Remedies: Move Function, Extract Function.
- **Message Chains.** A long navigation chain (a.b().c().d()) to reach the
  data you actually want. Remedies: Hide Delegate, Extract Function,
  Move Function.
- **Middle Man.** A class whose interface is dominated by methods that simply
  delegate to another class. Remedies: Remove Middle Man, Inline Function,
  Replace Superclass with Delegate, Replace Subclass with Delegate.
- **Insider Trading.** Two classes that know too much about each other's
  internals. Remedies: Move Function, Move Field, Extract Class, Hide
  Delegate.

## Smells as triggers, not rules

Each smell is a prompt to investigate, not a mandate to refactor
(Fowler, *Refactoring*, 2nd ed., 2018, Chapter 3). A Long Function is
sometimes the right level of detail for its context. A Comment sometimes
documents a genuine constraint that cannot be expressed in code. The
rule of three applies: if a smell appears repeatedly, the cost of acting
rises with each recurrence. If it appears once and the code is clear in
context, the right call may be to leave it. Smells guide judgement;
they do not replace it.

## Overlap with clean-code, solid-principles, and simplicity-principles

Many smells name the same problems from a different angle. Feature Envy
and Insider Trading relate to the Single Responsibility and Dependency
Inversion principles from `solid-principles`. Duplicated Code, Lazy
Element, and Speculative Generality are the targets that
`simplicity-principles` (YAGNI, DRY, KISS) works to prevent. Mysterious
Name and Long Function are central concerns of `clean-code`. Use those
skills for the design target; use this skill for the diagnostic signal.
The three are complementary, not redundant.

## Guardrails

- **Smells name symptoms, not causes.** Act on the underlying structural
  problem; do not treat the smell label as a mandate.
- **Never refactor without a test net.** Verify that the affected behaviour
  is under test before acting on any smell. If it is not, apply `legacy-code`
  first to establish a characterization test net.
- **One smell at a time.** A sweep that addresses multiple smells in a single
  commit makes failures untraceable. Fix one smell per commit and keep the
  bar green at each step.
- **Some smells are tolerated by convention.** Comments may be required by
  a style guide. Global configuration may be unavoidable. Record agreed
  exceptions in your project `CLAUDE.md` rather than silently overriding
  this skill.
- **Do not chase smells in code you are not already touching.** Opportunistic
  refactoring applies when you are working in the neighbourhood, not as a
  sweeping cleanup campaign across unrelated modules.

## Relationship to other skills

- **`refactoring-method`**: the mechanics of safe refactoring: the two hats,
  small steps, the test net, when not to refactor. This skill is the
  diagnostic; that one is the method.
- **`refactoring-catalog`**: the complete set of named refactorings with
  step-by-step mechanics and TypeScript examples. Use this skill to identify
  which smell you face; use that one for the mechanics of the chosen
  refactoring.
- **`clean-code`**, **`solid-principles`**, **`simplicity-principles`**:
  the target qualities that refactoring works toward. Those skills describe
  what well-factored code looks like; this skill names the signals that
  indicate you are not there yet.
- **`legacy-code`**: when the code exhibiting smells has no test coverage,
  that skill establishes a characterization test net first. Return here
  to diagnose once the bar is green.
- **`test-driven-development`**: when a smell is identified during a TDD
  cycle, the refactor step is the moment to act. The two skills compose
  naturally.

## Adapt to your context

This skill stays generic on purpose. Your team may set different thresholds:
tolerating longer functions in test files, accepting global configuration
constants, or agreeing to keep certain Data Classes as simple value
containers. Declare those in your own `CLAUDE.md` or a higher-priority
skill, which overrides this baseline. This skill does not impose specific
thresholds.

## Reference

For the full smell-to-refactorings reference table covering all 24 smells
(signal, why it hurts, and recommended refactorings per smell) and
TypeScript before/after examples for Long Function, Duplicated Code, Long
Parameter List, Feature Envy, and Primitive Obsession, read
`references/code-smells.md`.
