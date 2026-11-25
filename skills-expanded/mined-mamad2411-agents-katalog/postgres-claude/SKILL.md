# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Hereya package that provides PostgreSQL database deployment. It uses Docker containers for local development and automatically switches to AWS Aurora PostgreSQL when deployed to production.

## Commands

### Package Management
```bash
# Add this package to a project
hereya add hereya/postgres

# Deploy to a workspace
hereya deploy -w <workspace>

# Initialize Terraform
terraform init

# Plan Terraform changes
terraform plan

# Apply Terraform changes
terraform apply

# Destroy infrastructure
terraform destroy
```

### Development Environment
```bash
# Load environment variables (requires direnv)
direnv allow

# Set AWS profile and region manually if not using direnv
export AWS_PROFILE=hereya-dev
export AWS_REGION=eu-west-1
```

## Architecture

### Infrastructure Design
- **Local Development**: Deploys PostgreSQL as a Docker container using Terraform
- **Production**: Automatically switches to `hereya/aws-aurora-postgres` package via `onDeploy` configuration in `hereyarc.yml`
- **Data Persistence**: Configurable via `persist_data` variable, with optional custom `data_path`

### Key Files
- `hereyarc.yml`: Hereya package configuration that defines the deployment behavior
- `main.tf`: Terraform configuration for local PostgreSQL container
- `.envrc`: Environment variables for AWS configuration (used by direnv)

### Terraform Variables
- `port`: PostgreSQL port (default: 5432)
- `network_mode`: Docker network mode (default: "bridge")
- `persist_data`: Enable data persistence (default: true)
- `data_path`: Custom host path for data persistence (optional)

### Terraform Outputs
- `POSTGRES_URL`: Full PostgreSQL connection string
- `POSTGRES_ROOT_URL`: Root PostgreSQL connection string
- `DBNAME`: Generated database name

## Development Notes

- This is a pure Infrastructure as Code project - no build, test, or lint commands
- Uses `random_pet` provider to generate unique, friendly database names
- Data persistence logic in `main.tf` handles three scenarios:
  1. Custom `data_path` provided
  2. Auto-generated path based on database name
  3. Fallback to module directory
- The project assumes Docker is available and running on the local machine
- AWS credentials must be configured for production deployments