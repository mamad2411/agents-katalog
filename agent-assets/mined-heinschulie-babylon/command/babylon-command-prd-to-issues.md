---
allowed-tools: Bash(gh *), Bash(bun *), Read, Grep, Glob, Agent
description: Break a PRD into independently-grabbable GitHub issues using tracer-bullet vertical slices
argument-hint: [PRD issue number or URL]
model: opus
---

# Purpose

Break a PRD into independently-grabbable GitHub issues using vertical slices (tracer bullets). Each issue is a thin end-to-end slice through all integration layers — not a horizontal layer slice. Each sub-issue is linked as a native GitHub sub-issue to the parent PRD issue. Follow the `Instructions` and `Workflow` to interview the user, draft slices, and create issues.

## Variables

PRD_REF: $ARGUMENTS

## Instructions

- Each slice must cut through ALL layers end-to-end (schema, API, UI, tests) — never horizontal layer slices
- **Behaviors to Test is the TDD agent's sole work order** — if a slice touches frontend, frontend behaviors MUST appear in the Behaviors to Test list, not only in Acceptance Criteria. Backend-only Behaviors to Test on a full-stack slice guarantees the frontend won't be built.
- **Interleave backend and frontend behaviors by feature, not by layer.** Do NOT list all backend behaviors first and all frontend behaviors last — this causes the TDD agent to complete backend, feel "done," and skip frontend. Instead, group by feature: backend behavior → its frontend wiring → next feature's backend → its frontend wiring. Example: "addReaction creates entry" → "clicking reaction badge calls addReaction" → "getReactionCounts returns grouped counts" → "reaction bar displays Badge components with counts."
- A completed slice must be demoable or verifiable on its own
- Prefer many thin slices over few thick ones
- Slices are either HITL (requires human interaction like arch decision or design review) or AFK (can be implemented and merged without human interaction) — prefer AFK
- Create issues in dependency order (blockers first) so real issue numbers can be referenced
- Do NOT close or modify the parent PRD issue
- Use the issue template defined in the Workflow for all created issues
- Each sub-issue must be linked to the parent PRD issue as a native GitHub sub-issue via the GraphQL addSubIssue mutation

## Workflow

1. If PRD_REF is provided, fetch it with `gh issue view <number> --comments`. If not provided, ask the user for the PRD issue number or URL, then fetch it.
2. If the codebase has not been explored yet, explore it to understand current state relevant to the PRD
3. Draft vertical slices — for each slice identify:
   - **Title**: short descriptive name
   - **Type**: HITL / AFK
   - **Blocked by**: which other slices must complete first
   - **User stories covered**: which user stories from the PRD this addresses
4. Present the breakdown as a numbered list and ask the user:
   - Does the granularity feel right? (too coarse / too fine)
   - Are the dependency relationships correct?
   - Should any slices be merged or split further?
   - Are the correct slices marked as HITL and AFK?
5. Iterate until the user approves the breakdown
6. For each approved slice, assess implementation complexity:
   - `trivial` — single-file change, cosmetic, config tweak
   - `standard` — multi-file, straightforward logic
   - `complex` — architectural, multi-system, requires deep reasoning
   Create a GitHub sub-issue linked to the parent PRD issue using the `createSubIssue()` function from `adws/src/github.ts`. This function handles both issue creation AND sub-issue linking (GraphQL `addSubIssue` mutation) in a single call. Add labels: `sub-issue`, a type label (`bug`, `enhancement`, or `chore`), and the corresponding `complexity:<level>` label per issue.

   ```bash
   bun -e "
   import { createSubIssue } from './adws/src/github.ts';
   const result = await createSubIssue(PARENT_NUMBER, 'Issue title', \`FULL_BODY\`, ['sub-issue', 'enhancement', 'complexity:standard']);
   console.log(JSON.stringify(result));
   "
   ```

   Do NOT use inline GraphQL commands — `createSubIssue()` handles node ID resolution and the `addSubIssue` mutation internally.

### Issue Template

**CRITICAL — Behaviors to Test is the TDD agent's sole work order.** A TDD agent will implement ONLY what appears in the Behaviors to Test list, top-to-bottom. If a behavior is not in that list, it will not be built. Therefore:

- Every layer touched by this slice (schema, backend function, frontend component, wiring) MUST have at least one behavior in the list
- Frontend behaviors are behaviors too: "Clicking X calls Y", "Component renders Z when query returns data", "Empty state shows message W"
- If the slice touches UI, the LAST behaviors in the list must be frontend integration behaviors that prove the backend is wired to the UI
- Acceptance Criteria is a review checklist — it does NOT drive implementation. Never put implementation requirements only in Acceptance Criteria.

```
## Interface Specification

Public API, function signatures, types, and data structures this slice introduces or modifies. Be specific enough that a TDD agent can write tests from this section alone.

## Behaviors to Test (prioritized)

Interleave by feature — do NOT group all backend first, all frontend last:

1. [Backend] Feature A core behavior — describe expected input/output
2. [Frontend] Feature A wiring — UI calls backend and renders result
3. [Backend] Feature B core behavior — describe expected input/output
4. [Frontend] Feature B wiring — UI calls backend and renders result
5. [Frontend] Empty/error states display correctly

**Total: N behaviors (X backend, Y frontend)** ← include this count line

Order matters — a TDD agent will work through these top-to-bottom. This list is the COMPLETE work order — every item is mandatory. If a slice touches frontend, frontend behaviors MUST appear here (not only in Acceptance Criteria). Interleaving forces the agent to context-switch between layers instead of treating frontend as a skippable tail.

## Mocking Boundaries

What's real vs stubbed in tests for this slice:
- **Real**: [e.g., Convex functions, utility modules]
- **Stubbed**: [e.g., external API calls, auth session]

## Acceptance Criteria

Review checklist — the review step verifies these AFTER implementation. Do not put requirements here that aren't already covered by a Behavior to Test above.

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Dependencies

- **Blocked by**: #<issue-number> (if any), or "None — can start immediately"
- **Blocks**: #<issue-number> (if any)

## User stories addressed

Reference by number from the parent PRD:

- User story 3
- User story 7
```

## Report

List all created issues with their numbers, titles, types (HITL/AFK), and dependency relationships. Include a link to each issue and a summary of the overall breakdown structure.
