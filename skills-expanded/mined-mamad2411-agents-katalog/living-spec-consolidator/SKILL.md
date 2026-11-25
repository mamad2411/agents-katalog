---
name: living-spec-consolidator
description: Consolidate delivered version deltas into living domain specs under docs/specs/ — INDEX.md and per-domain markdown. Use after version delivery when requirements, code-review-report, and execution-handoff exist — typically at version closure. Updates specs incrementally; never overwrite unrelated content. Do NOT run before code review approval.
depends:
  - nextstage-harness
---

# Living Spec Consolidator

Maintain `{specs_root}/` as the current functional truth of the product.

Default `{specs_root}` = `{product_root}/docs/specs/`.

## Harness discovery

See `../nextstage-harness/references/harness-discovery.md` and `../nextstage-harness/references/artifact-layout.md`.

## When invoked

- After version closure workflow (post code review)
- **Not** before `code-review-report.md` exists for the version

## Prerequisites

- `{product_root}/docs/versions/{version_san}/requirements.md`
- `{product_root}/docs/versions/{version_san}/code-review-report.md`
- `{product_root}/docs/versions/{version_san}/execution-handoff.md` (tasks completed)

## Workflow

### 1. Identify affected domains

Map features to canonical domains (examples):

| Feature area | Domain file |
|--------------|-------------|
| Auth, login, RBAC | `auth.md` |
| Users, profiles | `users.md` |
| Billing | `billing.md` |
| Notifications | `notifications.md` |
| Reports | `reports.md` |
| Integrations | `integrations.md` |
| Agent / graph | `agent.md` |

Naming: English, kebab-case, singular (`user-profile.md`). Multi-domain features update multiple specs.

### 2. Per domain

**If `{specs_root}/{domain}.md` missing:** create from `references/domain-spec.template.md`

**If exists:** read entirely; **append or update** — never blind overwrite

For each relevant feature:

- Add or update `### Requirement:` blocks (SHALL + scenarios)
- Update `## Data model` and `## Endpoints` when schema/API changed
- Append `## Changelog` entry: `**{version_san}** — {ISO date}: {summary}`

### 3. Update INDEX.md

Create or update `{specs_root}/INDEX.md`:

```markdown
# Domain specs — {product_name}

| Domain | File | Last updated | Versions |
|--------|------|--------------|----------|
| auth | `docs/specs/auth.md` | {date} | {version_san} |
```

### 4. Consolidation report

Emit short report for handoff:

```
## Living specs updated
| Domain | Action | File |
...
Requirements added: N
Requirements updated: N
New specs: N
```

## Critical rules

- English for spec content
- Requirements use verifiable SHALL language
- Read before write on existing specs
- Planning orchestrator should read `INDEX.md` before new version requirements

## Related skills

- `requirements-generator` — reads living specs when planning
- `code-reviewer` — prerequisite approval
