---
name: architect
description: Make and record an architecture/design decision for non-trivial work — new subsystems, interfaces, data models, or significant refactors. Use when /plan flags a load-bearing decision. Delegates to the harness-claude:architect agent.
---

# /architect — design decision (ADR)

Goal: a concise, reviewable design with explicit trade-offs — not analysis paralysis.

## When to use
Only when the design is non-obvious: a new subsystem, a public interface/data model,
a cross-cutting change, or a refactor with several viable shapes. Skip for routine work.

## Do this
1. **Delegate to the `harness-claude:architect` agent** with the problem, constraints, and the
   existing architecture it must fit.
2. **Ground it before deciding:** name the architecture domain(s) the change touches and pull
   the matching cues from `../design/references/architecture-domains.md` (API, caching,
   cloud-native, message-queue, security). Use **context7** for live library/platform docs so
   the design doesn't assume capabilities that don't exist.
3. Require (each mandatory, not optional):
   - recommended approach + interfaces & data model;
   - **a do-nothing / simplest-possible alternative** considered explicitly (the YAGNI gate —
     the cheapest thing that could work, and why it's insufficient if you reject it);
   - other alternatives considered and why rejected;
   - **explicit non-functional trade-offs** — scale, latency, cost, security — stated, not implied;
   - **how it degrades under failure** (the unhappy path, not just the happy one);
   - **a quick threat model when the design crosses a trust boundary** (handles untrusted input,
     auth, secrets, or external calls): ask the four — what can be *abused*, what happens when it
     *fails open*, who *benefits* from breaking it, what's the *blast radius* — and name the trust
     boundaries. Skip when nothing untrusted crosses the design;
   - risks & mitigations.
4. Keep the recommendation decisive — one approach, justified.

## Output — ADR
```
## Context
## Decision (recommended approach)
## Alternatives & why not   (incl. the do-nothing / simplest option)
## Non-functional trade-offs (scale · latency · cost · security)
## Interfaces & data model
## Failure & degradation
## Threat model (only if it crosses a trust boundary)
## Risks & mitigations
```

Save the ADR (session file, or `docs/adr/` if the project keeps them).

## Exit criterion
A single recommended design with trade-offs stated. Then `/harness-claude:implement`.
