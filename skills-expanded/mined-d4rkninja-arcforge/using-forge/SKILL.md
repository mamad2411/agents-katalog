---
name: using-forge
description: "Use when a request needs ArcForge routing and explicitly asks to continue into inspection, review, change, or verification: choose the owning skill, choose Think, Review, Change, or Verify, resolve required, recommended, handoff, and optional-depth companions, sequence the work, then begin the routed first step. Produces an ordered routing plan with handoff payloads and names any skill that is not installed. Use think-forge for an unqualified route-only question."
---

# Using Forge

The executing router for the ArcForge skill set. It reads an explicit route-and-continue request, decides which skill owns each surface, chooses the mode, resolves companions, puts them in a safe order, and then begins the routed first step.

This skill routes. It does not answer the domain question itself.

**Core principle:** A request has one owner per surface, a mode, and a companion set. Name all three before work starts, or the request gets a partial answer from whichever skill happened to activate.

Every response produced by this skill MUST begin with this exact identity line, before any other prose:

```text
Active routing skill: Using Forge (`using-forge`) — route-and-continue.
```

Do not paraphrase or omit it. Naming the routed domain owner without naming this active router is incomplete.

## Routing Law

```text
NO DOMAIN WORK WITHOUT:
1. the requested outcome and the affected surfaces identified;
2. one owning skill chosen per surface, not one skill for the whole request;
3. the mode chosen from what the user actually wants: decide, inspect, apply, or prove;
4. required companions resolved before the owner they constrain, not after it finishes;
5. missing or uninstalled depth named with its exact technical ID.
```

## When to Use

Use this skill when:

- the user explicitly asks to route a request and continue into inspection, review, change, or verification in the same turn;
- an explicitly executable request spans more than one domain and the full set is not obvious — checkout, signup, tenant isolation, migration, release, incident follow-up;
- the owning skill is clear but the mode is not, and the user wants the work to continue after routing;
- a previous answer covered one domain and silently skipped an adjacent one;
- a companion skill is needed but which one, and in what order, is unresolved;
- part of the needed depth may not be installed and the route must stay honest about that.

## When Not to Use

- When the user already named a skill, use that skill directly. Do not re-route a settled request.
- When one domain plainly owns the request and no companion is in question, invoke that skill directly. Routing a single-domain request adds a step and no coverage.
- An unqualified question about where to start, which skill or mode to use, or what order to follow defaults to `think-forge`.
- When `think-forge` has already returned a route in the current user turn, do not re-enter this skill. Wait for an explicit later-turn request to continue into work.
- When a concrete pull request, merge request, commit range, patch, or repository diff needs findings and an approval recommendation, use `pull-request-review-gate`. When an architecture artifact needs an independent approval verdict, use `architecture-review-gate`. Routing is not review.
- For the domain decision itself, hand off. This skill never substitutes its own answer for the owning skill's work.

## Required Reference

Read [ArcForge routing map](references/routing-map.md) before naming a route. It carries the owning domain, triggers, exclusions, and typed companions for every skill. Route from that map, not from a skill name that merely sounds related.

## Routing Workflow

1. **State the requested outcome.** One sentence, in the user's terms. If the outcome is unclear, resolve that first — an unclear outcome cannot be routed, and guessing a skill hides the ambiguity.
2. **Split the request into surfaces.** Identity, contract, data, invariant, async work, flow control, secret, operations, migration, evidence, runtime, repository. A single sentence often carries three surfaces; a single skill covers one.
3. **Assign an owner per surface.** Use the ownership table below. Match on the surface's real subject, not on vocabulary that appears in passing. Check the exclusions column before settling.
   Do not collapse an invariant and its storage representation or enforcement into one surface. Stock or reservations, money precision, identifiers, durable intent, uniqueness, constraints, indexes, or conditional-write backstops create a `data-storage` surface. Put `transactions-consistency` first when it owns the invariant, then `data-storage` to model and enforce it.
4. **Choose the mode.** Decide what the user wants done, using the mode table. When the request combines them, order the modes Think → Review → Change → Verify and keep one ledger across the whole sequence.
5. **Resolve companions by type.** For each owner, read its companion list. Required companions enter the route. Recommended companions enter when their condition is met by either the request or an obligation or payload the route itself commits to; once the route depends on that condition, admit the companion before installation checking. Unknown implementation detail makes the companion's decision unresolved, not its ownership conditional. Handoff companions become a later step, not a parallel one. Optional depth enters only when the request asks for that depth.
6. **Order the route.** Apply the ordering rules below. An owner that depends on a required companion's decision runs after it.
7. **Write the handoff payload.** For every step, state what it receives and what output category the next step needs. A route without payloads is a list, not a plan. For an uninstalled step, keep Receives/Owns/Produces at the boundary-contract level; do not choose its mechanism, schema, state model, parameters, test matrix, or domain plan.
8. **Check installation.** Name any routed skill that is not installed, give its exact technical ID and installation group, and state what the route loses without it. Never present an uninstalled skill as if it ran.
9. **Emit the route, then perform step one's first action.** Produce the routing output below before any domain action. Then transfer control to the routed owner and actually perform the first safe, authorized action in the same turn. Report the action, the observed result, and concrete evidence such as inspected paths, commands, symbols, or the exact blocker. Future-tense prose such as “begin inspection” or “the next step will” is not continuation. If execution is blocked, report the attempted action and observed blocker rather than ending with a proposed action. Do not answer the domain question inside the routing output. A route-only request belongs directly to `think-forge`; do not activate this skill just to hand it to another router.

## Domain Ownership Table

| The request is really about | Owner | Do not route here for |
|---|---|---|
| Whole-system topology, boundaries, ownership, or cross-domain trade-offs | `system-architecture-harness` | A bounded specialist-domain question; an independent approval verdict; an AI control plane |
| LLM, RAG, memory, model routing, tool use, agent authority, evaluation | `ai-agent-system-architecture` | Non-AI architecture; an approval verdict |
| An independent verdict on an existing RFC, ADR, design, or plan | `architecture-review-gate` | Owning greenfield design; making repository changes |
| Findings, fixes, false-positive disposition, verdict, and instruction-derived score for a concrete pull request, merge request, commit range, patch, or repository diff | `pull-request-review-gate` | RFC or ADR approval; Git/ref mechanics; release certification; implementing fixes |
| Human, workload/service, device, tenant, and delegated identity; login, sessions, permissions, internal authorization | `auth-access` | General API shape; choosing cryptographic primitives |
| Endpoints, validation, errors, pagination, versioning, webhooks, SDKs | `api-contracts` | Queue internals; migration sequencing; authentication policy |
| Schemas, identifiers, money, time, indexes, files, search, lifecycle | `data-storage` | Isolation levels; migration sequencing; cache mechanics |
| Transactions, locking, idempotency, sagas, replication, sharding, ordering | `transactions-consistency` | Queue delivery mechanics; retry pacing; schema design |
| Jobs, workers, queues, events, outbox, acknowledgments, leases, batch, email, notifications | `async-messaging` | Isolation levels; retry pacing alone; public webhook contract |
| Caches, rate limits, quotas, retry/deadline budgets, timeouts, breakers, admission, backpressure | `resilience-flow-control` | Queue delivery semantics; transaction locking |
| Secrets, encryption, TLS, hashing, sensitive data, redaction, governed security exceptions, abuse, randomness | `security-privacy` | Owning the login flow; owning the request contract |
| Logs, metrics, tracing, health, audit, runbooks, backup, restore, DR, regions | `production-operations` | Deployment sequencing; owning sensitive-data policy |
| Schema and contract evolution, backfills, compatibility, CDC, cutover, legacy | `migration-evolution` | Designing a new contract; CI tooling; a rewrite decision |
| Test strategy, concurrency and failure evidence, load, release readiness | `quality-release` | Independent architecture approval; owning SLOs |
| Bootstrap, configuration, pools, networking, shutdown, artifact provenance/promotion, deploy gates, CI/CD | `runtime-delivery` | Schema semantics; owning telemetry; owning retry policy |
| Branches, merges, refs, protected refs, tags, versions, history, Git recovery | `git-workflows` | Deployment implementation alone; test strategy alone |

When two owners both fit a surface, the owner of the **invariant** leads and the other becomes a companion. When no owner fits, say so and name the closest owner plus what it will not cover, rather than forcing a match.

## Mode Selection for the Routed Skill

| The user wants | Mode | Route ends with |
|---|---|---|
| A decision, or the tradeoffs behind one | **Think** | A decision record and the validation path, with repository state unchanged |
| An assessment of what already exists | **Review** | Observed state separated from claims, prioritized findings, and blockers |
| An approved decision applied | **Change** | The change sequence, preserved contracts, and the rollback path, continuing into Verify |
| Proof that behavior holds | **Verify** | Checks actually run, observed results, and every unrun check labelled |

If the user names a mode, use it. Otherwise infer it and state the inference in one sentence. Change never reaches completion without Verify evidence. A request phrased as a question is usually Think or Review, not Change; do not upgrade it to Change because a fix seems obvious.

## Companion Resolution and Order

Resolve every owner's companions by type, then order the route:

| Type | Meaning for the route | Position |
|---|---|---|
| **Required** | The outcome cannot be completed safely without it | Before or with the owner |
| **Recommended** | Materially improves coverage; the owner keeps a safe local path | With the owner, when its condition is met |
| **Handoff** | Owns a separate decision reached from this one | A later step, with an explicit payload |
| **Optional depth** | Focused extra material | Only when the request asks for that depth |

Ordering rules:

1. An invariant owner precedes anything that derives from the invariant. Authoritative state is decided before post-commit work, notifications, or caches.
2. A required companion whose decision constrains the owner runs first. Identity and authorization precede the contract that exposes them. Secret and key policy precedes the flow that consumes it.
3. Evolution and delivery follow the target design. Migration sequencing and deploy ordering are decided after the shape they migrate toward.
4. Evidence closes the route. `quality-release` runs last on any route that ends in a readiness or completion claim.
5. Independent architecture review, when requested, is terminal and never a companion of the skill it reviews. A concrete changeset review may first pass an exposed RFC, ADR, topology, or architecture artifact plus relevant findings and gaps to `architecture-review-gate`; that later architecture gate is the terminal independent architecture step.
6. Do not run a handoff in parallel with its source. A handoff exists because the earlier decision produces its input.

## Handoff Contract

Every step in the route states three things:

- **Receives** — the decisions, constraints, and observed facts carried in from earlier steps.
- **Owns** — the decision this step is accountable for, and the surface it must not exceed.
- **Produces** — what the next step needs, including anything left unresolved.

Carry the ledger across the whole route: requirements, invariants, trust boundaries, authority, observed evidence, and open questions. A later step that silently drops an earlier invariant is a routing failure, not a domain failure.

For step one, the handoff is not complete until its owner has performed or attempted the first authorized action and the response reports the observation. A payload followed only by an imperative or future-tense action statement is still a route-only answer.

## Missing Skill and Standalone Safety

When a routed skill is not installed:

- name the exact technical ID and the installation group that provides it;
- state precisely which part of the request loses coverage;
- keep every safety requirement of the missing domain visible as an unresolved obligation;
- complete only the routing decision that is safe from installed material.

Never claim an unavailable skill or reference was loaded, never invent evidence from a skill that did not run, and never weaken a blocker because the depth that owns it is missing.

For an uninstalled step, a handoff may name only the input, owned surface, and category of required output. It must not prescribe the missing skill's concrete design, mechanisms, schemas, parameters, state transitions, tests, evidence matrix, or verdict. If the user asks for a “full plan,” stop at the safe route, any result produced by an actually installed first owner, and the unresolved missing-depth contracts.

## Output Contract

1. **Active routing skill** — the exact mandatory first line: **Active routing skill: Using Forge (`using-forge`) — route-and-continue.**
2. **Requested outcome** — the outcome in one sentence, and the surfaces it touches.
3. **Route** — ordered steps, each with skill, mode, and the reason that skill owns that surface.
4. **Companion record** — every companion by type, the condition that admitted it, and any considered and excluded.
5. **Handoff payloads** — receives, owns, and produces for each step.
6. **Coverage and gaps** — what the route covers, what it deliberately does not, and any surface with no clear owner.
7. **Installation status** — routed skills that are missing, their exact technical IDs or installation group, and the coverage lost.
8. **Open questions** — anything that must be answered before or during step one.
9. **First-action result** — after the route, the first action actually performed or attempted by the routed owner, its observed result, and concrete evidence or the exact blocker. A proposed future action does not satisfy this field.

## Stop Conditions

Stop and revise when any of these appears:

- the requested outcome is still ambiguous and a skill is being chosen anyway;
- the exact active-router identity line is absent, altered, or appears after other prose;
- the response ends with a proposed or future-tense first action instead of reporting an action actually performed or attempted and its observed result;
- this skill was activated for an unqualified route-only question;
- the routing output contains the domain answer instead of the route;
- a multi-surface request is routed to a single skill;
- an invariant owner absorbs a separately triggered storage representation or enforcement surface;
- a skill was matched on incidental vocabulary rather than the request's real subject;
- a required companion is listed after the owner it constrains, or dropped for brevity;
- a handoff is scheduled in parallel with the step that produces its input;
- a `think-forge` route-only answer returns to `using-forge` in the same user turn;
- an uninstalled skill is presented as available, loaded, or already run;
- an uninstalled skill's concrete design, mechanism, schema, parameters, state model, test matrix, evidence, or verdict is simulated inside its handoff;
- the mode was upgraded to Change because a fix looked obvious, without the user asking for a change;
- a route that ends in a readiness or completion claim has no evidence step;
- the router approves, reviews, or self-certifies work that `architecture-review-gate` or `pull-request-review-gate` owns;
- a safety blocker is softened because the skill that owns it is not installed;
- the user already named a skill and the route replaces their choice without saying why.

## References

- [ArcForge routing map](references/routing-map.md)

## Worked Example

- [Routing a prepaid checkout request across four domains](examples/worked-example-multi-domain-checkout.md)
