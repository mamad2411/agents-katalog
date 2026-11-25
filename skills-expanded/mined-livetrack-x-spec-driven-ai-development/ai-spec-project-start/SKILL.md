---
name: ai-spec-project-start
description: >-
  Install or upgrade SDAD; migrate an existing SDAD project;
  recover or repair `sdad-state.yaml`, INDEX, ledger, or handoff consistency;
  run or interpret SDAD Doctor;
  or diagnose the SDAD control plane. Use only for SDAD-specific bootstrap,
  migration, repair, and Doctor operations.
---

# AI-SPEC Project Start

Create the smallest SDAD control plane that lets an owner direct AI work,
separate evidence from confidence, and keep future sessions recoverable.

## Reference Routing

Read references only when their trigger applies:

- Read [references/runtime-contract.md](references/runtime-contract.md) before
  creating or changing an SDAD control surface. It owns steady-state v2 scale,
  execution scope, owner gates, targeted routes, evidence, and stop semantics.
- Read [references/starter-templates.md](references/starter-templates.md) when
  bootstrapping or repairing Standard/Full control files.
- Read [references/field-patterns.md](references/field-patterns.md) when
  translating lessons from another project, release/migration practice, or a
  reference implementation.
- Read [references/implicit-rules.md](references/implicit-rules.md) when creating
  or repairing Core 5/control rules, or when repeated confusion or failure
  should become a rule, playbook, test, validator, or template.

Do not load every reference by default.

## Workflow

### 1. Inspect Capability And Existing State

Determine whether the environment can edit the project filesystem.

Use this skill as a one-time bootstrap, install, upgrade, migration, repair, or
diagnosis entry point, not a per-session prompt. After setup, ordinary sessions
start with the installed repository adapter, then `sdad-state.yaml`, then
`docs/INDEX.md`; they invoke this skill again only for an SDAD-specific
operation named by the frontmatter trigger.

- In chat-only environments, plan and explain only. Do not install files or
  claim they were saved.
- In file-editing environments, inspect repository instructions, current files,
  version control state, source/tests, and existing SDAD surfaces before
  proposing changes.
- Preserve unrelated owner changes. Do not replace an existing control system
  merely because SDAD was requested.
- Treat review/audit requests as read-only unless the request also authorizes a
  change.

If the repository already has SDAD, start from its current adapter,
`sdad-state.yaml`, and `docs/INDEX.md`. Repair drift rather than rebuilding
from scratch.

This skill is not the default route for ordinary bug fixes, reviews, refactors,
documentation, implementation, generic release work, or handoff creation.

### 2. Interpret The Request

Inspect the request and repository first. Infer the goal, scale, work boundary,
validation claim, owner gates, and handoff trigger from available evidence. The
old five kickoff questions may be used internally, but they are not a required
owner questionnaire.

Report the result compactly:

```text
Interpreted goal:
Scale:
Work boundary:
Validation contract:
Owner gates:
Handoff trigger:
Reason:
Unresolved question: none
```

This is not another approval step. Proceed when the interpretation matches the
owner's intent and no gate blocks action; the owner may override it. Ask at most one unresolved blocking question only when the answer changes scale, execution scope, protected action or owner gate, claim boundary, or authority. Include a
recommended default and explain what the answer changes.

### 3. Select Scale

Use these defaults unless repository evidence requires a different scale:

- One-shot -> current request only.
- Mini -> unit.
- Standard -> packet.
- Full -> packet plus named owner gates.

Select Standard when multiple workers are involved, persistent state is needed,
or the packet only inspects, documents, or tests a protected area. Select Full
when the packet changes, accepts, or executes a protected action, or when named
owner gates are otherwise active. One-shot creates no persistent files. Mini
uses one instruction file and does not imply state v2.

### 4. Existing-Project Read-Only Migration Preview

For an existing project, produce a read-only migration preview before any SDAD
control-file write. Report exactly these items in order:

1. worktree status, owner changes, control files, sizes, and authority, including dirty or untracked owner material
2. pre-change Doctor result or read-only structural baseline
3. One-shot/Mini/stateful-Mini/v1 Standard-Full/mature-pre-v3 classification
4. active records versus history/archive candidates
5. exact history-preservation strategy
6. umbrella objective versus first executable leaf packet
7. each proposed validation command and bounded proves claim
8. immediately selectable routes and targeted-read strategy
9. current handoff existence and authority
10. owner-controlled decisions and evidence gates
11. active SPEC entrypoint, competing/additional SPECs, and proposed lineage
    reconciliation
12. proposed state, INDEX, ledger, and handoff writes without applying them
13. post-change Doctor strict and separate project-validation comparison plan

Route One-shot or stateless Mini away from v2 migration; a deliberately stateful Mini remains on v1. New Standard/Full bootstrap and eligible existing
Standard/Full migration use v2. Inventory v1 intensity, autonomy, save-state, and work-packet-state as legacy inputs and map authorization as follows:

- Level 0 -> no execution authorization.
- Level 1 -> unit.
- Level 2 -> packet.
- Level 3 -> explicit owner-approved packet list, not session scope.
- Level 4 -> scope selected separately plus named owner gates.

V2 uses `execution_scope: unit | packet`; v2 has no intensity or autonomy keys.
Set `validation_for` to the active packet before changing the version. Preserve
valid conditional owner authorization and reuse it only while packet, action,
conditions, expiry, evidence, and source/artifact identity remain unchanged. Re-approval
is required when any of those terms changes or the authorization expires.

Link or move legacy save-state content into a current handoff or an archive
without automatic deletion. Keep `docs/work-packet-state.md` as the legacy path
for the optional Delivery Readiness Model; it is not current packet authority.

For stateful work, normalize `active_spec` as the single normative SPEC
entrypoint. `SPEC-COMPLETE.md` is an integrated baseline, not an immutable or
automatically active document. Treat a SPEC supplied as current requirements as
a change request unless the owner limits it to review/draft/reference; hold affected work and compare
its acceptance boundary before classification. A merely discovered SPEC gains
no authority from metadata and remains a proposal only when nonconflicting.
Record the accepted amendment, bounded supplement, or replacement with its
baseline, effective packet, revision, and exact superseded scope before work.
Reject lineage cycles and implicit overlap. A material post-acceptance change
starts a new, never-reused packet ID and fresh validation.

Before replacing terminal state, require one durable owner-decision record that
pins the packet, active SPEC revision, source/artifact identity, evidence/claim
limits, residual risk, and decision. Later corrections or revocations append a
unique revising/superseding record and update affected current-claim pointers.

Show all proposed writes without applying them. Existing adoption authority
permits continuing after the preview unless scope, authority, data boundary,
protected action, or an owner gate requires a real decision. Ensure the proposed
INDEX, ledger, validation, routes, and handoff are coherent, then change state `version: 2` last. Compare post-change Doctor strict structural evidence and
project validation separately; Doctor never proves project correctness.

Only after that boundary, apply the proposed control-file changes. Preserve
project history and unrelated owner work.

### 5. Select Tool And Install One Adapter

Identify Codex, Claude Code, Cursor, Copilot Chat, or Generic. If ambiguous, ask
which file-editing tool is active. Claude Code means the local coding tool, not
Claude.ai browser chat.

For a source checkout, prefer the repository's installer. For no-clone setup:

1. Read the canonical `install-sources.json`.
2. Read the matching route in `docs/no-clone-quick-install.md`.
3. Use the exact revision, path, target, and SHA-256 from the manifest.
4. Show the source and hash result before saving.
5. Fail closed on fetch or hash mismatch.
6. Offer retry, pasted source, terminal installer, or manual clone/download;
   never invent an adapter from memory.

Install exactly one active adapter. One-shot installs none. Mini installs only
the matching Mini instruction file. Standard/Full installs the matching
full adapter before creating project control files.

Do not overwrite an existing file without showing the proposed difference.
Use force/replace only with owner authorization and preserve rollback behavior.

### 6. Bootstrap The Progressive Control Plane

For Standard or Full, create the files defined by
[references/starter-templates.md](references/starter-templates.md). The fixed
startup path is:

1. tool adapter;
2. `sdad-state.yaml`;
3. `docs/INDEX.md`;
4. current source/tests/runtime state;
5. only documents or policy/playbook headings routed for the active packet.

Do not make the full rulebook, archives, old handoffs, or optional evidence
files mandatory startup reads.

Keep roles singular:

- adapter: always-loaded safety and execution kernel;
- `sdad-state.yaml`: current scale, execution scope, packet, gates, validation,
  validation identity, and routed docs;
- `docs/INDEX.md`: trigger-to-file routing only;
- operating rules: durable policy loaded by heading;
- playbooks: procedures loaded on demand;
- SPEC/TODO/findings/notes: current authoritative work state;
- current handoff: optional continuity only;
- evidence/claim files: created only for an active claim.

If required files already exist, inspect and merge. Do not silently replace
project-specific paths, commands, decisions, or constraints.

### 7. Normalize And Bind The Work Packet

Normalize natural-language work into this internal packet envelope:

```text
Outcome / objective
Authority / reference
Constraints / allowed scope
Validation contract
Evidence required and claim limit
Stop condition / owner gates
Required report
```

Choose the first executable leaf packet under any broader objective. Each
delegated worker receives packet ID, objective, allowed scope, routes/files, validation, gates, stop condition, and required report because parent context is not assumed.

Write current routing values to `sdad-state.yaml`. Keep `routed_docs` limited
to eligible files that can affect the packet; current intent selects the path,
heading, active section, or targeted match actually read. Bind `validation_for`
to the active packet. Use current source and tests before implementing a plan.

### 8. Set Execution Scope And Owner Gates

Use `unit` for the current bounded unit or `packet` for the approved packet.
Multi-packet work requires an explicitly approved packet list. Scope does not
grant permission for release, migration, destructive action, sensitive data,
auth, money, security, rollback, production, or any other protected action;
keep those as named owner gates.

Proceed through review-worthy units without micro-approval. Stop only for the
conditions in the runtime contract.

### 9. Execute Or Route

For review-only work, return prioritized findings with file/line evidence,
impact, and validation limits.

For implementation, use a failing test or check first when the behavior is
testable, make the smallest coherent change, run focused checks, then run the
full relevant validation surface. Keep docs and current control state aligned.

For reference-derived work, create a source behavior to implemented behavior to
evidence map and label gaps. For product/hardware/package/remote/release claims,
use the optional evidence files named by the active route.

Record spec-unstated durable implementation judgments in
`docs/implementation-notes.md`. Use an ADR only for a hard-to-reverse,
surprising tradeoff. Do not record raw internal reasoning.

### 10. Finish At The Right Boundary

Call work evidence-ready only when scoped implementation, relevant checks, docs,
and residual risk are shown. Keep owner-accepted, hardware-verified,
release-candidate, and production-ready states separate.

Return a compact checkpoint:

- scale, execution scope, owner gates, and packet;
- changed files and behavior;
- checks run and what they prove;
- docs/control state changed or checked;
- open findings and unverified behavior;
- remaining risk and owner decisions;
- acceptance state and next step.

Create or update `current_handoff` only when another session, tool, person, or
machine needs actual continuity and reconstruction would be costly. Reconcile
direction first; a stop, redirect, block, or partial result alone does not
require a handoff. Link authorities instead of copying their contents.

## Existing-Project Rules

- Do not force SDAD onto a project that is better served by One-shot or Mini.
- Do not create optional files without an active job.
- Do not treat archived plans, product notes, external references, handoffs, or
  chat memory as current implementation authority.
- Do not treat a second SPEC, filename, date, or document order as authority
  without explicit active-SPEC incorporation or a packet pointer switch.
- Do not let a lower evidence tier support a stronger claim.
- Do not use broader execution scope to bypass owner gates.
- Do not assume commit authorizes push, release, deployment, migration, or an
  external message.
- Do not hide partial, degraded, skipped, simulated, or unverified behavior.
- Do not claim completion while current control state is stale.

## Sensitive Data Boundary

Sensitive data is an authorization boundary, not a size threshold. Use
metadata-only inspection by default. Do not read or expose credentials, keys,
tokens, cookies, `.env` contents, raw customer records, or private corpora
unless the task requires it and owner policy plus tool policy permit it. Stop
before reading when authorization is unclear.

## Guardrails

- Use evidence before questions; ask only the next blocking owner question.
- Use bounded reads for large or broad inputs.
- Prefer reversible local changes and preserve dirty working trees.
- Keep adapters self-contained; do not introduce runtime includes that their
  host tool will not load.
- Keep no-clone sources commit-pinned and hash-verified.
- Keep the fixed startup control plane inside repository line/character budgets.
- Validate links, templates, skill metadata, installers, and tests before
  declaring the bootstrap evidence-ready.
