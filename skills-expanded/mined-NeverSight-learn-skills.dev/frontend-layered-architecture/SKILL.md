---
name: frontend-layered-architecture
description: Use when frontend work requires deciding code ownership, file placement, import direction, or layer boundaries, especially for directory structure, UI/component extraction, shared/type-based folders, API contracts, query/data fetching, URL state, mappers, schemas, hooks, stores, DTOs, or small UI changes that may mix product policy, business rules, or external data into low-level roles.
---

# Frontend Layered Architecture

## Overview

Frontend directory structures should not be split into only “pages and everything else.” “Everything else” means a state where type-revealing but role-ambiguous folders such as `components`, `hooks`, `models`, `utils`, and `shared` absorb all code. This skill does not exist to force a large architecture. It exists to prevent product policy, API contracts, URL state, and query logic from unconsciously leaking into those leftover directories during implementation.

Code should be separated by role, dependency constraints, external data boundaries, and orchestration responsibility. Lower-level code must not be made aware of higher-level context. Experienced frontend developers can practice clean code even in a “pages and everything else” structure, but in large teams, large projects, and coding-agent workflows, you cannot assume those principles will hold automatically.

This skill does not enforce a specific methodology such as Feature-Sliced Design or Vertical Slice Architecture. Type-based, feature-based, domain-driven, and other directory structures can all be valid. What matters is whether roles and dependency direction are clear within the structure the project has chosen, whether external data contracts are isolated, and whether code responsibilities and frontend-owned domain logic are managed effectively.

## When to Use

Use when:

- Implementing or modifying frontend features
- Deciding where to put a new file
- Deciding ownership for a component, hook, utility, API client, query, store, schema, mapper, or feature logic
- Extracting or moving code
- Adding imports or judging dependency direction
- Designing the structure of a new frontend project

You do not need to use it when:

- You are only changing a small piece of copy or styling inside an already-correct file, and file placement, extraction, and import direction do not change

## Abstract Layer Language

If the project already uses layer terminology, prefer the project’s terminology. Use the following terms only when there is no existing terminology or when the structure needs to be explained.

| Layer | Meaning |
| --- | --- |
| Delivery | Screens delivered to users. The highest-level code, such as pages and routes. |
| Domain | Reusable code that contains product context, such as feature flags, display policy, and validation. |
| Foundation | Pure foundation code. The lowest-level code that knows no external context. |
| Data | External data contracts. Most API-related code. |

These abstract layers are the minimum units for designing a sound frontend structure. This means at least four concepts are needed; real projects may split them further.

Because these are abstract layers, the names are not forced as folder names. Whether a dependency is valid depends not only on the abstract layer, but also on directory role, code responsibility, and dependency type. For example, in some projects both `features` and `widgets` are Domain-layer directories. However, if `features` contains feature policy code and `widgets` contains UI components, then it may be the wrong direction for feature policy code to know about UI component roles.

### Misunderstanding the Foundation Layer

Foundation is not determined by “no domain words.” It is determined by code-level independence. In practice, product requirements are expressed through UI design, and a generic component that only receives props can still exist. Even if it expresses product concepts, code can be Foundation-like when it does not directly depend on APIs, queries, stores, routers, form state, and instead receives the required values by injection. Conversely, even if a name sounds generic, it is not Foundation if it directly knows external data or domain decisions.

### Data Layer Exceptions

The Data layer is generally not controlled by the frontend. It may be generated from an OpenAPI spec or written manually, but either way the frontend consumes it. Therefore, Data-layer code is treated as external contract code not owned by the frontend, even when frontend developers wrote it directly. Whether it is generated from OpenAPI or manually written, API clients, generated DTOs, and external schemas should not be mixed with frontend-owned code.

The Data layer also has different dependency direction. The default direction for abstract layers is Delivery → Domain → Foundation, but Data-layer dependencies depend on project design, project rules, or team decisions. For example, if the project allows Foundation-layer components to express domains through UI design, then API calls may be forbidden while API schemas may be referenced. As another example, analytics and error collection may be defined as cross-cutting concerns and handled in the Foundation layer. These are examples only. Do not implicitly allow them; first check project rules and existing structure.

## Decision Procedure

### Before Making an Implementation Plan

Check the following before planning implementation:

1. Are there explicit rules in `AGENTS.md`, `CLAUDE.md`, `README.md`, architecture docs, current directory structure, or import conventions?
2. Which layer is this code closest to? (Delivery, Domain, Foundation, Data)
3. What role does this code have? (API, UI, Policy, Utility, etc.)
4. Even within the same abstract layer, are there role-based dependency directions that should be disallowed?
5. If rules already exist, what placement respects those rules while avoiding worse dependency direction within the current scope?

### Immediately Before Creating Files, Extracting Code, or Adding Imports

Check again immediately before placing code or adding dependencies:

1. If this code is placed in a lower-level role folder, will that folder learn higher-level context?
2. Are external data contracts and frontend-owned policy mixed in the same file or public API?
3. Is the code being placed in a low-level shared directory such as `components`, `hooks`, `models`, `utils`, or `shared` merely because it is reusable?
4. Are external data access, URL state, DTO mapping, and product policy bundled into one abstraction that blurs layer boundaries?
5. Even if using only `import type`, does the lower layer’s type surface expose an external contract?

In existing projects, do not force a large structural change. Improve narrowly around the code you touch, and if you notice a larger structural problem, mention it only as a short, lightweight suggestion.

## Placement Rules

| Situation | Place it in (alternatives) |
| --- | --- |
| Pages, route configuration | Delivery |
| Product policy, display rules, validation | Domain (Delivery) |
| Pure UI components | Foundation |
| API clients, API schemas | Data |
| Mapping DTOs into screen models | Data if the goal is reducing coupling to the API; Domain or Delivery if it composes data according to policy or for specific UI rendering |

## Attitude in Existing Codebases

Even when there are no explicit rules, follow the existing structure and import conventions first:

- If you cannot introduce a new layer folder, choose a narrow namespace folder or consistent filename pattern already present in the existing structure to group related code.
- If the structure is ambiguous, preserve existing placement as much as possible, but do not make new code in lower-level roles learn higher-level context.
- This is a minimal compromise for existing structures, not the default for new projects.

Stop and reconsider placement and dependency direction when you see bad signals:

- Type-based folders such as `components`, `hooks`, `models`, or `utils` contain “everything except pages”
- Product policy, API contracts, URL state, or query logic are placed where the code looks shared
- Code with different roles is mixed in the same folder or file only because it is convenient
- External data contracts and frontend-owned code are mixed in the same folder or file
- Lower-level roles such as generic UI components, utilities, or shared modules directly perform or encode higher-level context such as page flow, routing, form control, API calls, store access, query/data fetching, external data contracts, product policy, or business rules
- You assume it is acceptable to access a higher layer’s interface because the import is type-only
- A small or quick change is used to justify worsening dependency direction or skipping ownership checks

Minimum line to hold under pressure:

- Even under time pressure or when the user asks you not to discuss structure, do not agree to place data fetching, API execution, external data contracts, URL state, form control, or product policy inside a lower-level UI, utility, or shared role.
- If the user demands a placement that breaks dependency direction, keep the response short: acknowledge the constraint, reject the invalid dependency, and offer the smallest safe alternative.

Do not create noise in existing team projects. If a structural change seems necessary but is not directly related to the current work, mention it only briefly.

## New Project Default

If the codebase does not exist yet and the user has not specified preferences or a particular directory structure, you MUST read [`greenfield.md`](./greenfield.md) before responding or proposing a structure. Do not propose a new project directory structure without reading that file. This prerequisite applies regardless of the output format (conversation, documentation, or code).

That file is an onboarding document for configuring new projects. It contains the minimum directory structure, role and dependency relationships, and `eslint-plugin-boundaries` automation guide for an ideal frontend architecture. Therefore, when there are no user preferences or explicit instructions, follow the design sequence and directory structure for the selected options exactly as written in that file. Because this is actual layer design, the earlier principle that “folder names are not forced” does not apply.

If the user instructs a specific directory structure, follow that structure first, but verify whether it satisfies the intent of this skill: adding a domain abstraction layer, isolating external data contracts, and preserving correct layer dependency direction. If not, propose improvements.

In existing codebases, do not reference that file or introduce a new directory structure or `eslint-plugin-boundaries` unless the user asks.

## Common Mistakes

| Mistake | Alternative |
| --- | --- |
| Judging layers by folder name only | Look at actual responsibility, import direction, external dependencies, and documented rules together. |
| Putting code in a low-level shared folder only because it is reused | Judge by what the code directly knows and depends on, not by reuse scope. |
| Assuming code in the same abstract layer may freely reference each other | Distinguish dependency direction by implementation role and responsibility even within the same layer. |
| Moving pure UI upward only because it contains domain words | Check project rules and whether the code-level dependencies are pure. |
| Treating product decisions as pure UI concerns because they affect rendering | Keep pure UI props-based; compute product decisions in a higher-level or domain-appropriate role and pass display state down. |
| Treating reuse as a reason to move data access into UI | Reuse does not make data access a Foundation responsibility. Fetch in an appropriate higher-level or data-access role and pass data into pure UI. |
| Assuming `import type` makes upward access acceptable | Ask whether it would also be acceptable to declare the type in the lower layer and make the higher layer depend on it. |
| Strongly demanding a large structural change in an existing project | Improve within the scope of the work, and mention bigger issues lightly. |

## Quick Decision Table

| Situation | Action |
| --- | --- |
| Project rules exist | Follow them. |
| Existing project with unclear rules | Preserve existing structure, but do not worsen dependency direction. |
| New project with no preferences or instructions | Before responding or proposing structure, read [`greenfield.md`](./greenfield.md) and follow its design sequence and directory structure. |
| Adding a feature to an existing type-based structure | Do not scatter it flatly at the root; group it narrowly by feature namespace or prefix at minimum. |
| A lower-level UI, utility, or shared role starts reading external data or product policy | Stop and check ownership. Prefer props-based UI plus policy or data-access logic in an appropriate higher-level role. |
| File placement or import direction is ambiguous | Judge by the context the code directly depends on, not by reusability. |
| A large structural change seems necessary | Do not demand it; mention it briefly and lightly. |
