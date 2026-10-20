# AGENTS.md (gtfs)

Orientation for an agent working in this service. `README.md` is the full
reference — every config variable, the ops endpoints, the `data/` layout,
and what a second service needs to know to read the database safely. This
file is a map to the import lifecycle's code and the invariants that keep
a bad feed from ever going live; it does not repeat the README's detail.

Also read the root [`AGENTS.md`](../AGENTS.md) — the commit convention,
the "no `Co-Authored-By: Claude`" rule, and the cross-project platform
facts apply here too.

## What this service is for

`gtfs` is the **only writer** of the SQLite database at
`<repo-root>/data/gtfs.sqlite`; `api` is the only other reader, connecting
through that same shared directory (a Docker volume in production, a plain
path in dev). This service serves no transit data itself — only
`/health`, `/status`, `/refresh`. If you're looking for stop search,
departure boards, or `/plan`, that's `api/`, not here.

## The import/swap/finalize lifecycle

One run, from `src/pipeline/importFeed.ts`'s `importFeed()`:

1. **Fetch conditionally.** `If-None-Match`/`If-Modified-Since` against the
   last successful run; a `304` ends the run with no write at all.
2. **Build under a `.building` name**, never the final name
   (`src/db/swap.ts`'s `buildingPathFor`). A build killed by a crash, OOM,
   or `SIGTERM` leaves a `.building` file that is swept at the start of
   the next run — never counted as a version, never a rollback candidate.
   The whole point: a file's existence under its *final* name
   (`gtfs-<version>.sqlite`) is the statement "this version was published."
3. **Gate before promoting** (`src/db/finalize.ts`'s `runSanityGates`) —
   see [Version gates](#version-gates) below. Any failure aborts the run
   and leaves the previous database live; **a failed run is always a
   no-op**, never a partial publish.
4. **Finalize for read** (`finalizeForRead`) — `ANALYZE`, then an explicit,
   verified `wal_checkpoint(TRUNCATE)`. This is not optional bookkeeping:
   better-sqlite3 only runs its automatic WAL checkpoint on `close()` when
   the closing connection is the *last* open one, and this service's own
   `readFeedMeta`/`readLiveState` deliberately hold a second connection
   open against the live database — so without an explicit, verified
   checkpoint here, committed rows could silently stay stranded in the
   `-wal` sidecar and never reach the file a naive copy or move would
   treat as complete.
5. **Promote and swap** — rename `.building` → `gtfs-<version>.sqlite`
   (re-checked for a collision immediately before, since `renameSync`
   overwrites silently), then `swapIn()` atomically repoints the
   `gtfs.sqlite` symlink at it. A symlink, not a renamed file, because WAL
   sidecars are keyed to their database's filename and can't travel with a
   plain rename — see README's [`data/` layout](README.md#data-layout).
   A reader with an open handle to the old file keeps reading it
   unaffected; a new connection resolves the new symlink target.
6. **Garbage-collect old versions** (`gcVersions`, `GTFS_KEEP_VERSIONS`) —
   runs *after* the swap has committed, deliberately: it must never be
   able to delete the file the live symlink now points at, even if it
   throws, so its failure is swallowed and only costs a leaked old
   version, never data loss.

`published` (a local boolean in `importFeed`) is the structural guarantee
behind this: once `swapIn()` returns, the catch block below it must never
delete `currentPath` again, no matter what runs after and throws. If you
touch this function, preserve that ordering — it's what makes "a
successful import can never be undone by a later, unrelated failure" true
by construction rather than by every future line remembering not to break
it.

## Version gates

`runSanityGates` in `src/db/finalize.ts`, run against the freshly built
(not-yet-promoted) database, every one of which must pass:

1. **Required tables non-empty** — `agency`, `routes`, `stops`, `calendar`,
   `trips`, `stop_times`, `shapes`. `translations` is tracked but not
   required; many real feeds ship none.
2. **Row counts within band of the previous run** (default 50%–200%) — a
   feed that collapsed or exploded in size fails here, not silently.
3. **Zero foreign-key orphans** — checked here because loading itself runs
   with `foreign_keys` off (`stop_times.txt` precedes `stops.txt` and
   `trips.txt` in the zip, so enforcing FKs during the load would reject
   rows that resolve later in the same file).
4. **No duplicate `(trip_ref, stop_sequence)` pairs** — nothing else
   enforces this uniqueness.
5. **`shapes.txt` grouped contiguously per `shape_id`** — the writer keeps
   only the first contiguous run of points for a `shape_id` and silently
   drops the rest if that id reappears after its group was already
   flushed. The resulting row's `point_count`/`total_length_m` still looks
   valid; this gate is the only place the truncation becomes visible.

Distinct and separate from all five: an **infrastructure** failure during
the load itself (`SQLITE_FULL`, `SQLITE_IOERR`, a corrupt page) aborts the
run outright rather than being absorbed into the bad-row ratio budget —
see `GTFS_MAX_BAD_ROW_RATIO` in the README's config table. A row that
fails coercion is upstream data noise the ratio gate exists to tolerate;
this machine failing mid-write is not the same kind of problem and must
not be charged to the same budget.

If you add a new required table or a new gate, put it in
`runSanityGates` and add it to this list — an agent (or a maintainer)
six months from now should be able to read this file and know every
condition that can hold a bad feed back from going live, without diffing
`finalize.ts` against its own history.

## Config validation

Like `api`, every numeric/enum config value in `src/config.ts` is
validated eagerly at module load and throws at boot on a bad value, naming
it — never silently falling back or failing later mid-run. `GTFS_URL`,
`GTFS_DATA_DIR` and the cron/timeout settings are all boot-gated; there is
deliberately no "0 disables it" escape hatch on the timeout ceilings,
since a disabled ceiling is exactly the state a typo must not produce.

## Tests

`npm test` runs entirely against a small fixture archive, no network. Real
feed behavior — WAF challenge pages, actual row counts, real timing — is
only exercised by `npm run test:live`, which is not run in CI. See
`README.md`'s [Running the live test](README.md#running-the-live-test)
section before relying on it in an automated context.
