---
name: ansible-role-testing
description: >
  Test Ansible roles with molecule/docker (or podman), idempotence, ansible-lint, and
  secret-safe fixtures for owned automation repos. Use when adding CI for roles, verifying
  converge/idempotence/verify, or preventing regressions before production apply.
---

# Ansible Role Testing

## Scope And Authorization

- **In scope:** Ansible roles/collections in repos you own; molecule against disposable containers/VMs.
- **Out of scope:** Pointing molecule at production inventory; using real prod secrets in CI logs.
- Prefer containers for unit-like role tests; use staging for full integration.
- Pair with `ansible-vault-usage` and `code-quality-standards`.

## When To Use

- Creating or refactoring an Ansible role.
- Adding GitHub Actions/GitLab CI for `molecule test` / `ansible-lint`.
- Proving idempotence (second converge changes 0).
- Catching template/handler regressions.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Vault encrypt/decrypt workflows | `ansible-vault-usage` |
| Org secrets program | `secrets-management-hygiene` |
| General Linux hardening content | linux hardening skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Stage | Purpose |
| --- | --- |
| `ansible-lint` | Static best practices |
| `molecule create` | Spin test instance |
| `converge` | Apply role |
| `idempotence` | Re-apply; expect no changes |
| `verify` | Assert state (testinfra/goss) |
| `destroy` | Cleanup |

## Workflow

### 1. Confirm role and success criteria

1. Record role path, supported platforms (EL9, Ubuntu 22.04, …), required privileges.
2. Success: lint clean; molecule test green on listed platforms; no secrets in repo; idempotent.
3. List dependencies (roles/collections).

### 2. Scaffold molecule (if missing)

```bash
cd roles/my_role
molecule init scenario -r my_role  # or collection-aware workflow
```

```yaml
# molecule/default/molecule.yml (illustrative)
dependency:
  name: galaxy
driver:
  name: docker
platforms:
  - name: instance
    image: geerlingguy/docker-ubuntu2204-ansible
    pre_build_image: true
provisioner:
  name: ansible
verifier:
  name: ansible
```

### 3. Write converge and verify

```yaml
# molecule/default/converge.yml
- name: Converge
  hosts: all
  roles:
    - role: my_role
```

```yaml
# molecule/default/verify.yml
- name: Verify
  hosts: all
  tasks:
    - name: Check service
      ansible.builtin.command: systemctl is-active myapp
      changed_when: false
```

### 4. Secrets in tests

1. Use dummy passwords in molecule fixtures — never prod vault files.
2. If role requires vault, inject CI secret via env and `ANSIBLE_VAULT_PASSWORD_FILE` pointing to temp file with mode 600.
3. Assert role fails closed when secrets missing if that is desired behavior.

### 5. Run locally and in CI

```bash
ansible-lint roles/my_role
cd roles/my_role && molecule test
# Idempotence alone:
molecule converge && molecule idempotence
```

```yaml
# CI sketch
- run: pip install ansible ansible-lint molecule molecule-plugins[docker]
- run: ansible-lint
- run: molecule test
```

### 6. Multi-platform matrix

1. Add platforms for each supported OS image.
2. Skip tags with `molecule converge -- --skip-tags slow` only when documented.
3. Fail CI on any platform in the support matrix.

### 7. Hand off

1. Document how to run molecule; required collections in `requirements.yml`.
2. Badge/CI required on PRs touching role.
3. Production apply still needs change window — tests reduce risk, not replace judgment.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Target | Ephemeral containers | Prod hosts as molecule driver |
| Idempotence | Enforced in CI | “Run twice manually sometimes” |
| Secrets | Dummy values | Real prod vault in git |
| Verify | Assertions on state | Converge-only smoke |

## Output Checklist

- [ ] Platforms and role path documented
- [ ] ansible-lint clean
- [ ] molecule scenario present
- [ ] converge + idempotence + verify green
- [ ] No real secrets in fixtures
- [ ] CI wired for PRs
- [ ] Collection deps pinned
- [ ] `code-quality-standards` applied

## Rules

- Owned automation only; never test against unapproved fleets.
- Prefer disposable infrastructure for molecule.
- Idempotence is part of the contract.
- Keep vault passwords out of logs.
- Lint + molecule before production apply.
