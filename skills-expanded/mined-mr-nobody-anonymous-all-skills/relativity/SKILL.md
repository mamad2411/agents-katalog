---
name: relativity
description: "Special and general relativity: Lorentz transformations, spacetime geometry, Einstein field equations, black holes, gravitational waves"
category: physics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/physics/relativity/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Relativity

## Scope
Einstein's theories of special and general relativity describe physics at high velocities and in strong gravitational fields. This skill covers both theories, their mathematical frameworks, experimental predictions, and computational methods.

## Special Relativity

### Postulates
1. The laws of physics are the same in all inertial reference frames
2. The speed of light c is the same in all inertial frames

### Lorentz Transformations
- γ = 1/√(1 - v²/c²) (Lorentz factor)
- t' = γ(t - vx/c²)
- x' = γ(x - vt)
- **Time dilation**: Δt = γΔt₀
- **Length contraction**: L = L₀/γ
- **Velocity addition**: u' = (u - v)/(1 - uv/c²)

### Four-Vectors
- **Spacetime interval**: ds² = -c²dt² + dx² + dy² + dz² (invariant)
- **Four-momentum**: pᵘ = (E/c, p), where E² = (pc)² + (mc²)²
- **Mass-energy**: E = γmc², rest energy E₀ = mc²

## General Relativity

### Core Principles
- **Equivalence principle**: Gravitational and inertial mass are identical; locally, gravity is indistinguishable from acceleration
- **Spacetime curvature**: Matter tells spacetime how to curve; spacetime tells matter how to move

### Einstein Field Equations
Gᵤᵥ + Λgᵤᵥ = (8πG/c⁴)Tᵤᵥ

Where: Gᵤᵥ = Rᵤᵥ - ½Rgᵤᵥ (Einstein tensor), Λ (cosmological constant), Tᵤᵥ (stress-energy tensor)

### Key Solutions
| Solution | Metric | Application |
|----------|--------|-------------|
| Schwarzschild | ds² = -(1-2GM/rc²)c²dt² + dr²/(1-2GM/rc²) + r²dΩ² | Non-rotating black holes, weak fields |
| Kerr | Rotating black hole metric (Boyer-Lindquist coords) | Rotating black holes |
| FLRW | ds² = -c²dt² + a(t)²[dr²/(1-kr²) + r²dΩ²] | Cosmology, expanding universe |

### Predictions & Tests
- **Gravitational redshift**: Δf/f = -ΔΦ/c²
- **Gravitational lensing**: θ = 4GM/(rc²) (point mass deflection)
- **Gravitational waves**: h ~ (4G/c⁴)(d²I/dt²)/r (quadrupole formula)
- **Perihelion precession**: Δφ = 6πGM/(ac²(1-e²)) per orbit
- **GPS corrections**: ~38 μs/day time dilation compensation required

## Computational Tools
- **SageMath/SageManifolds**: Tensor calculus on differentiable manifolds
- **xAct (Mathematica)**: Tensor computer algebra for GR
- **Einstein Toolkit**: Open-source numerical relativity (Cactus framework)
- **Python**: `einsteinpy` for symbolic GR calculations

## Standards & References
- Carroll — *Spacetime and Geometry*
- Hartle — *Gravity: An Introduction to Einstein's General Relativity*
- Misner, Thorne & Wheeler — *Gravitation*
- LIGO Scientific Collaboration — gravitational wave data (gwosc.org)
