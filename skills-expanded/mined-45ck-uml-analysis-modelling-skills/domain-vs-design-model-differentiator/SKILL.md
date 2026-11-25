    ---
    name: "domain-vs-design-model-differentiator"
    pack: "uml-analysis-modelling-pack"
    purpose: "Distinguish conceptual/domain modeling from design/implementation modeling so the right level of detail is used."
    inputs: ["requirements or scenario", "stakeholders or actors", "existing models if any", "constraints or assumptions"]
    outputs: ["structured modeling notes", "identified diagram elements", "open questions", "recommended next model or check"]
    handoffs: ["domain-class-modeler", "design-class-modeler", "model-consistency-checker"]
    ---
    # domain-vs-design-model-differentiator

    ## Purpose
    Distinguish conceptual/domain modeling from design/implementation modeling so the right level of detail is used.

    ## Trigger this skill when
    - You need to convert prose, examples, or requirements into a clearer model.
    - A team needs a shared view of actors, classes, flows, states, or deployment assumptions.
    - The existing model mixes abstraction levels or leaves important relationships implicit.

    ## Expected inputs
    - requirements or scenario
    - stakeholders or actors
    - existing models if any
    - constraints or assumptions

    ## Deliverables
    - structured modeling notes
    - identified diagram elements
    - open questions
    - recommended next model or check

    ## Operating procedure
    1. Determine the modeling goal before choosing notation.
    2. Extract candidate actors, entities, responsibilities, flows, states, or nodes from the input.
    3. Keep the abstraction level appropriate to the chosen model.
    4. Record open questions instead of silently inventing missing detail.
    5. Suggest the best next complementary view when useful.

    ## Quality gates
    - The model matches the purpose of the view.
    - Domain concepts are not confused with implementation decisions unless this is a design model.
    - Relationships, flow steps, or transitions are explicit rather than implied.
    - Uncertainty is surfaced as open questions.

    ## Handoff targets
    - domain-class-modeler
- design-class-modeler
- model-consistency-checker

    ## Output style
    - Be concrete and structured.
    - Prefer tables or bullets over vague prose.
    - Separate facts, inferred model elements, and open questions.
    - Note assumptions clearly.

    ## Failure modes to avoid
    - Do not add unnecessary notation just to look formal.
    - Do not collapse domain and design views into one blurry artifact.
    - Do not invent multiplicities, states, or operations without some rationale.
    - Do not leave contradictions between views unmentioned.

    ## Minimum output skeleton
    ```md
    ## Summary
    ## Candidate model elements
    ## Structured outputs
    ## Assumptions
    ## Open questions
    ## Recommended next skill
    ```
