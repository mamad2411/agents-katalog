---
name: common-ground
description: Establish and maintain enough shared understanding for ambiguous project work. Use when user intent, terminology, acceptance criteria, tacit preferences, or consequential assumptions may differ; after a misunderstanding; or before long-running work whose deviations would be expensive. Do not use for trivial mechanical tasks with clear, verifiable outcomes.
license: Apache-2.0
---

# Common Ground

Reach a **grounding criterion**: the user and agent mutually understand the work well enough for its current purpose, with the least necessary joint effort. Do not try to eliminate all uncertainty. Prevent material gaps from being decided silently.

The prompt, plan, and current beliefs are the **map**. The codebase, runtime, real constraints, and the user's reactions are the **territory**. Treat the four kinds of unknowns as a scan for gaps, not as four phases or four questionnaires.

## Invariants

- Ground before asking. Inspect relevant source, docs, tests, config, current behavior, and prior decisions before requesting information the environment can supply.
- The user owns intent, trade-offs, and acceptable outcomes. Evidence owns facts. The agent may recommend a default, but must not present an inferred preference as settled.
- Keep evidence-backed facts, user-confirmed decisions, agent assumptions, and unresolved unknowns visibly distinct.
- A gap is **material** when a plausible answer could change the goal, scope, domain meaning, user-visible behavior, public contract, data, security, permissions, external effects, a hard-to-reverse choice, or substantial work that verification would not cheaply catch. Material gaps require a user decision or explicit acceptance of the risk; other gaps need not block.
- Silence is not confirmation of a material user-owned choice.
- Alignment is continuous. Planning cannot exhaust unknown unknowns, so re-ground when the territory contradicts the map.
- An alignment-only request does not authorize implementation or external mutation.

## The Common Ground Loop

### 1. Ground the current map

Read the request and any existing canonical plan, spec, issue, glossary, or decision record. Inspect the relevant territory. Then form a compact working map:

- outcome and reason for the work;
- the user's starting point: what they know, what they know they do not know, and what they may only be able to judge by reacting to an example;
- observable evidence that it is done;
- accepted and rejected behavior;
- invariants, constraints, and out-of-scope boundaries;
- the decision surface most likely to change, such as domain terms, UX flows, interfaces, data, permissions, failure behavior, or rollout;
- the source of each important claim: user, evidence, or agent inference.

Surface contradictions and overloaded terms with concrete scenarios. Do not start with a generic questionnaire or merely paraphrase the prompt.

### 2. Scan for relevant unknowns

Scan only the decision surface, using these lenses:

| Lens | What to look for | Cheapest way to expose it |
| --- | --- | --- |
| Known known | A stated or proven requirement that may not actually be shared | Restate it with its source; compare the prompt with code and behavior |
| Known unknown | A recognized unresolved decision | Ask a discriminating question or propose a labeled default |
| Unknown known | A criterion the user can recognize but has not verbalized | Show contrasting references, examples, sketches, or a cheap prototype; turn reactions into criteria |
| Unknown unknown | A constraint or possibility not yet considered | Run a blind-spot pass over adjacent code, tests, history, official limits, failure modes, and prior art; propose a cheap probe |

Unknown unknowns cannot be enumerated completely. Report suspected blind spots as hypotheses with evidence and probes, never as a claim that the space is now exhaustive.

### 3. Route each gap instead of asking everything

Choose the mechanism by the gap's owner and shape:

| Gap | Action |
| --- | --- |
| Retrievable fact | Inspect, measure, or research it; do not ask the user |
| Fuzzy or conflicting term | Contrast concrete scenarios and settle a canonical meaning |
| User-owned preference or trade-off | Ask the user at the current decision frontier |
| Tacit taste or feel | Provide meaningfully different references or prototypes and ask for reactions |
| Hidden technical or operational risk | Run a focused blind-spot pass, spike, test, or pre-mortem |
| Knowledge held by another person | Identify the owner and create a targeted question or questionnaire |
| Low-impact, reversible, observable choice | State a recommended assumption, its disconfirming signal, and the later check; proceed |

For user questions:

- Ask only questions whose prerequisites are already settled. Ask one when its answer changes later questions; batch independent questions from the same frontier.
- State the decision, why different answers change the work, the relevant evidence, and a recommendation. Give a default only when taking it without an answer is safe.
- If the user cannot answer, change the method: inspect, explain, contrast, prototype, test, or leave the item explicitly unknown. Never invent an answer that merely sounds likely.
- Avoid broad prompts such as "anything else?" and questions the agent could answer from the territory.

### 4. Establish the alignment contract

Before consequential implementation, summarize:

- **Outcome and acceptance boundary**
- **Invariants and non-goals**
- **Evidence-backed facts**
- **User-confirmed decisions**
- **Assumptions**, each paired with a disconfirming signal or verification step
- **Remaining material gaps**, their owners, and the next cheapest move
- **Deviation policy** for discoveries during implementation

Keep this inline for contained work. For work that spans sessions or agents, or where decisions are costly to reverse, read [references/alignment-record.md](references/alignment-record.md) and persist the contract in the existing canonical artifact when possible.

Ask for a single confirmation when the contract contains newly inferred intent, a high-cost trade-off, or the user requested alignment before action. If the user already requested implementation and no material blocker remains, proceed under the visible contract without demanding ceremonial confirmation.

### 5. Re-ground during implementation

When new evidence changes the map, report the belief update compactly: what was learned, which contract item it affects, and what happens next.

- **Continue and record** when the deviation is local, reversible, inside the acceptance boundary, and existing verification will catch a wrong choice.
- **Stop and ask** when it changes the outcome, accepted behavior, domain meaning, public contract, data, security, permissions, external effects, cost, or a hard-to-reverse decision.
- Trust the territory over the plan for facts; preserve the user's authority over intent. Update stale plans instead of quietly diverging from them.
- Record only material decisions and deviations. Do not create an append-only diary of routine implementation choices.

### 6. Close the loop

Verify the result against the acceptance boundary, including at least one rejected or edge scenario when relevant. Report:

- what changed in product or domain terms, not just file names;
- material deviations and why they were safe or approved;
- assumptions that remain active and how they can be falsified;
- residual risks or unknowns;
- verification actually performed.

For complex work, give the user a concise explainer sufficient to review the result. Do not add a quiz unless the user asks for one or it is an explicit approval gate.

## Completion Test

Common ground is sufficient for the current purpose when:

- no material gap is hidden inside an agent assumption;
- accepted and unacceptable outcomes are distinguishable by observable examples or checks;
- important domain terms have one meaning in this context;
- low-risk assumptions are visible and falsifiable;
- the deviation policy matches the cost of being wrong;
- verification is defined before implementation and reported afterward.
