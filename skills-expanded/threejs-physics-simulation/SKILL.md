---
name: threejs-physics-simulation
description: Build calibrated physics and numerical simulations for Three.js or learning labs. Use for forces, motion, collisions, rigid bodies, springs, pendulums, levers, fluids approximations, fields, electricity, density, heat, optics, particles, Babylon/cannon-es physics, timestep logic, units, and deterministic simulation controls.
---

# Three.js Physics Simulation

Prefer analytical simulation over a physics engine when the phenomenon is simple. Use an engine only when collision/contact dynamics are the lesson.

## Choose The Solver

- Formula update: Coulomb force, density, capacitance, heat equation demos, optics rays, fields, graphs.
- Fixed-step integrator: projectile motion, pendulum, springs, particles, orbital toy models.
- `cannon-es`: rigid bodies, gravity, contact, vehicle/rover-like motion, stack/collision demos.
- Babylon physics plugin: use only in existing Babylon scenes.

## Requirements

- Define units and constants before code.
- Separate simulation state from visual meshes.
- Use fixed timestep or bounded delta for time-based simulation.
- Clamp inputs to physically meaningful ranges.
- Keep a reset path that restores state, not just camera.
- Leave calibration constants for physical-world approximations.
- Show the equation/result near the control, not hidden in code.

## Minimal Loop

For custom simulation:

```ts
const FIXED_DT = 1 / 60;
let accumulator = 0;

function frame(deltaSeconds: number) {
  accumulator += Math.min(deltaSeconds, 0.1);
  while (accumulator >= FIXED_DT) {
    stepSimulation(FIXED_DT);
    accumulator -= FIXED_DT;
  }
  syncMeshesFromState();
}
```

## References

Read `references/physics-patterns.md` for formulas, timestep, `cannon-es`, fields, and validation.
