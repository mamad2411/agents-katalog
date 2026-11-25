---
name: aws-networking
description: "Design secure VPC topologies, transit gateways, NAT gateways, VPC endpoints, and Route 53 routing."
type: procedural
category: cloud
domain: cloud
version: 1.0.0
author: "All-Skills Canonical Engineering Team"
license: "MIT"
risk: low
level: intermediate
triggers:
  - "aws vpc network architecture"
  - "transit gateway vpc endpoints"
keywords:
  - "aws"
  - "vpc"
  - "networking"
  - "transit-gateway"
provenance:
  source_repository: "all-skills/canonical"
  source_commit: "HEAD"
  source_path: "skills/cloud/aws-networking"
  imported_at: "2026-09-22T05:32:01.342370+00:00"
  license: "MIT"
  trust:
    level: trusted
    security_scan: passed
    behavioral_eval: passed
---

# AWS VPC & Network Architecture

## Purpose

Design secure VPC topologies, transit gateways, NAT gateways, VPC endpoints, and Route 53 routing.

This canonical skill provides deterministic, production-grade operational directives for AI agents executing autonomous engineering and verification tasks within the `cloud` domain.

## When to Use

- When designing, developing, optimizing, or debugging within `cloud` tasks.
- When an autonomous agent requires deterministic execution patterns for `aws-networking`.
- When verifying compliance, architecture, or performance standards in this domain.

## When NOT to Use

- When operating outside the scope of `cloud` engineering.
- When a more specialized sub-skill or external toolchain is explicitly requested by the user.

## Capabilities

- Structural design and implementation for AWS VPC & Network Architecture.
- Automated verification, schema compliance, and diagnostic troubleshooting.
- Performance profiling, security posture hardening, and error recovery.

## Inputs

- Project source files, configuration manifests, or task instructions.
- Target runtime environment parameters and toolchain dependencies.

## Workflow

1. **Pre-flight Assessment**: Inspect existing configuration and environment preconditions.
2. **Implementation & Transformation**: Apply focused, AST-aware structural modifications.
3. **Verification & Audit**: Execute domain-specific test suites, syntax checks, or simulation passes.
4. **Resolution**: Resolve any detected regressions or failure modes prior to completion.

## Tools

- Project-approved terminal tools, file editors, and verification test harnesses.

## Examples

- Standard operational execution pattern for `aws-networking`:
  ```bash
  # Verify environment readiness and execute task workflow
  allskills route "aws-networking"
  ```

## Safety

- Maintain strict workspace boundary sandboxing.
- Prevent unvetted credential exposure and destructive disk operations.
- Ensure all modifications are verified before concluding execution.

## Source

All-Skills Canonical Engineering Framework.

## Notes

- Pairs with relevant testing, linting, and architecture verification skills across the platform.
