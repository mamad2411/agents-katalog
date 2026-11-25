---
name: flutter-explain-codebase
description: Explains a Flutter project codebase in a structured, developer-friendly way, including architecture, state management, data flow, navigation, dependencies, risks, and prioritized next actions.
license: MIT
metadata:
  version: 0.1.0
  owner: mdazadhossain95
---
# Explain Flutter Codebase

## Purpose
Use this skill to analyze and explain an existing Flutter codebase quickly and clearly for onboarding, handoff, debugging, and planning refactors.

## Activation
Activate when the user asks to explain a Flutter app, module, architecture, folder structure, or how parts of the codebase work together.

## Inputs
Collect minimal context before analysis:
- Scope: whole project, feature folder, or specific files.
- Goal: onboarding, debugging, architecture review, refactor planning, performance review.
- Depth: quick, standard, or deep explanation.

If user gives no scope, default to project-level explanation.

## Analysis Workflow
Follow this order:

1) Project map
- Identify main folders and responsibilities.
- Summarize app entry points and bootstrapping.

2) Architecture
- Determine architecture style (layered, feature-first, mixed).
- Map core boundaries: presentation, domain/logic, data, shared/core.

3) State management
- Identify state solution(s): Riverpod, Bloc/Cubit, GetX, Provider, setState, others.
- Explain where each is used and why.
- Flag inconsistent or mixed usage hotspots.

4) Navigation and app flow
- Explain routing setup and screen transitions.
- Summarize primary user journey paths.

5) Data flow and integrations
- Trace data path from UI event to repository/service and back.
- Explain API clients, DTO/model mapping, caching, and persistence.
- Note authentication and push integration points if present.

6) Dependencies and cross-cutting concerns
- Highlight important packages and what each is used for.
- Explain logging, error handling, dependency injection, config/env handling.

7) Quality and risks
- Identify likely tech debt areas, coupling, duplication, and test gaps.
- Identify potential runtime-risk points (null handling, async race, network assumptions).

8) Actionable next steps
- Provide prioritized recommendations (high impact first).
- Include low-risk quick wins and medium-term refactors.

## Output Format
Return explanation in this structure:

1. Codebase Overview
2. Folder/Module Map
3. Architecture Summary
4. State Management Summary
5. Navigation and User Flow
6. Data and Integration Flow
7. Dependency Notes
8. Risks and Gaps
9. Recommended Next Steps

Keep it practical and concrete. Reference real files/symbols when available.

## Behavior Rules
- Prefer facts from code over assumptions.
- If evidence is missing, state assumptions explicitly.
- Avoid generic advice without tying it to observed structure.
- For deep explanations, include call-path examples.
- For quick mode, keep to high-signal architecture and flow.

## Optional Modes
- Quick mode: high-level map + top 5 findings.
- Standard mode: full structure above.
- Deep mode: include feature-by-feature walkthrough and targeted refactor plan.

## Validation Checklist
Before final response, verify:
- Scope is clear.
- Architecture and state management are identified.
- Data and navigation flow are explained.
- Risks are concrete and actionable.
- Next steps are prioritized.
