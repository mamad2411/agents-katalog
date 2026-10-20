---
name: vault-operations-and-pki-engine-configuration
description: >
  Guides operating a HashiCorp Vault cluster itself — initialization,
  unsealing (Shamir key shares or auto-unseal via cloud KMS/HSM),
  configuring the PKI secrets engine for internal certificate issuance
  (root/intermediate CA hierarchy, roles, short-lived leaf certs), and
  HA/DR cluster topology (Raft integrated storage, performance/DR
  replication). Use when the user asks to "unseal Vault", "set up
  auto-unseal", "configure Vault's PKI engine to issue internal certs",
  "stand up a Vault HA cluster", "design Vault DR replication", or
  "rotate a Vault root/intermediate CA". Distinct from consuming Vault
  as a secrets backend (see secrets-management and
  sealed-secrets-and-external-secrets-operator) — this skill is about
  operating Vault itself as infrastructure.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: security-scanning-tooling
  maturity: stable
---

# Vault Operations and PKI Engine Configuration

## Purpose

HashiCorp Vault is itself a piece of critical infrastructure that has to
be initialized, kept unsealed, made highly available, and operated with
its own upgrade and disaster-recovery discipline — separate from the
question of how applications *consume* secrets from it, which is
covered in [secrets-management](../../../devsecops/skills/secrets-management/SKILL.md)
and, for the Kubernetes-native sync pattern, in
[sealed-secrets-and-external-secrets-operator](../sealed-secrets-and-external-secrets-operator/SKILL.md).
This skill covers running Vault as the platform team operating it:
initialization and the seal/unseal lifecycle (Shamir key shares versus
auto-unseal against a cloud KMS or HSM), configuring the **PKI secrets
engine** to stand up an internal certificate authority hierarchy and
issue short-lived leaf certificates for internal mTLS, and designing
HA/DR topology with Raft integrated storage and cross-cluster
replication. Getting this operational layer wrong doesn't just cause an
outage for one team's secret lookups — since Vault is frequently the
root of trust for both secrets and internal PKI, a mishandled unseal
key, an un-replicated cluster, or a compromised root CA can cascade
across every system that depends on it.

## When to use

- Initializing a new Vault cluster and choosing between Shamir
  key-share unsealing and auto-unseal (AWS KMS, Azure Key Vault, GCP
  Cloud KMS, or an HSM via PKCS#11/Vault Enterprise).
- Setting up the **PKI secrets engine** to issue internal TLS
  certificates — a root CA, an intermediate CA, roles constraining what
  an application can request, and short-lived leaf certificate issuance
  for internal service-to-service mTLS.
- Designing or reviewing a Vault HA cluster's storage backend (Raft
  integrated storage vs. Consul) and its Performance/DR replication
  topology across regions or environments (Vault Enterprise feature).
- Rotating a Vault root or intermediate CA, or responding to a
  suspected compromise of Vault's own unseal material or CA private
  key.
- Recovering a Vault cluster after a restart when auto-unseal isn't
  configured and the cluster is sitting sealed.
- Planning a Vault version upgrade, including any storage-backend
  migration or seal-migration (Shamir → auto-unseal) steps.

## Prerequisites & environment

- Vault ≥ 1.15 recommended for stable Raft integrated-storage
  autopilot features (automated dead-server cleanup, state
  snapshots); PKI engine role/issuer behavior referenced below assumes
  the `pki` secrets engine's modern multi-issuer support (Vault ≥ 1.11),
  not the older single-CA-per-mount model.
- A storage backend decision made deliberately: **Raft integrated
  storage** (the current recommended default — no external dependency,
  built-in HA) versus **Consul** (viable if the org already operates
  Consul for other reasons, adds an external dependency Vault itself
  doesn't otherwise need).
- For auto-unseal: a cloud KMS key (AWS KMS, Azure Key Vault, GCP Cloud
  KMS) or HSM the Vault servers have network access and IAM permission
  to call, provisioned *before* initializing Vault against it.
- Vault Enterprise license if Performance Replication or DR Replication
  across clusters is required — the OSS edition supports Raft-based HA
  within one cluster but not cross-cluster replication.
- An odd number of Raft voter nodes (3 or 5) across separate failure
  domains (availability zones at minimum) for real HA — a single-node
  or even-numbered cluster does not tolerate a node failure safely.
- A secure, access-controlled process for storing Shamir unseal key
  shares (if not using auto-unseal) — distributed to separate
  key-holders, never all stored together, and never committed anywhere
  near source control.
- `vault` CLI matching the server version, and network/firewall access
  to the cluster's API port (default `8200`) and cluster port (`8201`).

## Step-by-step guidance

### Initialization, seal, and unseal

1. **Initialize the cluster once, capturing the recovery/unseal
   material immediately and securely**:
   ```bash
   vault operator init -key-shares=5 -key-threshold=3
   ```
   This returns 5 Shamir key shares (any 3 reconstruct the master key)
   and an initial root token. Distribute each share to a different
   named individual immediately — never store all shares together, and
   never leave them only in the terminal scrollback of the machine that
   ran `init`.

2. **Prefer auto-unseal over Shamir shares for any production cluster**
   — a cloud KMS or HSM unseals Vault automatically on restart without
   requiring key-holders to be paged and to type in shares manually:
   ```hcl
   # vault config: auto-unseal via AWS KMS
   seal "awskms" {
     region     = "us-east-1"
     kms_key_id = "<KMS_KEY_ID>"
   }
   ```
   With auto-unseal configured, `vault operator init` still returns
   **recovery keys** (used for `vault operator generate-root` and
   emergency operations) rather than Shamir unseal shares — these still
   need the same careful, distributed storage discipline as Shamir
   shares would.

3. **If using Shamir (no auto-unseal), unseal each server after every
   restart** with the threshold number of distinct key-holders each
   supplying their share:
   ```bash
   vault operator unseal <key-share-1>
   vault operator unseal <key-share-2>
   vault operator unseal <key-share-3>
   ```
   Every server in the cluster must be individually unsealed after a
   restart under Shamir — this operational burden, multiplied across
   every node and every restart, is the main practical reason to prefer
   auto-unseal in production.

4. **Verify cluster health and Raft peer status** after any restart or
   topology change:
   ```bash
   vault operator raft list-peers
   vault status
   ```
   Confirm the expected number of voters is present and one node holds
   `leader` status before considering a restart/failover complete.

### PKI secrets engine

5. **Enable and configure a root CA**, ideally offline/rarely-used, with
   a long validity, and an **intermediate CA** that actually signs leaf
   certificates day to day — never issue leaf certificates directly
   from the root:
   ```bash
   vault secrets enable -path=pki_root pki
   vault secrets tune -max-lease-ttl=87600h pki_root   # 10 years

   vault write -field=certificate pki_root/root/generate/internal \
     common_name="Example Internal Root CA" \
     ttl=87600h > root_ca.crt
   ```

6. **Generate an intermediate CA and get it signed by the root**:
   ```bash
   vault secrets enable -path=pki_int pki
   vault secrets tune -max-lease-ttl=43800h pki_int   # 5 years

   vault write -field=csr pki_int/intermediate/generate/internal \
     common_name="Example Internal Intermediate CA" > pki_intermediate.csr

   vault write -field=certificate pki_root/root/sign-intermediate \
     csr=@pki_intermediate.csr format=pem_bundle ttl=43800h \
     > intermediate.cert.pem

   vault write pki_int/intermediate/set-signed \
     certificate=@intermediate.cert.pem
   ```

7. **Define a role constraining what a given application can request**
   — allowed domains, max leaf TTL, key type — rather than a role that
   can issue a certificate for any name:
   ```bash
   vault write pki_int/roles/payments-svc \
     allowed_domains="payments.svc.internal" \
     allow_subdomains=true \
     max_ttl="72h" \
     key_type="rsa" key_bits=2048
   ```
   Short max TTLs (hours to a few days, not months) are the point of
   running an internal PKI engine — a leaf cert that expires in 72
   hours and is re-issued automatically by the workload has a small
   blast radius if ever exfiltrated, unlike a long-lived cert that
   would need explicit revocation.

8. **Issue a leaf certificate**, either via direct API call from a
   workload's Vault-authenticated identity, or via the Vault Agent /
   the PKI issuance pattern most Vault client libraries support:
   ```bash
   vault write pki_int/issue/payments-svc \
     common_name="payments.svc.internal" ttl="24h"
   ```
   Automate renewal (a sidecar or Vault Agent template re-requesting
   before the short TTL expires) rather than treating internal PKI
   issuance as a one-time manual step — this only works operationally
   at scale with automation, which is the focus of
   [certificate-lifecycle-management-at-scale](../certificate-lifecycle-management-at-scale/SKILL.md).

9. **Configure CRL/OCSP distribution** so revocation is actually
   enforceable, not just theoretically possible:
   ```bash
   vault write pki_int/config/urls \
     issuing_certificates="https://vault.example.internal:8200/v1/pki_int/ca" \
     crl_distribution_points="https://vault.example.internal:8200/v1/pki_int/crl"
   ```

### HA/DR topology

10. **Run Raft integrated storage across an odd number of voter nodes
    (3 or 5) spread across separate availability zones**:
    ```hcl
    storage "raft" {
      path    = "/vault/data"
      node_id = "vault-1"
    }
    cluster_addr = "https://vault-1.internal:8201"
    api_addr     = "https://vault-1.internal:8200"
    ```
    A 2-node or single-node "HA" setup provides no real quorum
    tolerance — a single node failure either has no failover (1 node)
    or creates a split-brain risk (2 nodes, no majority possible).

11. **Take regular Raft snapshots** as the backup mechanism, independent
    of any replication setup:
    ```bash
    vault operator raft snapshot save vault-snapshot-$(date +%Y%m%d).snap
    ```
    Store snapshots in a separate, access-controlled location (not on
    the same storage volume as the live cluster) and test restoring
    from one periodically — an untested backup is not a real recovery
    plan.

12. **For cross-region/cross-environment DR, use Vault Enterprise's DR
    Replication** (a passive, promotable secondary cluster) rather than
    relying on Raft snapshots alone for a full-region-loss scenario —
    snapshots give point-in-time recovery; DR replication gives a
    warm-standby cluster that can be promoted with minimal data loss.
    Performance Replication (also Enterprise) is a separate feature for
    reducing latency to geographically distributed clients, not a
    substitute for DR replication's failover purpose.

## Best practices

- Prefer auto-unseal (cloud KMS/HSM) over Shamir shares for any
  production cluster — the operational cost of manually unsealing every
  node after every restart, and the risk of losing enough distributed
  key shares to reconstitute the threshold, both go away with
  auto-unseal.
- Never issue leaf certificates directly from a root CA — always
  interpose an intermediate, and keep the root's private key material
  as offline/inaccessible as operationally feasible, brought online
  only for intermediate signing or rotation events.
- Keep leaf certificate TTLs short (hours to low days) and automate
  renewal — the security value of an internal PKI engine largely comes
  from short-lived certs, not from centralizing issuance alone.
- Scope PKI roles tightly (`allowed_domains`, `max_ttl`, key
  constraints) per application/service, not one broad role usable to
  request a certificate for any name.
- Run an odd number (3 or 5) of Raft voter nodes across separate
  failure domains, and validate quorum/peer status after any
  maintenance — an even-numbered or single-node deployment isn't really
  HA.
- Take and periodically test-restore Raft snapshots regardless of
  whether replication is also configured — replication protects against
  a cluster/region failure; snapshots protect against data corruption or
  operator error replication wouldn't catch (a bad write replicates
  everywhere just as fast as a good one).
- Store unseal/recovery key shares and root CA material with the same
  rigor as any other top-tier secret — distributed among named
  individuals, access-logged, and included in the organization's own
  incident-response plan for what happens if a share/holder is
  compromised.

## Common pitfalls

- **Symptom:** A Vault cluster restarts (node reboot, upgrade, incident)
  and comes back up `sealed`, and no on-call runbook exists for who
  holds the unseal shares.
  **Fix:** This is the exact failure mode auto-unseal exists to
  eliminate — migrate to cloud KMS/HSM-based auto-unseal for production
  clusters. If Shamir must be retained (e.g. a hard compliance
  requirement against auto-unseal), maintain a tested, on-call-visible
  runbook naming which individuals hold shares and how to reach them
  under incident pressure.

- **Symptom:** A "highly available" Vault cluster is actually 2 nodes,
  and a single node failure leaves the surviving node unable to reach
  Raft quorum, taking the whole cluster down.
  **Fix:** Run 3 or 5 voter nodes, never an even number — Raft quorum
  requires a strict majority, and a 2-node cluster has no way to
  achieve one if either node is unreachable.

- **Symptom:** Leaf certificates are issued from the PKI engine with a
  90-day or longer TTL "to reduce operational overhead," defeating much
  of the point of running an internal CA over just using long-lived
  static certificates.
  **Fix:** Set short max TTLs (hours to a few days) at the role level
  and invest in renewal automation (Vault Agent templating, a sidecar,
  or application-level renewal logic) instead — the operational cost of
  automating short-lived renewal is paid once; the security benefit
  compounds on every subsequent issuance.

- **Symptom:** A root CA's private key is routinely used to sign leaf
  certificates directly because setting up an intermediate "felt like
  extra steps," and a compromised application role now has a path back
  toward root-level trust.
  **Fix:** Always interpose an intermediate CA; keep the root
  accessible only for the rare intermediate-signing or rotation
  operation, ideally requiring a distinct, more tightly controlled
  access path than day-to-day PKI operations use.

- **Symptom:** Vault snapshots are taken but have never been restored
  in a drill, and during an actual incident the restore procedure turns
  out to be broken (wrong storage path, missing unseal material for the
  restored cluster).
  **Fix:** Schedule periodic restore drills against a non-production
  cluster as a standing operational practice — an untested backup
  procedure carries the same risk as no backup at all, just with false
  confidence attached.

## Worked example

**Scenario:** Stand up a new production Vault cluster on Raft integrated
storage with AWS KMS auto-unseal, then configure a two-tier internal PKI
hierarchy issuing short-lived mTLS certificates for a `payments-svc`
workload.

Server config (`vault-1.internal`, repeated per node with a unique
`node_id`):
```hcl
storage "raft" {
  path    = "/vault/data"
  node_id = "vault-1"
}
listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_cert_file = "/etc/vault/tls/vault.crt"
  tls_key_file  = "/etc/vault/tls/vault.key"
}
seal "awskms" {
  region     = "us-east-1"
  kms_key_id = "<KMS_KEY_ID>"
}
cluster_addr = "https://vault-1.internal:8201"
api_addr     = "https://vault-1.internal:8200"
```

Initialize (auto-unseal means this returns recovery keys, not Shamir
shares needed on every restart):
```bash
vault operator init -recovery-shares=5 -recovery-threshold=3
vault status   # confirm Sealed: false — auto-unseal engaged immediately
vault operator raft list-peers   # confirm 3 voters, one leader
```

PKI hierarchy:
```bash
vault secrets enable -path=pki_root pki
vault secrets tune -max-lease-ttl=87600h pki_root
vault write -field=certificate pki_root/root/generate/internal \
  common_name="Example Internal Root CA" ttl=87600h > root_ca.crt

vault secrets enable -path=pki_int pki
vault secrets tune -max-lease-ttl=43800h pki_int
vault write -field=csr pki_int/intermediate/generate/internal \
  common_name="Example Internal Intermediate CA" > pki_intermediate.csr
vault write -field=certificate pki_root/root/sign-intermediate \
  csr=@pki_intermediate.csr format=pem_bundle ttl=43800h > intermediate.cert.pem
vault write pki_int/intermediate/set-signed certificate=@intermediate.cert.pem

vault write pki_int/roles/payments-svc \
  allowed_domains="payments.svc.internal" \
  allow_subdomains=true max_ttl="72h" key_type="rsa" key_bits=2048
```

Leaf issuance (24h TTL, renewed automatically by a Vault Agent template
well before expiry):
```bash
vault write pki_int/issue/payments-svc \
  common_name="payments.svc.internal" ttl="24h"
```

Result: `payments-svc` receives a fresh leaf certificate at least daily
via automated renewal, signed by an intermediate that is itself signed
by an offline-most-of-the-time root, on a 3-node Raft cluster that
auto-unseals via AWS KMS on any restart with no manual key-share
handling required.

## Cross-references

- [vault-configuration-validation](../vault-configuration-validation/SKILL.md) —
  validating Vault policies, auth methods, and seal configuration before
  rolling out changes to the operational cluster this skill sets up.
- [secrets-management](../../../devsecops/skills/secrets-management/SKILL.md) —
  the application-facing side of using Vault as a secrets backend
  (KV engines, dynamic database secrets, rotation policy), which
  assumes the operational cluster this skill covers is already running.
- [sealed-secrets-and-external-secrets-operator](../sealed-secrets-and-external-secrets-operator/SKILL.md) —
  syncing secrets *from* an operating Vault cluster into Kubernetes
  `Secret` objects via External Secrets Operator.
- [certificate-lifecycle-management-at-scale](../certificate-lifecycle-management-at-scale/SKILL.md) —
  rotating and automating certificates issued by this PKI engine (or an
  enterprise CA) across many services beyond a single Kubernetes
  cluster's scope.
- [cert-manager-tls-automation](../../../kubernetes-platform/skills/cert-manager-tls-automation/SKILL.md) —
  cert-manager can itself be configured to request certificates from
  Vault's PKI engine as an `Issuer` backend for Kubernetes-native
  automated issuance.
