---
name: master-skills
description: Use when a task needs a capability from the master skills library (15 domains - development, business systems, AI, research, SEO, marketing, data, devops, security, testing, design, automation, product, documentation, support) and no more specific installed skill clearly covers it, or when the user asks what the library can do. SEO goes to seo-master; routing normally happens through master-auto-orchestrator. Not a substitute for a specific skill that already matches.
---

# Master Skills Library

## Purpose
Catalog of imported skills (43 from external repositories) plus an index of every installed skill grouped into 15 domains, with licenses and source attribution preserved.

## When to use
- A request maps to a library domain but no installed skill name matches.
- The user asks what skills/capabilities exist for a domain.
- An imported skill (read-in-place, no slash command) fits the task.

## When NOT to use
- A specific installed skill already matches (use that one directly).
- SEO tasks -> `seo-master`. Dashboards/KPIs/charts -> `erp-saas-analytics-visualization`. Substantial software builds -> `universal-development-planner`.

## Inputs
The user's task and the project context; domain is inferred.

## Core workflow
1. Read `RULES.md` and `ROUTER.md`; choose the domain folder(s) silently.
2. Open `<domain>/SKILL.md` for imported skills and the pointer to `INSTALLED.md`.
3. Open only the one skill needed (imported: path in the domain file; installed: invoke with the Skill tool).
4. Chain domains with `DEPENDENCIES.md` when the task spans domains.
5. Execute, verify, report.

## Decision rules
- Prefer an installed specific skill over an imported generic one.
- Same-name variants of installed skills are in `_alternates/`; use them only to compare, never auto-switch.
- Do not copy a capability into a second domain; link via `DEPENDENCIES.md`.

## Edge cases and failure handling
- Domain unclear -> search `99-UNCLASSIFIED/INSTALLED.md`, then the orchestrator registry.
- Imported skill needs an external account (e.g. connector tools) -> say so and fall back.
- Source license unknown (composio repo has no LICENSE) -> keep use internal; see `_licenses/README.md`.

## Validation
Confirm the chosen skill's SKILL.md exists, its instructions match the task, and dependencies are satisfied before executing; verify results with the matching testing/validation skill.

## Output requirements
Result of the task as a short `DONE`; no routing narration.

## Example
"Draft a LinkedIn post series" -> 06-MARKETING/social-media imported linkedin skills -> follow the post-writer instructions -> deliver posts.

## Related / dependencies
`REGISTRY.md`, `ROUTER.md`, `RULES.md`, `DEPENDENCIES.md`, `AUDIT.md`, `_licenses/`, `_alternates/`, `_merged/`, `QUALITY-AUDIT/`. Router: `master-auto-orchestrator`.

## References
`REGISTRY.md` (index), domain `INSTALLED.md` files (installed skills per domain).
