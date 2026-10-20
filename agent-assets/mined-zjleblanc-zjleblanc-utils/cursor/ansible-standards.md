---
description: Standards for Ansible collections, roles, and playbooks to ensure best practices and ansible-lint compliance.
globs: "**/*.{yml,yaml}", "galaxy.yml", "meta/runtime.yml"
alwaysApply: false
---

# Ansible Standards

## Best Practices

### Role Variables
Variables registered within a role MUST be prefixed with the role name to avoid namespace collisions and comply with `var-naming[no-role-prefix]`.

```yaml
# ❌ BAD
- name: Check status
  ansible.builtin.command: check_status
  register: r_status

# ✅ GOOD
- name: Check status
  ansible.builtin.command: check_status
  register: my_role_status
```

### Collection Versions
- In `galaxy.yml`, use `semantic_version` as a placeholder for CI-driven versioning.
- Always configure `.ansible-lint` to skip `galaxy[version]` and `schema[galaxy]` when using this placeholder.
- Enable `offline: true` in `.ansible-lint` to prevent fatal errors during dependency resolution in restricted environments.

### Supported Versions
- Ensure `meta/runtime.yml` specifies a currently supported Ansible version (e.g., `>=2.15.0`).
- Role metadata in `meta/main.yml` should use quoted strings for `min_ansible_version`.

```yaml
# ✅ GOOD (meta/main.yml)
galaxy_info:
  min_ansible_version: "2.15.0"
```

### Formatting
- No trailing spaces in YAML files.
- Always include a newline at the end of files.
- Use proper Jinja2 spacing: `{{ variable | filter }}`.
