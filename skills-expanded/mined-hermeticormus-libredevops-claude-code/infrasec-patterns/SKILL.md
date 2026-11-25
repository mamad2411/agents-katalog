---
name: infrasec-patterns
description: "Infrastructure security patterns: Checkov in CI with SARIF output, Vault Agent injection on Kubernetes, Vault PKI for short-lived TLS certificates, an AWS security baseline in Terraform, and network hardening. Use when adding IaC security scanning or hardening cloud and Kubernetes infrastructure."
---

# InfraSec Patterns

Checkov GitHub Actions, Vault dynamic secrets, Security Group rules, GuardDuty remediation, CloudTrail analysis.

## Checkov in CI with SARIF Output

```yaml
# .github/workflows/security.yml
name: Infrastructure Security Scan
on:
  pull_request:
    paths: ['terraform/**', '*.tf', 'kubernetes/**', 'Dockerfile*']

permissions:
  contents: read
  security-events: write

jobs:
  checkov:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Checkov Terraform scan
        id: checkov-tf
        uses: bridgecrewio/checkov-action@master
        with:
          directory: terraform/
          framework: terraform
          output_format: sarif
          output_file_path: checkov-tf.sarif
          soft_fail: false
          # Skip checks with documented justification
          skip_check: >
            CKV_AWS_144,  # S3 cross-region replication not required (single-region design)
            CKV2_AWS_5    # Security group not attached to ENI (managed by ECS)

      - name: Checkov Kubernetes scan
        uses: bridgecrewio/checkov-action@master
        with:
          directory: kubernetes/
          framework: kubernetes
          output_format: sarif
          output_file_path: checkov-k8s.sarif

      - name: Checkov Dockerfile scan
        uses: bridgecrewio/checkov-action@master
        with:
          directory: .
          framework: dockerfile
          output_format: sarif
          output_file_path: checkov-docker.sarif

      - name: Upload Checkov results to GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: '.'
          category: checkov
```

## Vault Agent Kubernetes Injection

```yaml
# Kubernetes deployment with Vault Agent sidecar
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    metadata:
      annotations:
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/role: "myapp-prod"
        # Inject database credentials as file
        vault.hashicorp.com/agent-inject-secret-db-config: "database/creds/myapp-readwrite"
        vault.hashicorp.com/agent-inject-template-db-config: |
          {{- with secret "database/creds/myapp-readwrite" -}}
          DATABASE_URL=postgresql://{{ .Data.username }}:{{ .Data.password }}@db.prod:5432/myapp
          {{- end }}
        # Inject as env vars
        vault.hashicorp.com/agent-inject-secret-config: "secret/data/myapp/prod/config"
        vault.hashicorp.com/agent-inject-template-config: |
          {{- with secret "secret/data/myapp/prod/config" -}}
          {{- range $key, $value := .Data.data -}}
          {{ $key }}={{ $value }}
          {{ end -}}
          {{- end }}
    spec:
      serviceAccountName: myapp-sa
      containers:
        - name: app
          image: myapp:latest
          command: ["/bin/sh", "-c"]
          args: ["source /vault/secrets/db-config && node server.js"]
```

```hcl
# Vault Kubernetes auth method
resource "vault_auth_backend" "kubernetes" {
  type = "kubernetes"
  path = "kubernetes"
}

resource "vault_kubernetes_auth_backend_config" "main" {
  backend            = vault_auth_backend.kubernetes.path
  kubernetes_host    = var.k8s_api_server
  kubernetes_ca_cert = var.k8s_ca_cert
}

resource "vault_kubernetes_auth_backend_role" "myapp" {
  backend                          = vault_auth_backend.kubernetes.path
  role_name                        = "myapp-prod"
  bound_service_account_names      = ["myapp-sa"]
  bound_service_account_namespaces = ["production"]
  token_ttl                        = 3600
  token_policies                   = ["myapp-prod-policy"]
}
```

## Vault PKI for Short-Lived TLS Certs

```hcl
# Vault PKI engine -- internal mTLS certificates
resource "vault_mount" "pki" {
  path                      = "pki"
  type                      = "pki"
  default_lease_ttl_seconds = 86400   # 24hr cert TTL
  max_lease_ttl_seconds     = 604800  # 7 day max
}

resource "vault_pki_secret_backend_root_cert" "root" {
  backend     = vault_mount.pki.path
  type        = "internal"
  common_name = "myapp Internal CA"
  ttl         = "87600h"   # 10 years for root CA
}

resource "vault_pki_secret_backend_role" "server" {
  backend          = vault_mount.pki.path
  name             = "server"
  allowed_domains  = ["*.production.svc.cluster.local", "*.example.com"]
  allow_subdomains = true
  max_ttl          = "24h"
  require_cn       = false
}
```

```bash
# Issue cert for a service (Vault CLI)
vault write pki/issue/server \
  common_name="myapp.production.svc.cluster.local" \
  ttl="24h"

# Using Consul Template to auto-renew certs
template {
  source = "cert.tpl"
  destination = "/etc/ssl/myapp.crt"
  command = "systemctl reload myapp"
}
```

## AWS Security Baseline Terraform

```hcl
# Enable Security Hub with AWS Foundational Security Best Practices
resource "aws_securityhub_account" "main" {}

resource "aws_securityhub_standards_subscription" "fsbp" {
  depends_on    = [aws_securityhub_account.main]
  standards_arn = "arn:aws:securityhub:${var.region}::standards/aws-foundational-security-best-practices/v/1.0.0"
}

resource "aws_securityhub_standards_subscription" "cis" {
  depends_on    = [aws_securityhub_account.main]
  standards_arn = "arn:aws:securityhub:${var.region}::standards/cis-aws-foundations-benchmark/v/1.4.0"
}

# Enable GuardDuty
resource "aws_guardduty_detector" "main" {
  enable = true

  datasources {
    s3_logs { enable = true }
    kubernetes {
      audit_logs { enable = true }
    }
    malware_protection {
      scan_ec2_instance_with_findings {
        ebs_volumes { enable = true }
      }
    }
  }
}

# CloudTrail multi-region
resource "aws_cloudtrail" "org_trail" {
  name                          = "org-trail"
  s3_bucket_name                = aws_s3_bucket.trail.id
  include_global_service_events = true
  is_multi_region_trail         = true
  enable_log_file_validation    = true
  kms_key_id                    = aws_kms_key.trail.arn

  event_selector {
    read_write_type           = "All"
    include_management_events = true
  }

  insight_selector {
    insight_type = "ApiCallRateInsight"
  }

  insight_selector {
    insight_type = "ApiErrorRateInsight"
  }
}

# Config: require MFA for IAM users
resource "aws_config_config_rule" "iam_mfa" {
  name = "iam-user-mfa-enabled"

  source {
    owner             = "AWS"
    source_identifier = "IAM_USER_MFA_ENABLED"
  }
}

# Auto-remediation for non-compliant Config rules
resource "aws_config_remediation_configuration" "iam_mfa" {
  config_rule_name = aws_config_config_rule.iam_mfa.name
  target_type      = "SSM_DOCUMENT"
  target_id        = "AWSConfigRemediation-SetIAMPasswordPolicy"
  automatic        = false   # Require manual approval for IAM remediations
}
```

## Network Security Hardening

```hcl
# Remove default VPC security group rules (CIS 4.3)
resource "aws_default_security_group" "default" {
  vpc_id = aws_vpc.main.id
  # Empty ingress/egress blocks = deny all
}

# VPC Flow Logs to S3
resource "aws_flow_log" "main" {
  log_destination      = "arn:aws:s3:::${var.flow_log_bucket}/vpc-flow-logs/"
  log_destination_type = "s3"
  traffic_type         = "REJECT"   # Only rejected traffic (anomaly detection)
  vpc_id               = aws_vpc.main.id

  destination_options {
    file_format                = "parquet"    # Compressed, queryable with Athena
    hive_compatible_partitions = true
    per_hour_partition         = true
  }
}
```
