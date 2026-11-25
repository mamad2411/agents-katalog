---
name: grill-with-docs
description: Grilling session that challenges your plan against the existing domain model, sharpens terminology, and updates documentation (docs/GLOSSARY.md, ADRs) inline as decisions crystallise. Use when user wants to stress-test a plan against their project's language and documented decisions.
---

<!-- Delete when: native Claude Code documentation indexer with inline term resolution UI is available -->

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing.

If a question can be answered by exploring the codebase, explore the codebase instead.

## Inputs

| Layer | File | Scope | Why |
|---|---|---|---|
| Reference | `docs/GLOSSARY.md` | Language + Relationships | The canonical terms to challenge the user's wording against |
| Reference | `docs/GLOSSARY-MAP.md` | Full file, if present | Tells you the repo is multi-context and where each glossary lives |
| Reference | `docs/adr/*.md` | Only ADRs touching the area under discussion | Decisions already settled; don't re-litigate them |
| Reference | `CONTEXT.md` | "Key Decisions" only | Project-level constraints. **Not** the glossary — different file, different schema |
| Working | The user's plan | Full | What's being grilled |

## Domain awareness

During codebase exploration, also look for existing documentation:

### File structure

Most repos have a single context:

```
/
├── CONTEXT.md                        ← project orientation, not the glossary
├── docs/
│   ├── GLOSSARY.md                   ← the domain language
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If `docs/GLOSSARY-MAP.md` exists, the repo has multiple contexts. The map points to where each one lives:

```
/
├── docs/
│   ├── GLOSSARY-MAP.md
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── GLOSSARY.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── GLOSSARY.md
│       └── docs/adr/
```

Create files lazily — only when you have something to write. If no `docs/GLOSSARY.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

**Pre-4.3 repos** kept the glossary at the root as `CONTEXT.md` (with a `CONTEXT-MAP.md`), which collided with Attacca's project-orientation `CONTEXT.md`. If you find a root `CONTEXT.md` whose content is a `## Language` glossary rather than Project/Stack/Key Decisions, offer to move it to `docs/GLOSSARY.md`. Don't move it silently.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `docs/GLOSSARY.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

### Update the glossary inline

When a term is resolved, update `docs/GLOSSARY.md` right there. Don't batch these up — capture them as they happen. Use the format in [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md).

`docs/GLOSSARY.md` should be totally devoid of implementation details. Do not treat it as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else. Project decisions go in `CONTEXT.md`; architectural trade-offs go in an ADR.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).

---

*Adapted from [mattpocock/skills](https://github.com/mattpocock/skills).*
