---
name: cloud-security
description: "Covers cloud security architecture: shared responsibility by service model (IaaS/PaaS/SaaS), CSPM/CWPP/CIEM/CNAPP/KSPM/DSPM defined precisely, IaC scanning, control plane vs data plane, and multi-cloud pitfalls. Use when the user asks about securing AWS, Azure or GCP, what a CNAPP or CSPM actually does, who is responsible for what in the cloud, cloud IAM as the perimeter, or Terraform/IaC misconfiguration scanning."
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Cloud Security Architecture

Two ideas drive every cloud design decision: **who is responsible for what** (shared responsibility), and **the control plane is the new perimeter** (the cloud API/IAM, not the network). Get those wrong and no tool saves you.

The tool-category definitions shift yearly: verify current definitions before citing. Good anchors: Wiz academy `https://www.wiz.io/academy`, Orca's acronym guide `https://orca.security/resources/blog/cwpp-cspm-ciem-cnapp/`, and the CSA `https://cloudsecurityalliance.org`.

## Shared responsibility: design by service model

The provider secures _of_ the cloud; you secure _in_ the cloud. The line moves with the service model: know exactly where yours sits.

- **IaaS** (VMs): you own OS, patching, runtime, network config, data, IAM. Most responsibility yours.
- **PaaS** (managed DB, app runtime): provider owns OS/runtime; you own config, identity, data, app code.
- **SaaS**: provider owns the stack; you own **identity, data, and configuration** (sharing settings, SSO, least privilege). The breach surface here is almost always _your config_, not their code.
- **Serverless / containers-as-a-service**: provider owns the host; you own function/image, IAM role, and dependencies.

The recurring failure mode: assuming the provider covers something on your side of the line. Misconfiguration (public bucket, over-permissive role, open security group) is your responsibility at every model and is the dominant cause of cloud breaches.

## Control plane vs data plane (the perimeter shift)

- **Control plane** = the cloud provider API/IAM/management: create, configure, delete resources, assume roles. **This is the new perimeter.** Owning an over-privileged IAM principal beats owning a server: an attacker reconfigures, exfiltrates, and pivots without touching a single host.
- **Data plane** = traffic to/from the running workload (the app serving requests).
- Defend the control plane first: phishing-resistant MFA on all human principals, no long-lived access keys, least-privilege roles, CloudTrail/audit-log everything, alert on privilege escalation and policy changes. CIEM (below) exists for exactly this.

## The acronym soup, defined precisely

Each category answers a different "what's wrong with my cloud" question. CNAPP is the platform that swallows several of them.

- **CSPM: Cloud Security Posture Management.** The oldest. Finds **misconfiguration of cloud-provider resources** (IaaS/PaaS objects: public S3, open SG, unencrypted volume, weak logging) against benchmarks (CIS, provider best practice). Config-plane, agentless. _Need it when:_ you have any cloud footprint: table stakes.
- **CWPP: Cloud Workload Protection Platform.** Protects **what runs inside** (VMs, containers, serverless, K8s pods): vuln scanning of workloads, runtime threat detection, behavioral baselining, host hardening. _Need it when:_ you run your own workloads (IaaS/containers), not pure SaaS.
- **CIEM: Cloud Infrastructure Entitlement Management.** Tackles the **IAM/entitlements** problem: human + machine identities accreting excessive permissions across accounts; right-sizing least privilege, finding privilege-escalation paths. _Need it when:_ multi-account, many roles, identity sprawl (i.e. any real org). This guards the control plane.
- **KSPM: Kubernetes Security Posture Management.** CSPM specialized for **Kubernetes**: cluster config, RBAC, network policies, pod security, admission control against benchmarks (CIS Kubernetes). _Need it when:_ you run K8s/EKS/GKE/AKS at scale.
- **DSPM: Data Security Posture Management.** Operates **at the data layer**: discover + classify sensitive data across cloud/SaaS/on-prem, map who can access it, flag exposure and compliance gaps. Newest major category; surged with AI/LLM data-flow concerns. _Need it when:_ you don't actually know where your sensitive data lives (most orgs).
- **CNAPP: Cloud-Native Application Protection Platform.** The **consolidation platform** (Gartner-coined) that unifies CSPM + CWPP + CIEM + IaC scanning (and increasingly KSPM/DSPM) into one tool that correlates findings across layers, e.g. "this public VM _and_ its over-privileged role _and_ a critical CVE = a real attack path," not three disconnected alerts. As of 2026 most enterprises are consolidating onto CNAPP rather than buying point tools. _Need it when:_ you have several point tools generating uncorrelated noise.

Mental model: CSPM=config, CWPP=workload, CIEM=identity, KSPM=k8s, DSPM=data, **CNAPP=all of it, correlated**. The value of CNAPP is the _correlation into attack paths_, not the feature checklist.

Adjacent (don't confuse): **SSPM** = SaaS posture (Salesforce/M365/Workday config); **ASPM** = application security posture (app-layer scanners: see `load_skill appsec-sdlc`).

## IaC scanning: shift the config left

- Scan **Terraform/CloudFormation/Bicep/Helm/K8s manifests** in CI _before_ deploy (tools: Checkov, tfsec/Trivy, KICS). Cheapest place to kill a misconfiguration: pre-provision, not post.
- IaC scanning + CSPM are complementary: IaC catches it in the PR, CSPM catches drift and click-ops changes in the running account. You need both: runtime always diverges from code.
- Enforce as a **policy-as-code gate** (OPA/Conftest, admission control) so a failing check blocks the merge/deploy, not just warns.

## Multi-cloud pitfalls

- **IAM models don't transfer.** AWS IAM ≠ Azure RBAC/Entra ≠ GCP IAM in semantics. "Least privilege" must be re-reasoned per cloud; a mental model from one _creates_ holes in another.
- **Inconsistent defaults / service parity**: encryption-at-rest, public-access-block, logging defaults differ per provider and per service. Don't assume.
- **Tooling lowest-common-denominator**: multi-cloud CNAPP coverage is uneven; depth per provider varies. Verify the tool actually covers your weakest cloud.
- **Identity federation sprawl**: federating one IdP into N clouds multiplies the blast radius of that IdP. The IdP becomes the crown jewel (`load_skill zero-trust`).
- **Don't go multi-cloud for security**: it multiplies the control surface and the expertise required. Multi-cloud is a business/resilience choice that _adds_ security cost, not a security win.
- **APAC sovereignty pitfall**: your global AWS/Azure/GCP tenant does **not** extend into China. The China regions are legally separate partitions run by a **local licensed operator** (AWS by Sinnet/NWCD, Azure by 21Vianet; GCP has no China region), with their own accounts, IAM, and no shared identity, plus ICP licensing and data-localization duties. Treat China (and other sovereign-cloud / data-localization regimes) as a distinct cloud with its own posture baseline, not just another region toggle.

## Where to enforce / cross-links

- Network containment in-cloud is **Security Groups** (per-instance) over NACLs (subnet): `load_skill network-segmentation`.
- Control-plane identity hardening is the cloud face of `load_skill zero-trust`.
- App-layer (code/deps/pipeline) is out of scope here: `load_skill appsec-sdlc`.
- Map cloud findings to controls with `load_skill control-mapping`; feed residual risk to `load_skill risk-assessment`.
- Container/K8s hardening: `load_skill container-kubernetes-security`; provider attestations (STAR/C5/FedRAMP): `load_skill cloud-assurance`.

## Rules

- Misconfiguration is yours at every service model: most cloud breaches are config, not provider CVEs.
- Defend the control plane (IAM) first; an over-privileged role beats a rooted box.
- IaC scan + CSPM both: code-time and runtime catch different failures.
- Buy CNAPP for the cross-layer attack-path correlation, not the acronym count; point tools only if the correlation isn't worth it yet.
