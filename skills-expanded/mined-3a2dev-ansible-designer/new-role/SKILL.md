---
name: new-role
description: Scaffold a complete Ansible role. Triggered by /new-role. Resolves role location from FQCN or path, asks whether multi-OS support is needed (RHEL, Solaris, Windows/WinRM), and generates a full role directory structure with realistic starter tasks, handlers, defaults, meta/main.yml, and OS-specific var files if requested. Shows summary before writing.
---

# new-role

Scaffold a complete Ansible role following the standard directory structure and production conventions.

---

## Required Inputs

Collect these parameters (one at a time, using discovery context for defaults):

1. **role_name** — The role name (e.g., `nginx`, `postgres`, `ntp`)
2. **location** — One of:
   - **role_path**: Directory to create the role in (e.g., `./roles/`, default from discovery `roles_path`)
   - **FQCN**: `namespace.collection.role` (e.g., `myorg.infra.nginx`) → creates role inside the collection
3. **multi_os** — MANDATORY question: "Does this role need multi-OS support? (RHEL / Solaris / Windows/WinRM) [yes/no]"
4. **description** — Brief role description for meta/main.yml

---

## FQCN Resolution

When the user provides a FQCN (`namespace.collection.role`):
1. Look in `./collections/ansible_collections/<namespace>/<collection>/roles/`
2. Also check `collections_path` entries from ansible.cfg
3. If the collection exists: create the role inside it
4. If the collection does not exist: warn and ask if the user wants to use `/ansible-designer:new-collection` first, or create the role standalone

---

## Multi-OS Question (MANDATORY)

Always ask this question — never skip it:

```
Does this role need multi-OS support?
  1. No — single platform (Linux/RHEL only)
  2. Yes — RHEL + Solaris + Windows/WinRM

Enter 1 or 2:
```

**If single-platform (option 1):** Generate standard role structure without OS var files.

**If multi-OS (option 2):** Generate:
- `vars/RedHat.yml`
- `vars/Solaris.yml`
- `vars/Windows.yml`
- `tasks/RedHat.yml`
- `tasks/Solaris.yml`
- `tasks/Windows.yml`
- OS detection block in `tasks/main.yml` using `ansible.builtin.include_vars` with `with_first_found`

---

## Files to Generate

### Single-platform role

```
roles/<role_name>/
├── defaults/main.yml
├── files/               (empty directory — create .gitkeep)
├── handlers/main.yml
├── meta/main.yml
├── tasks/main.yml
├── templates/           (empty directory — create .gitkeep)
├── tests/inventory
├── tests/test.yml
└── vars/main.yml
```

### Multi-OS role (additional files)

```
roles/<role_name>/
└── tasks/
    ├── main.yml          (with OS detection + include_vars)
    ├── RedHat.yml
    ├── Solaris.yml
    └── Windows.yml
└── vars/
    ├── main.yml
    ├── RedHat.yml
    ├── Solaris.yml
    └── Windows.yml
```

---

## Content Requirements

Use `references/role.md` as the base for all generated content.

### tasks/main.yml must include
- At least 3 realistic tasks for the named role (not generic "Install package" — use the actual component)
- FQCN for all modules
- Tags on every task (role_name + action category)
- `no_log: true` on any task that handles secrets or passwords per `references/security_vault.md`
- For multi-OS: OS detection block at the top using `ansible.builtin.include_vars` + `with_first_found`
- Include a smoke-test path aligned with `references/testing.md`

### defaults/main.yml must include
- Port number
- Package version pin
- Log directory
- Enable/disable feature flag
- At least 5 role-specific defaults (derive from role name)

### handlers/main.yml must include
- Reload handler
- Restart handler
- Both with FQCN module

### meta/main.yml must include
- Complete `galaxy_info` block
- Platforms: EL 8/9 (always); Solaris 11.4 and Windows 2019/2022 (if multi-OS)
- `min_ansible_version: "2.15"`

---

## Step 3 — Pre-Write Confirmation

Show summary:
```
Will create: ./roles/nginx/ (12 files)

  defaults/main.yml     — nginx port, worker count, log dir, SSL toggle
  handlers/main.yml     — Reload nginx, Restart nginx
  meta/main.yml         — galaxy_info: platforms EL 8/9, Solaris 11.4, Windows 2019/2022
  tasks/main.yml        — OS detection + 3 common tasks
  tasks/RedHat.yml      — RHEL: dnf install, firewalld, SELinux boolean
  tasks/Solaris.yml     — Solaris: pkgadd, svcadm enable
  tasks/Windows.yml     — Windows: win_package install, win_service
  vars/main.yml         — internal constants
  vars/RedHat.yml       — RHEL: package=nginx, service=nginx, config=/etc/nginx
  vars/Solaris.yml      — Solaris: package=SUNWnginx, smf_fmri=svc:/network/nginx
  vars/Windows.yml      — Windows: service_name="nginx", install_dir="C:\nginx"
  tests/test.yml        — smoke test playbook

Proceed? (yes/no)
```

---

## Step 5 — Final Output

Show file tree:
```bash
find roles/<role_name> -type f | sort
```

Suggest next step:
```
Next step: Run `ansible-lint roles/<role_name>/` to validate
           or use /ansible-designer:review-role for a structured review.
           To use in a playbook, run /ansible-designer:new-playbook.
```
