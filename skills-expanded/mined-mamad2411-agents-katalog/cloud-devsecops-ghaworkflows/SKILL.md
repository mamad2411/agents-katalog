---
name: cloud-devsecops-ghaworkflows
description: "Cloud Devsecops Ghaworkflows."
domain: cybersecurity
---

|
| SHA Pinning | Referencing GitHub Actions by their immutable commit SHA instead of mutable version tags |
| Script Injection | Attack where untrusted input (PR title, branch name) is interpolated into shell commands |
| GITHUB_TOKEN | Automatically generated token with configurable permissions scoped to the current repository |
| pull_request_target | Dangerous event trigger that runs in the base repo context with full permissions on fork PRs |
| Environment Protection | GitHub feature requiring manual approval before jobs accessing an environment can run |
| CODEOWNERS | File defining required reviewers for specific paths including workflow files |
| OIDC Federation | Using GitHub's OIDC token to authenticate to cloud providers without storing long-lived credentials |

## Tools & Systems

- **Dependabot**: Automated dependency updater that keeps pinned action SHAs current
- **StepSecurity Harden Runner**: GitHub Action that monitors and restricts outbound network calls from workflows
- **actionlint**: Linter for GitHub Actions workflow files that detects security issues
- **allstar**: GitHub App by OpenSSF that enforces security policies on repositories
- **scorecard**: OpenSSF tool that evaluates supply chain security practices including CI/CD

## Common Scenarios

### Scenario: Preventing Supply Chain Attack via Compromised Third-Party Action

**Context**: A widely-used GitHub Action is compromised and its v3 tag is updated to include credential-stealing code. Repositories using `@v3` automatically pull the malicious version.

**Approach**:
1. Pin all actions to SHA digests immediately across all repositories
2. Configure Dependabot for github-actions ecosystem to manage SHA updates
3. Restrict GITHUB_TOKEN permissions so even compromised actions have minimal access
4. Add StepSecurity harden-runner to detect anomalous outbound network calls
5. Review all third-party actions and replace unnecessary ones with inline scripts
6. Require CODEOWNERS approval for any changes to .github/workflows/

**Pitfalls**: SHA pinning without Dependabot means missing legitimate security updates to actions. Overly restrictive permissions can break legitimate workflows. Using `pull_request_target` for label-based gating still exposes secrets if the workflow checks out PR code.

## Output Format

```
GitHub Actions Security Audit
================================
Repository: org/web-application
Date: 2026-02-23

WORKFLOW ANALYSIS:
  Total workflows: 8
  Total action references: 34

SHA PINNING:
  [FAIL] 12/34 actions use mutable tags instead of SHA digests
  - .github/workflows/ci.yml: actions/setup-node@v4
  - .github/workflows/deploy.yml: aws-actions/configure-aws-credentials@v4

PERMISSIONS:
  [FAIL] 3/8 workflows have no explicit permissions (inherit default)
  [WARN] 1/8 workflows request write-all permissions

SCRIPT INJECTION:
  [FAIL] 2 workflow steps interpolate user input directly
  - .github/workflows/pr-check.yml:23: ${{ github.event.pull_request.title }}

SECRETS:
  [PASS] No secrets exposed in workflow logs
  [PASS] All production deployments use environment protection

SCORE: 6/10 (Remediate 5 HIGH findings)
```
