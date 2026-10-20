# Adding a New GitHub Variable for Cloud Run Service (via EnvVars + Python Config)

## 1. Define Terraform Variables

Add new variables to `variables.tf` with descriptions:

```hcl
variable "es_proxy_url" {
  type        = string
  description = "URL to the ElasticSearch cluster proxy."
}
# Repeat for other variables
```

## 2. Use GitHub Variables to set Terraform Variables

```yml
jobs:
  deploy_resources_services:
    steps:
      - name: Deploy Terraform stack
        working-directory: ${{ env.STORAGE_WD }}
        run: terraform apply -auto-approve
        env:
          # Existing variables
          TF_VAR_region: ${{vars.STORAGE_REGION}}
          # New variables
          TF_VAR_es_proxy_url: "${{vars.ES_PROXY_URL}}"
          # Add other proxy variables
```

## 3. Terraform Module Integration

Define environment variables in the services that require them.

Standard approach for our cloud run module is:

```hcl
module "results" {
  source        = "git::ssh://git@github.com/CroudTech/dst-terraform-module-cloud-run-microservice.git?ref=tags/v1.1.1"
  environment_variables = [
    # Existing variables
    {
      name  = "VERBOSE"
      value = var.verbose
    },
    # New variables
    {
      name  = "ES_PROXY_URL"
      value = var.es_proxy_url
    }
    # Add other proxy variables
  ]
}
```

If using concat, for example as api does:

```hcl
module "api" {
  source        = "git::ssh://git@github.com/CroudTech/dst-terraform-module-cloud-run-api-gateway.git?ref=tags/v1.0.0"
  environment_variables = concat([
    # Existing variables
    {
      name  = "GCP_REGION_ID"
      value = var.region
    },
    # New variables
    {
      name  = "ES_PROXY_URL"
      value = var.es_proxy_url
    }
    # Add other proxy variables
  ])
}
```

If directly defining a cloud run resource:

```hcl
resource "google_cloud_run_v2_service" "ai" {
  name        = local.ai_service_name
  template {
    containers {
      # Existing variables
      env {
        name  = "GCP_REGION_ID"
        value = var.region
      }
      # New variables
      env {
        name  = "ES_PROXY_URL"
        value = var.es_proxy_url
      }
      # Add other proxy variables
    }
  }
}
```

## 4. Create Python Config Class

Update `constants/constants.py` with a new config class:

```python
class _ESProxyConfig:
    ES_PROXY_URL_VAR = "ES_PROXY_URL"
    # Define all required variables as class attributes
    ES_PROXY_URL: EnvVar = EnvVar(name=ES_PROXY_URL_VAR)
```

## 5. Update Code to Use New Config

```python
# Import
from seomax.constants.constants import CONFIG

# Use
proxy_url = CONFIG.ES_PROXY.ES_PROXY_URL
```
