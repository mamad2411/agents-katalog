---
name: project-prose
description: Use when writing, editing, or reviewing technical documents, comments, decision records, agent instructions, prompts, or diagnostics for factual accuracy, complete contracts, and independence from private conversation, review, or draft context.
---

# Project Prose

Write technical prose a reader can use and verify from the current project. Preserve its facts, obligations, and necessary conditions.

## 1. Check the text against the project

For each questionable passage, ask:

> Can a reader with only the current repository resolve the references and verify the claims?

Inspect the relevant code, configuration, tests, and authoritative documents. Replace private conversation or review references with the actual contract. Qualify unresolved facts instead of inventing behavior. A resolvable link earns its place when it helps readers understand or maintain the system.

Look for these problems and apply the corresponding repair:

| Problem | Repair |
| --- | --- |
| Private draft numbers, phase labels, review rounds, or “as discussed” | State the relevant fact and cite an accessible owner |
| PR/commit narratives or stale “now,” “previously,” and “legacy” framing | Describe current behavior; retain history when it explains a necessary constraint |
| Arguments addressed to an imagined reviewer | State the actual reason, type guarantee, or ownership boundary |
| Obvious control-flow transcripts or code proofs | Keep the non-obvious contract, ordering, race, or failure semantics |
| Vague qualifiers or unowned plans | Specify evidence limits or a real issue/TODO and owner |
| Draft markers or inconsistent prose language | Remove residue while preserving technical tokens |

Judge meaning rather than deleting keywords. Stable issues, standards, incident evidence, alternatives, suppression reasons, and measurement boundaries can remain when they help future maintenance.

## 2. Edit the explanation's owner

Keep each explanation in its authoritative location:

| Information | Owner |
| --- | --- |
| Current behavior and implementation facts | Code, configuration, tests, and current documentation |
| Consumer contracts | The README, API documentation, JSDoc, or diagnostic consumers read |
| Lasting rationale, tradeoffs, and rejected alternatives | The active decision record |
| Incident and migration narratives | The project's history document or postmortem |

Elsewhere, retain the summary and links readers need. Update an existing engineering or data document before creating a parallel explanation. Leave directly discoverable directory, API, and field inventories to their source unless readers need a maintained projection.

Edit sources before derived artifacts: source comments before generated documentation, schemas before generated types. Regenerate through the supported process and inspect the result. Modify vendor files, fixtures, and snapshots only when an authorized source change requires regeneration. Keep frozen archive bodies unchanged; archived decisions explain history, while current sources establish current behavior.

## 3. Rewrite without losing the contract

Identify factual clauses before editing. Preserve:

- Preconditions, postconditions, invariants, and compatibility promises.
- Ownership, lifecycle, timing, cancellation, ordering, and races.
- Security assumptions, failure/recovery behavior, persistence, and wire semantics.
- User-visible behavior and evidence that calibrates limitations.

Use direct present-tense statements, explicit actors, and one main action per sentence. Keep obligation strength, applicability, and the distinction between assumptions and implemented behavior. Remove repeated caveats and explanations already supplied by the owning source.

## 4. Verify the finished text

Read the complete document without the old passage or chat. Check related passages, resolve retained references, and inspect the diff for lost obligations, duplicated reasons, or unsupported claims. Run the documentation, generation, translation, lint, and behavior checks applicable to the changed surface.

Report the edits, checks actually run, and unresolved facts or deferred work. A keyword search alone does not establish semantic correctness.
