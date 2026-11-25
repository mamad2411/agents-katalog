---
name: legacy-dependency-breaking
description:
  This skill should be used when a class or method cannot be instantiated or exercised in a test because of its dependencies: heavy constructors, singletons, static calls, global state, or hidden side effects that make the code impossible to isolate. Use it to choose a specific dependency-breaking technique (Sprout Method, Wrap Method, Extract Interface, Parameterize Constructor, Subclass and Override Method, Break Out Method Object, and the full Feathers dependency-breaking catalogue), even when the technique is not named. Use it also when new behaviour must be added immediately alongside untested code without first bringing that surrounding code under test. For the overall approach to changing legacy code safely, including seam identification, characterization tests, effect sketching, and the five-step algorithm that calls these techniques at step three, use the sibling skill `legacy-code-changes`.
---

# Legacy Dependency Breaking

Breaking a dependency means creating a point where you can substitute one
behaviour for another in a test without editing the code in that place. Feathers
distinguishes two reasons to do it: to **sense** effects you cannot otherwise
observe, and to **separate** code you cannot get into a harness at all (Feathers,
*Working Effectively with Legacy Code*, 2004, Chapter 3). Those two reasons
determine which technique you reach for. This skill is the catalogue; the method
that places these techniques in context is the sibling skill `legacy-code-changes`.

## The two reasons: sensing and separation

**Sensing** is the problem when code does the work but you have no way to
observe the result in a test. A method may deposit a value into a field you
cannot access, send a side-effecting call to a collaborator you cannot intercept,
or return nothing useful. You need a seam so the test can inspect what happened.

**Separation** is the problem when you cannot instantiate the class under test
at all, or cannot exercise a method without triggering destructive side effects.
Heavy constructors, singletons that initialise globally, static calls into
infrastructure, and mandatory resource acquisition in construction all cause
separation failures. The class does not co-operate with the test harness.

Identifying which problem you face first directs you to the right group of
techniques. Many techniques address one problem more directly than the other,
though some help with both. Three questions route you to a group:

- **Can I construct the class at all?** If construction triggers the side effect,
  you face separation at construction time: see *Get a class into a test harness*.
- **Can I exercise the method I care about?** If you can build the object but a
  hidden dependency inside the method blocks you, or hides the result you need to
  observe, you face separation or sensing at method scope: see *Get a method under
  test*.
- **Do I just need to add behaviour now, without touching the untested code?**
  That is not a sensing or separation problem but a risk-management move: see *Add
  behaviour without touching existing code*.

## Add behaviour without touching existing code

When the surrounding code resists testing and you must add new behaviour now,
the lowest-risk move is to write the new behaviour in new, tested code and leave
the tangled old code untouched. Feathers calls these the safest first moves when
you cannot yet get the surrounding code under test (Feathers 2004, Chapter 6).

- **Sprout Method.** Introduce a new method for the new behaviour, call it from
  the existing method, and test the new method in isolation. The existing method
  gains one new call site and nothing else changes in it.
- **Sprout Class.** When the new behaviour has enough complexity or state to
  warrant its own type, sprout a new class instead of a method. Instantiate and
  test the new class independently.
- **Wrap Method.** Rename the existing method, write a new method with the
  original name that calls the renamed original and adds the new behaviour before
  or after. Callers see no change; the new behaviour is tested in the wrapper.
- **Wrap Class.** Apply the same interception at the class level using the
  Decorator pattern: a new class implements the same interface or inherits from
  the same type, delegates to the original, and adds behaviour. Use this when
  wrapping a single method is not enough or when you want a seam without
  modifying the original class at all.

Reach for Sprout when the new behaviour clearly belongs inside the existing
class but the surrounding code is not yet testable. Reach for Wrap when you
cannot safely modify the existing class at all.

For technique mechanics, see `references/add-without-touching.md`.

## Get a class into a test harness

Getting a class under test fails most often because of dependencies in
construction: a heavy initialiser that opens a database connection, calls a
remote service, starts a thread, reads from a singleton, or requires global
state you cannot replicate in a test. The fix is to break the dependency via an
interface, a parameter, or an override so the class can be constructed without
triggering the side effect (Feathers 2004, Chapter 9).

The most commonly needed techniques:

- **Extract Interface.** Pull the methods you depend on into an interface. The
  production class implements it; the test supplies an alternative implementation.
  This is the cleanest structural move and the most reusable seam.
- **Parameterize Constructor.** Move a dependency the constructor currently
  creates or looks up into a parameter. The constructor receives it rather than
  acquiring it. Add a convenience overload that supplies the production default.
  This is usually the fastest path to testability.
- **Introduce Instance Delegator.** Wrap a static call in an instance method
  so the call can be overridden in a subclass or replaced by an injected
  collaborator.
- **Introduce Static Setter.** When a singleton is genuinely difficult to
  replace with injection, add a test-only (marked `@internal`) setter that allows the test to
  substitute the instance. Use only as a last resort; injection is preferable.
- **Extract and Override Factory Method.** Move object creation from the
  constructor into a factory method, then override it in a test subclass to
  return a lighter substitute.
- **Supersede Instance Variable.** Add a setter (test-only) for a
  dependency that is currently assigned in the constructor. Lets the test
  replace the value after construction. Use only as a last resort; prefer
  Parameterize Constructor when the constructor can accept a parameter.
- **Pull Up Feature.** If a class inherits from a problematic base, pull the
  feature you want to test into a separate superclass that does not carry the
  dependency.
- **Push Down Dependency.** Move the problematic dependency into a subclass
  so the class you need to test no longer owns it directly.
- **Replace Global Reference with Getter.** Wrap direct access to a global or
  static variable in a protected getter. A test subclass overrides the getter.
- **Encapsulate Global References.** Group related global variables into a
  class and pass that class as a dependency.

For technique mechanics, see `references/get-a-class-into-a-harness.md`.

## Get a method under test

When you can construct the class but cannot exercise the method you care about
without triggering a hidden dependency, the dependency is buried inside the
method body rather than in construction. Open an object seam by making the
dependency substitutable (Feathers 2004, Chapter 10).

The most commonly needed techniques:

- **Subclass and Override Method.** In a test subclass, override the method that
  holds the problematic dependency and replace it with a neutral stub. The method
  under test calls `this.dependencyMethod()`, which the subclass intercepts. This
  is the most general object seam.
- **Extract and Override Call.** Extract the single problematic call into its
  own protected method and override that method in a test subclass. Narrower than
  Subclass and Override Method; it isolates exactly the dependency rather than
  the whole collaborating method.
- **Extract and Override Getter.** Extract access to a dependency into a
  protected getter and override it in a test subclass. Most useful when the
  dependency is a value or an object reference rather than a call.
- **Extract and Override Factory Method.** As a method seam rather than a
  constructor fix: extract object creation inside a method into a protected
  factory method and override it to return a substitute.
- **Parameterize Method.** Add a parameter to the method for a dependency it
  currently resolves internally. The test passes a substitute; callers keep the
  old signature via an overload that supplies the default.
- **Break Out Method Object.** Extract the method into a new class whose
  constructor receives the method's locals as parameters. The new class is easier
  to construct and test in isolation.
- **Adapt Parameter.** Introduce a thin wrapper interface over a parameter type
  that is difficult to construct or substitute, so the test can pass a simpler
  implementation.
- **Primitivize Parameter.** Replace a complex parameter with the primitive
  values actually used by the method, eliminating the need to construct the
  complex object in the test.

Language-specific techniques (named here; mechanics in the reference file): **Replace Function with Function Pointer** (C only), **Definition Completion** (C and C++ only), **Link Substitution** (link-seam builds only), **Template Redefinition** (C++ and generic-typed languages only), **Text Redefinition** (interpreted languages only). These are noted for completeness; they do not apply to TypeScript.

For technique mechanics, see `references/get-a-method-under-test.md`.

## Guardrails

- **These techniques are scaffolding, not the target design.** Their sole purpose
  is to create a seam so tests can attach. Once green, refactor toward clean
  dependency management: constructor injection, ports and adapters, explicit
  interfaces. Do not leave the code in the barely-testable state the seam
  created.
- **Prefer the least invasive seam.** Start with Parameterize Constructor or
  Extract Interface before reaching for static setters or global-state surgery.
  The less the seam touches, the less it can break.
- **Do not break dependencies in code you will not test.** Every seam you open
  is a change to production code. Keep that change minimal and mechanical. Do not
  open seams speculatively.
- **Keep breaking changes behaviour-preserving.** A dependency-breaking change
  must not alter observable behaviour. The tests you write afterwards verify that
  it did not.
- **Refactor once green, not before.** Breaking a dependency to get tests in is
  step three (break dependencies) of the five-step change algorithm in
  `legacy-code-changes`. Do not attempt to redesign the class at the same time;
  that is step five (make changes and refactor), protected by the tests you write
  in step four.

## Relationship to other skills

- **`legacy-code-changes`**: the overall method for changing legacy code safely.
  It provides the five-step algorithm that places dependency breaking at step
  three. If you are uncertain which step you are on or need to understand seams,
  sensing, and separation in context, start there. This skill is the toolbox;
  that one is the method.
- **`test-driven-development`**: once the seam exists and the class is under test,
  the standard red-green-refactor cycle resumes. TDD also introduces the seam
  concept and testable design patterns this skill exploits.
- **`dependency-injection`**: the clean target after scaffolding is removed.
  Parameterize Constructor and Extract Interface are mechanical first steps toward
  proper DI; once tests exist, migrate to constructor injection as the standard
  approach.
- **`hexagonal-architecture`**: ports and adapters are the architectural expression
  of the interfaces you extract. Breaking dependencies toward Extract Interface
  points in the same direction as hexagonal ports.
- **`solid-principles`**: Extract Interface enacts the Dependency Inversion
  Principle; the Interface Segregation Principle guides how narrow the extracted
  interface should be. The techniques in this skill are mechanical applications
  of these principles under duress.
- **`clean-code`**: the refactor step after the seam is in and tests are green is
  where clean code practices apply. Breaking a dependency to testability is not
  an invitation to leave ugly structure behind.

## Adapt to your context

This skill stays generic on purpose. Your codebase will have established
conventions for seam patterns, preferred breaking techniques, and how test
subclasses are organised relative to the classes they test. If your team has
settled on specific techniques as defaults, or your language or framework makes
certain techniques more natural than others, declare those in your own
`CLAUDE.md` or a higher-priority skill, which overrides this baseline. This
skill does not impose them.

## Reference

The three reference files detail the techniques by intent group:

- `references/add-without-touching.md`: step-by-step mechanics for Sprout Method,
  Sprout Class, Wrap Method, and Wrap Class, with decision guidance for choosing
  between them and worked TypeScript examples.
- `references/get-a-class-into-a-harness.md`: full mechanics for all ten
  object-oriented techniques for breaking construction dependencies, annotated
  with the sensing or separation problem each one addresses.
- `references/get-a-method-under-test.md`: full mechanics for all techniques
  that open a seam inside a method body, including short notes on the five
  language-specific techniques not applicable to TypeScript.
