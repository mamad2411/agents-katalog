---
name: solid
description: >
  SOLID design review rules (SRP, OCP, LSP, ISP, DIP) for code reviews: what counts as a real
  design finding, what is only taste, how to cite it and how severe it is. Use when reviewing a
  diff, a pull request or recent changes for design problems, when asked for a "SOLID review",
  "design review", "is this class doing too much", or when a review checklist asks for
  SOLID. Pair it with the dry skill for duplication and with owasp-asvs for security.
---

# SOLID Review

A design finding is worth reporting only when the design **already costs something or will on
the next ordinary change** — a bug, an inconsistency, a change that has to touch many places, a
unit that cannot be tested. Style, naming taste, "could be more elegant" and textbook purity are
never findings.

## Scope

Review the changed code and what it calls, read whole — not only the diff hunks. Judge the
change against the conventions the repository already follows (its `AGENTS.md`/`CLAUDE.md`,
existing seams and patterns). A repo that keeps small scripts procedural is not violating SOLID
by doing so.

## Rules

### SRP — Single Responsibility

One unit (function, class, module, service) has to change for **two unrelated reasons**.
Name both reasons in the finding.

- Finding: an HTTP controller that validates input, builds SQL, renders e-mail and spawns a
  child process; a Drupal form submit handler that also syncs to a remote API.
- Not a finding: a long function that does one thing in several steps.

### OCP — Open/Closed

Adding the **next variant** (a check, a backend, a provider, a content type) requires editing a
`switch`/`if` chain in **several** places instead of one registration point (a map, a plugin
type, a tagged service, an event subscriber).

- Cite every place the next variant would have to touch.
- Not a finding: a single `match` in one place that is the registration point.

### LSP — Liskov Substitution

An implementation that **throws, no-ops or silently changes meaning** for part of the contract
it claims, so that callers must know which concrete class they have (`instanceof` checks,
"not supported" exceptions, a subclass that ignores an argument).

### ISP — Interface Segregation

Callers are forced to depend on methods they never use, or implementers must stub out half an
interface. Cite the unused methods and the stubbing implementers.

### DIP — Dependency Inversion

Business logic hard-wired to a concrete I/O dependency (network, filesystem, database, clock,
child process, a static `\Drupal::service()` call inside a class that supports injection) so
that it cannot be tested or swapped without it — **where the codebase already has a seam** for
that dependency elsewhere (DI container, an injected client, a clock service). Without an
existing seam, report it only if it already blocks a test the change needs.

## Severity

- `high` — the design problem has **already produced** a bug or an inconsistency you can point
  to (two branches of an `if` chain disagree, a stubbed method is called in production).
- `medium` — default: the next ordinary change will have to touch several places or cannot be
  tested without real I/O.
- `low` — cleanup that would help but costs nothing today.

## Reporting a finding

Each finding carries:

- **rule** — `SRP`, `OCP`, `LSP`, `ISP` or `DIP`;
- **location** — `file:line` (every location for OCP);
- **cost** — one sentence: what breaks or what the next change has to do because of it;
- **fix direction** — the smallest change that removes the cost, preferring a seam the codebase
  already has over a new abstraction.

Verify each finding against the code before keeping it: re-read the lines and confirm the cost
is real. Fewer, true findings beat a long list. A disagreement with the overall approach of a
change is one finding, not a rewrite.
