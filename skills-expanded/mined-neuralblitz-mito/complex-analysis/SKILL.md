-----

## name: complex-analysis
description: >
  Expert complex analysis assistant for mathematicians and physicists. Use this skill whenever the user needs:
  help with complex functions, contour integration, residue theory, conformal mapping, or understanding analytic
  structure in the complex plane. Includes both pure theory and applications to physics and engineering.
trigger: Any mathematical problem involving complex variables - from integration to potential theory to analytic number theory.
license: MIT
compatibility: opencode
metadata:
  audience: mathematicians
  category: mathematics

# Complex Analysis — Theory and Applications

Covers: **Complex Numbers · Analytic Functions · Complex Integration · Residue Theory · Conformal Mapping · Series**

-----

## Complex Numbers

### Algebraic Form

```
z = x + iy
```

Where i² = -1, x = Re(z), y = Im(z).

### Polar Form

```
z = r(cos θ + i sin θ) = re^{iθ}
```

Where r = |z| = √(x² + y²), θ = arg(z).

### Complex Conjugate

```
z̅ = x - iy
```

Properties:
- z z̅ = |z|²
- Re(z) = (z + z̅)/2
- Im(z) = (z - z̅)/(2i)

### Argument

```
arg(z) = θ, z = |z|e^{iθ}
```

Multi-valued: arg(z) = θ + 2πk.

### Euler's Formula

```
e^{iθ} = cos θ + i sin θ
```

Useful identities:
- e^{iπ} = -1
- e^{iπ/2} = i
- cos θ = (e^{iθ} + e^{-iθ})/2
- sin θ = (e^{iθ} - e^{-iθ})/(2i)

### Roots of Unity

Solutions to z^n = 1:
```
z_k = e^{2πik/n}, k = 0, 1, ..., n-1
```

### Complex Logarithm

```
log z = ln|z| + i arg(z)
```

Multi-valued: log z = Ln z + 2πik.

Principal value: Log z = ln|z| + iArg(z), with -π < Arg(z) ≤ π.

### Complex Exponentiation

```
z^w = e^{w Log z} = e^{w(log|z| + i arg z)}
```

May be multi-valued.

-----

## Analytic Functions

### Complex Differentiability

Function f is complex differentiable at z₀ if:
```
lim_{z→z₀} (f(z) - f(z₀))/(z - z₀) exists
```

This limit must be same from all directions.

### Holomorphic (Analytic)

f is holomorphic on open set if complex differentiable at every point.
Equivalent: complex analytic (power series expansion exists locally).

### Cauchy-Riemann Equations

For f(z) = u(x,y) + iv(x,y) to be holomorphic:
```
∂u/∂x = ∂v/∂y
∂u/∂y = -∂v/∂x
```

Equivalently in complex form:
```
∂f/∂z̅ = 0 (where ∂/∂z̅ = (1/2)(∂/∂x + i∂/∂y))
```

### Harmonic Functions

If f = u + iv holomorphic, then u and v satisfy Laplace's equation:
```
∇²u = 0, ∇²v = 0
```

Conjugate harmonic functions.

### Entire Functions

Holomorphic on entire complex plane.
Examples: polynomials, e^z, sin z, cos z.

### meromorphic Functions

Holomorphic except isolated poles.
Examples: rational functions, tan z, cot z.

### Isolated Singularities

| Type | Definition | Example |
|------|------------|---------|
| Removable | Limit exists | sin z / z at z=0 |
| Pole | |z|→∞ → ∞ | 1/z at z=0 |
| Essential | Neither | e^{1/z} at z=0 |

**Casorati-Weierstrass**: Near essential singularity, f gets arbitrarily close to any complex value.

### Laurent Series

Around isolated singularity:
```
f(z) = Σ_{n=-∞}^{∞} a_n (z - z₀)^n
```

- **Principal part**: terms with n < 0
- **Regular part**: terms with n ≥ 0

Classification:
- Removable: principal part = 0
- Pole of order m: finite principal part
- Essential: infinite principal part

-----

## Complex Integration

### Contour Integration

```
∫_γ f(z) dz = ∫_a^b f(γ(t)) γ'(t) dt
```

### ML-Estimate (Modulus Bound)

```
|∫_γ f(z) dz| ≤ M L
```

Where |f(z)| ≤ M on path of length L.

### Cauchy Integral Theorem

If f is holomorphic on simply connected domain D:
```
∮_C f(z) dz = 0
```

For any closed contour C in D.

### Cauchy Integral Formula

For f holomorphic inside and on C:
```
f^(n)(z₀) = (n!/(2πi)) ∮_C f(z)/(z - z₀)^{n+1} dz
```

For n = 0:
```
f(z₀) = (1/2πi) ∮_C f(z)/(z - z₀) dz
```

### Deformation Invariance

Homotopic contours give same integral.

### Winding Number

For closed contour C about point a:
```
n(C,a) = (1/2πi) ∮_C dz/(z - a)
```

Integer = number of times C winds counterclockwise around a.

### Argument Principle

```
(1/2πi) ∮ f'(z)/f(z) dz = N - P
```

Where N = zeros, P = poles (counted with multiplicity).

-----

## Residue Theory

### Residue Definition

Coefficient a_{-1} in Laurent expansion:
```
Res(f, z₀) = a_{-1}
```

### Residue Formula for Pole of Order m

```
Res(f, z₀) = (1/(m-1)!) lim_{z→z₀} d^{m-1}/dz^{m-1}[(z - z₀)^m f(z)]
```

For simple pole (m = 1):
```
Res(f, z₀) = lim_{z→z₀} (z - z₀)f(z)
```

### Residue Theorem

For domain containing closed contour C:
```
∮_C f(z) dz = 2πi Σ Res(f, z_k)
```

Sum over residues inside C.

### Using Residues for Integration

1. Identify singularities inside contour
2. Compute residues
3. Sum × 2πi

### Essential Integrals

**Type 1**: ∫₀^{2π} R(sin θ, cos θ) dθ
- Use z = e^{iθ}, dz = i z dθ

**Type 2**: ∫_{-∞}^{∞} f(x) dx
- Use upper/lower half-plane for real rational functions

**Type 3**: ∫₀^{∞} x^α f(x) dx
- Branch cuts needed

### Indented Contours

For integrals with poles on real axis:
- Small semicircles above/below
- Take limit as radius → 0

### Principal Value

```
PV ∮ f(z) dz = lim_{ε→0} (∮_{C_ε} f(z) dz)
```

Cauchy principal value exists even when simple pole on contour.

-----

## Series Expansions

### Taylor Series

For holomorphic f at z₀:
```
f(z) = Σ_{n=0}^{∞} a_n (z - z₀)^n
```

Radius of convergence = distance to nearest singularity.

### Maclaurin Series

Taylor series about 0.

Common expansions:
```
e^z = Σ z^n/n!
sin z = Σ (-1)^n z^{2n+1}/(2n+1)!
cos z = Σ (-1)^n z^{2n}/(2n)!
log(1+z) = Σ (-1)^n z^{n+1}/(n+1) (|z| < 1, z ≠ -1)
(1+z)^α = Σ C(α,n) z^n (|z| < 1)
```

### Radius of Convergence

R = distance from center to nearest singularity.

### Region of Convergence

| Series Type | ROC |
|-------------|-----|
| Taylor at interior point | Disk to nearest singularity |
| Laurent (inner) | Annulus between singularities |

### Uniform Convergence

On compact sets → can differentiate/integrate term-by-term.

### Weierstrass M-Test

If |f_n(z)| ≤ M_n for all z in domain and ΣM_n converges, then Σf_n converges uniformly.

### Abel's Theorem

If Σa_n converges, then:
```
lim_{r→1^-} Σa_n r^n = Σa_n
```

Power series converge at boundary except possibly at singular points.

-----

## Conformal Mapping

### Conformal (Biholomorphic)

f is conformal if:
- Holomorphic with non-zero derivative
- Or anti-holomorphic with non-zero derivative (reflection)

Angles preserved (except at critical points).

### Conformal Equivalence

Two domains are conformally equivalent if there exists bijective holomorphic map between them.

**Riemann Mapping Theorem**: Simply connected non-empty proper subdomain of C is conformally equivalent to unit disk.

### Möbius Transformations

```
f(z) = (az + b)/(cz + d), ad - bc ≠ 0
```

Properties:
- Map circles/lines to circles/lines
- Cross-ratio preserved
- 3 points determine transformation

### Mapping Examples

| Map | Formula | Maps to |
|-----|---------|---------|
| Translation | z → z + a | Shift |
| Rotation | z → e^{iθ}z | Rotate |
| Scaling | z → az | Scale |
| Inversion | z → 1/z | Reflect in unit circle |

### Schwarz-Christoffel Mapping

Maps upper half-plane to polygon:
```
f(z) = A + C ∫ (z - z₁)^{-α₁} ... (z - z_n)^{-α_n} dz
```

Where α_i π = interior angle at vertex.

### Green's Function

For domain D with boundary:
```
G(z, ζ) = log|z-ζ| - h(z,ζ)
```

Harmonic with boundary condition G = 0.

### Dirichlet Problem

Find harmonic function with prescribed boundary values.
Solved using conformal mapping to standard domain.

-----

## Entire and Meromorphic Functions

### Order of Entire Function

```
ρ = lim sup_{r→∞} log log M(r) / log r
```

Where M(r) = max|f(z)| on |z| = r.

Examples:
- Polynomial: ρ = 0
- e^z: ρ = 1
- e^{z²}: ρ = 2

### Hadamard's Theorem

For entire function of finite order ρ:
```
f(z) = e^{P(z)} Π(z)
```

Where P is polynomial of degree ≤ ρ, Π is product over zeros.

### Picard's Theorem

Entire function misses at most one value (Picard).

### Mittag-Leffler Expansion

For meromorphic function with poles {a_n}:
```
f(z) = g(z) + Σ [P_n(1/(z - a_n)) + c_n]
```

### Partial Fractions

For rational function:
```
f(z) = Σ A_n/(z - a_n) + polynomial
```

### Weierstrass Product

For zeros {a_n}:
```
P(z) = Π (1 - z/a_n) e^{z/a_n + ... + z^{m_n}/m_n a_n^{m_n}}
```

Ensures convergence.

-----

## Harmonic Functions

### Maximum Principle

Non-constant harmonic function cannot have interior maxima/minima.

### Mean Value Property

For harmonic u:
```
u(z₀) = (1/2π) ∫_0^{2π} u(z₀ + re^{iθ}) dθ
```

### Poisson Integral

For disk:
```
u(re^{iφ}) = (1/2π) ∫_0^{2π} u(e^{iθ}) P(r, φ-θ) dθ
```

Poisson kernel: P(r,θ) = (1 - r²)/(1 - 2r cos θ + r²)

### Schwarz Formula

For holomorphic f = u + iv:
```
f(z) = (1/2πi) ∮ f(ζ) (ζ + z)/(ζ - z) dζ/ζ
```

### Harnack's Inequality

For positive harmonic functions:
```
(r-1)/(r+1) ≤ u(z)/u(0) ≤ (r+1)/(r-1) for |z| = r
```

### Dirichlet Problem

Solve Laplace's equation with boundary conditions.
Solution: Poisson integral formula.

### Neumann Problem

Solve with specified normal derivative on boundary.

-----

## Analytic Continuation

### Analytic Continuation

Extend holomorphic function beyond original domain.

**Schwarz reflection principle**: If u = 0 on real axis segment, extend by reflection.

### Indirect Continuation

Via analytic path: if two domains overlap and functions agree on overlap, they give continuation.

### Monodromy Theorem

If continuation along any path is independent of homotopy class, function extends to universal cover.

### Riemann Surfaces

Function becomes single-valued on appropriate covering space.
Example: log z → covers of punctured plane.

### Natural Boundary

Domain where function cannot be analytically continued across any boundary point.

Example: Σz^n has unit circle as natural boundary.

### Analytic Continuation of Power Series

Original: f(z) = Σa_n(z - z₀)^n
Extended via: different center gives different expansion (same function where overlap).

### Schwarz Reflection

If f extends continuously to real interval and is real-valued there, can reflect:
```
f(z̅) = f(z)̅
```

-----

## Applications

### Evaluation of Real Integrals

Use contour integration with keyhole, upper/lower half-plane.

**Real rational**: Close in upper half-plane
**Trigonometric**: z = e^{iθ} substitution
**Half-plane**: Use Jordan's lemma

### Inverse Laplace Transform

Use Bromwich integral:
```
f(t) = (1/2πi) ∫_{c-i∞}^{c+i∞} F(s) e^{st} ds
```

### Fluid Dynamics

Complex potential: w(z) = φ + iψ
- φ = velocity potential
- ψ = stream function

Flow around cylinder with circulation.

### Electrostatics

Complex potential for 2D electrostatic problems.
Use conformal mapping to solve boundary value problems.

### Fourier Transform

```
F(ω) = ∫_{-∞}^{∞} f(t) e^{-iωt} dt
```

Use complex analysis for inversion, poles in complex plane.

### Number Theory

Analytic continuation of ζ(s):
```
ζ(s) = Σ n^{-s}
```

Non-trivial zeros: s = ½ + it (critical strip).

Functional equation relates ζ(s) to ζ(1-s).

-----

## Common Errors to Avoid

- Forgetting that complex differentiability is more restrictive than real
- Confusing isolated singularities and branch points
- Incorrectly handling multi-valued functions (log, root)
- Using Cauchy's theorem when function has singularities inside contour
- Forgetting to include all residues
- Confusing Taylor and Laurent series
- Incorrect branch cut placement
- Forgetting that conformal maps preserve angles, not orientations (anti-holomorphic)
- Using Poisson formula without checking boundary regularity
- Not considering that analytic continuation may not be unique (monodromy)

-----

## Key References

- **Complex Analysis** by Ahlfors — Classic text
- **Complex Analysis** by Stein & Shakarchi — Modern treatment
- **Functions of One Complex Variable** by Conway — More detailed
- **Visual Complex Analysis** by Needham — Geometric intuition

