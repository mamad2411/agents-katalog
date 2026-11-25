---
name: zip-tf
description: Creates a clean, timestamped zip archive of ai-accelerator-tf/. Regenerates the ORM schema, excludes build artifacts and sensitive tfvars, verifies the output contains no secrets or disallowed files, and saves to zipped/. Triggers when packaging, zipping, or archiving the Terraform code for sharing or upload.
user-invocable: true
allowed-tools: Bash, Read, AskUserQuestion
---

# Zip Terraform

## Arguments

- `$0` (optional) — Output directory. Default: `zipped/`. Example: `release_test_matrix/`.
- `$1` (optional) — Custom filename without `.zip` extension. Default: `<category>-<timestamp>`. Example: `v0.0.6_cuopt`.

If no arguments are provided, behavior is unchanged (timestamped zip in `zipped/`).

## Workflow

1. Read `ai-accelerator-tf/starter_pack_category.auto.tfvars` to detect the current category
2. Regenerate schema (run from repo root):
   ```bash
   source venv/bin/activate && python3 create_final_schema.py -c <category>
   ```
3. **Ask the user to confirm** before zipping — show the category, output filename, and exclusion list
4. Create the zip
5. Verify the zip contents
6. Report results

## Create the zip

OCI Resource Manager requires `schema.yaml` and the `.tf` files at the **root**
of the zip, and its Console validates **every** schema-shaped YAML it finds in
**every** subdirectory. So the zip must be built FLAT (from inside
`ai-accelerator-tf/`, not by zipping the folder) and must exclude the whole
`schemas/` tree except `schemas/frontend_skins.yaml` — the only `schemas/` file
Terraform reads at runtime (`frontend-skins.tf`). Shipping `schemas/*_schema.yaml`,
`schemas/generated/`, `schemas/tests/`, or `meta_schema.yaml` makes the Console
reject the stack with a generic "Errors exist in your schema file". (See BUGS.md
BUG-046.)

```bash
CATEGORY=$(grep -oP 'starter_pack_category\s*=\s*"\K[^"]+' ai-accelerator-tf/starter_pack_category.auto.tfvars)

# Use arguments if provided, otherwise use defaults
OUTPUT_DIR="${0:-zipped}"
mkdir -p "$OUTPUT_DIR"

if [ -n "$1" ]; then
  ZIP_NAME="$(pwd)/${OUTPUT_DIR}/${1}.zip"
else
  TIMESTAMP=$(date +"%Y-%m-%d-%H%M")
  ZIP_NAME="$(pwd)/${OUTPUT_DIR}/${CATEGORY}-${TIMESTAMP}.zip"
fi
rm -f "${ZIP_NAME}"

# FLAT zip (schema.yaml + .tf at root); exclude the schemas/ tree, then re-add
# frontend_skins.yaml (TF-read) and the category selector (dropped by *.tfvars).
( cd ai-accelerator-tf && \
  zip -r "${ZIP_NAME}" . \
    -x '.terraform/*' '.terraform.lock.hcl' '*.tfvars' \
       '*__pycache__/*' '*.pytest_cache/*' 'tests/*' 'schemas/*' && \
  zip "${ZIP_NAME}" schemas/frontend_skins.yaml starter_pack_category.auto.tfvars )

ls -lh "${ZIP_NAME}"
```

## Verify zip contents

Unzip into a temp directory, validate, then clean up:

```bash
VERIFY_DIR=$(mktemp -d)
unzip -qo "${ZIP_NAME}" -d "$VERIFY_DIR"
FAIL=0

# Must NOT contain
find "$VERIFY_DIR" -type d -name ".terraform" | grep -q . && echo "FAIL: .terraform/ found" && FAIL=1
find "$VERIFY_DIR" -name ".terraform.lock.hcl" | grep -q . && echo "FAIL: .terraform.lock.hcl found" && FAIL=1
BAD_TFVARS=$(find "$VERIFY_DIR" -name "*.tfvars" ! -name "starter_pack_category.auto.tfvars")
[ -n "$BAD_TFVARS" ] && echo "FAIL: disallowed .tfvars: $BAD_TFVARS" && FAIL=1

# Must contain
find "$VERIFY_DIR" -name "starter_pack_category.auto.tfvars" | grep -q . || { echo "FAIL: starter_pack_category.auto.tfvars missing"; FAIL=1; }
find "$VERIFY_DIR" -name "terraform.tfvars.example" | grep -q . || { echo "FAIL: terraform.tfvars.example missing"; FAIL=1; }

# ORM structure: schema.yaml MUST be at the zip root, and the ONLY schema YAML in
# the archive (the Console validates every schema-shaped file it finds). Only
# schemas/frontend_skins.yaml may remain under schemas/.
[ -f "$VERIFY_DIR/schema.yaml" ] || { echo "FAIL: schema.yaml not at zip root (ORM won't find it)"; FAIL=1; }
STRAY=$(find "$VERIFY_DIR/schemas" -name '*.yaml' ! -name 'frontend_skins.yaml' 2>/dev/null)
[ -n "$STRAY" ] && echo "FAIL: extra schema YAML in zip (Console will reject): $STRAY" && FAIL=1

# Strict schema validation: if OCI's strict meta-schema is present, validate the
# packaged root schema.yaml against it — catches enum-without-values, map
# valueType pointing at a primitive, boolean eq operands, and unsupported keys
# that the repo's lenient schemas/meta_schema.yaml (additionalProperties: true)
# does NOT flag but the live Console does.
if [ -f docs/meta_schema.yaml ]; then
  python3 - "$VERIFY_DIR/schema.yaml" docs/meta_schema.yaml <<'PY' || FAIL=1
import sys, yaml, jsonschema
schema = yaml.safe_load(open(sys.argv[1]))
meta = yaml.safe_load(open(sys.argv[2]))
errs = sorted(jsonschema.Draft7Validator(meta).iter_errors(schema), key=lambda e: list(e.path))
if errs:
    print(f"FAIL: schema.yaml has {len(errs)} strict meta-schema error(s):")
    for e in errs[:15]:
        print("  -", "/".join(map(str, e.path)) or "<root>", ":", e.message[:120])
    sys.exit(1)
print("OK: schema.yaml passes the strict OCI meta-schema")
PY
else
  echo "NOTE: docs/meta_schema.yaml not found — skipping strict schema validation (recommended to add it)"
fi

# PII / secrets scan — flag but don't auto-fail (user decides)
PII=$(grep -rl -E '(PRIVATE KEY|password\s*=\s*".+"|api_key\s*=\s*".+"|ocid1\.(user|tenancy)\.[a-zA-Z0-9.]+)' "$VERIFY_DIR" --include="*.tf" --include="*.tfvars" --include="*.yaml" --include="*.yml" --include="*.json" 2>/dev/null | grep -v "terraform.tfvars.example" | grep -v "\.example")
[ -n "$PII" ] && echo "WARNING: possible secrets in: $PII"

rm -rf "$VERIFY_DIR"
[ $FAIL -eq 0 ] && echo "ALL CHECKS PASSED" || echo "VERIFICATION FAILED — do not share this zip"
```

If any check fails, stop and alert the user. For PII warnings, show the flagged files and let the user decide.

## Report

Tell the user the zip filename, size, full path, and verification summary.
