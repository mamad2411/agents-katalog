---
name: member-memory-manager
description: Maintain this Member's private memory — what earns a line in the memory.md index, what belongs in a notes/ file instead, how to compact an index past half its budget, and when to demote knowledge that no longer earns a line. Read this skill when the injected memory block shows a maintenance warning, when the index approaches its budget, or before adding or renaming a note.
---

# Member Memory Manager

`memory.md` is a routing index, not a store, and its budget is real: the injected block states current usage, and past 16 KiB the index is not injected at all — the Member loses its own continuity. Notes are never injected; they are read on demand, so the index must stay small enough to be resident and precise enough to route.

## Three tiers

- **T0 `memory.md` (always injected)** — identity and role, durable rules that must bind every step, what is currently in hand, and one routing line per topic cluster. Target well under 8 KiB; treat 16 KiB as the hard ceiling.
- **T1 `notes/<cluster>/README.md` (read on demand)** — one line per note in that cluster. What T0 routes to is the cluster count (3–6), not the note count.
- **T2 `notes/<name>.md` (read on demand)** — one concept per file; update the existing file instead of writing a near-duplicate, and keep evidence, numbers, and commands here rather than in T0.

Screenshots, logs, and generated artifacts belong under `notes/assets/` and earn no index line anywhere.

## What earns a line

Apply one test before writing: would my future self make a wrong decision without this line? If not, it does not belong in T0. Team facts the ledger already owns, event logs, one-off task detail, credentials, and copies of a note's body never qualify.

## Lifecycle

- **Compact as you write.** Past roughly half the budget, merge and drop while adding rather than appending; naming a cluster in T1 is cheaper than naming its notes in T0.
- **Demote, do not delete.** A rule that stopped binding moves down a tier (T0 to a note, T1 to `notes/archive/`); archived knowledge stays readable and is never silently lost.
- **Separate rolling from settled.** "In hand" is overwritten as work moves; settled knowledge is compacted in place, and that section never accumulates history.

## Check after reorganizing

Re-read `memory.md` once: under budget, one line per cluster, every routing line resolving to a file that exists, and nothing that must bind every step living only in a note. The injected block reports the current size, so a later injection shows whether the rewrite took.
