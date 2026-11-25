---
name: ltspice
description: "Progressive-disclosure workflow for LTSpice / PyLTSpice circuit simulation. Use whenever the user wants to create a netlist, run a SPICE transient or AC simulation, inspect traces, or debug LTSpice convergence through PowerMCP — even when they just say 'simulate this circuit', 'why won't this conver"
category: electrical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Power-Agent/PowerSkills"
source_repository: "Power-Agent/PowerSkills"
source_path: "powerskills-tool/skills/ltspice/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# LTSpice workflow

Start with a runnable netlist and a clean batch simulation. Use plotting and GUI steps only after the run succeeds.

## Default tool ladder
1. `create_rc_transient_netlist(...)` for a minimal example, or `create_simulation_session(netlist_text)` for a real case.
2. `run_simulation(netlist_path, session_dir)` to generate the raw and log files.
3. `read_simulation_log(log_file_path)` if the run fails or looks suspicious.
4. `list_available_traces(raw_file_path)` before requesting plots.
5. `plot_specific_traces(raw_file_path, session_dir, trace_names)` for focused waveform review.
6. `view_netlist_in_ltspice(netlist_path)` only when the GUI is actually needed.

## Working rules
- Do not ask for broad plotting until the log is clean and the available traces are known.
- Simplify the netlist and shorten the run before tuning tolerances.
- Use a minimal reproducible circuit to debug startup or convergence issues.

## Deliver
- The netlist used and whether the batch run succeeded.
- The traces inspected.
- The likely root cause if the simulation misbehaved.
