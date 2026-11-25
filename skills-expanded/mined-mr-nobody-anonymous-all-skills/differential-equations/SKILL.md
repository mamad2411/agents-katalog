---
name: differential-equations
description: "ODEs and PDEs: solution methods, existence/uniqueness, boundary value problems, and dynamical systems"
category: mathematics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mathematics/differential-equations/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Differential Equations

## Scope
Differential equations describe relationships between functions and their derivatives. This skill covers ordinary differential equations (ODEs), partial differential equations (PDEs), solution techniques, and qualitative analysis.

## Ordinary Differential Equations (ODEs)

### First-Order ODEs
| Type | Form | Solution Method |
|------|------|----------------|
| Separable | dy/dx = f(x)g(y) | ∫dy/g(y) = ∫f(x)dx |
| Linear | y' + P(x)y = Q(x) | Integrating factor: μ = exp(∫P dx) |
| Exact | M dx + N dy = 0 where ∂M/∂y = ∂N/∂x | F(x,y) = ∫M dx + g(y) |
| Bernoulli | y' + P(x)y = Q(x)yⁿ | Substitution v = y¹⁻ⁿ |

### Second-Order Linear ODEs
ay'' + by' + cy = f(x)

**Homogeneous (f = 0)**: Characteristic equation ar² + br + c = 0
- Two real roots r₁ ≠ r₂: y = c₁e^(r₁x) + c₂e^(r₂x)
- Repeated root r: y = (c₁ + c₂x)e^(rx)
- Complex roots α ± βi: y = e^(αx)(c₁ cos βx + c₂ sin βx)

**Particular solution methods**:
- Undetermined coefficients (for polynomial, exponential, trig forcing)
- Variation of parameters: yₚ = u₁y₁ + u₂y₂ where u₁'y₁ + u₂'y₂ = 0

### Systems of ODEs
- x' = Ax → x(t) = e^(At)x₀
- **Matrix exponential**: e^(At) = PD(t)P⁻¹ where D(t) = diag(e^(λᵢt))
- **Phase plane analysis**: Classify equilibria by eigenvalues of Jacobian

### Dynamical Systems
- **Equilibrium classification**: Node (real, same sign), saddle (real, opposite sign), spiral (complex), center (purely imaginary)
- **Stability**: Asymptotically stable if all eigenvalues have Re(λ) < 0
- **Lyapunov functions**: V(x) > 0, V̇(x) < 0 → stable equilibrium
- **Bifurcations**: Saddle-node, pitchfork, Hopf, transcritical

## Partial Differential Equations (PDEs)

### Classification (2nd order, 2 variables)
- **Elliptic** (B² - 4AC < 0): Laplace/Poisson equation, steady-state problems
- **Parabolic** (B² - 4AC = 0): Heat/diffusion equation
- **Hyperbolic** (B² - 4AC > 0): Wave equation

### Key PDEs & Solutions
| Equation | Form | Solution Approach |
|----------|------|-------------------|
| Heat | uₜ = α²uₓₓ | Separation of variables, Fourier series |
| Wave | uₜₜ = c²uₓₓ | D'Alembert, normal modes |
| Laplace | uₓₓ + uᵧᵧ = 0 | Separation of variables, Green's functions |
| Schrödinger | iℏψₜ = Ĥψ | Eigenfunction expansion |

### Solution Techniques
- **Separation of variables**: u(x,t) = X(x)T(t), apply boundary conditions
- **Fourier series/transform**: Expand in orthogonal functions
- **Green's functions**: G(x,ξ) satisfying LG = δ(x-ξ)
- **Method of characteristics**: For first-order and hyperbolic PDEs

## Numerical Methods
- **Euler, RK4**: For ODE initial value problems
- **Finite difference**: Discretize spatial and temporal derivatives
- **Finite element**: Weak form with basis functions on mesh
- **Spectral methods**: Global basis functions (Fourier, Chebyshev)

## Tools
- **SciPy**: `odeint`, `solve_ivp` for ODEs
- **FEniCS/dolfinx**: FEM for PDEs in Python
- **MATLAB**: `ode45`, `pdepe`, PDE Toolbox
- **Mathematica**: `DSolve`, `NDSolve`

## References
- Boyce & DiPrima — *Elementary Differential Equations*
- Strauss — *Partial Differential Equations*
- Strogatz — *Nonlinear Dynamics and Chaos*
