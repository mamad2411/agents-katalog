---
name: ansible-preflight
description: Pre-deployment validation for Ansible changes targeting the Proxmox home-lab cluster — catches common mistakes before they become fix commits
when_to_use: |
  Use this skill when the user:
  - Is about to commit or run Ansible changes (roles, playbooks, inventory, group_vars, host_vars)
  - Asks to validate, lint, check, or preflight any YAML in the ansible/ directory
  - Has modified any role task, template, or defaults file
  - Is adding a new role or playbook to the cluster
  - Wants a dry-run before applying changes to the live Proxmox cluster
  - Says "preflight", "validate", "check before deploying", "dry run"
---

# Ansible Preflight Validation

You are helping validate Ansible changes for the **olympus** Proxmox cluster before they are deployed. The goal is to catch errors that historically required follow-up fix commits.

Always run validation from the `ansible/` directory with vault password available:

```bash
cd /path/to/home-lab/ansible
```

## Step 1: Syntax Check

Run syntax-only validation (no connection required):

```bash
ansible-playbook --syntax-check -i inventory/hosts.yml proxmox_cluster.yml \
  --vault-password-file ~/.vault_pass.txt

ansible-playbook --syntax-check -i inventory/hosts.yml service_vms.yml \
  --vault-password-file ~/.vault_pass.txt

ansible-playbook --syntax-check -i inventory/hosts.yml openclaw_cluster.yml \
  --vault-password-file ~/.vault_pass.txt
```

For a specific role or tag only:
```bash
ansible-playbook --syntax-check -i inventory/hosts.yml proxmox_cluster.yml \
  --tags <role_name> --vault-password-file ~/.vault_pass.txt
```

## Step 2: Lint Check

Run ansible-lint for best-practice violations:

```bash
cd ansible && uv run ansible-lint roles/<role_name>/
uv run ansible-lint playbooks/
```

Key lint rules to pay attention to:
- `no-changed-when` — shell/command tasks without `changed_when`
- `risky-shell-pipe` — shell commands piped without `pipefail`
- `no-free-form` — using free-form module args instead of structured YAML
- `fqcn-builtins` — using short names (e.g. `copy`) instead of FQCN (`ansible.builtin.copy`)

## Step 3: Dry Run (Check Mode)

Test against live hosts without making changes:

```bash
# Full playbook dry-run with diff output
ansible-playbook --check --diff -i inventory/hosts.yml proxmox_cluster.yml \
  --vault-password-file ~/.vault_pass.txt --tags <role>

# Single host dry-run
ansible-playbook --check --diff -i inventory/hosts.yml proxmox_cluster.yml \
  --limit r420.infiquetra.com --vault-password-file ~/.vault_pass.txt
```

**Note**: Check mode does not work reliably for tasks that use `delegate_to`, `run_once`, or pvecm/pveceph CLI commands — these will show as "skipped" in check mode even though they have real effects.

## Step 4: Variable Resolution Check

Verify variables are resolved before referencing them:

```bash
# Print all variables for a host (catches undefined vars before runtime)
ansible -i inventory/hosts.yml r420.infiquetra.com -m debug \
  -a "var=hostvars[inventory_hostname]" --vault-password-file ~/.vault_pass.txt
```

For template validation, test Jinja2 rendering:
```bash
ansible -i inventory/hosts.yml all -m debug \
  -a "msg={{ your_variable }}" --vault-password-file ~/.vault_pass.txt
```

## Step 5: Common Mistakes Check

Before finalizing, review the common mistakes catalog (`references/common-mistakes.md`) and manually verify the change doesn't exhibit any of the known patterns extracted from the fix commit history.

## Quick Preflight Checklist

When reviewing Ansible changes, check:

- [ ] `become: true` on all tasks that run as root (pvecm, pveceph, ceph, systemctl)
- [ ] `delegate_to: "{{ proxmox_master }}"` on all cluster-wide operations (pvecm join, ceph init)
- [ ] `run_once: true` paired with `delegate_to` when creating global resources
- [ ] `serial: 1` on node-join and OSD-add plays (prevents race conditions)
- [ ] `when: not ansible_check_mode` on tasks that can't run in check mode
- [ ] `changed_when: false` or `changed_when: result.rc != 0` on shell/command tasks
- [ ] `ignore_errors: false` — only use `ignore_errors: true` when genuinely OK to fail
- [ ] Variable defaults in `defaults/main.yml` for every variable used in tasks
- [ ] Idempotency: re-running the role should not change state if already applied
- [ ] Vault variables referenced as `{{ vault_var }}` exist in the encrypted vault file
