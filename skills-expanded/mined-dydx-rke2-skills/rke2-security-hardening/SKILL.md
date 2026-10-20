---
name: rke2-security-hardening
description: Use for questions about hardening self-hosted RKE2 clusters - the CIS benchmark profile (profile:cis), pod security standards/admission (PSA), secrets encryption at rest and key rotation, SELinux, certificate management and rotation, cluster join tokens, and FIPS 140 compliance.
---

# RKE2 Security & Hardening

RKE2 is "hardened by default" and passes most Kubernetes CIS Benchmark controls out of the box. Full compliance requires (1) host-level changes RKE2 will not make for you, and (2) opting in to CIS mode via the `profile` flag. Per-version CIS self-assessment guides (control-by-control checklists) are maintained upstream at https://docs.rke2.io (Security > CIS Self-Assessment Guide; v1.12 covers RKE2 v1.33+, v1.11 covers v1.29-v1.32, etc.).

Note on PSPs: PodSecurityPolicies were removed from Kubernetes in v1.25. On RKE2 v1.24 and older, CIS mode used PSPs (`global-restricted-psp` etc., controlled by `psp.rke2.io/*` annotations on kube-system). On v1.25+ the replacement is Pod Security Admission (PSA), covered below. Migrate any PSP-based hardening to PSA config.

## CIS Hardening (`profile: cis`)

Config lives in `/etc/rancher/rke2/config.yaml` (create the directory before installing RKE2; set the profile before first start, or stop RKE2 first):

```yaml
# /etc/rancher/rke2/config.yaml  (RKE2 v1.25+)
profile: "cis"
# For CIS benchmark 1.11 only (not needed for 1.9/1.10):
kube-apiserver-arg:
  - 'service-account-extend-token-expiration=false'
```

Older versions use versioned profile values: `cis-1.23` (v1.23-v1.26), `cis-1.6` (v1.19-v1.22). The generic `cis` value (v1.25+) automatically tracks whichever CIS benchmark applies to the running Kubernetes version, so upgrades need no config change.

When `profile` is set, RKE2:

1. **Validates host-level requirements** at startup and exits with a fatal error if unmet (etcd user, kernel parameters).
2. **Runs etcd as the `etcd` user/group** - creates the etcd data dir owned `etcd:etcd` and sets the etcd static pod's SecurityContext (CIS control 1.1.12).
3. **Applies NetworkPolicies** to the built-in namespaces (`kube-system`, `kube-public`, `default`).
4. **Applies restrictive file permissions** (600 instead of 644) to agent manifests and config files.
5. **Enforces restricted Pod Security Admission** cluster-wide (exempting `kube-system`, `compliance-operator-system`, `tigera-operator`).
6. **Sets `protect-kernel-defaults: true`** on the kubelet (kubelet exits if kernel params deviate from its defaults; RKE2 pre-checks the same params and errors early). Setting `profile` while explicitly setting `protect-kernel-defaults: false` is a fatal error.
7. **Configures hardened `--audit-log-*` API server args** and creates a default audit policy at `/etc/rancher/rke2/audit-policy.yaml` (default rule is `level: None` - see below).

### Host requirement 1: etcd user

The etcd user/group must exist on every server node before starting RKE2 in CIS mode (must be in `/etc/passwd`/`/etc/group` - NSS/systemd-userdb sources are not supported):

```bash
sudo useradd -r -c "etcd user" -s /sbin/nologin -M etcd -U
```

### Host requirement 2: kernel parameters (rke2-cis-sysctl.conf)

RKE2 ships a sysctl config but does not activate it. Apply it manually on fresh installs, before first cluster start (restarting systemd-sysctl on a live cluster can break CNI-managed sysctls):

```bash
# RPM/YUM/DNF install (CentOS/RHEL/SLES):
sudo cp -f /usr/share/rke2/rke2-cis-sysctl.conf /etc/sysctl.d/60-rke2-cis.conf
sudo systemctl restart systemd-sysctl

# Tarball install (Ubuntu etc.):
sudo cp -f /usr/local/share/rke2/rke2-cis-sysctl.conf /etc/sysctl.d/60-rke2-cis.conf
sudo systemctl restart systemd-sysctl

# No systemd-sysctl / /etc/sysctl.d? Apply at boot:
sudo sysctl -p /usr/local/share/rke2/rke2-cis-sysctl.conf
```

### Remaining operator work (not automated)

- **`default` ServiceAccounts** (CIS 5.1.5): set `automountServiceAccountToken: false` on the `default` ServiceAccount in every namespace. RKE2 handles `kube-system`, `kube-node-lease`, `compliance-operator-system`, and `tigera-operator`; you must patch the rest:

  ```bash
  for ns in $(kubectl get ns -o jsonpath="{.items[*].metadata.name}"); do
    kubectl patch serviceaccount default -n "$ns" \
      -p '{"automountServiceAccountToken": false}'
  done
  ```

- **Audit policy**: the default `/etc/rancher/rke2/audit-policy.yaml` logs nothing (`rules: [{level: None}]`). Edit it (e.g. `level: Metadata`) and `sudo systemctl restart rke2-server.service`. Logs go to `/var/lib/rancher/rke2/server/logs/audit.log`.
- **NetworkPolicies for your own namespaces**: CIS-mode policies cover only built-in namespaces; you manage policies for namespaces you create.

### CIS-mode NetworkPolicies

RKE2 applies `default-network-policy` (allow ingress only from pods in the same namespace) to `kube-system`, `kube-public`, and `default`, plus `default-network-dns-policy` (allow ingress to port 53 TCP/UDP) in `kube-system`. Exceptions preserved: DNS resolution, HTTP/S to the bundled ingress controller (incl. its admission webhook), HTTPS to metrics-server, HTTPS to the rke2-snapshot-validation-webhook. Policies are tracked via `np.rke2.io` / `np.rke2.io/dns` namespace annotations: if the annotation exists RKE2 leaves your changes alone; delete the annotation and restart RKE2 to reset a policy. Inspect with `kubectl get networkpolicies -A`.

## Pod Security Admission (v1.25+)

RKE2 writes a PSA AdmissionConfiguration to `/etc/rancher/rke2/rke2-pss.yaml` at startup and passes it to kube-apiserver via `--admission-control-config-file`.

**With `profile: cis`** - `restricted` enforced everywhere except exempted system namespaces:

```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: AdmissionConfiguration
plugins:
- name: PodSecurity
  configuration:
    apiVersion: pod-security.admission.config.k8s.io/v1beta1
    kind: PodSecurityConfiguration
    defaults:
      enforce: "restricted"
      enforce-version: "latest"
      audit: "restricted"
      audit-version: "latest"
      warn: "restricted"
      warn-version: "latest"
    exemptions:
      usernames: []
      runtimeClasses: []
      namespaces: [kube-system, compliance-operator-system, tigera-operator]
```

**Without a profile** - `enforce: "privileged"` everywhere (fully unrestricted defaults; per-namespace `pod-security.kubernetes.io/*` labels still work).

**To customize**: write your own PSA config file (e.g. change exemptions, use `baseline`, add exempt usernames) and point RKE2 at it:

```yaml
# /etc/rancher/rke2/config.yaml
pod-security-admission-config-file: /etc/rancher/rke2/custom-psa.yaml
```

## Secrets Encryption at Rest

RKE2 encrypts Kubernetes Secrets at rest by default: it generates an AES-CBC key, writes an EncryptionConfiguration to `/var/lib/rancher/rke2/server/cred/encryption-config.json`, and passes it to the API server as `--encryption-provider-config`. Provider order: `aescbc` first, then `identity`.

**Provider choice** (April 2025 releases onward: v1.30.12+rke2r1, v1.31.8+rke2r1, v1.32.4+rke2r1, v1.33.0+rke2r1): `--secrets-encryption-provider` selects `aescbc` (default) or `secretbox` (XSalsa20/Poly1305). FIPS 140-2 compliance requires `aescbc`. To migrate to `secretbox`: set `secrets-encryption-provider: secretbox` in config.yaml on all servers, sequentially `systemctl restart rke2-server.service`, then rotate keys as below.

### `rke2 secrets-encrypt` subcommands

| Subcommand | Purpose |
| --- | --- |
| `status` | Show encryption state, rotation stage, per-server hash agreement, key table |
| `rotate-keys` | One-shot rotation (modern procedure, Sept 2024 releases onward) |
| `prepare` | Classic stage 1: add new key |
| `rotate` | Classic stage 2: make new key active |
| `reencrypt` | Classic stage 3: rewrite all secrets with active key |

Take an etcd snapshot before rotating - improper rotation can cause permanent data loss.

### Key rotation - modern (v1.29.9+rke2r1 / v1.30.5+rke2r1 / v1.31.1+rke2r1 and newer)

Single server:

```bash
rke2 secrets-encrypt rotate-keys
rke2 secrets-encrypt status   # wait for: Current Rotation Stage: reencrypt_finished
```

HA (servers S1, S2, S3 - run commands from one server):

```bash
# On S1:
rke2 secrets-encrypt rotate-keys
rke2 secrets-encrypt status                 # wait for reencrypt_finished
# Then sequentially on S1, S2, S3 (wait for each to return):
systemctl restart rke2-server.service
```

### Key rotation - classic (older releases)

HA procedure: `prepare` on S1 -> sequentially restart S1,S2,S3 -> `rotate` on S1 -> sequentially restart all -> `reencrypt` on S1 -> wait for `reencrypt_finished` (`rke2 secrets-encrypt status` or `journalctl -u rke2-server`) -> sequentially restart all. On a single server, restart the kube-apiserver static pod between steps instead (`crictl ps --name kube-apiserver; crictl stop <ID>` with `CONTAINER_RUNTIME_ENDPOINT=unix:///var/run/k3s/containerd/containerd.sock`).

`status` fields: rotation stages are `start`, `prepare`, `rotate`, `reencrypt_request`, `reencrypt_active`, `reencrypt_finished`; "Server Encryption Hashes" tells you whether all HA servers share the same encryption config (mismatched hashes = restart servers before proceeding). The `*` in the key table marks the active key used to encrypt new secrets.

## SELinux

RKE2 supports SELinux-enforcing hosts (default on CentOS/RHEL 7+). The policy is the `rke2-selinux` RPM (https://github.com/rancher/rke2-selinux), a specialization of `container-selinux` for RKE2's non-standard containerd paths. It adds two context labels for control-plane static pods, avoiding over-privileged `spc_t`: `rke2_service_db_t` (read-write, e.g. etcd under `/var/lib/rancher/rke2/server/db`) and `rke2_service_t` (read-only, e.g. `/var/lib/rancher/rke2/server/tls`).

Enablement is a single boolean - config.yaml `selinux: true`, the `--selinux` flag, or `RKE2_SELINUX=true` - passed through to containerd's CRI `enable_selinux`:

```yaml
# /etc/rancher/rke2/config.yaml
selinux: true
```

- RPM installs enable SELinux support by default; tarball installs require the flag/env var explicitly.
- If AVC denials appear despite rke2-selinux + container-selinux being installed, reboot the node (sometimes required after policy install, before starting rke2).
- Amazon Linux 2 needs extra packages: `sudo amazon-linux-extras enable selinux-ng; sudo yum install selinux-policy-targeted -y`.
- Calico CNI with SELinux requires Tigera's additional `calico-selinux` policy RPM.

## Certificate Management

**Leaf (client/server) certs**: valid 365 days from issuance. On every RKE2 start, any cert expired or within 120 days of expiry is automatically renewed (same keys, extended lifetime). A Kubernetes Warning event `CertificateExpirationWarning` fires at 120 days out. (Threshold was 90 days before the May 2025 releases: v1.33.1/v1.32.5/v1.31.9/v1.30.13 +rke2r1.) So restarting RKE2 at least once a year keeps leaf certs fresh.

**Check expiry**:

```bash
rke2 certificate check --output table
# use --data-dir if non-default; --debug for troubleshooting
```

Each cert file contains the leaf plus its CA chain, so files appear multiple times in output.

**Manual rotation (new keys)**:

```bash
systemctl stop rke2-server
rke2 certificate rotate                      # all services
rke2 certificate rotate --service kubelet,etcd   # or specific ones
systemctl start rke2-server
```

Rotatable services: `admin`, `api-server`, `controller-manager`, `scheduler`, `rke2-controller`, `rke2-server`, `cloud-controller`, `etcd`, `auth-proxy`, `kubelet`, `kube-proxy`. (Before the Jan 2025 releases, rotate in order: etcd servers, then control-plane servers, then agents.)

**CA certificates**: self-signed CAs generated on first server startup, valid 10 years, NOT auto-renewed. Authoritative CA certs/keys live in the datastore's bootstrap key, encrypted with the server token as PBKDF2 passphrase (AES256-GCM + HMAC-SHA1); copies are extracted to `/var/lib/rancher/rke2/server/tls` at startup.

**CA rotation** with `rke2 certificate rotate-ca`:

- Stage updated CA certs/keys in a **separate temporary directory** - never overwrite live files in `/var/lib/rancher/rke2/server/tls`.
- `rke2 certificate rotate-ca --path=/opt/rke2/server` validates the new material, updates the encrypted bootstrap key in the datastore; new certs take effect on next RKE2 start. On success, restart RKE2 on all nodes - servers first, then agents.
- Non-disruptive only if the same root of trust is kept (same custom root CA, or new self-signed CAs cross-signed by the old ones - helper: `contrib/util/rotate-default-ca-certs.sh` in the k3s repo, run with `PRODUCT=rke2`).
- A brand-new untrusted root requires `--force`, re-configuring every node's token (the secure token embeds the CA hash - tokens may live in a `.env` file, systemd unit, or config.yaml), and restarting pods to trust the new root.

**Custom CA certs**: if CA files exist in `/var/lib/rancher/rke2/server/tls` before the first server ever starts, RKE2 skips self-signed generation. Required files: `server-ca.crt/key`, `client-ca.crt/key`, `request-header-ca.crt/key`, `etcd/peer-ca.crt/key`, `etcd/server-ca.crt/key`, and `service.key` (service-account signing key, no cert). Generate them from an existing root/intermediate with the k3s helper script:

```bash
mkdir -p /var/lib/rancher/rke2/server/tls
cp root-ca.pem intermediate-ca.pem intermediate-ca.key /var/lib/rancher/rke2/server/tls
curl -sL https://github.com/k3s-io/k3s/raw/master/contrib/util/generate-custom-ca-certs.sh | PRODUCT=rke2 bash -
```

Do NOT share a root/intermediate CA across clusters or reuse a general-purpose private CA: any client cert from one cluster authenticates to every cluster sharing the root, and Kubernetes has no CRL support - revocation means full CA replacement.

**Service-account issuer key**: rotate independently via `rotate-ca` with a staged `service.key` containing the NEW key first and the OLD key appended (so existing SA tokens stay valid):

```bash
mkdir -p /opt/rke2/server/tls
openssl genrsa -traditional -out /opt/rke2/server/tls/service.key 2048   # -traditional for OpenSSL 3
cat /var/lib/rancher/rke2/server/tls/service.key >> /opt/rke2/server/tls/service.key
rke2 certificate rotate-ca --path=/opt/rke2/server
# restart rke2-server on all servers; agents and pods need no restart
```

## Tokens

Tokens secure node joins and (server token) encrypt bootstrap data in the datastore.

**Formats**:

- **Secure** (preferred): `K10<cluster-CA-hash>::<credentials>` - the fixed `K10` prefix, SHA256 of the cluster server CA cert (PEM sum for self-signed; DER fingerprint for custom CAs), then user:password or bearer token. The joining node downloads `/cacerts` from the server, verifies the CA hash matches the token, validates the server cert against that CA, and only then sends credentials - authenticating the cluster to the node before the node authenticates itself.
- **Short**: credentials only; the joining node implicitly trusts whatever CA the server presents - initial connection is MITM-able. Note: the FIRST server of a cluster can only take a short token (unless using custom CAs), since the CA hash doesn't exist yet.

**Types**:

| Type | CLI / env | Notes |
| --- | --- | --- |
| Server | `--token` / `RKE2_TOKEN` | Auto-generated if unset; written to `/var/lib/rancher/rke2/server/token` in secure format. Joins servers AND agents; effectively full cluster admin - guard it and back it up with the datastore (it is the PBKDF2 passphrase for bootstrap data; needed for snapshot restore). |
| Agent | `--agent-token` / `RKE2_AGENT_TOKEN` | Defaults to the server token (`agent-token` file is a link to it). Set it on all servers to give agents a join credential that can't add servers. Static, non-expiring. |
| Bootstrap | `rke2 token` CLI | Dynamically created, auto-expiring kubeadm-style tokens, format `[a-z0-9]{6}.[a-z0-9]{16}` (id.secret). |

**`rke2 token` CLI**: `create` (prints secure-format token once - save it; `--ttl` default 24h, `0` = never expires; `--groups`, `--description`, `--usages`), `generate` (print a random token without registering it), `list`, `delete`, and:

**Server token rotation**:

```bash
rke2 token rotate --token <current> [--new-token <value>]   # random 16-char if omitted
```

Run on one server, then restart every server and agent that joined with the original token using the new value. The old token is invalidated for new joins.

## FIPS 140-2

RKE2 provides FIPS 140-2 enablement by building Go components with the Go BoringCrypto toolchain (go dev.boringcrypto branch), which swaps the standard Go crypto libraries for the NIST-validated BoringCrypto module (CMVP cert #4407). Compliance verification PDF is published on docs.rke2.io.

FIPS-compiled components:

- **Kubernetes**: API server, controller-manager, scheduler, kubelet, kube-proxy, metrics-server, kubectl.
- **Runtime**: etcd, containerd (+ shims: containerd-shim, -runc-v1, -runc-v2, ctr), crictl, runc.
- **Helm charts**: Flannel, Calico (chart components), CoreDNS.
- **CNI**: only **Canal (the default)** is rebuilt for FIPS; Calico/Cilium/Multus selected via `--cni` are not FIPS builds.
- **Ingress**: Traefik is not part of the published FIPS-compiled component list. For strict FIPS deployments, validate the ingress data path separately, or set `ingress-controller: none` and front the cluster with a FIPS-validated proxy/load balancer.

Caveats: secrets-at-rest encryption is FIPS-compliant only with the `aescbc` provider (not `secretbox`). Hardened images are multi-arch, but only Linux AMD64 is FIPS-compliant (Windows and s390x are not).

## Hardened Images

RKE2 hardened images are built from source (not mirrored from upstream) on a minimal hardened base - SUSE Linux Enterprise Base Container Image (SLE BCI) - scanned for vulnerabilities at build time, with all Go binaries compiled via the FIPS 140-2 build process. Hardening is identifiable from the image name; each RKE2 release publishes its image list as a release asset (e.g. `rke2-images-all.linux-amd64.txt` at https://github.com/rancher/rke2/releases).

## Quick Hardening Checklist

1. `useradd -r -c "etcd user" -s /sbin/nologin -M etcd -U` on all servers.
2. Copy `rke2-cis-sysctl.conf` into `/etc/sysctl.d/60-rke2-cis.conf` and apply (fresh installs only).
3. `profile: "cis"` in `/etc/rancher/rke2/config.yaml` before first start.
4. On SELinux hosts: install `rke2-selinux` (RPM default) or set `selinux: true` for tarball installs.
5. Patch `automountServiceAccountToken: false` on `default` ServiceAccounts in all namespaces.
6. Set a real audit policy in `/etc/rancher/rke2/audit-policy.yaml` and restart.
7. Add NetworkPolicies for operator-created namespaces.
8. Plan rotations: leaf certs auto-renew on restart within 120 days of expiry; CAs expire in 10 years (`rke2 certificate rotate-ca`); rotate secrets-encryption keys (`rke2 secrets-encrypt rotate-keys`) and the server token (`rke2 token rotate`) per policy.
9. Verify against the CIS self-assessment guide for your RKE2 version at https://docs.rke2.io.
