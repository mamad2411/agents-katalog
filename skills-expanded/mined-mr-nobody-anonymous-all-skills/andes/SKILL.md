---
name: andes
description: "Progressive-disclosure workflow for ANDES dynamic studies. Use whenever the user wants to run ANDES through PowerMCP for power flow, small-signal / eigenvalue analysis, or time-domain simulation — even when they just say 'check the damping', 'is this stable', 'run a fault', or 'look at the oscillati"
category: electrical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Power-Agent/PowerSkills"
source_repository: "Power-Agent/PowerSkills"
source_path: "powerskills-tool/skills/andes/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# ANDES workflow

Expose ANDES tools in stages. Do not jump into dynamics until the base case is loaded, solved, and understood.

## Default tool ladder
1. `run_power_flow(file_path)` to load the case and solve the steady-state point.
2. `get_system_info()` to summarize buses, generators, dynamic states, and controls.
3. `run_eigenvalue_analysis(file_path)` to screen oscillatory modes and poor damping.
4. `run_time_domain_simulation(step_size, t_end)` only after the disturbance and success criteria are explicit.

### Example sequence
Illustrative run on an ANDES-bundled case:
```
run_power_flow("ieee14.xlsx")           -> base case solved, 14 buses, 5 generators
get_system_info()                       -> dynamic models, governor and exciter types
run_eigenvalue_analysis("ieee14.xlsx")  -> dominant mode 0.42 Hz, damping 3.1%
run_time_domain_simulation(0.01, 10.0)  -> generator trip at t=1s, monitor rotor angles
```
The 3.1% damping is below the ~5% screening threshold, so this case escalates to
`dynamic-stability-mitigation` rather than stopping at "the modes look weak".

## Working rules
- Re-run the base power flow after any model or dispatch change before dynamic work.
- State the disturbance, clearing time, monitored channels, and pass or fail criteria before time-domain runs.
- Treat eigenvalue results as screening. Confirm critical cases in time domain.

## Escalation triggers
Quote the failing metric (mode + damping ratio, channel + recovery time) rather than saying "it is unstable".

| Observation | Escalate to |
|---|---|
| Eigenvalue with damping ratio below ~5% or any right-half-plane mode | `dynamic-stability-mitigation` |
| Time-domain run shows growing angles, sustained oscillations, or failed voltage recovery | `dynamic-stability-mitigation` |
| Base power-flow voltages outside [0.95, 1.05] pu | `voltage-violation-mitigation` |
| Frequency nadir, RoCoF, or settling frequency violates its limit after a generation-loss event | `frequency-response-mitigation` |

## Deliver
- The case used and whether the base case solved.
- The dynamic issue being checked.
- The main result and whether mitigation is now required.
