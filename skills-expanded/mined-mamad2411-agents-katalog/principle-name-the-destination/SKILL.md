---
name: principle-name-the-destination
description: "Apply before decomposing work into tickets, phases, or a map. State what done looks like before you break anything into parts."
user-invocable: false
---

# Name the Destination

Decide where the work is going before you cut it up. A decomposition is only correct relative to a destination.

**Why:** Tickets written without a stated end state describe activity rather than progress. You get a plausible-looking plan whose parts do not compose, and nobody notices until the last ticket closes and the thing still is not done.

**Pattern:**

- **State the end condition first**, concretely enough to be checkable. "Users can X" beats "improve X".
- **Decompose backward from it.** Each unit exists because the destination needs it; a unit you cannot trace back is scope.
- **Name what is out.** The excluded surface is part of the destination.
- **Re-read it when the map changes.** A destination that quietly moved is why the plan stopped making sense.

**Boundaries:**

- Genuinely exploratory work has a destination too - it is a *question answered*, not a feature shipped. Name that instead.

**The test:** Point at any ticket and ask what breaks about the destination if you delete it. No answer means it is scope, not work.
