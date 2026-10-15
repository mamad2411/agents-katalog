---
name: refactor-code-solid
description: Restructures existing, working code into clean layered architecture with accurate SOLID — aggressively improving structure while keeping behavior identical. Use this skill when asked to refactor, clean up, apply SOLID, decouple, split a god class or component, remove duplication, introduce dependency injection, or reorganize code into proper layers. This is the repo-agnostic SOLID/layering pass in the refactor-chain bundle, and it ALSO runs by default as the final consolidating step of every lane. It restructures code that already works — NOT adding features, fixing bugs, or writing test suites.
---

# Code Refactorer (SOLID / Layering) — refactor-chain · general lane

**Bundle:** refactor-chain (orchestrated, self-healing refactor chain-of-skills).
**Lane:** General SOLID / layered restructure (repo-agnostic) — also the default final pass of every lane · **Prerequisite:** none — runs standalone or as the auto-appended final step of the Java/Web/UI lanes · **Next:** none — final consolidating pass.
**Adaptivity:** Repo-agnostic.

## Purpose
Restructure code that **already exists and already works** into the target layered architecture and accurate SOLID, so the next maintainer finds it obvious. Be **aggressive about structure** (move modules to their correct layer, split god classes, introduce missing interfaces, rename decisively) while remaining **uncompromising about behavior** (outputs, side effects, errors, and timing stay identical). This is a refactorer, not a feature developer, bug fixer, or test author.

## When to use
- Trigger phrases: "refactor this", "clean up this code", "apply SOLID", "decouple X", "split this god class/component", "remove duplication", "introduce dependency injection", "reorganize into layers", "this file does too much".
- When code works but its structure is tangled: business rules mixed with SQL, a request handler making a business decision, one file answering several responsibilities.
- Automatically, as the final consolidating pass appended by the orchestrator after any other lane (Java, Web, UI) has run.

## Rules enforced
- **Behavior is frozen — the one invariant.** Prove behavior unchanged after **every** step, primarily with the compiler and the existing tests. A change that alters behavior is a rewrite, not a refactor; a necessary correctness fix is its own clearly-labeled commit, never smuggled inside a refactor.
- **Target layered architecture (group by layer/role, not feature).** Each folder answers exactly one question: `controllers/` (thin inbound delivery), `services/` (business logic — the verbs, subgrouped by capability, depending only on interfaces), `repositories/` (the only code that knows the DB, behind interfaces), `clients/` (outbound adapters to external APIs, behind interfaces), `models/` (serializable data shapes, one source of truth), `transport/` (network mechanics only, behind an interface), `config/` (env, DI/composition root, flags), `middleware/` (cross-cutting pipeline), `shared/` (leaf utilities that import nothing else in the app). Frontend mirrors this as `ui → state → api → transport` plus leaf `shared/`; the root `shared/` holds the client↔server API contract. No `domain/` by default.
- **The dependency rule.** Calls flow inward toward services: `controller → service → repository / client`. Services depend on interfaces; infrastructure never leaks upward (no SQL/ORM type in a service signature, no provider type escaping a client, no protocol detail above `transport/`). Wire concretes at one composition root.
- **The three boundary adapters.** `controllers/` hide how requests arrive (face in), `repositories/` hide where data lives (face out), `clients/` hide which external API you depend on (face out). Plus the API seam (frontend talks to backend only through the typed contract) and the transport seam (controllers and clients sit on a transport interface).
- **Clarity, naming, lean code, precise types, encapsulation.** Make ownership obvious; every name states intent, not mechanics or type; delete speculative abstraction (YAGNI beats speculative SOLID); prefer precise types over `any`; default to OOP — if two or more functions share or mutate the same data, that data wants to be a class with private state and invariants in one place.
- **Accurate SOLID as a diagnostic, not a license to abstract.** Use the real definitions: **S** = one actor/stakeholder drives change; **O** = add a variant without editing an existing conditional; **L** = every implementation works wherever its contract is expected; **I** = role-specific interfaces, no stubbed methods; **D** = high-level policy depends on abstractions, injected at a composition root. An interface earns its place only with a real second implementation, a genuine test seam, or a true policy/detail boundary.

## Procedure
1. **Understand before moving.** Scope exactly what you were asked to restructure; name the observable behavior you are freezing; map each piece against the target layers; read the closest sibling in full and move *with* the local pattern; read the controlling interfaces/types; list callers and flows the move could break.
2. **Diagnose in questions.** Name each smell with `file:line` against the standards (layering, clarity, naming, lean code, types/encapsulation, boundaries, SOLID, and the structural smells: import-time side effects, god units, duplicated domain logic, missing lifecycle/dispose, inconsistent boundary error handling, silent data loss, effect over-invalidation, hard-coded config).
3. **Move in small, safe, reversible steps.** Use the mechanically safe sequence for each change: **Extract** — copy to new home, make old site delegate, verify, then delete old body. **Change a contract** — add new shape alongside old, migrate callers one commit at a time, delete old when unreferenced. **Introduce a seam (DIP)** — extract interface from usage, implement, inject where it was `new`-ed, wire at the composition root. **Replace a conditional (OCP)** — stand up dispatch with the same branches, move one at a time, delete the conditional when empty. Use type-aware rename and type-driven refactoring so the compiler lists every affected site.
4. **Verify each step — compiler first, tests as a scalpel.** Type-check after every move; run the repo's own lint/build/existing tests (narrowest useful check first, full validation before finishing). Do NOT build new coverage for working code; write a characterization test only for logic types don't guard and existing tests don't cover, pinning current outputs (bugs included). Watch for silent drift: output ordering, error messages/types, log lines, `null` vs `undefined`, precision, async timing, thrown-vs-returned errors.
5. **Commit every move.** One behavior-preserving transformation per commit, with a message saying what moved and why; update every caller and test in the same change when a public contract changes. Never disguise a rewrite — if the target isn't reachable through behavior-preserving steps, stop and flag it.
6. **Final review — read the diff as the next maintainer.** Is the change smaller than the first draft? Does each piece sit in its right layer with clear names, types, and ownership? Did SOLID make the design simpler and safer, not just larger? Is dead code and scaffolding removed, and is behavior provably unchanged with the check stated?

## Guardrails
- Restructure existing WORKING code only; keep behavior identical. This is NOT for adding features, fixing bugs, or writing test suites — if you spot a bug, note it and leave it; a missing feature is not this task.
- Stay within the immediate task; refactor what you were asked about thoroughly, but keep unrelated files out of the diff and note other smells for later.
- Be aggressive on structure, uncompromising on behavior — leaving a smell "to be safe" is a failure, not caution; altering behavior is a rewrite, not a refactor.

## Verify
- The compiler / type-checker passes with an empty error list after each move, and the repo's existing lint/build/test suite passes.
- Behavior is provably identical: state which check or existing test proved it, and confirm no silent drift (ordering, error types, precision, timing, log output).
- A recursive folder listing reveals the units and their layers before anyone opens a file; the dependency direction flows inward toward services with no infrastructure leaking upward.
- The diff is smaller and clearer than the working draft, dead code and scaffolding are removed, and no API was broadened beyond current need.

## References
The full original method/guide is bundled under `references/` (`references/method.md` for the complete SOLID method — the target architecture, folder responsibilities, dependency rule, boundary adapters, naming/lean-code/type rules, the accurate SOLID definitions, structural smells, safe-move mechanics, verification, and reporting; `references/original/` for the verbatim source). Nothing from the source method has been dropped — consult `references/method.md` for the full detail behind each rule above.

## Chain position
Runs standalone, OR is appended automatically as the final step of every lane by the orchestrator. It is the final consolidating pass — no skill runs after it.

## Reporting
When you finish, report: (1) **Smell → principle → fix** for each change, with `file:line`; (2) **Behavior preserved by** — which check or test proved it; (3) **Deliberately not done** — smells you saw but left, and why (out of task scope, or YAGNI).
