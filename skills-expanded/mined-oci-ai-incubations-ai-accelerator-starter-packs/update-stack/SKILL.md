---
name: update-stack
description: Rebuild zip and update an existing ORM stack with latest code changes, then re-plan.
user-invocable: true
allowed-tools: Bash, Read, AskUserQuestion
argument-hint: [stack-id]
---

# Update Stack

Rebuild the deployment zip from current code and update an existing ORM stack.

## Arguments

- `$0` - ORM stack OCID (if not provided, list active stacks and ask user to select)

## Steps

1. Regenerate schema for current category:
   ```bash
   cd "$(git rev-parse --show-toplevel)"
   source venv/bin/activate
   python3 create_final_schema.py -c $(cat ai-accelerator-tf/starter_pack_category.auto.tfvars | grep -oP '(?<=")\w+(?=")')
   ```

2. Clean and create zip using the same exclusion logic as `/zip-tf` (excludes `.terraform/`, `.terraform.lock.hcl`, sensitive `*.tfvars`, `__pycache__/`, `.pytest_cache/`):
   ```bash
   rm -rf ai-accelerator-tf/.terraform ai-accelerator-tf/.terraform.lock.hcl
   rm -f lifecycle.zip
   cd ai-accelerator-tf && zip -r ../lifecycle.zip . \
     -x '.terraform/*' '.terraform.lock.hcl' '*.tfvars' '*__pycache__/*' '*.pytest_cache/*'
   zip ../lifecycle.zip starter_pack_category.auto.tfvars
   ```
   > For a general-purpose timestamped archive (not ORM upload), use `/zip-tf` instead.

3. Ask the user for their OCI CLI profile if not already set (common values: `SANJOSE`, `DEFAULT`).

4. Update stack:
   ```bash
   export OCI_CLI_PROFILE=<profile>
   oci resource-manager stack update --stack-id $0 --config-source lifecycle.zip --force
   ```

4. Run plan job and poll until completion

5. Report plan results to user
