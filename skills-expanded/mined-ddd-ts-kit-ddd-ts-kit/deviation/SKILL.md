---
name: deviation
description: >-
  Use when asked to skip a rule, do it quick and dirty, disable a check, add an
  eslint-disable or ts-ignore, put logic where it does not belong "just this once", skip
  tests or the glossary, or when the guard asks to confirm a suppression or a rules change.
allowed-tools:
  - Read
  - Bash(npx ddd-ts-kit explain *)
  - Bash(npx ddd-ts-kit generate adr *)
---

# Deviations

The project owner decides what the project is: which framework, ORM, broker, authorization
model, and even which rules apply. What nobody gets, the owner included, is a silent
exception: a shortcut that is not written down is a defect waiting to be copied.

## Tell the two requests apart

| Request | It is | Do |
|---|---|---|
| "Use Prisma, not Drizzle", "roles are enough, no ReBAC", "no outbox, we have no database" | a choice among supported options | apply it through the config and the generator |
| "Put this query in the controller, it's faster", "skip the test for now", "just disable the rule" | going around a rule | follow the steps below |

## When asked to go around a rule

1. **Say what the rule protects**, in one or two sentences, and the concrete cost of breaking
   it here (`npx ddd-ts-kit explain <rule-id>`). No lecture.
2. **Offer the conforming way and its real price.** Most shortcuts save minutes: the
   generator writes the port, the fake and the wiring. Say how long the right way takes.
   Often that ends the discussion.
3. **If the owner still wants the deviation, it is theirs to take.** Then make it visible
   and bounded:
   - the smallest scope: one line suppressed, never a file, a directory or a severity for
     the whole project; a severity is set for the files it is about,
     `"<rule>": { "severity": "off", "files": ["<glob>"] }` (`config/rule-off-everywhere`);
   - a decision record, written with `npx ddd-ts-kit generate adr "<title>" --deviation <what>`:
     context, what is deviated from, why, scope, and the condition under which it is removed;
   - the suppression or config entry carries the reason and the ADR number:
     `// ddd-ts-kit-disable-next-line layer/domain-purity -- ADR-0007: legacy tax engine`;
   - a follow-up noted where the team tracks work.
4. **If the rule itself is wrong for this project**, change the rule, not the code under it:
   severity or limit in `ddd-ts-kit.config.json`, with an ADR. That is a legitimate decision
   and it applies to everyone equally.

## What you never do on your own initiative

- add a suppression, lower a severity, widen `*AllowedPackages`, add an `extraDirectories`
  entry, relax the pipeline, skip or delete a test, weaken an assertion, or set `guard` to
  `off`, in order to get to green;
- present a deviation as done without saying it is one;
- split a deviation into small steps so that no single step looks like one.

When the guard asks for confirmation, state plainly what the change relaxes and why you are
proposing it, and let the owner answer.

## What you do not refuse

A deliberate, recorded decision of the owner. Argue once, clearly, then carry it out well.
The architecture serves the project, and the record is what keeps it honest.
