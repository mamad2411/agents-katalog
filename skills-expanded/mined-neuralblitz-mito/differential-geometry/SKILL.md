-----

## name: differential-geometry
description: >
  Expert differential geometry assistant for mathematicians and physicists. Use this skill whenever the user needs:
  help with smooth manifolds, Riemannian geometry, curvature, geodesics, or geometric structures on spaces.
  Includes both intrinsic differential geometry and applications to mathematical physics.
trigger: Any problem involving smooth spaces, curvature, or geometric analysis - from pure mathematics to general relativity.
license: MIT
compatibility: opencode
metadata:
  audience: mathematicians
  category: mathematics

# Differential Geometry — Manifolds, Curvature, and Geometry

Covers: **Smooth Manifolds · Tangent Spaces · Riemannian Metrics · Curvature · Geodesics · Connections · Lie Groups**

-----

## Smooth Manifolds

### Definition

An n-dimensional **smooth (C^∞) manifold** is a Hausdorff, second-countable space M with a smooth atlas: collection of charts (U_α, φ_α) where:

- U_α ⊂ M open cover
- φ_α: U_α → φ_α(U_α) ⊂ R^n
- Transition maps φ_β ∘ φ_α^{-1} are C^∞ where defined

### Examples

| Manifold | Description |
|----------|-------------|
| R^n | Euclidean space |
| S^n | n-sphere in R^{n+1} |
| T^n | n-torus = S^1 × ... × S^1 |
| Projective space P^n(R) | Lines through origin in R^{n+1} |
| Grassmannian G(k,n) | k-planes in R^n |

### Smooth Maps

A map f: M → N is smooth if in coordinates:
```
ψ ∘ f ∘ φ^{-1}: R^n → R^m
```
is C^∞ for all charts.

### Diffeomorphism

Smooth map with smooth inverse. Two manifolds are diffeomorphic if such map exists.

**Warning**: Manifolds may be homeomorphic but not diffeomorphic (exotic spheres).

### Submanifolds

N ⊂ M is embedded submanifold if inclusion is immersion and N has subspace topology.

### Partition of Unity

For paracompact manifold, smooth partition of unity exists:
```
Σ_i φ_i = 1
```

Enables global constructions from local data.

-----

## Tangent Spaces

### Tangent Vectors (Geometric)

Tangent vector at p ∈ M: equivalence class of curves γ(t) with γ(0) = p, tangent at t = 0.

### Tangent Vectors (Algebraic)

Derivation at p: linear map v: C^∞(M) → R satisfying:
```
v(fg) = v(f)g(p) + f(p)v(g)
```

This gives intrinsic definition.

### Tangent Space

Set of all tangent vectors at p:
```
T_pM
```

Dimension: dim T_pM = dim M

### Coordinate Basis

If (x¹, ..., xⁿ) are local coordinates:
```
∂/∂x^i|_p forms basis of T_pM
```

### Pushforward (Differential)

For smooth f: M → N:
```
f_*: T_pM → T_{f(p)}N
```

For curve: f_*(γ') = (f ∘ γ)'

### Pullback of Covectors

For function f: M → R:
```
df_p: T_pM → R
```

Coordinate expression: df = (∂f/∂x^i) dx^i

### Cotangent Space

Dual vector space:
```
T_p*M = (T_pM)*
```

Covectors: linear functionals on tangent vectors.

### Exterior Product

```
Λ^k T_p*M = k-forms at p
```

-----

## Vector Bundles

### Definition

Smooth fiber bundle with vector space fiber F = R^k and structure group GL(k, R).

Sections: smooth maps s: M → E with s(p) ∈ E_p.

### Tangent Bundle

```
TM = ⊔_p T_pM
```

Section of TM: vector field on M.

### Cotangent Bundle

```
T*M = ⊔_p T_p*M
```

Section: 1-form on M.

### Line Bundle

Vector bundle of rank 1. Equivalent to divisor class (complex case).

### Sections and Local Sections

Local section over U: s: U → E with π ∘ s = id_U.

### Transition Functions

On overlap U_α ∩ U_β:
```
g_{αβ}: U_α ∩ U_β → GL(k,R)
```

Determines bundle from coordinate charts.

### Operations on Bundles

- **Dual**: E* with fibers (E_p)*
- **Tensor product**: (E ⊗ F)_p = E_p ⊗ F_p
- **Exterior power**: Λ^k E
- **Direct sum**: E ⊕ F

-----

## Riemannian Metrics

### Definition

Riemannian metric g: smooth assignment of inner product on tangent spaces:
```
g_p: T_pM × T_pM → R
```

Smoothly varying with p.

### Length of Vector

|v|_p = √(g_p(v, v))

### Length of Curve

For parameterized curve γ: [a,b] → M:
```
L(γ) = ∫_a^b |γ'(t)|_γ(t) dt
```

### Riemannian Manifold

(M, g) with g a Riemannian metric.

### Examples

- Euclidean space: g = δ_ij dx^i ⊗ dx^j
- Sphere S^n: induced metric from R^{n+1}
- Hyperbolic space: Poincaré ball model

### Musical Isomorphisms

```
♭: TM → T*M, v ↦ g(v, ·)
♯: T*M → TM, ω ↦ g^{-1}(ω, ·)
```

Raising/lowering indices.

### Norm and Angle

Angle between vectors:
```
cos θ = g(v,w)/(|v||w|)
```

### Volume Form

For oriented Riemannian n-manifold:
```
dV_g = √|det g| dx¹ ∧ ... ∧ dx^n
```

-----

## Connections

### Levi-Civita Connection

Unique connection ∇ on (M,g) satisfying:
1. **Metric compatibility**: X(g(Y,Z)) = g(∇_X Y, Z) + g(Y, ∇_X Z)
2. **Torsion-free**: ∇_X Y - ∇_Y X = [X,Y]

**Christoffel symbols** in coordinates:
```
∇_{∂/∂x^i} ∂/∂x^j = Γ^k_{ij} ∂/∂x^k
```

### Covariant Derivative

For vector field Y along curve γ:
```
D_t Y = ∇_{γ'(t)} Y
```

This is the intrinsic derivative.

### Parallel Transport

Y along γ is parallel if D_t Y = 0.

Given initial Y(0), parallel transport along γ gives Y(t).

### Geodesics

Curve γ with γ'' = 0 (acceleration zero):
```
∇_{γ'} γ' = 0
```

In coordinates:
```
d²x^k/dt² + Γ^k_{ij} dx^i/dt dx^j/dt = 0
```

### Exponential Map

For v ∈ T_pM, geodesic γ_v with γ_v(0) = p, γ_v'(0) = v.

**Exponential map**:
```
exp_p: U ⊂ T_pM → M, v → γ_v(1)
```

Local diffeomorphism near 0.

### Logarithmic Map

Inverse of exp_p:
```
log_p: V ⊂ M → T_pM
```

### Geodesic Distance

For Riemannian manifold:
```
d(p,q) = inf{L(γ) | γ from p to q}
```

For Minkowski space: d = straight line length.

-----

## Curvature

### Riemann Curvature Tensor

```
R(X,Y)Z = ∇_X∇_Y Z - ∇_Y∇_X Z - ∇_{[X,Y]} Z
```

(1,3)-tensor. In coordinates: R^i_{jkl}.

### Curvature Operator

```
R(X,Y): TM → TM, Z ↦ R(X,Y)Z
```

### Sectional Curvature

For plane σ ⊂ T_pM:
```
K(σ) = g(R(e₁,e₂)e₂, e₁)/|e₁∧e₂|²
```

Depends only on the 2-plane.

### Ricci Curvature

Trace of Riemann:
```
Ric(X,Y) = tr( Z → R(Z,X)Y )
```

In coordinates: R_{ij} = R^k_{ikj}.

### Scalar Curvature

Trace of Ricci:
```
S = tr_g Ric = g^{ij} R_{ij}
```

### Geometric Interpretations

- **Sectional**: curvature of 2D surface through plane
- **Ricci**: volume comparison, Einstein equations
- **Scalar**: average sectional curvature

### Curvature and Topology

- **Gauss-Bonnet**: ∫_M K dA = 2π χ(M) (2D)
- **Chern-Gauss-Bonnet**: ∫_M χ(M) = (1/(8π)^{n/2} ∫ |P| (higher dimension)
- **Bonnet-Myers**: Ricci > (n-1)/R² → compact, diameter bounded

### Comparison Geometry

- **Rauch comparison**: geodesic comparison based on curvature bounds
- **Volume growth**: lower bounds on Ricci → volume bounds
- **Splitting theorem**: Ricci ≥ 0 + line → product structure

-----

## Geodesics and Distance Geometry

### Geodesic Equation

```
d²x^i/dt² + Γ^i_{jk} dx^j/dt dx^k/dt = 0
```

Second-order ODE → unique solution from initial conditions.

### Geodesic Completeness

All geodesics extend for all time.
Complete Riemannian manifolds: Hopf-Rinow theorem equivalent conditions.

### Minimal Geodesics

Between p and q, minimizing length curve is geodesic (locally).

### Cut Locus

Point where geodesic ceases to be minimizing.
After cut point, another geodesic is shorter.

### Injectivity Radius

```
inj(p) = min{distance to cut point in each direction}
inj(M) = inf_p inj(p)
```

### Convexity

**Geodesically convex**: unique minimizing geodesic between any two points.
**Strictly convex**: second fundamental form positive.

### Length Minimization

- **Hopf-Rinow**: Complete + bounded → compact
- **Gradient flow**: geodesics as critical points of energy functional

-----

## Submanifolds

### Immersions and Embeddings

f: N → M smooth with injective derivative.

Embedding: immersion + proper + topological embedding.

### Induced Metric

For submanifold with immersion i: (N, i*g) Riemannian.

### Second Fundamental Form

For submanifold Y ⊂ X:
```
II: T_pY × T_pY → (T_pY)^⊥
```

Measures extrinsic curvature.

### Mean Curvature

Trace of second fundamental form:
```
H = tr(II)
```

### Gauss Formula

For vector field along Y:
```
∇_X Y = (∇_X Y)^T + II(X,Y)
```

### Weingarten Formula

For normal vector field:
```
∇_X ν = -A_ν(X) + ∇_X^⊥ ν
```

Where A_ν is shape operator.

### Minimal Surfaces

Mean curvature H = 0 everywhere.
Euler-Lagrange for area functional.

-----

## Lie Groups

### Definition

Lie group G: smooth manifold with group structure (multiplication, inverse) smooth.

### Examples

| Group | Description |
|-------|-------------|
| GL(n,R) | Invertible n×n matrices |
| SL(n,R) | Determinant 1 |
| O(n) | Orthogonal matrices |
| SO(n) | Orientation-preserving orthogonal |
| U(n) | Unitary (complex) |
| SU(n) | Special unitary |
| Sp(n) | Symplectic |

### Lie Algebra

Tangent space at identity:
```
g = T_eG
```

Bracket: [X,Y] = XY - YX (commutator).

### Exponential Map

For X ∈ g:
```
exp: g → G
```

For matrix groups: exp(X) = e^X.

### One-Parameter Subgroups

γ(t) = exp(tX) satisfies:
- γ(0) = e
- γ'(0) = X
- γ(s+t) = γ(s)γ(t)

### Adjoint Representation

Ad: G → Aut(g)
Ad_g: X → gXg^{-1}

Derivative: ad: g → End(g), ad_X(Y) = [X,Y]

### Homomorphisms

Lie group homomorphism φ: G → H gives Lie algebra homomorphism dφ: g → h.

### Haar Measure

Unique left-invariant measure on Lie group.
Integration using bi-invariant metric when available.

-----

## Curvature Computations

### Curvature of Space Forms

**Sphere S^n(R)**:
- Sectional curvature = 1/R²
- Ricci = (n-1)/R² g
- Scalar = n(n-1)/R²

**Hyperbolic space H^n(R)**:
- Sectional curvature = -1/R²
- Ricci = -(n-1)/R² g
- Scalar = -n(n-1)/R²

**Flat space**:
- All curvatures = 0

### Product Metrics

For (M₁,g₁) × (M₂,g₂):
- Curvature: sum of individual
- Ricci: diagonal sum
- Sectional: independent 2-planes

### Warped Products

For f: M → (0,∞):
M_f = M ×_f N with metric g = g_M + f² g_N.

Useful for cosmology, black holes.

-----

## Geometric Analysis

### Laplace-Beltrami Operator

```
Δ_g f = div(∇f) = |g|^{-1/2} ∂_i(|g|^{1/2} g^{ij} ∂_j f)
```

### Hodge Laplacian

```
Δ = dδ + δd on forms
```

### Heat Kernel

Solution to heat equation:
```
(∂/∂t - Δ)K = 0
K(t,p,q) ~ (4πt)^{-n/2} e^{-d(p,q)²/4t}
```

### Geodesic Flow

Flow on unit tangent bundle:
```
Φ_t: SM → SM
```

Anosov if sectional curvature < 0.

### Geometric Evolution Equations

- **Ricci flow**: ∂g/∂t = -2Ric
- **Mean curvature flow**: ∂X/∂t = H
- **Yamabe flow**: ∂g/∂t = (R - r)g

-----

## Common Errors to Avoid

- Confusing tangent vectors with coordinate basis vectors
- Forgetting that curvature is a tensor (transforms correctly)
- Applying formulas without checking metric compatibility
- Confusing intrinsic and extrinsic curvature
- Forgetting that geodesics are locally length-minimizing, not globally
- Confusing the exponential map with matrix exponential (when different)
- Mixing up sectional, Ricci, and scalar curvature
- Not understanding that connection coefficients are not tensors
- Confusing pushforward and pullback directions
- Forgetting that Levi-Civita connection is metric compatible and torsion-free

-----

## Key References

- **Riemannian Geometry** by do Carmo — Standard intro
- **Introduction to Riemannian Manifolds** by Lee — Modern treatment
- **Differential Geometry** by Klingenberg — Advanced topics
- **Foundations of Differential Geometry** by Kobayashi & Nomizu — Comprehensive

