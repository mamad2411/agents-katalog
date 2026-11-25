---
name: workflow-volume-design
description: Design reliable 3B workflows that use named volumes or filesystem state. Use whenever a workflow stores or shares files, persists state across runs, receives concurrent requests, must let only one request win (bookings, reservations, claims, unique names, limited stock, or deduplication), keeps counters or shared records, uses an embedded database, handles uploads, builds reporting data, or needs temporary per-run files.
license: Apache-2.0
compatibility: Tines 3B
---

# Design workflows with volumes

Use this skill before creating or changing steps that use named volumes or filesystem-backed state. Discover the workflow tools available in the current interface. For an existing workflow, inspect its step graph, source, volume declarations, schedules, recent runs, and volume usage before changing the design. Separate measurements from assumptions.

Users describe the behavior they need, not a storage primitive. Choose file layouts, database formats, volume names, and mount options yourself. Ask only product questions that change the design, such as whether data must survive later Live runs, how fresh an answer must be, or how long records must be retained. Explain the resulting behavior in product terms.

## Core model

A volume is a named POSIX directory mounted at `/storage/<name>`. In Live, every workflow in a space that declares the same name mounts the same committed files. Draft branches have isolated files. `scope=run` gives one workflow run its own volume, shared by steps in that run that declare the same name and scope. A `:ro` mount is read-only.

A step reads the volume as it was committed when the step started and writes into a private view. Other steps see the last committed version, never its partial writes. A failed step discards its changes. A successful step publishes each volume separately and atomically, so files that must be committed together belong in one volume.

Two runs of the same step, different steps, or different Live workflows in the same space can write the same named volume at the same time. Run-scoped volumes are shared only by steps in one run, so separate runs do not write the same run-scoped volume.

When a step publishes, 3B checks every file and directory entry the step created, changed, or deleted. If any of them changed after the step started, the publication fails with a volume conflict that names the volume and the file, the step fails, and none of its changes to that volume are saved. Overlapping runs that write different paths both publish. Two runs that create the same new file conflict just as two runs that edit it do, while two runs that create the same directory do not. Only files a step writes are checked. A file it only read can change underneath it without a conflict.

File locks are the other coordination tool. `flock` and `fcntl` locks work across steps as they do between processes on one machine, and a step’s first lock on a file it has not changed brings its copy of that file up to date. So a run that locks a file before reading it and holds the lock through its write sees the latest version and takes turns with overlapping runs instead of conflicting. Only the locked file is refreshed, so lock the file being changed, not a separate lock file. Files a step only reads, claim files, and new unique records need no lock. SQLite locks its file for each transaction and DuckDB for as long as it is open, so neither needs extra locks, but SQLite with write-ahead logging coordinates through shared memory and its locks stay inside the step.

A routed step’s response reaches the caller before its volume changes publish. A request step therefore cannot promise its caller that a write was saved. When the caller needs the outcome, respond that the request is pending and let the caller read the published result. Linked downstream steps start only after the step’s changes publish, so send confirmations, notifications, and other side effects that depend on a write from a downstream step.

Follow the [secret-storage prohibition](../building-workflows/SKILL.md#volumes). Use stdin and stdout for small handoffs between adjacent steps. Use volumes when steps need filesystem paths, many related files, random access, or data that survives a step.

## Choose a pattern by the guarantee

Decide what the product must guarantee when requests overlap, then pick the matching pattern. Plain files support every pattern here.

- **Independent records.** Submissions, events, uploads, and messages that never compete get a new unique path each, such as `incoming/<date>/<unique-id>.json`. These writes never conflict.
- **One winner per key.** When at most one request may succeed for something, derive a stable key for it and use one claim file at `claims/<key>.json`. Examples are a booking for a resource and time slot, a claim on a task, a unique name, a unit of limited stock, an idempotency key, or a lease. If the claim file exists, answer right away that the key is taken. Otherwise create it with the request’s ID and respond that the request is pending, naming the key and the request ID. If two requests race, the later publication conflicts and its claim is discarded. The caller confirms the outcome by reading that claim file and comparing the request ID, which gives a final answer as soon as either claim publishes. Releasing the claim deletes the file, and a deletion that overlaps another change to that file also conflicts. When a rule spans more than one key, claim every key it depends on in the same volume, so the claims publish or fail together. For one booking per person per day, claim both the resource’s slot and the person’s day. For a time range, claim each fixed slot it covers.
- **Shared state changed in place.** For a counter, a small status document, or one subject’s record that several runs update, lock the file, read it, change it, write it back, and unlock it, so overlapping runs take turns. Without the lock, the later run conflicts and its change is lost. Hold the lock only for the read and write, never across connector or network calls. If a request step changes the state, record the request ID in the file so a lookup can confirm the change landed. Partition this state by subject so unrelated updates never wait on the same file.
- **State derived from many inputs.** For indexes, aggregates, reports, and databases that many requests contribute to, request steps write independent records to an inbox. A consumer step applies a bounded batch, updates the derived files, and records each applied input’s ID with the derived data. It deletes input only once a later run finds that ID in the published data, because a locked file can publish separately from the rest of its step’s changes, so the update and the deletions can land in either order. Overlapping consumers take turns on a database’s locks or conflict on the derived files they both change, skip input already recorded as applied, and leave the rest in the inbox for the next run. Recheck current state when applying each input, because it may be stale by then, and record rejected input or its outcome when the product needs it.
- **The caller needs the outcome.** Because responses precede publication, return a request ID, then serve the result from a read-only lookup of published state, such as the claim file, the record, or an outcome file the consumer writes. A page can poll that lookup until the result appears. Bound the polling, and if nothing has published after several seconds, treat the attempt as failed and let the caller resubmit with the same request ID.

```text
request  → validate → read claims/<key>.json or views/<subject-id>.json
                    → create claims/<key>.json or inbox/<bucket>/<unique-id>.json → respond pending
lookup   → read claims/<key>.json or outcomes/<request-id>.json from a read-only mount
consumer → delete input already recorded as applied → apply a bounded inbox batch → update derived files
```

A conflict is the expected result when overlapping runs change the same file without a lock. The losing step shows as failed with a volume conflict, and 3B does not run it again, even when the step sets `retry_seconds`. Design so that losing is harmless. A claim that lost is visible to the caller’s lookup, and input a consumer did not apply stays in the inbox for the next run. Keep input until the change that consumed it is published, and give each request an idempotency key that survives retries. When a user asks about these failed runs, explain that they are the losing side of a race and that nothing was lost. Do not reach for an external database or a separate service only to serialize writes. Recommend one when the product needs queries, transactions across many records, or a synchronous answer these patterns cannot give.

## Shape the request path

Design the common request around the answer its caller needs. When possible, one entry step validates the request, reads only that subject’s current view, writes a new record or claim file, and responds. Mount only the volumes it uses. A direct response should not also start downstream steps that merely decide there is no work. Keep connector calls, large scans, aggregation, and database updates off a frequent request path when the product permits a short delay.

For concurrent requests, give each delivery, device, customer, or job a distinct record path. Use stable subject keys for direct lookups, unique IDs for new immutable records, and idempotency keys that survive retries. Do not append from many runs to one shared file or update a shared database from request steps. A small file per subject often suffices for point lookups. Mount a volume read-only in steps that only read it.

```Dockerfile
VOLUME ["incoming"]
VOLUME ["views:ro"]
```

Keep lookup work proportional to the subject being requested, not to all retained records.

Only create downstream executions for work that must follow this request. A scheduled or otherwise low-concurrency step can update derived state separately when a brief delay is acceptable. Preserve the required authentication, response signing, freshness, and failure behavior. If the caller needs an immediate result that cannot be computed from current and pending state, keep the necessary work on its response path.

## Embedded databases

Start with files per record, key, or subject. Use an embedded database only when the product needs its queries or transactions. A database file is shared state that is changed in place, so open it on the volume, never as a copy read into memory or `/tmp` and written back, which skips its locks. Request steps may query a published copy through a read-only mount but should send changes through an inbox to a consumer. For SQLite, set `PRAGMA journal_mode=DELETE` on every open, because some frameworks enable write-ahead logging and it persists in the file, and set a busy timeout of a few seconds so a writer waits its turn. Start a transaction that reads and then writes with `BEGIN IMMEDIATE`, because two transactions that both read first cannot both upgrade to a write. Another step that opens a DuckDB file while it is open fails, so open it only for the work that needs it and run `CHECKPOINT` before closing. Close the database before the step exits so no journal is left beside it to publish out of step with the main file. Keep it in one volume with the inbox that feeds it. If one consumer cannot keep up, partition the database by a stable key into independent files.

## Bound background work and storage

Move aggregation, database updates, view refreshes, and cleanup out of frequent entry steps when a short delay is acceptable. Give each run a fixed record and time budget. Overlapping consumer runs are safe but waste work, so keep each run short enough to finish before the next one starts. When a tick only triggers a scan of durable pending records, skip obsolete ticks instead of replaying them after a queue delay. Apply the bound before reading, parsing, or sorting a growing directory. Use direct paths or bounded time- or key-based buckets so selecting the next batch stays cheap. A schedule must drain sustained input faster than records arrive. Otherwise, its queue and volume usage grow even when each run succeeds.

Remove or compact applied files according to the required retention period. Keep necessary outcomes and idempotency information, but avoid retaining full payloads twice without a product need. Estimate retained logical bytes from input size, arrival rate, derived files, database working files, and retention time. All volumes in a space share the space’s storage limit, and new runs in the space are refused once it is reached, so inspect actual volume usage when it may affect the design. Do not silently drop required data to save space.

For source data, inspect metadata and filter before downloading when possible. Fetch only needed files, and use pagination, change feeds, ranges, streams, or batches for larger inputs. If the complete collection is required, plan ingestion, retention, and recovery from interruption rather than relying on one large download.

Check representative requests, duplicates, overlapping requests for the same key, and sustained traffic. Inspect request latency, waiting executions, background run duration, oldest pending age, pending files and bytes, and volume usage. A successful scheduled run is not enough. Pending work must repeatedly drain under the expected arrival rate.

## Lifetime and draft storage

Use `VOLUME ["state"]` when files should survive and be visible to later Live runs. A read-only step declares `VOLUME ["state:ro"]`. Every workflow in the space that declares `state` shares its Live files.

Draft branches start with isolated files for the same name. Whether a draft starts empty, copies Live’s data, or copies the data of the branch it was forked from is decided per draft. When the workflow context describes that decision as pending, follow its instructions and record the answer with `seedBranchStorage` before running any step that mounts the volume; a copy is a snapshot, so later changes in the draft never affect Live or the source branch. The user can reset a draft’s stored data from the storage browser. Draft files are discarded when the draft is pushed live; only when the workflow has no Live storage yet is the user offered to seed Live with the draft’s data.

Use `VOLUME ["work:scope=run"]` for files needed only within one workflow run. A reader declares `VOLUME ["work:scope=run,ro"]`. Every step sharing that run-scoped volume must declare `scope=run`. `VOLUME ["work:ro"]` names a different, persistent volume. Scope changes lifetime, not whether writers overlap within a run.

## Other useful shapes

- Independent uploads, generated artifacts, and cache entries can use one directory per job or source key. Readers can use those paths directly when no cross-job query is needed.
- DuckDB suits batch analysis over tabular data. When a SQLite database grows to hundreds of megabytes read by scattered lookups, `PRAGMA page_size = 65536`, set before the first table is created or applied once with `VACUUM`, cuts the reads a lookup costs. A small database or one scanned once per run does best with the defaults. Use a remote source when it can answer the required query without a local copy.
- Separate volumes when ownership, lifetime, or retention differs. Do not split files that require one atomic publication across volumes. More volumes and mounts also add work to every step that uses them.
- Read-only APIs and dashboards should mount read-only views. If a shared summary is needed, a consumer can update it from completed records.

## How volume I/O behaves

Volumes are network-backed and read on demand in 64 KiB blocks. Opening a file costs nothing, an unread block costs a network round trip, and data a step has read stays cached while its memory allows, so scattered small reads across a large file are the expensive shape and sequential reads are cheap. A successful step publishes only the blocks it changed; fsync adds nothing, and a file deleted before the step ends costs nothing. `/tmp` and the working directory are memory-backed, 512 MiB each by default, inside the step’s memory limit, which the CPU count and memory a process reads from the system do not reflect.

This matters only for a step whose time is dominated by one large file. For that step, prefer fewer and larger reads over scattered small ones, stream a scan rather than load the file whole, group writes so each block is dirtied once, and leave rereads to the file cache rather than a large cache inside the process, which counts toward the step’s memory. Keep a change only when a representative run before and after justifies it.

When explaining the finished workflow, describe what the caller sees, which results are pending at first, and when they become final. Mention storage details only when they affect the product’s behavior or the user asks.
