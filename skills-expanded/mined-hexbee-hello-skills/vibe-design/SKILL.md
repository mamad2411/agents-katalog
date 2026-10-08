---
name: vibe-design
description: Design, specify, implement, or review AI-native and Agent product interfaces with explicit product intent, domain semantics, controlled GenUI/A2UI behavior, design-system constraints, complete interaction states, and evidence-based evaluation. Use for Agent dashboards, copilots, conversational interfaces, generative reports, AI workflows, design specs, information architecture, component selection, anti-generic visual direction, UI critique, or turning an ambiguous AI product request into reusable design declarations and acceptance criteria.
---

# Vibe Design

Turn human design judgment into declarations an Agent can execute and checks an evaluator can audit. Optimize for controlled quality, not unconstrained generation.

## Origin

Use Alibaba Cloud Design's [Vibe Design Playbook](https://alibaba-cloud-design.github.io/vibe-designing-playbook/) as the conceptual source for this skill. This skill reorganizes the playbook's ideas into an executable Codex workflow and evaluation contract.

## Route the task

Choose the smallest applicable mode:

- **Specify**: turn a vague request into product intent, flows, states, boundaries, and acceptance criteria.
- **Design**: choose information architecture, page shape, component semantics, visual direction, and interaction behavior.
- **Implement**: inspect the repository's existing tokens, components, patterns, and constraints before changing code; preserve the product language.
- **Review**: inspect the actual artifact, collect evidence, score it against the relevant criteria, identify blockers, and return executable revision instructions.
- **Systematize**: extract repeated design judgments into reusable declarations, component rules, templates, or evaluation criteria.

Do not produce every possible artifact by default. Create only what the task needs.

## Core workflow

1. **Establish the brief**
   - Identify the user, goal, context, primary task, business risk, platform, and maturity stage.
   - Separate stated facts, discovered facts, assumptions, and unresolved decisions.
   - Do not present invented roles, thresholds, limits, breakpoints, policies, or domain rules as facts. Label useful placeholders as proposed defaults and list material values that require confirmation.
   - Classify the page shape: brand landing page, product console, conversational interface, data dashboard, content/documentation, or a justified custom shape.

2. **Make the function complete**
   - Define the main path and branch paths.
   - Cover loading, empty, error, permission, timeout, disabled, partial-success, undo/recovery, and destructive-action states as relevant.
   - State what the system may do automatically, what requires confirmation, and what it must never do.
   - Write testable acceptance criteria rather than subjective approval language.

3. **Choose the structural starting point**
   - Decide what deserves persistent space, what is contextual, and what appears only at a decision point.
   - Prefer an existing product template or shell when available.
   - Generate architecture variants only when different attention priorities are genuinely plausible; compare them by task outcome, not visual novelty.

4. **Map semantics to components**
   - Use existing product components and tokens when implementing in a repository.
   - Distinguish status, risk, category, action, navigation, feedback, and container roles.
   - Keep domain meaning, component semantics, and visual styling separate.
   - Do not hardcode a value when a design token exists. Expose a system gap instead of silently inventing a new convention.

5. **Decide what should be dynamic**
   - Use fixed UI for stable navigation, settings, repeated approvals, and durable information architecture.
   - Use GenUI only where task path, evidence, content structure, or user decision points vary with context.
   - Prefer controlled generation: let the Agent declare intent, data, actions, and behavior; let the client own components, tokens, accessibility, validation, and fallback.
   - Give users enough process visibility to judge and intervene, not an unfiltered execution trace.

6. **Refine craft**
   - Create a clear attention hierarchy and meaningful density.
   - Use color, surface, motion, and emphasis only when they communicate role or state.
   - Remove generic AI patterns: default purple-blue gradients, equal white-card grids, indiscriminate glass effects, decorative uppercase labels, emoji-as-icons, excessive pills, and purposeless bounce.
   - Preserve keyboard access, focus visibility, readable contrast, reduced-motion behavior, and recoverability.

7. **Evaluate and return**
   - Review the artifact, not the creator's intent.
   - Use available DOM/CSS checks, screenshots, click tests, content evidence, and task paths.
   - Separate deterministic defects from design judgment.
   - Do not let an average score hide a broken primary task, wrong domain logic, unreadable content, or disconnected states.
   - Return a small prioritized revision plan with evidence, impact, destination declaration, and a verifiable completion condition.

## Declaration map

Use these as distinct responsibilities:

| Declaration | Question it answers |
| --- | --- |
| `spec.md` | What must the feature do to be complete? |
| `domain.md` | What data, state, risk, permission, and action semantics are correct here? |
| `craft.md` | What cross-domain design quality rules prevent weak execution? |
| `design.md` | What visual roles, tokens, derivations, states, and gap policies are authoritative? |
| `components` | Which components are allowed, and what does each mean? |
| `template` | What page skeleton and density fit this scenario? |

Treat the skill as the scheduling contract and the evaluator as the acceptance contract. Do not duplicate rules across declarations.

## Read references selectively

- Read [references/design-engineering.md](references/design-engineering.md) when writing declarations, planning a page, selecting components/templates, or turning requirements into acceptance criteria.
- Read [references/dynamic-interaction.md](references/dynamic-interaction.md) when designing Agent loops, GenUI, A2UI, conversational workflows, dynamic cards, or generated reports.
- Read [references/evaluation.md](references/evaluation.md) when reviewing an artifact, building a rubric, defining a delivery gate, or creating revision instructions.
- Read [references/craft-and-lexicon.md](references/craft-and-lexicon.md) when setting visual direction, removing generic AI styling, or translating vague taste words into observable rules.

## Output contracts

Match the output to the request:

- For a **spec**, produce scope, information architecture, flows, component behavior, edge states, and Given/When/Then acceptance criteria.
- For a **design proposal**, include the chosen page shape, attention priority, key regions, component semantics, dynamic/fixed boundary, and unresolved risks.
- For an **implementation**, make the requested changes and verify the primary path, edge states, responsiveness, accessibility, and repository checks.
- For a **review**, lead with the release decision and blockers, then evidence-backed findings and a prioritized return plan.
- For a **design system extraction**, record each rule once in its proper declaration and state when it is invoked and how it is evaluated.

Never use “more polished,” “more premium,” or “improve the UX” as a final instruction without translating it into observable changes and acceptance conditions.

When evidence is incomplete, keep the work executable by distinguishing `confirmed`, `inferred`, `proposed default`, and `needs decision`; never conceal uncertainty behind precise-looking numbers.
