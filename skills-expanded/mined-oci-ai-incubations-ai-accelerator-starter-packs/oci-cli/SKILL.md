---
name: oci-cli
description: Run OCI CLI commands — list resources, check container images, manage compartments, query services.
user-invocable: true
allowed-tools: Bash, Read, AskUserQuestion
argument-hint: <command description or OCI CLI command>
---

# OCI CLI

Run OCI CLI commands against the configured tenancy.

## Arguments

- `$0` - A natural language description of what to do, or a raw OCI CLI command to execute.

## Ask Before Running Commands

Before running OCI CLI commands, ask the user:

- Which OCI region to use (`<region>`). Do not assume a default region.
- Which compartment to use (`<compartment_ocid>` or `<compartment_name>`).
- Whether they want to use a specific OCI CLI profile (`<oci_cli_profile>`) from their local OCI config.

If the user provides a compartment name, resolve it to an OCID with IAM:

```bash
OCI_CLI_PROFILE=<oci_cli_profile> oci iam compartment list -c <tenancy_ocid> --compartment-id-in-subtree true --all --query "data[?name=='<compartment_name>'].id | [0]" --raw-output
```

If the user is not using a named profile, omit `OCI_CLI_PROFILE=<oci_cli_profile>` and run `oci ...` directly.

## Configuration

- Use placeholders in commands and fill them from user input:
  - Optional profile: `OCI_CLI_PROFILE=<oci_cli_profile>`
  - Region: `<region>`
  - Compartment: `<compartment_ocid>`
  - Tenancy (for IAM commands): `<tenancy_ocid>`

## Common Operations

### Container Registry (OCIR)
```bash
# List repositories
OCI_CLI_PROFILE=<oci_cli_profile> oci artifacts container repository list -c <compartment_ocid> --region <region>

# List image tags in a repository
OCI_CLI_PROFILE=<oci_cli_profile> oci artifacts container image list -c <compartment_ocid> --repository-name <repo_name> --region <region>

# Check if a specific image tag exists
OCI_CLI_PROFILE=<oci_cli_profile> oci artifacts container image list -c <compartment_ocid> --repository-name <repo_name> --display-name "<repo_name>:<tag>" --region <region>
```

### Compute
```bash
# List instances
OCI_CLI_PROFILE=<oci_cli_profile> oci compute instance list -c <compartment_ocid> --region <region>

# List shapes available
OCI_CLI_PROFILE=<oci_cli_profile> oci compute shape list -c <compartment_ocid> --region <region>

# Check capacity
OCI_CLI_PROFILE=<oci_cli_profile> oci compute compute-capacity-report create --compartment-id <compartment_ocid> --availability-domain <ad> --shape-availabilities '[{"instanceShape": "<shape>"}]' --region <region>
```

### Resource Manager (ORM)
```bash
# List stacks
OCI_CLI_PROFILE=<oci_cli_profile> oci resource-manager stack list -c <compartment_ocid> --region <region>

# Get stack details
OCI_CLI_PROFILE=<oci_cli_profile> oci resource-manager stack get --stack-id <stack_ocid> --region <region>

# List jobs for a stack
OCI_CLI_PROFILE=<oci_cli_profile> oci resource-manager job list -c <compartment_ocid> --stack-id <stack_ocid> --region <region>
```

### Kubernetes (OKE)
```bash
# List clusters
OCI_CLI_PROFILE=<oci_cli_profile> oci ce cluster list -c <compartment_ocid> --region <region>

# Get kubeconfig
OCI_CLI_PROFILE=<oci_cli_profile> oci ce cluster create-kubeconfig --cluster-id <cluster_ocid> --region <region> --kube-endpoint PUBLIC_ENDPOINT --file $HOME/.kube/config --token-version 2.0.0
```

### IAM
```bash
# List availability domains
OCI_CLI_PROFILE=<oci_cli_profile> oci iam availability-domain list -c <tenancy_ocid> --region <region>

# List compartments
OCI_CLI_PROFILE=<oci_cli_profile> oci iam compartment list -c <tenancy_ocid>
```

### Networking
```bash
# List VCNs
OCI_CLI_PROFILE=<oci_cli_profile> oci network vcn list -c <compartment_ocid> --region <region>

# List subnets
OCI_CLI_PROFILE=<oci_cli_profile> oci network subnet list -c <compartment_ocid> --region <region>
```

## Guidelines

- Always use `--query` and `--output table` for readable output when listing resources.
- Use `--all` for paginated results when needed.
- For destructive operations (delete, terminate), always confirm with the user first.
- If a command fails with auth errors, verify the selected profile (or default profile) is correct.
- If unsure what commands are available, run `oci --help` or see the OCI CLI docs: https://docs.oracle.com/en-us/iaas/tools/oci-cli/latest/oci_cli_docs/
- If unsure which parameters a command needs, run `oci <command_placeholder> --help` to see required/optional parameters and expected format.
