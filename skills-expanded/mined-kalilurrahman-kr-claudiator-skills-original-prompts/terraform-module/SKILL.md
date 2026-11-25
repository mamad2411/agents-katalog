---
name: terraform-module
description: Production Terraform modules for infrastructure as code. Outputs reusable modules with variables, state management, and CI/CD integration.
argument-hint: [infrastructure type, cloud provider, module scope]
allowed-tools: Read, Write, Bash
---

# Terraform Module Design

Design reusable Terraform modules for infrastructure as code. Not basic HCL — proper module structure, variables, outputs, state management, and multi-environment deployment.

## Process

1. **Define scope.** VPC, EC2, RDS, S3, entire application stack.
2. **Structure module.** Variables, resources, outputs, data sources.
3. **Manage state.** Remote backend (S3 + DynamoDB), workspaces.
4. **Add validation.** Variable constraints, preconditions, lifecycle rules.
5. **Version modules.** Git tags, module registry, semantic versioning.
6. **Plan environments.** Dev, staging, production with tfvars.
7. **Integrate CI/CD.** terraform plan on PR, apply on merge.

## Output Format

### Terraform Module: [Infrastructure Component]

**Provider:** AWS  
**Resources:** VPC, subnets, NAT, security groups  
**State Backend:** S3 + DynamoDB locking  
**Environments:** dev, staging, prod  
**Version:** 1.2.0

---

## Module Structure

```
terraform-aws-vpc/
├── main.tf              # Primary resources
├── variables.tf         # Input variables
├── outputs.tf           # Output values
├── versions.tf          # Provider versions
├── README.md            # Documentation
├── examples/
│   ├── simple/          # Basic usage
│   └── complete/        # Full example
└── modules/
    ├── subnets/         # Nested module
    └── nat/             # Nested module
```

---

## Basic Module (VPC)

### main.tf
```hcl
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = var.enable_dns_hostnames
  enable_dns_support   = var.enable_dns_support

  tags = merge(
    var.tags,
    {
      Name = var.vpc_name
    }
  )
}

resource "aws_subnet" "public" {
  count = length(var.public_subnet_cidrs)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = var.azs[count.index]
  map_public_ip_on_launch = true

  tags = merge(
    var.tags,
    {
      Name = "${var.vpc_name}-public-${count.index + 1}"
      Type = "Public"
    }
  )
}

resource "aws_subnet" "private" {
  count = length(var.private_subnet_cidrs)

  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = var.azs[count.index]

  tags = merge(
    var.tags,
    {
      Name = "${var.vpc_name}-private-${count.index + 1}"
      Type = "Private"
    }
  )
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = merge(
    var.tags,
    {
      Name = "${var.vpc_name}-igw"
    }
  )
}

resource "aws_eip" "nat" {
  count  = var.enable_nat_gateway ? length(var.public_subnet_cidrs) : 0
  domain = "vpc"

  tags = merge(
    var.tags,
    {
      Name = "${var.vpc_name}-nat-eip-${count.index + 1}"
    }
  )
}

resource "aws_nat_gateway" "main" {
  count = var.enable_nat_gateway ? length(var.public_subnet_cidrs) : 0

  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id

  tags = merge(
    var.tags,
    {
      Name = "${var.vpc_name}-nat-${count.index + 1}"
    }
  )

  depends_on = [aws_internet_gateway.main]
}
```

### variables.tf
```hcl
variable "vpc_name" {
  description = "Name of the VPC"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "Must be valid IPv4 CIDR."
  }
}

variable "azs" {
  description = "Availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]
}

variable "enable_nat_gateway" {
  description = "Enable NAT Gateway for private subnets"
  type        = bool
  default     = true
}

variable "enable_dns_hostnames" {
  description = "Enable DNS hostnames in VPC"
  type        = bool
  default     = true
}

variable "enable_dns_support" {
  description = "Enable DNS support in VPC"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}
```

### outputs.tf
```hcl
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}

output "public_subnet_ids" {
  description = "IDs of public subnets"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "IDs of private subnets"
  value       = aws_subnet.private[*].id
}

output "nat_gateway_ids" {
  description = "IDs of NAT gateways"
  value       = aws_nat_gateway.main[*].id
}

output "internet_gateway_id" {
  description = "ID of Internet Gateway"
  value       = aws_internet_gateway.main.id
}
```

### versions.tf
```hcl
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

---

## Usage Example

```hcl
# main.tf (root module)
module "vpc" {
  source  = "git::https://github.com/company/terraform-aws-vpc.git?ref=v1.2.0"

  vpc_name = "production-vpc"
  vpc_cidr = "10.0.0.0/16"

  azs                  = ["us-east-1a", "us-east-1b", "us-east-1c"]
  public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_subnet_cidrs = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]

  enable_nat_gateway = true

  tags = {
    Environment = "production"
    Project     = "my-app"
    ManagedBy   = "Terraform"
  }
}

# Use outputs
resource "aws_instance" "app" {
  subnet_id = module.vpc.private_subnet_ids[0]
  # ...
}
```

---

## Remote State Backend

### backend.tf
```hcl
terraform {
  backend "s3" {
    bucket         = "my-company-terraform-state"
    key            = "vpc/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

### Create S3 + DynamoDB for state
```hcl
# bootstrap/main.tf
resource "aws_s3_bucket" "terraform_state" {
  bucket = "my-company-terraform-state"

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  versioning_configuration {
    status = "Enabled"
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

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-state-lock"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
```

---

## Multi-Environment Setup

### environments/dev/terraform.tfvars
```hcl
vpc_name = "dev-vpc"
vpc_cidr = "10.1.0.0/16"

public_subnet_cidrs  = ["10.1.1.0/24", "10.1.2.0/24"]
private_subnet_cidrs = ["10.1.11.0/24", "10.1.12.0/24"]

azs = ["us-east-1a", "us-east-1b"]

enable_nat_gateway = false  # Save costs in dev

tags = {
  Environment = "dev"
  ManagedBy   = "Terraform"
}
```

### environments/prod/terraform.tfvars
```hcl
vpc_name = "prod-vpc"
vpc_cidr = "10.0.0.0/16"

public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
private_subnet_cidrs = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]

azs = ["us-east-1a", "us-east-1b", "us-east-1c"]

enable_nat_gateway = true

tags = {
  Environment = "production"
  ManagedBy   = "Terraform"
}
```

### Deploy to environment
```bash
cd environments/dev
terraform init
terraform plan
terraform apply

cd ../prod
terraform init
terraform plan
terraform apply
```

---

## Data Sources

```hcl
# Get latest Amazon Linux 2 AMI
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Get current AWS account ID
data "aws_caller_identity" "current" {}

# Get available AZs
data "aws_availability_zones" "available" {
  state = "available"
}

# Use data sources
resource "aws_instance" "app" {
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = "t3.micro"

  tags = {
    Account = data.aws_caller_identity.current.account_id
  }
}
```

---

## Lifecycle Rules

```hcl
resource "aws_instance" "app" {
  ami           = var.ami_id
  instance_type = var.instance_type

  lifecycle {
    create_before_destroy = true  # Create new before destroying old
    prevent_destroy       = false
    ignore_changes        = [ami]  # Don't replace on AMI update
  }
}

resource "aws_s3_bucket" "data" {
  bucket = "critical-data-bucket"

  lifecycle {
    prevent_destroy = true  # Can't be destroyed
  }
}
```

---

## Conditional Resources

```hcl
resource "aws_eip" "nat" {
  count  = var.enable_nat_gateway ? var.az_count : 0
  domain = "vpc"
}

resource "aws_db_instance" "replica" {
  count = var.create_read_replica ? 1 : 0

  replicate_source_db = aws_db_instance.primary.id
  instance_class      = var.replica_instance_class
}

# Dynamic blocks
resource "aws_security_group" "app" {
  name   = "app-sg"
  vpc_id = var.vpc_id

  dynamic "ingress" {
    for_each = var.ingress_rules

    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }
}
```

---

## CI/CD Integration

### GitHub Actions
```yaml
name: Terraform

on:
  pull_request:
    paths:
      - 'terraform/**'
  push:
    branches: [main]

jobs:
  terraform:
    runs-on: ubuntu-latest
    env:
      AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
      AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

    steps:
      - uses: actions/checkout@v3

      - uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.5.0

      - name: Terraform Format
        run: terraform fmt -check -recursive

      - name: Terraform Init
        run: terraform init
        working-directory: ./terraform

      - name: Terraform Validate
        run: terraform validate
        working-directory: ./terraform

      - name: Terraform Plan
        if: github.event_name == 'pull_request'
        run: terraform plan -no-color
        working-directory: ./terraform

      - name: Terraform Apply
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        run: terraform apply -auto-approve
        working-directory: ./terraform
```

---

## Testing Terraform

### Terratest (Go)
```go
package test

import (
	"testing"
	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

func TestVPCModule(t *testing.T) {
	terraformOptions := &terraform.Options{
		TerraformDir: "../examples/simple",
		Vars: map[string]interface{}{
			"vpc_name": "test-vpc",
			"vpc_cidr": "10.99.0.0/16",
		},
	}

	defer terraform.Destroy(t, terraformOptions)
	terraform.InitAndApply(t, terraformOptions)

	vpcID := terraform.Output(t, terraformOptions, "vpc_id")
	assert.NotEmpty(t, vpcID)

	subnetIDs := terraform.OutputList(t, terraformOptions, "public_subnet_ids")
	assert.Equal(t, 3, len(subnetIDs))
}
```

---

## Common Patterns

### Count vs For_Each
```hcl
# Count (positional)
resource "aws_subnet" "public" {
  count      = 3
  cidr_block = var.public_cidrs[count.index]
}

# For_Each (key-based, better for updates)
resource "aws_subnet" "public" {
  for_each = toset(var.public_cidrs)

  cidr_block = each.value
}
```

### Locals
```hcl
locals {
  common_tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
    Project     = var.project_name
  }

  vpc_name = "${var.project_name}-${var.environment}-vpc"
}

resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
  tags       = local.common_tags
}
```

## Rules

- Remote state backend (S3 + DynamoDB) required for team collaboration — prevents concurrent edits.
- Module versioning with Git tags mandatory — pin module versions in production.
- Variables must have descriptions and types — self-documenting infrastructure.
- Outputs for all important resource IDs — enables module composition.
- Validate variables with validation blocks — catch errors at plan time.
- Never hardcode credentials — use AWS roles, environment variables, or secret managers.
- Tag all resources with Environment, ManagedBy, Project — cost tracking and ownership.
- Use terraform fmt before commits — consistent code style.
- Plan before apply, always — review changes before executing.
- Separate state per environment (dev/staging/prod) — isolate blast radius.
