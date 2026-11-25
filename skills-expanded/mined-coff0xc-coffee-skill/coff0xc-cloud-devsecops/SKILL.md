---
name: coff0xc-cloud-devsecops
description: "Use when the user requests cloud, container, Kubernetes/K8s, serverless, DevSecOps, supply chain, CI/CD, or secrets: AWS/Azure/GCP, IAM, S3/Blob/GCS, Docker, Terraform/IaC, GitHub Actions, SBOM/SCA, secret scanning, pipeline risk. Manual trigger: Use coff0xc-cloud-devsecops."
---

# coff0xc-cloud-devsecops

<!-- skill-id: cs-cds-0e9b4c6a -->

## Quick Rules (read this first for everyday tasks)
> **[Read-only first]** Look first at IaC, K8s, Dockerfiles, CI workflows, dependencies, and secret exposure; do not change the cloud by default.
> **[Control mapping]** Map issues to identity, network, secrets, images, supply chain, pipeline, and audit logs.
> **[Verification gate]** Provide minimal fixes, config diffs, scan/policy checks, and residual risk.
> **[Hard boundary]** Confirm first for cloud resource writes, permission changes, CI/CD releases, secret rotation, and production cluster actions.

Follow this section first for ordinary cloud/DevSecOps reviews; expand the full workflow only for real environment changes, release gates, or multi-cloud architecture review.

## Capability
Read-only-first assessment capability for cloud-native, containers, CI/CD, supply chain, and secret governance. The goal is risks with evidence, fixes that can land, and verification that can be reproduced.

## What It Can Deliver
- Cloud/IaC/K8s/CI/CD risk inventory
- Least-privilege, network isolation, pipeline gate, and secret-rotation recommendations
- SBOM/SCA/secret-scanning strategy
- Local lint/plan/read-only checks and verification path

## What Input It Can Take
- Terraform/CloudFormation, K8s manifests, Dockerfiles
- GitHub Actions/CI configuration, lockfiles, SBOMs, image scan results
- Cloud account read-only output, logs, env examples, secret-discovery leads

## Safe-Use Boundaries
- Read-only analysis of local configuration and authorized evidence by default
- Cloud writes, IaC apply, kubectl apply/delete, workflow dispatch, and secret revocation must be confirmed first
- When a secret value is found, report only its type, location, and handling recommendation; do not repeat the full value
- Security capabilities are used only for authorized, defensive, detection, hardening, validation, and reporting purposes by default; do not provide unauthorized attack, credential theft, persistence, detection evasion, C2, phishing collection, data exfiltration, or destructive steps.

## Why You Can Trust It
- Reviews by identity, network, data, runtime, and supply-chain layers
- Distinguishes configuration risk from genuinely reachable risk
- Outputs fix priority and rollback/verification methods

## Typical Usage
```text
Use coff0xc-cloud-devsecops to check Docker, K8s, CI/CD, and supply-chain risks.
Use coff0xc-cloud-devsecops to assess IAM, S3 exposure, and serverless permissions in Terraform.
Use coff0xc-cloud-devsecops to harden this GitHub Actions workflow and secret usage.
```

## Default Output
- Close with only done, verified, remaining, and next steps; give a path or location for any file/code/rule artifacts.
- Checks not actually run are marked unverified; security/architecture conclusions carry an evidence level.

## Expand on Demand
- Everyday tasks use only the quick rules, capability boundaries, and typical usage above; do not read the full gates by default.
- Read `references/full-workflow.md` only for deep architecture, complex multi-stage work, quality evaluation, release, formal delivery, or when the current task lacks evidence.
- After reading a reference, keep context to the minimum necessary; do not output long process write-ups or extra self-justifying material just because a reference exists.
