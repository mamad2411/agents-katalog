# RO-Crate Metadata Bundle Starter

Use this skill to package a small local data file into an RO-Crate directory with basic provenance-rich metadata and a compact summary of the generated graph.

## What it does

- copies one local data file into a fresh RO-Crate directory
- writes `ro-crate-metadata.json` with a named root dataset and measurement metadata
- reports the crate path, graph entity counts, and bundled data files

## When to use it

- you need a verified starter for `data-provenance-tracking`
- you want a lightweight pattern for packaging outputs with reusable metadata
- you need a deterministic RO-Crate fixture for tests or demos

## Example

```bash
./slurm/envs/data-tools/bin/python skills/data-acquisition-and-dataset-handling/rocrate-metadata-bundle-starter/scripts/build_rocrate_metadata_bundle.py \
  --input skills/data-acquisition-and-dataset-handling/rocrate-metadata-bundle-starter/examples/toy_measurements.csv \
  --crate-dir scratch/rocrate/toy_bundle \
  --summary-out scratch/rocrate/toy_bundle_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/data-acquisition-and-dataset-handling/rocrate-metadata-bundle-starter/tests -p 'test_*.py'`
- Expected summary: `has_metadata_file == true`, `data_entity_count == 1`, `root_dataset_name == "Toy Measurement Bundle"`
