---
name: solid
description: "Use when locking module boundaries, class/API shape, or dependency direction after a design/spec is clear; when new packages, ports, or IO edges are about to be planned; when unit tests need many mocks; or when a review/refactor shows coupling or God-class smell. Do not use as the main skill while product decisions are still open (that is grill)."
---

# SOLID

> **Output language:** answer and write artifacts in the user's own language (match their messages, not the repo's history).

## Overview

Apply **SOLID** so behavior is easy to change and to test without a pile of mocks.

**Companion skills:** shape the product with **grill** → **write-spec**; prove behavior with **tdd** + **test-design**. This skill is only **structure and dependency direction**.

**Core principle: hard to test usually means hard to use — fix the boundaries, don't paper over them with mocks.**

## Trigger modes (important)

| Mode | When | What to do |
|------|------|------------|
| **Gate (primary)** | After **write-spec** (or waived design), before **write-plan**, if the slice adds modules / ports / IO edges | Full workflow below — announce `Using solid to …` |
| **Rescue** | Tests need ≥3 mocks; review/PR coupling; mid-**tdd** stuck on structure | Full workflow; then return to caller |
| **Smell only (inside grill)** | Comparing approaches that imply different boundaries | **Do not** load this skill as the main skill. Grill keeps the session; option labels may note one boundary smell ("this binds domain to SQL → mock pile later"). Formal solid waits for Gate |

**Default:** if product "what/why" is still open → **grill**, not solid.

## When to Use

- Spec approved and the next step would invent packages, ports, or dependency arrows
- Designing or reviewing module boundaries, class/API shape, dependency direction
- Unit tests need many mocks to "isolate"
- Refactors aimed at testability; PR adds coupling / God class

**When NOT to use:**

- Product decisions still open (use **grill**)
- Pure glue / drive-by rename / throwaway spike
- Tiny change with **no new boundary** (existing type, one behavior) — skip Gate; go **write-plan** or **tdd**
- As a substitute for grilling product trade-offs

## The Iron Law (non-negotiable)

```
1. New non-trivial behavior lives behind a boundary you can name (SRP).
2. Domain/policy does not depend on IO/framework details (DIP).
3. Fake abstractions invented only to satisfy a test are forbidden (no theater).
```

**Violating the letter is violating the spirit.** "Just mock the world" and "God class is fine for now" do not count.

## The five, as engineering checks

### S — Single Responsibility

- One unit → one reason to change
- If the name needs "and" / "manager of everything" → split
- Separate: orchestration vs policy vs IO vs formatting

### O — Open/Closed

- Prefer extending via new types/strategies/composition over editing a core switch forever
- YAGNI: don't pre-build plugin systems; do stop smearing new cases into a blob

### L — Liskov Substitution

- Subtypes must honor the caller's contract (pre/postconditions, errors)
- No "inherits for reuse" that surprises callers; prefer composition

### I — Interface Segregation

- Small, caller-shaped ports — not one mega-interface
- Callers shouldn't depend on methods they never use

### D — Dependency Inversion

- High-level policy depends on abstractions (ports), not on DB/HTTP/FS/SDK concretes
- Adapters at the edge; core stays pure/fakeable
- **Signal:** unit test needs ≥3 mocks → likely DIP/SRP failure (see test-design)

## Workflow (when invoked — Gate or Rescue)

Announce "Using solid to …", then:

1. **Name the units** — what each does, how you use it, what it depends on
2. **Draw dependency arrows** — domain → ports ← adapters (never domain → SQL/HTTP client directly)
3. **SRP pass** — split "and" responsibilities
4. **ISP pass** — trim fat interfaces
5. **DIP pass** — push IO out; inject ports
6. **Theater check** — every new interface must have a *product* reason, not only a test reason
7. **Hand off** — **write-plan** (Gate) or resume **tdd** (Rescue). If product questions reopened → **grill**

## Red Flags

- God class / package that "knows the whole feature"
- Domain imports ORM, HTTP client, or UI kit
- Subclass overrides that weaken invariants
- Interface with 15 methods for one caller that uses 2
- New interface used only in tests (no production adapter)
- Unit test mocks half the system to "isolate"

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "Split later when it hurts" | It already hurts when you need 4 mocks. |
| "Concrete is simpler than a port" | Until the second IO path. Port + one adapter is cheaper than rewrites. |
| "Inheritance reuses code" | Inheritance couples hierarchies; compose instead. |
| "One service interface keeps it tidy" | Fat interfaces force fake methods and ISP debt. |
| "Mocks prove DIP" | Mocks hide DIP failure. Fewer mocks after a real port is the proof. |
| "We're still grilling — run full solid now" | Smell in option labels only. Full solid after what/why is locked. |

## Checklist

- [ ] Product what/why already locked (or Rescue mid-implementation)
- [ ] Each unit has one clear purpose and a name without "and"
- [ ] Dependency arrows point inward to policy, not out to IO
- [ ] Ports are small; adapters own frameworks
- [ ] No test-only abstractions
- [ ] Ready for write-plan or tdd/test-design without mock piles

## Hand-off

**Transition gate** — before the boundaries go to **write-plan** (Gate) or back to code (Rescue), ask the user (one AskUserQuestion; never auto-advance):

```
A) Recommended: Proceed → write-plan (Gate) / resume tdd (Rescue)
B) Review first — run **review** on these boundaries (`references/solid.md`; upstream = spec's promised boundaries), then return to this gate
C) Adjust — rework the structure, then return to this gate
D) Something else (I will type it)
```

- Product decisions still open → **grill** → **write-spec**
- Boundaries locked → **write-plan**
- Implementing → **tdd** + **test-design**
- Shipping → **review** / **commit-and-push**
