---
name: idempotency
description: Every operation — task, script, or deployment — must be safe to re-run without side effects.
---

# Idempotency

Every infrastructure operation must be safe to re-run. Running the same task, script, or apply twice must leave the system in the same state as running it once.

## Principles

- **State-based, not action-based:** check desired state before making changes; don't assume the current state.
- **No side effects on re-run:** scripts should not fail or corrupt state when run a second time.
- **Convergence:** repeated runs should converge to the desired state, even if the system starts partially configured.

## Ansible

- Use `state: present` / `state: absent` modules instead of `shell` commands.
- When `shell`/`command` is unavoidable, use `creates:` or `changed_when: false` to prevent repeated runs from reporting false changes.
- Never use `command: rm -rf /path` — use `file: path=/path state=absent`.

## Terraform

- All resources must be fully declarative; avoid `local-exec` and `null_resource` unless unavoidable.
- When `local-exec` is used, guard it with `triggers` to prevent re-execution.
- Use `lifecycle.create_before_destroy` for zero-downtime replacement.

## Shell scripts

- Check if work is needed before doing it: `[ -f /path ] || create_it`.
- Use `mkdir -p` not `mkdir`; use `cp -f` not `cp` for idempotent file ops.
- Clean up temp files even on failure with `trap 'rm -f /tmp/work' EXIT`.

## Docker Compose

- Use named volumes with explicit mounts; never rely on anonymous volume state.
- Service names are stable; renaming a service breaks `docker compose down` on old containers.

## Examples

```yaml
# BAD — Ansible: shell command that fails on second run; not idempotent
- name: Create app directory
  ansible.builtin.command: mkdir /opt/app

# GOOD — Ansible: state-based module; safe to re-run
- name: Ensure app directory exists
  ansible.builtin.file:
    path: /opt/app
    state: directory
    mode: "0755"
```

```sh
# BAD — shell script: mkdir fails if directory already exists
mkdir /tmp/workspace
cp config.json /tmp/workspace/

# GOOD — shell script: idempotent file operations
mkdir -p /tmp/workspace
cp -f config.json /tmp/workspace/
```
