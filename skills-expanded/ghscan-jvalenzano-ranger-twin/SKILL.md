# Cruise Methodology

## Description
Recommends timber cruise protocols (variable radius, fixed radius, strip, line) based on stand
characteristics, terrain, and inventory objectives. Calculates optimal basal area factor (BAF),
sampling intensity, and plot locations for post-fire timber inventory.

## Triggers
When should the agent invoke this skill?
- User asks about timber cruise design or protocol
- Query mentions "cruise methodology" or "sampling design"
- Request for BAF selection or plot layout
- Questions about sampling intensity or plot count
- Stand inventory planning requests
- Post-fire timber assessment setup

## Instructions
Step-by-step reasoning for the agent:
1. **Assess Stand Characteristics**: Evaluate tree size, density, and variability
   - Average DBH determines BAF selection
   - Stand density affects plot size and count
   - Species mix impacts sampling strategy
2. **Select Methodology**: Choose appropriate cruise method
   - Variable radius (prism/relaskop) for mixed stands
   - Fixed radius for uniform stands or young growth
   - Strip cruise for long narrow areas
   - Line plot for accessibility constraints
3. **Calculate BAF**: For variable radius plots
   - Large trees (>24" DBH): BAF 40
   - Medium trees (16-24" DBH): BAF 20
   - Small trees (<16" DBH): BAF 10
4. **Determine Sampling Intensity**: Based on stand variability
   - High variability: 15-20% sampling intensity
   - Moderate variability: 10-15% intensity
   - Low variability: 5-10% intensity
5. **Generate Plot Locations**: Systematic or random layout
   - Grid spacing for systematic plots
   - Random coordinates within sector boundaries
   - Stratification by burn severity or stand type

## Inputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| fire_id | string | Yes | Unique fire identifier (e.g., "cedar-creek-2022") |
| sector | string | No | Specific sector to design cruise for |
| stand_type | string | No | Forest stand composition (e.g., "Douglas-fir/Western Hemlock") |
| avg_dbh | number | No | Average tree diameter in inches |
| stand_density | string | No | Stand density class: "sparse", "moderate", "dense" |
| terrain | string | No | Terrain difficulty: "flat", "moderate", "steep", "very_steep" |
| objective | string | No | Cruise objective: "salvage", "volume", "stocking", "research" |
| target_confidence | number | No | Desired confidence level (default: 0.90) |
| total_acres | number | No | Total area to cruise |

## Outputs
| Output | Type | Description |
|--------|------|-------------|
| fire_id | string | The analyzed fire identifier |
| recommended_method | string | Cruise methodology (Variable Radius, Fixed Radius, Strip, Line) |
| baf | number | Basal area factor for variable radius (10, 20, 30, 40) |
| plot_radius_ft | number | Fixed plot radius in feet (if fixed radius method) |
| sampling_intensity_pct | number | Percentage of area to sample |
| num_plots | number | Recommended number of plots |
| plot_locations | array | Generated plot coordinates (if sector provided) |
| reasoning_chain | array | Step-by-step methodology decisions |
| confidence | number | Recommendation confidence (0-1) |
| data_sources | array | Sources used for calculations |
| recommendations | array | Implementation guidance |

## Reasoning Chain
Step-by-step reasoning for the agent:
1. First, assess stand characteristics (DBH, density, composition)
2. Then, select the most appropriate cruise method for the terrain and objective
3. Next, calculate BAF or plot radius based on average tree size
4. Then, determine sampling intensity based on stand variability and target confidence
5. Finally, generate systematic plot locations if sector geometry provided

## Resources
- `resources/sampling-protocols.json` - Cruise method decision matrix
- `resources/baf-tables.json` - BAF selection guide by tree size

## Scripts
- `scripts/recommend_methodology.py` - Python implementation of cruise design
  - Function: `execute(inputs: dict) -> dict`
  - Inputs: `{"fire_id": "cedar-creek-2022", "sector": "SW-1"}`
  - Returns: Complete cruise methodology recommendation with plot layout

## Examples

### Example 1: Variable Radius Cruise Design
**Input:**
```json
{
  "fire_id": "cedar-creek-2022",
  "sector": "SW-1",
  "stand_type": "Douglas-fir/Western Hemlock",
  "avg_dbh": 28.5,
  "stand_density": "dense",
  "terrain": "steep",
  "objective": "salvage",
  "total_acres": 2150
}
```

**Output:**
```json
{
  "fire_id": "cedar-creek-2022",
  "sector": "SW-1",
  "recommended_method": "Variable Radius Plot",
  "baf": 20,
  "sampling_intensity_pct": 12,
  "num_plots": 15,
  "plot_locations": [
    {"plot_id": "SW1-01", "coords": [-122.1156, 43.6567], "elevation": 3400},
    {"plot_id": "SW1-02", "coords": [-122.1089, 43.6623], "elevation": 3650}
  ],
  "reasoning_chain": [
    "Average DBH 28.5 inches indicates large timber -> BAF 20 recommended",
    "Dense stand with high variability -> 12% sampling intensity",
    "Steep terrain + salvage objective -> Variable radius method preferred",
    "2,150 acres × 12% sampling = 258 acres, 15 plots recommended",
    "Systematic grid layout with 375-foot spacing"
  ],
  "confidence": 0.92,
  "data_sources": ["FSVeg stand data", "Timber cruise handbook PNW-GTR"],
  "recommendations": [
    "Use 20 BAF prism or relaskop for plot sampling",
    "Establish plots on systematic 375-foot grid",
    "Stratify by burn severity for more precise estimates",
    "Measure all in-trees for DBH, height, defect, and species"
  ]
}
```

### Example 2: Fixed Radius for Young Growth
**Input:**
```json
{
  "fire_id": "cedar-creek-2022",
  "stand_type": "Lodgepole Pine",
  "avg_dbh": 11.2,
  "stand_density": "dense",
  "terrain": "flat",
  "objective": "stocking"
}
```

**Output:**
```json
{
  "fire_id": "cedar-creek-2022",
  "recommended_method": "Fixed Radius Plot",
  "plot_radius_ft": 24.0,
  "sampling_intensity_pct": 8,
  "num_plots": 20,
  "reasoning_chain": [
    "Average DBH 11.2 inches indicates small timber -> Fixed radius preferred",
    "Dense stocking + uniform stand -> 8% sampling intensity",
    "Flat terrain allows efficient systematic layout",
    "1/20-acre plots (24-foot radius) appropriate for small trees"
  ],
  "confidence": 0.88,
  "data_sources": ["FSVeg stand data"],
  "recommendations": [
    "Use 1/20-acre fixed radius plots (24-foot radius)",
    "Measure all trees >5 inches DBH",
    "Record stocking density and regeneration"
  ]
}
```

## References
- USFS Timber Cruising Handbook FSH 2409.12
- Variable Plot Sampling: Grosenbaugh (1952) "Plotless Timber Estimates"
- PNW-GTR-019: "Cruising and Evaluating"
- Cedar Creek Timber Plots: `data/fixtures/cedar-creek/timber-plots.json`
