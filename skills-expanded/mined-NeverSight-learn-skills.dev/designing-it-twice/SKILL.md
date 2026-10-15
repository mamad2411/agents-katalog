---
name: designing-it-twice
description: Generate two or three radically different interface designs for a module, each under a different design constraint, then compare and let the user pick. Counters AI's tendency to commit to the first plausible interface. Use before implementing a new module's public interface, when an existing interface feels wrong but the right shape isn't obvious, or when the user mentions "design it twice" or "design alternatives". Skip for trivial interfaces (a single function with obvious signature) or when the interface shape is already locked in.
---

# Designing It Twice

From Ousterhout, *A Philosophy of Software Design*, chapter 11: your first design is unlikely to be the best. The cost of generating a second or third design is tiny compared to the cost of living with a bad interface. AI's natural failure mode is committing to the first plausible interface — because the first plausible interface is always plausible, and "plausible" feels like "done."

This skill produces **radically different** interface designs, each under a different constraint, so the alternatives don't drift toward the same shape. Then you compare and pick.

This is a thinking skill, not an implementation skill. No code under the proposed interface gets written here.

## Process

1. **Gather requirements.** Before designing, confirm what the module needs to do, who calls it, what the key operations are, and what should be hidden inside vs exposed. If `SPEC.md` (or any similar specification document) exists, read it. If not, ask the user briefly — don't run a full `clarifying-intent`-style interrogation here, that's a different skill.
2. **Generate designs in parallel** using sub-agents (Task tool) when available. Each sub-agent gets the same requirements and a *different* constraint (see below). Run them simultaneously to prevent contamination.
3. **If sub-agents aren't available**, generate sequentially with deliberate amnesia: write design 1, then explicitly start design 2 with "Now ignore everything in design 1 and approach this from constraint X." Sequential is worse than parallel — alternatives drift toward the first design — but it's better than not designing twice.
4. **Use radically different constraints.** Examples:
   - Design A: minimize method count — aim for 1–3 methods total
   - Design B: maximize flexibility — support many use cases through configuration
   - Design C: optimize the common case — make the 80% path trivial; allow ugly escape hatches for the 20%
   - Design D: take inspiration from a specific paradigm or library (e.g., "shape this like a builder pattern," "shape this like Unix pipes," "shape this like the standard library's <X>")
5. **Each design returns the same standardized output** (see format below): interface signature, usage example, what's hidden internally, tradeoffs.
6. **Present designs sequentially** so the user can absorb each before the comparison. Don't dump all three at once.
7. **Compare in prose**, not in a table. Tables force false symmetry; prose lets you say "Design A is much better for the common case but breaks down past 1k items, where Design B is the only viable option." Highlight where the designs diverge most.
8. **Ask the user to pick** — and ask whether elements from one design should be incorporated into another. Often the best design is a hybrid.
9. **Hand off** to `planning-by-modules` (to convert the chosen interface into a plan) or directly to `tdd-with-feedback-loops` (if the interface is small enough to implement immediately).

## Rules

- **Enforce radical difference.** If two designs have the same shape with different names, they're not alternatives — they're the same design twice. Reject and re-spawn.
- **No implementation in this skill.** Interfaces only. Sketch usage examples, but don't write the bodies.
- **Don't evaluate based on implementation effort.** "Design A is easier to implement" is a weak criterion that biases toward the first plausible thing. Evaluate on *interface quality* — what callers must know, what's hidden, how it survives change.
- **Don't let the user pre-commit to one design before seeing the others.** If the user says "I think it should look like X," produce X *and* two other radically different options. They might still pick X, but now they know what they rejected.
- **Use Ousterhout's evaluation lens** (see below) to compare. Don't invent ad-hoc criteria.
- **Stop at three designs in most cases.** Two minimum, three usually right, four when the design space is genuinely huge. More than four is paralysis.

## Standardized output for each design

Each design returns:

```
## Design <X>: <one-line name capturing the constraint>

**Constraint applied:** <what made this design different>

### Interface signature

<types, methods, params — the public surface only>

### Usage example

<a realistic caller using the interface>

### What this design hides internally

<the complexity that lives inside, invisible to callers>

### Tradeoffs

<one paragraph: what this design is good at, what it's bad at, and what kind of evolution it survives or breaks under>
```

## Evaluation criteria

From Ousterhout. Apply each lens to each design:

- **Interface simplicity.** Fewer methods and simpler params mean easier to learn and harder to misuse. Count the things a caller must know.
- **Generality.** Can this interface handle reasonable future use cases without changing? But beware over-generalization — an interface that handles "any future use case" usually serves none well.
- **Implementation efficiency.** Does the interface shape allow an efficient implementation, or does it force awkward internals? An interface that's clean for callers but impossible to implement well is a trap.
- **Depth.** A small interface hiding significant complexity is a deep module — good. A large interface with thin implementation is a shallow module — bad. Deep modules are the goal.

## Example: designing a notification dispatcher

**Requirement:** A module that takes events and decides what notifications to send (email, push, in-app), respecting user preferences.

### Design A: minimize method count

```typescript
interface Notifier {
  notify(event: Event): Promise<void>;
}
```

Single method. The module hides routing logic, channel selection, deduplication, retry. Callers can't even see that channels exist. Hides the most complexity behind the smallest interface.

**Hidden:** channel selection, user preference lookup, template rendering, retry, deduplication.

**Tradeoffs:** maximally simple for callers; hard to test specific channels; harder to extend with caller-specific routing rules.

### Design B: maximize flexibility

```typescript
interface Notifier {
  notify(event: Event, opts?: NotifyOpts): Promise<NotifyResult>;
  preview(event: Event, opts?: NotifyOpts): NotifyPreview;
  registerChannel(channel: Channel): void;
  registerTemplate(eventType: string, template: Template): void;
  setUserPreferences(userId: string, prefs: UserPrefs): void;
}
```

Five methods, several configuration objects. Callers can introspect, preview, register custom channels and templates.

**Hidden:** less — channels and templates are surfaced as concepts.

**Tradeoffs:** flexible for power users; many ways to misuse; large surface to test; new callers face cognitive overhead even for the common case.

### Design C: optimize the common case

```typescript
interface Notifier {
  notify(event: Event): Promise<void>;
  notifyWithOverrides(event: Event, overrides: ChannelOverrides): Promise<void>;
}
```

Two methods. Common path is `notify(event)`. The 5% case where callers need per-call control gets a separate method that opts into more knobs.

**Hidden:** routing, preferences, templates — same as Design A.

**Tradeoffs:** common case is trivial; escape hatch exists for unusual cases; adds method count vs Design A but in a controlled way; clear which method is the "default."

### Comparison

Design A is the deepest module — smallest interface hiding the most complexity. If notification routing is well-understood and stable, A wins. Design B is shallow by Ousterhout's definition: every concept inside the module leaks into the interface. Choose B only if callers genuinely need to customize channels and templates at runtime — a rare requirement that's frequently overestimated.

Design C is the right answer for most products: the common case is one call, the rare case is one different call, and nothing else escapes. If you have to pick one without more information, C is the safest bet.

> Which design fits your primary use case? Are there elements from another design (the `preview` method from B?) you'd want to keep?

## Anti-patterns to refuse

- **Three designs that are minor variations of the same shape.** Refuse. Re-spawn with stricter constraint differences.
- **A "best of all worlds" combined design produced before the user has compared the alternatives.** Refuse. The point is contrast; combining too early collapses it.
- **Implementing during design.** Refuse. This skill stops at the interface and one usage example per design.
- **Evaluating on "which is easier to write."** Refuse. The cost of writing is small; the cost of living with the wrong interface is large.
- **Skipping the design-twice exercise because "the right shape is obvious."** Be skeptical of obviousness. The first plausible interface is always plausible — that's not a signal that it's right.

## Post-output instruction

After the user picks a design (possibly hybrid), state:

> Chosen interface: <summary of selected design or hybrid>. Hand off to `planning-by-modules` to expand into a module-level plan, or directly to `tdd-with-feedback-loops` if the interface is small enough to implement now.
