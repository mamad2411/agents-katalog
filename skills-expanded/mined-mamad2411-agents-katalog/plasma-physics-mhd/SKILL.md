---
name: plasma-physics-mhd
description: Expertise in Magnetohydrodynamics (MHD), kinetic theory, and plasma stability analysis.
version: 1.0.0
---

# Plasma Physics & MHD Skill

<skill_definition>
This skill handles the behavior of the ionized gas. It uses the Grad-Shafranov equation to find equilibrium, analyzes instabilities (Kink, Ballooning, Tearing), and models transport (how fast heat leaks out).
</skill_definition>

<usage_instructions>
1.  **Equilibrium**: Solve for the magnetic flux surfaces (nested toroids).
2.  **Stability**: Check the Troyon limit (Beta limit) and Greenwald limit (Density limit).
3.  **Transport**: Estimate energy confinement time (tau_E) using scaling laws like ITER98(y,2).
4.  **Heating**: Model interactions of alpha particles and external heating (NBI, RF).
</usage_instructions>

<output_template>
## Plasma Profile
*   **Central Temperature**: 15 keV
*   **Density**: 1e20 m^-3
*   **Beta_N**: 2.5 (Stable)
*   **Confinement Time**: 3.2 seconds
</output_template>
