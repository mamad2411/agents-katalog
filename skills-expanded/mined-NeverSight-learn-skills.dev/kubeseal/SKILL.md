---
name: "kubeseal"
description: "Seal Kubernetes Secrets into SealedSecrets using kubeseal for secure GitOps storage. Use when users need to create or update SealedSecrets, seal credentials for GitOps repos, or migrate secrets between services. NEVER leak plaintext credentials or seal keys in output, logs, or files."
license: MIT
allowed-tools: Bash, Read, Write, Glob, Grep, kubernetes_resources_get, kubernetes_pods_log
---

# Kubeseal: Seal Kubernetes Secrets

## Overview

Seal Kubernetes Secrets into Bitnami SealedSecrets that are safe to store in Git. SealedSecrets are asymmetrically encrypted — anyone can encrypt (seal), but only the sealed-secrets controller in the cluster can decrypt (unseal).

> Validated against `kubeseal` v0.37.0. Flag names are stable across recent releases, but run `kubeseal --help` if a command behaves unexpectedly.

**Key insight:** the public certificate (`tls.crt`) is *not* secret — it is a public key, safe to share and even commit. Only the controller's private key (`tls.key`) is sensitive. Sealing is a purely local, offline operation once you have the cert; no cluster access is needed to seal.

## CRITICAL SECURITY RULES

### NEVER LEAK CREDENTIALS

1. **NEVER print plaintext credentials** to stdout, conversation output, or any readable medium.
2. **NEVER write plaintext secrets to files** in the repository or any version-controlled location.
3. **NEVER echo or log secret values** — use variables and pipe directly.
4. **NEVER include plaintext secrets in commit messages, PR descriptions, or comments.**
5. **ALWAYS overwrite or zero-out temp files** containing plaintext secrets immediately after use.
6. **NEVER leak seal key material** — the private key (`tls.key`) must never be printed, committed, or shared. Only the public key (`tls.crt`) is needed for sealing.

### Temp File Handling

**Prefer approaches that never write plaintext to a named file on disk** (see "Seal via stdin" and `--raw` below). When a temp file is unavoidable:

- Write temp secret files to `/tmp/` with descriptive names.
- After sealing, **overwrite** the temp file contents with empty or garbage data.
- Never `rm` temp files (may be blocked by permission rules) — overwrite instead:
  ```bash
  echo "" > /tmp/secret-temp.yaml
  ```
- Never commit temp files to the repository.

> Note: the public cert (`tls.crt` / `.pem`) is **not** sensitive and does **not** need sanitizing — sealing it away only forces a re-fetch. Only overwrite files that contain *plaintext secret values* or the *private key*.

## Prerequisites

- `kubeseal` CLI installed and available
- Public key certificate (`tls.crt`) from the sealed-secrets controller
- Access to the Kubernetes cluster (for retrieving existing secret values via MCP)

## Workflow

### 1. New SealedSecret

**Preferred — seal via stdin (no plaintext file on disk):**

The sealed output is safe to write directly into the repo. Only the *input* is sensitive, and piping it via a heredoc keeps it off the filesystem entirely.

```bash
kubeseal --cert /path/to/tls.crt -o yaml -f /dev/stdin > path/to/repo/sealedsecret.yaml <<'EOF'
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
  namespace: my-namespace
type: Opaque
stringData:
  key1: "value1"
  key2: "value2"
EOF
```

**Alternative — temp file (when you must inspect/edit the plaintext first):**

```bash
# Write secret to temp file (NEVER to repo)
cat > /tmp/my-secret.yaml <<'EOF'
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
  namespace: my-namespace
type: Opaque
stringData:
  key1: "value1"
  key2: "value2"
EOF

# Seal and output YAML (sealed output is safe to write straight to the repo)
kubeseal --cert /path/to/tls.crt --format yaml -f /tmp/my-secret.yaml > path/to/repo/sealedsecret.yaml

# SANITIZE the plaintext temp file immediately (the sealed output is not sensitive)
echo "" > /tmp/my-secret.yaml
```

### 2. Update Existing SealedSecret (Preserving Fields)

When updating some keys in a SealedSecret (e.g., changing S3 credentials but keeping a database password), you have two options:

- **Update individual keys** with `--raw` (paste into `encryptedData`) or `--merge-into` — you only need the values of the keys you're changing.
- **Re-seal the whole secret** — you need the plaintext of ALL keys, retrieved from the cluster.

#### Step 1: Retrieve existing secret from the cluster

```bash
# Use kubernetes_resources_get MCP tool to read the decrypted Secret
# The SealedSecret controller auto-decrypts into a regular Secret in the cluster
```

Or via kubectl:
```bash
kubectl get secret <name> -n <namespace> -o jsonpath='{.data}'
```

#### Step 2: Decode and re-seal with updated values

> **DANGER — do not interpolate secret values into YAML.** A value containing `"`, `:`, `\n`, leading spaces, or `$` will break the quoting and either corrupt the secret or make `kubeseal` fail with `error: no secrets found`. This is common with generated passwords and S3 keys. **Never** build YAML like `password: "$EXISTING_PASS"`.

**Safe approach — seal each key individually with `--raw`, then merge.** `--raw` reads the value from stdin as raw bytes (no YAML quoting involved), so special characters are handled correctly. Under the default `strict` scope you must pass `--name` and `--namespace`, and they must match the target SealedSecret.

```bash
NS=my-namespace
NAME=my-secret

# Decode a value you want to PRESERVE (capture in variable, NEVER echo)
EXISTING_PASS=$(printf '%s' '<base64value>' | base64 -d)

# Re-seal the preserved value and the updated value straight into the repo file.
# printf '%s' avoids adding a trailing newline to the secret.
printf '%s' "$EXISTING_PASS" | kubeseal --cert /path/to/tls.crt \
  --raw --namespace "$NS" --name "$NAME" --from-file=/dev/stdin
# -> paste the output under spec.encryptedData.password in path/to/repo/sealedsecret.yaml

printf '%s' 'new-value' | kubeseal --cert /path/to/tls.crt \
  --raw --namespace "$NS" --name "$NAME" --from-file=/dev/stdin
# -> paste the output under spec.encryptedData.access-key-id
```

Or use `--merge-into` (see below) to update individual keys in place without touching the others.

**If you must build a full Secret object** (e.g. a fresh SealedSecret from scratch), avoid quoting pitfalls by base64-encoding values into the `data:` field instead of `stringData:`:

```bash
cat > /tmp/updated-secret.yaml <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: $NAME
  namespace: $NS
type: Opaque
data:
  access-key-id: $(printf '%s' 'new-value' | base64 -w0)
  password: $(printf '%s' "$EXISTING_PASS" | base64 -w0)
EOF

kubeseal --cert /path/to/tls.crt --format yaml -f /tmp/updated-secret.yaml > path/to/repo/sealedsecret.yaml

# SANITIZE the plaintext temp file
echo "" > /tmp/updated-secret.yaml
```

### 3. Fetch Public Key From Cluster

If you don't have the public key locally, fetch it from the running sealed-secrets controller. Use `--controller-namespace` / `--controller-name` to locate the controller — **not** `--namespace`, which sets the CLI request scope and has no effect on cert fetching. The defaults are `sealed-secrets-controller` in `kube-system`.

```bash
# Defaults (controller "sealed-secrets-controller" in "kube-system"):
kubeseal --fetch-cert > /tmp/sealed-secrets-cert.pem

# Non-default location:
kubeseal --fetch-cert \
  --controller-namespace sealed-secrets \
  --controller-name sealed-secrets > /tmp/sealed-secrets-cert.pem
```

`--fetch-cert` returns only the **public** cert — it is safe to keep and reuse (do **not** sanitize it).

If `kubeseal` can't reach the controller service directly, fetch the cert from the active key Secret. The key Secret has a generated name, so select it by label rather than a fixed name:

```bash
kubectl get secret -n kube-system \
  -l sealedsecrets.bitnami.com/sealed-secrets-key=active \
  -o jsonpath='{.items[0].data.tls\.crt}' | base64 -d > /tmp/sealed-secrets-cert.pem
```

> **Caution:** the key Secret also contains `tls.key` (the private key). Extract **only** `tls.crt` as shown above. Never write, print, or commit `tls.key`.

## kubeseal Command Reference

### Common Flags

| Flag | Purpose |
|------|---------|
| `--cert <file\|URL>` | Public key file (or URL) for encryption (overrides controller auto-detect) |
| `-o, --format yaml\|json` | Output format (default: json) |
| `-f, --secret-file <file>` | Input Secret YAML file (use `/dev/stdin` to pipe) |
| `-n, --namespace <ns>` | Namespace scope for **the secret being sealed** (not the controller's location) |
| `--scope strict\|namespace-wide\|cluster-wide` | Scoping of the sealed secret (default: `strict`) |
| `--merge-into <file>` | Merge sealed keys into existing SealedSecret file (in-place) |
| `--raw` | Encrypt a single raw value from `--from-file`; requires `--scope`, plus `--name`+`--namespace` for strict scope |
| `--from-file <file>` | (with `--raw`) Source the value from a file; use `/dev/stdin` for a pipe |
| `--name <name>` | Name of the sealed secret (required with `--raw` under strict scope) |
| `--re-encrypt` | Re-encrypt an existing SealedSecret with the controller's latest key (needs cluster) |
| `--validate` | Verify the sealed secret decrypts — **contacts the controller; requires cluster access** |
| `--fetch-cert` | Print the controller's public cert to stdout |
| `--controller-namespace <ns>` | Namespace where the controller runs (default: `kube-system`) |
| `--controller-name <name>` | Controller name (default: `sealed-secrets-controller`) |
| `--recovery-unseal` | Disaster-recovery decrypt using `--recovery-private-key` (**handles the private key — use with extreme caution**) |

### Scope Modes

- **`strict`** (default): Can only be unsealed with the exact namespace and name.
- **`namespace-wide`**: Can be unsealed in the specified namespace with any name.
- **`cluster-wide`**: Can be unsealed in any namespace with any name.

### Merge Into Existing

To update individual keys without re-sealing the entire secret (useful when you can't retrieve all plaintext values):

```bash
# Seal only the keys you want to update
cat > /tmp/delta-secret.yaml <<'EOF'
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
  namespace: my-namespace
type: Opaque
stringData:
  new-key: "new-value"
EOF

# Merge into existing sealed secret
kubeseal --cert /path/to/tls.crt --merge-into path/to/repo/sealedsecret.yaml -f /tmp/delta-secret.yaml

# SANITIZE
echo "" > /tmp/delta-secret.yaml
```

**WARNING**: `--merge-into` adds or updates keys but does NOT remove keys. To remove a key, you must re-seal the entire secret from scratch.

### Encrypt a Single Value (`--raw`)

`--raw` encrypts one value and prints the ciphertext string — you paste it under `spec.encryptedData.<key>` yourself. This is the safest way to handle values with special characters (it reads raw bytes from stdin, bypassing YAML quoting entirely) and it never writes plaintext to a file.

```bash
# strict scope (default): --name AND --namespace are REQUIRED and must match the target SealedSecret
printf '%s' 'p@ss"word:with$pecial' | kubeseal --cert /path/to/tls.crt \
  --raw --namespace my-namespace --name my-secret --from-file=/dev/stdin

# namespace-wide: only --namespace required
printf '%s' 'value' | kubeseal --cert /path/to/tls.crt \
  --raw --scope namespace-wide --namespace my-namespace --from-file=/dev/stdin

# cluster-wide: neither required
printf '%s' 'value' | kubeseal --cert /path/to/tls.crt \
  --raw --scope cluster-wide --from-file=/dev/stdin
```

- Use `printf '%s'` (not `echo`) to avoid appending a trailing newline to the secret value.
- The `--raw` ciphertext is bound to the scope/name/namespace you pass. If they don't match the SealedSecret it's pasted into, the controller will refuse to unseal it.

### Rotate to a New Controller Key (`--re-encrypt`)

After the controller's key pair is rotated, existing SealedSecrets still decrypt (the controller keeps old keys) but should be re-encrypted to the latest key. This requires cluster access:

```bash
kubeseal --re-encrypt -o yaml -f path/to/repo/sealedsecret.yaml > /tmp/reencrypted.yaml
cp /tmp/reencrypted.yaml path/to/repo/sealedsecret.yaml
```

`--re-encrypt` never exposes plaintext — the re-encryption happens inside the controller.

## SealedSecret YAML Structure

```yaml
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: my-secret
  namespace: my-namespace
spec:
  encryptedData:
    key1: AgC...base64encrypteddata...==
    key2: AgC...base64encrypteddata...==
  template:
    metadata:
      name: my-secret
      namespace: my-namespace
    type: Opaque
```

## Common Patterns

### S3-Compatible Object Store Credentials

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: s3-credentials
  namespace: my-namespace
type: Opaque
stringData:
  access-key-id: "<access-key>"
  secret-access-key: "<secret-key>"
```

### Database Credentials

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
  namespace: my-namespace
type: Opaque
stringData:
  username: "admin"
  password: "<password>"
```

### TLS Certificate

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: tls-cert
  namespace: my-namespace
type: kubernetes.io/tls
stringData:
  tls.crt: |
    -----BEGIN CERTIFICATE-----
    ...
    -----END CERTIFICATE-----
  tls.key: |
    -----BEGIN PRIVATE KEY-----
    ...
    -----END PRIVATE KEY-----
```

## Pitfalls and Gotchas

1. **Each key is encrypted independently** — you can't mix encrypted values from different sealing operations into the same `encryptedData` block without re-sealing. Use `--merge-into` or re-seal the entire secret.

2. **SealedSecrets are bound to the controller's key pair** — the controller retains old keys after rotation, so existing SealedSecrets keep decrypting. But new seals need the current public cert, and best practice is to `kubeseal --re-encrypt` existing SealedSecrets onto the latest key. If old keys are ever purged, un-re-encrypted SealedSecrets become undecryptable.

3. **`stringData` vs `data`** — use `stringData` for plaintext values (kubeseal handles encoding). Use `data` for pre-base64-encoded values.

4. **Scope matters** — a `strict`-scoped SealedSecret can only be unsealed with the exact name and namespace. If you rename the secret, it won't unseal. Use `namespace-wide` or `cluster-wide` if name changes are expected.

5. **Temp file hygiene** — always overwrite temp files after sealing. Never leave plaintext secrets on disk.

6. **Git history** — if a secret was accidentally committed, it remains in git history. Use `git filter-repo` to remove it, then rotate the credential.

## Verification

**Before deploying**, validate the sealed secret against the live controller (this contacts the cluster — it does not work offline):

```bash
# --validate talks to the controller (no --cert needed); add --controller-namespace/--controller-name if non-default
kubeseal --validate -f path/to/repo/sealedsecret.yaml
```

**After deploying**, verify it unsealed correctly:

```bash
# Check the Secret exists and has the expected keys
kubectl get secret <name> -n <namespace> -o jsonpath='{.data}' | python3 -c "import sys,json; [print(k) for k in json.load(sys.stdin).keys()]"
```

Or use the kubernetes_resources_get MCP tool to inspect the decrypted Secret.

## Post-Sealing Checklist

- [ ] Temp files overwritten (not just deleted)
- [ ] No plaintext credentials in shell history (use `set +o history` before sensitive operations)
- [ ] No credentials in git diff output
- [ ] SealedSecret YAML committed to the correct branch
- [ ] No seal private keys (`tls.key`) in the repository or output
- [ ] Verified the sealed secret unseals correctly on the cluster
