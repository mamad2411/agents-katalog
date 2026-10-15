---
name: geometry
description: Apply Euclidean geometry to game development, rendering, and simulation — covering planes, line-plane intersections, raycasting, collision detection, bounding volumes, vectors, normals, and spatial tests. Use this skill whenever the user is working on hit detection, physics, ray-vs-mesh intersection, frustum culling, overlap tests, AABB, OBB, sweep tests, point-in-triangle, closest-point queries, or any spatial math that powers a game, physics engine, or renderer. Also triggers on "check if the ray hits", "plane equation", "find the normal of a face", "where does the line cross", "is this point inside", "detect collision", "bounding box overlap", "distance from point to plane", and any context involving vectors, dot products, cross products, or coordinate geometry applied to real-time systems.
---

# Geometry for Games, Rendering & Simulation

Geometry in code is about answering spatial questions precisely and quickly: Does this ray hit that triangle? Are these two boxes overlapping? Which side of a plane is this point on? This skill covers the Euclidean geometry that drives collision, rendering, and physics systems.

---

## Euclidean Fundamentals

### The Building Blocks

| Primitive | Definition in code |
|---|---|
| **Point** | A position: `{x, y, z}` — no size, no direction |
| **Vector** | A displacement or direction: `{x, y, z}` — no fixed position |
| **Line** | `P(t) = origin + t * direction` — infinite, parametric |
| **Ray** | Same as a line but `t ≥ 0` — has a start, extends forever |
| **Segment** | `P(t) = A + t * (B - A)`, `t ∈ [0, 1]` — bounded both ends |
| **Plane** | All points satisfying `dot(N, P) = d` — infinite flat surface |
| **Triangle** | Three vertices A, B, C — the workhorse of 3D meshes |

The distinction between a *point* and a *vector* matters even though they both have xyz components. Points describe where something is; vectors describe how to get there. Confusing them leads to transform bugs (a point translates; a direction vector should not).

---

## Vectors — The Core Tool

### Essential Operations

```js
// Dot product — measures alignment; result is a scalar
function dot(a, b) { return a.x*b.x + a.y*b.y + a.z*b.z; }

// Cross product — produces a vector perpendicular to both inputs
function cross(a, b) {
  return {
    x: a.y*b.z - a.z*b.y,
    y: a.z*b.x - a.x*b.z,
    z: a.x*b.y - a.y*b.x
  };
}

// Length (magnitude)
function length(v) { return Math.sqrt(dot(v, v)); }

// Normalise — make unit length (length = 1)
function normalise(v) {
  const len = length(v);
  return { x: v.x/len, y: v.y/len, z: v.z/len };
}

function sub(a, b)  { return { x: a.x-b.x, y: a.y-b.y, z: a.z-b.z }; }
function add(a, b)  { return { x: a.x+b.x, y: a.y+b.y, z: a.z+b.z }; }
function scale(v, s){ return { x: v.x*s,   y: v.y*s,   z: v.z*s   }; }
```

### What the Dot Product Tells You

`dot(A, B) = |A| |B| cos(θ)` — for **unit vectors**, this equals the cosine of the angle between them.

| Value | Meaning |
|---|---|
| `dot > 0` | Vectors point in roughly the same direction (angle < 90°) |
| `dot = 0` | Perpendicular |
| `dot < 0` | Vectors point away from each other (angle > 90°) |
| `dot = 1` | Identical directions (unit vectors) |
| `dot = -1` | Opposite directions (unit vectors) |

This makes dot the fast test for: "Is the camera facing this surface?", "Is this enemy in front of the player?", "Is this face lit?"

### What the Cross Product Gives You

`cross(A, B)` gives a vector perpendicular to both, with magnitude `|A| |B| sin(θ)`.

- **Face normal:** `cross(B - A, C - A)` for triangle ABC
- **Winding order check:** cross product direction tells you CW vs CCW
- **Triangle area:** `length(cross(B - A, C - A)) / 2`

---

## Planes

A plane divides space into two half-spaces. It is defined by a **normal** (unit vector perpendicular to it) and a **signed distance from the origin**:

```
Plane equation: dot(N, P) - d = 0
```

- `dot(N, P) - d > 0` → point P is in front of the plane
- `dot(N, P) - d < 0` → point P is behind the plane
- `dot(N, P) - d = 0` → point P is on the plane

### Computing a Plane from Three Points

```js
function planeFromPoints(a, b, c) {
  const normal = normalise(cross(sub(b, a), sub(c, a)));
  const d = dot(normal, a);
  return { normal, d };
}
```

### Signed Distance from a Point to a Plane

```js
function signedDist(plane, point) {
  return dot(plane.normal, point) - plane.d;
}
```

Used in frustum culling, portal rendering, BSP trees, and contact manifold generation. Positive = in front; negative = behind; absolute value = shortest distance.

---

## Raycasting

A ray is `P(t) = origin + t * direction` with `t ≥ 0`. The goal is finding the smallest positive `t` where the ray hits something.

### Ray vs. Plane

```js
function rayPlane(rayOrigin, rayDir, plane) {
  const denom = dot(plane.normal, rayDir);
  if (Math.abs(denom) < 1e-6) return null;  // parallel
  const t = (plane.d - dot(plane.normal, rayOrigin)) / denom;
  return t >= 0 ? t : null;
}
```

### Ray vs. Triangle (Möller–Trumbore)

The standard algorithm for mesh intersection. Uses barycentric coordinates to confirm the hit is inside the triangle.

```js
function rayTriangle(orig, dir, A, B, C) {
  const EPSILON = 1e-8;
  const edge1 = sub(B, A);
  const edge2 = sub(C, A);
  const h = cross(dir, edge2);
  const a = dot(edge1, h);
  if (Math.abs(a) < EPSILON) return null;  // parallel

  const f = 1.0 / a;
  const s = sub(orig, A);
  const u = f * dot(s, h);
  if (u < 0 || u > 1) return null;

  const q = cross(s, edge1);
  const v = f * dot(dir, q);
  if (v < 0 || u + v > 1) return null;

  const t = f * dot(edge2, q);
  return t > EPSILON ? { t, u, v } : null;
}
```

The returned `u` and `v` are barycentric coordinates for interpolating vertex attributes (UVs, normals, colours) at the hit point:

```js
const w = 1 - u - v;
const interp = add(add(scale(attrA, w), scale(attrB, u)), scale(attrC, v));
```

### Ray vs. Sphere

```js
function raySphere(orig, dir, centre, radius) {
  const oc = sub(orig, centre);
  const b = dot(oc, dir);
  const c = dot(oc, oc) - radius * radius;
  const disc = b * b - c;
  if (disc < 0) return null;
  const t = -b - Math.sqrt(disc);
  return t >= 0 ? t : (-b + Math.sqrt(disc) >= 0 ? -b + Math.sqrt(disc) : null);
}
```

### Ray vs. AABB (Slab Method)

```js
function rayAABB(orig, dir, min, max) {
  let tmin = -Infinity, tmax = Infinity;
  for (const axis of ['x', 'y', 'z']) {
    if (Math.abs(dir[axis]) < 1e-8) {
      if (orig[axis] < min[axis] || orig[axis] > max[axis]) return null;
    } else {
      const invD = 1 / dir[axis];
      let t1 = (min[axis] - orig[axis]) * invD;
      let t2 = (max[axis] - orig[axis]) * invD;
      if (t1 > t2) [t1, t2] = [t2, t1];
      tmin = Math.max(tmin, t1);
      tmax = Math.min(tmax, t2);
      if (tmin > tmax) return null;
    }
  }
  return tmin >= 0 ? tmin : (tmax >= 0 ? tmax : null);
}
```

---

## Collision Detection

### Point Tests

**Point inside AABB:**
```js
function pointInAABB(p, min, max) {
  return p.x >= min.x && p.x <= max.x &&
         p.y >= min.y && p.y <= max.y &&
         p.z >= min.z && p.z <= max.z;
}
```

**Point inside sphere (use squared distance — avoids `sqrt`):**
```js
function pointInSphere(p, centre, radius) {
  const d = sub(p, centre);
  return dot(d, d) <= radius * radius;
}
```

**Point inside triangle (2D):**
```js
function pointInTriangle2D(p, A, B, C) {
  function sign(p1, p2, p3) {
    return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y);
  }
  const d1 = sign(p, A, B), d2 = sign(p, B, C), d3 = sign(p, C, A);
  const hasNeg = (d1 < 0) || (d2 < 0) || (d3 < 0);
  const hasPos = (d1 > 0) || (d2 > 0) || (d3 > 0);
  return !(hasNeg && hasPos);
}
```

### AABB vs. AABB Overlap

```js
function aabbOverlap(minA, maxA, minB, maxB) {
  return minA.x <= maxB.x && maxA.x >= minB.x &&
         minA.y <= maxB.y && maxA.y >= minB.y &&
         minA.z <= maxB.z && maxA.z >= minB.z;
}
```

Two AABBs overlap only when they overlap on **all three axes simultaneously** — this is the Separating Axis Theorem (SAT) for axis-aligned boxes.

### Sphere vs. Sphere

```js
function sphereOverlap(centreA, rA, centreB, rB) {
  const d = sub(centreA, centreB);
  return dot(d, d) <= (rA + rB) * (rA + rB);
}
```

### Closest Point on a Segment to a Point

Foundational for capsule colliders, rope segments, and distance queries:

```js
function closestPointOnSegment(A, B, P) {
  const AB = sub(B, A);
  const t = dot(sub(P, A), AB) / dot(AB, AB);
  return add(A, scale(AB, Math.max(0, Math.min(1, t))));
}
```

### Separating Axis Theorem (SAT)

Two convex shapes do **not** overlap if there exists any axis along which their projections don't overlap. Test all candidate axes and return false the moment you find a separating one; if none separates them, they intersect.

For OBBs the 15 candidate axes are: 3 face normals of A + 3 face normals of B + 9 edge cross products.

---

## Normals, Winding, and Backface Culling

### Face Normal

```js
function faceNormal(A, B, C) {
  return normalise(cross(sub(B, A), sub(C, A)));
}
```

Vertex winding order determines which side is "front":
- **CCW:** front face in OpenGL / WebGL default
- **CW:** front face in Direct3D / Metal default

### Backface Culling

```js
// viewDir points FROM the camera TOWARD the surface
function isFrontFacing(normal, viewDir) {
  return dot(normal, viewDir) < 0;
}
```

If `dot(normal, cameraToSurface) >= 0`, the face points away — skip drawing it.

### Reflecting a Vector

```js
// incident points toward the surface; normal points away
function reflect(incident, normal) {
  return sub(incident, scale(normal, 2 * dot(incident, normal)));
}
```

---

## Coordinate Systems and Transforms

### Local vs. World Space

Every object has a **local** coordinate system and lives somewhere in **world** space. Converting between them requires a transform matrix (or position + rotation + scale).

Key rule when transforming normals: use the **inverse-transpose** of the model matrix. Normals are not position vectors — they transform differently.

### Perspective Projection (3D → 2D)

```
screenX = (point.x / -point.z) * focalLength
screenY = (point.y / -point.z) * focalLength
```

`focalLength = 1 / tan(fovY / 2)`. In a right-handed coordinate system the camera looks down -Z, hence the negation.

### Homogeneous Coordinates

In 4D homogeneous space: a **point** is `(x, y, z, w=1)`, a **direction** is `(x, y, z, w=0)`. The `w` component makes matrix translation possible and encodes the point/direction distinction so direction vectors are never incorrectly translated.

---

## Frustum Culling

A frustum is six planes (near, far, left, right, top, bottom). An object can be culled if it is entirely on the wrong side of any single plane:

```js
function sphereInFrustum(planes, centre, radius) {
  for (const plane of planes) {
    if (signedDist(plane, centre) < -radius) return false;  // fully outside
  }
  return true;
}
```

Extract frustum planes from the view-projection matrix using the Gribb/Hartmann method.

---

## Distances

```js
// 2D
const d2 = Math.hypot(bx - ax, by - ay);

// 3D
const d3 = Math.hypot(bx - ax, by - ay, bz - az);

// Prefer squared distance for comparisons — avoids sqrt entirely
const distSq = (bx-ax)**2 + (by-ay)**2 + (bz-az)**2;
```

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Normalising a zero-length vector | Guard: `if (length(v) < 1e-8) return fallback` |
| Forgetting `t ≥ 0` in ray tests | Negative `t` means the hit is behind the ray origin |
| Raw dot product for angle comparison | Normalise both vectors first |
| Unnormalised plane normal | Breaks signed-distance calculations |
| Transforming normals with the model matrix | Use the inverse-transpose |
| AABB test with `<` not `<=` | Touching surfaces should count as overlapping in physics |
| Euler angles for smooth 3D rotation | Use quaternions to avoid gimbal lock |

---

## Quick Reference

| Query | Pattern |
|---|---|
| Face normal | `normalise(cross(B−A, C−A))` |
| Signed distance to plane | `dot(N, P) − d` |
| Ray hits plane at | `t = (d − dot(N, orig)) / dot(N, dir)` |
| Point on ray | `orig + t * dir` |
| AABB overlap | All 3 axis intervals overlap |
| Sphere overlap | `distSq ≤ (rA + rB)²` |
| Backface cull | `dot(N, camToSurf) ≥ 0` → skip |
| Reflect vector | `I − 2·dot(I,N)·N` |
| Closest point on segment | Clamp `t = dot(P−A, B−A) / |B−A|²` to [0,1] |
| Interpolate at hit | Barycentric coords `(u, v, 1−u−v)` from ray-triangle |

---

## Resources

- [Geometry — Math is Fun](https://www.mathsisfun.com/geometry/)
- [Solid Geometry — Math is Fun](https://www.mathsisfun.com/geometry/solid-geometry.html)
- [Pythagoras in 3D — Math is Fun](https://www.mathsisfun.com/geometry/pythagoras-3d.html)

## Related Skills

- **linear-algebra** — vectors, matrices, transformations, and systems of equations that underpin all spatial math
- **trigonometry** — angles, orbits, rotations, and sin/cos in 2D/3D space
- **physics** — velocity, acceleration, forces, and dynamics that build on geometry for realistic motion and interactions
