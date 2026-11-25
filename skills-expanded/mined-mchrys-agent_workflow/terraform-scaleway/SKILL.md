---
name: terraform-scaleway
description: Deploy OpenRAG infrastructure on Scaleway using Terraform when user asks to provision, deploy, create Scaleway infrastructure, GPU instances, L4 instances, or Terraform deployment. Automatically checks GPU availability, creates Terraform configs, and deploys L4-1-24G GPU instance with flexible IP and security group.
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Terraform Scaleway Deployment Skill

## Objective

Automate OpenRAG infrastructure deployment on Scaleway using Terraform:
- Check Scaleway CLI configuration and credentials
- Verify GPU L4-1-24G availability across zones
- Create Terraform configuration files
- Initialize and apply Terraform to provision GPU instance
- Output instance IP and SSH access command

## When to Use

Activate this skill when user requests:
- "Deploy OpenRAG on Scaleway with Terraform"
- "Provision Scaleway GPU instance"
- "Create L4 GPU infrastructure"
- "Setup Scaleway infrastructure with Terraform"
- "Terraform deployment for OpenRAG"
- "Provision L4-1-24G instance"
- Any variation requesting Scaleway infrastructure automation

## Prerequisites Check

Before starting deployment, verify:

1. **Scaleway CLI installed and configured**:
   ```bash
   scw version
   scw config get access-key
   scw config get secret-key
   scw config get default-project-id
   ```

2. **Terraform installed**:
   ```bash
   terraform version  # Should be >= 1.0
   ```

3. **jq installed** (for JSON parsing):
   ```bash
   jq --version
   ```

If any prerequisite is missing, inform user and provide installation instructions.

## Instructions

### Step 1: Verify Scaleway Configuration

Check Scaleway CLI authentication:

```bash
# Verify credentials are configured
if ! scw account project list &>/dev/null; then
    echo "ERROR: Scaleway CLI not configured"
    echo "Run: scw init"
    exit 1
fi

# Get project ID
PROJECT_ID=$(scw config get default-project-id)
echo "Project ID: $PROJECT_ID"
```

If configuration missing, guide user to run `scw init`.

### Step 2: Check GPU L4-1-24G Availability

Check availability across all zones:

```bash
echo "Checking GPU L4-1-24G availability..."

ZONES=("fr-par-1" "fr-par-2" "pl-waw-2")
AVAILABLE_ZONE=""

for ZONE in "${ZONES[@]}"; do
    AVAILABLE=$(scw instance server-type list zone=$ZONE type=L4-1-24G -o json 2>/dev/null | \
        jq -r '.[0].available // false')

    if [ "$AVAILABLE" = "true" ]; then
        echo "✅ GPU L4-1-24G available in zone: $ZONE"
        AVAILABLE_ZONE=$ZONE
        break
    else
        echo "❌ GPU L4-1-24G NOT available in zone: $ZONE"
    fi
done

if [ -z "$AVAILABLE_ZONE" ]; then
    echo "⚠️  WARNING: GPU L4-1-24G not available in any zone"
    echo "Options:"
    echo "  1. Wait 15-30 minutes and retry"
    echo "  2. Try later (peak hours have less availability)"
    echo "  3. Use different GPU type (L4-2-24G, etc.)"
    echo "  4. Use CPU instance (DEV1-M) temporarily"
    exit 1
fi

echo "Selected zone: $AVAILABLE_ZONE"
```

**If GPU unavailable**: Ask user to choose alternative action.

### Step 3: Create Terraform Configuration Directory

Create deployment directory:

```bash
mkdir -p deployment/scaleway/terraform
cd deployment/scaleway/terraform
```

### Step 4: Generate Terraform Files

Copy templates from skill directory to deployment directory:

**Read templates**:
- Read `.claude/skills/terraform-scaleway/templates/versions.tf`
- Read `.claude/skills/terraform-scaleway/templates/variables.tf`
- Read `.claude/skills/terraform-scaleway/templates/main.tf`
- Read `.claude/skills/terraform-scaleway/templates/outputs.tf`
- Read `.claude/skills/terraform-scaleway/templates/terraform.tfvars.example`

**Create files** in `deployment/scaleway/terraform/`:
1. Write `versions.tf` (Terraform and provider configuration)
2. Write `variables.tf` (Variable definitions)
3. Write `main.tf` (Resources: instance, IP, security group)
4. Write `outputs.tf` (Output instance IP, ID, SSH command)
5. Write `terraform.tfvars.example` (Template for variables)

**Update zone in main.tf** if different from fr-par-1 (use AVAILABLE_ZONE from Step 2).

### Step 5: Create terraform.tfvars

Create `terraform.tfvars` with actual values:

```bash
# Get project ID from Scaleway config
PROJECT_ID=$(scw config get default-project-id)

# Create terraform.tfvars
cat > terraform.tfvars <<EOF
project_id       = "$PROJECT_ID"
zone             = "$AVAILABLE_ZONE"
region           = "fr-par"
instance_name    = "openrag-prod-gpu"
instance_type    = "L4-1-24G"
root_volume_size = 100
tags             = ["openrag", "production", "gpu", "terraform"]
EOF
```

### Step 6: Initialize Terraform

```bash
cd deployment/scaleway/terraform
terraform init
```

Expected output: Provider downloaded, backend initialized.

If error occurs, check:
- Internet connectivity
- Terraform registry access
- Terraform version compatibility

### Step 7: Validate Configuration

```bash
terraform validate
terraform fmt
```

### Step 8: Plan Deployment

```bash
terraform plan
```

Review the plan output:
- Should create 3 resources: instance, IP, security group
- Verify instance type is L4-1-24G
- Verify zone is correct
- Check root volume size (100 GB)

**Ask user for confirmation** before applying.

### Step 9: Apply Terraform Configuration

```bash
terraform apply
```

**Important**: This will create billable resources (0.75€/hour).

Monitor output for:
- Resource creation progress
- Any errors or warnings
- Estimated time to complete

Typical deployment time: 2-5 minutes.

### Step 10: Retrieve Outputs

After successful apply:

```bash
# Get all outputs
terraform output

# Get specific values
INSTANCE_ID=$(terraform output -raw instance_id)
INSTANCE_IP=$(terraform output -raw instance_public_ip)
INSTANCE_ZONE=$(terraform output -raw instance_zone)
SSH_COMMAND=$(terraform output -raw ssh_command)

echo "================================"
echo "✅ Deployment Successful!"
echo "================================"
echo "Instance ID:   $INSTANCE_ID"
echo "Public IP:     $INSTANCE_IP"
echo "Zone:          $INSTANCE_ZONE"
echo "Instance Type: L4-1-24G (1x NVIDIA L4 GPU, 8 vCPU, 48GB RAM)"
echo ""
echo "SSH Access:"
echo "  $SSH_COMMAND"
echo ""
echo "Cost: 0.75€/hour (~540€/month 24/7)"
echo "================================"
```

### Step 11: Verify Instance

Verify instance is running:

```bash
# Check instance status
scw instance server get $INSTANCE_ID zone=$INSTANCE_ZONE

# Wait for SSH to be ready (may take 1-2 minutes)
echo "Waiting for SSH to be ready..."
for i in {1..60}; do
    if ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no root@$INSTANCE_IP "echo SSH ready" 2>/dev/null; then
        echo "✅ SSH is ready!"
        break
    fi
    echo -n "."
    sleep 5
done
```

### Step 12: Next Steps Instructions

Provide user with next steps:

```
Next Steps:
1. Configure DNS A record: <your-domain> → $INSTANCE_IP
2. Wait for DNS propagation (5-60 minutes)
3. Deploy OpenRAG application (see Phase 1 in spec)
4. Run deployment script on instance

Files created:
- deployment/scaleway/terraform/versions.tf
- deployment/scaleway/terraform/variables.tf
- deployment/scaleway/terraform/main.tf
- deployment/scaleway/terraform/outputs.tf
- deployment/scaleway/terraform/terraform.tfvars

Terraform state:
- deployment/scaleway/terraform/terraform.tfstate (DO NOT commit to git)

To destroy infrastructure:
  cd deployment/scaleway/terraform && terraform destroy
```

## Error Handling

### GPU Not Available

If no GPU available in any zone:
1. Inform user of situation
2. Suggest alternatives:
   - Wait and retry (15-30 min)
   - Try off-peak hours
   - Use L4-2-24G (2 GPUs, double price)
   - Use CPU instance temporarily (DEV1-M)
   - Use external LLM API (Mistral, OpenAI)

### Authentication Error

If Scaleway CLI auth fails:
1. Run `scw init` to reconfigure
2. Verify credentials in Scaleway console
3. Check environment variables (SCW_ACCESS_KEY, SCW_SECRET_KEY, SCW_PROJECT_ID)

### Terraform Init/Apply Errors

Common issues:
- **Provider download fails**: Check internet connectivity
- **Resource already exists**: Check existing resources with `scw instance server list`
- **Quota exceeded**: Check Scaleway quotas in console
- **Invalid credentials**: Re-run `scw init`

### Instance Creation Timeout

If instance takes too long:
1. Check Scaleway console for instance status
2. Verify zone has capacity
3. Try different zone
4. Contact Scaleway support

## Expected Output

Successful deployment provides:
- Instance ID (UUID)
- Public IP address
- SSH command for access
- Zone and instance type confirmation
- Cost information
- Next steps instructions

Example:
```
================================
✅ Deployment Successful!
================================
Instance ID:   11111111-2222-3333-4444-555555555555
Public IP:     51.159.123.45
Zone:          fr-par-1
Instance Type: L4-1-24G (1x NVIDIA L4 GPU, 8 vCPU, 48GB RAM)

SSH Access:
  ssh root@51.159.123.45

Cost: 0.75€/hour (~540€/month 24/7)
================================
```

## Cost Awareness

Always inform user about costs:
- **L4-1-24G**: 0.75€/hour
  - 8h/day usage: ~132€/month
  - 24/7 usage: ~540€/month
- **Flexible IP**: 2€/month
- **Storage 100GB**: ~10€/month

**Cost optimization tips**:
- Stop instance when not in use: `scw instance server stop <id>`
- Use scheduled start/stop
- Consider spot instances (when available)
- Monitor usage with `scw instance server get`

## Additional Resources

For detailed Terraform and Scaleway CLI reference, see:
- [reference.md](reference.md) - Complete CLI and Terraform documentation
- Spec: `.agents/specs/scaleway_production_deployment_simple.md`
- Templates: `.claude/skills/terraform-scaleway/templates/`

## Terraform State Management

**IMPORTANT**:
- `terraform.tfstate` contains sensitive data
- **DO NOT** commit to git
- Add to `.gitignore`:
  ```
  deployment/scaleway/terraform/*.tfstate
  deployment/scaleway/terraform/*.tfstate.backup
  deployment/scaleway/terraform/.terraform/
  deployment/scaleway/terraform/terraform.tfvars
  ```

For production, use remote state:
- Terraform Cloud
- S3 backend
- Consul
- Scaleway Object Storage

## Summary

This skill automates the complete infrastructure provisioning workflow:
1. ✅ Verifies prerequisites
2. ✅ Checks GPU availability across zones
3. ✅ Creates Terraform configuration
4. ✅ Deploys L4-1-24G GPU instance
5. ✅ Provides SSH access and next steps

Total time: ~10-15 minutes (including checks and deployment)
