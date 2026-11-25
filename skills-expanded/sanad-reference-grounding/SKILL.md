---
name: sanad-reference-grounding
description: Create, refresh, consume, and audit pinned external reference evidence for Sanad plans and implementation tasks while keeping tracked project knowledge clean and source-neutral. Use when planning or implementing a task that benefits from reference projects, when a task declares reference_grounding or evidence_id, when evidence is missing or stale, when reference repositories must be discovered or downloaded, and when producing an Adopt/Adapt/Reject or reference-parity record.
---

# Ground Sanad Work in External Evidence

Use one completion-oriented workflow for both evidence authoring and implementation. Publicly
acknowledge that Sanad learns from external reference projects while keeping source-specific
navigation details in the ignored local evidence store.

## Choose the mode

- **Author or refresh:** Use when planning a new reference-informed task, when no packet exists,
  or when a source revision changed.
- **Consume:** Use when implementing or reviewing a task with a current packet.
- **Audit:** Use after implementation to compare the result with adopted and adapted obligations.

Read [references/evidence-packet-authoring.md](references/evidence-packet-authoring.md) completely
before authoring, refreshing, discovering, or downloading sources.

## Resolve before implementation

1. Run `scripts/resolve_packet.sh <task-id>` from the primary checkout or a linked worktree.
2. Follow the returned status:
   - `ready`: read the packet completely and continue in Consume mode.
   - `authoring_required`: enter Author mode and create the missing store data or packet.
   - `refresh_required`: enter Refresh mode and reconcile the changed source.
   - `source_unavailable`: exhaust catalog, public discovery, and authorized access options before blocking.
3. Read the governing `AGENTS.md` and license for each selected source tree.
4. Read any `navigation_aid` paths returned by the resolver when they accelerate discovery.
   Treat them as optional maps, not evidence authority.
5. Inspect every mandatory source file, symbol, and test in the packet. Reports are navigation
   aids only; source and tests are authoritative.
6. If a source working tree is dirty, determine whether the changed files overlap mandatory
   evidence. Do not treat unrelated dirt as a blocker and do not overwrite user changes.

Do not stop merely because a packet, catalog entry, or local clone is absent. Build or repair the
recoverable evidence first, rerun the resolver, then continue implementation.

## Produce the local grounding record

Create a run record under the resolver-provided `run_records` directory. Include:

- task ID and packet fingerprint;
- verified source revisions;
- exact files, symbols, and tests inspected;
- an `Adopt / Adapt / Reject` matrix;
- source-neutral invariants and test obligations;
- unresolved contradictions or missing evidence.

## Maintain tracked knowledge hygiene

Sanad may state publicly that it uses external reference projects. Keep tracked files focused on
Sanad rather than filling them with another project's navigation details.

- Track source-neutral behavior, ownership, state machines, security boundaries, decisions, and tests.
- Keep specific reference-project names, repository and file paths, class/function/symbol names,
  commit hashes, raw audits, and comparison matrices in the ignored evidence store.
- Use only an opaque evidence ID and packet fingerprint when tracked progress needs traceability.
- Preserve legally required license notices and attribution in tracked files when code is copied
  or adapted; this legal obligation is an explicit exception to the source-detail boundary.
- Reject patterns that conflict with Sanad's accepted design instead of importing them because
  they exist in a reference.

## Audit after implementation

Reopen the run record and compare finished behavior and focused tests with every adopted or
adapted obligation. Mark each item `satisfied`, `deviated`, or `not applicable`, with a
source-neutral explanation. Return deviations to the task design before completion.

Block Gate R0 only after recoverable authoring, refresh, discovery, and download paths have been
exhausted and a concrete unresolved reason remains.
