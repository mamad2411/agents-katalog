---
name: app-audit
description: Audit applications against your platform engineering constitution. Use when validating that code, configurations, and deployments align with organizational infrastructure standards.
license: MIT
metadata:
  author: radius-skills
  version: "1.0.0"
---

# App Audit

Audit applications and their infrastructure configurations against the standards defined in your `Platform-Engineering-Constitution.md`.

## Workflow

1. **Read the platform constitution.** Load `Platform-Engineering-Constitution.md` and extract all auditable standards (providers, regions, naming, tags, container standards, IaC conventions, network policies, secret management).
2. **Discover application artifacts.** Scan the repository for IaC files (`.bicep`, `.tf`, `*.yaml`), Dockerfiles, Kubernetes manifests, CI/CD configs, and application code.
3. **Run audit checks** against each category below.
4. **Generate an audit report** with findings, severity levels, and remediation recommendations.
5. **Present the report** to the user and offer to fix any issues found.

## Audit Categories

### 1. Cloud Provider & Region Compliance

Check that all infrastructure targets only approved providers and regions.

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Approved providers only | Provider blocks in Terraform, resource types in Bicep | 🔴 Critical |
| Approved regions only | `location`, `region` parameters in IaC | 🔴 Critical |
| No hardcoded cloud-specific resources in app.bicep | Should use portable Radius types | 🟡 Warning |

### 2. Container Standards

Verify Dockerfiles and container configurations meet standards.

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Non-root user | `USER` directive in Dockerfile (not root) | 🔴 Critical |
| Health endpoints | `/healthz` and `/readyz` endpoints in application code | 🟡 Warning |
| Multi-stage build | Multiple `FROM` stages in Dockerfile | 🟡 Warning |
| Image registry | Images reference approved registries (ACR, ECR) | 🟡 Warning |
| No `latest` tag in production | Image tags should be pinned | 🟡 Warning |

### 3. IaC Standards

Validate Terraform/Bicep follows constitution conventions.

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Approved IaC tooling | Only uses tooling listed in constitution | 🔴 Critical |
| Module versions pinned | `version = "~> X.Y"` in module blocks | 🟡 Warning |
| Remote state backend | `backend` block configured in Terraform | 🟡 Warning |
| Variables have descriptions | All `variable` blocks have `description` | 🟢 Info |
| Variables have type constraints | All `variable` blocks have `type` | 🟢 Info |
| `terraform fmt` clean | Code passes `terraform fmt -check` | 🟢 Info |

### 4. Naming Conventions

Verify resource names follow the constitution's pattern.

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Resource names match pattern | Names follow `<org>-<env>-<region>-<service>-<type>` | 🟡 Warning |
| Consistent casing | All lowercase, hyphens as separators | 🟢 Info |

### 5. Tagging / Labeling

Ensure all required tags are present.

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Required tags present | All tags from constitution (`environment`, `team`, `service`, `managed-by`, `cost-center`) | 🟡 Warning |
| No missing tags on resources | Every resource has all required tags | 🟡 Warning |

### 6. Network & Security

Validate network and security configurations.

| Check | What to look for | Severity |
|-------|-----------------|----------|
| NetworkPolicies defined | Kubernetes NetworkPolicy manifests exist | 🟡 Warning |
| No secrets in source code | Grep for API keys, passwords, tokens | 🔴 Critical |
| Secret management aligned | Uses approved secret management (K8s Secrets, Key Vault, Secrets Manager) | 🟡 Warning |
| RBAC enabled | Cluster configs enable RBAC | 🟡 Warning |

### 7. Radius-Specific Checks

If the app uses Radius, validate Radius configuration.

| Check | What to look for | Severity |
|-------|-----------------|----------|
| `bicepconfig.json` exists | Required for Radius Bicep extensions | 🔴 Critical |
| Portable resource types used | `Radius.*` or `Applications.Datastores/*` instead of cloud-specific | 🟡 Warning |
| `environment` parameter present | All Radius resources include `environment` | 🔴 Critical |
| Recipe properties set | Properties expected by recipes are declared (e.g., `size`) | 🟡 Warning |
| Connection env var handling | App code handles both `_PROPERTIES` JSON and individual vars | 🟡 Warning |
| Health probes configured | Container resources include readiness/liveness probes | 🟡 Warning |
| No local file paths in recipes | Recipe template paths use OCI registry URLs | 🔴 Critical |
| No `localhost` in image/recipe refs | Should use `host.docker.internal` or cloud registry | 🟡 Warning |

## Audit Report Format

```markdown
# Application Audit Report

**Repository:** <repo-name>
**Date:** <date>
**Constitution Version:** <version from changelog>

## Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | N |
| 🟡 Warning | N |
| 🟢 Info | N |
| ✅ Pass | N |

## Findings

### 🔴 Critical

#### [C1] <Finding Title>
- **File:** `path/to/file:line`
- **Issue:** Description of what's wrong
- **Constitution Reference:** Section N — <section title>
- **Remediation:** How to fix it

### 🟡 Warning

#### [W1] <Finding Title>
- **File:** `path/to/file:line`
- **Issue:** Description of what's wrong
- **Constitution Reference:** Section N — <section title>
- **Remediation:** How to fix it

### 🟢 Info

#### [I1] <Finding Title>
- **Recommendation:** Suggested improvement

### ✅ Passing Checks

- Provider compliance: ✅
- Region compliance: ✅
- Container non-root: ✅
- ...
```

## How to Run an Audit

When invoked, perform these steps:

1. **Find the constitution:**
   ```
   Look for Platform-Engineering-Constitution.md in repo root or parent directories
   ```

2. **Scan for artifacts:**
   ```bash
   # Find all auditable files
   find . -name "*.bicep" -o -name "*.tf" -o -name "Dockerfile*" \
          -o -name "*.yaml" -o -name "*.yml" -o -name "bicepconfig.json"
   ```

3. **Run checks** by reading each file and comparing against constitution rules.

4. **Check application code** for health endpoints, connection handling, and secret exposure:
   ```bash
   # Health endpoints
   grep -rn "healthz\|readyz" --include="*.go" --include="*.js" --include="*.py"
   
   # Secret patterns (flag for review)
   grep -rn "password\s*=\s*['\"]" --include="*.tf" --include="*.bicep"
   grep -rn "API_KEY\|SECRET_KEY\|PRIVATE_KEY" --include="*.go" --include="*.js" --include="*.py"
   
   # Connection handling
   grep -rn "CONNECTION_.*_PROPERTIES" --include="*.go" --include="*.js" --include="*.py"
   ```

5. **Generate the report** using the format above.

## Guardrails

- **Never modify files during an audit.** This skill is read-only. Only report findings and recommendations.
- **Always reference the constitution section** that each finding relates to.
- **Be specific about file paths and line numbers** in findings.
- **Offer to fix issues** after presenting the report, but wait for user approval.
- **Don't flag style issues** — only flag standards violations defined in the constitution.
- **Distinguish severity accurately** — Critical = security risk or hard policy violation, Warning = best practice deviation, Info = improvement opportunity.
- **Acknowledge passing checks** — don't just report failures. Show what's already compliant.
- **If no constitution exists**, tell the user and recommend using the `platform-constitution` skill to create one first.
