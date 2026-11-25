---
name: spades-caching
description: Eight years of accumulated SpaDES Cache() lessons and the conclusion they reached -- when a pipeline framework owns caching, disable reproducible's cache entirely rather than layering two caches. Covers cache scoping, what must never reach a cache key, and the option firewall.
when_to_use: Deciding whether to Cache() something in a SpaDES module or pipeline; a simulation re-runs when it should not, or does not re-run when it should; cache collisions between study areas or machines; setting reproducible.useCache or .useCache module parameters; editing the arguments of a tar_simspades() or similar simulation target in a targets pipeline.
---

# Caching in SpaDES

Over a hundred commits across eight years touch caching in these projects. The
chronology is worth knowing because it converged somewhere specific.

## Where it ended: one cache, and it is not this one

When a pipeline framework (`targets`) owns the dependency graph, **let it own the
cache too**. Two caches layered over each other produce results that are stale
according to one and current according to the other, and neither reports a problem.

The pattern that works:

- every module gets `.useCache = FALSE`;
- `Cache()` is never called in the pipeline definition;
- an explicit **option firewall** is installed so nothing re-enables it by default:

```r
reproducible.useCache    = FALSE
reproducible.useMemoise  = FALSE
reproducible.useCloud    = FALSE
spades.cacheChaining     = FALSE
spades.saveSimOnExit     = FALSE
spades.browserOnError    = FALSE
spades.recoveryMode      = FALSE
spades.allowInitDuringSimInit = FALSE
spades.futureEvents      = FALSE
```

That firewall carries its own maintenance note, which is the right instinct:
*"Audited against SpaDES.core 3.1.2.9016 / reproducible 3.1.1.9062; audit it again
on each dev bump."* An option firewall is only valid against the versions it was
audited against.

## Simulations run from a targets pipeline

When the pipeline is `targets`, a simulation stage is usually one target built by a
factory such as `tar_simspades()`:

- **Every factory argument is part of the command hash.** `tar_simspades()`
  `bquote()`s its arguments in at definition time, so a cosmetic edit to an argument
  block invalidates the simulation. One project records the cost:

  > `local_workers` toggling 8 -> 1 -> 8 and the 9014 -> 9015 `mem_workers`/`mem_frac`
  > command-shape change kept invalidating the baked command hash

  -- for a stage whose rebuild is 22 hours. Keep runtime resource knobs out of the
  factory call, and check the rebuild cost before editing an argument block.
- **A variant that must not invalidate the main run gets a copied spec, not a shared
  one.** One project keeps a gated experimental variant deliberately *not* derived
  from its main simulation spec, so editing the variant can never invalidate the
  22-hour main run. Do not "deduplicate" it.
- **Register the factory with tarborist** so the IDE can see the targets, in
  `.vscode/settings.json`: `"tarborist.additionalSingleTargetFactories":
  ["tar_simspades"]`.

## If you are caching anyway, the accumulated lessons

Each of these is a dated fix in the record:

- **Scope the cache by study area.** Cache paths shared across study areas collide,
  and the collision is silent -- you get another region's result.
- **Never cache stochastic simulation events**, and never cache post-processing
  events. Both were tried and both were reverted.
- **Keep cosmetic arguments out of the cache key.** A plotting-time argument
  (`.plotInitialTime`) once invalidated an entire simulation cache because the cache
  treated it as a semantic change. Conversely, a resource knob baked into a key
  invalidates expensive work whenever you retune it.
- **Cache validity can be machine-specific.** Backends were switched three times in
  four weeks (SQLite, Postgres, RDS) chasing this; an NFS-shared SQLite cache
  **deadlocks** under concurrent writes from multiple workers. Keep any
  SQLite-backed cache on local scratch, and share only content-addressed file
  caches over NFS.
- **`userTags` discipline** matters as much as the key -- untagged cache entries
  cannot be selectively invalidated later.
- Upstream argument names drift (`cacheRepo` became `cachePath`); pin your
  dependency versions and check the signature rather than assuming.

## `prepInputs` and friends: known sharp edges

- **An empty `cropTo`/`maskTo` geometry silently yields no cropping** -- you get the
  whole source raster back with no warning. Assert the geometry is non-empty first.
- **Reprojection before cropping is the expensive default.** Some helpers
  reproject the full source extent before cropping to your window. Crop in the
  source CRS first: one case went from >50 minutes to ~1.4 seconds.
- **Unauthenticated cloud downloads can silently write an HTML sign-in page** where
  a restricted file was expected, ~970 KB of it, which then fails much later as
  "not recognized as a supported file format". Check the downloaded file's type,
  not just that a file arrived.
- A `file://` URL to a multi-file format (shapefile) can drop the sidecars and fail
  on the missing `.shx`. Prefer single-file formats (GPKG).
