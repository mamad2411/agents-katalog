---
name: fullstack-design-backend-orchestrator
description: "Create premium modern UI design (v0/lovable style), production-grade backend architecture, and auto-optimize even rough user commands before execution. Use when building React or React Native products that need clean system design, scalable APIs, strict quality gates, and prompt-to-output reliability."
argument-hint: "Describe product idea, target users, platform (web or native), tech stack, and constraints"
user-invocable: true
disable-model-invocation: false
---

# Fullstack Design + Backend Orchestrator

## Outcome
This skill converts rough user prompts into an optimized implementation brief, then delivers:
- A premium, modern design system and UI structure
- React or React Native component architecture
- A production-grade backend plan and code scaffold
- Validation checklists to reduce rework and runtime bugs
- Automatic command normalization so short or mixed-language instructions still become high-quality prompts

## When to Use
Use this skill when the user asks for one or more of these:
- "Design this like v0/lovable"
- "Build modern, clean, error-free UI"
- "Write backend like top-tier models"
- "Improve my prompt before executing"
- "Give fullstack architecture and implementation"

## Inputs Required
Collect or infer these fields before implementation:
- Product goal and target audience
- Platform: web (React/Next.js) or native (React Native/Expo)
- Preferred stack: TypeScript, state management, DB, backend runtime
- Constraints: deadline, team size, performance requirements, security level
- Must-have screens/features and non-functional requirements
- Raw user command text (including short, mixed-language, or incomplete instructions)

If fields are missing, infer safely and explicitly list assumptions.

## Procedure

### Step 1: Command Intake + Prompt Compiler (mandatory)
Treat every user request as potentially incomplete and normalize it before planning.

Command normalization rules:
- Preserve original intent and tone, but rewrite into precise engineering language.
- Accept short forms, mixed Uzbek/English, and ambiguous wording without failing.
- Expand vague words ("mukammal", "zamonaviy", "toza", "hatosiz") into measurable quality criteria.
- Detect missing constraints and fill them using safe defaults; clearly mark assumptions.

Rewrite normalized input into an optimized internal prompt using this structure:
1. Role and objective
2. Product context
3. Functional requirements
4. Non-functional requirements
5. Design language constraints
6. Backend architecture constraints
7. Output format requirements
8. Acceptance criteria

Then validate the optimized prompt:
- Is scope testable?
- Are constraints concrete?
- Are outputs measurable?
If not, iterate once and improve it.

Prompt acceptance contract:
- Never execute directly from raw command text.
- Always execute from the optimized prompt version.
- Always include an "Assumptions" block when user input is incomplete.

### Step 2: Product Blueprint
Produce a concise implementation blueprint:
- Feature map
- Information architecture
- Screen/page map
- Domain model summary
- API boundary map
- Integration risks

Decision branch:
- If requirements are unclear: choose an MVP cut and document exclusions.
- If enterprise/security-heavy: enforce stricter backend defaults (RBAC, audit logs, rate limiting, idempotency).

### Step 3: Design System + UI Direction
Generate a high-quality design direction (not generic boilerplate):
- Visual concept: typography, spacing, color tokens, elevation, motion
- Component set: buttons, forms, cards, nav, tables/lists, dialogs
- States: hover/focus/disabled/loading/error/empty/success
- Responsive rules: mobile/tablet/desktop
- Accessibility: color contrast, keyboard navigation, focus visibility, semantic structure

For React Native:
- Use native-friendly spacing, gesture patterns, safe area behavior, platform-specific interactions
- Prefer performant list rendering and layout patterns

Frontend non-negotiables:
- Avoid generic template aesthetics; each design must define a clear visual identity.
- Define and use design tokens for color, spacing, type scale, radius, and shadows.
- Ensure responsive behavior for key breakpoints and edge-case content lengths.
- Include loading, empty, error, success, and skeleton states for primary screens.
- Ensure WCAG-aware contrast and visible focus states.

### Step 4: Frontend Architecture
Create structured frontend plan and code guidance:
- Folder structure and naming conventions
- Data flow and state boundaries
- Reusable component strategy
- Error boundary and loading strategy
- Form validation strategy
- API client patterns and caching approach

Implementation defaults (unless overridden):
- Web: Next.js + TypeScript strict mode + reusable component architecture.
- Native: React Native (Expo) + TypeScript + platform-aware UI primitives.
- Styling: token-driven system with reusable primitives, not ad-hoc inline styles.
- Quality: lint + typecheck + build must pass before completion.

Quality gates:
- No duplicated business logic in UI layer
- Clear separation of presentation and data orchestration
- Type-safe models and props
- Consistent spacing rhythm and typography hierarchy across screens
- Interaction states are complete for all critical components

### Step 5: Backend Architecture + Implementation
Build backend approach with production concerns first:
- API-first contract (request/response/error schema)
- Domain services and repository boundaries
- AuthN/AuthZ strategy (JWT/session/OAuth, RBAC)
- Input validation and sanitization
- Observability: structured logging, tracing hooks, metrics
- Reliability: retries, timeouts, idempotency, pagination, rate limiting
- Data integrity: transactions and migration strategy

Output style:
- Start with architecture decisions and trade-offs
- Provide endpoint contract examples
- Provide implementation scaffold with test strategy

### Step 6: Prompt-to-Output Alignment Check
Before final output, verify the result still matches the optimized prompt:
- Every must-have requirement is mapped to an artifact
- Security and performance requirements are addressed
- Missing pieces are clearly marked as TODO with rationale

### Step 7: Final Delivery Format
Return in this exact order:
1. Optimized Prompt (used internally)
2. Assumptions and constraints
3. Design system and UI plan
4. Frontend architecture and implementation plan
5. Backend architecture and API plan
6. Quality checklist
7. Next implementation steps (small, executable sequence)

## Quality Checklist
Mark each item Pass/Fail:
- Prompt is specific and testable
- Raw user command was normalized before execution
- Optimized prompt is shown and traceable to original intent
- UI direction is modern and coherent
- Accessibility checks are included
- React/React Native architecture is scalable
- Backend includes auth, validation, observability, and reliability
- API contracts are explicit and versionable
- Error handling strategy is defined end-to-end
- Testing strategy includes unit + integration + critical e2e paths

## Failure Handling
If the request is too broad or conflicting:
- Split into milestones (MVP -> V1 -> V2)
- Prioritize critical user journeys
- Return what was intentionally deferred

If user command is too short:
- Infer product type from context
- Apply safe defaults
- Continue execution with transparent assumptions instead of blocking

If tech stack is not provided:
- Default to TypeScript-first stack and explain why.

## Example Invocation
/fullstack-design-backend-orchestrator Build a subscription-based fitness app for mobile and web. Optimize my prompt first, then produce modern UI direction and backend architecture with security and testing plan.

/fullstack-design-backend-orchestrator Menga zamonaviy va mukammal React Native design va kuchli backend ber. Avval promptimni mukammallashtirib ol.
