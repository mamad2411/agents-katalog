---
name: vault-helper
description: Streamlines Ansible Vault secret management for the olympus cluster — scaffolds new secrets, validates vault references, and guides rotation workflows
when_to_use: |
  Use this skill when the user:
  - Needs to add a new secret or credential to the cluster
  - Is setting up a new service that needs credentials
  - Wants to rotate a credential
  - References vault_ variables in Ansible tasks
  - Asks about ansible-vault commands or encrypted variables
  - Is onboarding a new service VM or agent VM that needs secrets
---

# Ansible Vault Helper — Olympus Cluster

## Vault File Location

All secrets live in a single encrypted vault file:

```
ansible/inventory/group_vars/all/all.yml
```

This file is encrypted with Ansible Vault and requires `~/.vault_pass.txt` to edit.

## Editing Secrets

```bash
cd ansible

# Open for editing (decrypts in-place, re-encrypts on save)
ansible-vault edit inventory/group_vars/all/all.yml \
  --vault-password-file ~/.vault_pass.txt

# View without editing
ansible-vault view inventory/group_vars/all/all.yml \
  --vault-password-file ~/.vault_pass.txt

# Decrypt to plain text (CAREFUL — do not commit decrypted file)
ansible-vault decrypt inventory/group_vars/all/all.yml \
  --vault-password-file ~/.vault_pass.txt
```

## Adding a New Secret

### Step 1: Determine the vault variable name

Convention: all vault variables are prefixed with `vault_`:

```yaml
vault_<service>_<credential_type>: <secret_value>

# Examples:
vault_grafana_admin_password: supersecret
vault_pbs_api_token: user@pbs!tokenid=secret
vault_zeus_discord_token: Bot abc123xyz
vault_idrac_password: dell_root_password
```

### Step 2: Add to the vault file

```bash
ansible-vault edit inventory/group_vars/all/all.yml \
  --vault-password-file ~/.vault_pass.txt
```

Add the new variable in the appropriate section. Keep related secrets grouped.

### Step 3: Reference in the role

In the role's `tasks/setup.yml`, reference as `{{ vault_<name> }}`:

```yaml
- name: Set service password
  ansible.builtin.template:
    src: config.yml.j2
    dest: /etc/service/config.yml
  vars:
    password: "{{ vault_grafana_admin_password }}"
```

Or pass via environment variable in Docker Compose:

```yaml
# In a template file
environment:
  - GF_SECURITY_ADMIN_PASSWORD={{ vault_grafana_admin_password }}
```

### Step 4: Add default placeholder in `defaults/main.yml`

```yaml
# roles/<role>/defaults/main.yml
# Do NOT put real values here — this is for documentation only
grafana_admin_password: "{{ vault_grafana_admin_password }}"
```

## New Service Secret Scaffolding

When setting up a new service, these variables typically need to be vaulted:

| Service Type | Required Secrets |
|-------------|-----------------|
| Monitoring exporter | `vault_<exporter>_api_token`, `vault_<exporter>_password` |
| Discord bot | `vault_<agent_name>_discord_token` |
| Proxmox API user | `vault_proxmox_api_token_secret` |
| PBS integration | `vault_pbs_api_token` |
| External service | `vault_<service>_api_key` |
| Database | `vault_<db>_password`, `vault_<db>_root_password` |

## Vault Reference Check

Verify every `vault_*` variable used in tasks has a corresponding vault entry:

```bash
# Find all vault variable references in roles:
grep -r "vault_" ansible/roles/ --include="*.yml" | grep -v "^#" | \
  grep -oP 'vault_\w+' | sort -u

# Compare against what's in the vault:
ansible-vault view inventory/group_vars/all/all.yml \
  --vault-password-file ~/.vault_pass.txt | grep "^vault_" | \
  awk '{print $1}' | sort -u
```

Any variable in the first list but not the second needs to be added to the vault.

## Credential Rotation

### Step 1: Identify all references

```bash
grep -r "vault_<old_var_name>" ansible/ --include="*.yml"
# Also check templates:
grep -r "vault_<old_var_name>" ansible/roles/*/templates/
```

### Step 2: Update the service credential externally

(Log into the service — Grafana, PBS, Proxmox API, Discord portal, etc. — and rotate the credential there first)

### Step 3: Update the vault

```bash
ansible-vault edit inventory/group_vars/all/all.yml \
  --vault-password-file ~/.vault_pass.txt
# Update the value
```

### Step 4: Re-apply affected roles

```bash
cd ansible
ansible-playbook -i inventory/hosts.yml service_vms.yml \
  --tags <affected_service> \
  --vault-password-file ~/.vault_pass.txt
```

### Step 5: Verify

Confirm the service is working with the new credential before committing.

## Current Vault Variables Reference

See `references/vault-patterns.md` for the complete list of expected vault variables and their purpose.
