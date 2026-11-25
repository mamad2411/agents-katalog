---
name: devops-iac
description: "Infrastructure as Code con OpenTofu (última versión 1.x estable), Terraform y Pulumi. Cubre estado remoto, modules, workspaces, providers cloud (AWS/GCP/Azure), Bicep para Azure, y mejores prácticas de IaC. Actívala al definir infraestructura como código, migrar de Terraform a OpenTofu, o gestionar cloud resources."
disable-model-invocation: true
---

# Infrastructure as Code

Guía de IaC. **OpenTofu (última versión 1.x estable) como default.** Terraform y Pulumi como alternativas.

---

## Elección de herramienta

| Herramienta | Licencia | Mejor para |
|-------------|----------|------------|
| **OpenTofu (última versión 1.x estable)** | MPL 2.0 (open source) | ✅ Default recomendado. Vendor-neutral, state encryption nativo |
| **Terraform** | BSL (cambió en 2023) | Equipos atados a HCP/Terraform Enterprise |
| **Pulumi** | Apache 2.0 | Infraestructura en lenguajes de propósito general (TS, Python, Go) |
| **Bicep** | MIT | Solo Azure. DSL nativo de Microsoft. |

---

## OpenTofu (última versión 1.x estable)

### Estructura de proyecto

```
infra/
├── main.tf              # Provider + backend
├── variables.tf          # Variables de entrada
├── outputs.tf            # Outputs
├── terraform.tfvars      # Valores para variables
├── modules/
│   ├── kubernetes/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── database/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
└── environments/
    ├── staging/
    │   ├── main.tf
    │   └── terraform.tfvars
    └── production/
        ├── main.tf
        └── terraform.tfvars
```

### Backend remoto (S3/GCS/Azure)

```hcl
# main.tf
terraform {
  backend "s3" {
    bucket  = "miapp-tfstate"
    key     = "production/terraform.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}

provider "aws" {
  region = var.region
}
```

### Módulos

```hcl
# modules/database/main.tf
variable "instance_class" { type = string }
variable "allocated_storage" { type = number }
variable "db_name" { type = string }
variable "username" { type = string }
variable "password" { type = string, sensitive = true }

resource "aws_db_instance" "main" {
  identifier        = "miapp-${var.environment}"
  engine            = "postgres"
  engine_version    = "18.1"
  instance_class    = var.instance_class
  allocated_storage = var.allocated_storage
  db_name           = var.db_name
  username          = var.username
  password          = var.password
  storage_encrypted = true
  backup_retention_period = 30
  skip_final_snapshot     = false
  final_snapshot_identifier = "miapp-final-${var.environment}"
}

output "endpoint" {
  value     = aws_db_instance.main.endpoint
  sensitive = true
}

# Uso en environment
module "database" {
  source = "../../modules/database"

  instance_class    = "db.t4g.medium"
  allocated_storage = 100
  db_name           = "miapp"
  username          = var.db_username
  password          = var.db_password
}
```

### State encryption (nativo en OpenTofu)

```hcl
terraform {
  encryption {
    key_provider "aws_kms" "main" {
      kms_key_id = "alias/tfstate-key"
      region     = "us-east-1"
    }
    method "aes_gcm" "default" {
      keys = [key_provider.aws_kms.main]
    }
    state {
      method = method.aes_gcm.default
    }
  }
}
```

### Workspaces (entornos)

```bash
tofu workspace new staging
tofu workspace new production

tofu workspace select staging
tofu apply -var-file=environments/staging/terraform.tfvars
```

---

## Pulumi (TypeScript/Python)

```typescript
import * as aws from "@pulumi/aws";

const db = new aws.rds.Instance("miapp-db", {
  engine: "postgres",
  engineVersion: "18.1",
  instanceClass: "db.t4g.medium",
  allocatedStorage: 100,
  dbName: "miapp",
  username: "admin",
  password: config.requireSecret("dbPassword"),
  storageEncrypted: true,
  backupRetentionPeriod: 30,
  skipFinalSnapshot: false,
  finalSnapshotIdentifier: "miapp-final",
});

export const dbEndpoint = db.endpoint;
```

---

## Bicep (Azure)

```bicep
param location string = resourceGroup().location
param dbName string
param adminPassword string

@secure()
param adminPassword string

resource postgresServer 'Microsoft.DBforPostgreSQL/flexibleServers@2024-08-01' = {
  name: 'miapp-pg-${uniqueString(resourceGroup().id)}'
  location: location
  sku: { name: 'Standard_B2ms', tier: 'Burstable' }
  properties: {
    administratorLogin: 'pgadmin'
    administratorLoginPassword: adminPassword
    version: '18'
    storage: { storageSizeGB: 100 }
    backup: { backupRetentionDays: 30 }
  }
}

output connectionString string = 'Host=${postgresServer.properties.fullyQualifiedDomainName};Database=${dbName}'
```

---

## Mejores prácticas IaC

```hcl
# ✅ Variables tipadas con validación
variable "environment" {
  type    = string
  validation {
    condition     = contains(["staging", "production"], var.environment)
    error_message = "Environment must be staging or production"
  }
}

# ✅ Secrets como variables sensitive (nunca en output)
variable "db_password" {
  type      = string
  sensitive = true
}

# ✅ Tags obligatorios
locals {
  required_tags = {
    Environment = var.environment
    Project     = "miapp"
    Owner       = "platform-team"
    ManagedBy   = "opentofu"
  }
}

# ✅ .gitignore
# *.tfstate
# *.tfstate.*
# .terraform/
# terraform.tfvars (si contiene secrets)
```

---

## Flujo de trabajo

```bash
# 1. Validar
tofu validate
tofu fmt -check

# 2. Plan (revisar cambios)
tofu plan -out=tfplan

# 3. Review entre pares del plan

# 4. Aplicar
tofu apply tfplan

# 5. Ver outputs
tofu output
```

---

## Checklist IaC

- [ ] Estado remoto (S3/GCS/Azure) con encriptación
- [ ] State locking (DynamoDB/Consul) para evitar conflictos
- [ ] Módulos reutilizables para componentes comunes (DB, K8s cluster)
- [ ] Variables tipadas con validación
- [ ] Secrets marcados como `sensitive` (no en logs/outputs)
- [ ] Tags obligatorios en todos los recursos
- [ ] `.gitignore` excluye `.tfstate` y `.terraform/`
- [ ] CI: `tofu validate` + `tofu fmt -check` + `tofu plan`
- [ ] Plan revisado por pares antes de apply
