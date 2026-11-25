---
name: trigonometry
description: Apply trigonometry to creative coding, graphics, and animation — including angles, rotations, oscillations, orbits, and wave functions using sine and cosine. Use this skill whenever the user wants to move something in a circle, create a wave or pulse effect, animate orbiting objects, rotate shapes or vectors, calculate angles between points, build a compass or dial, or implement any repeating/periodic motion. Also triggers on "make it spin", "orbit around", "bouncing/bobbing animation", "figure out the angle", "point toward the cursor", "spiral path", "pendulum", "breathing effect", "ripple", "polar coordinates", or any time math.sin / math.cos appears in context. Covers 2D and 3D graphics applications.
---

# Trigonometry for Creative Coding & Graphics

Trigonometry is the backbone of spatial math in code. Whenever something moves in an arc,
rotates, oscillates, or needs to "know" where it is on a circle, you're doing trig.

---

## The Essentials (Radians First)

JavaScript's `Math.sin()`, `Math.cos()`, and `Math.atan2()` — and their equivalents
in Python, GLSL, WGSL, and p5.js — all work in **radians**, not degrees.

| Concept | Formula |
|---|---|
| Degrees → Radians | `rad = deg * (Math.PI / 180)` |
| Radians → Degrees | `deg = rad * (180 / Math.PI)` |
| Full circle | `2 * Math.PI` (~6.283) |
| Half circle | `Math.PI` (~3.14159) |
| Quarter circle | `Math.PI / 2` (~1.5708) |

**One intuition to anchor everything:** Imagine the unit circle — a circle with radius 1
centred at the origin. For any angle θ, the point on that circle is `(cos θ, sin θ)`.
That's it. Everything else is scaling.

---

## Core Functions

### sin and cos — the circular pair

```js
// Position of a point on a circle of radius r, at angle theta
const x = cx + r * Math.cos(theta);
const y = cy + r * Math.sin(theta);
```

- `cos` drives **horizontal** (x-axis) position
- `sin` drives **vertical** (y-axis) position
- Both return values between −1 and 1
- They are **90° out of phase** with each other — which is why they combine to trace a circle

### atan2 — measure angle from a vector

```js
// Angle from point A to point B (result in radians)
const angle = Math.atan2(B.y - A.y, B.x - A.x);
```

Always use `atan2(y, x)` — not `atan(y/x)` — because `atan2` handles all four quadrants
and avoids division-by-zero. Note the argument order: **y first, then x**.

### tan — the ratio

`tan(θ) = sin(θ) / cos(θ)` — rarely used directly in graphics; more useful for
computing angles from side ratios.

---

## Key Identities for Graphics

You don't need to memorise all trig identities. These are the ones that come up in code:

| Identity | Use in code |
|---|---|
| `sin²θ + cos²θ = 1` | Keep a point on the unit circle; normalise a direction vector |
| `sin(−θ) = −sin(θ)` | Flip vertical oscillation |
| `cos(−θ) = cos(θ)` | Cosine is symmetric — mirror motion horizontally |
| `sin(θ + π/2) = cos(θ)` | Convert between sine and cosine wave |
| `sin(2θ) = 2 sin(θ) cos(θ)` | Frequency doubling |
| `cos(A+B) = cosA cosB − sinA sinB` | Rotation matrix derivation |

---

## Trigonometry Table (Common Angles)

| Angle (deg) | Radians | sin | cos | tan |
|---|---|---|---|---|
| 0° | 0 | 0 | 1 | 0 |
| 30° | π/6 | 0.5 | √3/2 ≈ 0.866 | 1/√3 ≈ 0.577 |
| 45° | π/4 | √2/2 ≈ 0.707 | √2/2 ≈ 0.707 | 1 |
| 60° | π/3 | √3/2 ≈ 0.866 | 0.5 | √3 ≈ 1.732 |
| 90° | π/2 | 1 | 0 | ∞ |
| 180° | π | 0 | −1 | 0 |
| 270° | 3π/2 | −1 | 0 | ∞ |
| 360° | 2π | 0 | 1 | 0 |

---

## 2D Graphics Patterns

### Circular / Orbital Motion

Move an object along a circle around a centre point:

```js
// In an animation loop — t increases over time
const speed = 0.02;  // radians per frame
const radius = 100;

function update(t) {
  const x = cx + radius * Math.cos(t * speed);
  const y = cy + radius * Math.sin(t * speed);
  // draw object at (x, y)
}
```

For **elliptical** orbits, use different radii for x and y:

```js
const x = cx + rx * Math.cos(angle);
const y = cy + ry * Math.sin(angle);
```

For **offset phase** (multiple moons, staggered orbits):

```js
const phaseOffset = (i / totalObjects) * Math.PI * 2;
const x = cx + r * Math.cos(angle + phaseOffset);
const y = cy + r * Math.sin(angle + phaseOffset);
```

### Oscillation / Wave Motion

The sine wave is the most natural oscillator — smooth, bounded, periodic:

```js
// Vertical bob — oscillates between (cy - amplitude) and (cy + amplitude)
const y = cy + amplitude * Math.sin(time * frequency);

// Horizontal sweep
const x = cx + amplitude * Math.cos(time * frequency);

// Combined: Lissajous figure
const x = cx + rx * Math.cos(time * freqX);
const y = cy + ry * Math.sin(time * freqY);
```

**Breathing / pulsing size:**
```js
const scale = 1 + 0.2 * Math.sin(time * 2);  // pulses ±20%
```

**Pendulum swing:**
```js
const angle = maxAngle * Math.cos(time * Math.sqrt(g / length));
const x = pivotX + length * Math.sin(angle);
const y = pivotY + length * Math.cos(angle);
```

### Sprite / Object Rotation

Point an object toward a target (e.g., a character facing the mouse):

```js
const angle = Math.atan2(target.y - self.y, target.x - self.x);
// In p5.js:
rotate(angle);
// In canvas 2D:
ctx.rotate(angle);
```

Rotate a point around an origin:

```js
function rotatePoint(px, py, cx, cy, angle) {
  const dx = px - cx, dy = py - cy;
  return {
    x: cx + dx * Math.cos(angle) - dy * Math.sin(angle),
    y: cy + dx * Math.sin(angle) + dy * Math.cos(angle)
  };
}
```

### Polar Coordinates

Convert between polar `(r, θ)` and Cartesian `(x, y)`:

```js
// Polar → Cartesian
const x = r * Math.cos(theta);
const y = r * Math.sin(theta);

// Cartesian → Polar
const r = Math.sqrt(x * x + y * y);
const theta = Math.atan2(y, x);
```

**Spiral (Archimedean):** radius grows with angle

```js
for (let theta = 0; theta < Math.PI * 10; theta += 0.1) {
  const r = spacing * theta;
  const x = cx + r * Math.cos(theta);
  const y = cy + r * Math.sin(theta);
  // plot point
}
```

**Rose curve:** `r = cos(k * theta)`

```js
for (let theta = 0; theta < Math.PI * 2; theta += 0.01) {
  const r = amplitude * Math.cos(k * theta);
  const x = cx + r * Math.cos(theta);
  const y = cy + r * Math.sin(theta);
}
```

### Distance and Angle Between Points

```js
// Distance
const dist = Math.sqrt((bx - ax) ** 2 + (by - ay) ** 2);
// Or using hypot:
const dist = Math.hypot(bx - ax, by - ay);

// Angle from A to B
const angle = Math.atan2(by - ay, bx - ax);

// Normalised direction vector (unit vector)
const nx = (bx - ax) / dist;
const ny = (by - ay) / dist;
```

---

## 3D Graphics Patterns

In 3D, trig underpins rotation matrices, spherical coordinates, and camera math.

### Spherical Coordinates → Cartesian (3D Point on a Sphere)

Given latitude (phi, φ) and longitude (theta, θ) on a sphere of radius r:

```js
// φ: polar angle from the +Y axis (0 = top, π = bottom) — also called "inclination"
// θ: azimuthal angle around the Y axis
const x = r * Math.sin(phi) * Math.cos(theta);
const y = r * Math.cos(phi);
const z = r * Math.sin(phi) * Math.sin(theta);
```

Use this for: planet surfaces, star fields, distributing points on a globe, skybox sampling.

### Rotation Matrices

Rotation in 3D is performed by multiplying a point by a rotation matrix. Each matrix
rotates around one axis. These are derived directly from sin/cos identities.

**Rotate around Z-axis (2D equivalent in 3D):**
```
| cos θ  -sin θ  0 |
| sin θ   cos θ  0 |
|  0       0     1 |
```

```js
function rotateZ(x, y, z, angle) {
  return {
    x: x * Math.cos(angle) - y * Math.sin(angle),
    y: x * Math.sin(angle) + y * Math.cos(angle),
    z: z
  };
}
```

**Rotate around X-axis:**
```js
function rotateX(x, y, z, angle) {
  return {
    x: x,
    y: y * Math.cos(angle) - z * Math.sin(angle),
    z: y * Math.sin(angle) + z * Math.cos(angle)
  };
}
```

**Rotate around Y-axis:**
```js
function rotateY(x, y, z, angle) {
  return {
    x: x * Math.cos(angle) + z * Math.sin(angle),
    y: y,
    z: -x * Math.sin(angle) + z * Math.cos(angle)
  };
}
```

When using Three.js or a similar library, prefer `object.rotation.set(x, y, z)` or
quaternions for composing rotations — chaining raw matrices introduces gimbal lock.

### Gimbal Lock and Quaternions

Euler angles (combining X, Y, Z rotations in sequence) suffer from **gimbal lock** —
when two axes align, a degree of freedom is lost and rotations collapse into 2D.
For smooth 3D rotation, use quaternions via `THREE.Quaternion` or equivalent.

```js
// Three.js: rotate toward a target using quaternions
const quaternion = new THREE.Quaternion();
quaternion.setFromEuler(new THREE.Euler(rx, ry, rz, 'XYZ'));
mesh.quaternion.slerp(targetQuaternion, 0.1); // smooth interpolation
```

### 3D Orbital Path

Orbit a point around the Y-axis at height `h`:

```js
function orbitY(cx, h, cz, radius, angle) {
  return {
    x: cx + radius * Math.cos(angle),
    y: h,
    z: cz + radius * Math.sin(angle)
  };
}
```

For a tilted orbit (inclined orbital plane), rotate the points after computing the flat orbit.

### GLSL / Shader Trig

In GLSL shaders (WebGL/Three.js ShaderMaterial), the same functions apply but without
the `Math.` prefix:

```glsl
// Fragment shader: radial gradient ring
float dist = length(uv - vec2(0.5));
float ring = sin(dist * 20.0 - uTime * 2.0); // animated ripple
gl_FragColor = vec4(vec3(ring), 1.0);

// Rotate UV coordinates around centre
float c = cos(uAngle);
float s = sin(uAngle);
vec2 rotatedUV = vec2(
  c * (uv.x - 0.5) - s * (uv.y - 0.5) + 0.5,
  s * (uv.x - 0.5) + c * (uv.y - 0.5) + 0.5
);
```

### Camera Orbit (Three.js / WebGL)

Classic spherical camera controller:

```js
// Orbit camera around target
camera.position.x = target.x + radius * Math.sin(phi) * Math.cos(theta);
camera.position.y = target.y + radius * Math.cos(phi);
camera.position.z = target.z + Math.sin(phi) * Math.sin(theta);
camera.lookAt(target);
```

---

## Compound and Advanced Patterns

### Layered Oscillations (Noise-like motion)

Stack sine waves with different frequencies and amplitudes to break the mechanical feel:

```js
function noisyOscillation(t) {
  return (
    0.5 * Math.sin(t * 1.0) +
    0.25 * Math.sin(t * 2.3 + 1.1) +
    0.125 * Math.sin(t * 5.1 + 2.4)
  );
}
```

### Easing with Sine

Smooth start-stop using the sine curve's S-shape:

```js
// t goes from 0 to 1
const eased = 0.5 - 0.5 * Math.cos(t * Math.PI); // ease in-out
const easeIn = Math.sin(t * Math.PI / 2);          // ease in
const easeOut = 1 - Math.cos(t * Math.PI / 2);     // ease out
```

### Lerp Angle (Shortest Arc)

When linearly interpolating between angles, always take the shortest arc:

```js
function lerpAngle(a, b, t) {
  let diff = ((b - a + Math.PI) % (Math.PI * 2)) - Math.PI;
  return a + diff * t;
}
```

### Wrap Angle

Keep an angle in the range [0, 2π] or [-π, π]:

```js
const wrapped = ((angle % (Math.PI * 2)) + Math.PI * 2) % (Math.PI * 2); // [0, 2π]
const signed = Math.atan2(Math.sin(angle), Math.cos(angle));               // [-π, π]
```

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Using degrees with `Math.sin()` | Convert to radians first: `angle * Math.PI / 180` |
| `atan(y/x)` instead of `atan2(y, x)` | `atan2` handles all quadrants and avoids divide-by-zero |
| Y-axis is inverted in canvas/SVG | In screen space, Y increases downward — `sin` produces downward motion by default |
| Gimbal lock in 3D Euler rotations | Use quaternions for 3D rotation composition |
| Circular motion looks like a line | You swapped sin/cos or used the same function for both x and y |

---

## Quick Reference

| Task | Code |
|---|---|
| Point on circle | `x = cx + r * cos(θ)`, `y = cy + r * sin(θ)` |
| Object facing target | `angle = atan2(dy, dx)` |
| Oscillate | `val = centre + amplitude * sin(time * freq)` |
| Rotate point 2D | `x' = cos(θ)·x - sin(θ)·y`, `y' = sin(θ)·x + cos(θ)·y` |
| Sphere point (3D) | `x = r·sin(φ)·cos(θ)`, `y = r·cos(φ)`, `z = r·sin(φ)·sin(θ)` |
| Distance | `Math.hypot(dx, dy)` |
| Angle wrap [-π, π] | `Math.atan2(Math.sin(a), Math.cos(a))` |
| Degrees to radians | `deg * Math.PI / 180` |
| Sine ease in-out | `0.5 - 0.5 * Math.cos(t * Math.PI)` |

---

## Resources

- [Trigonometric Cheat Sheet — GeeksforGeeks](https://www.geeksforgeeks.org/maths/trigonometric-cheat-sheet/)
- [Trigonometry Index — Math is Fun](https://www.mathsisfun.com/algebra/trigonometry-index.html)
- [Interactive Unit Circle — Math is Fun](https://www.mathsisfun.com/algebra/trig-interactive-unit-circle.html)

## Related Skills

- **Geometry** — Triangle properties, polygon collision, line intersections, and spatial partitioning. Use geometry when you need to detect collisions, find intersection points, calculate angles within shapes, or tessellate surfaces.
- **Linear Algebra** — Vectors, matrices, dot products, and cross products. Essential for 3D transformations, lighting calculations, physics simulations, and any operation involving direction or magnitude.
- **Physics** — Velocity, acceleration, forces, collisions, and dynamics. Use physics when you need to simulate motion with momentum, apply forces to objects, handle gravity and friction, or model realistic interactions between bodies.

