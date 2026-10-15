---
name: bound-the-unknown
description: >-
  Probe unfamiliar ground on a stated budget, and stop when the shape appears
  rather than when patience runs out. For the state before anything is a task,
  where you cannot yet say whether this is a bug, a feature, or nothing. Use when
  a second probe has run and no finding has been named, when a question needs a
  command nobody has run yet, when a read came back different from what you
  expected, or when you are about to write a script to find something out. Covers
  the budget said out loud first, read-only probing, where the intermediate is
  kept, when to stop, and what the probe leaves behind. Nobody needs telling to
  look; what fails is stopping. Not for a symptom that already has a name, a
  change that already exists, or a tool that will not run.
---

# Bound the Unknown

**Core principle.** Looking is not the hard part. Stopping is.

- **This is the state before anything is a task.** You cannot yet say whether it is a bug, a feature, or nothing at all.
- **The weight sits in *Say the budget first* and *Stop on a shape*.** Everything between them is cheap once those two hold.
- **You opened this in the middle of something.** This is how to do that work, not a replacement for it. Name what you were doing before you start, and return to it when this is done.

## When this opens

**The first probe is indistinguishable from an ordinary question. The second is not.**

- **Two probes have run and no finding has been named.** That is the countable trigger. Waiting for a feeling that terrain is unclear does not work, because that feeling arrives late or never.
- **A question needs a command nobody has run yet.**
- **A read came back different from what was expected.**
- **A script is about to be written to find something out.**

## Say the budget first

**State how far you intend to go before the first probe, where I can see it.** A bounded search I can interrupt is worth more than an unbounded one that arrives finished.

- **Say it in probes or in minutes**, whichever the work is measured in.
- **Three cycles is a sound default.** Dispatch, evaluate, refine. A fourth rarely finds what the third missed.
- **Announce the extension rather than sliding into it.** Going past the budget is allowed. Doing so silently is what turns a search into a session.
- **Report what the budget stopped**, not only what it found. An unfinished search with a named boundary is a result.

## Probe without changing anything

**Keep the probe read-only until the shape is explained.**

- **Nothing is installed, no state is mutated, no credential is refreshed.** A probe that changes the thing being studied has destroyed its own evidence.
- **Prefer a count, then a list of paths.** Only some questions need the lines themselves.
- **Independent probes go in one call.**
- **Write the large intermediate to a file and query the file.** Pasting it in to read three lines of it is the expensive mistake, and the same extract answers the next four questions for free.
- **Leave the file and say where it is.** A second attempt that still has the data is cheap.

## Stop on a shape

**Finish on a finding, never on fatigue.**

- **The shape is known when the next decision no longer needs another probe.** That is the test, and it is not the same as knowing everything.
- **Close with an explicit decision**, not with a summary of what was seen. A search that ends in prose ends nowhere.
- **Name what was ruled out.** It is the half that stops the ground being covered twice, and it is free at this moment.
- **An empty result counts only when the query is reported beside it.**

## Prove before you place

**Placement chosen while a technical unknown is open is a guess wearing the costume of design.**

- **Where the unknown is technical, prove it first**, then choose where the code lives. An isolated probe answers the question without paying for placement twice.
- **Where the unknown is only structural, the target is already known.** Restructure first and build into it.
- **The common error is applying restructure-first while the unknown is still technical.** That refactors confidently in the wrong direction.

## What the probe leaves behind

**The code may survive. Its unproven status may not.**

- **Discard it when the value was the knowledge.** The question has been answered and rewriting under a test is cheap.
- **Harvest it when the value was a working path** through a hostile integration that is expensive to rederive.
- **Either way, what ships is proven.** Harvest the shape, never the status.
- **Remove the instrumentation before closing.** Every tag comes out.

## What this does not own

| The situation | Belongs to |
| --- | --- |
| the symptom already has a name | finding a cause from a signal that reproduces |
| the change already exists | judging a change before it lands |
| you know what to build and are choosing where | the structure of owned code |
| the tool itself will not run | a blocker treated as an incident |

## Routing

- **The finding closes as a decision**, with what it ruled out, wherever this project keeps decisions.
- **Once the shape is known this stops.** Carrying on is habit rather than method.
- **A direct instruction from the user outranks anything here.**
