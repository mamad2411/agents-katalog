---
name: new-conf
description: Generate an annotated ansible.cfg for a specific environment. Triggered by /new-conf. Asks for target environment (dev, CI, or AWX) and generates a fully annotated ansible.cfg covering all official sections including defaults, privilege escalation, SSH connection, vault config, callback plugins, and fact caching. Shows summary before writing.
---

# new-conf

Generate an annotated ansible.cfg for a specific environment.

---

## Required Inputs

1. **target_path** — Where to write the ansible.cfg (default: `./ansible.cfg`; warn if one already exists)
2. **environment** — Target environment:
   - `dev` — development workstation, local VMs
   - `ci` — CI/CD pipeline (GitHub Actions, GitLab CI, Jenkins)
   - `awx` — AWX / Ansible Automation Platform

---

## Behavior

### Step 1 — Discovery
Run discovery per `references/discovery.md`. Check if an ansible.cfg already exists at the target path. If it does:
```
An ansible.cfg already exists at ./ansible.cfg.
Overwriting it will replace all current settings.
Use /ansible-designer:update-conf to make targeted changes instead.
Proceed with overwrite? (yes/no)
```

### Step 2 — Parameter Collection
Ask for environment if not provided. Show options:
```
Which environment is this ansible.cfg for?
  1. dev — Development (local VMs, permissive settings, verbose output)
  2. ci  — CI/CD pipeline (strict, no interactive prompts, minimal output)
  3. awx — AWX / Automation Controller (callback plugins, fact caching)

Enter 1, 2, or 3:
```

### Step 3 — Pre-Write Confirmation
Show summary:
```
Will create: ./ansible.cfg (dev profile)

Sections:
  [defaults]          — inventory=./inventory, forks=10, yaml callback, profile_tasks
  [diff]              — always=True, context=5
  [privilege_escalation] — become=True, sudo
  [ssh_connection]    — pipelining=True, ControlMaster=auto
  [persistent_connection] — connect_timeout=30

Security notes:
  host_key_checking=False (dev only — NOT for production)
  All settings annotated with justification comments

Proceed? (yes/no)
```

### Step 4 — Generate ansible.cfg
Use the appropriate profile from `references/ansible_cfg.md`:
- `dev` → Profile 1
- `ci` → Profile 2
- `awx` → Profile 3

**All non-default values must have an inline comment explaining why.**
**Security-sensitive settings (host_key_checking=False) must have a justification comment.**
**Any vault guidance must stay aligned with `references/security_vault.md`.**

### Step 5 — Final Output
Show file path:
```bash
ls -la ./ansible.cfg
```

Suggest next step:
```
Next step: Validate with `ansible --version` to confirm the config is loaded
           or use /ansible-designer:review-conf to check for security issues.
```

---

## Sections to Include (all environments)

Every generated ansible.cfg must include all of these sections, populated with environment-appropriate values:

1. `[defaults]` — inventory, remote_user, private_key_file, host_key_checking, forks, timeout, log_path, roles_path, collections_path, retry_files_enabled, stdout_callback, callbacks_enabled, gathering, fact_caching, fact_caching_connection, fact_caching_timeout, error_on_undefined_vars
2. `[diff]` — always, context
3. `[privilege_escalation]` — become, become_method, become_user, become_ask_pass
4. `[ssh_connection]` — pipelining, control_path, control_master, control_persist, ssh_args
5. `[persistent_connection]` — connect_timeout, command_timeout
6. `[colors]` (dev only) — highlight, verbose, warn, error
7. Vault config comment block — vault_password_file or vault_identity_list guidance

---

## Environment Differences Summary

| Setting | dev | ci | awx |
|---------|-----|-----|-----|
| host_key_checking | False (dev only) | False (ephemeral runners) | True |
| stdout_callback | yaml | json | minimal |
| callbacks_enabled | profile_tasks, timer | (empty) | (empty — AWX injects) |
| fact_caching | jsonfile | memory | redis |
| forks | 10 | 20 | 25 |
| log_path | ./ansible.log | (empty) | (empty) |
| diff.always | True | True | False |
