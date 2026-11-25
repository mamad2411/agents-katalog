---
name: knowledge-processor
description: >
  Reconcile useful new information with scoped knowledge and retrieve relevant
  context before dependent work. Shared continuity infrastructure for all work;
  no software workflow or user repository is required for project knowledge.
  Use when new information is worth keeping or prior context is needed before
  dependent work; NOT for a larger research artifact (use knowledge_capture).
status: active
relevant_for: ["solution-expert"]
invocation:
  primary: cross-cutting
  secondary: [workflow-step:close, user-facing]
disable-model-invocation: false
modes: [process, wrap-up, user-signal]
uses: []
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Knowledge Processor

**Ground rule:** Preserve knowledge about the subject and what is needed to continue
open work. Do not turn the conversation or work process into a factual chronicle.
Admission details: [continuous-maintenance.md §Admission](continuous-maintenance.md#admission).

Canonical semantic lifecycle for knowledge and continuity. Modes specialize this
contract; boot, save and housekeeping invoke it. No database, hook, background
worker, automatic import or development engine is implied.

## Inputs and scope

Input: candidate information or retrieval need, active project, configured user
scope if any, and mode `process`, `user-signal` or `wrap-up`. Resolve location and
permissions through `framework/user-scope.md`. Project knowledge belongs to its
verified project/topic owner; private person facts only to the resolved
`<user_repo>/context/user/`. No user scope: project continuity still works; report
unroutable person facts, never create a profile or private fallback in the project.
A visiting agent retains its own user identity and follows the visited project's
entry and authorization rules without adopting another person's profile.

## Continuous maintenance

When a user scope is configured or the project's rules require ongoing knowledge maintenance: read and follow
`skills/knowledge_processor/continuous-maintenance.md` at boot and after compaction (authority, same-cycle
reconciliation, checkpoint before a topic switch, update-not-append, the FACTS line, blocked writes).

## Executable lifecycle

### 1. Retrieve and establish a coherent baseline

Before an answer, update or dependent continuation that needs stored context: read and follow
`skills/knowledge_processor/retrieve.md` (verified owner and baseline, bounded search and its stop, using what was
retrieved).

### 2.–5. Admit, place, validate and publish

Before admitting, writing, correcting, moving or removing a claim: read and follow
`skills/knowledge_processor/write.md` (§2 admit, scope and compare; §3 place and curate; §4 validity and provenance;
§5 bounded impact and protected publication).

### 6. History, imports and maintenance

When writing history or the handoff, importing sources, or restructuring (splitting, merging or renaming) owners:
read and follow `skills/knowledge_processor/history-imports.md`.

## Modes and outcome

- `process`: `modes/process.md` — project facts/impact; routes person facts separately.
- `user-signal`: `modes/user-signal.md` — personal placement under the shared lifecycle.
- `wrap-up`: `modes/wrap-up.md` — common continuity/history, selected domain contribution.

DONE: admitted deltas reconciled at authorized owners, routes/current views coherent,
pending operation clear, and actual outcome verified. No-change PRESENT is success.
FAIL: report unavailable scope, evidence, coherent snapshot or pending recovery;
retain recoverable work in its scope, never claim completion on partial persistence.
Close-phase retros supply their Patterns-Emerged as process input; do not re-extract
raw sessions. Selected development closeout audit obligations remain domain-owned.

Incident handling: collect observations and locate/assess impact; defer transient
current-state replacement until the incident's recovery/fix boundary. Preserve
necessary incident checkpoints and approvals under local incident rules. Afterwards
reconcile observed end state and relevant failed attempts. No live action is
implicitly authorized by knowledge maintenance.
