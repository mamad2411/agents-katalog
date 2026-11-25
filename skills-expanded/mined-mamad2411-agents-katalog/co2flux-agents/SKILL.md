# Project Instructions

## Quick start: project setup

This project queries an Oracle SensorDB for CO2 vertical profile data and generates animated visualizations.

**Python requirements:**
- Python 3.11+ (project uses `tomllib`)
- Virtual environment via `python -m venv venv`
- Install dependencies: `pip install -r requirements.txt`

**Oracle setup:**
- Oracle credentials in `/home/dimitri/Documents/.env` or project `.env`
- Uses `python-oracledb` in **thick mode** (required for native encryption on this database)
- Oracle Instant Client: `/opt/oracle/instantclient_19_26`
- On Linux: prepend `/opt/oracle/instantclient_19_26` and `/tmp/ora_compat` to `LD_LIBRARY_PATH` to resolve libaio compatibility

**Running scripts:**
```bash
python Sensors_Description/co2_vertical_profile_viewer.py
python scripts/update_co2_sheet.py
```

## Sensors_Description memory

For tasks in `Sensors_Description` related to:

- `variables_schema.xlsx`
- CO2 viewer scripts
- Oracle SensorDB access

read this file first:

- `Sensors_Description/workflow_memory.md`

Then open the canonical task-specific documents referenced from that file.

## Established conventions

### Configuration pattern

Scripts in this project use TOML for user-facing configuration:

- **Default config:** `Sensors_Description/co2_vertical_profile_viewer_config.toml`
- **Local overrides:** `Sensors_Description/co2_vertical_profile_viewer_config.local.toml`
- **Pattern:** Scripts load default first, then apply local overrides if file exists
- **Recommended workflow:**
  1. Keep shared defaults in the `.toml` file
  2. Use `.local.toml` for machine-specific or run-specific settings
  3. Both files are under version control (`.local.toml.example` is a template)

Current config sections:
- `[profile]`: slope, x/y coordinates, date range for visualization
- `[surface_air]`: separate coordinates for air point (used by extended viewers)
- `[oracle]`: machine-specific Oracle Instant Client path and environment setup

### Workbook

- The canonical human-readable rulebook for extending
  `Sensors_Description/variables_schema.xlsx` is:
  `Sensors_Description/variables_schema_notes.md`
- The executable source of truth for the `CO2` sheet is:
  `scripts/update_co2_sheet.py`
- Core rule: **one row = one meaningful time series channel**
  (not just a sensor dump; curated for PDE / inverse problem relevance)
- Workbook validation is done against Oracle, not just inventory metadata

### Viewers

- Shared viewer requirements live in:
  `Sensors_Description/co2_vertical_profile_viewer_requirements.md`
- If a viewer is known-good and trusted by the user, prefer creating a clone
  for new functionality instead of editing the original script.
- Current stable original:
  `Sensors_Description/co2_vertical_profile_viewer.py`
- Current additive clone:
  `Sensors_Description/co2_viewer_add_surface.py`

**Key viewer design patterns:**
- Visualization: horizontal bars with depth on y-axis, CO2 concentration on x-axis
- Fixed CO2 axis range: `0...8000 ppm` across all plots for visual consistency
- Animation: every available measurement (no smoothing, resampling, or filtering)
- Time synchronization: use "last known value" at each frame time
- Missing data: display available depths only, no interpolation
- Output: animated GIF + final JPEG with annotations (time, slope, coordinates, values)
- Config parameters: defined at top of script, not CLI arguments

### Oracle

- Credentials live in:
  `/home/dimitri/Documents/.env`
- Connection instructions for this environment are documented in:
  `Sensors_Description/variables_schema_notes.md`

**Environment-specific setup:**
- Use **thick mode**: `oracledb.init_oracle_client(lib_dir=ORACLE_CLIENT_LIB_DIR)`
  (thin mode fails with `DPY-3001` on this database)
- Linux library compatibility: create symlink for `libaio.so.1` at `/tmp/ora_compat`
- Connection pattern: use `oracledb.makedsn()` with host, port, sid from `.env`
- Query pattern: fetch time series by time windows (not full sensor history at once)
- Always close: `cur.close()` and `conn.close()`

## Working style for repeated tasks

- Reuse the established conventions from the canonical docs instead of
  re-deriving them.
- When extending user-facing scientific scripts, preserve trusted behavior and
  isolate new behavior in a clone unless the user explicitly wants in-place
  edits.
