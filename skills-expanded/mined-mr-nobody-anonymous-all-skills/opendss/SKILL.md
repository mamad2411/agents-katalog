---
name: opendss
description: "Progressive-disclosure workflow for OpenDSS distribution-feeder studies. Use whenever the user wants to compile a DSS model, solve a distribution circuit, inspect feeder bus voltages or power, sweep load multipliers, or run daily / harmonic studies through PowerMCP — even when they just say 'solve t"
category: electrical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Power-Agent/PowerSkills"
source_repository: "Power-Agent/PowerSkills"
source_path: "powerskills-tool/skills/opendss/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# OpenDSS workflow

Start with a solved feeder. Do not jump to daily or harmonic studies until the base feeder compiles and the voltage profile is understood.

## Default tool ladder
1. `compile_and_solve(dss_file)` to load and solve the circuit.
2. `get_total_power()` and `get_bus_voltages()` to confirm the base operating point.
3. `set_load_multiplier(load_mult)` for simple scenario sweeps.
4. `run_daily_energy_meter(meter_name, hours)` for daily feeder behavior.
5. `get_harmonic_results(load_name, harmonic)` only after the harmonic question is well scoped.

## Working rules
- Fix compile or solve errors before any scenario analysis.
- For voltage issues, inspect the weak buses first.
- Separate load-growth screening from harmonic analysis; they answer different questions.
- Keep feeder, meter, and load names explicit in the response.

## Escalation triggers
Quote the weak bus + voltage or the loaded element rather than saying "there is a problem".

| Observation | Escalate to |
|---|---|
| `get_bus_voltages` shows pu outside the feeder band (e.g. < 0.95 or > 1.05) | `voltage-violation-mitigation` |
| A line, transformer, or regulator loaded above its rating | `thermal-overload-mitigation` |
| `compile_and_solve` succeeds to compile but the solution diverges | `convergence-failure-mitigation` |
| The study is DER (PV, storage) integration or hosting capacity on the feeder | `der-hosting-capacity-mitigation` |

## Deliver
- The compiled feeder and base-case status.
- The voltage or power quantities checked.
- Any scenario result and whether mitigation is needed.
