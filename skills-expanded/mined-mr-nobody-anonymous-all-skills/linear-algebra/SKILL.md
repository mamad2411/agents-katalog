---
name: linear-algebra
description: "Vector spaces, matrices, eigenvalues, linear transformations, inner product spaces, and decompositions"
category: mathematics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mathematics/linear-algebra/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Linear Algebra

## Scope
Linear algebra studies vector spaces, linear maps, and their representation as matrices. It is foundational to nearly all quantitative disciplines.

## Vector Spaces
- **Axioms**: Closed under addition and scalar multiplication, contains zero vector
- **Subspace**: Non-empty subset that is itself a vector space
- **Span**: span(v₁,...,vₙ) = all linear combinations
- **Linear independence**: Σ cᵢvᵢ = 0 implies all cᵢ = 0
- **Basis**: Linearly independent spanning set; dim(V) = number of basis vectors

## Matrices & Linear Maps

### Operations
- Matrix multiplication: (AB)ᵢⱼ = Σₖ AᵢₖBₖⱼ — not commutative
- **Transpose**: (Aᵀ)ᵢⱼ = Aⱼᵢ
- **Inverse**: AA⁻¹ = I; exists iff det(A) ≠ 0
- **Rank**: dim(column space) = dim(row space)
- **Nullity**: dim(null space); Rank-Nullity: rank(A) + nullity(A) = n

### Systems of Equations (Ax = b)
- **Gaussian elimination**: Row echelon form → back substitution
- **Solution types**: Unique (rank = n), infinite (rank < n, consistent), none (inconsistent)
- **Cramer's Rule**: xᵢ = det(Aᵢ)/det(A) — practical only for small systems

## Eigenvalues & Eigenvectors
- **Definition**: Av = λv where λ = eigenvalue, v = eigenvector (v ≠ 0)
- **Characteristic polynomial**: det(A - λI) = 0
- **Properties**: tr(A) = Σ λᵢ, det(A) = Π λᵢ
- **Diagonalization**: A = PDP⁻¹ where D = diag(λ₁,...,λₙ), P = [v₁|...|vₙ]
- **Symmetric matrices**: All eigenvalues real, eigenvectors orthogonal

## Matrix Decompositions
| Decomposition | Form | When to Use |
|--------------|------|-------------|
| LU | A = LU | Solving Ax = b efficiently |
| QR | A = QR (Q orthogonal, R upper triangular) | Least squares, eigenvalue algorithms |
| SVD | A = UΣVᵀ | Any matrix; rank, pseudoinverse, PCA |
| Cholesky | A = LLᵀ | Symmetric positive definite |
| Spectral | A = QΛQᵀ | Symmetric/Hermitian matrices |

### Singular Value Decomposition (SVD)
- A = UΣVᵀ where U, V orthogonal, Σ diagonal with σ₁ ≥ σ₂ ≥ ... ≥ 0
- **Applications**: Data compression (keep top k singular values), pseudoinverse (A⁺ = VΣ⁺Uᵀ), PCA, LSA
- **Condition number**: κ(A) = σ_max/σ_min — measures numerical sensitivity

## Inner Product Spaces
- **Inner product**: ⟨u,v⟩ satisfying linearity, symmetry, positive definiteness
- **Norm**: ||v|| = √⟨v,v⟩
- **Orthogonality**: ⟨u,v⟩ = 0
- **Gram-Schmidt**: Produce orthonormal basis from any basis
- **Projection**: proj_W(v) = Σ ⟨v,eᵢ⟩eᵢ (onto subspace with ONB {eᵢ})

## Computational Tools
- **NumPy**: `np.linalg.eig`, `np.linalg.svd`, `np.linalg.solve`
- **SciPy**: Sparse matrix support, iterative solvers
- **LAPACK**: Fortran library underlying most numerical linear algebra
- **MATLAB**: Native matrix operations
- **Julia**: First-class matrix support

## References
- Strang — *Introduction to Linear Algebra*
- Axler — *Linear Algebra Done Right*
- Horn & Johnson — *Matrix Analysis*
