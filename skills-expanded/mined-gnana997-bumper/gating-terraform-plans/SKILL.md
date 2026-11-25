---
name: gating-terraform-plans
description: Gates Terraform and OpenTofu changes with bumper before they are applied — turns a plan into JSON, scans it for destructive, irreversible, or non-compliant changes, and blocks apply until issues are fixed and the plan is verified. Use when about to run terraform/tofu plan or apply, when writing or editing .tf files, or when reviewing infrastructure changes.
---

# Gating Terraform plans with bumper

bumper is a Terraform/OpenTofu plan safety gate. Run it before every apply. It
needs the `bumper` CLI on PATH (https://github.com/gnana997/bumper). If bumper is
not installed, do not apply destructive changes — tell the user to install it.

## Workflow

Follow these steps in order. Never skip the scan, and never apply while
high/critical findings stand.

1. Produce a plan file:
   ```
   terraform plan -out plan.tfplan
   terraform show -json plan.tfplan > plan.json
   ```
   (OpenTofu: `tofu plan` / `tofu show -json`.)

2. Scan it:
   ```
   bumper plan.json
   ```
   Add `--explain` for plain-English detail, or `--format json` for machine-readable
   findings. Exit codes: 0 = clean, 1 = findings present, 2 = usage error.

3. Triage by severity:
   - **critical / high** → STOP. Do not apply. Go to step 4.
   - **medium / low** → review; proceed only if each finding is understood and acceptable.

4. Fix → re-scan loop (repeat until clean or every finding is consciously accepted):
   a. Edit the `.tf` to remove the hazard or narrow its blast radius.
   b. Re-run `terraform plan -out plan.tfplan && terraform show -json plan.tfplan > plan.json`.
   c. `bumper plan.json`.
   d. If findings remain, return to (a).

5. Record a verdict so the apply is unblocked:
   ```
   bumper verify plan.tfplan
   ```
   This scans the saved plan and, on a pass, writes a sha256-bound verdict. To accept
   a reviewed risk explicitly: `bumper verify --accept plan.tfplan`.

6. Apply the exact plan you verified:
   ```
   terraform apply plan.tfplan
   ```

## Why verify the .tfplan, not the JSON

The verdict is bound to the plan file's sha256. bumper's apply-guard hook blocks
`terraform apply` for any plan that has not been verified — so applying a different
or re-generated plan is rejected until you verify it. Never apply a plan you have
not scanned.

## Example

Asked to "add an S3 bucket and apply":
1. `terraform plan -out plan.tfplan && terraform show -json plan.tfplan > plan.json`
2. `bumper plan.json` → **HIGH**: `aws_s3_bucket` has no public-access block.
3. Add `aws_s3_bucket_public_access_block`, re-plan, re-scan → clean.
4. `bumper verify plan.tfplan` → verdict recorded.
5. `terraform apply plan.tfplan`.

## Full, version-matched procedure

For the complete steps and any rules specific to this installed bumper version:
```
bumper skills get plan-gate
```
