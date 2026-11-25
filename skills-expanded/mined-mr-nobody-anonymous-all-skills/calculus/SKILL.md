---
name: calculus
description: "Limits, derivatives, integrals, sequences, series, multivariable calculus, and vector calculus"
category: mathematics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mathematics/calculus/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Calculus

## Scope
Calculus is the mathematical study of continuous change. This skill covers single-variable calculus (differentiation and integration), multivariable calculus, and vector calculus.

## Single-Variable Calculus

### Limits
- lim(x→a) f(x) = L means f(x) can be made arbitrarily close to L
- **L'Hôpital's Rule**: If lim f/g gives 0/0 or ∞/∞, then lim f/g = lim f'/g'
- **Squeeze theorem**: If g(x) ≤ f(x) ≤ h(x) and lim g = lim h = L, then lim f = L

### Derivatives
- **Definition**: f'(x) = lim(h→0) [f(x+h) - f(x)]/h
- **Rules**: Product (fg)' = f'g + fg', Quotient (f/g)' = (f'g - fg')/g², Chain: (f∘g)' = f'(g(x))·g'(x)
- **Common**: d/dx[xⁿ] = nxⁿ⁻¹, d/dx[eˣ] = eˣ, d/dx[ln x] = 1/x, d/dx[sin x] = cos x

### Integration
- **Fundamental Theorem**: ∫ₐᵇ f(x)dx = F(b) - F(a) where F' = f
- **Techniques**: Substitution, integration by parts (∫u dv = uv - ∫v du), partial fractions, trig substitution
- **Improper integrals**: Convergence tests (comparison, limit comparison, p-test)

### Series
- **Taylor series**: f(x) = Σ f⁽ⁿ⁾(a)(x-a)ⁿ/n!
- **Key expansions**: eˣ = Σ xⁿ/n!, sin x = Σ (-1)ⁿx²ⁿ⁺¹/(2n+1)!, 1/(1-x) = Σ xⁿ (|x|<1)
- **Convergence tests**: Ratio test, root test, integral test, alternating series test

## Multivariable Calculus
- **Partial derivatives**: ∂f/∂x, ∂f/∂y; chain rule for multivariable functions
- **Gradient**: ∇f = (∂f/∂x, ∂f/∂y, ∂f/∂z) — points in direction of steepest ascent
- **Multiple integrals**: ∬f dA, ∭f dV; change variables with Jacobian
- **Optimization**: Set ∇f = 0, classify with Hessian matrix (second derivative test)

## Vector Calculus
- **Divergence**: ∇·F = ∂Fₓ/∂x + ∂Fᵧ/∂y + ∂F_z/∂z (scalar, measures source/sink)
- **Curl**: ∇×F (vector, measures rotation)
- **Line integrals**: ∫_C F·dr = ∫ₐᵇ F(r(t))·r'(t) dt
- **Surface integrals**: ∬_S F·dS = ∬_D F·(rᵤ × rᵥ) dA
- **Divergence Theorem**: ∭_V (∇·F) dV = ∯_S F·dS
- **Stokes' Theorem**: ∬_S (∇×F)·dS = ∮_C F·dr
- **Green's Theorem**: ∮_C (P dx + Q dy) = ∬_D (∂Q/∂x - ∂P/∂y) dA

## Tools
- **Wolfram Alpha / Mathematica**: Symbolic computation
- **SymPy (Python)**: Free symbolic mathematics
- **MATLAB**: Numerical integration, ODE solvers
- **GeoGebra**: Visualization of calculus concepts

## References
- Stewart — *Calculus: Early Transcendentals*
- Spivak — *Calculus*
- Apostol — *Calculus* (Vols. 1-2)
