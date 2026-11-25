---
name: psse
description: "Progressive-disclosure workflow for PSS/E studies through PowerMCP. Use whenever the user wants to open a PSS/E case, solve the base case, discover the right PSSPY command, or run targeted PSS/E automation — even when they just say 'open this sav', 'solve it', or 'how do I change this in PSSE'. Expo"
category: electrical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Power-Agent/PowerSkills"
source_repository: "Power-Agent/PowerSkills"
source_path: "powerskills-tool/skills/psse/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# PSSE workflow

Treat PSSE as a layered interface. Start with the built-in base-case tools. Use generic `psspy` execution only after the correct command and argument shape are known.

## Default tool ladder
1. `open_case(case)`
2. `solve_case()`
3. `search_psspy_commands(query, category)` or `lookup_psspy_command(function_name)` to discover the right API entry point.
4. `run_psspy_command(function_name, arguments)` only after the command contract is explicit.

## Working rules
- Do not use `run_psspy_command` as a search tool. Search or look up first.
- Keep every executed command tied to a study objective, not just API curiosity.
- Re-solve or re-check the case after commands that alter topology, controls, or dispatch.

## Escalation triggers
Quote the bus or branch and its value rather than saying "violations exist". Use `dynamic-stability-mitigation` for dynamic-performance issues.

| Observation | Escalate to |
|---|---|
| Bus voltage < 0.95 or > 1.05 pu after `solve_case` | `voltage-violation-mitigation` |
| Branch loading above its MVA rating | `thermal-overload-mitigation` |
| Contingency run returns binding N-1 cases | `contingency-mitigation` |
| `solve_case` fails to converge | `convergence-failure-mitigation` |
| Fault duty near or above breaker interrupting ratings | `short-circuit-mitigation` |

## Deliver
- The case, the command path chosen, and why it was needed.
- The arguments passed to the command.
- The study outcome and any required mitigation.
