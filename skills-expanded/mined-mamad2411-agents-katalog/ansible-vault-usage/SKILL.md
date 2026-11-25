---
name: ansible-vault-usage
description: >
  Ansible Vault encrypt/decrypt, vault IDs, password files, rekey, and CI secret injection
  so playbooks never commit plaintext secrets. Use when ansible-vault, vault_id, encrypted
  group_vars/host_vars, vault password file, rekey, or CI decrypt for ansible-playbook on
  owned repos — not HashiCorp Vault product ops alone (different tool).
---

# Ansible Vault Usage

## Scope And Authorization

- **In scope:** Ansible repositories and inventories you operate.
- **Out of scope:** Decrypting vault files without authorization; committing vault passwords.
- Note: **Ansible Vault** ≠ HashiCorp Vault (see catalog for HV). This skill is Ansible’s encrypt-at-rest for vars/files.
- Pair with `ansible-role-testing` and `secrets-management-hygiene`.

## When To Use

- Encrypting `group_vars` / `host_vars` / secret files in git.
- Multiple vault IDs (dev vs prod).
- CI playbook runs that need decrypt.
- Rekey after personnel change or password leak.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Molecule/lint role testing | `ansible-role-testing` |
| HashiCorp Vault server | vault skills in catalog |
| Age/SOPS file encryption | `age-encryption-cli` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Command / concept | Use |
| --- | --- |
| `ansible-vault encrypt` | Whole file |
| `encrypt_string` | Inline secret in YAML |
| `decrypt` / `view` / `edit` | Access plaintext safely |
| `--vault-id` | Named passwords |
| `rekey` | Change password |
| Password file / prompt | Runtime unlock |

## Workflow

### 1. Confirm success criteria

1. No plaintext secrets in git history going forward; vault password distribution documented; CI works; rekey runbook exists.
2. Decide single vault vs multiple IDs (`dev@prompt`, `prod@prompt`).

### 2. Encrypt secrets

```bash
# Whole file
ansible-vault encrypt group_vars/prod/vault.yml
# Create new
ansible-vault create group_vars/prod/vault.yml
# Inline
ansible-vault encrypt_string 's3cr3t' --name 'db_password'
```

```yaml
# group_vars/prod/main.yml can reference vault.yml vars
db_password: "{{ vault_db_password }}"
```

### 3. Vault IDs and password files

```bash
# Encrypt with label
ansible-vault encrypt --vault-id prod@prompt group_vars/prod/vault.yml
# Runtime
ansible-playbook site.yml --vault-id prod@./.vault/prod_pass
chmod 600 ./.vault/prod_pass   # never commit
```

```gitignore
.vault/
*.vault_pass
```

### 4. Edit / view safely

```bash
ansible-vault edit group_vars/prod/vault.yml
ansible-vault view group_vars/prod/vault.yml
# Avoid long-lived decrypted copies on disk
```

### 5. CI injection

```bash
# CI secret -> file
printenv ANSIBLE_VAULT_PASSWORD > "$RUNNER_TEMP/vpass"
chmod 600 "$RUNNER_TEMP/vpass"
ansible-playbook site.yml --vault-password-file "$RUNNER_TEMP/vpass"
```

1. Prefer OIDC to cloud secret stores over long-lived CI secrets when possible.
2. Mask passwords in CI logs.

### 6. Rekey and rotation

```bash
ansible-vault rekey --vault-id prod@prompt group_vars/prod/vault.yml
# Or rekey many:
find group_vars -name 'vault.yml' -print0 | xargs -0 ansible-vault rekey
```

1. Rotate when someone with password leaves.
2. Verify playbook after rekey in staging.

### 7. Verify hygiene

```bash
# Fail if high-entropy secrets unencrypted (heuristic)
rg -n "password:|secret:|api_key:" group_vars/ host_vars/ | rg -v 'ANSIBLE_VAULT|vault_'
ansible-lint
```

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Storage | Encrypted vault.yml in git | Plain `password: hunter2` |
| Passwords | Password manager / CI secret | Vault pass committed |
| Scope | Split prod/dev vault IDs | One password forever for all envs |
| Edits | `ansible-vault edit` | Decrypt, commit plain, re-encrypt later |

## Output Checklist

- [ ] Secrets identified and encrypted
- [ ] Vault IDs strategy documented
- [ ] Password distribution + gitignore done
- [ ] Playbook decrypt works locally and CI
- [ ] Rekey runbook tested
- [ ] Lint/secret scan clean of plaintext
- [ ] `code-quality-standards` applied

## Rules

- Never commit vault passwords or decrypted secrets.
- Use vault IDs to separate environments.
- Rekey on personnel or suspected leak.
- Ansible Vault protects git rest; still use least privilege on hosts.
- Do not confuse with HashiCorp Vault operations.
