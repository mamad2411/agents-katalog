# AGENTS.md - pi runtime intent layer

This file is auto-loaded by pi-CLI when an agent operates inside the
`.pi/` tree. It is the pi equivalent of `CLAUDE.md` for Claude Code,
deliberately kept separate because pi runs a different runtime, does
NOT inherit Claude Code's MCP configuration, and ships its own extension
set under `.pi/extensions/`.

If you are running under Claude Code, prefer `.claude/commands/task/`
and the workspace-level `CLAUDE.md` files - they auto-load there.

## WHY this surface exists

The `.pi/` tree mirrors `.claude/commands/task/` so a single lok task
can move freely between the two runtimes mid-lifecycle without losing
state. Both sides read and write the same workflow YAML at
`docs/status/clo-XX-workflow.yaml`, advance through the same phase set,
and reach the same Linear ticket via the same approved MCP tool subset.

The two sides are kept in sync by hand. Schema drift between
`extensions/orchestrate/index.ts` (`PHASE_CONFIG`,
`ALLOWED_TRANSITIONS`, `TYPE_ALLOWED_PHASES`) and the phase markdown is
the failure mode this layer exists to prevent.

## INTENT - non-negotiable invariants

These bind every phase script and every extension that mutates state.
If a change to the code or to a phase file would break one of these,
stop and reconcile both sides before landing.

1. **Workflow YAML is the single source of truth.** Every state mutation
   goes through `update_workflow_state` / `transition_phase`. No phase
   script writes to `docs/status/clo-XX-workflow.yaml` directly. No
   reviewer report, comment, or PR is allowed to imply state that the
   YAML does not record.

2. **The state machine enforces gate ordering.** `transition_phase`
   rejects a move when the outgoing phase lacks its required fields or
   history events. Bypassing it with `validation_override: true` is a
   last resort and must be justified in `details`. Phase scripts must
   NOT set `status: complete` until their phase's exit-state checklist
   passes - in particular `implement` stays at `status: validating`
   until the codex+synthesis gate produces a clean verdict.

3. **Schema parity between code and docs.** Any change to required
   fields, allowed transitions, allowed task-type x phase combinations,
   or required history events MUST land in both places in the same
   commit:
   - `.pi/extensions/orchestrate/index.ts` (`PHASE_CONFIG` etc.)
   - the relevant `.pi/orchestrator/phases/*.md` "Required exit state"
     and "History events required" sections
   - the `.claude/commands/task/phases/*.md` mirror, for any phase file
     that declares a "Required exit state" section
   Verify with `node .pi/scripts/check-schema-parity.mjs` before
   committing. Drift means the runtime gates one set of fields while
   the docs describe another - a silent failure mode. Fields documented
   in YAML but not gated by `PHASE_CONFIG` must be annotated with
   `# optional` inline so the parity checker treats them as
   intentionally informational. The Claude mirror is checked only where
   it declares an exit state; `--verbose` lists the phases still
   outside the gate, and bringing one under it is just adding the
   section.

4. **MCP least-privilege.** Linear access is the approved 7-tool subset
   (`list_issues`, `get_issue`, `save_issue`, `list_comments`,
   `save_comment`, `list_issue_statuses`, `list_projects`, plus
   `get_team` conditionally) per `docs/guides/linear-mcp-adapter.md`.
   `LINEAR_MCP_FULL_SURFACE=1` is an escape hatch, not a default. Do
   not add tools to the bridge without updating the adapter doc first.

5. **Auto Mode is the default, but auto-approval is logged.** Each
   phase file names the preconditions that allow auto-approval. When
   pi auto-approves, it records the reason in
   `phases.<phase>.auto_approval_reason`. Silent auto-approval is a
   regression.

6. **Confidentiality.** Never paste Linear ticket bodies, PII, customer
   data, or repository content of another tenant into review files,
   commit messages, or comments. Reference paths and ticket IDs only.

7. **Cross-task memory flows through `.pi/lessons/`.** Durable rules
   surfaced at task completion are written there, not into per-task
   workflow YAMLs that future tasks will not read. The contract:
   - `complete.md` § "Step 4.5 - Extract lessons" surveys the
     workflow YAML for violated assumptions, validation-gate fix
     iterations, flagged suggestions, plannotator annotations, and PR
     incidents. It writes a new `L<n>` block either into an existing
     topic file (e.g. `pr-review-failures.md`) or a per-task file at
     `.pi/lessons/clo-XX-<slug>-lessons.md`.
   - **There are two lesson stores and both are live.** `.pi/lessons/`
     holds topic files written by the complete phase; `docs/lessons/`
     holds per-lesson files written by `/session:wrap` (CLO-625 put
     seven there). A consult that greps one store silently drops half
     the corpus.
   - Future tasks consult both BEFORE drafting: `design.md` Step 0
     (before generating the draft) and `implement.md` Step 0 (before
     slicing work) `grep -rl <keyword> .pi/lessons/ docs/lessons/` for
     keywords relevant to the touched modules / subsystems (e.g.
     `backend`, `workflow`, `conductor`, `tasks`, `apply_verify`) and
     cite hits in the design assumption list or the implementation plan.
   - Lessons are append-only. Existing entries are not edited - a
     superseding incident produces a new `L<n>` that cross-references
     the old one.
   - Phase scripts cite `.pi/lessons/<file>.md § L<n>` rather than
     restating the rationale inline. Lessons are the rationale store;
     phase scripts are procedure.

## HOW - where to look

| Need | Open |
|---|---|
| State machine source of truth (transitions, required fields, history) | `extensions/orchestrate/index.ts` |
| Linear MCP bridge (transport, filtering, tool prefix) | `extensions/linear/index.ts` |
| Phase procedures (dispatch order, exit-state checklists) | `orchestrator/phases/*.md` |
| Reviewer personas (verdict format, scoring axes) | `agents/*.md` |
| Durable lessons from past incidents (cited by phase scripts) | `lessons/*.md` |
| Layout, schema reference, extension behavior, install steps | `IMPLEMENTATION_SUMMARY.md` |
| Phase-script index and conventions | `orchestrator/README.md` |

The validation gate inside `implement.md` step 4 is the lok equivalent
of a separate `review` phase. It runs the `pre-pr-validation` workflow
(`.lok/workflows/pre-pr-validation.toml`) and synthesizes the codex
report (or the Claude fallback's, when Codex fails). There is no
standalone review phase here.

The canonical assets under `.lok/` (`lok.toml`, `workflows/`, `prompts/`)
are project-tracked, not local-only. A worktree created for a feature
branch must inherit them so the implement validation gate can run there
without manual `cp` rescue. Per-user overrides go under `.lok/local/`,
which `.gitignore` excludes.

## Maintenance rules

- Any required-field / history change mirrors into `PHASE_CONFIG` in
  `extensions/orchestrate/index.ts` AND the relevant phase file's
  "Required exit state" / "History events required" sections in the
  same commit. Verify symmetry with:
  ```
  node .pi/scripts/check-schema-parity.mjs
  ```
  Exit 0 means the runtime gate and the docs agree on required fields
  and history events. Exit 1 lists the drift per phase. Add `# optional`
  inline in the YAML for fields that are documented but not gated.
- Any YAML-schema change reflects in the relevant phase file's
  "Required exit state" section AND in `extensions/orchestrate/README.md`.
- A new durable lesson from an incident lands in `.pi/lessons/` and is
  cited from the relevant phase script - do not inline incident
  narrative into phase scripts.
