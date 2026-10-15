---
name: sp-grill-with-doc
description: Use when the user wants a design, plan, or approach stress-tested against the project's own domain model and documented decisions - terminology challenged, contradictions with the real code surfaced, CONTEXT.md and ADRs kept current as decisions land - and does NOT need an implementation plan produced afterward. Use grill-then-plan instead when a written plan is the required outcome.
effort: max
---

<what-to-do>

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing.

If a question can be answered by exploring the codebase, explore the codebase instead.

</what-to-do>

<supporting-info>

## Domain awareness

During codebase exploration, also look for existing documentation:

### File structure

Most repos have a single context:

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `CONTEXT-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

Create files lazily — only when you have something to write. If no `CONTEXT.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

## During the session

### Ask in the user's terms, not the model's

The person answering knows the product, not necessarily the schema. Pose every
question in what they can see and do — which screen, what they press, what
happens next — and only then give the model-level backing. When two or more
paths are in play, a small table beats prose:

| | where | what you press | what it writes |
|---|---|---|---|
| A | the screen that exists today | the control already on it | a row owned by its parent |
| B | the screen we are changing | no such control exists yet - it is what we are adding | a row owned by nobody |

The table is the SHAPE, not the scope. The same framing fits a queue, a schema,
a CLI flag or a cron job: name the surface the user would actually observe,
whatever that surface is.

Then make the stake observable with one concrete walk-through: "you save an
item while working inside project X; three months later you delete project X;
today the item disappears from your library too." A user who cannot picture
the consequence cannot choose between the options.

Two tells that the FRAMING was wrong rather than the explanation: the answer
comes back as a question ("what do you mean?", "which step of the app is
this?"), or you needed entity names and ADR numbers just to state the options.
Re-pose it - do not re-explain it at greater length.

Put trade-off reasoning in the message body where it can actually be read;
keep option labels to a few words.

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

### Update CONTEXT.md inline

When a term is resolved, update `CONTEXT.md` right there. Don't batch these up — capture them as they happen. Use the format in [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

`CONTEXT.md` should be totally devoid of implementation details. Do not treat `CONTEXT.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Record every decision as an ADR

Always create an ADR for **every** design decision — one ADR per decision, the
moment the decision is made. Do not batch or defer. Create `docs/adr/` lazily on the
first ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).

A decision qualifies if one option was chosen over another — architectural shape,
technology choice, naming, scope boundary, safety mechanism, a deliberate no. When in
doubt, write the ADR. A short ADR is better than a missing one.

Record the **options**, not just the winner. Every ADR opens with a small Mermaid
decision diagram (see `references/diagram-convention.md`,
Rule 3) carrying one `|rejected|` branch per alternative that was genuinely on the
table, each with its one-line reason for losing — that is what stops the same
option being re-proposed in six months.

</supporting-info>
