---
name: reuse-and-patterns
description: Reasoning framework for reuse decisions and design pattern selection. Use when deciding whether to adopt a library, framework, or existing component vs. building something new; when evaluating whether a design pattern applies to a problem; when designing for extension or future variation; or when an abstraction is being extracted from duplicated code. Covers reuse strategy trade-offs, design pattern signals (when a pattern fits vs. when it adds indirection without value), and variability design.
---

# Reuse and Patterns

Reuse is not just about code. It is an architectural decision with technical and organisational consequences. The core question is never "can we reuse this?" — it is "what do we give up by reusing vs. building, and is that trade-off worth it?"

For design pattern signals see [patterns.md](patterns.md).
For reuse strategy trade-offs see [reuse-strategies.md](reuse-strategies.md).

## Why reuse often fails

Reuse fails for predictable reasons. Knowing them helps evaluate whether a proposed reuse is likely to succeed.

**Technical failure modes:**
- Reuse done only at the code level — copy-paste without abstraction — produces clones that diverge silently
- No comprehensive consideration of non-functional requirements: the reused component works but has wrong performance, security, or reliability characteristics for this context
- Unclear dependencies: the component brings transitive dependencies that conflict with the consuming system
- Unclear correctness guarantees: the component's behaviour under edge conditions is undocumented or unknown

**Organisational failure modes:**
- Reuse not planned in advance — the component is discovered after a parallel solution was already built
- No incentive structure for the team that built the component to maintain it for other consumers
- Not-Invented-Here resistance: teams prefer building because they control it, understand it, and get credit for it

**Ask before reusing:**
- What are the correctness guarantees of this component under the conditions we will use it?
- What are its performance characteristics under our load profile?
- What happens when it releases a breaking version?
- Who maintains it, and what is their incentive to keep it compatible with our use case?
- What would it cost to replace it if it fails us?

## Variability

Reusable components must manage variation — different consumers need different behaviour. How variation is handled determines how reusable the component actually is.

**Compile-time variability** — different versions of the component are built for different consumers. High control, no runtime overhead, but requires separate builds and makes a single shared component harder to maintain.

**Configuration variability** — the component reads configuration at startup. Simple, widely understood, but limits the kinds of variation that can be expressed (usually scalar values, not structural differences).

**Extension points (hooks/plugins)** — the component defines explicit extension points that consumers implement. More flexible, but requires the component author to anticipate the axes of variation in advance.

**Composition** — consumers assemble the component with other components to produce the variant they need. Requires good module boundaries. The most flexible but also the hardest to reason about.

**Ask:** What axes of variation do current and near-future consumers actually need? Design for those. Do not design for all conceivable variation — that produces a framework nobody can understand.
