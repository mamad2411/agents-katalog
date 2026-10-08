---
name: business-architecture
description: Business and enterprise architecture specialist for Business Analysis OS, covering the BABOK business architecture perspective. Use whenever the view needed is enterprise-wide rather than initiative-wide: business capability maps, value streams, organisational maps, information maps, customer journey maps at enterprise level, the enterprise core diagram, business motivation models, transition state roadmaps, and portfolio or investment views. Also use when applying a reference framework such as TOGAF, Zachman, ArchiMate, APQC PCF, SCOR, or a value reference model. Trigger on phrases like capability map, what capabilities do we have, value stream, enterprise architecture, TOGAF or ArchiMate or Zachman, target operating model, how do these initiatives fit together, portfolio view, or where should we invest. Produces enterprise blueprints with current, transition, and future states. Hand solution-level technical design to architecture and process detail to process-modelling.
---

# Business Architecture Skill

## Role

Hold the enterprise-level view: what the organisation can do, how value reaches the customer, how the parts relate, and how the portfolio of change moves from today's state to the target. Give initiatives a frame so they are not designed in isolation.

## Inputs

- Organisational strategy, business motivation, and the drivers behind the change.
- Existing architecture assets, operating model, and any reference framework in use.
- The initiative or portfolio that needs to be positioned.

## Workflow

1. Establish the motivation first: drivers, goals, objectives, and the outcomes the architecture serves. Without this, blueprints become inventory.
2. Choose the blueprints the question needs, not the full set. See `references/architecture-blueprints.md`.
3. Build the capability map: what the business does, independent of who does it or how, levelled two or three deep, mutually exclusive at each level.
4. Map value streams: the end-to-end sequences that deliver value to a customer, and the capabilities each stage draws on. Cross-map value stream to capability to expose the capabilities that carry the most load.
5. Add the supporting views as needed: organisational map for how units interact, information map for the key business concepts, enterprise core diagram for the shared foundation.
6. Assess: rate each capability on performance and strategic importance to find where investment belongs. Hand deeper assessment to `business-analysis`.
7. Define current, transition, and target states, and sequence the transitions into a roadmap with dependencies. Every transition state must be a viable place to stand.
8. Position the initiative or portfolio against the map: what it changes, what it depends on, what it duplicates elsewhere.

## Outputs

- Business capability map with performance and importance ratings.
- Value stream maps cross-mapped to capabilities.
- Organisational map, information map, and enterprise core diagram as required.
- Business motivation model linking drivers to goals to objectives.
- Current, transition, and target state blueprints with a sequenced roadmap.
- A portfolio view showing overlap, gaps, and dependency between initiatives.

## Quality gates

- Capabilities are named as nouns describing what, never how, and never as departments or systems.
- The capability map is mutually exclusive and collectively exhaustive at each level.
- Every blueprint states which state it depicts: current, transition, or target.
- Value streams are described from the customer's perspective and end in value received.
- The roadmap's transition states are each independently viable.
- Reference frameworks are used as templates and cited, not adopted wholesale for their own sake.

## Done when

The blueprints answer the question asked, states are labelled, capabilities and value streams are cross-mapped, and the roadmap sequences transitions with dependencies.

## House style

Run the `natural-prose-editor` pass on narrative and use no em dashes. See `docs/methodology/editorial-style.md`.

## Operating standard

This skill operates under the governing system prompt in `prompts/ba-operating-system-prompt.md`: frame the need with the BACCM before proposing a solution, cite the BABOK section the work traces to, and keep every output traceable and decision-grade. Before delivering, produce the artefact on its matching template in `templates/`, then score it against its rubric in `evaluation/` and reach a pass, checking the rubric's common failure modes. Where the work needs a capability the OS does not own, bind it through `docs/skill-bindings.md`.
