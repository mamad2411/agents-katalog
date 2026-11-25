---
name: keep-the-thread-across-boundaries
description: >-
  Hold what a session settled so it survives a compaction, a model change, a
  resume, or a handoff: the objective in hand, the requests parked behind it, and
  every decision with the alternative it rejected. Use when a decision is made, a
  constraint is stated, an approval is given, the objective changes, or a second
  request arrives before the first is finished. Use again on the far side, when
  you are working from a summary rather than the conversation that produced it.
  A decision that lived only in the conversation did not survive it, and the one
  nobody wrote down is the one that gets re-argued at the worst moment. Not for
  facts with evidence, which belong wherever the host already keeps them, and not
  for durable records a later reader needs, which is a documentation decision.
---

# Keep the Thread Across Boundaries

**Core principle.** A boundary does not lose the work. It loses the reasons.

- **The record is the memory this holds.** Not the transcript, not the plan, and not a fact store. Only what settled and what is still open.
- **The weight sits in *An entry stands alone*.** Every other rule here is cheap once entries are written that way, and worthless when they are not.
- **You opened this in the middle of something.** This is how to keep that work, not a replacement for it. Name what you were doing before you start, and return to it when this is done.

## Five moments, and nothing else

**Write when something settles.** These are the only triggers, and they are events rather than states.

| When | Write |
| --- | --- |
| a decision is made | `decide` |
| a constraint is stated | `decide`, because a constraint is a decision with an open scope |
| an approval is given | `decide`, marked as approval, which expires at a boundary |
| the objective changes | `push`, which parks whatever was in hand |
| a second request arrives before the first closes | `push` if it interrupts, nothing if it is a dependency or independent |

- **Steering is not a moment.** Carry on, look at this instead, try the other one. These change what happens next and settle nothing.
- **A frame is pushed only when there is state worth restoring.** A decision already made, or more than one step done. Otherwise do the second thing and carry on, because a ledger of trivia is worse than no ledger.

## An entry stands alone

**Write it as the thing settles, in words that need no previous turn.** The moment it settles is the only moment the referent is guaranteed present.

- **Approval is anaphoric by nature.** "Yes, do that" names nothing. The entry is the thing approved, written out, not the word yes.
- **The test is cold reading.** If someone reads only the record in two weeks and cannot tell what was decided, the entry is not finished.
- **Carry the alternative that lost**, as `over`. Reopening then needs a new fact rather than a gap in memory. It is usually free. A rival was ruled out. A workaround was refused. A placement was compromised.
- **Writing it is also a misunderstanding check.** Stating what you understood was settled, in the same turn, surfaces a wrong reading now instead of after the work is done.

## What crosses, and what does not

**A boundary is a compaction, a model change, a resume, or a handoff.** Two things cross it in opposite directions, and collapsing them into one rule is the failure this skill exists to prevent.

- **A decision survives.** A recorded choice with its rejected alternative is not a question again.
- **An authorization does not.** Acting is irreversible, so it is pending again unless the approval is still visible. Render the two separately, or the record will claim something is approved after the approval has died.
- **On the far side, read before acting**, and say what you promoted into the current turn and what you left as background. A record nobody promotes from becomes archaeology; one that promotes everything stops being a record.

## The shape on disk

**An append-only log is the truth, and the rendering is the interface.** No materialised state file, so a partial write cannot corrupt what is known, and the history comes free.

```txt
push    <text>              new item; whatever was in hand is parked beneath it
pop                         close the current item and restore the one beneath
decide  <what> --over <no>  record against the current item
brief   [--line]            render: the whole state, or the one line for this turn
```

- **The per-turn line comes from the record.** Opening a turn with the objective and what is parked is how the line is produced, so reading is not a discipline anyone has to remember.
- **Prune by rendering, never by deleting.** Decisions from closed items move to a settled section and the rendering shows the most recent few. Nothing leaves the log.
- **Resolve where it lives rather than declaring it.** What the request named, then what the instruction file declares, then a directory that already exists. Report the path chosen.

## Before a boundary you can see

**A compaction cannot be seen arriving, so the record is kept current instead of written when one looms.**

- **Checkpoint on what is visible.** An announced compaction, a resume, or a handoff. Also a large ingestion, and there the checkpoint goes before the read. The read may be what pushes the boundary.
- **State it flat and last in the turn**, so a summariser keeps it whole rather than compressing it into prose.
- **Use both channels.** The file survives the boundary and needs someone to open it. The stated block may be dropped by the summariser and needs nobody. They fail differently.
- **On a handoff it travels whole.** The receiver has nothing to reconstruct it from.

## What this does not hold

- **A fact with its evidence** belongs wherever the host already keeps them. Two homes for one fact is how they start disagreeing.
- **A durable record a later reader needs** is a documentation decision, not this. This holds what is in flight; some of it graduates, most of it does not.
- **The transcript.** Messages average many times the length of the entry that distils them, and a buffer of recent messages is what several collections already keep and why it does not help them.

## Routing

- **Every skill writes here at its own settle points.** A budget stated before probing, a rival ruled out, a placement compromised, a slicing chosen: each is already announced somewhere, and this is where the announcement leaves a trace.
- **A review reads it** rather than reconstructing the reasoning at the end.
- **A direct instruction from the user outranks anything here.**
