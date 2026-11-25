---
name: vibe-decision-docs
description: Turn a user-confirmed Build Context into aligned product, technical, and UI decision documents before an MVP build. Use after vibe-deep-research has produced a confirmed Context with a product idea, research findings, user decisions, deliverables, constraints, source material, work order, and decision boundaries.
---

# Vibe Decision Docs

Create the three documents that constrain the first build: product, technical, and UI. This is a decision step, not an excuse to generate polished speculative documentation or to begin coding without confirmation.

## Inputs and preconditions

Require a `context.md` with `Status: User-confirmed` from `$vibe-deep-research`, or equivalent user-confirmed material. If the Context is not confirmed, return it to `$vibe-deep-research`; do not convert recommendations or assumptions into build commitments. Read the actual repository instructions, current architecture, relevant code, tests, and deployment configuration whenever an existing project is in scope.

Before writing, identify whether the user has confirmed:

- the target user, critical task, MVP boundary, and non-goals;
- any data, privacy, authentication, integration, and deployment constraints; and
- which decisions the agent may make locally versus which require user confirmation.

If a material item required to bound the first build is absent, return it as a decision request to `$vibe-deep-research`. Do not invent it to make the documents look complete.

## Create the document set

Use [the product template](assets/product-template.md), [technical template](assets/technical-template.md), and [UI template](assets/ui-template.md). Write exactly the three deliverables named in the confirmed Context to its configured documentation directory: `product.md`, `technical.md`, and `ui.md`. If no documentation directory is confirmed, ask before writing files; a conversation draft is not a replacement for the requested three documents.

Put `Source Context`, `Status: Draft`, and `Updated` at the top of each file. Keep research evidence in its linked research memo; do not repeat a broad competitor or architecture survey in these documents.

### Product document

Specify user, problem, single critical path, MVP scope, non-goals, success criteria, and acceptance examples. Distinguish real capabilities from fixtures or simulated states.

### Technical document

Specify the smallest architecture that can support the critical path: boundaries, data/state ownership, interfaces, dependency choices, error behavior, observability, test strategy, and deployment assumptions. Record meaningful alternatives and why they were not selected. Do not claim a service works until the relevant runtime path has been tested.

### UI document

Specify information hierarchy, screens/components, input, loading/running, success/result, empty, error, and mobile/responsive states. Explain what the user must understand or do in each state; screenshots are evidence or references, not a substitute for behavior.

## Reconcile before handoff

Run this internal cross-document check before delivery; do not create a fourth deliverable:

| Check | Required agreement |
|---|---|
| Scope | Product MVP and technical implementation boundary match. |
| Main path | The UI states make the product’s critical task possible. |
| Reality | Every fixture/simulation is marked in both product and technical documents. |
| Failure | Technical failure cases appear in the UI error/empty states where users encounter them. |
| Acceptance | Each success criterion has a direct verification approach. |
| Constraints | Privacy, access, platform, and deployment constraints appear wherever they affect a choice. |

Record unresolved conflicts rather than silently deciding them. Then request human confirmation of the documents before a Build prompt is issued.

## Handoff

After confirmation, build only the narrowest vertical slice that proves the critical path. If the implementation changes behavior, contracts, architecture, tests, durable formats, or repository documentation, use the external companion [ds-spec-loop](https://github.com/songyang0603/ds-spec-loop) rather than duplicating its Spec and evidence method here.

## Quality check

Before completion, ensure the documents are decision aids:

- no generic feature list without a critical path;
- no architecture chosen solely because it is popular;
- no UI documentation that omits running, error, or mobile states when they matter;
- no unverified implementation claim; and
- a future agent can implement the confirmed scope without reopening product strategy.
