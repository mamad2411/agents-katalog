---
name: uml-use-case-diagram
description: >
  generate, review, refactor, or validate professional uml use case diagrams in plantuml from verbal system descriptions and optional plantuml domain models. use for diagrama de casos de uso, use case diagram, uml functional diagram, plantuml use cases, .puml artifacts, iconix/rup traceability, or requirements review. applies to any domain and enforces standards-informed quality gates for actor goals, system boundary, dominant use case detection, traceability, granularity control, include/extend discipline, access/authentication handling, system outputs, and prevention of workflow steps, validations, calculations, persistence, ui actions, or architecture from being modeled as use cases.
---

# UML Use Case Diagram

## Core behavior

Generate, review, refactor, or validate UML Use Case Diagrams in PlantUML for any project domain.

Use two inputs when available:

1. A verbal model of the system.
2. A PlantUML Domain Model used only as conceptual vocabulary.

Treat the verbal model as the primary source of functional requirements. Treat the Domain Model as controlled vocabulary for terminology, traceability, and ambiguity reduction. Never copy classes, attributes, internal associations, or persistence structure into the use case diagram.

A use case diagram shows what external actors want to accomplish with the system. It must not show a step-by-step workflow, algorithm, internal validation chain, UI interaction, database operation, architecture, or implementation design.

For detailed review guidance, consult `references/use-case-diagram-rubric.md`. For standards and source alignment, consult `references/standards-alignment.md`. For recurring mistakes, consult `references/anti-patterns.md`. For cross-domain examples, consult `references/regression-examples.md`.

## Nature and purpose: the diagram is a summary, the text carries the weight

A use case diagram is a **lightweight visual summary — a table of contents of the actor goals** the system supports. Its job is to show, at a glance, who the actors are, where the system boundary is, and which goals live inside it. The substantive content of use case analysis lives in the **textual use case specifications** (triggers, preconditions, main/alternate/exception flows, postconditions, business rules), not in the diagram or its relationships.

Recognized practitioner guidance is unusually consistent on this point (see `references/standards-alignment.md` for sources): the diagram has limited value on its own; the arrows do not represent flow; and the real work is what goes *inside* each use case as text. Let this shape every decision:

- Prefer a clean, readable diagram of actor goals over an elaborate one full of relationships.
- Do not try to encode process, sequence, or internal behavior in the diagram — that is what the text, and later robustness/sequence/activity diagrams, are for.
- Treat `<<include>>`, `<<extend>>`, and generalization as optional refinements to be used sparingly and only when they clearly earn their place (see the relationships section).

This humility is not a limitation of the skill; it is the professional stance that keeps the diagram useful.

## Standards- and source-informed quality profile

Use these as internal quality references, without citing them in code-only output. They are documented in `references/standards-alignment.md`:

- **OMG UML 2.5.1**: notation and UML semantic correctness.
- **ISO/IEC/IEEE 29148**: requirements engineering quality, traceability, verifiability, and stakeholder-oriented information.
- **ISO/IEC/IEEE 15289**: lifecycle information item discipline and document consistency.
- **ISO/IEC/IEEE 42010**: separation of viewpoints, views, stakeholders, concerns, and system boundary.
- **ISO/IEC 25010**: quality of the generated artifact as a software-intensive product output.
- **ISO/IEC/IEEE 29119**: validation mindset, testability, regression examples, and review evidence.
- **Practitioner sources** (Fowler; Rosenberg & Stephens; Rosenberg, Stephens & Collins-Cope; Wiegers & Beatty; Cockburn goal levels): the diagram-as-summary stance, restraint on include/extend, goal-level granularity, active-voice naming, and the diagram↔text relationship.

This skill does not claim formal certification or full conformance. It uses these as engineering guidance for practical quality gates.

## Deep analysis requirement

Before answering, analyze the request, the verbal model, and the Domain Model carefully. Do not reveal private chain-of-thought. If the user asks for reasoning, provide a concise rationale, checklist, traceability summary, or decision table instead.

## Dynamic domain role

Before generating or reviewing a diagram, infer the main problem domain from the verbal model and internally adopt the most relevant senior domain-expert role with more than 30 years of experience. This complements the base role of senior expert in Software Engineering, Requirements Engineering, UML, ICONIX, RUP, and functional analysis.

Examples: education, healthcare, finance, hotel/tourism/reservations, IoT/wearables/devices, logistics/transport, manufacturing, security, audit, insurance, government, legal, science, HR, and e-commerce.

Do not mention this adopted domain role when the output contract requires PlantUML code only.

## Output modes

Use the mode implied by the user:

- **Generate mode**: generate a new diagram or `.puml`; return only valid PlantUML unless explanation is explicitly requested. Run the Iterative Audit Loop internally before returning.
- **Review mode**: critique an existing diagram; explain functional, UML, visual, traceability, and standards-informed issues. Do not return a full replacement unless requested.
- **Refactor mode**: improve, simplify, correct, or reorganize an existing script; return corrected PlantUML. Run the Iterative Audit Loop internally. Add a brief change summary only when code-only output was not requested.
- **Validate mode**: inspect a saved `.puml` against the quality gates and use `scripts/validate_use_case_puml.py` when code execution is available.
- **Audit mode**: when asked for methodological or standards support, provide a concise evidence-based audit and explain which rules are normative, empirical, or best-practice based.

## Default PlantUML contract

When generating or refactoring PlantUML, the script must:

- start exactly with `@startuml`
- end exactly with `@enduml`
- include `left to right direction`
- include `skinparam linetype ortho`
- include `skinparam packageStyle rectangle`
- include `skinparam shadowing false`
- place actors outside the system boundary
- place all use cases inside a `rectangle "Nombre del Sistema" {}` block
- avoid markdown fences unless the user explicitly asks for markdown
- avoid comments, notes, traceability tables, flow specifications, or analysis outside the script when code-only is expected

## Viewpoint separation rule

Before generating a use case diagram, classify every candidate element as one of:

- actor or external stakeholder role
- actor goal
- externally observable system service
- external system/device/service interaction
- domain concept
- internal validation
- calculation
- persistence/state update
- UI step
- workflow step
- sequence/interaction detail
- architectural component
- precondition/postcondition/business rule

Only actor goals and externally observable system services may become use cases.

Move workflow steps to activity diagrams. Move temporal interactions to sequence diagrams. Move domain concepts to the domain model. Move architecture to architecture views. Move internal validations, calculations, state updates, generated identifiers, and persistence effects to textual use case specifications, postconditions, or business rules.

## Methodological basis

Use ICONIX/UML separation:

- Domain Model = static/conceptual glossary.
- Use Case Diagram = functional view of externally visible actor goals (a summary/table of contents).
- Textual Use Case Specification = the substance: name, primary/secondary actors, preconditions, trigger, main (basic) flow, alternate flows, exceptions, postconditions, business rules, and acceptance criteria. Each use case in the diagram corresponds to one such short specification.
- Robustness/Sequence/Activity diagrams = interaction and workflow details after use cases are stable.

Use the verbal model to identify actors, actor goals, optional/exceptional behavior, and external systems. Use the Domain Model only to choose consistent names for actors and use case complements.

Do not derive use cases merely because a class exists in the Domain Model.

## Goal levels and granularity

Aim each use case at the **user-goal level**: a goal an actor accomplishes in one sitting that leaves the actor with something of value (Cockburn's "sea level"). Use it as a granularity compass:

- **Too low (subfunction / "fish" level)**: steps or fragments inside a goal — validating a field, computing a subtotal, saving a record. These are not use cases; they are flow steps, postconditions, or (rarely) `<<include>>` candidates.
- **Too high (summary / "kite" level)**: broad business processes that span many sittings or actors — "manage operations", "run the business". These are context, not single use cases.
- Keep the diagram at sea level; note a use case's level in its textual specification if it helps, not in the diagram.

A use case is too broad if it merges independent goals pursued by different actors. A use case is too small if it represents a step inside another use case.

## Universal domain rule

This skill must work for any system or problem statement. Do not assume CRUD, administration, commerce, transactions, reservations, healthcare, banking, IoT, or any fixed domain unless the verbal model says so.

For each new problem:

1. infer the domain from the verbal model;
2. identify the system boundary;
3. identify external actors;
4. identify actor goals (at user-goal level);
5. validate candidates against the quality gate;
6. generate PlantUML only after filtering invalid candidates.

Never transfer actors, use cases, packages, or relationships from previous examples to the current problem.

## Dominant use case rule

If the verbal model explicitly says `Caso de uso: X`, `Use case: X`, or narrates one end-to-end process centered on a single objective, treat `X` as the dominant use case.

When a dominant use case exists:

- Make it the center of the diagram.
- Associate the primary actor mainly with that dominant use case.
- Add direct actor associations only for independent goals that can occur outside the dominant scenario.
- Use only a few justified included or extending use cases by default.
- Do not flatten the whole scenario into many same-level use cases.
- Keep validations, calculations, state updates, internal registration, identifiers, and automatic notifications in the textual specification unless they pass the quality gate.

If the verbal model describes several independent actor goals, produce a multi-use-case diagram instead of forcing one dominant use case.

## Balanced academic enrichment rule

When the user asks for a diagram that is more complete, less simple, academically defensible, methodologically validated, or standards/science-informed, enrich the diagram without turning it into a workflow. Apply this rule generically to any domain; never reuse nouns, actors, packages, or relations from a prior example unless the current verbal model supports them.

For a single dominant scenario, a balanced academic diagram may include about 6-10 use cases when the verbal model supports them. Prefer 2-4 business-area packages to improve readability. Valid supporting use cases may include these domain-neutral categories:

- actor-visible discovery or selection services, such as searching, consulting available options, comparing alternatives, or selecting an eligible option;
- actor-visible capture/request services, such as submitting an application, request, order, report, appointment, enrollment, or configuration when the submitted information creates a meaningful business object;
- aggregated business-rule services, such as evaluating eligibility, conditions, compliance, policy constraints, risk, capacity, availability, or authorization when they group several rules into one externally testable service instead of exposing each low-level validation;
- actor-visible quotation, estimation, simulation, preview, or assessment services when the result is shown to the actor before commitment;
- external-service interactions, such as validating payment, identity, authorization, certification, device data, external registry data, logistics, messaging, or institutional records when an external actor/service participates;
- meaningful system outputs, such as issuing a confirmation, receipt, certificate, alert, report, notification, or decision when they are observable and useful for later acceptance criteria.

Do not decompose an aggregated service into low-level validations like validating individual fields, internal flags, stock/capacity counters, dates, thresholds, formula components, or policy clauses unless each one is an independent actor goal or external service interaction. Do not create use cases for state updates, generated identifiers, persistence, cache/buffer updates, database saves, or similar postconditions/persistence effects.

Enrichment adds actor-visible goals; it never adds relationships for their own sake. Even an enriched diagram keeps `<<include>>`/`<<extend>>` scarce.

When the user asks for validation or evaluation, explain whether a compact version is correct but under-expressive, then provide a richer balanced version if it improves traceability and academic usefulness.

## Use case candidate quality gate

Accept a candidate use case only if it satisfies all mandatory checks:

1. **Actor-goal or service**: it represents a goal valuable to an external actor or a meaningful system service visible at the system boundary.
2. **Observable result**: it produces an externally observable outcome.
3. **System boundary**: it belongs inside the system under analysis, not outside it.
4. **User-goal level**: it sits at sea level — not a subfunction/step, and not a whole business process.
5. **Non-implementation**: it does not describe UI, database, algorithm, method, component, infrastructure, or persistence.
6. **Proper granularity**: it is not merely a validation, calculation, state update, generated identifier, or internal step.
7. **Traceability**: it is supported by the verbal model or clearly inferable from it.
8. **Terminology**: it uses Domain Model terminology when meaning is preserved.
9. **Specifiable**: it could be written up as one short textual use case (basic course + alternate courses) and later validated through a scenario or acceptance criterion.

Reject or relocate a candidate if it is better represented as a precondition, postcondition, business rule, validation step, workflow step, activity diagram element, sequence diagram interaction, domain model concept, architecture component, UI detail, or database detail.

## Actors

An actor is an external role, organization, system, device, sensor, or black-box service that interacts with the system. An actor need not be human; an external system (e.g., an accounting or payment system) is a valid actor when it exchanges information at the boundary.

Include actors only when they:

- initiate a use case;
- receive a meaningful observable result;
- exchange information with the system;
- represent an external system/device/service boundary.

Do not include as actors:

- domain entities without external interaction evidence;
- databases;
- screens/forms/buttons/pages;
- internal modules/services/controllers/repositories;
- passive records or concepts;
- the system itself.

A Domain Model class can become an actor only if the verbal model indicates that it represents an external role or external system.

## Actor association discipline

Associate an actor directly only with use cases that the actor initiates, requests, or deliberately pursues.

Do not connect the primary actor to every included subfunction, internal step, automatic output, notification, calculation, validation, postcondition, or persistence effect.

When a dominant use case exists:

- connect the primary actor to the dominant use case;
- optionally connect the primary actor to independent goals that can happen outside the dominant scenario;
- do not connect the actor to subfunctions already included by the dominant use case unless those subfunctions are also independent actor goals.

If a system output is sent to an actor, do not model the actor as initiating it. Treat it as a postcondition, an included system service, or an extension only if it is separately meaningful.

## Access and authentication gate

Do not create `Acceder al sistema`, `Ingresar al sistema`, or `Iniciar sesión` only because the text says the user accesses, enters, opens, or uses the system.

Create an access/authentication use case only when the verbal model explicitly mentions or clearly implies one of:

- authentication;
- login/logout;
- credential validation;
- account registration;
- identity verification;
- role-based access;
- session management.

Otherwise, treat access as a precondition of the relevant use case.

## Granularity rules (CRUD, validation, calculation, persistence, output)

Keep use cases business-oriented and externally visible (see goal levels above).

CRUD rule:

- If the verbal model explicitly says create, edit, delete, approve, assign, publish, etc., model those as separate use cases when they are actor goals.
- If the verbal model only says manage/administer, use a general `Gestionar ...` use case unless the text supports decomposition.

Validation/calculation/persistence rule:

- Internal validations are not use cases.
- Calculations are not use cases unless the actor explicitly asks the system to calculate something as a goal.
- State updates, internal registration, persistence, and generated identifiers are usually postconditions, not use cases.
- A validation may be a use case only when it is an observable interaction with an external service or actor, such as a payment gateway, identity provider, medical device, sensor, or external registry.

System-output rule:

- `Generar comprobante`, `Emitir certificado`, `Enviar notificación`, or similar may be use cases only when they represent meaningful services visible to an actor.
- Do not directly associate the receiving actor as initiator unless that actor requests the output.
- If the output is automatic and mandatory, prefer postcondition or a limited `<<include>>` only if it improves comprehension or academic traceability.
- If the output is conditional, exceptional, or optional, consider `<<extend>>` only if it is externally observable and important.
- Add an external notification actor only when the text mentions electronic notification, email/SMS/messaging, or an external delivery service can be reasonably inferred; otherwise keep the output internal to the system boundary.

## Relationships: simple associations first, include/extend with restraint

Actor–use-case **associations are the backbone** of the diagram. `<<include>>`, `<<extend>>`, and generalization are refinements to be used sparingly — recognized practitioner guidance is emphatic that overusing them is a leading cause of analysis paralysis and adds little real value (see `references/standards-alignment.md`). Default to **none**, and add one only when its gate is fully satisfied and it genuinely improves clarity.

Use `<<include>>` only if all are true:

1. The included behavior is mandatory for the base use case.
2. The behavior is externally meaningful or testable as a separate subgoal/service.
3. Extracting it improves clarity (e.g., it is shared by two or more base use cases).
4. It is not being used merely to show temporal order.
5. It is not an internal validation, calculation, persistence operation, state update, generated identifier, or UI step.

Use `<<extend>>` only if all are true:

1. The behavior is optional, conditional, exceptional, or role-dependent.
2. The base use case can complete without it.
3. The extension is externally observable.
4. The extension improves clarity.
5. It does not represent a minor internal validation failure or low-level error handling step (those belong in the textual alternate/exception flows).

Prefer a compact diagram of actor goals over a dense dependency web. When in doubt, leave the relationship out and capture the behavior in the use case text.

## Generalization rules

Use actor generalization only when a general role is explicit or clearly inferable and multiple specialized actors share behavior.

Use case generalization is rarely worth it: avoid it in first approximations, and use it only when there are clear functional variants of a general goal and it demonstrably improves clarity. Prefer separate use cases or textual alternate flows instead.

## Use case naming and the diagram–text link

Name each use case as an **active-voice infinitive verb plus a domain-model noun/complement** (e.g., `Reservar habitación`, `Programar cita`, `Reportar incidente`). Use the Domain Model's terms so the same vocabulary flows from domain model → diagram → textual specification.

Remember the diagram is a table of contents: each use case name is the title of a short textual use case, ideally expressible in the classic two-paragraph form — one paragraph for the basic course (what the actor and system do when all goes well) and one for the alternate courses (what can go differently). If a candidate cannot be named as a clear actor goal, or cannot be written as such a short specification, it is probably a step, rule, or internal effect, not a use case.

## Internal traceability matrix

For every actor and use case candidate, internally track:

- source sentence or phrase from the verbal model;
- related Domain Model term, if any;
- candidate type: actor, use case, precondition, postcondition, internal step, validation, workflow step, external system;
- decision: include, exclude, merge, rename, or move to textual specification;
- reason.

Do not show this matrix in code-only mode. Show it only in review, audit, or explanation mode.

## Iterative Audit Loop

Do not return the first draft as final. Build the diagram the way use case modeling is actually taught — draft it, audit it against the gates, correct it — and converge on a clean, minimal summary. Before returning (generate and refactor modes) and as the backbone of review mode, run an internal loop:

1. **Refine.** Produce or update the diagram: actors outside the boundary, actor goals inside, associations, and only justified include/extend.
2. **Audit.** Inspect the current draft against, in order: (a) the use case candidate quality gate and the PlantUML contract; (b) the anti-pattern catalog in `references/anti-patterns.md`; (c) viewpoint separation, actor-association discipline, access/auth gate, include/extend restraint, and goal levels; and (d) when a `.puml` file exists and tools can run, `scripts/validate_use_case_puml.py`.
3. **Correct.** Fix each finding, or make a deliberate decision to keep it and note why (e.g., a justified external-system actor).
4. **Check convergence and stop (quantified).** The loop closes when all of these hold at once: **zero critical and zero major findings**; **at most two minor** ones, documented and justified; **every use case and every actor traceable** to the verbal model; and **two consecutive passes with no new findings** — one clean pass can be luck, two cannot. **Hard cap: five passes.** If critical or major findings remain at the cap, do **not** declare success: deliver the best available result, mark the status **`AUDIT NOT PASSED`**, list the open findings, and say what input or user decision would close each one. A declared failure is more useful than an optimistic all-clear, because the user can act on it. The cap is also methodological: the diagram is meant to be a lightweight summary, so once it cleanly shows the actor goals, adding more use cases or relationships usually subtracts clarity. Genuine trade-offs (a candidate that could be a use case or a postcondition; an output that could be include or extend) are surfaced as short review notes instead of looping.

Keep the loop's passes private in generate mode and return the converged diagram. In review or audit mode, you may show a concise convergence summary of what changed and what stabilized.

## Review severity levels

When reviewing a diagram, classify findings as:

- **Critical**: violates UML semantics or system boundary.
- **Major**: confuses actor goals with internal steps, or invents unsupported functionality.
- **Moderate**: excessive include/extend, visual clutter, weak traceability, or overconnected actors.
- **Minor**: naming, layout, package, or readability issue.
- **Suggestion**: optional improvement.

## Visual quality

Prefer:

- one clear dominant use case when the problem is one scenario;
- simple associations over dense dependency webs;
- few, justified include/extend relations;
- packages only for clear business areas;
- readable left-to-right layout;
- short, active-voice use case names.

Do not optimize visual simplicity by deleting required actor goals.

## Validation and regression mindset

When a saved `.puml` file is available and code execution is available, run:

```bash
python scripts/validate_use_case_puml.py path/to/use_case_diagram.puml
```

Use the validator as a mechanical risk detector inside the Iterative Audit Loop, not as proof of conceptual correctness. Warnings require analyst judgment.

For recurring evaluation, use the cross-domain examples in `references/regression-examples.md` and verify expected actors, dominant use case, allowed use cases, forbidden internal steps, and external services.

## If the user asks for a `.puml` file

Create one `.puml` file containing only the PlantUML script. Use a clear lowercase filename such as `caso_01_casos_uso.puml` unless the user provides a specific name.
