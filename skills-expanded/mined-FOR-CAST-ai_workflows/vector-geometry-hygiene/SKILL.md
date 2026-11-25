---
name: vector-geometry-hygiene
description: The sf and terra vector-repair sequence distilled from repeated corrective commits -- validity, geometry-column drift, attribute-geometry agreement, polygon/multipolygon cast order, join direction, units handling, and why terra::makeValid() and sf::st_make_valid() are not interchangeable.
when_to_use: Any sf or terra vector set operation (union, intersection, difference, erase, dissolve, buffer); polygons coming back empty, slivered, or with dropped attributes; "attribute variables are assumed spatially constant" warnings; units errors; casting between POLYGON and MULTIPOLYGON.
paths:
  - "**/*.R"
---

# Vector geometry hygiene

Five separate corrective commits in one project's history converge on a single
safe sequence. Each fixed a real, silent data loss.

## The canonical sequence

```r
a <- sf::st_make_valid(a)
a <- sf::st_set_geometry(a, "geom")     ## the column name drifts between operations
a <- sf::st_set_agr(a, "constant")      ## declare attribute-geometry agreement

out <- sf::st_difference(a, b)          ## the actual operation

out <- sf::st_make_valid(out)           ## set ops can produce invalid geometry
out <- sf::st_cast(out, "MULTIPOLYGON", warn = FALSE)   ## order matters
out <- sf::st_cast(out, "POLYGON",      warn = FALSE)
```

Why each step exists:

| Step | What it prevents |
| --- | --- |
| `st_make_valid()` **before** | invalid input silently yields empty or wrong output |
| `st_set_geometry("geom")` | the active geometry column name drifts between operations, so a later join or write picks the wrong column |
| `st_set_agr("constant")` | silences the attribute-geometry warning *and* avoids **dropped attributes** -- a fix commit exists titled "dropped polygons issue in seral patches union" |
| `st_make_valid()` **after** | union and intersection routinely emit invalid rings |
| cast MULTIPOLYGON **then** POLYGON | *"cast multipolygon before cast polygon b/c mix of polygon/multipolygon produced"* -- casting a mixed set straight to POLYGON drops features |

## `st_make_valid()` is not always the right repair

For polygons with reversed winding order (common in tenure and administrative
boundary data), `sf::st_make_valid()` **collapses them to slivers**. One project
states the rule flatly: repair with `terra::makeValid()`, *never*
`sf::st_make_valid()`, for those layers.

Practical rule: check the area before and after any repair.

```r
before <- sum(sf::st_area(x))
x <- repair(x)
after  <- sum(sf::st_area(x))
stopifnot(abs(as.numeric(after - before) / as.numeric(before)) < 0.01)
```

A repair that changes total area by more than rounding has not repaired anything.

## Functions that do not exist

`sf::st_delete()` does not exist. The operation you want is `sf::st_difference()`.
A commit exists whose entire purpose is making that substitution.

## Join direction is a modelling decision

> use left join for the two layers with the leading group -- we want to keep/use
> the first layer's geometries throughout

Whichever side you join *from* supplies the geometry. Getting it backwards silently
substitutes one layer's polygons for another's, and the result still looks like a
map. State in a comment which layer's geometry survives, and why.

## Units

`units` objects propagate through arithmetic and then break comparisons and
indexing:

```r
rad_px <- ceiling(rad / pixel_size)
if (inherits(rad_px, "units")) {
  rad_px <- units::drop_units(rad_px)      ## guarded: an unconditional call ERRORS
}                                          ## when the value is not a units object
```

An unconditional `units::drop_units()` was committed, then fixed by adding the
`inherits()` guard. Conversely, `do.call(c, ...)` **preserves** units where `c()`
in some paths does not -- used deliberately in the corpus with that comment.

## Loud failure for unmapped domain values

When reclassifying a categorical field, a value with no mapping must not silently
vanish:

```r
## loud on purpose: a new domain value must not silently drop out of the footprint
unmapped <- setdiff(unique(layer[[fld]]), names(reclass))
if (length(unmapped)) {
  warning(layer_key, " has ", fld, " values with no reclass entry: ",
          paste(unmapped, collapse = ", "))
}
```

The same principle, stated in another project as a rule: **a directive that matches
nothing must not pass silently.**

## Uniqueness of classification keys

A classification key must be unique across the dimensions the consumer actually
tests. One integration bug arose because a class code was unique per *class* but
not per *(dataset, class)* pair, and the consumer only tested the class -- so two
different datasets returned the identical feature set and **every linear feature
was double-counted**. Check what the consumer keys on, not what looks unique to you.

Related: `abbreviate()` collisions. Abbreviating identifiers to build output names
collided 68 times out of 399 in one project, and *"colliding units silently
overwrite each other's aggregates and figures"*. The documented non-fix is also
worth knowing: **do not vectorise `abbreviate()`** -- the codes would then depend on
which other units are present, so adding a layer could silently rename another
unit's outputs.

## Non-recursive file listing drops nested data

```r
list.files(dir, pattern = "\\.shp$")                    ## misses nested layers
list.files(dir, pattern = "\\.shp$", recursive = TRUE)  ## correct
```

A non-recursive listing dropped nested shapefiles and the loss was
*"indistinguishable from a legitimate 'doesn't intersect the study area' drop, with
no warning."* Count what you found and assert it is what you expected.
