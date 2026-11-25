---
name: classical-mechanics
description: "Newtonian mechanics: kinematics, dynamics, conservation laws, rigid body motion, Lagrangian and Hamiltonian formulations"
category: physics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/physics/classical-mechanics/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Classical Mechanics

## Scope
Classical mechanics covers the motion of macroscopic objects under forces, from point particles to rigid bodies and continuous media. This skill provides the analytical frameworks, solution strategies, and computational approaches used in physics and engineering.

## Core Frameworks

### Newton's Laws
1. **Inertia**: A body remains at rest or in uniform motion unless acted upon by a net external force.
2. **F = ma**: The net force on a body equals its mass times its acceleration. In component form: Σ Fₓ = m·aₓ, Σ Fᵧ = m·aᵧ, Σ F_z = m·a_z.
3. **Action-Reaction**: For every force, there exists an equal and opposite reaction force on the other body.

### Kinematics Equations (Constant Acceleration)
- v = v₀ + at
- x = x₀ + v₀t + ½at²
- v² = v₀² + 2a(x - x₀)

### Conservation Laws
- **Energy**: K₁ + U₁ + W_nc = K₂ + U₂ where K = ½mv², U = mgh (gravitational), U = ½kx² (elastic)
- **Momentum**: Σp_before = Σp_after (when net external force = 0)
- **Angular Momentum**: L = Iω = r × p, conserved when net external torque = 0

### Lagrangian Mechanics
The Lagrangian L = T - V, where T is kinetic energy and V is potential energy. The Euler-Lagrange equation:
d/dt(∂L/∂q̇ᵢ) - ∂L/∂qᵢ = Qᵢ (generalized non-conservative forces)

**When to use Lagrangian over Newtonian**:
- Systems with constraints (pendulums, pulleys, tracks)
- Generalized coordinates simplify the problem
- Constraint forces are not needed

### Hamiltonian Mechanics
H = Σ pᵢq̇ᵢ - L. Hamilton's equations: q̇ᵢ = ∂H/∂pᵢ, ṗᵢ = -∂H/∂qᵢ
Used when: phase-space analysis is needed, canonical transformations simplify the problem, or transitioning to quantum mechanics.

## Problem-Solving Methodology
1. **Identify the system**: Draw a free-body diagram. List all forces (gravity, normal, friction, tension, spring, applied).
2. **Choose coordinates**: Pick axes aligned with motion or constraints. Use generalized coordinates for complex systems.
3. **Apply appropriate framework**: Newton for simple problems, Lagrange for constrained systems, Hamilton for phase-space analysis.
4. **Apply initial/boundary conditions**: Solve for unknowns using given values.
5. **Verify**: Check dimensions, limiting cases, energy conservation.

## Computational Tools
- **Python**: `scipy.integrate.odeint` for numerical solutions to equations of motion
- **Mathematica/Wolfram**: Symbolic Lagrangian computation
- **MATLAB/Octave**: ODE solvers (`ode45`, `ode23`)
- **VPython/GlowScript**: 3D visualization of motion

## Standards & References
- Goldstein, Poole & Safko — *Classical Mechanics* (3rd ed.)
- Taylor — *Classical Mechanics*
- Landau & Lifshitz — *Mechanics* (Course of Theoretical Physics, Vol. 1)
