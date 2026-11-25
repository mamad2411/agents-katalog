---
name: requirements-sync
description: Use when initializing project requirements documentation or synchronizing confirmed conversational requirements and corrections with project specs, architectural constraints, and relevant delivery records.
---

# Requirements Sync

Maintain project documents that let a future reader understand the agreed system behavior without reconstructing the conversation. Use the project's existing documentation conventions.

## Write For The Document's Reader

Keep each addition only when it helps the reader understand current behavior, acceptance, constraints, a consequential decision, or an actionable open question. Express the effective requirement directly: after a format correction, write "Export records as CSV."

Requirements describe the product; architecture describes responsibilities and boundaries; agent rules describe collaboration. Keep task narration, discarded alternatives, and editing explanations in the work report or existing change history when useful for coordination. A business restriction such as local-only storage belongs in the requirement because it defines behavior. Wording that merely answers a previous correction does not.

Track implementation and verification in the project's existing status or change records. Where none exists and delivery state matters, use one compact status summary with links. Per-requirement provenance, progress, and checklists are optional, not default fields. Relate any recorded evidence to the behavior it actually establishes.

## Establish The Working Agreement

- Locate the target project and read applicable agent rules, documentation entrypoints, authoritative requirements, architecture, and active changes. Clarify an ambiguous target before writing.
- Establish intended behavior from available user decisions and authoritative specifications; use inspected implementation to establish current behavior. Keep unsupported architectural claims as open questions only when they affect the task.
- Preserve existing document language; default generated project documents to Chinese when no convention exists. Preserve unrelated content and authorization boundaries.
- For discussion-only, planning-only, or read-only requests, keep proposed changes in the conversation. For an unambiguous instruction to change behavior, synchronize it directly.

## Initialize Or Adopt

When initializing, adding missing document homes, or repairing the documentation entrypoint, read [references/project-docs.md](references/project-docs.md). It contains the fallback layout, content outlines, and persistent project-rule fragment.

Reuse existing document homes and specification workflows, including OpenSpec. Initialization establishes documentation and routing; application structure stays under the project's own design process. Ordinary sync work may establish missing document homes when authorized.

During initialization or a requested routing repair, add concise synchronization rules and a read-when index to the existing agent entrypoint, creating `AGENTS.md` when none exists. Follow established routing across multiple entrypoints. Merge equivalent rules and leave already adequate content unchanged on repeated initialization. Ordinary requirement edits use that routing as established.

Entrypoint instructions must be usable by a future agent independently of this skill. Their effect depends on the host loading them and the agent following them.

## Classify Each Conversational Change

| Input | Treatment |
| --- | --- |
| Explicit product behavior, business rule, acceptance condition, or lasting constraint | Update the corresponding confirmed requirement. |
| Correction, replacement, or cancellation | Edit the existing item to the agreed effective behavior and preserve unaffected decisions; clarify if the resulting behavior is ambiguous. |
| Question, tentative idea, or agent-proposed enhancement | Keep it in the discussion. When the user asks to retain it, record a concise candidate separately. |
| Commit, build, or temporary investigation instruction | Execute only within task authorization; usually no product requirement entry is needed. |
| Fix restoring already specified behavior | Reuse the existing requirement; update relevant acceptance or evidence only when needed. |

Process corrections as they arrive and consolidate related updates. A clear replacement supersedes the old wording; clarify unresolved contradictions or ambiguities that change the outcome, continuing independent work when possible.

## Synchronize And Check Impact

1. Read the matching requirement, architectural constraints, and affected entrypoints or callers before implementation. Check ownership, shared state, interfaces, and consequential failure paths.
2. Update the authoritative behavior and acceptance conditions. Keep one home per rule, use links from related documents, and leave superseded wording to version history.
3. Edit small changes in place. For cross-module behavior, interfaces, or architectural decisions, use the existing change mechanism or a concise note under `docs/changes/` when needed. Record useful goal, impact, decisions, and acceptance by linking canonical requirements.
4. Keep confirmed intent, implementation, and verification distinct in the appropriate records. Establish implementation from inspected changes and verification from checks actually run. Record the relevant scope and result; static review, build, local tests, runtime, and visual evidence establish different things.
5. Update architecture from inspected implementation or explicit design decisions, identifying intended design where it differs from the implementation. Document only boundaries and unknowns that matter to the affected behavior.

In an existing specification workflow, use its proposal/delta and status conventions. Record pending intent in the active change artifact and synchronize a delivered-state spec at the workflow's normal point.

## Reconcile Before Delivery

- Reconcile available user decisions, documents, and implementation. Preserve effective requirements and distinguish pending changes and candidates from delivered behavior in their proper records.
- Read the changed deliverables as a maintainer who has not seen the conversation. Remove process residue; retain limitations and rationale that affect actual use or maintenance. Apply this check to headings, names, examples, comments, and copied templates as well as prose.
- Check links and the diff. A repeated initialization should leave adequate documents unchanged.
- Report meaningful changes, link updated documents, and give relevant evidence and outstanding blockers. Keep task-specific progress and verification details in this report or the existing work record.

Apply the user's existing authorization boundaries to all operations.
