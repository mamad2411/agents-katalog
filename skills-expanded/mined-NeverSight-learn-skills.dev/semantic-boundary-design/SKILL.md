---
name: semantic-boundary-design
description: Use when cross-layer feature, migration, integration, port, refactor, review, bug fix, or design planning needs one owner for user/domain meaning across UI, route, client state, command, API, storage, realtime, adapter, or presentation layers. Trigger for identity aliases, lifecycle/status, permissions/capabilities, route/query grammar, command payloads, result/event projection, freshness/fallback/revision semantics across representations, compatibility translation, duplicated meaning rules, or multiple representations of the same user/domain meaning. Do not use for read-only owner discovery, local flow cleanup after owners are clear, pure async responsiveness/freshness work, or scope-control alone.
---

# Semantic Boundary Design

## Purpose

Prevent semantic drift by assigning one owner to each meaning-defining decision.

Many layers may observe, pass, or render the same data. Only one layer should decide what that data means for identity, lifecycle, permission, commands, routes, events, compatibility, or presentation.

## Use / Do Not Use

Use this skill before or during cross-layer work when:

- one capability crosses several representations
- aliases, fallbacks, labels, statuses, permissions, or lifecycle rules are spreading through callers
- a non-owner caller starts parsing, normalizing, translating, or inferring meaning
- an adapter starts preserving product policy instead of translating shapes
- tests freeze helper internals instead of owner-boundary behavior

Do not use this skill for:

- tiny local edits with no semantic boundary movement
- read-only discovery of existing owners; use `source-owner-audit`
- local flow cleanup after owners are clear; use `structure-first`
- pure async freshness, responsiveness, or race-prone interaction work; use `interactive-state-flow`
- change-scope control alone; use `justified-change`

## Adjacent Skills

- `source-owner-audit` finds current source owners from evidence. This skill places semantic decisions once the owner question needs design.
- `structure-first` shapes the current unit after owners are known. This skill starts at the capability-wide owner ledger.
- `interactive-state-flow` specializes in freshness, pending, stale, and async presentation behavior. This skill handles freshness/fallback/revision only when it is semantic contract ownership across representations.
- `justified-change` keeps implementation scope proportional. This skill decides where meaning-defining rules belong.

## Operating Flow

1. Name the capability in user or domain terms.
2. List representation crossings: source record, read model, UI draft, user intent, route/query state, command input, API payload, command result, realtime patch, presentation model, compatibility adapter.
3. List semantic decisions: identity/alias, lifecycle/status, permission/capability, command grammar, route/navigation grammar, freshness/conflict/revision/pending/fallback, projection/presentation, compatibility.
4. Assign one owner per decision. Pick the smallest durable owner only when current source or explicit task context shows enough evidence and authority to decide the meaning. If no layer has both, write `decision needed -> missing evidence/authority` and name who must decide only when that decision owner is evidenced or explicitly provided.
5. Define caller boundaries: callers may pass, select, invoke, display, or render; callers must not interpret, normalize, re-decide, or preserve policy unless they own that decision.
6. Refactor only the scope justified by the current task.
7. Add guards that fail when semantic decisions leak into callers.
8. Hand off source discovery, local code shape, async freshness, or scope control to the adjacent owner skill when that concern becomes primary.

## Owner Selection Rules

- Schema or field aliases -> record/contract owner.
- User intent shape -> UI surface or command input owner.
- Final command payload -> session/command owner.
- API request parsing -> application route owner, not framework wrapper.
- Route or query grammar -> navigation owner.
- Permission or capability -> policy owner.
- Labels and actions -> surface/view-model owner.
- Result envelope, patch, or resync semantics -> application/realtime result owner.
- Stale, pending, fallback, conflict, or revision acceptance -> freshness-owning route, session, or screen owner.
- Compatibility behavior -> adapter translates shapes; policy ownership requires an explicit assignment.

## Drift Smells

- `x || y || z` fallback chains outside the record/contract owner.
- Duplicated lifecycle or status checks.
- UI code builds final command payloads directly from records.
- Route components parse or build shared query grammar.
- API wrappers read business request fields.
- Realtime or event handlers re-decide lifecycle, permission, or policy.
- Revision, conflict, pending, fallback, or freshness keys are duplicated.
- Adapters preserve policy instead of translating to the owner.
- Tests assert helper internals instead of owner-boundary behavior.

## Required Guards

Choose the smallest guard that protects the owner boundary:

- contract tests for alias normalization, command payload shape, route/query grammar, or result envelopes
- boundary tests showing callers pass/render/invoke without reinterpreting meaning
- negative cases for stale, fallback, permission, lifecycle, or compatibility behavior
- type or schema constraints that make duplicate interpretation hard to express
- regression tests for user-visible behavior that depends on the semantic decision

Do not freeze helper internals. Assert that the owner decides meaning once and callers cannot silently choose another meaning.

## Output Contract

Use this compact shape when reporting a plan, review, or implementation note:

- `Capability:` user/domain capability
- `Representation Crossings:` data or control forms involved
- `Semantic Decisions:` decisions that could drift
- `Owner Ledger:` `decision -> owner or decision needed -> reason`
- `Caller Boundaries:` allowed caller behavior and prohibited interpretation
- `Drift Smells:` observed or likely leaks
- `Required Guards:` tests, schemas, or checks
- `Handoffs:` adjacent skills or follow-up owners

## Final Gates

- Is the capability named in user/domain terms?
- Does every semantic decision have exactly one owner, or a named `decision needed`?
- Can callers observe, pass, render, or invoke without deciding meaning?
- Are adapters limited to translation unless policy ownership is explicit?
- Are fallback, freshness, lifecycle, permission, and compatibility decisions owned where they can be verified?
- Is refactor scope limited to the current task?
- Do guards verify owner-boundary behavior rather than helper internals?
