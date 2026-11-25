---
name: aws-terraform
description: AWS infrastructure with Terraform. Use when creating modules, managing remote state, writing tftest.hcl tests, refactoring IaC or following HashiCorp style guide.
---

# AWS Terraform

Skill para desarrollo de infraestructura AWS con Terraform: módulos reutilizables, state remoto, style guide oficial de HashiCorp, testing con `.tftest.hcl`, seguridad, refactoring de módulos y estándares de IaC. Integra mejores prácticas de [HashiCorp Agent Skills](https://github.com/hashicorp/agent-skills).

## Principios fundamentales

- Infraestructura como código: todo recurso AWS se define en Terraform. Cero recursos manuales en consola.
- Módulos reutilizables: extraer patrones repetidos en módulos con interfaces claras (variables tipadas, outputs, validaciones).
- State remoto obligatorio: S3 + DynamoDB para locking. Nunca state local en equipo.
- Plan antes de apply: siempre revisar `terraform plan` antes de aplicar cambios.
- Style guide de HashiCorp: seguir convenciones oficiales de formato, naming y organización.

## Organización de archivos (HashiCorp Style Guide)

| Archivo | Propósito |
|---|---|
| `terraform.tf` | Versión de Terraform y required_providers |
| `providers.tf` | Configuración de providers |
| `main.tf` | Recursos principales y data sources |
| `variables.tf` | Variables de input (orden alfabético) |
| `outputs.tf` | Outputs (orden alfabético) |
| `locals.tf` | Valores locales calculados |

## Estructura de proyecto recomendada

```
infra/
├── environments/
│   ├── dev/
│   │   ├── terraform.tf
│   │   ├── providers.tf
│   │   ├── main.tf          # Llama a módulos
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── prod/
├── modules/
│   ├── api/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── tests/
│   │       └── api_test.tftest.hcl
│   ├── data/
│   └── compute/
└── terraform.tf              # Version constraints compartidas
```

## Style Guide (basado en HashiCorp oficial)

### Formato y convenciones
- 2 espacios por nivel de indentación (no tabs).
- Alinear signos `=` en argumentos consecutivos.
- Meta-arguments primero (`count`, `for_each`, `depends_on`), luego arguments, luego blocks, `lifecycle` al final.
- Ejecutar `terraform fmt -recursive` antes de cada commit.

### Naming
- Lowercase con underscores para todos los nombres.
- Nombres descriptivos excluyendo el tipo de recurso.
- Singular, no plural.
- `main` como nombre default cuando solo hay una instancia.

```hcl
# ❌ Malo
resource "aws_instance" "webAPI-aws-instance" {}
resource "aws_instance" "web_apis" {}

# ✅ Bueno
resource "aws_instance" "web_api" {}
resource "aws_vpc" "main" {}
```

### Variables: siempre con type, description y validation
```hcl
variable "environment" {
  description = "Target deployment environment"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "database_password" {
  description = "Password for the database admin user"
  type        = string
  sensitive   = true
}
```

### Outputs: siempre con description
```hcl
output "vpc_id" {
  description = "ID of the created VPC"
  value       = aws_vpc.main.id
}

output "database_password" {
  description = "Database administrator password"
  value       = aws_db_instance.main.password
  sensitive   = true
}
```

### Preferir for_each sobre count
```hcl
# ✅ for_each para recursos nombrados
variable "instance_names" {
  type    = set(string)
  default = ["web-1", "web-2", "web-3"]
}

resource "aws_instance" "web" {
  for_each = var.instance_names
  tags     = { Name = each.key }
}

# count solo para creación condicional
resource "aws_cloudwatch_metric_alarm" "cpu" {
  count = var.enable_monitoring ? 1 : 0
}
```

## State remoto

```hcl
# terraform.tf
terraform {
  required_version = ">= 1.7"

  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "env/dev/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

## Provider con default tags
```hcl
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

# Multi-region con alias
provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"
}
```

## Módulos reutilizables

### Diseño de módulo
```hcl
# modules/api/variables.tf
variable "name" {
  description = "Name prefix for API resources"
  type        = string
}

variable "lambda_invoke_arn" {
  description = "Lambda function invoke ARN for API integration"
  type        = string
}

variable "stage_name" {
  description = "API Gateway stage name"
  type        = string
  default     = "v1"
}

# modules/api/main.tf
resource "aws_apigatewayv2_api" "main" {
  name          = "${var.name}-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda" {
  api_id             = aws_apigatewayv2_api.main.id
  integration_type   = "AWS_PROXY"
  integration_uri    = var.lambda_invoke_arn
  payload_format_version = "2.0"
}

# modules/api/outputs.tf
output "api_endpoint" {
  description = "API Gateway endpoint URL"
  value       = aws_apigatewayv2_stage.main.invoke_url
}
```

### Refactoring de módulos (basado en HashiCorp refactor-module skill)
- Agrupar recursos acoplados (VPC + subnets) en un módulo.
- Interfaces explícitas: variables tipadas con validación, outputs para atributos consumidos.
- Usar `moved` blocks (Terraform 1.1+) para migrar state sin recrear recursos:

```hcl
moved {
  from = aws_instance.web
  to   = module.compute.aws_instance.web
}
```

- Siempre ejecutar `terraform plan` después de refactoring para verificar cero cambios.

## Testing con .tftest.hcl (Terraform 1.6+)

### Unit test (plan mode)
```hcl
# tests/api_test.tftest.hcl
run "test_api_gateway_created" {
  command = plan

  variables {
    name              = "test-api"
    lambda_invoke_arn = "arn:aws:lambda:us-east-1:123456789012:function:test"
    stage_name        = "v1"
  }

  assert {
    condition     = aws_apigatewayv2_api.main.protocol_type == "HTTP"
    error_message = "API Gateway should use HTTP protocol"
  }

  assert {
    condition     = aws_apigatewayv2_api.main.name == "test-api-api"
    error_message = "API name should include prefix"
  }
}
```

### Integration test (apply mode)
```hcl
run "test_full_deployment" {
  command = apply

  variables {
    name              = "integration-test"
    lambda_invoke_arn = "arn:aws:lambda:us-east-1:123456789012:function:test"
  }

  assert {
    condition     = output.api_endpoint != ""
    error_message = "API endpoint should not be empty after deployment"
  }
}
```

### Mock providers (Terraform 1.7+)
```hcl
mock_provider "aws" {
  mock_resource "aws_apigatewayv2_api" {
    defaults = {
      id = "mock-api-id"
    }
  }
}

run "test_with_mocks" {
  command = plan
  providers = { aws = aws }

  assert {
    condition     = aws_apigatewayv2_api.main.name == "test-api"
    error_message = "API name mismatch"
  }
}
```

## Seguridad en Terraform (basado en HashiCorp style guide)

- Cifrado en reposo por defecto en todos los recursos que lo soporten.
- Networking privado donde aplique.
- Least privilege en security groups.
- Nunca hardcodear credenciales o secretos.
- Marcar outputs sensibles con `sensitive = true`.

```hcl
# S3 bucket seguro
resource "aws_s3_bucket" "data" {
  bucket = "${var.project}-${var.environment}-data"
  tags   = local.common_tags
}

resource "aws_s3_bucket_versioning" "data" {
  bucket = aws_s3_bucket.data.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "data" {
  bucket                  = aws_s3_bucket.data.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

## Comandos esenciales

```bash
# Inicializar
terraform init

# Formatear
terraform fmt -recursive

# Validar sintaxis
terraform validate

# Plan (siempre antes de apply)
terraform plan -out=tfplan

# Apply
terraform apply tfplan

# Destroy (solo dev)
terraform destroy

# Import recurso existente
terraform import aws_instance.web i-1234567890abcdef0

# State operations
terraform state list
terraform state show aws_instance.web
terraform state mv aws_instance.old module.compute.aws_instance.new
```

## Version pinning
```hcl
terraform {
  required_version = ">= 1.7"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"  # Permite minor updates
    }
  }
}
```

Operadores: `= 1.0.0` (exacta), `>= 1.0.0` (mínima), `~> 1.0` (permite incremento del componente más a la derecha), `>= 1.0, < 2.0` (rango).

## Herramientas de validación

```bash
# Formato y validación básica
terraform fmt -recursive
terraform validate

# Linting
tflint --recursive

# Seguridad
tfsec .
checkov -d .

# Costos
infracost breakdown --path .
```

## Version control: qué commitear y qué no

| ✅ Commitear | ❌ No commitear |
|---|---|
| Todos los `.tf` | `terraform.tfstate` |
| `.terraform.lock.hcl` | `.terraform/` |
| | `*.tfplan` |
| | `.tfvars` con datos sensibles |

## Anti-patrones a evitar

- ❌ State local en equipo (sin S3 + DynamoDB locking).
- ❌ `terraform apply` sin `terraform plan` previo.
- ❌ Variables sin `type`, `description` ni `validation`.
- ❌ Hardcodear account IDs, ARNs o regiones.
- ❌ Un solo archivo `main.tf` gigante con toda la infra.
- ❌ Módulos sin tests `.tftest.hcl`.
- ❌ `count` para recursos nombrados (usar `for_each`).
- ❌ No usar `default_tags` en el provider.
- ❌ Recursos sin tags.
- ❌ No ejecutar `terraform fmt` antes de commit.
- ❌ Credenciales en `.tfvars` o en código.
- ❌ Ignorar `terraform validate` y `tflint`.

## Checklist de revisión Terraform

- [ ] Archivos organizados según convención (terraform.tf, providers.tf, main.tf, variables.tf, outputs.tf).
- [ ] `terraform fmt -recursive` ejecutado.
- [ ] `terraform validate` sin errores.
- [ ] Variables con type, description y validation donde aplique.
- [ ] Outputs con description.
- [ ] Naming: lowercase, underscores, descriptivo, singular.
- [ ] State remoto con S3 + DynamoDB locking.
- [ ] Provider con `default_tags`.
- [ ] Version constraints pinneadas.
- [ ] Módulos con tests `.tftest.hcl`.
- [ ] Seguridad: cifrado, public access bloqueado, least privilege.
- [ ] `tflint` y `tfsec`/`checkov` ejecutados.
- [ ] `.terraform.lock.hcl` commiteado.
