-----

## name: algebraic-geometry
description: >
  Expert algebraic geometry assistant for mathematicians and advanced students. Use this skill whenever the user needs:
  help with algebraic varieties, scheme theory, cohomology, or understanding the geometric properties of solutions
  to polynomial equations. Includes both classical algebraic geometry and modern scheme-theoretic approaches.
trigger: Any pure mathematics problem involving polynomials, varieties, or geometric algebra - from solving systems
  of equations to understanding modern algebraic geometry.
license: MIT
compatibility: opencode
metadata:
  audience: mathematicians
  category: mathematics

# Algebraic Geometry — Varieties, Schemes, and Cohomology

Covers: **Affine Varieties · Projective Varieties · Schemes · Sheaves · Cohomology · Dimension Theory · Algebraic Curves**

-----

## Affine Algebraic Geometry

### Affine Space

n-dimensional affine space over algebraically closed field k:
```
A^n(k) = k^n
```

Points correspond to n-tuples (a₁, ..., a_n).

### Affine Varieties

An **affine variety** is an irreducible algebraic set:
```
V(I) = {p ∈ A^n | f(p) = 0 for all f ∈ I}
```

Where I is an ideal in k[x₁, ..., x_n].

**Hilbert's Nullstellensatz**:
```
I(V(J)) = √J for any ideal J
```

The correspondence between radical ideals and varieties is bijective.

### Coordinate Ring

```
k[V] = k[x₁, ..., x_n]/I(V)
```

The coordinate ring captures the algebraic information of the variety.

### Morphisms of Affine Varieties

A morphism φ: V → W corresponds to k-algebra homomorphism:
```
φ* : k[W] → k[V]
```

**Finite morphisms**: Integral extension
**Dominant morphisms**: Dense image

### Dimension

**Krull dimension**: Length of longest chain of prime ideals.

For variety V:
```
dim V = dim k[V]
```

Properties:
- dim A^n = n
- dim of hypersurface = n - 1
- Points have dimension 0

### Hilbert Function

```
H_V(t) = dim_k k[V]_t
```

For projective varieties, this is eventually polynomial (Hilbert polynomial).

### Regular Functions

For affine variety V, regular functions are elements of coordinate ring:
```
O_V(V) = k[V]
```

On open set U, regular functions are locally given by fractions with denominator non-zero on U.

-----

## Projective Geometry

### Projective Space

n-dimensional projective space:
```
P^n(k) = (k^{n+1} \ {0}) / ~
```

Where (a₀, ..., a_n) ~ λ(a₀, ..., a_n) for λ ≠ 0.

Homogeneous coordinates: [x₀ : x₁ : ... : xₙ]

### Projective Varieties

A **projective variety** is a closed subset of Pⁿ(k) defined by homogeneous polynomials.

**Projective Nullstellensatz**:
```
I(V(I)) = √I for homogeneous ideal I
V(I) = ∅ ⇔ √I contains all x_i
```

### Homogeneous Coordinates

Ring of polynomials graded by total degree:
```
k[x₀, ..., x_n] = ⊕_{d≥0} k[x₀, ..., x_n]_d
```

A polynomial is homogeneous of degree d if all monomials have degree d.

### Homogenization

For polynomial f ∈ k[x₁, ..., x_n] of degree d:
```
f^h = x₀^d f(x₁/x₀, ..., x_n/x₀)
```

### Dehomogenization

Setting x₀ = 1:
```
f^h|_{x₀=1} = f
```

### Projective Coordinate Ring

```
k[V] = k[x₀, ..., x_n]/I(V)
```

Graded by degree: k[V] = ⊕_{d≥0} k[V]_d

### Proj Construction

For graded ring S:
```
Proj(S) = {prime ideals not containing S_+}
```

This is the universal projective variety with homogeneous coordinate ring S.

### Affine Cover

Pⁿ has (n+1) affine open sets:
```
U_i = {x ∈ Pⁿ | x_i ≠ 0} ≅ Aⁿ
```

Transition maps given by rational functions.

-----

## Morphisms and Rational Maps

### Regular (Morphic) Maps

A morphism f: X → Y of varieties is locally given by regular functions:
```
f = (f₀, ..., f_m) with f_i ∈ O_X(U)
```

### Dominant Maps

f is dominant if f(X) is dense in Y. This corresponds to:
```
k(Y) ⊂ k(X) (field extension)
```

### Rational Maps

A rational map is morphism defined on open subset:
```
φ: X ⇢ Y = (f₀, ..., f_m) with f_i rational functions
```

**Domain of definition**: Where denominators nonzero.

### Birational Maps

A birational map is rational map with rational inverse:
```
k(Y) ≅ k(X)
```

Varieties are **birationally equivalent** if such map exists.

**Theorem**: Every smooth variety is birationally equivalent to a hypersurface in Pⁿ for sufficiently large n.

### Resolution of Singularities

For any variety V, there exists birational morphism:
```
π: V' → V
```

Where V' is smooth (non-singular). This is Hironaka's theorem (characteristic 0).

-----

## Sheaves and Local Theory

### Presheaf

For topological space X, presheaf F assigns:
- To each open U: group/ring F(U)
- To each inclusion V ⊂ U: restriction map F(U) → F(V)

With properties:
- F(∅) = 0
- Restriction is functorial

### Sheaf

A presheaf is a sheaf if:
1. **Locality**: Sections determined by restrictions to opens
2. **Gluing**: Locally compatible sections glue uniquely

**Sheaf of regular functions** O_X on variety X.

### Stalk

Stalk at point x:
```
F_x = lim_{x∈U} F(U)
```

Germs: equivalence classes of sections near x.

### Sheaf Homomorphism

Map of sheaves φ: F → G gives maps on all stalks:
```
φ_x: F_x → G_x
```

### Kernel and Cokernel

For sheaf homomorphism φ: F → G:
- Kernel: (ker φ)(U) = ker(F(U) → G(U))
- Cokernel: (coker φ)(U) = coker(F(U) → G(U))

### Sheaf Cohomology

Derived functors of global sections:
```
H^i(X, F) = R^iΓ(X, F)
```

Properties:
- H⁰(X, F) = Γ(X, F) (sections)
- H^i(X, F) = 0 for i > dim X on affine varieties (Serre)
- Flasque sheaves give exact global sections

### Čech Cohomology

For open cover U = {U_i}:
```
Č^p(F) = ∏ F(U_{i₀}∩...∩U_{i_p})
```

Differential: δ: Č^p → Č^{p+1}
H^*(U, F) = H^*(Č^*(F))

-----

## Cohomology of Sheaves

### Invertible Sheaves (Line Bundles)

Picard group:
```
Pic(X) = H¹(X, O_X*)
```

Line bundles correspond to divisors modulo linear equivalence.

### Divisors

Weil divisor: formal sum of codimension 1 subvarieties
```
D = Σ n_i V_i
```

Cartier divisor: locally principal codimension 1 subscheme

For Noetherian normal variety: Weil ↔ Cartier

### Canonical Divisor

For smooth variety X:
```
K_X = div(ω_X) where ω_X = Ω^n_{X/k}
```

### sheaf O(D)

For divisor D:
```
Γ(U, O(D)) = {f ∈ k(X)* | div(f) + D ≥ 0 on U}
```

### Adjunction Formula

For smooth subvariety Y ⊂ X:
```
K_Y = (K_X + Y)|_Y
```

### Riemann-Roch Theorem (Curves)

For line bundle L on curve C:
```
h⁰(C, L) - h⁰(C, K_C ⊗ L⁻¹) = deg L + 1 - g
```

Where g = genus of C.

### Hodge Diamond (Surfaces)

For smooth projective surface:
```
h^{p,q} = dim H^p(X, Ω^q_X)
```

With h^{p,q} = h^{q,p}.

-----

## sheaf Cohomology Computations

### Cech to Derived Functor

For good open cover, Čech cohomology computes sheaf cohomology:
```
H^*(U, F) ≅ H^*(X, F)
```

### Serre Duality

For smooth projective variety X of dimension n:
```
H^i(X, F) ≅ H^{n-i}(X, K_X ⊗ F⁻¹)*
```

### Leray Spectral Sequence

For map f: X → Y:
```
E²_{p,q} = H^p(Y, R^q f_* F) ⇒ H^{p+q}(X, F)
```

### Vanishing Theorems

**Kodaira vanishing**: For ample L on smooth projective:
```
H^i(X, K_X ⊗ L) = 0 for i > 0
```

**Serre vanishing**: For ample L, for large m:
```
H^i(X, O(mL)) = 0 for i > 0
```

### Hirzebruch-Riemann-Roch

For line bundle L on X:
```
χ(X, L) = χ(O_X) + (L^{n})/n! + higher (Todd genus)
```

-----

## Classical Enumerative Geometry

### Chern Classes

Total Chern class:
```
c(E) = 1 + c₁(E) + c₂(E) + ...
```

For line bundle: c₁(L) = divisor class of L.

### Schubert Calculus

Intersection theory on Grassmannians:
- Flags, conditions on subspaces
- Giambelli-Soudry-Thom formula

### Hilbert Scheme

Parametrizes all subschemes of Pⁿ with given Hilbert polynomial.

For 0-dimensional schemes of degree d:
```
Hilb^d(Pⁿ) dimension = n·d
```

### Counting Curves

**Gromov-Witten invariants**: Count curves of given genus through generic points.

**Donaldson-Thomas invariants**: Count subschemes satisfying ideal sheaf conditions.

### Severi Varieties

Parametrizes plane curves of degree d with δ nodes:
```
V_{d,δ} ⊂ P^{d(d+3)/2}
```

-----

## Modern Scheme Theory

### Schemes

Scheme X is locally ringed space locally isomorphic to affine scheme:
```
Spec R = {prime ideals of R}
```

Structure sheaf O_X on Spec R.

### Fiber Product

For morphisms X → S and Y → S:
```
X ×_S Y = Spec (O_X ⊗_{O_S} O_Y)
```

### Separated Morphisms

Morphism f: X → Y is separated if diagonal is closed.

### Proper Morphisms

Proper = separated + universally closed. 
Projective morphisms are proper.

### Flat Morphisms

Locally: Tor^O_{Y, f(x)}(O_X,x, k(f(x))) = 0 for i > 0

Properties:
- Fibers vary "continuously"
- Base change for cohomology

### Descent Theory

Grothendieck's fpqc descent:
- Quasi-coherent sheaves descend
- Effective descent for morphisms

### Algebraic Stacks

Generalizes moduli spaces with automorphisms:
- DM stacks: Deligne-Mumford
- Artin stacks: general

-----

## Dimension Theory

### Dimension of Affine Variety

```
dim V = transcendence degree of k(V) over k
```

Equivalently: length of generic chain of irreducible subvarieties.

### Dimension of Scheme

```
dim X = sup length of chain of irreducible closed subsets
```

### Krull's Principal Ideal Theorem

For Noetherian ring:
```
height P ≤ n if P contains n elements of a system of parameters
```

### Height and Depth

- Height of prime: length of longest chain to (0)
- Depth of module: length of maximal regular sequence

### Regular Local Rings

Local ring is regular if:
```
dim = minimal number of generators of maximal ideal
```

Geometrically: non-singular point.

### Singular Locus

```
Sing(X) = {x ∈ X | O_{X,x} not regular}
```

For variety over characteristic 0, singular locus is proper closed subset.

### Normal Varieties

Normal: Integral, locally integral closure in function field.
- Normalization: birational morphism from normal variety
- Normality ⇒ Serre's R1 + S2 conditions

-----

## Algebraic Curves

### Riemann Surface

Smooth algebraic curve = compact Riemann surface.
Genus g relates to topology:
- g = (2 - #faces + #edges - #vertices)/2 for triangulation
- g = b_1/2 for Betti number

### Canonical Embedding

For g ≥ 2, complete linear system |K_C| embeds C into P^{g-1}.

**Theorem (Riemann)**: Complex algebraic curves = compact Riemann surfaces.

### Elliptic Curves

g = 1: Smooth cubic in P².

Group law: chord-tangent process.
- Identity: point at infinity
- Associativity: geometric

Complex tori: C/Λ ≅ elliptic curve.

### Hyperelliptic Curves

g ≥ 2: Double cover of P¹ branched at 2g+2 points.

Model: y² = f(x) where deg f = 2g+1 or 2g+2.

### Moduli of Curves

M_g: moduli space of genus g curves.
- Dimension: 3g - 3
- Compactification M̅_g by stable curves

### Jacobian

Pic⁰(C) ≅ Alb(C) = H⁰(K_C)*/H¹(O_C)

Complex torus J(C) = H⁰(K_C)*/H¹(O_C)

### Torelli Theorem

C determined by J(C) with polarization.

-----

## Common Errors to Avoid

- Confusing affine and projective varieties
- Forgetting to homogenize/dehomogenize when switching
- Ignoring that projective closure adds points at infinity
- Confusing dimension of variety with dimension of ambient space
- Not understanding sheaf vs. presheaf distinction
- Applying algebraic results without checking hypotheses (e.g., normality)
- Forgetting that field must be algebraically closed for Nullstellensatz
- Confusing regular and rational functions
- Misunderstanding sheaf cohomology vs. singular cohomology

-----

## Key References

- **Algebraic Geometry** by Hartshorne — Standard text
- **Algebraic Geometry** by Griffiths & Harris — Classical methods
- **Algebraic Geometry** by Shafarevich — Introduction
- **Principles of Algebraic Geometry** by Harris — More accessible

