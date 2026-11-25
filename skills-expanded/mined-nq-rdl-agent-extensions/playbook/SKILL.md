---
license: CC-BY-4.0
description: >-
  Write, review, and debug Ansible content: playbooks, roles, inventories,
  group_vars/host_vars, Jinja2 templates, collections (requirements.yml,
  FQCN), ansible-vault secrets, and ansible-navigator runs. Use when the user
  mentions Ansible or these files, asks to scaffold a role or fix a failed
  play, or uses a layered playbook layout (layer1_*, layer2_*). Not for
  Puppet, Chef, or Salt.
compatibility: >-
  Requires Python 3.11+, ansible-core 2.16+, ansible-lint 24.0+
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Ansible Skill

Write, modify, debug, and optimise Ansible content.

When you create, scaffold, or restructure a role, read
[references/role-reference.rst](references/role-reference.rst) (role layout,
defaults vs vars, meta, handlers, templates). Playbook, inventory, variable,
and single-task work does not need it.

## Dependencies

The user's project should have these installed (via pip, pipx, pixi, or devcontainer):

| Package | Version | Purpose |
|---------|---------|---------|
| `ansible-core` | >= 2.16 | Playbook execution, modules |
| `ansible-lint` | >= 24.0 | Linting playbooks and roles |
| `jmespath` | >= 1.0 | `json_query` filter support |
| `ansible-navigator` | latest | Local execution and testing (optional, often provided by devcontainer) |

```bash
# Lint a playbook or role
ansible-lint playbooks/site.yml

# Syntax check without a live inventory
ansible-playbook --syntax-check playbooks/site.yml -i localhost,

# Install collections from requirements.yml
ansible-galaxy collection install -r requirements.yml
```

## Core Principles

These aren't arbitrary rules — they reflect how the team actually works and what keeps
production stable.

### FQCN Everywhere

Always use fully qualified collection names. Never use short module names. The team uses
`ansible-core` with collections installed via `requirements.yml`, and FQCN prevents ambiguity
and makes collection dependencies explicit.

```yaml
# Correct
- ansible.builtin.dnf:
    name: chrony
    state: present

# Wrong — never do this
- dnf:
    name: chrony
    state: present
```

### Lean Role Structure

Only create directories that contain files. An empty `vars/` or `meta/` directory is noise.
A role with only tasks needs only `tasks/`. Grow the structure as the role's needs grow.

A minimal role is just:
```
roles/my_role/
└── tasks/
    └── main.yml
```

A role with configuration templates and tuneable defaults expands to:
```
roles/my_role/
├── defaults/
│   └── main.yml
├── handlers/
│   └── main.yml
├── tasks/
│   └── main.yml
└── templates/
    └── my_config.j2
```

See [references/role-reference.rst](references/role-reference.rst) for the full pattern.

### Task Splitting by Concern

When a role does more than one logical thing, split tasks into focused files and delegate
from `main.yml`. This keeps diffs reviewable and lets team members reason about changes
in isolation.

```yaml
# roles/vm_configure/tasks/main.yml
---
- name: Configure system packages
  ansible.builtin.import_tasks: packages.yml

- name: Configure NTP via chrony
  ansible.builtin.import_tasks: chrony.yml

- name: Configure SELinux policies
  ansible.builtin.import_tasks: selinux.yml
```

Use `import_tasks` for static inclusion (the default). Use `include_tasks` only when you
need conditional or looped inclusion at runtime.

### Layered Playbook Architecture

Playbooks are organised in numbered layers that run in dependency order, with a `site.yml`
that orchestrates the full stack and a `preflight_checks.yml` gate that validates prerequisites
before any changes.

```
playbooks/
├── site.yml                  # Orchestrator — imports layers in order
├── preflight_checks.yml      # Validation gate — runs first
├── layer1_hypervisor.yml     # Physical host / hypervisor setup
├── layer2_vm_config.yml      # VM-level OS configuration
└── layer3_application.yml    # Application-layer setup (example)
```

New playbooks should follow this layering convention. If a playbook doesn't fit a layer,
it gets a descriptive name (not a number).

### Test-Before-Apply Pattern

When a play modifies critical system state, prefer a two-phase approach:

1. **Check mode first** — Run with `--check --diff` to preview changes
2. **Apply with verification** — Run the actual play, then verify the outcome with a
   dedicated validation task or a subsequent preflight check

For handlers that restart services, include a verification step:

```yaml
handlers:
  - name: Restart chronyd
    ansible.builtin.systemd:
      name: chronyd
      state: restarted
    notify: Verify chronyd

  - name: Verify chronyd
    ansible.builtin.command:
      cmd: chronyc tracking
    changed_when: false
    register: chrony_verify
    failed_when: "'Leap status     : Normal' not in chrony_verify.stdout"
```

### Rollback Awareness

Roles that modify system state should, where practical, capture the prior state and
provide a tagged rollback path. This isn't always possible (you can't un-apply an SELinux
policy trivially), but when it is — especially for configuration file changes — include it.

```yaml
- name: Backup existing config
  ansible.builtin.copy:
    src: /etc/chrony.conf
    dest: /etc/chrony.conf.ansible-backup
    remote_src: true
  tags: [chrony, rollback-prep]
```

## Inventory Conventions

The team uses static YAML inventories structured per environment:

```
inventories/
└── production/
    ├── hosts.yml
    ├── group_vars/
    │   ├── all.yml
    │   └── <group_name>.yml
    └── host_vars/
        └── <hostname>.yml
```

- One file per host in `host_vars/`
- Group variables scoped to the narrowest applicable group
- `all.yml` for truly global settings (DNS, NTP servers, proxy config, etc.)
- Hostnames follow organisational naming conventions (e.g., `thhs-p-rdl01`)

## Secrets Management

### Ansible Vault (Primary)

Use Ansible Vault for encrypting sensitive variables. Prefer encrypting individual
variables with `ansible-vault encrypt_string` over encrypting entire files — it keeps
diffs meaningful and lets team members see which variables exist even if they can't
read the values.

```yaml
# group_vars/all.yml
proxy_password: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  ...encrypted content...
```

### HashiCorp Vault (When Needed)

For secrets that need centralised lifecycle management or are shared across non-Ansible
systems, use the `community.hashi_vault` collection lookup plugin:

```yaml
- name: Retrieve database password
  ansible.builtin.set_fact:
    db_password: "{{ lookup('community.hashi_vault.hashi_vault',
      'secret/data/myapp:db_password',
      url='https://vault.example.com') }}"
  no_log: true
```

Always set `no_log: true` on tasks that handle secrets retrieved from Vault.

## Local Development Tooling

The team's local development workflow:

- **`.devcontainer`** provides a consistent development environment across the team
- **`ansible-navigator`** for local execution and testing (stdout mode for quick runs,
  interactive mode for debugging)

When suggesting commands for local execution, prefer `ansible-navigator run` over
`ansible-playbook` directly:

```bash
# Local execution via navigator
ansible-navigator run playbooks/site.yml -i inventories/production/hosts.yml --mode stdout

# Syntax check
ansible-navigator run playbooks/site.yml --syntax-check --mode stdout

# Check mode (dry run)
ansible-navigator run playbooks/site.yml -i inventories/production/hosts.yml --check --diff --mode stdout
```

## Common Module Patterns

Key module choices for common infrastructure tasks:

- **Package management**: `ansible.builtin.dnf` or `ansible.builtin.apt` depending on OS family;
  use `ansible_pkg_mgr` fact or `when: ansible_os_family == 'RedHat'` guards to handle both
- **Services**: `ansible.builtin.systemd` for systemd-managed services; `ansible.builtin.service`
  as a portable fallback when the init system varies across targets
- **Firewall**: `ansible.posix.firewalld` for firewalld-based distros; `ansible.builtin.iptables`
  or `community.general.ufw` for others
- **SELinux**: `ansible.posix.seboolean`, `ansible.posix.selinux` for policy;
  `community.general.sefcontext` for file contexts — guard with `when: ansible_selinux.status == 'enabled'`
- **NTP**: template the daemon config file (e.g., `/etc/chrony.conf` or `/etc/ntp.conf`) rather
  than modifying it in-place; use `ansible.builtin.template` + handler to restart the service
- **Users and groups**: `ansible.builtin.user`, `ansible.builtin.group`; prefer `uid`/`gid`
  pinning for consistency across hosts

## Collection Dependencies

Any collection beyond `ansible.builtin` must be declared in `requirements.yml` at the project
root. FQCN usage makes these dependencies visible — if a task uses `ansible.posix.firewalld`,
the reader knows `ansible.posix` must be installed.

```yaml
# requirements.yml
---
collections:
  - name: ansible.posix
    version: ">=1.5"
  - name: community.general
    version: ">=8.0"
  - name: community.hashi_vault
    version: ">=6.0"
```

Install collections into the project (not user-global):

```bash
ansible-galaxy collection install -r requirements.yml -p ./collections
```

Then configure `ansible.cfg` to pick up the local collections path:

```ini
[defaults]
collections_path = ./collections
```

This keeps the collection versions pinned per-project and avoids system-wide installs polluting
other projects on the same machine.

## Writing Style for Ansible Content

- **Task names are mandatory** and should read as imperative sentences:
  `"Install required packages"`, `"Configure chrony NTP sources"`, `"Enable and start firewalld"`
- **Comments sparingly** — task names carry the narrative; comments explain *why*, not *what*
- **Consistent YAML style** — 2-space indent, no trailing whitespace, blank line between tasks
- **Tags** — use them for layer/role/concern grouping, not for individual tasks
- **`become: true`** at the play level when the entire play needs privilege, not per-task
