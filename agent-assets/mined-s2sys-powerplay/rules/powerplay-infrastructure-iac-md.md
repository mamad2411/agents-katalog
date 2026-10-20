---
name: infrastructure-iac
description: Infrastructure as Code standards — Terraform, CloudFormation, Bicep, IaC best practices, state management, GitOps
globs: ["**/*.tf", "**/*.json", "**/*.bicep", "**/*.yaml", "**/*.yml", "**/terraform/**", "**/cloudformation/**"]
alwaysApply: false
---

# Infrastructure as Code (IaC) Standards

Infrastructure as Code defines cloud resources declaratively. Master Terraform, CloudFormation, and Bicep for reproducible, version-controlled deployments.

---

## Terraform Best Practices

**ALWAYS**:
- Use modules for reusability (compute, network, database modules)
- Version providers and modules explicitly (prevent breaking changes)
- Use remote state (Terraform Cloud, S3 backend) — never local state
- Enable state locking (prevent concurrent modifications)
- Use workspaces for multiple environments (dev, staging, production)
- Implement least privilege IAM roles for Terraform execution
- Use variable validation (restrict invalid inputs)
- Review plan before apply (terraform plan)

**NEVER**:
- Store sensitive data in code (use variables, Secrets Manager)
- Use local state (breaks team collaboration)
- Run terraform from personal machines (use CI/CD)
- Modify state manually (always use terraform commands)

### ✅ GOOD Terraform Structure

```hcl
# Directory structure
# terraform/
# ├── main.tf (main resources)
# ├── variables.tf (input variables)
# ├── outputs.tf (outputs)
# ├── providers.tf (provider config)
# ├── terraform.tfvars (dev values)
# ├── modules/
# │   ├── network/
# │   │   ├── main.tf
# │   │   ├── variables.tf
# │   │   └── outputs.tf
# │   └── database/
# │       ├── main.tf
# │       ├── variables.tf
# │       └── outputs.tf
# └── environments/
#     ├── dev.tfvars
#     ├── staging.tfvars
#     └── production.tfvars

# providers.tf — Remote state + versioning
terraform {
  required_version = ">= 1.3.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"  # Allow patch updates only
    }
  }
  
  # Remote state (S3 backend)
  backend "s3" {
    bucket         = "terraform-state-prod"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Environment = var.environment
      Project     = var.project_name
      ManagedBy   = "Terraform"
    }
  }
}

# variables.tf — Input variables with validation
variable "environment" {
  description = "Environment name (dev, staging, production)"
  type        = string
  
  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be dev, staging, or production."
  }
}

variable "instance_count" {
  description = "Number of EC2 instances"
  type        = number
  default     = 1
  
  validation {
    condition     = var.instance_count > 0 && var.instance_count <= 10
    error_message = "Instance count must be between 1 and 10."
  }
}

# main.tf — Using modules
module "network" {
  source = "./modules/network"
  
  vpc_cidr            = var.vpc_cidr
  availability_zones  = var.availability_zones
  environment         = var.environment
}

module "database" {
  source = "./modules/database"
  
  environment    = var.environment
  db_name        = var.database_name
  db_user        = var.database_user
  db_password    = var.database_password  # From Secrets Manager
  subnet_ids     = module.network.private_subnet_ids
  security_group = module.network.db_security_group
}

# Resource
resource "aws_instance" "app" {
  count           = var.instance_count
  ami             = data.aws_ami.latest_amazon_linux.id
  instance_type   = var.instance_type
  subnet_id       = module.network.private_subnet_ids[count.index % length(module.network.private_subnet_ids)]
  security_groups = [module.network.app_security_group.id]
  
  tags = {
    Name = "app-${count.index + 1}"
  }
}

# outputs.tf
output "database_endpoint" {
  description = "Database connection endpoint"
  value       = module.database.endpoint
}

output "instance_ips" {
  description = "Private IPs of application instances"
  value       = aws_instance.app[*].private_ip
}

# Module: modules/network/main.tf
variable "vpc_cidr" {
  type = string
}

variable "availability_zones" {
  type = list(string)
}

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "vpc-${var.environment}"
  }
}

resource "aws_subnet" "private" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 4, count.index)
  availability_zone = var.availability_zones[count.index]
  
  tags = {
    Name = "private-${var.availability_zones[count.index]}"
  }
}

output "private_subnet_ids" {
  value = aws_subnet.private[*].id
}
```

---

## Terraform State Management

**ALWAYS**:
- Use remote state (S3, Terraform Cloud, Azure Storage)
- Enable state encryption (at rest + in transit)
- Enable state locking (DynamoDB, blob container lease)
- Backup state regularly (retention policy)
- Restrict state access (IAM, RBAC)
- Use separate state per environment (dev, staging, prod)
- Version state snapshots (git + archive)

**NEVER**:
- Commit .tfstate files to git (security risk)
- Manually edit state files
- Share state credentials
- Skip state backup

### ✅ GOOD Remote State Setup

```hcl
# S3 backend with encryption and locking
terraform {
  backend "s3" {
    bucket         = "terraform-state-production"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true                    # Server-side encryption
    dynamodb_table = "terraform-locks"       # State locking
    role_arn       = "arn:aws:iam::ACCOUNT:role/TerraformRole"
  }
}

# Create S3 bucket + DynamoDB lock table (bootstrap)
resource "aws_s3_bucket" "terraform_state" {
  bucket = "terraform-state-production"
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  
  versioning_configuration {
    status = "Enabled"  # Version all state changes
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_dynamodb_table" "terraform_locks" {
  name           = "terraform-locks"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "LockID"
  
  attribute {
    name = "LockID"
    type = "S"
  }
}
```

---

## CloudFormation Templates

**ALWAYS**:
- Use YAML format (more readable than JSON)
- Organize with nested stacks (modularity)
- Use parameter validation (AllowedValues, AllowedPattern)
- Use mappings for region-specific values
- Store templates in version control
- Use change sets before applying (preview changes)
- Enable termination protection on production stacks

**NEVER**:
- Hardcode account IDs or regions (use Pseudo parameters)
- Skip change set review
- Use UPDATE_REPLACE for production resources (data loss)

### ✅ GOOD CloudFormation Template

```yaml
# CloudFormation with nested stacks
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Production application stack'

Parameters:
  Environment:
    Type: String
    AllowedValues: [dev, staging, production]
    Default: dev
    Description: Environment name
  
  ApplicationName:
    Type: String
    Default: MyApp
    MinLength: 1
    MaxLength: 50
    Description: Application name

Mappings:
  EnvironmentConfig:
    dev:
      InstanceType: t3.micro
      DBInstanceClass: db.t3.micro
      DesiredCapacity: 1
    staging:
      InstanceType: t3.small
      DBInstanceClass: db.t3.small
      DesiredCapacity: 2
    production:
      InstanceType: t3.medium
      DBInstanceClass: db.r5.large
      DesiredCapacity: 3

Resources:
  NetworkStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/network.yaml
      Parameters:
        VpcCIDR: 10.0.0.0/16
        Environment: !Ref Environment

  DatabaseStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/database.yaml
      Parameters:
        DBInstanceClass: !FindInMap [EnvironmentConfig, !Ref Environment, DBInstanceClass]
        Environment: !Ref Environment
        VpcId: !GetAtt NetworkStack.Outputs.VpcId
        PrivateSubnetIds: !GetAtt NetworkStack.Outputs.PrivateSubnetIds

  ApplicationStack:
    Type: AWS::CloudFormation::Stack
    DependsOn: DatabaseStack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/application.yaml
      Parameters:
        InstanceType: !FindInMap [EnvironmentConfig, !Ref Environment, InstanceType]
        DesiredCapacity: !FindInMap [EnvironmentConfig, !Ref Environment, DesiredCapacity]
        Environment: !Ref Environment
        DatabaseEndpoint: !GetAtt DatabaseStack.Outputs.DBEndpoint

Outputs:
  ApplicationURL:
    Description: Application URL
    Value: !GetAtt ApplicationStack.Outputs.LoadBalancerURL
    Export:
      Name: !Sub '${ApplicationName}-URL'
  
  DatabaseEndpoint:
    Description: Database endpoint
    Value: !GetAtt DatabaseStack.Outputs.DBEndpoint
    Export:
      Name: !Sub '${ApplicationName}-DBEndpoint'
```

---

## Bicep (Azure IaC)

**ALWAYS**:
- Use symbolic names (friendly names, not Azure resource IDs)
- Use variables for reusability
- Use outputs to reference created resources
- Use metadata for documentation
- Organize with modules
- Use parameter decorators (validation)

**NEVER**:
- Hardcode property values (use parameters)
- Create resources without names
- Skip documentation

### ✅ GOOD Bicep Template

```bicep
// main.bicep
param environment string = 'dev'
param location string = resourceGroup().location
param applicationName string = 'myapp'

@minLength(1)
@maxLength(10)
param instanceCount int = 1

var resourcePrefix = '${applicationName}-${environment}'

// Network module
module networkModule 'modules/network.bicep' = {
  name: 'networkDeployment'
  params: {
    location: location
    vnetName: '${resourcePrefix}-vnet'
    environment: environment
  }
}

// Database
resource sqlDatabase 'Microsoft.Sql/servers/databases@2021-11-01' = {
  parent: sqlServer
  name: '${applicationName}db'
  location: location
  sku: {
    name: environment == 'production' ? 'S2' : 'S0'
  }
}

// App Service using module output
resource appService 'Microsoft.Web/sites@2022-03-01' = {
  name: '${resourcePrefix}-app'
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: appServicePlan.id
    virtualNetworkSubnetId: networkModule.outputs.appSubnetId
  }
}

// Outputs
@description('Application URL')
output applicationUrl string = 'https://${appService.properties.defaultHostName}'

@description('Database connection string')
output connectionString string = 'Server=${sqlServer.name}.database.windows.net;Database=${sqlDatabase.name};'

// modules/network.bicep
param vnetName string
param location string
param environment string

resource virtualNetwork 'Microsoft.Network/virtualNetworks@2021-12-01' = {
  name: vnetName
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.0.0.0/16'
      ]
    }
    subnets: [
      {
        name: 'app'
        properties: {
          addressPrefix: '10.0.1.0/24'
        }
      }
    ]
  }
}

output appSubnetId string = '${virtualNetwork.id}/subnets/app'
```

---

## GitOps with IaC

**ALWAYS**:
- Store IaC in git repository (version control)
- Use separate branches for environments (dev, staging, prod)
- Require pull request reviews before merging (approval workflow)
- Use CI/CD to apply infrastructure changes (terraform plan → apply)
- Tag releases with version numbers (reproducible deployments)
- Document infrastructure decisions in commit messages

**NEVER**:
- Apply changes manually (always via CI/CD)
- Skip PR reviews
- Merge directly to main without tests

### ✅ GOOD GitOps Workflow

```yaml
# .github/workflows/terraform.yml
name: Terraform Apply

on:
  push:
    branches: [main]
    paths: ['terraform/**']
  pull_request:
    paths: ['terraform/**']

jobs:
  plan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.3.0
      
      - name: Terraform Init
        working-directory: terraform
        run: terraform init
      
      - name: Terraform Plan
        working-directory: terraform
        run: terraform plan -out=tfplan
        env:
          TF_VAR_environment: ${{ github.ref == 'refs/heads/main' && 'production' || 'staging' }}
      
      - name: Comment PR with Plan
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: "Terraform plan ready for review"
            })

  apply:
    needs: plan
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - uses: hashicorp/setup-terraform@v2
      
      - name: Terraform Init
        working-directory: terraform
        run: terraform init
      
      - name: Terraform Apply
        working-directory: terraform
        run: terraform apply -auto-approve
        env:
          TF_VAR_environment: production
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

---

## IaC Security Checklist

- [ ] Terraform: Remote state, state locking, encrypted secrets
- [ ] CloudFormation: Change sets reviewed, nested stacks, parameter validation
- [ ] Bicep: Module organization, parameter validation, metadata
- [ ] State management: Encryption, backup, access control, versioning
- [ ] Variables: No hardcoded secrets, validation rules, defaults
- [ ] GitOps: All changes via CI/CD, PR approvals, version tags
- [ ] IAM: Least privilege role for IaC execution, MFA for sensitive changes
- [ ] Audit: CloudTrail logs, change tracking, cost estimation pre-apply

---

## Summary

Good Infrastructure as Code:
1. **Declarative** — Describe desired state, not steps
2. **Versioned** — All infrastructure in git with history
3. **Modular** — Reusable modules for common patterns
4. **Tested** — Plan review before apply, policy as code
5. **Secure** — Secrets external, state protected, least privilege
6. **Observable** — Logs tracked, changes audited, costs monitored

Master Terraform/CloudFormation/Bicep for repeatable, reliable cloud deployments.
