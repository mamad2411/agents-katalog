---
name: infrastructure-testing
description: >-
  Testing strategies for Terraform, Bicep, and Azure infrastructure. Covers
  static analysis, plan validation, deployment testing, policy compliance,
  smoke tests, and canary deployments.
when-to-use: >-
  Invoke when adding tests to infrastructure code, validating Terraform or
  Bicep deployments, designing post-deployment checks, or building CI
  pipeline quality gates for infrastructure changes.
categories:
  - testing
  - infrastructure
  - terraform
  - bicep
---

# Infrastructure Testing

Infrastructure without tests is infrastructure that breaks in production. Test at every stage: before plan, after plan, after deploy.

## Testing Pyramid for Infrastructure

```
         ╱ Canary / Smoke ╲        ← Post-deployment, live traffic
        ╱  Deploy Validation ╲     ← Assert deployed resource config
       ╱   Plan Validation    ╲    ← Inspect plan output
      ╱    Static Analysis     ╲   ← Lint, format, security scan
```

Run the bottom of the pyramid in seconds. Reserve the top for pipeline stages.

---

## Terraform Testing

### Static Analysis (Seconds)

| Tool | Purpose | Speed |
|---|---|---|
| `terraform validate` | Syntax and internal consistency | Seconds |
| `terraform fmt` | Format compliance | Seconds |
| **tflint** (azurerm ruleset) | Deprecated arguments, invalid values, naming | Seconds |
| **Checkov** | Security and compliance scanning (CIS, NIST, PCI-DSS) | Seconds |

Run all four on every commit. No exceptions.

### Plan Validation (Minutes)

- `terraform plan` — preview changes, catch unexpected destroys, identify drift
- **terraform-compliance** — BDD-style policy testing against plan output
- Plan assertions — programmatic inspection of plan JSON for expected resource counts
- **Infracost** — estimate cost impact of planned changes before apply

### Terraform Test Framework (Minutes)

Native `terraform test` command — HCL-based tests that deploy, validate, and destroy:

- Tests run in isolated environments to avoid impacting real infrastructure
- Assert on resource attributes, output values, and data source results
- Runs as part of CI pipeline — fail the build on test failure

### Terratest (Go, 5-30 Minutes)

Full lifecycle testing: deploy → validate with Azure SDK calls → destroy:

- Best for complex validation requiring programmatic inspection
- Supports retry logic for eventual consistency in cloud resources
- Parallel test execution for faster feedback
- Use for module testing before publishing to registry

---

## Bicep Testing

### What-If Operations

- `az deployment group what-if` — preview changes without deploying
- Available at all scopes: resource group, subscription, management group, tenant
- Use `--confirm-with-what-if` to preview and prompt before deploying
- Integrate into PR validation to show reviewers what will change

### ARM-TTK (Template Test Toolkit)

- Validates ARM/Bicep templates against best practices
- Checks parameter naming, secure parameter usage, API versions
- Run as part of CI to catch template issues early

### Pester for Deployment Validation

Post-deployment validation using PowerShell and Pester:

```powershell
Describe "Storage Account" {
    It "Should have HTTPS-only enabled" {
        $sa = Get-AzStorageAccount -ResourceGroupName $rgName -Name $saName
        $sa.EnableHttpsTrafficOnly | Should -Be $true
    }

    It "Should have TLS 1.2 minimum" {
        $sa = Get-AzStorageAccount -ResourceGroupName $rgName -Name $saName
        $sa.MinimumTlsVersion | Should -Be "TLS1_2"
    }
}
```

- Query deployed resources with `Get-AzResource` and assert configuration
- Verify NSG rules, encryption settings, managed identity assignments
- Publish test results as NUnit XML for pipeline consumption

---

## Policy Testing

### Azure Policy Compliance

- Verify deployed resources comply with assigned policies
- Use `Get-AzPolicyState` to check compliance status programmatically
- Test policy definitions in isolated subscriptions before broad assignment
- Validate deny policies by attempting non-compliant deployments (expect failure)

### Resource Deployment Validation

- After every deployment, verify resources match the specification
- Check SKUs, regions, networking rules, identity configuration
- Use Azure Resource Graph for efficient bulk queries across resources
- Script validations and run as post-deployment pipeline stage

---

## Smoke Tests After Deployment

Run immediately after every deployment:

- [ ] Hit health check endpoints
- [ ] Verify DNS resolution and TLS certificates
- [ ] Check port connectivity to dependencies
- [ ] Verify application can reach database, cache, APIs
- [ ] Validate configuration values (connection strings, feature flags)
- [ ] Automated smoke tests block promotion to next environment on failure

---

## Canary Deployments

- Route small percentage of traffic to new version first
- Monitor error rates, latency, and resource consumption during canary window
- Automated rollback if metrics degrade beyond threshold
- Gradually increase traffic percentage as confidence grows
- Use Azure Traffic Manager, Front Door, or Kubernetes canary strategies

---

## CI Pipeline Integration

| Stage | What Runs | Blocks PR? |
|---|---|---|
| Pre-commit | `terraform fmt`, `terraform validate`, tflint | Yes |
| PR validation | Checkov, terraform-compliance, `what-if` | Yes |
| Plan review | `terraform plan` output in PR comment, Infracost | Advisory |
| Post-deploy (dev) | Pester assertions, smoke tests | Yes (blocks staging) |
| Post-deploy (staging) | Full integration + smoke tests | Yes (blocks prod) |
| Post-deploy (prod) | Smoke tests, canary monitoring | Triggers rollback |

## Related Skills

- `terraform-style-guide` — Terraform formatting and structure
- `bicep-style-guide` — Bicep formatting and structure
- `pipeline-quality-gates` — CI/CD quality gate configuration
- `testing-strategy` — General testing strategy and pyramid
