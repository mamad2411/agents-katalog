---
name: right-of-way-expert
description: Use when coordinating utility transmission corridors with other infrastructure (geometric conflict detection, relocation design, cost estimation, schedule risk), generating CUSPAP-style location overview narratives from an address or PIN for appraisal reports, applying easement valuation methods (percentage-of-fee, income capitalization, before/after), or planning ROW acquisition for linear infrastructure.
---

## Workflows

This skill bundles three workflows for linear-infrastructure right-of-way work. Route by task:

| If you need to... | Go to section |
|---|---|
| Identify and resolve utility conflicts in a proposed ROW corridor, design relocations, estimate costs and schedule risk | **Utility Conflict Analysis Framework** |
| Generate a CUSPAP-style location overview narrative from an address or PIN for an appraisal report | **Location Overview Generator** |
| Value a permanent or temporary easement (percentage-of-fee, income capitalization, before/after, paired sales) | Use the standalone `easement-valuation-methods` skill in the appraisal-valuation plugin — it carries the calculators and the USPAP/CUSPAP/Yellow Book/IVS compliance framework |

## Key Concepts

### Right-of-Way (ROW) Definition

**ROW** is the legal corridor needed for infrastructure operation and maintenance. Specifications vary by infrastructure type:

**Transmission Lines (Hydro):**
- Width: 20-90m depending on voltage (69kV to 500kV)
- Restrictions: No permanent structures, height limitations, access requirements
- Operators: Hydro One, municipal utilities, independent power producers

**Pipelines:**
- Width: 10-40m depending on product type and pressure
- Restrictions: No excavation within buffer zones, weight limitations, access requirements
- Operators: Enbridge Gas, Enbridge Liquid Pipelines, regional gas distributors

**Transit Corridors:**
- Width: 15-50m depending on mode (LRT, subway, commuter rail, BRT)
- Restrictions: Exclusive use, grade separation requirements, noise/vibration buffers
- Operators: Municipal transit authorities, GO Transit, provincial rail agencies

## Utility Conflict Analysis Framework

Six-phase workflow. Detailed examples, cost tables, coordination scripts, risk matrices, and best-practice expansions live in **[utility-conflict-playbook.md](utility-conflict-playbook.md)** — load it whenever you need the worked examples or the cost numbers, not the skeleton.

### Phase 1 — Utility Inventory and Conflict Identification

1. **Obtain utility locates** — submit Ontario 811 request (5-10 business days) and contact each operator directly (Hydro One, Enbridge Gas, municipal utilities, telecom, conservation authorities). Locate drawings give ±0.3m accuracy with depth, type, and specifications.
2. **Geometric conflict detection** — classify by horizontal proximity (in ROW = direct; <5m = high; 5-15m = medium; >15m = low) and by vertical interaction (parallel stacking, perpendicular crossing, grade separation).
3. **Classification matrix:**

| Conflict Type | Priority | Relocation | Timeline | Cost Impact |
|---|---|---|---|---|
| Direct conflict (in ROW) | CRITICAL | Mandatory | Months 0-3 | High |
| High risk (<5m) | HIGH | Likely | Months 1-4 | Medium-High |
| Medium risk (5-15m) | MEDIUM | Possible | Months 2-6 | Medium |
| Low risk (>15m) | LOW | Unlikely | Months 3-12 | Low |
| Overhead crossing | MEDIUM | Coordination | Months 2-5 | Medium |
| Underground crossing | HIGH | Design | Months 1-6 | Medium-High |

**Canonical example (115kV transmission corridor, 45m width):** a gas pipeline 8m from the ROW edge is HIGH RISK (requires relocation or increased clearance); a telecom cable 3m from the centerline is a DIRECT CONFLICT (mandatory relocation); a water main 12m out is MEDIUM (coordination required); a fiber line 25m out is LOW (standard notification). See playbook for the LRT vertical-conflict example and full locate-request procedure.

### Phase 2 — Relocation Design Requirements

Each utility class has standard design options. Pick by cost, schedule, and constraint fit:

- **Hydro transmission** (NESC, CSA C22.1, Hydro One standards) — new parallel route ($500K-$2M/km), underground burial ($2-$5M+/km), or clearance agreement ($10-$50K).
- **Gas pipeline** (CSA Z662, Utility Commission, Enbridge standards) — parallel relocation ($300-$800K/km), grade separation in casing ($400K-$1M), or directional drill ($600K-$1.5M).
- **Telecom / water / sewer** (CSA B411, municipal standards) — route-around, casing crossing, aerial route, parallel relocation, or pressure-main conversion depending on the asset.

Full pros/cons and per-option detail in the playbook.

### Phase 3 — Cost Estimation by Utility Type

Order-of-magnitude per-km ranges (see playbook for full pressure/voltage/diameter tables and cost-component breakdowns):

| Utility | Base range per km |
|---|---|
| Transmission line (overhead, by voltage) | $600K-$3M |
| Transmission line (underground burial) | $2.5M-$10M |
| Gas pipeline (by pressure class & method) | $200K-$1.8M |
| Telecom cable (route option dependent) | $150K-$1.6M total |
| Water main (by diameter) | $250-$1000/m |
| Sewer main (gravity or pressure) | $200-$800/m |

### Phase 4 — Coordination Timeline

Typical multi-utility corridor sequence:

```
Month 0-3:   Utility ID & design (locates → meetings → relocation design → permits)
Month 3-6:   Easements & regulatory approvals (ROW, environmental, municipal, Utility Commission)
Month 6-12:  Utility relocation execution (transmission on critical path; gas/water/sewer/telecom in parallel)
Month 12+:   Main project construction begins
```

**Critical path items and delay risk:**

1. Transmission switchover — ±3-4 months if low-demand window missed
2. Gas pressure testing — ±2-3 months for regulatory issues
3. Municipal permits — ±1-2 months
4. Environmental approvals (species at risk) — ±3-6 months

Full Gantt-style breakdown and dependency chain in the playbook.

### Phase 5 — Utility Owner Coordination

Each operator has its own stakeholder map, meeting cadence, document set, and cost allocation convention:

- **Hydro One** — ~40% project / 60% utility split; weekly meetings during switchover.
- **Enbridge Gas** — utility typically 50-75% of relocation; design approval gate at Month 3.
- **Municipal water/sewer** — project typically 75-100%; some jurisdictions require full project funding.
- **Bell/Rogers telecom** — project typically 50-100%; minimal regulatory oversight.

Detailed cadence and document checklists for each operator in the playbook.

### Phase 6 — Risk Assessment

Track schedule and budget risk on a structured register. Highest-impact items:

- Transmission switchover window missed (Medium probability, 3-4 month impact) → schedule 2-3 backup windows.
- Environmental survey required (Medium probability, 3-6 month impact) → conduct early if species at risk possible.
- Transmission line relocation cost upside +30-50% → maintain 2-3 design alternatives, negotiate utility share.

Full schedule risk table, budget risk table, specific-component escalation breakdowns, and the five mitigation strategies (early engagement, multiple options, geotech, regulatory pre-coordination, contingency planning) are in the playbook.

### Tooling

The `/right-of-way-analysis` slash command integrates conflict detection with cost estimation. See the playbook for invocation patterns and a complete sample input JSON file.

## Location Overview Generator

Generates a location overview for an Ontario property given a PIN (9 digits) or municipal address. Orchestrates geocoding, queries provincial/municipal/heritage/brownfield/TRCA/GTFS/census providers, and produces a consolidated markdown or JSON report — useful for scoping ROW conflicts, heritage constraints, and environmental flags before detailed conflict analysis.

**Run location overview:**
```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/right-of-way-expert/scripts
python3 -m Location_Overview.main "100 Queen Street West, Toronto"
python3 -m Location_Overview.main --format json "150 King Street West, Toronto"
python3 -m Location_Overview.main --no-save "123 Main Street, Mississauga"
```

**CLI flags:**
- `input` (positional) — PIN (9 digits) or municipal address
- `--format` / `-f` — `markdown` (default) or `json`
- `--no-save` — print only, do not save
- `--verbose` / `-v` — verbose logging

### When to Use

- Scoping ROW conflicts, heritage constraints, and environmental flags before detailed conflict analysis
- Drafting the "Location Overview" / "Neighbourhood Description" section of a CUSPAP-compliant appraisal report
- Address research ("describe the location of [address]") for an acquisition target
- Validating that a corridor route avoids floodplains, Heritage Conservation Districts, or contaminated sites
- Establishing regional context, transit accessibility, and planning framework for a subject property

### Three-Phase Workflow

The Python script handles **Phase 1** (API data collection). Phases 2 and 3 are performed in-conversation by the model after reading the script output.

1. **Phase 1 — API Data Collection (automated)** — parse input as PIN (9 consecutive digits, e.g. `123456789` or `12345-6789`) vs. address; geocode and resolve municipality; query Nominatim, Ontario GeoHub, Toronto/Ottawa Open Data, Overpass API, Heritage Registry, Brownfields ESR, TRCA Conservation, Transit GTFS, Census Demographics; emit consolidated markdown or JSON.
2. **Phase 2 — Deep Web Research (skip when speed matters)** — supplement API data using `WebSearch` and `WebFetch` across five domains: Municipal Planning, Heritage, Environmental, Development Activity, Market Context. Full query templates and municipality-specific anchor domains in **[location-overview-playbook.md](location-overview-playbook.md)**.
3. **Phase 3 — Narrative Synthesis** — combine API output and web findings into flowing prose suitable for direct paste into an appraisal report. Do **not** emit tables or bullet lists in the final narrative.

### Narrative Output Structure

The narrative must follow CUSPAP location description conventions and cover all ten sections in order: (1) Property Identification, (2) Regional Context, (3) Neighbourhood Description, (4) Transportation & Accessibility, (5) Amenities & Services, (6) Planning Framework, (7) Development Activity, (8) Environmental Considerations, (9) Market Context, (10) Conclusion.

Full paragraph counts, content checklists, and CUSPAP-specific guidance per section are in the playbook.

### Quality Criteria

- **Prose, not tables** — reads like an appraisal report section, not a data dump.
- **Specificity over generality** — name the building, developer, Secondary Plan, transit station, conservation authority; quantify distances.
- **Attribute findings** — note API data vs. web research so a reviewer can verify.
- **Flag uncertainty** — explicitly note when planning application status, environmental clearance, or assessment data could not be confirmed; recommend verification.
- **Respect the limits** — no PIN-to-address resolution via OnLand/Teranet; MPAC requires paid subscription; web-sourced planning status may be stale.

### Save Convention

Save the final narrative to:
`$CLAUDE_PROJECT_DIR/Reports/YYYY-MM-DD_HHMMSS_location_overview_narrative_[address_slug].md`

Present to the user: the full narrative text in chat, the saved file path, the list of data sources used (API + web), and verification recommendations for any uncertain items.

## Best Practices (summary)

1. **Early utility engagement** (Month 0-1, not 3-4) — saves 2-3 months by identifying fatal flaws before detailed engineering.
2. **Systematic conflict documentation** — spreadsheet with utility, location, type, priority, options, recommendation.
3. **Design-phase coordination** — weekly utility meetings during Months 2-4, not quarterly.
4. **Timeline integration** — never start main project construction before all utilities are fully relocated and tested.
5. **Cost contingencies** — typical 25-50%; 40%+ justified for high-risk items (transmission switchover, directional drilling).
6. **Owner relationship management** — single point of contact, 24-hour response, monthly status (weekly during construction).

Full expansions, key questions per utility, sample contingency stack, and deliverables checklist in **[utility-conflict-playbook.md](utility-conflict-playbook.md)**.

## Related Skills

- `expropriation-timeline-expert` (expropriation-law) — critical-path scheduling with utility relocation integration
- `land-assembly-expert` (this plugin) — multi-parcel acquisition phasing
- `easement-valuation-methods` (appraisal-valuation) — compensation valuation when an easement is taken

## Key Terms

- **Right-of-Way (ROW)** — Legal corridor required for infrastructure operation and maintenance
- **Geometric Conflict** — Spatial conflict between proposed ROW and existing utility (horizontal or vertical)
- **Relocation** — Moving existing utility to alternative location, alignment, or elevation
- **Grade Separation** — Utility crosses over or under another with clearance (bridge, casing, directional drill)
- **Switchover** — Temporary service interruption while transferring from old to new alignment (critical for transmission)
- **Directional Drill** — Boring under surface to cross utility over existing infrastructure
- **Cased Crossing** — Underground casing protecting utility as it crosses another utility
- **Cathodic Protection** — System protecting steel pipelines from corrosion (requires relocation coordination)
- **NESC** — North American Electric Safety Code (transmission line clearance standards)
- **Pressure Testing** — Pressurizing pipeline to verify integrity after relocation (regulator-required)
- **Environmental Mitigation** — Actions to minimize ecological impacts of relocation work
- **Critical Path** — Sequence of activities that determines minimum project duration
- **Switchover Window** — Specific time period when utility can be de-energized (e.g., low-demand season)
