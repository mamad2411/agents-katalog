---
name: mauro-coding-style
version: 1.3.0
description: Use for PHP/MySQL/JavaScript repositories developed in the Mauro house style. Applies reusable naming, database, compatibility, simplicity, reuse-first and AI/LLM integration conventions independently of the Mauro CRUD framework.
---

# Mauro Coding Style

Shared coding conventions for Mauro PHP/MySQL/JavaScript applications.

This Skill defines the reusable technical dialect of Mauro projects. It is independent from any specific application and from the Mauro CRUD framework.

## Activate when

Use this Skill when:
- a repository is identified as a Mauro project;
- the repository `AGENTS.md` or `PROJECT.md` points to Mauro coding conventions;
- new PHP/MySQL/JavaScript code should follow the established Mauro house style;
- a project-specific task needs naming/database/compatibility conventions that are shared across Mauro applications.

Do not activate solely because a repository happens to use PHP, MySQL or JavaScript.

## Ownership boundary

This Skill owns reusable style and conventions only.

It does not own:
- generic agent autonomy/safety → global/repository `AGENTS.md`;
- project-specific architecture/facts → `PROJECT.md`;
- Mauro CRUD T0/T1/T2/T3 contracts → `mauro-crud`;
- PHP AI/LLM integration workflow and safety → `php-ai-integration`;
- schema/data/index/trigger/stored-routine migration safety → `mysql-change-safety`;
- feature planning, bug investigation or code review → focused workflow skills;
- deployment/FTP policy → deployment workflow;
- secrets → runtime secret storage.

When repository evidence contradicts a shared convention, preserve the repository's current behavior and classify the difference as a project-specific deviation. Forward-looking house-style rules for new or substantially rewritten code still apply unless runtime compatibility forbids them.

## Design philosophy

- Prefer simple, explicit code over unnecessary abstraction.
- Preserve compatibility and existing business behavior before modernization.
- Do not introduce a framework, ORM, service container, build system or architectural layer unless the task clearly benefits from it.
- Do not rewrite working legacy code merely to satisfy fashionable best practices.
- Prefer small, localized changes with clear execution paths.
- Reuse an established local pattern before inventing a new one.
- Keep business/domain terminology in Italian when the codebase uses Italian.
- Optimize for maintainability by the actual team and codebase, not theoretical purity.

## Repository-first reuse contract

Before creating a new function, helper, component, interaction pattern, query shape or abstraction, follow:

```text
DISCOVER → REUSE → ADAPT → CREATE
```

Search in this order:
1. same file/page/module;
2. same repository;
3. same Mauro/framework family;
4. shared skill conventions;
5. only then create something new.

Rules:
- reuse an existing implementation when semantics match;
- adapt the closest established pattern when exact reuse is not possible;
- create a new abstraction only when no suitable existing one exists or when the requirement explicitly needs different behavior;
- local project consistency is preferred over generic best practice unless the local pattern is unsafe, defective, incompatible, or explicitly being replaced;
- do not create near-duplicate helpers, wrappers or feature-specific utilities when a general existing abstraction already covers the need;
- repository search is part of implementation, not an optional cleanup step.

## PHP conventions

- Follow the PHP version actually supported by the repository.
- Preserve existing bootstrap/include patterns unless explicitly refactoring them.
- Prefer direct, readable control flow.
- Before creating a helper or utility, search the repository for equivalent definitions and usages; reuse the established helper when semantics match.
- Reuse existing global/helper functions when they are the established local abstraction.
- A reusable helper must be named for its behavior, not for the feature that first needs it, and belong in the repository's canonical shared-helper area when sharing is justified.
- Before calling a non-local function, verify that its definition exists and that the real bootstrap/include chain makes it available in that execution path.
- Use PHP short array syntax `[]` for all new arrays. When modifying existing code, use `[]` for arrays added or substantially rewritten, but do not mass-convert unrelated legacy `array()` syntax.
- Keep multiline HTML built inside PHP strings semantically indented and readable as maintainable markup, even when the resulting output would be identical.
- When a family of functions uses a single `$params` associative array, preserve that convention for neighboring functions.
- Do not introduce namespaces, Composer packages, classes or dependency injection into a legacy area only for stylistic reasons.
- When Composer is already present or a new dependency is justified, keep dependency scope explicit and minimal.
- Never embed secrets or API keys in source code.

## Database conventions

Apply when consistent with the repository or when creating a new Mauro schema:

- Primary key: `ID`, integer auto-increment unless the project has an established alternative.
- Foreign/reference fields: `ID` + entity name, e.g. `IDAzienda`, `IDUtente`, `IDCorso`.
- Boolean/state flags: prefix `IS_` where the existing schema uses this convention.
- Derived/denormalized display fields: prefix `Tab_`; when the project maintains them through DB triggers/procedures, do not write them from PHP.
- Lookup/config tables may use the established `tab_` prefix.
- Preserve existing table/column casing and Italian domain names.
- Do not introduce declared foreign keys, ORM mappings, prepared-statement migrations or schema renames as incidental cleanup in a legacy project.
- Security fixes are not blocked by style conventions: when a task is security-sensitive, use the safest change compatible with the application and its blast radius.

## JavaScript/UI conventions

- Preserve the repository's existing frontend stack; do not replace jQuery/vanilla/Bootstrap/Tailwind merely for modernization.
- Extend existing helpers and interaction patterns when practical.
- Before introducing new markup/classes/interaction conventions, inspect analogous UI already present in the same module/repository.
- Prefer native project layout, iconography, action ordering, labels, tooltips and interaction behavior over generic framework defaults.
- Avoid new build tooling unless the repository already uses it or the task requires it.
- Preserve existing UI behavior unless the task explicitly changes it.
- Additive UI actions must not accidentally alter neighboring controls, links or permissions.
- Load `frontend-change` for concrete presentation/interaction work.

## Naming and domain language

- Keep established Italian business terms unchanged.
- Preserve existing function, table, field and route names unless renaming is the explicit task.
- Prefer names that match the surrounding codebase over generic English abstractions.
- Do not translate domain concepts only to make code appear more conventional.

## AI / LLM integration for PHP

For PHP applications that require LLM or agentic functionality, use **Neuron AI** as the default application-level AI abstraction when runtime compatibility permits.

This section owns only the house-style choice. Load `php-ai-integration` for implementation, validation, tool safety, provider portability, failure handling and persistence boundaries.

Rules:
- Prefer `neuron-core/neuron-ai` over direct provider-specific SDK calls for new PHP AI integrations.
- Provider/model/API keys belong in environment/runtime secret storage, never committed source.
- Reuse an existing project abstraction instead of creating parallel AI clients.
- Direct raw provider calls are a documented project deviation when Neuron cannot support a required capability or an existing legacy integration must be preserved.
- Neuron AI currently requires PHP 8.1+. On older runtimes, do not silently introduce an incompatible dependency; preserve the current integration, upgrade runtime explicitly, or isolate AI behind a compatible service boundary.
- For current Neuron APIs and supported providers, use official Neuron documentation/skills rather than memorized signatures.

## Source-of-truth order

For a concrete repository:

1. current repository code and runtime constraints;
2. repository `AGENTS.md`;
3. `PROJECT.md` and registered durable project knowledge;
4. this shared Skill;
5. assumptions.

## Verification

After changes:
- apply ADS chapter 06 minimum sufficient verification proportional to scope/risk;
- inspect the final diff for unintended modernization, duplication or naming drift;
- verify that any new helper/component/pattern was preceded by repository discovery and is actually necessary;
- verify newly added/reworked PHP arrays use `[]` without unrelated mass conversion;
- verify non-local helper/function calls are actually defined and reachable through the execution path;
- inspect multiline generated HTML for source readability when touched;
- verify DB naming and derived-field behavior when persistence is touched; load `mysql-change-safety` when schema/data/index/trigger/routine changes are involved;
- for UI work, verify functional correctness plus native visual/interaction consistency through `frontend-change`;
- for AI/LLM work, verify provider selection/configuration is not hard-coded into business logic and no secret is committed;
- explicitly state runtime checks that could not be executed.
