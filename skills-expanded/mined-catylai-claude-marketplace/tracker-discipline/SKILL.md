---
name: tracker-discipline
description: "Defines the seven issue states, the dedupe, parenting and comment-trail rules, and the project's Issue tracker section. Use when moving an item's state, creating or re-parenting an item, commenting on progress, or mapping a tracker's workflow. Not for the start-of-work check (use pre-work-gate)."
license: MIT
---

# Tracker Discipline

The rules for keeping a tracker truthful, whatever product hosts it. This skill owns the status
vocabulary, the dedupe rule, the parenting rules and the comment trail. The tracker adapters
(`github-issues`, `jira-tracker`, or a connected tracker tool) supply the calls; they map onto
the names defined here rather than restating them.

A state, a parent link and a comment are all claims that other people act on without checking.
Every rule below exists to keep those claims true.

## Before you start

Read the `## Issue tracker` section of the project's `CLAUDE.md` for the tracker, the status
mapping and the parent mechanism. If it is missing, ask for the rows the current step needs in
one question and carry on. The template, and which skill reads which row, is in
`references/tracker-config.md`.

## Status vocabulary

Seven states, and only these seven. The identifiers in the first column are the closed set
every skill and adapter uses; the tracker's own names appear only in the Status mapping table.

| State | It claims | Entry condition (all must hold) |
| --- | --- | --- |
| `backlog` | Captured, not yet prioritised. | Written well enough that someone else could pick it up and ask the right questions. |
| `ready` | Prioritised and startable. | Scope understood, parent set, no open blocker, acceptance stated. |
| `in-progress` | Someone is working it now. | Assigned, and work on this item has begun, including reading the code for it. |
| `in-review` | Waiting on someone else's judgement. | A reviewable change exists and is linked from the item; checks are green or their failure is explained on the item. |
| `done` | Finished and integrated. | The change is merged (or, for a non-code item, the decision is recorded) and acceptance is met. |
| `parked` | Deliberately deferred. | A reason and a revisit condition are recorded. |
| `declined` | Deliberately not done. | A reason is recorded. The item stays for the record. |

Happy path: `backlog → ready → in-progress → in-review → done`. Two departures are normal:

- **Review rejection** returns the item to `in-progress`, because `in-review` claims a reviewer
  is waiting and during rework none is.
- **Blocked work** returns to `ready` or `parked` with the blocker recorded. "Blocked" is a
  facet, not an eighth state: record it as a comment or as the tracker's native dependency link,
  and a `blocked` label or flag is fine as a filter alongside one of the seven.

Rules:

1. **Move the state when the thing happens.** Enter `in-progress` when work on the item starts
   and `in-review` as the change is opened, not at the end of the day.
2. **Map, do not extend.** Every tracker state maps onto one of the seven. Where the tracker has
   no equivalent (commonly `in-review` or `parked`), record how it is carried instead, for
   example `in-review = In Progress + linked PR`, in the Status mapping table.
3. **One item, one state.** An item that is "in progress and also in review" is two items.
4. **Keep finished and abandoned apart.** Abandoned work is `parked` or `declined`; `done`
   means integrated. Collapsing them hides whether the backlog shrinks because work lands or
   because work is dropped. A mapping keeps exactly one state meaning "work has begun", one
   meaning "waiting on a reviewer", and distinct terminal states for `done` and `declined`.

Read-only exploration that is not tied to an item (answering a question about the code) moves
nothing. Reading the code as the first step of working a known item is `in-progress`.

**Live** means `backlog`, `ready`, `in-progress` or `in-review`. `done`, `declined` and `parked`
items are not live and cannot be parents.

## Dedupe before creating

Before creating any item, search the tracker for an existing one:

1. Search open items (every live state plus `parked`) on the symptom or outcome, not on the
   wording you were about to use; the existing item was written by someone else in other words.
2. If the work looks like a regression, search `done` items too and link the one it undoes.
3. Record the result as exactly one of:

| Result | Meaning | Next |
| --- | --- | --- |
| `NEW` | Nothing matching exists. | Create the item (see parenting below). |
| `DUPLICATE → <KEY>` | An item already covers it. | Comment on `<KEY>` with the new evidence instead of creating. |
| `UNCHECKED` | The search could not run (no access, tool denied). | Tell the user, and create only if they confirm. |

## Parenting

Every item that is not top level has a live parent. An orphan is a defect to fix when found.

**The candidate-parent list is a query, run every time.** Parents open, close and get renamed,
so a cached list in a skill, config file or memory note is wrong within weeks and trusted while
wrong. A staleness note does not fix that; it only documents it.

1. **Shortlist.** Query live parents that suit most work (the current time-boxed buckets, the
   platform and infrastructure buckets, or the board's equivalent): five to ten entries.
2. **Full set.** Only if nothing on the shortlist fits: every live parent.

Filter on state category, not one state name, so finished, declined and parked parents all drop
out. Trackers accept a dead parent without complaint, so read the parent's state back after
setting it.

When creating an item:

1. Run the dedupe check above.
2. Decide whether the item is top level. Create a top-level item only after the user explicitly
   approves it, because a new top-level item is a planning decision.
3. Otherwise run the shortlist, and present it or propose one candidate with the reason.
4. If nothing fits, run the full set. If nothing fits there either, ask whether a new top-level
   item is warranted and wait for the answer.
5. Set the parent in the create call itself; a follow-up step is the one that gets skipped.

When auditing, treat all three of these as orphans and re-parent them the same way: no parent;
a parent that is `done`, `declined` or `parked`; a parent that no longer exists.

## Comment trail

The item outlives the session; the chat does not. Anything a reviewer or the next person needs
goes on the item before review starts or before you stop. Write for a reader who has the diff and
lacks the reasoning.

Post these three, each with the state move it explains:

```markdown
**Start** (with the move to `in-progress`)
Branch: `<branch>`. Plan: <approach in one or two sentences>.
Differs from the description: <what the item got wrong, or "nothing">.

**Handoff / pause** (state unchanged, or to `ready`/`parked` if blocked)
Where it stands: <done so far>. Known broken: <or "nothing">.
Blocker: <what, who unblocks it, since when, or "none">. Next step: <one action>.

**Finish** (with the move to `done`)
Merged in <link>. Acceptance: <which criteria were verified, and how>.
Split out: <follow-up keys, or "none">.
```

Also comment on a change of approach, a discovery that invalidates the description, and the
outcome of a scope negotiation, so nobody re-litigates it in review. Skip progress noise such as
"still working on this"; it trains readers to skim past the comments that matter.

A tracker comment is not a session handoff. For a document that lets a fresh session resume the
work, use `engineering-workflows:handoff`, and link it from the handoff comment.

## Examples

<example>
Situation: PROJ-88 is `in-review`; the reviewer requests changes.
Action: move PROJ-88 to `in-progress` and comment "Review requested changes to the retry
backoff; reworking. Next step: switch to jittered backoff." Move it back to `in-review` when the
updated change is pushed.
</example>

<example>
Situation: an audit finds PROJ-140 whose parent PROJ-20 is `parked`.
Action: PROJ-140 is an orphan even though it has a parent. Run the shortlist, propose PROJ-31
(the live platform bucket) with the reason, set it after the user agrees, and read PROJ-140
back to confirm the new parent is live.
</example>

<example>
Situation: asked to file "login page times out". The dedupe search on "timeout" and "sign-in"
finds open PROJ-77 "Auth service slow under load".
Action: report `DUPLICATE → PROJ-77`, then comment on PROJ-77 with the new symptom and when it
was seen. Create nothing unless the user says it is a different problem.
</example>

## When something is unavailable

- **No tracker access** (no adapter, no connected tool, tool denied, or a web session without a
  tracker connector): print the exact state move, parent link and comment text for the user to
  apply, and say none of it is recorded until they confirm.
- **No Status mapping entry:** ask which tracker state corresponds to the one you need, use it, and
  offer to add the mapping to `CLAUDE.md` afterwards.

## Verify

After every state move, parent change or comment, read the item back and check:

- its state maps to the one of the seven you intended;
- a new or changed parent exists and is live;
- the comment is present on the item, not only in this conversation;
- a create call recorded its dedupe result (`NEW`, `DUPLICATE → <KEY>` or `UNCHECKED`).

If automation (a hook, an agent, an adapter call) claimed to do any of these, apply the same
read-back; a silent failure leaves the item asserting something false.
