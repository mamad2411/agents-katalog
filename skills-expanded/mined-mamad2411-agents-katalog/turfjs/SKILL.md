---
name: turfjs
description: Navigate the Turf.js (turfjs.org) geospatial library to pick the right function for a task. Use this skill whenever the user writes code touching Turf.js, the @turf/* npm packages, GeoJSON manipulation, or geospatial computations like distance, area, buffer, point-in-polygon, intersection, or clustering — even if "Turf" isn't named. Trigger on imports from @turf/turf or any @turf/ package, on tasks involving lon/lat coordinates and computation (not just rendering), and on v6 to v7 migration questions. ALSO trigger when the user is working with a map library (Leaflet, Mapbox GL, MapLibre, Google Maps, OpenLayers, deck.gl) AND drawing or editing shapes — Leaflet.draw, Mapbox GL Draw, react-leaflet-draw, terra-draw, OpenLayers Draw interaction — because Turf is the canonical pair for "user drew a polygon, now compute on it." Do NOT trigger for pure map-rendering, tile-loading, marker-placement, or basemap-styling questions where no geometric computation, drawing, or editing is involved.
---

# Turf.js Packages

A category-by-category routing guide to the [Turf.js](https://turfjs.org) v7.3.0 API so you can find the right function fast. Every function listed here is real and from v7.3.0; if a user is on v6 there are signature differences — see `references/foot-guns.md`.

## What Turf is, in one breath

Turf is a modular geospatial analysis library for JavaScript/TypeScript. It consumes and produces **GeoJSON** ([RFC 7946](https://tools.ietf.org/html/rfc7946)) and expects WGS84 longitude/latitude coordinates (lon first, then lat — easy to get backwards). Each function is shipped as both a micro-package (`@turf/buffer`) and bundled into the meta package (`@turf/turf`).

## Install + import patterns

```bash
# Get everything
npm install @turf/turf

# Or get individual modules (smaller bundle)
npm install @turf/buffer @turf/distance
```

```typescript
// Bundled
import * as turf from "@turf/turf";
const buffered = turf.buffer(feature, 500, { units: "meters" });

// Individual (preferred for bundle size in browser apps)
import { buffer } from "@turf/buffer";
import { distance } from "@turf/distance";
```

**GeoJSON type imports come from `@types/geojson`, NOT from Turf:**

```typescript
import type { Feature, Polygon, FeatureCollection, Point, LineString } from "geojson";
// You may need: npm install --save-dev @types/geojson
```

## Pick a category for the task

The user's natural-language task usually maps to one of 18 categories. Scan the table, jump to the section, find the function.

| Task sounds like... | Go to |
|---|---|
| "how far / how big / where is the center" | [Measurement](#measurement) |
| "snap coords / round / flip lat-lng" | [Coordinate Mutation](#coordinate-mutation) |
| "buffer, simplify, union, intersect, rotate, voronoi" | [Transformation](#transformation) |
| "convert lines to polygons, explode multi-geometry, flatten" | [Feature Conversion](#feature-conversion) |
| "split a line, find self-intersections, arc between points" | [Misc](#misc) |
| "build a Point / LineString / Polygon / FeatureCollection" | [Helpers](#helpers) |
| "generate fake / test geometry" | [Random](#random) |
| "sample N random features from a collection" | [Data](#data) |
| "isolines, isobands, contours, IDW interpolation, TIN" | [Interpolation](#interpolation) |
| "which points fall inside this polygon / tag features by region" | [Joins](#joins) |
| "generate a grid of hexes / squares / triangles" | [Grids](#grids) |
| "find the nearest point in a set" | [Classification](#classification) |
| "cluster points (k-means, DBSCAN)" | [Aggregation](#aggregation) |
| "iterate every coordinate / feature / segment" | [Meta](#meta) |
| "validate that this input is the GeoJSON type I expect" | [Assertions](#assertions) |
| "true/false predicate: contains, crosses, overlaps, touches, within" | [Booleans](#booleans) |
| "convert km↔miles, degrees↔radians, project to Mercator" | [Unit Conversion](#unit-conversion) |
| "angle between three points, Moran's I, spatial stats" | [Other](#other) |

---

## Measurement

"How far, how big, where is the centroid, what's the bbox" — quantitative properties of geometry.

- `along(line, distance, opts?)` — point at a given distance along a LineString
- `area(geojson)` — area in square meters
- `bbox(geojson)` — `[west, south, east, north]` bounding box
- `bboxPolygon(bbox)` — turn a bbox array into a Polygon Feature
- `bearing(start, end, opts?)` — compass bearing in degrees (-180..180), `final: true` for the back-bearing
- `center(features, opts?)` — geometric center (midpoint of bbox)
- `centerOfMass(polygon)` — center of mass (more "weighted" than `center`)
- `centroid(features)` — mean of all vertices (cheap, fast, ignores area)
- `destination(origin, dist, bearing, opts?)` — point at distance + bearing from origin
- `distance(from, to, opts?)` — great-circle distance between two points
- `envelope(features)` — bounding-box polygon enclosing all features
- `greatCircle(start, end, opts?)` — great-circle line between two points
- `length(line, opts?)` — total length of a LineString/MultiLineString
- `midpoint(p1, p2)` — midpoint between two points
- `pointOnFeature(geojson)` — a point guaranteed to lie on the feature (useful for labeling)
- `pointToLineDistance(point, line, opts?)` — min distance from point to line
- `pointToPolygonDistance(point, polygon, opts?)` — min distance from point to polygon edge (0 if inside)
- `polygonTangents(point, polygon)` — two tangent points from an exterior point
- `rhumbBearing(start, end, opts?)` — constant-compass bearing (loxodrome)
- `rhumbDestination(origin, dist, bearing, opts?)` — rhumb-line destination
- `rhumbDistance(from, to, opts?)` — rhumb-line distance
- `square(bbox)` — smallest square bbox containing the input bbox

**Pick between `center` / `centerOfMass` / `centroid`:** `centroid` is fastest (vertex average) but skewed by vertex density. `centerOfMass` respects shape. `center` is just the bbox midpoint — useless for labeling oddly-shaped features.

## Coordinate Mutation

Reshape coordinates without changing the kind of feature.

- `cleanCoords(geojson)` — remove redundant collinear / duplicate vertices
- `flip(geojson)` — swap `[lon, lat]` → `[lat, lon]` (fix incorrectly-ordered data)
- `rewind(geojson, opts?)` — fix ring winding order to match GeoJSON RFC (CCW outer, CW holes)
- `round(num, precision?)` — round a single number
- `truncate(geojson, opts?)` — drop decimal places from coordinates (shrink payload)

## Transformation

Produce new geometry from input geometry.

- `bboxClip(feature, bbox)` — clip a feature to a bbox (rectangle crop)
- `bezierSpline(line, opts?)` — smooth a LineString with a Bezier curve
- `buffer(geojson, radius, opts?)` — expand/shrink geometry by `radius` (default units: **kilometers**)
- `circle(center, radius, opts?)` — approximate circle as a Polygon (`steps` controls smoothness)
- `clone(geojson)` — deep-clone (preserves bbox, id)
- `concave(points, opts?)` — concave hull (alpha-shape)
- `convex(features, opts?)` — convex hull
- `difference(features)` — polygon A minus B (input is a 2-feature `FeatureCollection<Polygon|MultiPolygon>`)
- `dissolve(features, opts?)` — merge touching polygons, optionally only when a property matches
- `intersect(features, opts?)` — polygonal intersection (input is `FeatureCollection<Polygon|MultiPolygon>`, **not** two args — v7 breaking change)
- `lineOffset(line, distance, opts?)` — offset a line by N units perpendicular
- `polygonSmooth(features, opts?)` — Chaikin-smooth polygon corners
- `simplify(geojson, opts?)` — Ramer-Douglas-Peucker simplification (`tolerance`, `highQuality`)
- `tesselate(polygon)` — triangulate a polygon into a FeatureCollection of triangles
- `transformRotate(features, angle, opts?)` — rotate around pivot
- `transformScale(features, factor, opts?)` — scale around an origin
- `transformTranslate(features, dist, bearing, opts?)` — move by distance + bearing
- `union(features, opts?)` — polygonal union (input is `FeatureCollection<Polygon|MultiPolygon>` — same v7 change as `intersect`)
- `voronoi(points, opts?)` — Voronoi diagram (returns a FeatureCollection of Polygon)

## Feature Conversion

Switch between geometry kinds and shapes of collection.

- `combine(features)` — group same-type Points/LineStrings/Polygons into Multi* features
- `explode(geojson)` — every coordinate becomes its own Point feature
- `flatten(geojson)` — `MultiPolygon` → many `Polygon` features (and similar)
- `lineToPolygon(line, opts?)` — close a ring of lines into a Polygon
- `polygonToLine(polygon)` — extract the polygon's boundary as LineString(s)
- `polygonize(lines)` — turn an arrangement of LineStrings into the Polygons they enclose

## Misc

The "everything else about lines and shapes" bucket — slicing, intersections, arcs, shortest paths.

- `kinks(line)` — find self-intersection points of a (multi)LineString
- `lineArc(center, radius, bearing1, bearing2, opts?)` — arc as a LineString
- `lineChunk(line, segmentLength, opts?)` — split a line into chunks of fixed length
- `lineIntersect(a, b)` — all intersection Points of two lines/polygons
- `lineOverlap(line1, line2, opts?)` — overlapping segments of two lines
- `lineSegment(geojson)` — explode any line/polygon into 2-vertex LineStrings
- `lineSlice(start, stop, line)` — slice a line between two points already on it
- `lineSliceAlong(line, startDist, stopDist, opts?)` — slice by distance, not points
- `lineSplit(line, splitter)` — split a line by any geometry that crosses it
- `mask(polygon, mask?)` — create a "hole punch" polygon (outer mask minus inner)
- `nearestPointOnLine(line, point, opts?)` — closest point ON the line to a reference point
- `sector(center, radius, b1, b2, opts?)` — pie-slice Polygon between two bearings
- `shortestPath(start, end, opts?)` — route around obstacle polygons
- `unkinkPolygon(polygon)` — split self-intersecting polygons into valid ones

## Helpers

Constructors. Use these to build GeoJSON safely (they set `type`, structure, validate ring closure, etc.) rather than hand-writing object literals.

- `feature(geom, props?, opts?)` — wrap a geometry in a Feature
- `featureCollection(features, opts?)` — wrap features in a FeatureCollection
- `geometryCollection(geometries, props?, opts?)` — build a GeometryCollection feature
- `lineString(coords, props?, opts?)` — `[[lon, lat], ...]` → LineString feature
- `multiLineString(coords, props?, opts?)`
- `multiPoint(coords, props?, opts?)`
- `multiPolygon(coords, props?, opts?)`
- `point(coord, props?, opts?)` — `[lon, lat]` → Point feature
- `polygon(rings, props?, opts?)` — outer ring + optional holes → Polygon feature (auto-closes if needed)

## Random

Generate synthetic geometry — useful for testing and demos, not for "I need real data".

- `randomLineString(count?, opts?)`
- `randomPoint(count?, opts?)`
- `randomPolygon(count?, opts?)`
- `randomPosition(bbox?)` — a single random `[lon, lat]` (Position, not Feature)

## Data

- `sample(featureCollection, num)` — return `num` features chosen at random (without replacement)

## Interpolation

Make continuous surfaces from scattered points, or contour lines from a grid.

- `interpolate(points, cellSize, opts?)` — IDW interpolation onto a grid
- `isobands(pointGrid, breaks, opts?)` — filled contour bands (Polygons) from a grid of points
- `isolines(pointGrid, breaks, opts?)` — contour lines (LineStrings) from a grid of points
- `planepoint(point, triangle)` — z-value of a point inside a triangle by linear interpolation
- `tin(points, z?)` — Triangulated Irregular Network from a set of points

## Joins

Spatial joins between points and polygons.

- `pointsWithinPolygon(points, polygons)` — return only the points that fall inside any of the polygons
- `tag(points, polygons, polyKey, outKey)` — for each point, copy a polygon property onto it (e.g., tag stops with their borough)

## Grids

Tessellate a bbox into a grid of cells.

- `hexGrid(bbox, cellSide, opts?)` — flat- or pointy-top hexagon grid
- `pointGrid(bbox, cellSide, opts?)` — grid of Point features
- `squareGrid(bbox, cellSide, opts?)`
- `triangleGrid(bbox, cellSide, opts?)`

## Classification

- `nearestPoint(target, points)` — find the closest Point from a FeatureCollection to a target Point. (For "closest point ON a line", use `nearestPointOnLine` in [Misc](#misc).)

## Aggregation

- `clustersDbscan(points, maxDistance, opts?)` — DBSCAN clustering (density-based; auto-discovers cluster count, marks noise)
- `clustersKmeans(points, opts?)` — K-means clustering (you specify `numberOfClusters`)
- `collect(polygons, points, inProp, outProp)` — gather a property from points into each containing polygon (e.g., list of zip codes within each county)

## Meta

Iteration / reduce helpers for traversing GeoJSON structure. Use these instead of writing recursive descent yourself.

- `clusterEach(fc, property, fn)` / `clusterReduce(fc, property, fn, init)` — iterate groups produced by clustering
- `coordAll(geojson)` — flat array of all `[lon, lat]` positions
- `coordEach(geojson, fn, excludeWrapCoord?)` — callback per coordinate
- `coordReduce(geojson, fn, init, excludeWrapCoord?)`
- `featureEach(featureCollection, fn)` / `featureReduce(...)`
- `flattenEach(geojson, fn)` / `flattenReduce(...)` — like `featureEach` but unwraps Multi* into singletons
- `geomEach(geojson, fn)` / `geomReduce(...)` — iterate raw Geometry objects
- `getCluster(fc, filter)` — pull out a specific cluster
- `getCoord(point)` / `getCoords(any)` — extract the coordinate array
- `getGeom(feature)` — extract the geometry from a Feature
- `getType(feature)` — `"Point"` / `"Polygon"` / etc. as a string
- `propEach(fc, fn)` / `propReduce(fc, fn, init)` — iterate properties
- `segmentEach(geojson, fn)` / `segmentReduce(...)` — iterate 2-vertex segments

## Assertions

Throw if input isn't the expected GeoJSON type. Use at function boundaries.

- `collectionOf(fc, type, name)` — assert FeatureCollection of a given geometry type
- `containsNumber(coords)` — sanity-check coordinate arrays
- `featureOf(feature, type, name)` — assert a single Feature's geometry type
- `geojsonType(value, type, name)` — assert any GeoJSON object's `type`

## Booleans

Predicates returning `true`/`false`. Useful for filters, validation, spatial queries.

- `booleanClockwise(line)` — is a ring clockwise?
- `booleanConcave(polygon)` — is the polygon concave (vs. convex)?
- `booleanContains(a, b)` — does A fully contain B?
- `booleanCrosses(a, b)` — do A and B cross (geometries of different dimension)?
- `booleanDisjoint(a, b)` — no shared points?
- `booleanEqual(a, b)` — same geometry, same coords (order-sensitive — use `booleanEqual` not `===`)
- `booleanIntersects(a, b)` — any shared points? (the "do they touch at all" check)
- `booleanOverlap(a, b)` — same-dimension overlap (interiors intersect but neither contains the other)
- `booleanParallel(line1, line2)` — are two LineStrings parallel?
- `booleanPointInPolygon(point, polygon, opts?)` — the classic; `ignoreBoundary` option available
- `booleanPointOnLine(point, line, opts?)`
- `booleanTouches(a, b)` — only boundaries touch, interiors disjoint
- `booleanWithin(a, b)` — is A fully within B? (inverse of `booleanContains`)

**Pick between predicates:** "does my point fall inside this region" → `booleanPointInPolygon`. "do these regions overlap at all" → `booleanIntersects`. "is region A fully inside region B" → `booleanWithin` (or `booleanContains` with args swapped).

## Unit Conversion

- `azimuthToBearing(az)` / `bearingToAzimuth(bearing)` — between 0..360 azimuth and -180..180 bearing
- `convertArea(value, from?, to?)` — between m², km², mi², acres, etc. (uses `AreaUnits`)
- `convertLength(value, from?, to?)` — between km, miles, meters, feet, etc. (uses `Units`)
- `degreesToRadians(deg)` / `radiansToDegrees(rad)`
- `lengthToDegrees(dist, units?)` — approximate (uses earth radius)
- `lengthToRadians(dist, units?)` / `radiansToLength(rad, units?)`
- `toMercator(geojson)` / `toWgs84(geojson)` — project between EPSG:4326 (WGS84 lon/lat) and EPSG:3857 (Web Mercator meters)

**`Units` enum (length):** `"meters" | "kilometers" | "miles" | "nauticalmiles" | "inches" | "yards" | "feet" | "centimeters" | "centimetres" | "metres" | "kilometres" | "millimeters" | "millimetres" | "radians" | "degrees"`. Note the British spellings work too.

## Other

The catch-all — spatial statistics, helpers that didn't fit elsewhere.

- `angle(startPoint, midPoint, endPoint, opts?)` — angle at `midPoint` between the other two
- `booleanValid(geojson)` — is this a valid GeoJSON geometry per the spec?
- `centerMean(features, opts?)` — mean-center (sensitive to outliers)
- `centerMedian(features, opts?)` — median-center (robust to outliers; iterative)
- `directionalMean(lines, opts?)` — average direction of a set of lines
- `distanceWeight(fc, opts?)` — spatial weights matrix for spatial-autocorrelation analyses
- `ellipse(center, xSemi, ySemi, opts?)` — ellipse Polygon
- `findPoint(fc, opts)` / `findSegment(fc, opts)` — locate a point/segment in a collection by index
- `geometry(type, coords, bbox?)` — build a raw Geometry object (rarely needed — prefer the typed helpers)
- `isNumber(x)` / `isObject(x)` — runtime type checks
- `lineEach(geojson, fn)` / `lineReduce(...)` — iterate LineStrings inside any geometry
- `lineStrings(coords, props?, opts?)` / `points(...)` / `polygons(...)` — bulk constructors → FeatureCollection
- `moranIndex(fc, opts?)` — Moran's I (global spatial autocorrelation)
- `nearestNeighborAnalysis(fc, opts?)` — average nearest-neighbor stats
- `nearestPointToLine(points, line, opts?)` — the point in a set closest to a line
- `pNormDistance(p1, p2, p?)` — p-norm distance (Euclidean if `p=2`)
- `quadratAnalysis(fc, opts?)` — quadrat counting for point-pattern analysis
- `rbush()` — wraps the [rbush](https://github.com/mourner/rbush) spatial index, GeoJSON-aware
- `rectangleGrid(bbox, w, h, opts?)` — non-square rectangles
- `standardDeviationalEllipse(fc, opts?)` — SDE for directional dispersion

---

## TypeScript usage

GeoJSON types from `@types/geojson` are the lingua franca; Turf's function signatures consume and produce them. Always type your inputs with the narrowest GeoJSON type that fits — Turf will narrow returns automatically.

```typescript
import * as turf from "@turf/turf";
import type {
  Feature,
  FeatureCollection,
  Point,
  Polygon,
  MultiPolygon,
  LineString,
} from "geojson";

interface StopProperties {
  id: string;
  routeId: string;
}

const stops: FeatureCollection<Point, StopProperties> = /* ... */;
const route: Feature<LineString> = /* ... */;

// `nearest` is correctly typed as Feature<Point, StopProperties>
const nearest = turf.nearestPoint(turf.point([-122.4, 37.8]), stops);

// `buffered` is Feature<Polygon | MultiPolygon>
const buffered = turf.buffer(route, 500, { units: "meters" });
```

For richer property typing, parameterize: `Feature<Polygon, MyProps>` and `FeatureCollection<Polygon, MyProps>`.

See `references/typescript-patterns.md` for narrower patterns: type guards on geometry kind, casting strategies for `intersect`/`union` (which lose property types), and generic wrappers that preserve property types through pipelines.

## Common foot-guns

Read `references/foot-guns.md` for the long form. The greatest hits:

1. **`buffer` defaults to kilometers.** `turf.buffer(point, 100)` is 100 km, not 100 m. Always pass `{ units: "meters" }` if you mean meters.
2. **v7 `intersect` / `union` / `difference` take a `FeatureCollection`, not two args.** Old v6 examples on Stack Overflow show `turf.intersect(a, b)` — that throws in v7. Wrap with `turf.featureCollection([a, b])`.
3. **Coordinates are `[lon, lat]`, not `[lat, lon]`.** Easy to flip if you copy from a service that returns the other order. Use `turf.flip(...)` to fix in bulk.
4. **`buffer` may return `undefined`** for degenerate inputs (negative radius too large, etc.). Type narrowing in strict TS will force you to handle this.
5. **GeoJSON types are NOT exported by Turf.** `import { Polygon } from "@turf/turf"` won't work — import from `geojson` (`@types/geojson`).
6. **Ring winding matters.** GeoJSON RFC 7946 wants CCW outer rings, CW holes. If a polygon "looks inverted" in some renderers or `area` is negative, `rewind` it.
7. **`length` is for LineStrings, `distance` is for two points.** Confusing them is the #1 wrong-tool error.

## When you need more depth

- `references/foot-guns.md` — all the version differences, signature changes between v6 → v7, and silent-failure modes
- `references/typescript-patterns.md` — strict typing recipes, generic helpers, `interface` patterns for properties
- `references/function-index.md` — flat alphabetical lookup of every function with full signature and npm package name (handy when you know the name and just need the import)
- `references/categories/measurement.md` — picking between centroid / center / centerOfMass; great-circle vs rhumb; units defaults
- `references/categories/transformation.md` — set operations in v7, buffer specifics, simplify topology pitfalls, worked union/intersect pipelines
- `references/categories/booleans.md` — decision tree for picking the right predicate, the DE-9IM relations behind them
- `references/categories/meta.md` — when to use `coordEach` vs `featureEach` vs `flattenEach`, performance notes
- `references/categories/joins.md` — typed patterns for points-in-region tagging, multi-polygon scenarios
- `references/categories/aggregation.md` — DBSCAN vs k-means picking, what `collect` actually does

When picking a function, the heuristic is: **search by task verb in the table above, then scan the category section for the narrowest fit, then check `references/foot-guns.md` if the function involves units, polygon operations, or anything that changed between v6 and v7. For the heavier categories (measurement, transformation, booleans, meta, joins, aggregation), the per-category deep dives include decision trees and worked examples that resolve close calls.**
