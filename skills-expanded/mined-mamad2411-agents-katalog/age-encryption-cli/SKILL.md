---
name: age-encryption-cli
description: >
  age (FiloSottile/age) encrypt/decrypt for files and SOPS integration: X25519
  recipients, SSH recipients, identity files, armor, and git-friendly workflows. Use when
  encrypting secrets for repos, handoffs, or SOPS-age backends on owned systems — not for
  breaking others’ ciphertext or committing private identities.
---

# age Encryption CLI

## Scope And Authorization

- **In scope:** encrypting data for teams/systems you operate; managing your recipients/identities.
- **Out of scope:** attacking others’ encrypted files; sharing private keys in tickets/chat.
- Private identities (`age1...` secret keys / `AGE-SECRET-KEY-1...`) are high-value secrets.
- Prefer hardware-backed or passphrase-protected storage for long-term identities.
- Pair automation with `code-quality-standards` and `secrets-management-hygiene`.

## When To Use

- Encrypt files for multiple recipients with `age`.
- SOPS using `age` as creation rule backend.
- Replacing ad-hoc GPG for simple file encryption in CI/dev.
- Generating and rotating recipient keys for a team.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Org-wide secrets program | `secrets-management-hygiene` |
| Ansible Vault | `ansible-vault-usage` |
| Cloud KMS-only envelope patterns | cloud secrets skills |
| ACME/TLS cert automation | `acme-dns01-automation` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Item | Purpose |
| --- | --- |
| Recipient | Public key (`age1...`) or SSH pubkey that can decrypt |
| Identity | Private key file for decrypt |
| `-a` / armor | ASCII armored ciphertext for git |
| `-R` | Recipients file (list of public keys) |
| `-i` | Identity file(s) for decrypt |
| SOPS | Encrypts structured YAML/JSON/env fields with age |

## Workflow

### 1. Confirm scope and success criteria

1. Record data class, who must decrypt (humans, CI bots), and storage location (git vs object store).
2. Success: encrypt with intended recipients only; CI decrypts via bot identity; rotation plan exists.
3. Decide passphrase-protected identity vs machine identity.

### 2. Install and generate keys

```bash
# Install per platform (examples)
# go install filippo.io/age/cmd/...@latest
age --version
age-keygen -o key.txt
# key.txt contains AGE-SECRET-KEY-1... and prints public age1...
age-keygen -y key.txt   # show public recipient from identity file
```

1. Store `key.txt` outside git; chmod `600`.
2. Publish only the `age1` public recipient to the team list.

### 3. Encrypt and decrypt files

```bash
# Single recipient
age -r age1xxxxxxxx -o secrets.yaml.age secrets.yaml

# Multiple recipients
age -r age1alice -r age1bob -o bundle.age bundle.tar

# Recipients file
cat > recipients.txt <<'EOF'
# alice
age1alice...
# bob
age1bob...
# ci bot
age1ci...
EOF
age -R recipients.txt -a -o secrets.env.age secrets.env

# Decrypt
age -d -i key.txt -o secrets.env secrets.env.age
```

**SSH recipient (convenient for humans):**

```bash
age -R ~/.ssh/id_ed25519.pub -o f.age f
age -d -i ~/.ssh/id_ed25519 -o f f.age
```

### 4. SOPS + age pattern

```yaml
# .sops.yaml
creation_rules:
  - path_regex: secrets/.*\.yaml$
    age: >-
      age1alice...,age1bob...,age1ci...
```

```bash
sops --encrypt --in-place secrets/prod.yaml
sops --decrypt secrets/prod.yaml > /dev/shm/prod.yaml
# Edit
sops secrets/prod.yaml
```

1. Never commit decrypted plain files.
2. CI: inject bot identity via secret store; `SOPS_AGE_KEY_FILE` or `SOPS_AGE_KEY`.

### 5. Rotation and access control

| Event | Action |
| --- | --- |
| Person joins | Add recipient; re-encrypt secrets |
| Person leaves | Remove recipient; re-encrypt **all** secrets with new recipient set |
| Bot compromise | Generate new bot identity; revoke old; rotate ciphertext |
| Suspected leak | Rotate identities + all encrypted payloads |

```bash
# Re-encrypt for new recipient set (decrypt with old, encrypt with new)
age -d -i key.txt -o - old.age | age -R recipients-new.txt -a -o new.age
```

### 6. Verify

```bash
# Wrong identity must fail
age -d -i wrong-key.txt secrets.env.age && echo 'FAIL: decrypted' || echo 'ok deny'
# List recipients (metadata) when using tools that support inspection; otherwise doc recipients file
sha256sum secrets.env.age
```

1. Confirm armored files are readable as ASCII in PRs.
2. Ensure shell history does not capture passphrases (`set +o history` practices).

### 7. Hand off

1. Document recipients owners, identity backup, and SOPS paths.
2. CODEOWNERS on `recipients.txt` / `.sops.yaml`.
3. Train team: never paste `AGE-SECRET-KEY` into chat.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Keys | Public in repo; private in vault | Identity committed to git |
| Recipients | Explicit file + rotation | Encrypt only to personal laptop key for team secrets |
| CI | Ephemeral key mount | Long-lived key in plaintext log |
| Format | Armored for git text | Binary blobs without need |
| Rotation | Leave re-encrypt checklist | Remove person but leave old ciphertext |

## Output Checklist

- [ ] Recipients and owners listed
- [ ] Identities stored safely (not in git)
- [ ] Encrypt/decrypt path tested for humans and CI
- [ ] SOPS rules (if used) cover secret paths
- [ ] Rotation procedure documented
- [ ] Armor/git hygiene decided
- [ ] Access removal path tested once
- [ ] `code-quality-standards` on scripts

## Rules

- Protect private identities like production root keys.
- Encrypt only for current need-to-know recipients.
- Do not attempt to “break age” for unauthorized access.
- Prefer age/SOPS over DIY crypto.
- Never log plaintext secrets during decrypt in CI.
