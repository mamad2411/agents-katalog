---
name: story-intake
description: >-
  Normalize a single starting input — free-form text, an external ticket id or URL, a local
  story path, a local work-item path, or a greenfield idea — into one canonical requirements.md
  that every later pipeline phase reads, and guarantee a work-item reference exists before those
  requirements are written. Invoked automatically by sdlc-engine at Phase 1; also triggers on
  direct asks like "normalize these requirements", "turn this into requirements", or "write
  requirements from this ticket". Not for: planning, estimating,
  scaffolding, or implementing — it only normalizes and clarifies input into
  requirements.md.
---

# story-intake

Turn exactly one starting input into a single canonical `requirements.md`, and make sure a
resolvable work-item reference is on file before that document is written.

> This is the mouth of the pipeline. Everything downstream (design, planning, complexity, QA,
> implementation) reads the `requirements.md` you produce and assumes a work item already exists.
> Get the normalization right and stay inside the output contract — no phase artifacts leak from
> here.

When this intake belongs to a managed runtime run, lifecycle and work-item
decisions remain in SQLite. Use the runtime authority reference at
`../../references/runtime-authority.md`; `requirements.md` and work-item ledgers
are human-facing artifacts or compatibility views and never advance the run by
direct append alone; refresh compatibility ledgers with `legacy.export`.

## When to run

- **Automatic**: `sdlc-engine` calls this at Phase 1. Human-in-the-loop runs enter through
  `sdlc-guided`; autonomous runs enter through `sdlc-auto`.
- **Direct**: a user asks you to normalize a blob of requirements, convert a ticket into
  requirements, or spec out a greenfield idea.

Do not hand-call this for anything past normalization. Planning, estimation, design, and
implementation belong to later phases.

## Inputs

| Input | Meaning |
|---|---|
| `raw_input` | The single starting artifact: text, ticket id/URL, story path, or local work-item path. |
| `mode_flag` | `--greenfield` marks the input as a net-new idea with no source ticket. |
| `run_dir` | The current run directory. All run-scoped writes land under here. |

## Detection order (first match wins)

Classify `raw_input` in this exact order and stop at the first funnel that matches:

1. `--greenfield` flag present → **greenfield funnel**.
2. Path matching the local story glob (`docs/stories/*.md`) → **story-file funnel**.
3. Path matching the local work-item glob (`docs/superpowers/work-items/`) → **local work-item funnel**.
4. Looks like an external ticket id or URL → **ticket-adapter funnel**.
5. Otherwise → **free-form funnel**.

## Work-item resolution

A work-item reference **must** resolve before `requirements.md` is written. Select the source per
funnel:

| Situation | Work-item source |
|---|---|
| Existing local work item | Use its path. |
| Story file | Prefer the story's `**Work Item**` field; else create/update one under `docs/superpowers/work-items/`, writing the path back into the story only if editing the story is in run scope. |
| External ticket + adapter receipt | Create/update a local item; store the adapter key/URL in the `**External Ticket**` field. |
| External ticket, no adapter | Local item with an unresolved external marker (`ticket-unresolved:<id>`). |
| Free-form / greenfield | Local item keyed by a stable kebab slug derived from the goal. |

> A missing external ticket **never blocks intake**. External tickets are optional and
> adapter-driven; when one is absent or unresolvable, a repository-local work item is created or
> linked in its place.

### Adapter behavior

Ticket lookup is adapter-driven and read from `.agentic/guides/` (`project.md`,
`integration/*`). Consult `${CLAUDE_PLUGIN_ROOT}/references/work-item-adapters.md` for the adapter
contract. This skill performs **lookup only** — it never creates or updates external tickets. The
branch-guard-gated `prepare_for_development` sync is emitted later by the orchestrator, not here.

| Adapter state | Behavior |
|---|---|
| No adapter configured | Do **not** fail intake. Write from the raw ticket id/URL, mark the source unresolved, add an open question, and record a `work_item.adapter_warning` event plus external sync `pending`. |
| Configured but fails | Continue via the local item. Append a `work_item.adapter_receipt` event with `status: "failed"` to both ledgers, and mark external sync `failed`. |

## On every local work-item create/update

First determine whether the selected run has `.agentic/state/runtime.sqlite3`.
For a managed run, persist the work-item event through the coordinator-owned
runtime event operation, then call `legacy.export` to regenerate the two
compatibility ledgers. Never append those JSONL files directly. The six steps
below describe the artifact set and remain the direct procedure only for an
unmanaged legacy run.

Do all six, every time:

1. Write the canonical work-item file at `docs/superpowers/work-items/<id-or-slug>.md`.
2. Mirror/summarize it to the run-dir file `<run_dir>/work-item.md`.
3. For an unmanaged run, append the applicable event to the canonical ledger
   `docs/superpowers/work-items/work-item-events.jsonl`. For a managed run,
   record it through `event.record` and let `legacy.export` render this view.
4. For an unmanaged run, append the same run-relevant event to the run-dir
   ledger `<run_dir>/work-item-events.jsonl`. For a managed run, do not write
   the compatibility file directly.
5. Link the run-dir `requirements.md` from the work item's `## Linked Artifacts` and `## History` sections.
6. If no resolved external ticket, record external sync as `pending`.

### Event names (JSONL append)

`work_item.created` · `work_item.transitioned` · `work_item.linked_artifact` ·
`work_item.adapter_receipt` · `work_item.adapter_warning`

The adapter-receipt failure event carries `status: "failed"`.

## Branch-name suggestion

| Funnel | Suggestion |
|---|---|
| Ticket | The ticket id, verbatim. |
| Greenfield | `feature/<kebab-name>` derived from the goal. |
| Free-form | Ask the pipeline (HITL) or auto-derive (autonomous). |

## Output: `requirements.md`

Write to `<run_dir>/requirements.md` with these field labels and sections, verbatim:

```
**Source**
**Work Item**
**Original input**

## Goal
## Acceptance Criteria
## Context
## Open questions
```

`**Source**` uses this enum, verbatim:

```
free-form | story:<path> | local-work-item:<path> | ticket:<id-or-url> | ticket-unresolved:<id-or-url> | greenfield
```

Grounding rules:

- **Never invent acceptance criteria** that are not in the source. Missing or ambiguous detail
  goes to `## Open questions`.
- Capture greenfield input **verbatim**; run no scaffold commands at this stage.
- Vague input (e.g. "Add it.") is preserved as-is; the ambiguity is surfaced as open questions and
  deferred downstream to the `requirements.ambiguous` gate — do not resolve it here.

## Output contract (exhaustive write set)

Write only these files. Nothing else is written, copied, or moved:

- `<run_dir>/requirements.md`
- `<run_dir>/work-item.md`
- `<run_dir>/work-item-events.jsonl`
- `docs/superpowers/work-items/<slug>.md`
- `docs/superpowers/work-items/work-item-events.jsonl`

`design.md`, `plan.md`, `complexity.json`, and every other phase artifact are **never** produced
here. Prior-run paths in a work item's `## Linked Artifacts` / `## History` are read-only context —
never copy or reference them into the current run dir.

## Non-goals

- No planning, estimation, design, or implementation.
- No scaffold commands for greenfield (no project-init, no vcs-init).
- No creating or updating external tickets from the story-file or local work-item funnels.
- No phase artifacts beyond the output contract.
- A missing external ticket is not a blocker.

## References

- `${CLAUDE_PLUGIN_ROOT}/references/work-item-adapters.md` — adapter lookup contract and outcomes.
- `.agentic/guides/` (`project.md`, `integration/*`) — project-local adapter configuration.

## Related skills

- `sdlc-engine` — Phase 1 caller; emits the dev-lifecycle `prepare_for_development` sync after
  branch-guard success.
- `sdlc-guided` — human-in-the-loop entry.
- `sdlc-auto` — autonomous entry.
