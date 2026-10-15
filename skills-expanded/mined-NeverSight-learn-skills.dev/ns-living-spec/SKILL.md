---
name: ns-living-spec
description: (NS) Consolidate delivered deltas into living domain specs under docs/specs/ — INDEX.md and per-domain markdown. Use after version closure when requirements, Approved code review, and execution-handoff exist; in ad-hoc mode when ns-coder (or the human) passes an Approved behavioral diff and docs/specs/ already exists; or in appearance mode from ns-proto-creator / ns-proto-visual-guide (no Code Review gate) for product-visible UX behavior. Updates specs incrementally; never overwrite unrelated content. Do NOT run Version/Ad-hoc before code review approval; appearance mode is the exception for prototype/visual handoff.
license: Apache-2.0
metadata:
  author: nextstage-brasil
  version: "1.3"
depends:
  - ns-harness
---

# Living Spec Consolidator

Maintain `docs/specs/` as current functional truth of product.

## Session boot

See `../../ns-harness/references/session-boot.md` and `../../ns-harness/references/artifact-layout.md`.

## Modes

| Mode | When | Source of truth | Code Review gate |
| ---- | ---- | --------------- | ---------------- |
| **Version** (default) | Version closure after delivery | `docs/versions/{version_san}/` artifacts | Required (`Approved`) |
| **Ad-hoc** | Invoked by `ns-coder` (or human) after `Code Review: Approved` | `{task_description}` + approved `git diff` | Required (`Approved`) |
| **Appearance** | Invoked by `ns-proto-creator` or `ns-proto-visual-guide` | Guide/prototype path + short behavioral delta | **None** |

**Appearance** if invoker pass mode `appearance` (or equivalent: guide/prototype path + behavioral delta, no review verdict). **Ad-hoc** if mode `ad-hoc` (or equivalent: no `{version_san}`, task description + approved diff). Else **Version**.

## When invoked

- Version closure post `Code Review: Approved` — **Version**
- Ad-hoc coding, review **Approved**, `docs/specs/` exists — **Ad-hoc**
- Prototype create/evolve or normative visual guides documenting behavioral UX — **Appearance**
- **Not** Version/Ad-hoc before `Approved` verdict

## Prerequisites

### Version mode

- `docs/versions/{version_san}/requirements.md`
- Invoker reports `Code Review: Approved` (score ≥ 9) — no `code-review-report.md` required
- `docs/versions/{version_san}/execution-handoff.md` (tasks completed)

### Ad-hoc mode

- `docs/specs/` already exists (**not** create tree from scratch)
- Invoker reports `Code Review: Approved` (score ≥ 9)
- `{task_description}` + approved working-tree diff (behavioral change)
- **Skip** (no writes) if diff non-behavioral: cosmetic, rename-only, pure refactor with no API/schema/UX/domain behavior change — report skipped

### Appearance mode

- Input: path to appearance guide and/or `prototype/` surface + short **behavioral delta** (what users can do / see changed or captured)
- May **create** `docs/specs/` + `INDEX.md` if missing
- SHALL only for **product-visible** behavior (flows, fields, states, permissions cues)
- **Never** paste `Element | How it should appear` tables into domain specs — link guide instead
- **Skip** pure chrome polish (spacing, color tweak, font swap, no behavior change) — report reason
- No Code Review / Approved requirement

## Workflow

Shared steps 1–4 all modes. Changelog label differs by mode.

### 1. Identify affected domains

Map features to canonical domains (examples):

| Feature area      | Domain file        |
| ----------------- | ------------------ |
| Auth, login, RBAC | `auth.md`          |
| Users, profiles   | `users.md`         |
| Billing           | `billing.md`       |
| Notifications     | `notifications.md` |
| Reports           | `reports.md`       |
| Integrations      | `integrations.md`  |
| Agent / graph     | `agent.md`         |

Naming: English, kebab-case, singular (`user-profile.md`). Multi-domain features update multiple specs.

**Ad-hoc:** map from `{task_description}` + diff only — no invent unrelated domains.

**Appearance:** map from behavioral delta + guide/prototype scope only; add domain links to appearance docs under Related / references when useful.

### 2. Per domain

**If `docs/specs/{domain}.md` missing:** create from `references/domain-spec.template.md`

**If exists:** read entirely; **append or update** — never blind overwrite

Per relevant feature:

- Add or update `### Requirement:` blocks (SHALL + scenarios)
- Update `## Data model` + `## Endpoints` when schema/API changed (Version/Ad-hoc)
- Appearance: prefer UX/behavior requirements; no invent APIs/schemas not evidenced
- Append `## Changelog` entry:
  - **Version:** `**{version_san}** — {ISO date}: {summary}`
  - **Ad-hoc:** `**adhoc-YYYY-MM-DD** — {ISO date}: {summary}` (summary from task + diff)
  - **Appearance:** `**appearance-YYYY-MM-DD** — {ISO date}: {summary}`

### 3. Update INDEX.md

Create or update `docs/specs/INDEX.md`:

```markdown
# Domain specs — {product_name}

| Domain | File                 | Last updated | Versions      |
| ------ | -------------------- | ------------ | ------------- |
| auth   | `docs/specs/auth.md` | {date}       | {version_san or adhoc-YYYY-MM-DD or appearance-YYYY-MM-DD} |
```

### 4. Consolidation report

Emit short report for handoff:

```
## Living specs updated
| Domain | Action | File |
...
Mode: {version|ad-hoc|appearance}
Requirements added: N
Requirements updated: N
New specs: N
```

If skipped (non-behavioral, polish-only, or Ad-hoc missing `docs/specs/`):

```
## Living specs skipped
Reason: {missing docs/specs/|non-behavioral diff|chrome polish only}
```

## Critical rules

- English for spec content
- Requirements use verifiable SHALL language
- Read before write on existing specs
- Planning orchestrator read `INDEX.md` before new version requirements
- Ad-hoc must not create version artifacts under `docs/versions/`
- Ad-hoc must not invent `{version_san}`
- Appearance must not paste normative Element|How tables into specs
- Appearance must not require Code Review Approved

## Related skills

- `ns-spec-driven` — reads living specs when planning (`references/requirements-generator.md`)
- `ns-reviewer` — prerequisite approval for Version/Ad-hoc
- `ns-coder` — may invoke ad-hoc after Approved
- `ns-proto-creator` / `ns-proto-visual-guide` — may invoke appearance mode
