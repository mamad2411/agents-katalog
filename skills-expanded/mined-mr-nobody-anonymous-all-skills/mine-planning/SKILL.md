---
name: mine-planning
description: "Strategic and operational mine planning: pit optimization, sequencing, scheduling, cut-off grade analysis, and production planning"
category: mining
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mining/mine-planning/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Mine Planning

## Scope
Mine planning encompasses the strategic and tactical decisions that convert a mineral resource into a profitable, safe, and compliant mining operation. This skill covers pit optimization, production scheduling, cut-off grade analysis, and mine design.

## Resource Model Foundation
- **Block model**: 3D grid of blocks, each with estimated grade, tonnage, density, rock type
- **Kriging**: Geostatistical interpolation (ordinary, simple, indicator kriging)
- **Variogram**: Spatial correlation model: γ(h) = ½ Var[Z(x+h) - Z(x)]
  - Components: nugget, sill, range
  - Models: spherical, exponential, Gaussian

## Pit Optimization
- **Lerchs-Grossmann algorithm**: Graph-based method for optimal ultimate pit limit (UPL)
- **Floating cone**: Simplified but sub-optimal cone-based approach
- **Block economic value**: V = (Grade × Recovery × Price - Processing Cost) × Tonnage - Mining Cost × Tonnage
- **Revenue factor / pit shells**: Generate nested pits at varying commodity prices → pit-by-pit graph for strategy

### Cut-Off Grade
- **Break-even cut-off**: Grade where mining revenue = total cost
  - g_cutoff = (Mining + Processing + G&A) / (Recovery × Price × Payable)
- **Lane's model**: Optimizes cut-off considering mine, mill, and market capacities
- **Opportunity cost**: Include the value of displacing ore from the schedule

## Production Scheduling
- **Long-term (strategic)**: 5-20 year LOM plan; annual or quarterly periods
- **Medium-term (tactical)**: 1-5 year detail; monthly periods
- **Short-term (operational)**: Weekly/daily schedules; equipment allocation

### Scheduling Optimization
- **Linear programming (LP)**: Maximize NPV subject to:
  - Mining rate constraints (equipment capacity)
  - Processing rate constraints (mill throughput)
  - Blending constraints (grade, deleterious elements)
  - Slope stability (geotechnical)
  - Sequencing precedences (can't mine below before above)
- **MIP (Mixed Integer Programming)**: Binary variables for block selection by period
- **Heuristic methods**: Genetic algorithms, simulated annealing for large problems

## Mine Design (Open Pit)
- **Bench geometry**: Bench height (typically 10-15m), bench width, catch berms
- **Inter-ramp slope angle**: Typically 40-55° depending on rock quality
- **Ramp design**: Grade ≤ 10% (1 in 10), width = 2.5 × truck width + clearance
- **Haulage optimization**: Truck-shovel fleet matching, dispatch systems

## Underground Mine Planning
- **Methods**: Room-and-pillar, cut-and-fill, sublevel stoping, block caving, longwall
- **Method selection**: Based on ore body geometry, rock quality, grade, depth
- **Stope optimization**: Maximize extracted value while maintaining structural integrity
- **Ventilation planning**: Required airflow = f(equipment diesel kW, personnel, blasting gases)

## Software Tools
- **Whittle (Dassault)**: Strategic pit optimization (Lerchs-Grossmann)
- **MineSched / Minemax**: Production scheduling
- **Surpac / Vulcan / Datamine**: Geological modeling and mine design
- **GEOVIA (Dassault)**: Integrated mine planning suite
- **Deswik**: Modern mine planning and scheduling

## Standards & References
- CIM/JORC/NI 43-101 — Mineral Resource/Reserve reporting standards
- SME Mining Engineering Handbook
- Hustrulid, Kuchta & Martin — *Open Pit Mine Planning and Design*
