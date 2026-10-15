---
name: puda-data
description: Extract, hash, export, and report on PUDA experimental data. Provides data provenance through SHA-256 hashing. Supports multiple devices (first, biologic) and measurement types (CV, OCV, CA, PEIS, GEIS).
---

# PUDA Data Skills

Comprehensive data management for PUDA laboratory experiments with pluggable architecture.

## Quick Start

```python
import sys
sys.path.append("/home/bears/.openclaw/workspace/.claude/skills/puda-data/scripts")

# Extract data
from extractor import get_runs_by_type, extract_measurement_data
from adapters import AdapterRegistry, register_all

# Register adapters (auto-registers first, biologic)
register_all()

# Get data
run_id = get_runs_by_type("CV", 1)[0][0]
df = extract_measurement_data(run_id, "CV")

# Hash for provenance
from hasher import generate_fingerprint
fp = generate_fingerprint(run_id)
print(f"Hash: {fp['measurement_hash']}")

# Plot
from plotter import plot_measurement
plot_path = plot_measurement(run_id, "CV")

# Full report
from report import generate_report
report_path = generate_report(run_id)
```

## Architecture

```
puda-data/
├── config.py              # Path discovery (env, markers, cwd)
├── registry.py            # SchemaRegistry (column definitions)
├── extractor.py           # Data extraction from DB
├── hasher.py              # SHA-256 provenance
├── exporter.py             # CSV/JSON export
├── plotter.py             # PlotterRegistry (pluggable plots)
├── report.py              # Markdown report builder
└── adapters/
    ├── __init__.py         # DeviceAdapter ABC + registry
    ├── first.py            # First machine / qubot adapter
    └── biologic.py         # Biologic potentiostat adapter
```

## Core Concepts

### 1. Path Discovery (config.py)

Automatically finds project root via:
1. `PUDA_PROJECT_ROOT` env var
2. `puda.db` in parent directories
3. `puda.config` in parent directories
4. `experiment.md` in parent directories
5. `protocols/` in parent directories
6. `cwd()` fallback

```python
from config import get_project_root, get_db_path, get_report_dir

print(get_project_root())  # /path/to/workspace
print(get_db_path())       # /path/to/workspace/puda.db
```

### 2. Schema Registry (registry.py)

Maps `(device, command)` → column names, units, plot axes.

```python
from registry import SchemaRegistry, Schema

# Get schema
schema = SchemaRegistry.get("first", "CV")
print(schema.columns)  # ['potential', 'current', 'time', 'extra', 'flag']

# Register new schema
SchemaRegistry.register("mydevice", "CUSTOM", Schema(
    columns=["freq", "magnitude", "phase"],
    units={"freq": "Hz", "magnitude": "dB"},
    primary_x="freq",
    primary_y="magnitude"
))

# Get or create default
schema = SchemaRegistry.get_or_default("unknown", "CV")
```

**Built-in schemas:**

| Device | Command | Columns |
|--------|---------|---------|
| first | CV | potential, current, time, extra, flag |
| first | OCV | potential, current, time, extra, flag |
| first | CA | time, current, voltage, extra, flag |
| first | PEIS | frequency, Z_real, Z_imag, phase, flag |
| biologic | CV | E, I, time, Ewe, flag |
| biologic | PEIS | frequency, Z_real, Z_imag, phase, magnitude |

### 3. Device Adapters (adapters/)

Abstract device-specific data extraction.

```python
from adapters import DeviceAdapter, AdapterRegistry, register_all

register_all()  # Registers first, biologic adapters

# Get adapter for device
adapter = AdapterRegistry.get("biologic")

# Auto-detect device from run
adapter = AdapterRegistry.get_or_default("first")

# Unknown device gets GenericAdapter fallback
adapter = AdapterRegistry.get_or_default("unknown_device")
```

**Adding a new device:**
```python
from adapters import DeviceAdapter, AdapterRegistry

class MyDeviceAdapter(DeviceAdapter):
    @property
    def name(self): return "mydevice"
    
    def extract_data(self, payload, command):
        # Navigate device-specific payload structure
        data = payload.get("response", {}).get("data", {})
        return pd.DataFrame(data.get("0", []))

AdapterRegistry.register(MyDeviceAdapter())
```

### 4. Plotter Registry (plotter.py)

Pluggable visualization functions.

```python
from plotter import register_plotter, plot_measurement

# Registered plotters: CV, OCV, PEIS, CA
plot_path = plot_measurement(run_id, "CV")  # Auto-routes to correct plotter

# Add custom plotter
@register_plotter("MY_DATA")
def plot_my_data(run_id, **kwargs):
    df = extract_measurement_data(run_id, "MY_DATA")
    plt.plot(df["x"], df["y"])
    return save_plot(...)
```

## API Reference

### Extractor

```python
from extractor import (
    extract_measurement_data,  # Get DataFrame for a run
    get_runs_by_type,          # List runs by command type
    get_latest_measurements,   # Get recent measurement DataFrames
    get_run_info,              # Get run metadata
    get_protocol,              # Get protocol definition
    list_all_runs,             # List all runs
)

# Examples
df = extract_measurement_data(run_id, "CV", device="biologic")
runs = get_runs_by_type("CV", limit=10)
measurements = get_latest_measurements("PEIS", limit=5)
info = get_run_info(run_id)
protocol = get_protocol(protocol_id)
all_runs = list_all_runs(limit=20)
```

### Hasher

```python
from hasher import (
    hash_measurement,       # SHA-256 of DataFrame
    hash_run,               # Aggregate hash of all commands
    generate_fingerprint,   # Full fingerprint with metadata
    verify_integrity,       # Check if data matches stored hash
    compare_runs,           # Compare two runs
    demonstrate_integrity,  # Show hash changes on modification
)

# Examples
fp = generate_fingerprint(run_id)
# Returns: {run_id, measurement_hash, run_hash, checksum, 
#           data_points, x_range, y_range, ...}

is_valid = verify_integrity(run_id, expected_hash)
comparison = compare_runs(run_id1, run_id2)
demo = demonstrate_integrity(run_id)  # Shows avalanche effect
```

### Exporter

```python
from exporter import (
    export_to_csv,           # Export DataFrame to CSV
    export_to_json,           # Export with metadata + hashes
    export_protocol,          # Export protocol definition
    export_full_experiment,   # Export everything at once
)

# Examples
csv_path = export_to_csv(run_id)
json_path = export_to_json(run_id)
prot_path = export_protocol(run_id)
results = export_full_experiment(run_id)
```

### Report

```python
from report import ExperimentReport, generate_report

# One-liner
report_path = generate_report(run_id, command_name="CV")

# Custom report
report = ExperimentReport(run_id, "CV", "My Experiment")
report.add_metadata()
report.add_hashes()
report.add_summary()
report.add_plot("CV Curve", plot_measurement, {"run_id": run_id, "command": "CV"})
report.add_table("Stats", {"key": "value"})
report.add_markdown("## Notes\nCustom observations.")
report.save("report.md")
```

### Plotter

```python
from plotter import (
    plot_measurement,   # Main entry point (auto-routes to correct plotter)
    plot_cv,            # CV forward/backward scatter
    plot_ocv,           # OCV time series
    plot_nyquist,       # PEIS Nyquist plot
    plot_ca,            # CA current vs time
    plot_default,       # Generic scatter of first 2 columns
    get_data_summary,   # Summary statistics
)

# Examples
path = plot_measurement(run_id, "CV")
path = plot_measurement(run_id, "PEIS")  # Routes to nyquist
summary = get_data_summary(run_id)
```

## Database Schema

```sql
protocol(run_id, user_id, username, description, commands, created_at)
run(run_id, protocol_id, created_at)
sample(sample_id, run_id, data_payload, created_at)
measurement(measurement_id, sample_id, data_payload, created_at)
command_log(command_log_id, run_id, step_number, command_name, payload, machine_id, command_type, created_at)
```

## Supported Data Types

| Type | Status | Plot Function |
|------|--------|---------------|
| CV | ✅ Full | `plot_cv` (forward/backward scatter) |
| OCV | ✅ Full | `plot_ocv` (time series) |
| CA | ✅ Full | `plot_ca` (current vs time) |
| PEIS | ✅ Full | `plot_nyquist` (Z_real vs -Z_imag) |
| GEIS | ✅ Ready | Generic fallback |

## Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `PUDA_PROJECT_ROOT` | Override project root discovery | `/home/user/puda-project` |

## Files

```
puda-data/
├── SKILL.md              # This file
├── scripts/
│   ├── config.py         # Path discovery
│   ├── registry.py       # SchemaRegistry
│   ├── extractor.py      # Database queries
│   ├── hasher.py         # SHA-256 hashing
│   ├── exporter.py       # CSV/JSON export
│   ├── plotter.py        # PlotterRegistry
│   ├── report.py         # Report builder
│   └── adapters/
│       ├── __init__.py   # DeviceAdapter ABC
│       ├── first.py      # First machine adapter
│       └── biologic.py   # Biologic adapter
└── references/           # Detailed docs (future)
```

## Requirements

```bash
pip install pandas matplotlib numpy
```

---

**Refactor History:**
- 2026-03-21: Added pluggable adapter architecture (config, registry, adapters)
