---
name: module-contract
description: The SpaDES module metadata contract -- defineModule, expectsInput/createsOutput, reqdPkgs remote specs, explicit loadOrder, and the .inputObjects timing trap where objects supplied via inputs= are still NULL and a CRS comparison silently reprojects your data. Never infer a module's interface; read its defineModule().
when_to_use: Wiring a SpaDES module into a pipeline or another module; editing defineModule metadata; a module reports a NULL object it should have received; compareGeom or CRS errors during simInit; renaming or forking a module; "could not find function" from inside a nested module.
paths:
  - "**/modules/**/*.R"
  - "**/*.R"
---

# The module contract

## Never infer an interface -- read `defineModule()`

A pipeline scaffold whose module wiring was *"approximated from an upstream
reference"* had every stage's inputs and outputs wrong until each was audited
against the fork's actual metadata. The interface is declarative and cheap to
read:

```sh
grep -A400 'defineModule' modules/<mod>/<mod>.R | grep -E 'expectsInput|createsOutput' 
```

Check the **fork you have pinned**, not the upstream module of the same name, and
not your memory of it.

## `.inputObjects()` runs before `inputs=` is loaded

This is the sharpest trap in SpaDES wiring, and one project states it three
separate times in one file.

`.inputObjects()` runs during `simInit()` -- **before** the `inputs=` table loads.
So any object a module touches in `.inputObjects()` must be passed **in memory**
(via the objects/globals path), not as a file input.

Three documented consequences:

1. A module deriving one layer from another in `.inputObjects()` sees `NULL` and
   fails later at a `compareGeom()`.
2. A module reading a study area and a template raster in `.inputObjects()` gets
   `NULL` for whichever came via `inputs=`.
3. **The worst: silent data mutation.** A module compares the CRS of a study area
   against a template and against a reporting polygon. Supplied via `inputs=`, the
   first two are `NULL` at that point, so the comparison sees an NA-CRS study area
   against a loaded reporting polygon and **spuriously reprojects (modifies) the
   reporting polygon.** No error; the data is simply wrong downstream.

Rule: if an object is named anywhere inside `.inputObjects()`, hand it over
in-memory. Passing a file path across the boundary is not enough.

## Do not add `outputs=` where a module already registers its own

If a module owns its per-replicate saves and calls `registerOutputs()`, adding a
redundant `outputs=` specification makes `saveFiles()` re-write the same paths at
`end(sim)` **without** `overwrite = TRUE`, and the run dies with
`[writeRaster] file exists` -- in one case three and a half hours in.

Conversely, know whether your runner **wipes the output directory** before running.
One does by default, *"because terra's writeRaster()/writeVector() and module-side
saves do NOT overwrite, so leftover files from a prior run would error."* An
aggregation stage reading a previous stage's outputs must therefore opt out of the
wipe, or it deletes the very files it is aggregating.

## `reqdPkgs` and nested modules

`reqdPkgs` carries remote specs with branches and version floors:

```r
reqdPkgs = list(
  "data.table", "terra", "ggplot2",
  "PredictiveEcology/LandR@development (>= 1.1.0.9003)",
  "PredictiveEcology/SpaDES.tools@development (>= 2.1.2.9000)"
)
```

Two failure classes come from this one field:

**1. Never fetch a module at run time.** A module that nests another via
`simInitAndSpades()` and calls `getModule("owner/mod@development", overwrite = TRUE)`
mid-run is fetching an arbitrary unpinned HEAD *during* the simulation. That is a
reproducibility hole -- the nested module's version is not captured anywhere -- and
it caused intermittent `could not find function` failures. The fix is to fork and
pin every nested module.

**2. `spades.loadReqdPkgs` flips to `FALSE` for nested runs.** SpaDES.core sets it
`FALSE` once the outer `simInit`/`spades` has warmed up, as a load-once
optimisation. A module that nests another inherits `FALSE`, so the **nested
`simInit` skips loading the nested module's own `reqdPkgs`** -- producing
`could not find function` for a package the nested module correctly declares. Set
it explicitly `TRUE` around a nested run.

**3. One repo at two branches breaks the whole solve.** The dependency resolver
treats the request as a single problem, so one repo requested at two different
branches anywhere in the graph fails the entire solve *and* reports every other
package as conflicting -- which reads like a much bigger problem than it is. Audit
for it before debugging anything else.

Also: `reqdPkgs` is invisible to `renv`, which follows only
Imports/Depends/LinkingTo. Projects carry an `_dependencies.R` shim
(`if (FALSE) { library(...) }`) so those packages stay in the lockfile.

The same blindness reaches package citations: `grateful::cite_packages()` finds
packages with `renv::dependencies()`, so it never sees a module's `reqdPkgs`. Pass
`pkgs =` explicitly -- the pipeline's packages plus
`workflowtools::get_module_packages()` -- and check the result as
`citation-integrity` in `r-project-core` describes.

## Set `loadOrder` explicitly

Implicit load order is unreliable once modules are nested or branched. State it.

## Renaming or forking a module: three names must match

The module's **directory name**, its **`.R` file name**, and the `name` field
inside `defineModule()` must all agree before the module will load. Renaming a
fork without changing all three fails in a way that looks like a missing module.

## Formatting

The `defineModule()` block is a hand-aligned DSL. Add these to `air.toml`'s `skip`
list so the formatter leaves it alone:

```toml
skip = ["defineModule", "defineParameter", "expectsInput", "createsOutput",
        "scheduleEvent", "globalVariables", "use"]
```
