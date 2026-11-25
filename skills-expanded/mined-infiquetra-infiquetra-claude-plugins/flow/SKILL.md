---
name: flow
description: |
  Operator-facing GraphQL + REST helpers for the active project boards. Wraps
  the GitHub APIs the orchestrator uses, so Jeff can do per-card work
  (set Initiative/Objective fields, link or unlink sub-issues, validate card bodies,
  self-heal labels, open or close repair windows, discover project mappings, assign covered issues to Team Mimir) without writing GraphQL by
  hand. Each command is idempotent where possible, and surfaces partial
  failures clearly.
when_to_use: |
  Use this skill when the user wants to:

  Set Initiative or Objective on a card (project FIELDS, not labels):
  - "Set Initiative on this card to platform-quality"
  - "Mark this issue as part of the Auth MVP Objective"
  - "Update the Objective field on campps-mvp#42"

  Discover what fields/options exist on a project (live, not cached):
  - "What Initiative options exist?"
  - "List the Objective field options"
  - "What can I set Initiative to?"

  Find which project a repo belongs to:
  - "Which project does athena-service map to?"
  - "Where do I add cards from this repo?"

  Assign an issue to Team Mimir intake:
  - "Assign this issue to Mimir"
  - "Send infiquetra/mimir-pilot-claude-plugins#42 through Mimir intake"

  Link a child issue as a sub-issue of a parent:
  - "Link #43 as a sub-issue of #42"
  - "Make this a child of campps-context-library#1"
  - "Set up the parent/child relationship between these issues"

  Remove an accidental or retired parent layer:
  - "Unlink #43 from #42"
  - "Make this capability top-level again"
  - "Remove the redundant outcome parent without closing either issue"

  Self-heal missing labels (so other operations don't fail mid-flow):
  - "Make sure the high-priority label exists on campps-mvp"
  - "Verify the type labels are on this repo's label set"
  - "Create the capability label if it's missing"

  Open or close a repair window (a card's own verification failed):
  - "Open a repair window on #42 — here's the failing test run"
  - "Close the repair window on campps-mvp#42; the fix passed every scenario"
  - "Record that this card's own verification failed, with the citation"

  Pre-flight an issue body against the card_validator schema:
  - "Validate the card body for #42"
  - "Will this issue pass plan-review?"
  - "Check if my issue body matches the card_validator contract"

  Don't use this skill for:
  - Creating issues (use `issues:create`)
  - Moving cards between Status columns (use `board:move`)
  - General board health (use `board:view`)

  These are *helpers*, not full workflows. The full issue-creation and optional-parent
  card-creation workflow is in `infiquetra-sdlc/docs/workflows/blueprint-to-issue.md`;
  this skill provides the building blocks the workflow uses.
---

# flow

Operator-facing helpers over the GraphQL + REST APIs the active boards use.
Each command is a thin wrapper with idempotency + clear error messages.

## Commands

```bash
# Set a single-select project field on a card
sdlc_manager.py flow set-field \
  --project campps --repo campps-mvp --number 42 \
  --field Initiative --option platform-quality

# Lifecycle fields (Status, Stage) write EVERY board carrying the issue —
# all-or-none. --project is validated as a carrying board, not honored as a
# single-board restriction, and --reason (optional) is recorded per board.
sdlc_manager.py flow set-field \
  --project operations --repo infiquetra-sdlc --number 42 \
  --field Status --option Implementing --reason "failed verify, returning to active"

# Set the same single-select field on multiple cards in one discovery pass
sdlc_manager.py flow set-field \
  --project operations --repo infiquetra-claude-plugins --numbers 101,102,103 \
  --field Status --option Capturing

# Set multiple fields on multiple cards in one discovery pass
sdlc_manager.py flow set-field \
  --project operations --repo infiquetra-claude-plugins --numbers 101,102,103 \
  --field Status --option Capturing \
  --field Objective --option defects-claude-plugins

# List the options on a project field (live discovery — IDs rotate)
sdlc_manager.py flow field-options \
  --project campps --field Objective

# Resolve which project a repo maps to
sdlc_manager.py flow discover-project --repo athena-service

# Apply the live-covered repository's existing Mimir intake trigger
sdlc_manager.py flow assign-mimir \
  --repo mimir-pilot-claude-plugins --number 42

# Link child as native sub-issue of parent (cross-repo OK; idempotent)
sdlc_manager.py flow link-sub-issue \
  --parent-repo campps-context-library --parent-number 1 \
  --child-repo campps-mvp --child-number 42

# Remove only the native relationship (cross-repo OK; idempotent)
sdlc_manager.py flow unlink-sub-issue \
  --parent-repo campps-context-library --parent-number 1 \
  --child-repo campps-mvp --child-number 42

# Self-healing label: 404 → create; exists → no-op; other errors raise
sdlc_manager.py flow verify-label \
  --repo campps-mvp --name high-priority \
  --color D93F0B --description "High priority"

# Pre-flight a card body against the card_validator schema
sdlc_manager.py flow validate-card --repo campps-mvp --number 42

# Open a repair window: adds the schema-declared `repair-window` label and
# posts the FAILING result as the citation. --citation is required and must
# be non-blank. Idempotent: a card already carrying the label is a no-op.
sdlc_manager.py flow repair-window \
  --repo campps-mvp --number 42 \
  --action open \
  --citation "uv run pytest tests/test_x.py::test_y -q → 1 failed"

# Close a repair window: removes the label and posts the PASSING result.
# Close only when a later deployed version passes every prescribed scenario.
sdlc_manager.py flow repair-window \
  --repo campps-mvp --number 42 \
  --action close \
  --citation "uv run pytest tests/test_x.py::test_y -q → 1 passed"
```

## Idempotency contract (per command)

| Command | Idempotent? | Failure behavior |
|---|---|---|
| `set-field` | yes (same option = same final state) | Raises if an option doesn't exist; error message lists current options. With `--numbers` and repeated `--field/--option` pairs, reports every updated/failed issue-field update and exits non-zero after reporting if any item fails. For `Status`/`Stage` (W6): the write is atomic across every board carrying the issue — preflight failures write nothing; a failed write is compensated; a failed COMPENSATION halts with a named divergence (exit non-zero, no retry). Per-issue atomicity for `--numbers`. |
| `field-options` | read-only | Raises if project or field doesn't exist |
| `discover-project` | read-only | Returns "not mapped" or "excluded" without erroring |
| `assign-mimir` | yes (existing trigger label = no mutation) | Reads live Team Mimir coverage, open-issue state, current principal authority, and the existing trigger label before mutation; verifies label and Objective state after mutation. Unsupported, closed, unauthorized, missing-label, or unreadable cases fail closed. |
| `link-sub-issue` | yes (re-POST returns 422 "already exists" → success) | Raises on non-422 errors; rejects PR-as-parent |
| `unlink-sub-issue` | yes (verified issues + absent relationship returns 404 -> success) | Verifies both issues first; rejects PR-as-parent; propagates auth/rate-limit/server errors |
| `verify-label` | yes (no-op if exists; create if 404) | Raises on auth/rate-limit/server errors (NOT silently treated as missing) |
| `validate-card` | read-only | Exits non-zero if card body fails validation |
| `repair-window` | yes (open: label already present = no mutation, no second comment; close: label absent = no mutation, no second comment) | Refuses BEFORE any network call when `--citation` is missing/blank, or when the vendored schema does not declare a `marker_kind: label` repair-window marker, or when the marker's declared `marker_source` labels config does not define it. Never writes a project field. |

## Hard rules

- **Objective is a project field plus scorecard, not an issue type or parent requirement.** Never apply a plain `objective` type label or `objective:*` / `initiative:*` colon-prefixed labels. Use `flow set-field` instead.
- **Field option IDs rotate on rename/recreate.** Never cache them. Every command that reads field state calls `flow field-options` (or its equivalent GraphQL query) at start.
- **Verify-label distinguishes 404 from other errors.** A 401/403/5xx must NOT be silently treated as missing — that would create labels under the wrong auth context or mask real failures.
- **Link only real decomposition.** Capabilities are top-level by default and grouped by the `Objective` field. Both sub-issue commands require an issue parent; PRs are rejected.
- **Assign-Mimir never creates policy.** It does not admit repositories, create `intake:mimir`, use alternate credentials, or comment. Team Mimir's live exact-repository coverage and the repository-owned label must already exist.
- **A repair window is a cited label, never a project field.** The encoding (the `repair-window` label and its definition source) is read from the schema's `repair_window_encoding` block — an outdated schema is a refusal, not a guess. Every transition cites the test result verbatim (failing on open, passing on close).

## Where this fits in the broader workflow

The Phase A carry-over #2 decision (Initiative + Objective as project
fields) made `flow set-field` the canonical mechanism for hierarchy
assignment. The blueprint-to-issue workflow calls into:

- `flow link-sub-issue` / `flow unlink-sub-issue` (optional decomposition relationship)
- `flow set-field` (Initiative + Objective + Status fields)

`validate-card` is the pre-flight check before plan-review fires. If a card
body doesn't pass `validate-card`, the orchestrator will reject it on the
`Ready for Planning` → `Designing` transition; running this command before
pushing the card to `Ready for Planning` saves a round-trip.

## Authoritative source

The card_validator schema is mirrored from
`home-lab/ansible/roles/hermes_orchestrator/files/card_validator.py`. When
that file's contract changes, update `validate_card_body` in
`scripts/sdlc_manager.py` to match.

## Related

- `issues` — issue creation flows with Objective assignment and optional parent linkage
- `board` — Status column moves + board view
- `labels` — bulk label deploy (this skill's `verify-label` is the per-call self-heal)
- `milestones` — per-repo milestone management (Objective tracking is now project-field-based; milestones are an optional secondary mechanism)
- `infiquetra-sdlc/docs/engineering-journal/DECISIONS.md` — Initiative/Objective decision (2026-05-03)
- `infiquetra-sdlc/docs/workflows/blueprint-to-issue.md` — full 8-step issue-creation playbook
