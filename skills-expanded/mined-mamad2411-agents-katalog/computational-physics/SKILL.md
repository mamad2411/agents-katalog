-----

## name: computational-physics
description: >
  Expert computational physics assistant for physicists and students. Use this skill whenever the user needs:
  help with numerical methods, solving differential equations, Monte Carlo simulations, or implementing
  computational approaches to physical problems. Includes algorithm design and code optimization.
trigger: Any physics problem requiring numerical simulation - from classical mechanics to quantum systems.
license: MIT
compatibility: opencode
metadata:
  audience: physicists
  category: physics

# Computational Physics — Numerical Methods and Simulation

Covers: **Numerical Integration · ODE Solvers · PDE Methods · Monte Carlo · Spectral Methods · High-Performance Computing**

-----

## Numerical Integration

### Newton-Cotes Formulas

**Trapezoidal Rule**:
```
∫_a^b f(x)dx ≈ (b-a)/2 [f(a) + f(b)]
```

Error: -(b-a)³/12 f''(ξ)

**Simpson's Rule**:
```
∫_a^b f(x)dx ≈ (b-a)/6 [f(a) + 4f((a+b)/2) + f(b)]
```

Error: -(b-a)⁵/2880 f⁴(ξ)

### Gaussian Quadrature

Nodes and weights chosen optimally:
```
∫_{-1}^{1} f(x)dx ≈ Σ w_i f(x_i)
```

For n points: exact for polynomials up to degree 2n-1.

**Common rules**:
- Gauss-Legendre: [-1, 1], any weight
- Gauss-Laguerre: [0, ∞), e^{-x}
- Gauss-Hermite: (-∞, ∞), e^{-x²}
- Gauss-Chebyshev: [-1, 1], 1/√(1-x²)

### Composite Rules

Divide interval into N subintervals:
- Composite Simpson: O(h⁴)
- Composite trapezoid: O(h²)

### Adaptive Quadrature

Adjust step size based on error estimate:
```
Error ≈ |S₁ - S₂|
```

If error > tolerance, subdivide region.

### Multi-Dimensional Integration

Monte Carlo methods often better for high dimensions:
```
∫ f(x) dⁿx ≈ V ⟨f⟩
```

Variance reduction: importance sampling.

### Numerical Integration Errors

| Method | Order | Error |
|--------|-------|-------|
| Trapezoid | 2 | h² |
| Simpson | 4 | h⁴ |
| Gauss (n pts) | 2n | h^{2n} |

-----

## Ordinary Differential Equations

### Initial Value Problems

Find y(t) given y(t₀) = y₀.

### Euler's Method

```
y_{n+1} = y_n + h f(t_n, y_n)
```

First order accurate: O(h).

### Runge-Kutta Methods

**RK2 (Midpoint)**:
```
k₁ = h f(t_n, y_n)
k₂ = h f(t_n + h/2, y_n + k₁/2)
y_{n+1} = y_n + k₂
```

**RK4 (Classical)**:
```
k₁ = h f(t_n, y_n)
k₂ = h f(t_n + h/2, y_n + k₁/2)
k₃ = h f(t_n + h/2, y_n + k₂/2)
k₄ = h f(t_n + h, y_n + k₃)
y_{n+1} = y_n + (k₁ + 2k₂ + 2k₃ + k₄)/6
```

Fourth order: O(h⁴).

### Adaptive Step Size

Estimate error with two methods (RK4/5):
```
Error = |y_5 - y_4|
```

Adjust h accordingly.

### Implicit Methods

Backward Euler:
```
y_{n+1} = y_n + h f(t_{n+1}, y_{n+1})
```

Requires solving equation (Newton iteration).
A-stable (unconditionally stable).

### Stiff Equations

When solution has both fast and slow scales:
- Use implicit methods
- BDF (Backward Differentiation Formula)
- Gear's method

### Boundary Value Problems

Given y(a) = α, y(b) = β.

**Shooting method**: Convert to IVP, iterate.
**Finite difference**: Discretize, solve linear system.

### Green's Functions

For linear ODE:
```
Ly = f, y(a)=y(b)=0
G solves LG = δ
y = ∫ G(x,s) f(s) ds
```

-----

## Partial Differential Equations

### Classification

| Type | Form | Example |
|------|------|---------|
| Elliptic | ∇²u = f | Laplace, Poisson |
| Parabolic | ∂u/∂t = ∇²u | Heat equation |
| Hyperbolic | ∂²u/∂t² = ∇²u | Wave equation |

### Finite Difference Method

Replace derivatives with differences:
```
∂²u/∂x² ≈ (u_{i+1} - 2u_i + u_{i-1})/h²
```

### Finite Difference Laplacian

In 2D:
```
∇²u ≈ (u_{i+1,j} + u_{i-1,j} + u_{i,j+1} + u_{i,j-1} - 4u_{i,j})/h²
```

### Stability Analysis

Von Neumann stability analysis:
```
G = amplification factor
```

Method stable if |G| ≤ 1.

### Explicit Methods

Forward time, centered space (FTCS):
```
u^{n+1}_j = u^n_j + r(u^n_{j+1} - 2u^n_j + u^n_{j-1})
```

r = Δt/Δx² must satisfy r ≤ 1/2 for stability.

### Implicit Methods

Backward time, centered space (BTCS):
```
-r u^{n+1}_{j-1} + (1+2r)u^{n+1}_j - r u^{n+1}_{j+1} = u^n_j
```

Unconditionally stable.

### Crank-Nicolson

Trapezoidal in time:
```
(1 + rL/2)u^{n+1} = (1 - rL/2)u^n
```

Second order in time and space.

### Alternating Direction Implicit (ADI)

Split into x and y directions:
- 2D and 3D problems
- Tridiagonal solves

### Finite Element Method

Weak form: multiply by test function, integrate:
```
∫ Ω ∇v · ∇u dΩ = ∫ Ω v f dΩ + ∫ ∂Ω v g ds
```

Discretize with basis functions.

### Finite Element Steps

1. Define mesh
2. Choose basis functions
3. Assemble stiffness matrix
4. Apply boundary conditions
5. Solve linear system

### Spectral Methods

Expand in basis functions:
```
u(x) = Σ a_n φ_n(x)
```

Derivative: differentiate coefficients analytically.
Fast: use FFT.

### Galerkin Spectral

Project equation onto basis:
```
⟨φ_m, L(Σa_n φ_n)⟩ = ⟨φ_m, f⟩
```

Coefficients satisfy ODE system.

### Pseudo-Spectral

Evaluate nonlinear terms in physical space:
- Transform to spectral
- Differentiate
- Transform back
- Handle nonlinear in physical

-----

## Molecular Dynamics

### Newton's Equations

Molecular dynamics solves:
```
m_i a_i = F_i = -∇_i U
```

Integration: Verlet, velocity Verlet.

### Velocity Verlet

```
r(t+Δt) = r(t) + v(t)Δt + ½a(t)Δt²
v(t+Δt/2) = v(t) + ½a(t)Δt
Calculate a(t+Δt)
v(t+Δt) = v(t+Δt/2) + ½a(t+Δt)Δt
```

Energy conservation: good.

### Time Step

Typically 1-2 fs for water:
- Fast vibrations (O-H stretch) ~4000 cm⁻¹
- Δt << shortest period

### Potential Energy Functions

Lennard-Jones:
```
U(r) = 4ε[(σ/r)¹² - (σ/r)⁶]
```

Morse:
```
U(r) = D_e(1 - e^{-a(r-r_e)})²
```

### Force Calculation

O(N²) for N particles:
- Cutoff at ~2.5σ
- Neighbor lists reduce to O(N)

### Periodic Boundary Conditions

Simulate bulk:
- Copy infinite lattice
- Minimum image convention
- Ewald for electrostatics

### Ewald Summation

Split Coulomb into short/long range:
- Real space: screened
- Reciprocal space: wave sum
- O(N^{3/2}) vs O(N²)

### Temperature Control

**Thermostat**: Nose-Hoover, Langevin:
- Samples canonical ensemble
- Couples to heat bath

### Pressure Control

**Barostat**: Nose-Hoover, Parrinello-Rahman:
- Samples isothermal-isobaric
- Changes box size/shape

### Ensembles

| Ensemble | Variables | Application |
|----------|-----------|-------------|
| NVE | N, V, E | Microcanonical |
| NVT | N, V, T | Canonical |
| NPT | N, P, T | Isobaric-isothermal |
| μVT | μ, V, T | Grand canonical |

### Free Energy Calculations

- Thermodynamic integration
- Umbrella sampling
- Metadynamics
- Free energy perturbation

-----

## Monte Carlo Methods

### Random Number Generation

**Linear congruential generator**:
```
x_{n+1} = (a x_n + c) mod m
```

Quality: Mersenne Twister, xorshift.

### Metropolis-Hastings Algorithm

1. Propose new state x' from q(x'|x)
2. Accept with probability A = min(1, p(x')q(x|x')/(p(x)q(x'|x)))
3. If reject, keep old state

For symmetric q: A = min(1, p(x')/p(x))

### Ising Model Simulation

```
ΔE = 2J Σ_{⟨ij⟩} S_i S_j
```

Flip spin with Metropolis criterion.

### Importance Sampling

Choose proposal distribution to reduce variance:
```
w(x) ≈ target distribution
```

### Variance Reduction

- Antithetic variates
- Control variates
- Stratified sampling
- Importance sampling

### Monte Carlo Integration

```
I = ∫ f(x) p(x) dx ≈ (1/N) Σ f(x_i)/p(x_i)
```

Error: σ/√N independent of dimension.

### Simulated Annealing

Optimize by slowly reducing temperature:
- T high: explore broadly
- T low: settle into minimum

### Parallel Tempering (Replica Exchange)

Simulate at multiple temperatures:
- Swap configurations
- Improves sampling

### Quantum Monte Carlo

- Path integral Monte Carlo
- Variational Monte Carlo
- Diffusion Monte Carlo

### Lattice Gauge Theory

Monte Carlo for QCD:
- SU(3) link variables
- Wilson action
- HMC algorithm

-----

## Spectral Methods

### Fourier Series

```
f(x) = Σ a_k e^{ikx}
```

Derivative: ik a_k
Integral: -i a_k / k

### Fast Fourier Transform (FFT)

O(N log N) vs O(N²) DFT:
```
X_k = Σ_{n=0}^{N-1} x_n e^{-i2πkn/N}
```

### FFT Applications

- Solving PDEs
- Convolution/correlation
- Spectral analysis

### Chebyshev Polynomials

T_n(cos θ) = cos(nθ):
- Roots: Chebyshev nodes
- Near-minimax approximation

### Collocation Method

Satisfy PDE at collocation points:
- Non-periodic: Chebyshev
- Periodic: Fourier

### Domain Decomposition

Split into subdomains:
- Schwarz methods
- N-body with FFT

### Pseudo-Spectral

Nonlinear terms in physical space:
- Aliasing errors
- 2/3 rule removes high modes

### Multi-Grid

Accelerate iterative solvers:
- Restrict to coarse grid
- Solve, interpolate back
- Multiple levels

-----

## High-Performance Computing

### Parallelization Strategies

| Level | Unit |
|-------|------|
| Bit | SIMD, vector |
| Instruction | ILP |
| Thread | Shared memory |
| Process | Distributed memory |

### OpenMP

Shared memory pragmas:
```
#pragma omp parallel for
for (i = 0; i < N; i++) {
    // work
}
```

### MPI

Distributed memory messaging:
- Point-to-point: Send, Recv
- Collectives: Allreduce, Allgather

### CUDA/OpenCL

GPU computing:
- Kernels execute on device
- Memory transfer: host/device
- Threads in blocks/grid

### GPU Memory Hierarchy

| Memory | Scope | Speed |
|--------|-------|-------|
| Register | Thread | Fastest |
| Shared | Block | Fast |
| Global | All | Slow |

### Roofline Model

Performance bound:
- Compute bound: peak FLOPS
- Memory bound: bandwidth

### Load Balancing

Distribute work evenly:
- Static: pre-determined
- Dynamic: adapt at runtime

### Communication Optimization

- Reduce messages
- Overlap compute/comm
- Collective algorithms

### Strong vs. Weak Scaling

- Strong: fixed problem, more CPUs
- Weak: larger problem, more CPUs

### Amdahl's Law

Parallel fraction limits speedup:
```
S(p) = 1/(f + (1-f)/p)
```

-----

## Solving Linear Systems

### Direct Methods

**LU Decomposition**: A = LU
- Gaussian elimination
- O(n³)
- Stable with pivoting

**Cholesky**: A = LL^T for symmetric positive definite.

### Iterative Methods

| Method | Convergence | Application |
|--------|-------------|-------------|
| Jacobi | Slow | Simple |
| Gauss-Seidel | Better | SPD matrices |
| SOR | Parameter-dependent | General |
| Conjugate Gradient | Fast | SPD |
| GMRES | Minimal residual | General |

### Conjugate Gradient

For SPD systems:
```
x_{k+1} = x_k + α_k p_k
```

Krylov subspace methods.

### Preconditioning

Improve convergence:
- ILU: incomplete LU
- Jacobi: diagonal
- Multigrid: coarse grid

### Sparse Matrices

Store only non-zeros:
- CSR, COO formats
- Exploit sparsity in solvers

### Fast Multipole Method (FMM)

O(N) N-body:
- Expand multipoles
- Translate between boxes

-----

## Eigenvalue Problems

### Power Iteration

Find largest eigenvalue:
```
x_{k+1} = Ax_k
x_{k+1} ← x_{k+1}/|x_{k+1}|
```

### Inverse Power

Find eigenvalue near σ:
```
(A - σI)^{-1}x
```

### QR Algorithm

Compute all eigenvalues:
- Shifts for convergence
- O(n³) for dense

### Lanczos Method

Krylov subspace for largest eigenvalues:
- Sparse matrices
- Approximate eigenvectors

### Davidson Method

For large sparse:
- Preconditioned subspace iteration
- Good for diagonal dominant

### Singular Value Decomposition

A = UΣV^T:
- Applications: PCA, image processing
- Computing: Golub-Reinsch

-----

## Validation and Verification

### Code Testing

- Unit tests
- Integration tests
- Regression tests

### Analytical Solutions

Compare against:
- Known exact solutions
- Simplified models
- Asymptotic limits

### Convergence Testing

Refine resolution:
- Show expected order
- Estimate error

### Benchmarking

Compare against:
- Established codes
- Experiments
- Theoretical limits

### Uncertainty Quantification

- Propagate errors
- Sensitivity analysis
- Monte Carlo error

### Debugging Tools

- Debuggers (gdb, lldb)
- Memory checkers (valgrind)
- Profilers (gprof, perf)

-----

## Common Errors to Avoid

- Using unstable numerical methods
- Not checking convergence
- Ignoring numerical precision
- Forgetting boundary conditions
- Wrong time step units
- Not validating against known solutions
- Confusing periodic and aperiodic boundary conditions
- Underestimating O(N²) scaling
- Ignoring cache effects
- Not using appropriate data structures

-----

## Key References

- **Numerical Recipes** by Press et al. — Practical algorithms
- **Computational Physics** by Landau & Paez — Introduction
- **Monte Carlo Statistical Methods** — Monte Carlo
- **Spectral Methods** by Canuto et al. — Spectral methods

