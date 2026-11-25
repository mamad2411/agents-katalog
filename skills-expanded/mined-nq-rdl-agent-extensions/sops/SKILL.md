---
name: sops
license: CC-BY-4.0
description: >-
  Use when encrypting or decrypting `.env`, `.yaml`, `.json`, or `.ini` secrets
  — even if the user does not say "SOPS" explicitly. Triggers on: storing
  secrets in Git safely, Age encryption, HashiCorp Vault transit, `SOPS_AGE_KEY_FILE`,
  `SOPS_AGE_RECIPIENTS`, `VAULT_ADDR`, or any request to keep config files
  secret while keeping diffs reviewable. Covers key generation, `.sops.yaml`
  creation rules, in-place editing, multi-recipient setups, and key rotation
  with `sops updatekeys`. Load for `.env`, YAML, JSON, INI, and binary file
  encryption tasks even when the user reaches for words like "encrypt my
  cluster secrets", "seal this config", or "share secrets with my team".
compatibility: >-
  Requires sops CLI; and either age (for Age backend) or a HashiCorp Vault
  instance with the transit engine enabled (for Vault backend). Examples
  tested with sops 3.13.3, age 1.3.2 and Vault 2.1.1 dev server on
  2026-09-29. The `sops encrypt`/`decrypt`/`edit`/`rotate` subcommands need
  sops >= 3.9.0 and `SOPS_EDITOR` needs >= 3.10.0 (sops CHANGELOG.md).
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# SOPS Encryption Skill

Encrypt and decrypt secrets with [SOPS](https://github.com/getsops/sops) (Secrets OPerationS). SOPS encrypts only the *leaf values* in YAML/JSON/ENV/INI/BINARY files — keys stay in plaintext, keeping diffs reviewable in Git. This skill covers the **Age** and **HashiCorp Vault** backends.

---

## Quick Reference

| Operation | Command | Reference |
|-----------|---------|-----------|
| Encrypt (Age) | `sops encrypt --age <pubkey> file.yaml > file.enc.yaml` | [age.rst](references/age.rst) |
| Encrypt (Vault) | `sops encrypt --hc-vault-transit $VAULT_ADDR/v1/sops/keys/mykey file.yaml > file.enc.yaml` | [vault.rst](references/vault.rst) |
| Decrypt to stdout | `sops decrypt file.enc.yaml` | [age.rst](references/age.rst) |
| Edit in place | `sops edit file.enc.yaml` | [age.rst](references/age.rst) |
| Rotate recipients | `sops updatekeys -y file.enc.yaml` | [age.rst](references/age.rst) / [vault.rst](references/vault.rst) |
| Init `.sops.yaml` | Add `creation_rules` to project root | both references |

---

## The Encryption Flow

1. **Identify the format** — SOPS auto-detects from the file extension (`.yaml`, `.json`, `.env`, `.ini`). Use `--input-type` / `--output-type` when the extension is ambiguous or unrecognised (an unknown suffix such as `.enc` or `.txt` is read as JSON).
2. **Choose the backend** — Age for simplicity (key file on disk); Vault for centralised, audited key management.
3. **Configure recipients** — either pass `--age` / `--hc-vault-transit` on the CLI, or commit a `.sops.yaml` at the project root so SOPS picks up the right key automatically.
4. **Execute** — `sops encrypt`, `sops decrypt`, or `sops edit` as needed.

---

## Generating an Age Key

```bash
mkdir -p "$HOME/.config/sops/age"
age-keygen -o "$HOME/.config/sops/age/keys.txt"
```

The public key is printed to **stderr** — copy it into `--age` or `.sops.yaml`. The private key written to `keys.txt` is what SOPS uses for decryption. See [age.rst](references/age.rst) for default lookup paths on Linux and macOS.

---

## `.sops.yaml` Workflow

A `.sops.yaml` at the project root tells SOPS which key to use for each path, so you never need to pass `--age` or `--hc-vault-transit` manually:

```yaml
creation_rules:
  - path_regex: ^(secrets/|\.env)
    encrypted_regex: ^(data|stringData|password|token|secret)$
    age: >-
      age1yt3tfqlfrwdwx0z0ynwplcr6qxcxfaqycuprpmy89nr83ltx74tqdpszlw,
      age1s3cqcks5genc6ru8chl0hkkd04zmxvczsvdxq99ekffe4gmvjpzsedk23c
```

`encrypted_regex` scopes encryption to matching *keys* only — useful for Kubernetes secrets where you want `data` and `stringData` encrypted but not the rest of the manifest. Omit it to encrypt all leaf values.

---

## Key Rotation

After updating `.sops.yaml` with new recipients, re-encrypt the data key without touching plaintext values:

```bash
sops updatekeys -y secrets/prod.yaml
```

Without `-y`, `updatekeys` asks `Is this okay? (y/n)`; with no terminal (scripts, CI, `find -exec`) it reads EOF and leaves the file unchanged.

See the rotation subsections in [age.rst](references/age.rst) and [vault.rst](references/vault.rst) for backend-specific steps.

---

## Gotchas

- **SOPS encrypts values, not keys.** Key names stay in plaintext — diffs remain reviewable, but don't put secrets in key names.
- **Top-level arrays are not supported.** Wrap arrays in an object: `{"data": [...]}` instead of `[...]`.
- **Keep the file extension stable.** SOPS detects format from the extension at decrypt time. Renaming `.yaml` to `.txt` causes a parse failure — use `--input-type` / `--output-type` if you must change it.
- **Name encrypted dotenv files so the type is still detectable.** A `.env.enc` suffix is read as JSON (`Could not unmarshal input data: invalid character ...`), so `sops decrypt .env.enc` and `sops decrypt -i .env.enc` both fail. Pass the type explicitly — `sops decrypt --input-type dotenv --output-type dotenv .env.enc > .env` — or keep a `.env` suffix (`secrets.enc.env`), which `sops decrypt` and `-i` detect.
- **A missing `SOPS_AGE_KEY_FILE` is not fatal on its own.** SOPS loads every key source; if another one (e.g. the default `keys.txt`) holds the key, decryption still succeeds. If none does, the error names the file: `failed to open SOPS_AGE_KEY_FILE file: open <path>: no such file or directory`.
- **Vault tokens are needed at both encrypt *and* decrypt time.** A valid token (`VAULT_TOKEN` or `~/.vault-token`) is required by both; without it Vault returns `403 permission denied`. `VAULT_ADDR` is only needed to encrypt — the file stores `vault_address` in its metadata and decrypt uses that.
- **Don't commit the age private key.** Only the public key belongs in `.sops.yaml` or `--age`. The private key file (`keys.txt`) should be in `.gitignore`.
- **Verify against the canonical docs.** The upstream README is now a stub; if observed behaviour differs from the tested versions above, check [getsops.io/docs](https://getsops.io/docs/) and `sops <command> --help` for the installed version.

---

## Reference Guides

Load the appropriate reference based on the backend in use:

- [**Encrypting with Age**](references/age.rst) — Age key generation, encryption, decryption, in-place editing, SSH key support, and recipient rotation. Load this when the user is using Age or mentions `age-keygen`, `SOPS_AGE_KEY_FILE`, or `SOPS_AGE_RECIPIENTS`.
- [**Encrypting with HashiCorp Vault**](references/vault.rst) — Vault transit engine setup, authentication (token / AppRole), encryption, decryption, and key rotation with `vault write -f .../rotate`. Load this when the user mentions Vault, `VAULT_ADDR`, or `hc_vault_transit_uri`.
