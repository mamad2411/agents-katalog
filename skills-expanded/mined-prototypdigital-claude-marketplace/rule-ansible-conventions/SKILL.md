---
name: ansible-conventions
description: Follow Ansible best practices for idempotent, maintainable infrastructure automation.
---

# Ansible conventions

Non-idempotent or unnamed tasks make playbook runs unpredictable: re-runs report false changes, failures are hard to trace, and hardcoded secrets leak into logs and version control. Enforce idempotency in CI with `ansible-lint --profile production`.

## Modules and naming

- Use fully qualified collection names (FQCN): `ansible.builtin.copy` not `copy`.
- Every task must have a descriptive `name:`.
- Avoid `shell` and `command` modules; prefer native modules.
- When `shell`/`command` is unavoidable, always set `changed_when:` and `failed_when:`.

## Idempotency and safety

- Every task must be safe to re-run without changing the system state.
- Use `ansible-lint --profile production` before committing.
- Test with `--check --diff` to verify idempotency.

## Secrets and handlers

- Tasks handling secrets must set `no_log: true`.
- Handlers run only on change; use them for service restarts, not side effects.
- Never hardcode passwords; use `vars_prompt`, vault, or env lookups.

## Role structure

- Follow standard layout: `defaults/`, `tasks/`, `handlers/`, `templates/`, `files/`, `vars/`.
- Define all variables in `defaults/main.yml` with safe defaults.
- Keep tasks in `tasks/main.yml` focused; extract to `tasks/subtask.yml` when >20 lines.

## Jinja2 templating

- Always use `| default()` filter for optional variables to prevent undefined errors.
- Use `| to_json` or `| to_yaml` when embedding structured data.
- Keep logic in tasks; templates render, not compute.
- All referenced variables must be defined in `defaults/` or `group_vars/`.

## Examples

```yaml
# BAD — short module name, no task name, hardcoded password, no changed_when
- copy:
    src: app.conf
    dest: /etc/app/app.conf
- command: echo "password123" | passwd root

# GOOD — FQCN, descriptive name, vault secret, changed_when on command
- name: Deploy application config
  ansible.builtin.copy:
    src: app.conf
    dest: /etc/app/app.conf
    mode: "0644"

- name: Set root password from vault
  ansible.builtin.shell: echo "{{ vault_root_password }}" | passwd root
  changed_when: false
  no_log: true
```
