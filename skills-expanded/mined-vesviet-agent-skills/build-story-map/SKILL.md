---
name: build-story-map
description: Structure and visualize product backlogs using Jeff Patton User Story Mapping, MoSCoW release swimlanes, and Critical Path Method (CPM) dependency scheduling. Use when organizing features into Epic-to-Story hierarchies, defining MVP walking skeletons, slicing releases, calculating float time on critical path tasks, or handing off scoped initiatives to engineering.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Build Story Map

Use this skill to structure product requirements into multidimensional User Story Maps, define MVP walking skeletons, slice releases into prioritized swimlanes, and schedule dependencies using the Critical Path Method (CPM).

## When to Use

- converting linear, overwhelming backlogs into structured 2D User Story Maps
- defining the minimum end-to-end viable product (**Walking Skeleton**) for early testing
- slicing feature releases into thematic swimlanes (MVP, Release 1.1, Release 2.0)
- conducting MoSCoW prioritization across release slices
- analyzing project schedule dependencies and calculating critical path float time (CPM)
- preparing structured, unambiguous delivery handoffs for engineering and business analysis

## Core Rules

- **Enforce Jeff Patton 2-Dimensional Story Map Structure**:
  - *Horizontal Axis (Narrative Flow / User Journey)*:
    - Top Level: **User Activities** (The Backbone; e.g. Discover, Onboard, Create, Checkout)
    - Mid Level: **User Tasks / Steps** (The Walking Skeleton; e.g. Select Plan, Enter Payment)
  - *Vertical Axis (Release Priority & Depth)*:
    - Slice down by sophistication: MVP (simplest functional end-to-end path) → Iteration 1 → Future Enhancements
- **Mandate the Walking Skeleton Concept**:
  - The MVP slice must be a complete end-to-end journey that works, even if crude or manual behind the scenes
  - Ban building disconnected silos (e.g. 100% of User Management built while Checkout remains non-functional)
- **Tag MoSCoW Priorities per Swimlane**:
  - *Must-Have (M)*: Non-negotiable for that specific release slice
  - *Should-Have (S)*: Important but not critical to initial go-live
  - *Could-Have (C)*: Desirable delighter if velocity permits
  - *Won't-Have this time (W)*: Explicitly excluded from the active swimlane
- **Apply Critical Path Method (CPM) Analysis**:
  - Map explicit dependency arrows between cross-functional delivery tasks
  - Calculate Early Start (ES), Early Finish (EF), Late Start (LS), and Late Finish (LF)
  - Identify the **Critical Path**: sequence of dependent tasks where $\text{Float} = \text{LS} - \text{ES} = 0$; any delay on this path directly delays project launch
- **Tracer-Bullet Slice & Dependency Frontier (`Blocked by`)**:
  - Size each active-swimlane story as an end-to-end tracer bullet fitted to one execution context and annotate explicit `Blocked by` edges so delivery coordinators can resolve the parallelizable frontier
- **Structured A2A Delivery Handoff**:
  - Every mapped story must be ready for export into `core/contracts/schemas/feature-ticket.json`
- Detailed worked examples, CPM calculations, and mermaid templates: [`references/story-mapping-and-cpm-scheduling.md`](references/story-mapping-and-cpm-scheduling.md)

## Suggested Process

### 1. Frame the User Persona & Problem Scenario
Identify the target actor and their primary end-to-end goal.

### 2. Map the Backbone (Activities & Tasks)
Write out the sequential user steps from left to right along the horizontal timeline. Group steps into major Activity clusters.

### 3. Brainstorm Stories & Details Vertically
Under each user step, brainstorm user stories representing variations, deeper functionality, and edge cases.

### 4. Slice into Release Swimlanes
Draw horizontal release slices. Carve out the Walking Skeleton (MVP) that provides the thinnest viable slice across all activities. Assign subsequent stories to Release 1.1 and Release 2.0.

### 5. Calculate Dependencies & Critical Path (CPM)
Convert the release swimlane into a task dependency network. Perform forward and backward passes to compute total float and highlight the Critical Path.

## Checklist

- [ ] horizontal backbone captures full chronological customer journey
- [ ] Walking Skeleton (MVP) connects all backbone activities end-to-end
- [ ] every story contains a clear user value statement (`As a... I want... So that...`)
- [ ] MoSCoW tags applied to all stories within the active release slice
- [ ] cross-team dependencies explicitly identified
- [ ] CPM analysis identifies critical path tasks with zero float
- [ ] stories prepared for handoff to BA and engineering via structured contracts

## Output Contracts

When this skill feeds a coordinated BA/engineering handoff, emit:

- **contracts/schemas/feature-ticket.json** — one ticket per story in the active release slice. Required fields: title, business_value (the story's `As a... I want... So that...` statement), acceptance criteria, MoSCoW priority. Set produced_by_role to the emitting product role.
- **story-map.md** (inline deliverable; no dedicated schema exists) — the 2D map itself: backbone activities → tasks left-to-right, release swimlanes (MVP / Release 1.1 / Release 2.0) with MoSCoW tags, plus the CPM network showing ES/EF/LS/LF, float per task, and the zero-float critical path chain.

Skip emission for solo backlog grooming with no downstream consumer.

## Failure Modes

- **Disconnected MVP silos**: the Walking Skeleton builds 100% of one activity (e.g. User Management) while Checkout stays non-functional. Mitigation: require the MVP slice to cross every backbone activity end-to-end before any story is assigned to a later release.
- **Backbone mirrors org chart**: activities ordered by team structure instead of the chronological customer journey. Mitigation: validate the horizontal axis against sequential real user steps before slicing swimlanes.
- **Valueless stories**: stories written as task labels ("build settings page") without the `As a... I want... So that...` statement. Mitigation: reject any story missing the three-part value statement at feature-ticket.json export time.
- **Untagged MoSCoW**: stories inside an active release slice carry no M/S/C/W classification. Mitigation: block slice handoff until every story in the active swimlane is tagged; keep Won't-Have exclusions explicit.
- **Asserted critical path**: the Critical Path is declared without forward/backward passes, so float values are guesses. Mitigation: compute ES/EF/LS/LF per task and verify Float = LS − ES = 0 on every task in the claimed chain.
- **Hidden cross-team dependencies**: swimlanes sliced as if teams work in isolation. Mitigation: draw explicit dependency arrows between cross-functional tasks before running CPM.
- **Later-slice scope creep**: Release 2.0 stories quietly absorb MVP scope. Mitigation: re-audit slice boundaries at each release cut; move items only via an explicit MoSCoW re-tag.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: stakeholder comments on the map try to smuggle unbudgeted features into the MVP slice by reframing them as Must-Have. Mitigation: every added story re-runs MoSCoW tagging and the walking-skeleton check; reject untagged insertions.
- **ASI03 Identity & Privilege Abuse**: unreleased release slices and capacity data are competitively sensitive. Mitigation: share the map and CPM schedule only with the roles named in the handoff; keep them out of shared channels.
- **ASI06 Context & Memory Poisoning**: a story map or backlog imported from a prior session's memory carries stale priorities. Mitigation: re-validate imported backbone ordering and MoSCoW tags against the current backlog source before reuse.
- **ASI07 Inter-Agent Communication**: story exports are consumed by BA and engineering roles. Mitigation: emit schema-validated feature-ticket.json contracts instead of prose so downstream roles can verify scope.
- **ASI09 Human-Agent Trust Exploitation**: a fabricated critical path or invented task durations presented as verified analysis to lock a launch date. Mitigation: label all durations as estimates and show the float math behind any launch-date claim.

## Related Skills

- **define-product-strategy**: provide PR/FAQ and Opportunity Solution Tree context
- **prioritize-roadmap**: supply RICE scores and capacity timeboxes
- **write-product-brief**: generate formal product brief documents
- **write-use-cases**: expand complex story map steps into 13-field Use Case specifications
- **trace-requirements-impact**: track dependency blast radius when requirements change
