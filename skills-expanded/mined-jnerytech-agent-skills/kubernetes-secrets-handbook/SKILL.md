---
name: kubernetes-secrets-handbook
description: "Knowledge base from \"Kubernetes Secrets Handbook\" by Emmanouil Gkatziouras, Rom Adams & Chen Xi. Use when applying their frameworks for Kubernetes Secrets, etcd encryption at rest (KMS/DEK/KEK), RBAC and audit policy, Secrets Store CSI Driver, HashiCorp Vault and CyberArk Conjur, cloud secret stores (AWS/Azure/GCP), backups and disaster recovery, or CI/CD secret handling — studying the book, or referencing its concepts."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Kubernetes Secrets Handbook
**Authors**: Emmanouil Gkatziouras, Rom Adams, Chen Xi (Packt, 2024) | **Pages**: ~294 | **Chapters**: 14 | **Generated**: 2026-08-14

## How to Use This Skill

- **Without arguments** — load the core frameworks below for reference
- **With a topic** — ask about `envelope encryption`, `secret zero`, `CSI driver`, `Vault auth`, or another indexed topic; I find and read the relevant chapter
- **With a chapter** — ask for `ch07`; I load that specific chapter file
- **Browse** — ask "what chapters do you have?" for the full index

When you ask about a topic not covered below, I will read the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

### The premise: encoded is not encrypted
`Secret.data` values are **base64-encoded, not encrypted**, and land in etcd as plaintext. etcd itself "does not provide any encryption capabilities" except on the wire. Kubernetes ships a Secrets *framework*, not a vault — "By design, Kubernetes will not become a storage system or an encrypted Vault."

### The five exposures (Ch 1) — the threat model everything else answers
1. **kube-apiserver** — anyone who can `get secret` reads the value
2. **etcd API service** — API-driven; access or network trace exposes data
3. **etcd database file** — a plain binary file, `grep`-able
4. **Node filesystem** — the etcd volume is attached to a node
5. **Backups** — cluster backups contain the unencrypted etcd file

RBAC only closes #1. #3–#5 survive perfect RBAC — which is why encryption at rest (Ch 3) and backup security (Ch 6) are separate problems.
**Plus (Ch 7)**: Kubernetes has **no need-to-know distribution** — anyone with root on any node reads any Secret by impersonating the kubelet.

### Platform vs. Application Secrets — the split that decides what may be offloaded
- **Platform Secrets** (internal components, add-ons) → **keep in Kubernetes**. Offload them and a vault partition "will start collapsing" the cluster and all workloads.
- **Application Secrets** (database, S3, third-party APIs) → **offload candidates** for Vault/cloud stores.

Use `EncryptionConfiguration` for the former; use the CSI Driver + an external store for the latter. **Compose both** — "there is not one software to address all needs" (Ch 14).

### Envelope encryption and provider precedence (Ch 3)
`kube-apiserver` reads an ordered **provider list** (`identity` / `aescbc` / `aesgcm` / `kms`):
- **Writes** use the **first** provider. **Reads** are **header-driven** (provider + version + key stamped on the object).
- **Migration** = put the new provider first, keep the old one below, **then rewrite every Secret**. Removing the old provider early makes unrewritten Secrets permanently unreadable.

Prefer **`kms` + envelope encryption**: a **DEK** encrypts the payload (local, in-memory under KMSv2); a **KEK** encrypts the DEK (remote, on the KMS). Use **one KEK per cluster** — sharing one is a single point of failure. KMSv1 is deprecated in 1.28; KMSv2 GA in 1.29.
`aesgcm`/`aescbc` are the fast on-ramp but put the key base64 in a YAML file **on the control-plane disk** — a disk breach yields both key and ciphertext.

### Encryption at rest is one ring of an onion, not a checkbox
**Transport (TLS, internal too)** → **Linux hardening (SCAP/CIS/NIST, OpenSCAP)** → **Disk encryption (FDE/SED)** → **Filesystem encryption (dm-crypt / LUKS / NBDE)** → **Kubernetes native encryption**. Each ring stops a different attacker; none substitutes for another.

### The five named anti-patterns (Ch 7) — learn the names, the fix follows
| Anti-pattern | Tell | Fix |
|---|---|---|
| **Secret zero** | One master key unlocks everything | Key splitting, **Shamir's Secret Sharing** quorum, HSM, MFA |
| **Secret access ballooning** | An LDAP group of 10 became 400 | RBAC + **JIT access** + step-up auth + access-growth **metrics** |
| **Secret valet parking** | CI fetches all Secrets to the host FS | **Dynamic short-TTL Secrets** + *verified* deletion + per-workload fetch |
| **Secret sprawl** | Same credential in source, wiki, Dropbox | **Centralize** (Vault, CyberArk) |
| **Secret island** | Jenkins Secrets + AWS Secrets, no shared policy | Centralize **+ integrate via APIs**; else you get shadow IT |

Secret zero largely disappears under cloud IAM but **persists on-prem/private cloud**. Sprawl and islands are opposite failures of the same axis.

### Cyber risk over cybersecurity (Ch 5)
Start from **"what regulations must we comply with?"**, not from technology. IT-centric, incident-driven, lock-everything-down security produces disabled controls and shadow infrastructure. Risk management sizes controls to the asset and reports business value. Use **CIS Benchmarks** as the unifying layer across overlapping regulations (HIPAA, GDPR, PCI-DSS, NIS2…), then the published mappings as regulator-facing evidence.

**The five CIS rules for Secrets**: **1.2.29** (`--encryption-provider-config` set) · **1.2.30** (provider is `aescbc`/`aesgcm`/`kms`) · **3.2.2** (audit policy covers `Secret`, `ConfigMap`, `TokenReview`) · **5.4.1** (**prefer Secrets as files over environment variables**) · **5.4.2** (consider external secret storage).

### Workload identity — the credential-free bridge
The same pattern on all three clouds and in CI/CD: a Kubernetes ServiceAccount (or a CI job's OIDC token) is federated to a cloud identity, so **no static credential exists in the cluster or the pipeline**. The scoping field **is** the security control — AWS `Condition` on `<oidc>:sub`, Azure federated-credential `subject`, GCP SA annotation, GitHub `attribute.repository`. Omit it and any workload can assume the identity.

### Vault's inverted trust (Ch 11)
Rather than giving Kubernetes a Vault credential, **Vault asks Kubernetes to vouch for the Pod** via a `TokenReview` on the ServiceAccount JWT. Nothing Vault-specific is stored in etcd. The app's SA needs `system:auth-delegator` — provisioning the ServiceAccount alone is not sufficient.

### Seven qualities of any external secret store (Ch 11)
High availability · encryption of data (**and of the keys that encrypt it**) · secure access via policies · versioning · RBAC · Kubernetes integration with no sensitive keys in etcd · auditing.

### Two consumption paradigms, and the alignment rule (Ch 12)
**Convert to native Secrets** (caching, no external SPOF, sync burden) vs **direct fetch** (freshest, cleaner audit, latency + dependency).
**Alignment rule**: Pod-lifecycle mechanisms (init container, sidecar, CSI) → **direct fetch**. API extensions (webhook, CRD, custom API server) → **conversion**.

### Debug top-down, and hash — never print (Ch 4)
Secret bugs surface as a *dependent component* failing. Start at the app, follow logs to the controller, then the Secret. Verify values by **MD5-comparing inside a throwaway Pod** — printing a Secret ships it to CloudWatch/Datadog/Cloud Monitoring and forces rotation. Only `dockercfg` Secrets are content-validated; invalid TLS and basic-auth Secrets apply cleanly and fail later.

### Secrets are tier-0, and the backup is a copy of everything (Ch 6)
Some Secrets **cannot be regenerated** (vendor-issued, hardware-bound, time-bound). Encrypt backups with rotatable keys, restrict access, make storage immutable (S3 Object Lock / WORM), and **run gamedays** covering cluster loss, store loss, **and backup-system loss**. A robust backup strategy with unencrypted backups is worse than none.

### Lifecycle, not storage (Ch 13)
**Provision → store → distribute → rotate → decommission → revoke.** Decommissioning must be wired into service-retirement workflows. In CI/CD: masking is a speed bump (write to a file, print the file), job logs persist, and **never share Secrets between test and production**.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-understanding-secrets-management.md) | Understanding Kubernetes Secrets Management | Five security exposures, Platform vs Application Secrets, base64≠encryption |
| [ch02](chapters/ch02-secrets-management-concepts.md) | Walking through Secrets Management Concepts | Secret types, `stringData` vs `data`, RBAC four-object model, audit policy |
| [ch03](chapters/ch03-encrypting-secrets-native.md) | Encrypting Secrets the Kubernetes-Native Way | Provider list precedence, envelope encryption (DEK/KEK), etcd onion layers, LUKS/NBDE |
| [ch04](chapters/ch04-debugging-troubleshooting.md) | Debugging and Troubleshooting Secrets | Five-step evaluation checklist, isolate-the-Secret, hash-don't-print, double-base64 trap |
| [ch05](chapters/ch05-security-auditing-compliance.md) | Security, Auditing, and Compliance | Cyber risk vs cybersecurity, five CIS rules, DevSecOps insertion points, Trivy/kube-bench/StackRox |
| [ch06](chapters/ch06-disaster-recovery-backups.md) | Disaster Recovery and Backups | Tier-0 framing, three backup strategies, versioning strategy, DRP elements, six backup security guidelines |
| [ch07](chapters/ch07-challenges-and-risks.md) | Challenges and Risks in Managing Secrets | Secret zero, ballooning, valet parking, sprawl, islands; five-phase maturity model; kubelet impersonation |
| [ch08](chapters/ch08-cloud-secret-store-aws.md) | Exploring Cloud Secret Store on AWS | Two-lever cloud pattern, IRSA, Secrets Store CSI Driver architecture, Terraform lifecycle |
| [ch09](chapters/ch09-cloud-secret-store-azure.md) | Exploring Cloud Secret Store on Azure | Workload Identity + federated credential, Azure RBAC over access policies, Diagnostic settings |
| [ch10](chapters/ch10-cloud-secret-store-gcp.md) | Exploring Cloud Secret Store on GCP | Three-tier IAM scope, GKE Workload Identity, `container-engine-robot` gotcha, CMK etcd encryption |
| [ch11](chapters/ch11-external-secret-stores.md) | Exploring External Secret Stores | Seven qualities, Vault Kubernetes auth flow, seal/unseal + Shamir, Raft `(n-1)/2`, Conjur |
| [ch12](chapters/ch12-integrating-with-secret-stores.md) | Integrating with Secret Stores | Two consumption paradigms, eight integration mechanisms, SealedSecrets, brokers, service mesh |
| [ch13](chapters/ch13-case-studies-real-world.md) | Case Studies and Real-World Examples | Four production qualities, five CI/CD risks, OIDC federation, rotation mechanics, Keywhiz case study |
| [ch14](chapters/ch14-conclusion-and-future.md) | Conclusion and the Future | KEP-3299/KMSv2 roadmap, five requested enhancements, how to file an issue, five DevSecOps principles |

## Topic Index

- **Admission controllers / mutating webhooks** → ch11, ch12
- **aesgcm / aescbc** → ch03, ch07
- **Argo CD / GitOps** → ch02, ch13
- **Audit policy (Kubernetes)** → ch02, ch05, ch07
- **AWS Secrets Manager / KMS / CloudTrail** → ch08, ch06
- **Azure Key Vault** → ch09, ch06
- **Backups & disaster recovery** → ch06, ch13
- **base64 encoding** → ch01, ch02, ch04
- **Broker / secretless broker** → ch12
- **CI/CD secret risks** → ch13
- **CIS Benchmarks** → ch05
- **ConfigMap** → ch01, ch03
- **CRDs / custom controllers** → ch12
- **CSI Driver (Secrets Store)** → ch08, ch09, ch10, ch11, ch12, ch14
- **CyberArk Conjur** → ch11
- **DEK / KEK / envelope encryption** → ch03, ch08
- **DevSecOps** → ch05, ch14
- **Disk & filesystem encryption (LUKS, dm-crypt, NBDE)** → ch03, ch14
- **`EncryptionConfiguration`** → ch03, ch07, ch14
- **etcd** → ch01, ch03, ch06, ch13
- **GCP Secret Manager / Cloud KMS** → ch10, ch13
- **Helm Secrets / SOPS** → ch02, ch04, ch13
- **Immutable Secrets** → ch02
- **Init containers / sidecars / DaemonSets** → ch11, ch12
- **IRSA (AWS workload identity)** → ch08
- **KEP-3299 / KMSv1 vs KMSv2** → ch03, ch14
- **Keywhiz (Square)** → ch13
- **kube-bench / Compliance Operator / StackRox / Trivy** → ch05
- **kubelet impersonation / root exploit** → ch07
- **Platform vs Application Secrets** → ch01, ch14
- **RBAC (Role, ClusterRole, bindings)** → ch02, ch07, ch13
- **Rotation** → ch06, ch07, ch08, ch13
- **SealedSecrets / kubeseal** → ch12, ch13
- **Secret types (Opaque, TLS, dockercfg, SA token)** → ch02, ch04, ch13
- **Secret zero / ballooning / valet parking / sprawl / islands** → ch07
- **Service mesh / Istio / Citadel / mTLS** → ch12
- **Shamir's Secret Sharing** → ch07, ch11
- **`stringData` vs `data`** → ch02, ch04
- **Terraform** → ch08, ch09, ch10
- **tmpfs** → ch12, ch13
- **Vault (HashiCorp)** → ch03, ch06, ch11, ch12, ch13, ch14
- **Vault Agent Injector** → ch11
- **Velero / etcdctl** → ch06
- **Workload Identity (Azure/GCP) & Federation** → ch09, ch10, ch13

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions and chapter references
- [patterns.md](patterns.md) — techniques, integration patterns, and named anti-patterns with fixes
- [cheatsheet.md](cheatsheet.md) — decision rules, thresholds, provider comparison, tells and smells

---

## Scope & Limits

This skill covers the book's content (Kubernetes ~1.28 era, 2024). Version-specific facts — KMSv2 GA in 1.29, KMSv1 deprecation in 1.28, CSI provider support matrices, cloud console URLs — should be re-verified against current documentation before acting. For hands-on work in your own cluster, combine with project-specific tooling and the live Kubernetes docs.
