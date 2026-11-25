---
name: azure-cli
description: Azure CLI helper for managing Azure resources, AI Foundry deployments, and monitoring credits. Use when working with Azure cloud services, deploying models, checking resource status, or managing the $4500 credit budget.
---

# Azure CLI Helper

Streamlined Azure CLI commands for managing cloud resources and AI deployments.

## Quick Start

### 1. Login to Azure

```bash
# Interactive login
./scripts/az-login.sh

# Or manually
az login --use-device-code
```

### 2. Check Your Resources

```bash
# View all AI Foundry resources
./scripts/check-ai-foundry.sh

# Monitor credits and usage
./scripts/monitor-credits.sh
```

## Common Tasks

### Managing AI Foundry Deployments

**List all AI services:**
```bash
az cognitiveservices account list -o table
```

**Check specific deployment:**
```bash
az cognitiveservices account show --name <account-name> --resource-group <rg>
```

**Test Mistral endpoint:**
```bash
curl -X POST "https://<your-endpoint>.cognitiveservices.azure.com/openai/deployments/Mistral-Large-3/chat/completions?api-version=2024-05-01-preview" \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_API_KEY" \
  -d '{"messages": [{"role": "user", "content": "Hello"}]}'
```

### Resource Management

**List resource groups:**
```bash
az group list -o table
```

**List all resources in a group:**
```bash
az resource list --resource-group <group-name> -o table
```

**Check VM status:**
```bash
az vm list -o table
```

### Credit Management

**View subscription details:**
```bash
az account show
```

**List all subscriptions:**
```bash
az account list -o table
```

**Set active subscription:**
```bash
az account set --subscription "<subscription-name-or-id>"
```

## Your Azure Setup

### Current Configuration

- **Resource Group:** `brokencircuits-1334-resource`
- **Region:** `east2`
- **Models Deployed:**
  - Mistral Large 3
  - Kimi K2 Thinking
- **Available Credits:** ~$4500

### Quick Model Access

Instead of complex Azure CLI commands, use these simple wrappers:

```bash
# Call Mistral 3 Large
python3 /home/sarah/models/mistral.py "Your prompt here"

# Call Kimi K2 Thinking  
python3 /home/sarah/models/kimi.py "Your prompt here"
```

Or use the aliases:
```bash
mistral "Explain quantum computing"
kimi "Analyze this architecture"
```

## Scripts Reference

| Script | Purpose | Usage |
|--------|---------|-------|
| `az-login.sh` | Login to Azure | `./scripts/az-login.sh` |
| `check-ai-foundry.sh` | Check AI deployments | `./scripts/check-ai-foundry.sh [rg] [workspace]` |
| `monitor-credits.sh` | Monitor credit usage | `./scripts/monitor-credits.sh` |

## Azure CLI Installation

If not installed:

```bash
# Ubuntu/Debian
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Verify installation
az --version
```

## Troubleshooting

**"Not logged in" error:**
```bash
az login --use-device-code
```

**"Resource not found":**
- Check you're using correct resource group
- Verify deployment name matches exactly

**"Access denied":**
- Ensure your account has contributor/owner role
- Check subscription is active

**API key issues:**
```bash
# Get keys for your resource
az cognitiveservices account keys list --name <account> --resource-group <rg>
```

## Cost Optimization Tips

With $4500 in credits:

1. **Monitor regularly** - Check usage weekly
2. **Use scripts** - Avoid keeping resources running idle
3. **Clean up** - Delete unused deployments
4. **Track spending** - Set up budget alerts in Azure Portal

## Useful Links

- [Azure Portal](https://portal.azure.com)
- [Azure CLI Docs](https://docs.microsoft.com/en-us/cli/azure/)
- [AI Foundry Docs](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [Cost Management](https://portal.azure.com/#view/Microsoft_Azure_Billing/SubscriptionsBlade)

## Examples

### Deploy a new model (when needed)

```bash
# Create deployment (requires az ml extension)
az ml model create --name <model-name> --path <path> --resource-group <rg> --workspace-name <ws>
```

### Check endpoint health

```bash
# Test if endpoint is responding
curl -I https://<endpoint>.cognitiveservices.azure.com/health
```

### List all deployments

```bash
az cognitiveservices account deployment list --name <account> --resource-group <rg>
```

## Integration with OpenCode

While OpenCode doesn't natively support Azure AI Foundry models, you can:

1. **Use the model scripts** (recommended)
2. **Create custom provider** (advanced)
3. **Use Azure OpenAI** (if you deploy GPT models)

The scripts in `/home/sarah/models/` provide seamless access to your Mistral and Kimi deployments.

---

*Azure CLI skill for managing cloud resources and AI deployments*
