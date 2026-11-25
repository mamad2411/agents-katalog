---
name: end
description: |
  Close a work session into a restartable handoff: reconcile relevant repository and
  Linear state, preserve durable knowledge under the current role's authority, and
  leave user changes intact. Auto-trigger when the user ends or wraps up a session.
---

# End Session

Goal: leave completed work, remaining work, and their durable records in agreement.
Apply only the parts relevant to this session. Ordinary conversation needs no ledger update or handoff; save a brief when unfinished work has context worth carrying forward.

Success means:

- relevant issues have truthful signed outcomes; finished work is moved to Done only after its outcome is recorded;
- a future session can identify the working-tree state, verification evidence, and strongest next action;
- durable knowledge is judged, recorded by its authorized writer, and remains findable;
- pre-existing or another session's changes remain untouched.

Does not count: a generic recap; closing an issue before its outcome is recorded; treating a transient outcome as durable fact; writing frozen daily-note data; or a delegated agent settling OptMem.

Stop when the handoff states what is complete and open, every in-scope ledger update has either succeeded or has a named blocker, and `git status` has been read again.

## Close the loop

1. Read the applicable `AGENTS.md`, active spec or task brief, relevant Linear issues and comments, the current diff, and `git status`. Identify the work this session actually owns; do not claim unrelated dirty files.
   - Find every ticket the session touched, not only the ones still in mind: list the keys in this session's own tool calls (injected instructions name many tickets; this skips them), then judge which were materially worked rather than only read:
     `jq -r 'select(.type=="assistant")|.message.content[]?|select(.type=="tool_use")|.input|tostring' <transcript-store>/*/<session-id>*.jsonl | grep -ohE '\b[A-Z]{2,5}-[0-9]+\b' | sort | uniq -c | sort -rn`
2. Run the smallest verification that supports the outcome. Shared `CLAUDE.md` governs independent review; project instructions govern additional checks. Keep evidence with the result, including unrun checks and their reason.
3. Commit this session's own verified work under the standing authorization. Preserve existing user changes. Push only to a destination and scope already authorized in the active conversation; publication remains ask-first.
4. For tracked work, reconcile the live ledger using the runtime's follow-up convention: post a signed outcome on each materially worked issue before moving completed work to Done; file material follow-ups needing ownership or later action; leave failed writes visible and the issue open.
   - Each closing comment starts with the closure summary: `Delivered:`, `Still unresolved:`, `Continues in:`, `Evidence:` (ruling of 2026-11-11). Anything still owed names its open home under `Continues in:`.
   - Check that each ticket worked sits in the outcome project it serves, or that its start comment says why none fits. Correct its current-state block when a fact changed.
   - When work that started this session has no project home and may outgrow one issue, ask the operator: project, parent issue or single issue, with your recommendation. Mechanics: "Projects and relations" in the convention.
5. Read the runtime's knowledge-management reference before handling proposals or durable memory. Apply its current grammar, duplicate checks, proposal dispositions, and verification rules. Record only material outcomes, current state, durable propositions, or find-again documents; never mutate the frozen daily-note layer.
6. Authority is role-specific: a user-facing primary judges and writes accepted OptMem records; a delegated agent returns canonical candidates to its primary and never settles OptMem. Honor a field-dispatch result contract when one exists, without inventing one for ordinary work.
7. A user-facing primary names its session for what it actually did: `sessions --rename '<3–8 word title>'`. Put the project name first (e.g. "<project>: release checklist rework"). The default title comes from the first message and is often wrong. A delegated agent skips this step.
8. Re-read `git status`. Report completed and open work, verification, commits/pushes (or why absent), ledger/memory outcomes, remaining working-tree state, and the exact restart action.

When a check, ledger write, memory judgment, or push is blocked, keep the artifact and report the evidence rather than declaring a clean close.
