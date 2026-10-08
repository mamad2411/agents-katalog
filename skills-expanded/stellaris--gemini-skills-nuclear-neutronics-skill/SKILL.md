---
name: nuclear-neutronics
description: Expertise in neutron transport, tritium breeding, radiation shielding, and material activation.
version: 1.0.0
---

# Nuclear Neutronics Skill

<skill_definition>
This skill deals with the 14.1 MeV neutrons produced by D-T fusion. It calculates how these neutrons heat the blanket, breed new fuel (Lithium -> Tritium), and damage structural materials over time.
</skill_definition>

<usage_instructions>
1.  **Tritium Breeding**: Calculate the Tritium Breeding Ratio (TBR). Must be > 1.05 for self-sufficiency.
2.  **Shielding**: Size the water/steel layers to protect the superconducting magnets from quenching.
3.  **Activation**: Estimate how radioactive the vessel will be after shutdown.
4.  **Heat Deposition**: Map where the energy is actually absorbed for thermal cycle efficiency.
</usage_instructions>

<output_template>
## Neutronics Report
*   **Reaction**: D + T -> He4 + n
*   **Neutron Wall Loading**: 2 MW/m^2
*   **TBR**: 1.12 (Self-sufficient)
*   **Magnet Shielding**: Sufficient (Fluence < limit)
</output_template>
