---
name: grill-with-docs
description: Grilling session that challenges your plan against the existing domain model, sharpens terminology, and updates documentation (a domain glossary and ADRs under .context/) inline as decisions crystallise. Use when user wants to stress-test a plan against their project's language and documented decisions.
---

<what-to-do>

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing.

If a question can be answered by exploring the codebase, explore the codebase instead.

</what-to-do>

<supporting-info>

## Where the domain docs live

All project context lives under a `.context/` folder at the repo root. Unlike `.iudex/` (operational state, gitignored), **`.context/` is tracked project documentation — commit it.** That is also what makes the glossary and ADRs visible inside iudex ticket worktrees (which only see committed files), so the impl and QA agents share the same language.

```
.context/
├── glossary.md          # the domain glossary
├── <area>.md            # optional extra glossaries for a monorepo (e.g. ordering.md, billing.md)
├── adr/                 # architectural decision records
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── prd/                 # PRDs produced by to-prd (not glossary — kept in a subfolder)
```

- **The glossary** is every top-level `*.md` file directly inside `.context/`. Most repos have a single `.context/glossary.md`. A monorepo with multiple bounded contexts can add one file per context (`.context/ordering.md`, `.context/billing.md`); read them all, and when the current topic spans several, infer which context it belongs to — if unclear, ask. (Files in subfolders like `adr/` and `prd/` are NOT glossary.)
- **ADRs** live in `.context/adr/` with sequential numbering: `0001-slug.md`, `0002-slug.md`, etc.

Create files lazily — only when you have something to write. If no `.context/glossary.md` exists, create it when the first term is resolved. If no `.context/adr/` exists, create it when the first ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in the glossary, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

### Update the glossary inline

When a term is resolved, update `.context/glossary.md` (or the relevant context file) right there. Don't batch these up — capture them as they happen, using the **Glossary format** below.

The glossary should be totally devoid of implementation details. Do not treat it as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the **ADR format** below.

## Glossary format

Each glossary file:

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Order**:
{A one or two sentence description of the term}
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account
```

Rules:

- **Be opinionated.** When multiple words exist for the same concept, pick the best one and list the others under `_Avoid_`.
- **Keep definitions tight.** One or two sentences max. Define what it IS, not what it does.
- **Only include terms specific to this project's context.** General programming concepts (timeouts, error types, utility patterns) don't belong even if the project uses them extensively. Before adding a term, ask: is this a concept unique to this context, or a general programming concept? Only the former belongs.
- **Group terms under subheadings** when natural clusters emerge. If all terms belong to a single cohesive area, a flat list is fine.

For a monorepo with multiple contexts, each context gets its own file (`.context/ordering.md`, `.context/billing.md`). If relationships between contexts matter, capture them at the top of the most relevant file or in `.context/glossary.md`:

```md
## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking
- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched` events; Billing consumes them to generate invoices
```

## ADR format

ADRs live in `.context/adr/` using sequential numbering: `0001-slug.md`, `0002-slug.md`, etc. Scan the directory for the highest existing number and increment by one. Create `.context/adr/` lazily — only when the first ADR is needed.

Template:

```md
# {Short title of the decision}

{1-3 sentences: what's the context, what did we decide, and why.}
```

That's it. An ADR can be a single paragraph. The value is in recording *that* a decision was made and *why* — not in filling out sections.

Optional sections (only when they add genuine value; most ADRs won't need them):

- **Status** frontmatter (`proposed | accepted | deprecated | superseded by ADR-NNNN`) — useful when decisions are revisited
- **Considered Options** — only when the rejected alternatives are worth remembering
- **Consequences** — only when non-obvious downstream effects need to be called out

### What qualifies for an ADR

- **Architectural shape.** "We're using a monorepo." "The write model is event-sourced, the read model is projected into Postgres."
- **Integration patterns between contexts.** "Ordering and Billing communicate via domain events, not synchronous HTTP."
- **Technology choices that carry lock-in.** Database, message bus, auth provider, deployment target. Not every library — just the ones that would take a quarter to swap out.
- **Boundary and scope decisions.** "Customer data is owned by the Customer context; other contexts reference it by ID only." The explicit no-s are as valuable as the yes-s.
- **Deliberate deviations from the obvious path.** "We're using manual SQL instead of an ORM because X." Anything where a reasonable reader would assume the opposite.
- **Constraints not visible in the code.** "We can't use AWS because of compliance requirements." "Response times must be under 200ms because of the partner API contract."
- **Rejected alternatives when the rejection is non-obvious.** If you considered GraphQL and picked REST for subtle reasons, record it — otherwise someone will suggest GraphQL again in six months.

## After the session

When the plan is hardened, hand it to **to-prd** to write it up as a PRD under `.context/prd/` (using the sharpened glossary vocabulary), then **to-issues** to slice it into iudex tickets.

</supporting-info>
