---
name: destroy-stack
description: Destroy an OCI Resource Manager stack's infrastructure.
user-invocable: true
allowed-tools: Bash, Read, AskUserQuestion
argument-hint: [stack-id]
---

# Destroy Stack

Tear down infrastructure managed by an ORM stack.

## Arguments

- `$0` (optional) - ORM stack OCID. If not provided, list active stacks and ask user to select.

## Steps

1. Ask the user for their OCI CLI profile (common values: `SANJOSE`, `DEFAULT`) and compartment (name or OCID). If a name is given, resolve with:
   ```bash
   export OCI_CLI_PROFILE=<profile>
   oci iam compartment list --compartment-id-in-subtree true --all \
     --query "data[?name=='<compartment-name>'].id | [0]" --raw-output
   ```

2. If no stack ID provided, list stacks:
   ```bash
   oci resource-manager stack list -c <compartment-ocid> --all
   ```

3. Confirm with user before destroying

5. Create destroy job:
   ```bash
   oci resource-manager job create-destroy-job --stack-id $0 --execution-plan-strategy AUTO_APPROVED
   ```

6. Poll job status until completion (check every 60s)

7. Verify destroy logs are clean

## If Destroy Fails

- If it fails on the Kubernetes provider, update the stack with `--terraform-version 1.5.x` and retry
- If that doesn't work, try with `--refresh=false` if available
- Report any remaining errors to the user
