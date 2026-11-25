---
name: universal-capability-map
description: Build and maintain an evidence-backed, machine-readable map of what a software product actually supports.
version: 2.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [capabilities, product-map, evidence, verification, planning, coding-agents]
    related_skills: [hermes-agent-skill-authoring]
---

# Universal Capability Map

## When to Use

- Before planning or implementing — check what the product already
  supports, so you build only the missing or broken portion.
- After any completed change or release — update evidence and state so the
  map keeps reflecting reality.
- Before answering "does the product support X?" — answer from the map, not
  from memory or source-code name matching.
- When auditing a codebase or a claim — the map is the single source of
  truth for what exists, and every status must be derivable from evidence.
- The format is product-agnostic: desktop applications, web applications,
  APIs, CLIs, libraries, games, plugins/extensions, internal tools, agent
  systems, and other software products.

Don't use it for: Jira-style task tracking, full requirements management,
project-management frameworks, test-management platforms, or release
management. The map answers one question and stays small:

> What can this product actually do right now, and what evidence supports
> that claim?

## What it is

A lightweight, machine-readable, human-editable model of what a software
product actually supports. Capabilities are stable, named claims about
observable product behavior; evidence records prove (or disprove) each
claim; the current state is derived from the active evidence rather than
from vibes.

Three conceptual layers keep the methodology adaptable without weakening
its defaults:

1. **Core format** — the interoperable data model: capabilities, states,
   claims, evidence, dependencies, dimensions, scenarios, provenance.
2. **Recommended policy** — strong defaults: stable IDs, evidence before
   status claims, preserve history, explicit regressions, append rather
   than rewrite evidence, verify user-visible behavior, keep the map
   current with implementation changes.
3. **Optional advanced features** — scenario coverage, source fingerprints,
   commit-aware evidence, supersession, dimensions, dependency analysis.
   Adopt them only when a project needs them.

## The state model

Each capability has exactly one state:

| state | meaning |
| --- | --- |
| `unknown` | The capability exists in the map, but the repository has not been sufficiently inspected to determine implementation state. Lack of evidence is NOT proof of absence. |
| `not_implemented` | The capability has been inspected or explicitly declared absent. No usable implementation exists. |
| `partial` | Some meaningful portion exists, but the complete user-visible capability is not available. |
| `implemented` | The capability exists and has valid implementation-level evidence. |
| `verified` | The capability has current verification-level evidence demonstrating that it works as claimed. |

`deprecated: true` is independent of state — a capability can be
`verified` and deprecated, or `not_implemented` and not deprecated.

**State-change policy.** Status is not required to move only forward. The
rule is:

> Status must never be silently changed to hide history. Regressions and
> demotions are allowed, but historical evidence remains intact and the
> reason for the state change must be explicit.

A verified feature that later breaks becomes `partial`, `implemented`, or
`not_implemented` — with its previous verification history preserved and a
`regression:` (or `state_change_reason:`) note explaining the change. The
checker rejects silent demotions and claims above what evidence supports.

## Capabilities are claims

A capability is a **testable product claim**, not a feature label or an
implementation artifact. A good capability answers:

> What observable thing can the product do?

```yaml
- id: panel-docking
  name: Panel Docking
  area: workspace
  claim: A user can dock any dockable panel to each supported docking region.
  description: Optional longer explanation.
```

`claim` is strongly recommended and preferred for new maps. Prefer claims
about behavior ("a user can filter the list without reloading") over
implementation descriptions ("uses a debounced search input"). If a
capability cannot be phrased as an observable behavior, it is probably not
a capability.

## Dependencies

```yaml
depends_on:
  - drag-drop
  - layout-state
  - docking-target-rendering
blocked_by:            # optional
  - layout-engine-rewrite
```

Dependencies are **planning and reasoning information**, never
auto-promotion: the checker never marks a capability implemented merely
because its dependencies are implemented. The checker validates that every
referenced ID exists, rejects self-dependencies and obvious dependency
cycles, and the report identifies:

- dependencies per capability
- missing dependency IDs
- capabilities blocked by incomplete dependencies (a `depends_on` target
  that is not `implemented`/`verified`, or anything in `blocked_by`)
- high-impact dependencies used by many capabilities

## Aliases and tags

```yaml
aliases:
  - favorite models
  - pinned models
  - starred models
tags:
  - model-browser
  - ui
  - personalization
```

Aliases and tags exist for **discovery**: coding agents search aliases,
tags, IDs, and claims for a requested behavior, so a request phrased
"favorite models" still finds `model-favorites`. They reduce dependence on
guessing the exact canonical ID. The checker validates that both are lists
of non-empty strings.

## Sources and evidence

Two different things, kept deliberately separate:

- **`sources`** — *why the capability exists*: provenance links back to the
  spec, issue, task, user requirement, design, API contract, or release
  that called for it.
- **`evidence`** — *proof of current implementation or behavior*: what was
  actually run, observed, or reviewed.

```yaml
sources:
  - type: spec
    locator: docs/product-spec.md#panel-docking
  - type: issue
    locator: "#482"
```

Allowed source types: `spec`, `issue`, `task`, `user_requirement`,
`design`, `api_contract`, `release`, `other`. Sources are provenance
records, not evidence; a spec reference never makes a capability
implemented.

## Dimensions

Dimensions answer:

> Where is this capability complete or incomplete?

```yaml
dimensions:
  backend: implemented
  api: implemented
  ui: partial
  tests: verified
  docs: implemented
required_dimensions:   # optional
  - backend
  - ui
```

Dimension states use the same vocabulary (`unknown`, `not_implemented`,
`partial`, `implemented`, `verified`). The overall state is never
automatically derived from dimensions; the agent declares the overall
state explicitly. When `required_dimensions` is present, the checker warns
if any required dimension is incomplete (not `implemented`/`verified`).

## Evidence

One evidence record per file under `capabilities/evidence/`:

```json
{
  "uid": "EV-001",
  "capability_id": "auth-login",
  "kind": "test_result",
  "outcome": "pass",
  "locator": "tests/test_auth.py::test_login",
  "date": "2026-08-30",
  "commit": "abc123",
  "branch": "main",
  "version": "1.4.0",
  "notes": "Verified successful login and invalid-password rejection."
}
```

Required: `uid`, `capability_id`, `kind`, `outcome`. Optional: `scenario`,
`locator`, `date`, `commit`, `branch`, `version`, `environment`,
`platform`, `notes`, `supersedes`, `source_fingerprint`. Only the required
fields are needed for old/simple records — everything else is opt-in.

**Kinds prove different things.** No kind universally "outranks" another:

| existence-level (proves something exists or ran) | verification-level (demonstrates behavior) |
| --- | --- |
| `file_change`, `command_result`, `diagnostic`, `inspection`, `build_result` | `test_result`, `integration_test`, `e2e_test`, `review`, `manual`, `visual_review`, `accessibility_test` |

- a unit test may prove behavior in isolation
- an end-to-end test may prove integrated behavior
- manual or visual evidence may prove interaction or visual behavior that
  automation does not capture
- file existence alone proves very little

**Append, never rewrite.** Historical evidence is never edited or deleted.
A new record is appended; the old one stays as history. This is what makes
regressions visible.

## Freshness and supersession

Historical PASS is not permanent proof. Current state is derived from
**active** evidence — the most recent relevant evidence, or explicit
supersession:

```json
{ "uid": "EV-042", "supersedes": ["EV-041"] }
```

Rules:

- latest active verification PASS may support `verified`
- latest active implementation PASS may support `implemented`
- later FAIL evidence invalidates earlier PASS evidence for current-state
  derivation, unless a still-later PASS supersedes or resolves it
- superseded evidence is preserved but no longer authoritative
- when chronology cannot be determined confidently (e.g. PASS and FAIL
  with no dates), the checker reports **RECONCILIATION REQUIRED** instead
  of silently choosing

The checker validates supersession references (no dangling targets, no
cycles) and reports stale/superseded evidence counts.

## Verification scenarios

Optional, for capabilities whose claim contains multiple meaningful
behaviors:

```yaml
verification:
  scenarios:
    - id: dock-left
      description: Dock a panel to the left region.
    - id: dock-right
      description: Dock a panel to the right region.
    - id: persist-layout
      description: Restart application and restore docking layout.
```

Evidence may reference a scenario:

```json
{ "uid": "EV-105", "capability_id": "panel-docking", "scenario": "persist-layout", "kind": "e2e_test", "outcome": "pass" }
```

The checker validates scenario references and shows scenario coverage. A
capability claiming `verified` with declared scenarios must have
verification-level pass evidence for every scenario — otherwise the
checker reports RECONCILIATION REQUIRED. Projects that do not need
scenarios simply omit them.

## What makes a capability verified

Verification comes from **verification-level evidence itself** — an active
`test_result`, `integration_test`, `e2e_test`, `review`, `manual`,
`visual_review`, or `accessibility_test` with outcome `pass` — not from a
string in `verified_by`. `verified_by` remains as optional contextual
metadata:

```yaml
verified_by:
  - PR-214
  - release-1.4.0
```

but it never substitutes for evidence. A capability is `verified` because
active verification-level evidence supports its claim. (Legacy maps that
used `verified_by` as the gate keep working, but produce a warning telling
you to add real verification evidence.)

## UI and support functions are first-class capabilities

The most common failure mode this map prevents: the core product works,
then someone says "now give it a good UI" — and the UI is terrible,
because its support functions were never enumerated, so the agent
improvises UI plumbing mid-flight. UI infrastructure is **ordinary product
capability**, not secondary polish. Enumerate it on the map from the start:

- **State** — loading, error, empty, stale, optimistic state, undo/redo,
  persistence.
- **Interaction** — form validation, keyboard controls, focus management,
  drag/drop, selection, search, filter, pagination, contextual menus.
- **Presentation** — responsive layout, themes, typography, density,
  icons, localization, visual hierarchy.
- **Feedback** — progress, errors, warnings, confirmations, toasts,
  skeleton states.
- **Accessibility** — keyboard navigation, ARIA, contrast, screen-reader
  flow, reduced motion, scalable text.
- **Data** — fetch, cache, refresh, invalidation, offline handling, retry,
  staleness indicators.

Then the map reads like a build order: with the core `implemented` /
`verified` and the UI capabilities `not_implemented`, the report's gap
list IS the UI checklist. A working product whose support capabilities are
all `not_implemented` is not "done, plus needs UI"; it is a product whose
gap list happens to be the entire UI.

## How agents use the map

**Before implementation:**

1. Search aliases, tags, IDs, and claims for the requested behavior.
2. Determine whether it already exists.
3. Inspect dependencies and dimensions.
4. Follow active evidence.
5. Identify gaps or stale verification.
6. Build only the missing or broken portion.
7. Add fresh evidence after work.
8. Update current state without deleting history.
9. Re-run the checker.

**Before answering "does the product support X?",** answer from:

- the capability's `claim`
- its current status
- its dimensions
- its active evidence
- known regressions

— not from memory or source-code name matching alone. If no capability
matches, the honest answer is "not in the map" — which is itself a product
gap to surface.

## Method — create the map

1. **Inventory.** From the product spec or feature lists, enumerate every
   user-visible behavior the product must support, grouped by area. Cover
   the whole product: implemented, partial, not-yet-started, and
   un-inspected. Include support/UI functions (§UI) alongside core
   behaviors. One capability = one observable behavior with a stable
   kebab-case id (e.g. `auth-login`, `panel-docking`).
   Completion: every spec'd behavior appears exactly once.

2. **Declare.** Write `capabilities.yaml` — every capability with
   `id`, `name`, `area`, `claim`, and an initial state (`unknown` if not
   yet inspected, otherwise `not_implemented`). Add aliases/tags,
   dependencies, sources, and dimensions as they become known.
   Completion: the checker runs clean (warnings about missing claims
   acceptable at first).

3. **Evidence.** When a capability exists and works, append an evidence
   JSON under `capabilities/evidence/` (prefer a verification-level kind
   with the actual test as `locator`) and cite its `uid` in the
   capability's `evidence` list. Never reference an evidence file that
   does not exist.
   Completion: every promoted capability has at least one resolving
   active evidence ref.

4. **Set state from evidence.** Declare `implemented` only with
   implementation-level pass evidence; declare `verified` only with
   verification-level pass evidence. The checker will reject a state the
   evidence does not support.

5. **Commit the map.** Commit `capabilities.yaml` and the evidence files
   with the change that created/updated the capability — the map and its
   proof are declarative knowledge. Never commit runtime traces or logs
   into the evidence directory.

## Automatic maintenance — keep the map current

State changes only through the policy — evidence first, explicit reasons
for demotion — never by hand-editing to make the checker pass. Wire these
triggers into the normal completion flow so the map updates in the same
turn as the work:

1. **Every change / task completion.** Run the affected tests. For each
   capability with passing results, append the evidence, cite it, and set
   the state the evidence supports. Then run the checker.
2. **On VERIFIED task / PR / release.** Add verification-level evidence
   and set `verified` (plus `verified_by` as context) in the same change.
3. **On regression.** A failing test means: append the FAIL evidence
   (never delete or edit old evidence), demote with an explicit
   `regression:` reason, and let the checker confirm. Then fix and append
   fresh pass evidence — the history shows the full arc.
4. **Session start / periodic.** Run the checker and the report. Reconcile
   gaps, unknown capabilities, regressions, and any RECONCILIATION
   REQUIRED items. Investigate anything whose state the evidence does not
   explain.
5. **Spec changes.** When the product spec adds or changes behavior,
   extend `capabilities.yaml` in the same change. Never delete a
   capability id — ids are stable; add `deprecated: true` instead.

## Mechanical check

```bash
python scripts/check_capabilities.py .                    # validation
python scripts/check_capabilities.py --report .           # human-readable report
python scripts/check_capabilities.py --report --gaps .    # filtered report
python scripts/check_capabilities.py --report --area workspace .
python scripts/check_capabilities.py --report --capability panel-docking .
python scripts/check_capabilities.py --json .             # machine-readable report
```

Filters: `--gaps`, `--regressions`, `--unknown`, `--partial`,
`--deprecated`, `--reconciliation`, `--area AREA`, `--capability ID`.
`--json` emits a structured report for tooling.

Exit codes: `0` = consistent (warnings may still be printed); `1` =
structural errors and/or RECONCILIATION REQUIRED items.

The checker validates: duplicate/malformed capability IDs, allowed status
values, missing required fields, duplicate evidence UIDs, missing evidence
`uid`/`capability_id`/`kind`/`outcome`, invalid kinds/outcomes, malformed
dates, evidence targeting unknown capabilities, dangling capability
evidence references, unreferenced evidence files, missing dependency IDs,
self-dependencies, dependency cycles, malformed aliases/tags/dimensions/
source records, malformed scenario references, duplicate scenario IDs,
invalid `supersedes` references, supersession cycles, and — where
practical — local `locator` existence (remote, conceptual, command, and PR
locators are never failed).

## Reconciliation

When evidence conflicts or current state cannot be derived safely, the
checker prints **RECONCILIATION REQUIRED** and exits `1` — it never
silently guesses. Examples:

- latest PASS and FAIL have ambiguous ordering
- evidence references contradictory current commits
- supersession graph is invalid
- declared status does not match usable evidence
- verification scenario coverage is incomplete but the state says verified

A reconciliation item means a human or agent must look at the evidence and
resolve the conflict explicitly — by appending resolving evidence, by
correcting the declared state with an explicit reason, or by fixing the
schema.

## Backward compatibility

Maps written for the older three-state format (`not_implemented`,
`implemented`, `verified`) keep working:

- old states are a subset of the new vocabulary
- old evidence files (uid/capability_id/kind/outcome/locator/date) remain
  valid; all new fields are optional
- `verified_by` as a string is accepted (legacy pattern) and produces a
  warning instead of an error — the new rule is verification comes from
  evidence
- old maps whose implementation evidence would now support `verified`
  produce a "consider promoting" warning, not an error

No migration is required to upgrade; the warnings tell you what to tighten
when you are ready.

## Project layout

```text
capabilities.yaml                  # declaration + declared state
capabilities/
  evidence/
    EV-001.json                    # one evidence record per file
```

One-evidence-file-per-record stays the default: it is easy to inspect in
git diffs and trivially appendable. Very large projects may later move to
an immutable JSONL ledger or another append-oriented evidence store, but
nothing in the current format requires it.

## Pitfalls

- Declaring `implemented`/`verified` with no usable evidence → checker
  error. Add evidence first.
- A later FAIL with no `regression:` reason → RECONCILIATION REQUIRED.
  Demotions are allowed; silent ones are not.
- Deleting or rewriting old evidence to hide a regression is worse than
  the regression — append FAIL evidence and let the map tell the truth.
- Treating ancient PASS as proof: current state comes from the latest
  active evidence, not the first PASS ever recorded.
- `verified_by` is context, not proof. Verification needs verification-
  level evidence.
- Dependencies are planning info — never auto-promote a capability because
  its dependencies are done.
- Editing state to match a wish instead of evidence: the checker derives
  state from evidence and will not agree.
- `unknown` is not `not_implemented`. No evidence means "not yet
  inspected", not "absent".
- Missing claims: a capability without a claim is a label, and labels do
  not tell you what to verify.

## Verification

- [ ] `python scripts/check_capabilities.py .` exits 0.
- [ ] `python scripts/check_capabilities.py --report .` matches reality:
      gaps, unknowns, regressions, and reconciliation items are all
      expected or resolved.
- [ ] Every capability has a stable kebab-case id and a claim phrased as
      observable behavior.
- [ ] Every `implemented` capability has at least one resolving active
      implementation-level pass evidence.
- [ ] Every `verified` capability has active verification-level pass
      evidence (scenario coverage complete when scenarios are declared).
- [ ] Every demotion carries an explicit `regression:` / `state_change_reason:`.
- [ ] Historical evidence is never edited or deleted; regressions are
      visible as FAIL records.
- [ ] `tests/run_tests.py` passes after checker changes.
- [ ] The map and its evidence are committed with the change they describe.
