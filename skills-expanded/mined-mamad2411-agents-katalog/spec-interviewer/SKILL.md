---
name: spec-interviewer
description: This skill should be used when the user wants to create a detailed specification document through an in-depth interview process. It conducts a thorough, multi-round interview covering technical implementation, UI/UX, concerns, tradeoffs, edge cases, and requirements before writing the final spec to a file.
argument-hint: "[instructions] e.g., 'a real-time chat application' or 'an API for managing inventory'"
allowed-tools: AskUserQuestion, Write
---

# Spec Interviewer

## Overview

Conduct an exhaustive, multi-round interview to produce a comprehensive specification document. The interview digs deep into non-obvious aspects of the project — architecture tradeoffs, failure modes, edge cases, security implications, scalability concerns, and user experience nuances — before synthesizing everything into a structured spec file.

## Interview Process

### Phase 1: Core Understanding

Begin by reading the provided instructions to understand the domain. Ask the first round of questions focused on:

- The core problem being solved and who it's for
- What success looks like and how it will be measured
- Existing constraints (tech stack, budget, timeline, team size, infrastructure)
- What has already been decided vs. what is open for discussion

Limit each round to 2-4 focused questions. Avoid surface-level questions whose answers are obvious from the instructions.

### Phase 2: Deep Exploration

Based on answers from Phase 1, drill into specifics across these dimensions. Cover each that is relevant, across multiple rounds:

**Technical Architecture**
- Data model shape, relationships, and access patterns
- State management approach and consistency requirements
- Integration points with external systems or APIs
- Offline behavior, caching strategy, sync conflicts

**User Experience**
- Critical user flows and their happy paths
- Error states, empty states, loading states
- Permissions model and what different user roles can see/do
- Accessibility requirements and device/browser targets

**Edge Cases & Failure Modes**
- What happens when things go wrong (network failures, partial saves, race conditions)
- Data validation rules and boundary conditions
- Concurrency scenarios (multiple users editing, duplicate submissions)
- Migration path from existing systems if applicable

**Operational Concerns**
- Monitoring, alerting, and observability needs
- Deployment strategy and rollback plan
- Performance targets (latency, throughput, payload sizes)
- Security considerations (auth, data privacy, rate limiting)

**Business & Product**
- Prioritization: what is MVP vs. future phases
- Dependencies on other teams or external factors
- Compliance or regulatory requirements
- Internationalization and localization needs

### Phase 3: Clarification & Gaps

Review all gathered information. Identify contradictions, ambiguities, or gaps. Ask targeted follow-up questions to resolve them. Continue until confident the spec can be written without guesswork.

### Phase 4: Write the Spec

Once the interview is complete, synthesize all answers into a structured specification document. Write it to a file named based on the project (e.g., `spec-<project-name>.md`). Confirm the output path with the user before writing.

The spec should include:

1. **Project Overview** — problem statement, goals, success metrics
2. **Scope** — what is in and out of scope, MVP vs. future
3. **User Roles & Permissions** — who uses the system and what they can do
4. **Functional Requirements** — detailed feature descriptions organized by domain
5. **Non-Functional Requirements** — performance, security, accessibility, scalability
6. **Technical Architecture** — data model, integrations, infrastructure decisions
7. **User Flows** — step-by-step descriptions of key workflows
8. **Edge Cases & Error Handling** — documented failure modes and expected behavior
9. **Open Questions** — anything that still needs resolution
10. **Milestones** — phased delivery breakdown if applicable

## Guidelines

- Ask non-obvious questions. Skip anything that can be trivially inferred from the instructions.
- Probe for contradictions. If the user wants "real-time" but also "offline-first," surface that tension.
- Be specific. Instead of "How should errors be handled?", ask "If a payment fails mid-checkout with items already reserved, should the reservation be held or released, and for how long?"
- Keep rounds short (2-4 questions) to avoid overwhelming the user.
- Continue interviewing until all relevant dimensions have been covered. Do not rush to write the spec.
- The spec document should be detailed enough that a developer could begin implementation without further clarification.

<instructions>$ARGUMENTS</instructions>
