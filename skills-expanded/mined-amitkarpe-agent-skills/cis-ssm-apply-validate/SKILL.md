---
name: cis-ssm-apply-validate
description: Safe SSM document publish, pin-default, apply, and validation workflow for CIS and related remediation documents, with durable evidence capture and rollback-aware logging.
---

# CIS SSM Apply Validate

Use this skill to publish or update an SSM command document, pin the default version, apply it to one instance, and save durable evidence.

## Use when

- publishing a new SSM remediation document
- updating an existing remediation document
- applying a document to one target safely
- validating document parameters and SSM agent reachability before mutation

## Scripts

### Validate inputs and target

```bash
bash scripts/validate.sh \
  --document-file <doc.yaml> \
  --parameters-file <params.json> \
  --output-dir <outdir> \
  [--instance-id <i-xxx>] \
  [--profile <profile>] \
  [--region <region>]
```

### Full workflow

```bash
bash scripts/apply.sh \
  --document-name <name> \
  --document-file <doc.yaml> \
  --parameters-file <params.json> \
  --instance-id <i-xxx> \
  --output-dir <outdir> \
  [--profile <profile>] \
  [--region <region>] \
  [--wait-timeout 600] \
  [--skip-upload]
```

## Rules

- run `validate.sh` first unless `apply.sh` is already doing it
- use a unique `output_dir` per run
- save evidence under `~/.AGENTS-temp/<repo>/...`
- prefer one-instance apply and validation before wider rollout
- treat rollback as a document-version problem first, not an in-chat procedure

## Tests

Basic tests and fixtures live under `tests/`.
