---
name: mobile-ux-architect
description: Turn a mobile product brief or feature definition into an actionable UX architecture covering actors, journeys, task flows, decisions, recovery paths, information architecture, navigation, screen map, object lifecycles, state matrix, permissions, device surfaces, and meaningful iOS/Android differences. Use before mobile wireframes, UI design, prototypes, or implementation, and when an existing mobile flow needs restructuring or completeness review.
---

# Mobile UX Architect

Translate product intent into a traceable interaction structure. Define what each screen and state must accomplish without choosing visual style or drawing wireframes.

## Select the mode

- **Create**: derive a new UX architecture from a product brief.
- **Refine**: resolve gaps, contradictions, or excess complexity in an existing flow.
- **Feature**: insert a bounded feature into an existing navigation and object model.

Use `mobile-product-brief` first when the user problem, audience, activation, MVP boundary, or trust model is unresolved. Use `mobile-reference-research` for source discovery and `analyze-mobile-ui` for detailed reference analysis when reference products drive key decisions.

## Establish the input contract

Prefer `product-brief.json` plus its human-readable brief. Validate the upstream JSON when its validator is available. Record:

- Source brief path, schema version, and date.
- Primary actors, scenarios, objects, constraints, and open decisions.
- Required platform and device integrations.
- Assumptions added by this Skill.

Stop and request a decision only when an unresolved issue changes the safety model, primary actor, core value loop, or MVP boundary. Otherwise proceed with a labeled assumption.

## Follow the workflow

### 1. Create a requirement ledger

Translate the brief into stable `R1`, `R2`, and later requirement IDs. Preserve the source path and mark each item `must`, `should`, or `could`. Include product value, trust, accessibility, recovery, and platform requirements—not just features.

Do not silently add scope. New UX assumptions remain separate from upstream decisions.

### 2. Model actors and objects

Define each actor's goal, permissions, and ownership boundaries. Model durable objects and their lifecycle states before naming screens. Examples include invitation, membership, draft, order, check-in, delivery, permission, and widget configuration.

Read [references/flow-modeling.md](references/flow-modeling.md) for actor, object, flow, and state rules.

### 3. Prioritize scenarios

List entry, activation, repeat-use, recovery, management, and exit scenarios. Assign `critical`, `important`, or `supporting` priority. Every must-have requirement must appear in at least one scenario.

### 4. Map user journeys

For each critical scenario, show trigger, user intent, steps, system feedback, friction or uncertainty, recovery, and observable outcome. Do not invent emotion as a fact; mark anticipated concerns as design risks.

### 5. Build decision-complete task flows

Create stable `F1`, `F2`, and later flow IDs. Include:

- Entry conditions and deep links.
- User actions and system responses.
- Decisions and branches.
- Permission denial, cancellation, timeout, offline, conflict, and partial failure where applicable.
- Completion condition and safe exit.
- Resume behavior after interruption.

Use Mermaid only when it materially clarifies branching. Keep the structured JSON authoritative.

### 6. Design information architecture

Choose top-level destinations from recurring user goals, not a desired tab count. Separate persistent destinations, hierarchical detail, modal tasks, global overlays, and system handoffs. Define back behavior, state preservation, deep links, and where unfinished work resumes.

Read [references/mobile-ia-patterns.md](references/mobile-ia-patterns.md) before finalizing navigation.

### 7. Build the screen map

Assign stable `S1`, `S2`, and later screen IDs. For each screen specify:

- Single responsibility and user question answered.
- Entry points and exit destinations.
- Primary and secondary actions.
- Objects read or changed.
- Required states and recovery.
- Requirement and flow coverage.
- Platform-specific expression where behavior differs.

Do not create a separate screen when a state, sheet, dialog, inline disclosure, or system surface is more appropriate. Do not specify color, typography, pixel layout, or decorative components.

### 8. Complete the state matrix

Cover applicable first-use, empty, partial, loading, slow, offline, failed, retrying, permission, account, object lifecycle, destructive, blocked, stale, expired, conflict, and accessibility-pressure states.

Every state needs a trigger, user-visible meaning, available action, recovery, and owning screen or surface. Never use a generic “error state” to hide distinct consequences.

### 9. Specify permissions and device surfaces

For each permission define contextual pre-prompt, system prompt trigger, denial behavior, restricted state, settings recovery, and core-value fallback.

For widgets, notifications, Live Activities, lock-screen controls, sensors, cameras, biometrics, and similar surfaces define activation, freshness, privacy exposure, tap destination, unsupported behavior, and platform differences. A system surface cannot be the only path to core value.

### 10. Preserve platform behavior

Define outcome parity separately from implementation parity. Record meaningful differences in navigation, back behavior, sheets, permission flow, widgets, system settings, target sizes, insets, text scaling, process restoration, and assistive technology.

### 11. Check traceability and complexity

Require:

- Every `must` requirement maps to a scenario, flow, screen, and acceptance signal where applicable.
- Every screen maps to at least one requirement or platform obligation.
- Every destructive or sensitive action has confirmation, consequence copy, and recovery when possible.
- Critical flows have non-happy paths and interruption behavior.
- The architecture contains no orphan screen, dead-end state, or circular dependency without an exit.

### 12. Produce and validate

When files are requested or the Skill is part of a design workflow, create:

- `ux-flow.md` using [assets/ux-flow-template.md](assets/ux-flow-template.md).
- `screen-map.md` using [assets/screen-map-template.md](assets/screen-map-template.md).
- `ux-architecture.json` using [assets/ux-architecture-template.json](assets/ux-architecture-template.json) and [references/ux-architecture-schema.md](references/ux-architecture-schema.md).

Run `python3 scripts/validate_ux_architecture.py <path-to-ux-architecture.json>` and fix every error. Treat warnings as review prompts.

When a low-fidelity layout contract is needed before visual styling, hand the validated architecture to `mobile-wireframe`; do not overload this Skill with visual layout decisions.

## Enforce the output order

1. Architecture summary and source contract.
2. Requirement ledger and assumptions.
3. Actors, objects, and lifecycle states.
4. Prioritized scenarios and journeys.
5. Critical task flows and recovery.
6. Information architecture and navigation.
7. Screen map and screen responsibilities.
8. State, permission, and device-surface matrices.
9. Platform differences, traceability, and acceptance signals.
10. Open questions and confidence.

## Run the quality gate

Read [references/ux-architecture-rubric.md](references/ux-architecture-rubric.md) and revise every blocker before completing.

Do not finish until critical flows are decision-complete, must-have requirements are traceable, recovery is explicit, platform differences are meaningful, and the output remains visual-design agnostic.
