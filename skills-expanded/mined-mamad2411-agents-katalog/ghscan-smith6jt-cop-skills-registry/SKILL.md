# Sentinel Validation & Project Promotion

## Goal
Promote projects processed outside Snakemake (by legacy batch scripts) to "completed" status by validating their output and creating missing `.snakemake_complete` sentinel files.

## Context
- `kintsugi workflow batch` uses sentinel files to determine project eligibility
- Projects processed by batch scripts have output (TIFs + manifest JSON) but no sentinels
- Without sentinels, these projects appear "eligible" and could be reprocessed unnecessarily
- 25 projects were in this state (Feb 25, 2026)

## What Worked

### Validation Script (`scripts/create_si_sentinels.py`)
- Parse `signal_isolation_manifest.json` for metadata (method, tissue_type, quality scores, channel list)
- Verify every channel in manifest has corresponding `.tif` file(s) in output directory
- Check TIF file sizes > 0 bytes (basic integrity)
- Extract summary statistics (global/weighted/recipe counts, mean_quality)
- Write sentinel matching exact Snakemake format (key=value, one per line)
- `--dry-run` flag for safe preview

### Sentinel Format (must match Snakemake-generated sentinels exactly)
```
stage=signal_isolation
completed=<timestamp from manifest>
method=auto
tissue_type=spleen
recipe_dir=/path/to/recipes
total=28
global=0
weighted=4
recipe=24
skipped=0
errors=0
mean_quality=0.803
files=28
duration_minutes=0.0
```

### Key Decisions
- Use manifest `timestamp` as `completed` date (not current time) — preserves original processing date
- Set `duration_minutes=0.0` since we can't recover original runtime
- Trust manifest quality scores (all were 0.70-0.86, not 0.0 as initially suspected)

## What Failed

| Attempt | Problem | Fix |
|---------|---------|-----|
| Assumed quality=0.000 in manifests | Plan said metrics weren't recorded — actually they were all populated (0.70-0.86) | Read actual manifests instead of trusting secondhand reports |
| TIF glob `"$cyc"*.tif` for nested CH subdirs | Stitched TIFs are in `cyc01/CH1/01.tif`, not `cyc01/*.tif` | Use `find -name "*.tif"` for recursive search |
| Top-level sentinel check for per-cycle dirs | `stitched/.snakemake_complete` doesn't exist — sentinels are per-cycle `stitched/cyc01/.snakemake_complete` | Check cycle-level sentinels for per-cycle stages |
| Cleaning all dirs without top-level sentinel | Would delete completed stitch cycles with valid per-cycle sentinels | Leave partial work intact — Snakemake handles it via per-cycle sentinel + per-channel skip-existing |

## Stale Script Deployment (Related Discovery)

`workflow config` only copies scripts if they DON'T already exist. This means:
- Updated `qc_report.py` (with signal_isolation handler) was in source but not deployed projects
- 1901CC2A's signal isolation succeeded but QC failed because deployed `qc_report.py` had no `signal_isolation` case
- Fix: bulk-copy updated scripts to all project workflows after any source change

```bash
for proj in ../KINTSUGI_Projects/*/; do
    target="$proj/workflow/scripts/qc_report.py"
    [ -f "$target" ] && cp workflow/scripts/qc_report.py "$target"
done
```

## Final Parameters
- Validation: manifest parse + per-channel TIF existence + size > 0
- Sentinel source: manifest metadata (not re-analysis)
- Dry-run first, always
- Result: 25 projects validated, 0 errors, all quality 0.70-0.86

## Environment
- KINTSUGI on HiPerGator (SLURM)
- Python 3.11, Snakemake 8.x
- February 2026
