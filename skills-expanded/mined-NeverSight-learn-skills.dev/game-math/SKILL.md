---
name: game-math
description: Advanced mathematics for game development, graphics programming, and generative art — covering vectors, matrices, coordinate spaces, rotation (quaternions, Euler angles), geometric primitives, polar/spherical coordinates, kinematics, rigid-body physics, and parametric curves. Use this skill whenever the user asks about 2D/3D math, transformations, coordinate spaces, camera systems, rotation representation, raycasting, collision geometry, physics simulation, animation curves, or procedural geometry. Also triggers on "how do I rotate", "transform this vector", "gimbal lock", "quaternion slerp", "bézier curve", "perspective projection", "dot product", "world space vs local space", and any context involving graphics pipeline math.
---

# Game & Graphics Math

Deep, actionable guidance on the mathematics that drives games, real-time graphics, and generative art — from position and direction to full rendering pipelines and physics simulation.

For specialised deep-dives, see the **Related Skills** section at the bottom of this file.

## Topics

### 1. Cartesian Coordinate Systems
**Explanation**: 1D, 2D, and 3D spaces using perpendicular axes (x, y, z). Used for positioning, movement, and rendering in almost all games and graphics engines.
**When to Use**: Any time you need to represent or manipulate positions, directions, or distances.
**Example**:
- 2D: `position = (x, y)`
- 3D: `position = (x, y, z)`

### 2. Vectors
**Explanation**: Quantities with both magnitude and direction. Support operations like addition, subtraction, scaling, dot/cross products.
**When to Use**: Movement, forces, normals, directions, lighting, and more.
**Example**:
- Addition: `v3 = v1 + v2`
- Dot product: `v1 · v2` (angle/cosine, projection)
- Cross product: `v1 × v2` (perpendicular vector in 3D)

### 3. Multiple Coordinate Spaces
**Explanation**: Transforming between world, object, camera, and screen spaces using basis vectors and transformation matrices.
**When to Use**: Rendering pipelines, hierarchical models, camera movement.
**Example**:
- World to camera: `cameraMatrix * worldPosition`

### 4. Introduction to Matrices
**Explanation**: Rectangular arrays of numbers for representing linear transformations (rotation, scaling, translation).
**When to Use**: Chaining multiple transformations, animating, projecting, or rotating objects.
**Example**:
- 2D rotation: `R = [[cosθ, -sinθ], [sinθ, cosθ]]`
- Matrix multiplication: `M * v`

### 5. Matrices and Linear Transformations
**Explanation**: Use matrices to perform rotation, scaling, projection, reflection, shearing, and combine them efficiently.
**When to Use**: Animating, simulating, or rendering objects in 2D/3D.
**Example**:
- Combine: `M = T * R * S` (translate, rotate, scale)
- Orthographic projection: flattening 3D to 2D

### 6. More on Matrices
**Explanation**: Determinants (invertibility), matrix inversion (undoing transforms), orthogonal matrices (pure rotation), 4x4 homogeneous matrices (for 3D with translation), perspective projection.
**When to Use**: Camera/view transforms, undoing transforms, perspective rendering.
**Example**:
- Inverse: `M_inv = inverse(M)`
- Perspective: `P * v` (project 3D to 2D)

### 7. Polar Coordinate Systems
**Explanation**: 2D polar (r, θ), 3D cylindrical/spherical coordinates. Useful for circular motion, orbits, and procedural effects.
**When to Use**: Spirals, orbits, radial gradients, mapping textures to spheres.
**Example**:
- Convert: `x = r * cosθ, y = r * sinθ`
- Spherical: `(ρ, θ, φ)`

### 8. Rotation in Three Dimensions
**Explanation**: Representing orientation with matrices, Euler angles, axis-angle, and quaternions. Each has tradeoffs for interpolation, gimbal lock, and performance.
**When to Use**: 3D camera, object rotation, smooth interpolation (slerp), avoiding gimbal lock.
**Example**:
- Quaternion: `q = (w, x, y, z)`
- Euler to quaternion conversion

> **Watch out**: Euler angles suffer from gimbal lock when two rotation axes align. Prefer quaternions for smooth 3D interpolation (`slerp`). Always clarify coordinate-system handedness (right-handed vs left-handed) before combining transforms from different sources.

### 9. Geometric Primitives
**Explanation**: Mathematical representations of lines, rays, spheres, AABBs, planes, triangles, polygons. Used for collision, rendering, and spatial queries.
**When to Use**: Raycasting, hit detection, mesh generation, bounding volumes.
**Example**:
- Ray-sphere intersection
- AABB overlap test

### 10. Mathematical Topics from 3D Graphics
**Explanation**: The graphics pipeline, mesh representation, texture mapping, lighting models, and animation basics.
**When to Use**: Rendering, shading, animating, and simulating 3D scenes.
**Example**:
- Mesh: list of vertices + faces
- Phong lighting: `color = ambient + diffuse + specular`

### 11. Mechanics 1: Linear Kinematics and Calculus
**Explanation**: Describes motion using velocity, acceleration, derivatives, and integrals.
**When to Use**: Simulating movement, physics, and animation curves.
**Example**:
- Velocity: `v = dx/dt`
- Position from velocity: `x = ∫v dt`

### 12. Mechanics 2: Linear and Rotational Dynamics
**Explanation**: Newton's laws, forces, momentum, collisions, and rigid body simulation.
**When to Use**: Physics engines, collision response, real-time simulation.
**Example**:
- F = m * a (force)
- Conservation of momentum in collisions

> **Watch out**: Use a fixed timestep for physics integration — tying the physics step to the render framerate causes non-deterministic, frame-rate-dependent simulation. Semi-implicit Euler (update velocity first, then position) is more stable than forward Euler for spring/oscillator systems.

### 13. Curves in 3D
**Explanation**: Parametric curves (Hermite, Bézier, splines), interpolation, and continuity. Used for animation paths, modeling, and procedural art.
**When to Use**: Camera paths, smooth animation, procedural geometry, drawing tools.
**Example**:
- Bézier curve: `B(t) = (1-t)^2*P0 + 2(1-t)t*P1 + t^2*P2`
- Spline interpolation for smooth paths

---

## Related Skills

Game-math-expert is a broad overview across 13 domains. When a topic needs production-depth or language-specific pseudocode, reach for the specialist skills below.

### trigonometry
Deep implementation guidance for angles, oscillations, circular/orbital motion, spiral paths, atan2 for rotational pointing, and trig in shaders. Covers 2D and 3D applications with worked code.

**Reach for this skill when:** topics 7 (polar coords), 8 (rotation angles), or any request involving `sin`/`cos`/`atan2`, phase offsets, wave motion, or spherical camera controllers.

### geometry
Euclidean spatial math: planes, normals, raycasting (ray-triangle via Möller–Trumbore, ray-sphere, ray-AABB), collision detection (AABB, sphere, SAT), point-in-shape tests, closest-point queries, backface culling, and frustum tests.

**Reach for this skill when:** topics 9 (geometric primitives) or 3 (coordinate spaces), or when the user is building a collision system, ray picker, physics broadphase, or spatial query.

### physics
Numerical integration methods (Euler, Verlet, RK4), rigid body dynamics, impulse-based collision response, spring-mass systems, position-based dynamics (PBD) for cloth/soft bodies, and SPH fluid simulation.

**Reach for this skill when:** topics 11–12 (kinematics, dynamics) need expanded implementation — fixed timestep loops, PBD cloth, fluid sims, or choosing the right integrator.

### linear-algebra
Matrix internals: determinants, inverses, orthonormal bases, eigenvalues, SVD, and their geometric meanings. Covers 4×4 homogeneous transforms, normal-transform fix (inverse-transpose), and the math behind projection matrices.

**Reach for this skill when:** topics 4–6 (matrices and transforms) need rigorous derivation, or the user is debugging a transform pipeline, building a custom projection matrix, or working with skinning / morph targets.

### animation-specialist
Full motion design stack: CSS keyframes, GSAP timelines, spring physics, SVG morphing, scroll-driven animation, and the math behind easing curves. Connects game-math curves to real animation implementations.

**Reach for this skill when:** topic 13 (curves) connects to an animation system — camera dolly paths, character IK, or procedural animation driven by splines.

### threejs-3d-webgpu
Three.js and WebGPU scene setup, materials, lighting, shader authoring (GLSL/WGSL via TSL), post-processing, and performance. Translates game-math concepts directly into Three.js API calls.

**Reach for this skill when:** the user is implementing game-math concepts in a Three.js or WebGPU project — projections, instanced meshes, custom shaders, or camera rigs.

### p5js-creative-coding
Creative and generative coding with p5.js — 2D/3D sketches, interaction, noise, particle systems, and visual experiments. Bridges math concepts to exploratory creative output.

**Reach for this skill when:** the user wants to visualise or prototype a game-math concept (e.g., "show me how quaternion slerp looks", "draw a Bézier curve") in an interactive sketch.

---

## References
- "3D Math Primer for Graphics and Game Development" — Dunn & Parberry
- "Real-Time Rendering" — Akenine-Möller et al.