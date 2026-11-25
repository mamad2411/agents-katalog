---
name: design-docs
description: Writes and reviews technical design documents (RFCs) and Architecture Decision Records (ADRs) with goals and non-goals, real alternatives, risks, security, rollout, rollback and observability. Use when planning a new system, service or major feature, choosing between architectures or technologies, recording an architectural decision, writing an RFC or ADR, or reviewing someone else's design doc. Not for user-facing documentation or API reference docs.
license: MIT
---

# Design Docs and ADRs

A design doc exists to get the right decision made before code is written, and to record why it was made. Lead with the decision, show the alternatives you rejected and why, and make every claim checkable by a reviewer.

## When to use

| Situation | Artifact |
|---|---|
| New service or system, cross-team API, shared data model change, work over ~2 engineer-weeks | Design doc (RFC) |
| Hard-to-reverse choice: new database, new infrastructure, new language or framework | Design doc, then an ADR for the decision |
| Security, privacy or compliance-sensitive change | Design doc with a real security section |
| One significant decision with limited scope (adopt a library, change a protocol, deprecate something) | ADR only |
| Small, local, easily reverted change | A good PR description is enough |
| Bug fix | No doc. Link the issue. |

Rule of thumb: write a doc when the decision is expensive to reverse or affects people outside the team.

## Workflow

1. **Follow local conventions first.** Search the repo for existing docs and templates: `docs/adr/`, `doc/adr/`, `docs/decisions/`, `docs/architecture/decisions/`, `docs/rfcs/`, `rfcs/`, files named `*adr*` or `*rfc*`. Reuse the existing template, numbering and status values if they exist.
2. **Gather context before writing.** Read the relevant code, existing ADRs, related incidents and metrics. Ask the user for what you cannot find: deadline, SLOs, expected load, budget, owning team, compliance needs. Do not invent numbers.
3. **Write the problem, goals and non-goals before any solution.** If you cannot state the problem in three sentences with evidence, stop and ask.
4. **Generate real alternatives.** At least two credible options plus "do nothing". Compare all of them against the same criteria (see the table pattern below).
5. **Write the proposal** with enough detail to review: components, interfaces, data model, key flows, failure handling, capacity numbers.
6. **Fill in the operational sections:** risks, security and privacy, rollout and rollback, observability, cost, open questions with owners.
7. **Self-review** against the checklist in "Done when".
8. **Hand the draft to the user.** Do not post it, share it, or request reviewers on their behalf without asking.
9. **After the decision:** set the status, record ADRs for the key decisions, and link the doc from the code or README it affects.

## Design doc sections

| Section | What goes in it | Common failure |
|---|---|---|
| Header | Title, author, status (Draft / In review / Accepted / Rejected / Superseded), date, reviewers, decision maker | No named decision maker, so the doc never closes |
| Summary | 3-5 sentences: the problem, the proposed decision, the cost | Summary describes the problem but hides the decision |
| Context | Current state, why now, evidence (metrics, incidents, user requests) | "Everyone knows" context that new readers lack |
| Goals | Measurable outcomes ("p99 under 300 ms at 2k req/s") | Vague words: scalable, robust, seamless |
| Non-goals | Things a reasonable reader might expect that you will not do | Missing, so scope creeps during review |
| Proposal | Diagram, components, APIs, data model, flows, failure modes, capacity math | Code-level detail instead of design |
| Alternatives | Each option with honest pros, cons and why rejected | Strawman options set up to lose |
| Risks | Each risk with likelihood, impact and mitigation | Only technical risks; no people or schedule risks |
| Security and privacy | Data classification, authn/authz, PII flows, threat highlights, compliance | "N/A" with no reason |
| Rollout and migration | Phases, feature flags, backward compatibility, data migration, rollback plan | No way back once started |
| Observability and operations | Metrics, alerts, SLOs, dashboards, runbooks, on-call owner | "We'll add monitoring later" |
| Cost | Infrastructure and people cost, ongoing maintenance | Only build cost, never run cost |
| Open questions | Each with an owner and a date | Questions that silently become assumptions |

Use [references/rfc-template.md](references/rfc-template.md) for the full fill-in template.

## Writing for reviewers

- **Lead with the decision.** A reviewer should know what is being asked of them after the first paragraph.
- **Use concrete numbers.** Show back-of-envelope math for load, storage growth and cost. Example: "40M events/day ≈ 460/s average; assume 5x peak ≈ 2,300/s; at 1 KB each ≈ 40 GB/day before replication."
- **Mark estimates as estimates** and say where every other number came from.
- **State assumptions explicitly** so reviewers can attack them.
- **Separate facts, opinions and decisions.** "Measured", "we believe", "we will".
- **Compare alternatives in one table** using the same criteria:

  | Criterion | Option A: Postgres | Option B: DynamoDB | Do nothing |
  |---|---|---|---|
  | Fits access pattern | ... | ... | ... |
  | Operational cost | ... | ... | ... |
  | Team experience | ... | ... | ... |
  | Migration effort | ... | ... | ... |
  | Reversibility | ... | ... | ... |

- **Draw diagrams as code** so they live in version control. Mermaid renders natively on GitHub and GitLab. Use C4 levels: a context diagram (system and its users and neighbours) and a container diagram (deployable units and data stores) cover most docs. Add a sequence diagram for any non-trivial flow.

  ```mermaid
  sequenceDiagram
    Client->>API: POST /orders
    API->>DB: insert order (status=pending)
    API->>Queue: publish OrderCreated
    API-->>Client: 202 Accepted
  ```

- **Keep it short.** Most design docs fit in 2-6 pages. Move detail to appendices.

## ADRs

An ADR records one decision, its context and its consequences. Default to the Michael Nygard format unless the repo already uses another (MADR is a common alternative that adds explicit "Considered options").

- **Title:** numbered short noun phrase, e.g. `ADR-0007: Use PostgreSQL for the orders service`.
- **Status:** Proposed, Accepted, Deprecated, or Superseded by ADR-NNNN.
- **Context:** the forces at play, written neutrally.
- **Decision:** "We will ..." in active voice.
- **Consequences:** what becomes easier, what becomes harder, what we now must do.

Rules:

- **One decision per ADR.** About one page.
- **File naming:** `docs/adr/0007-use-postgresql-for-orders.md` (or the repo's existing pattern). Numbers increase and are never reused.
- **Accepted ADRs are immutable.** To change a decision, write a new ADR that supersedes the old one, and change only the old one's status line to `Superseded by ADR-0012`.
- **Record rejected decisions too** when the debate was significant; it stops the same argument from restarting.
- If the repo uses adr-tools, `adr new "Title"` creates the next numbered file and `adr new -s 7 "Title"` supersedes ADR 7.

Use [references/adr-template.md](references/adr-template.md) for the template and a worked example.

## Reviewing a design doc

When asked to review, check in this order and label every comment **blocking**, **should fix**, or **nit**:

1. Is the problem real and backed by evidence? Is "do nothing" seriously considered?
2. Are goals measurable and non-goals stated?
3. Are the alternatives genuine, compared on the same criteria?
4. Failure modes: what happens when each dependency is slow, down, or returns bad data?
5. Is there a rollout plan with a working rollback, including for data changes?
6. Security and privacy: who can access what, where PII flows, what is logged.
7. Observability: which metric or alert tells us it is broken?
8. Do the capacity and cost numbers survive a sanity check?
9. Is there a named owner for building and for operating it?

Give the author the top three issues first, then the rest.

## Anti-patterns

- **Solution looking for a problem** — the doc starts from a technology, not from a need. Rewrite from the problem.
- **Strawman alternatives** — options nobody would pick, listed to make the proposal look good. Reviewers stop trusting the doc.
- **Implementation spec disguised as design** — class diagrams and method signatures instead of decisions. Keep code detail out.
- **Retro-justification** — doc written after the code to approve it. If that is what it is, label it as a record, not a proposal.
- **No non-goals** — scope grows with every review comment.
- **No rollback** — especially for data migrations and protocol changes.
- **Editing an accepted ADR** to change the decision — write a superseding ADR instead.
- **Invented numbers** — an agent filling gaps with plausible figures. Ask, or mark as an estimate with the reasoning.

## Done when

- [ ] The summary states the proposed decision in the first paragraph.
- [ ] Goals are measurable; non-goals are listed.
- [ ] At least two real alternatives plus "do nothing" are compared on the same criteria.
- [ ] Failure modes, rollout and rollback are covered, including data.
- [ ] Security and privacy are addressed, or marked not applicable with a reason.
- [ ] Observability names concrete metrics and alerts and an operating owner.
- [ ] Every number is sourced or marked as an estimate.
- [ ] Open questions each have an owner.
- [ ] Once accepted, each key decision is recorded as an ADR.

## References

- [references/rfc-template.md](references/rfc-template.md) — read when writing a new design doc or RFC from scratch.
- [references/adr-template.md](references/adr-template.md) — read when recording or superseding an architectural decision.
