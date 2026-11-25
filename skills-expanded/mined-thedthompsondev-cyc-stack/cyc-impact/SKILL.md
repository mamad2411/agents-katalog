---
name: cyc-impact
description: "Find what a change could break beyond the lines it edits, and prove the fact that makes it safe. Use before any substantive change, when a change touches shared state, storage, or interfaces, or when a build or verify step reveals an unexpected dependency."
---

# Map the blast radius

Listing callers is not the job; search does that in a second. The job is to find the **load-bearing fact**, the one thing the change is safe *because of*, and prove it. Read-only: finding an affected area does not authorize editing it. See the [impact-analysis standard](../../docs/impact-analysis.md) and [handoff contract](../../docs/skill-contract.md).

## The core loop

1. **Check the history.** Read the [context](../cyc-context/SKILL.md) docs and [error ledger](../cyc-error-ledger/SKILL.md) entries for the touched paths. Recorded gotchas are the first connections to check.
2. **Start from the chain.** Take the call chain from [Understand](../cyc-understand/SKILL.md). Mark every hop the change will touch.
3. **Trace outward from the changed data, not the changed file.** Who else reads this field, row, key, or event? Who writes it? Search for the data name, the storage key, and the event name, not just the import.
4. **Look where search stops.** Imports miss the dangerous connections. Check each of these that exists in the project:
   - saved data already on disk or in a database (old records missing the new field)
   - wire formats: API responses, JSON contracts, generated clients
   - config, feature flags, route or plugin registration by string name
   - scheduled jobs, webhooks, queues, and event subscribers
   - other languages or services reading the same store
   - derived UI: counts, filters, sort orders, badges, empty states
   - timing: concurrent writes, teardown, running the action twice
5. **Name the load-bearing fact.** "This is safe because every reader goes through `getAssignments()`, which defaults missing fields." Then prove it at the highest rung you can reach:

   | Rung | Evidence |
   | --- | --- |
   | 1 | Someone said so |
   | 2 | Pointed at the line |
   | 3 | Walked through the failure case by reading |
   | 4 | Ran a script or test that shows it |
   | 5 | Reproduced it in the running app |

   Aim for rung 4 on anything touching storage or shared interfaces. Report the rung reached for each fact.
6. **Split the map into Risks and Cleared.** Risks: connections that could break, each with the check that would catch it. Cleared: connections you checked and why they are safe, with the rung. A map with no Cleared section usually means nothing was actually checked.
7. **Name the cheapest check before build.** The one test or script that would most likely catch a mistake. It goes straight into [Verify](../cyc-verify/SKILL.md)'s matrix.

Keep it proportionate. A copy change inside one component needs a two-line map. A storage or interface change needs the full loop.

## Done when

- The load-bearing fact is stated and proven at rung 4 or higher, or its lower rung is stated with why.
- Every Risk row has a check that would show it red.
- The search list in step 4 was applied, and skipped categories have a reason ("no background jobs in this project: searched for cron, schedule, queue").

## Output

| Location | Connection and evidence | Risk or Cleared | Rung | Check |
| --- | --- | --- | --- | --- |
| `storage.ts:15` loadAll | Reads saved assignments; old records lack `finished` | Risk | 4 (script loaded fixture) | Legacy-record load test |
| `Counter.tsx:8` | Counts `filter(a => !a.finished)` | Risk | 2 | Count after mark-finished |
| `ReminderJob` | Registered by name in `jobs.json`; reads same store | Cleared: skips unknown fields | 3 | none needed |

## Anti-patterns

| Name | The tell | Fix |
| --- | --- | --- |
| Caller dump | A list of every file that imports the module | Find the load-bearing fact instead |
| Import-only search | Only `import` statements were searched | Search the data name, key, and event |
| Unproven "safe" | "Should be fine" with no rung | Prove it or label it rung 1 |
| Scope creep | Map item becomes "also fix the reminder job" | Map it; changing it needs the user's scope |

## Handoff

Pass the Risks table, the load-bearing fact, and the cheapest check to [Design](../cyc-design/SKILL.md) and on to Verify. When build or verify finds something the map missed, come back here, add it, and name which checks it adds. That missed connection is also worth a note for [Reflect](../cyc-reflect/SKILL.md).
