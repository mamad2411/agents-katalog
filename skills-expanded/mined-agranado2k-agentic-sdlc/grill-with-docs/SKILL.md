---
name: grill-with-docs
description: Grilling session that challenges your plan against the project's documented domain language and decision records, sharpens terminology, and updates the glossary and ADRs inline as decisions crystallise. Use when user wants to stress-test a plan against their project's language and documented decisions.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
metadata:
  phase: planner
---

<what-to-do>

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing.

If a question can be answered by exploring the codebase, explore the codebase instead.

As each branch resolves, record it — after the decision, never in place of it: `sh scripts/trace.sh emit kind=grill.decision [subject=<prd:#N, ticket:#N or branch:x, when the plan has one>] outcome=accepted|overridden data.recommended='<your recommended answer>' data.answer='<the answer taken>' reason='<why they chose it, one line>' || :`. `accepted` is your recommendation taken, `overridden` is theirs instead. The trace is written here and never read (the kit's ADR-0008); unconfigured, the call is a silent no-op.

</what-to-do>

<supporting-info>

## Domain awareness

During codebase exploration, also read the project's own documentation. This kit
puts it in two places, both of them pointed at from the root `AGENTS.md`:

The root `AGENTS.md` is the agent manual, and it points at both:

- `docs/` — the project's memory
  - `docs/domain-glossary.md` — the ubiquitous language
  - `docs/diary.md` — the chronology; "Current state" first
  - `docs/adr/` — the decision records: `docs/adr/INDEX.md` says what is
    currently binding, `docs/adr/NNNN-template.md` is copied to start a new
    one, and the numbered records sit beside them
- `constitution/` — the layered rules the manual points at

A repo with several bounded contexts may keep one glossary section (or one
glossary file) per context and let `docs/domain-glossary.md` be the index. Infer
which context the current topic belongs to; if it is not obvious, ask — an
ambiguous context is itself a finding.

If the project's layout differs, read `AGENTS.md`: the manual names where the
glossary and the decision records actually live, and it is the authority here,
not this file.

Create files lazily — only when you have something to write. If no glossary
exists yet, create it when the first term is resolved. If no decision-record
directory exists, create it when the first record is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in the
glossary, call it out immediately. "Your glossary defines 'cancellation' as X,
but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

### Update the glossary inline

When a term is resolved, update the glossary right there. Don't batch these up —
capture them as they happen. Use the format in
[GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md).

The glossary should be totally devoid of implementation details. Do not treat it
as a spec, a scratch pad, or a repository for implementation decisions. It is a
glossary and nothing else.

### Offer decision records sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).

</supporting-info>

---

*Adapted from `engineering/grill-with-docs` in [mattpocock/skills](https://github.com/mattpocock/skills) — MIT, see `.agents/skills/LICENSE-mattpocock-skills.md`. Upstream keeps the ubiquitous language in a root `CONTEXT.md` and proposes its own ADR template; both sidecars were rewritten to point at the artifacts this kit establishes.*
