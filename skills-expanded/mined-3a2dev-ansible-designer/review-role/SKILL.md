---
name: review-role
description: Review an existing Ansible role and produce a structured severity report grouped by CRITICAL, WARNING, and INFO. Triggered by /review-role. Checks directory structure completeness, task FQCN, tag coverage, no_log on secret tasks, defaults vs vars usage, meta/main.yml validity, and handler correctness. NEVER modifies files.
---

# review-role

Review an Ansible role and produce a structured severity report. This command never modifies files.

---

## Required Inputs

1. **role_name or FQCN** — The role to review (resolved from discovery if not provided)

---

## Behavior

### Step 1 — Discovery
Run discovery per `references/discovery.md`. Locate the role:
- By name in `roles_path` directories
- By FQCN in `collections_path` directories

### Step 2 — Load Role
Read all files in the role directory: tasks/, defaults/, vars/, handlers/, meta/, templates/.

### Step 3 — Generate Severity Report

```
## Role Review: <role_name>
Path: <role_path>
Reviewed: <timestamp>
Tasks found: <count>  Handlers: <count>

---

### CRITICAL
[Critical issues]

### WARNING
[Warnings]

### INFO
[Informational notes]

---
Summary: <X> critical, <Y> warnings, <Z> info
```

---

## Checks to Perform

### CRITICAL

| Check | Condition | Message |
|-------|-----------|---------|
| Bare module names | Any task uses module without FQCN | `[tasks/main.yml:line <N>] Task "<name>" uses bare module name '<mod>' — must use FQCN` |
| Missing no_log on secrets | Task has `password:`, `secret:`, `token:`, or references `vault_*` variables without `no_log: true` | `[tasks/main.yml:line <N>] Task "<name>" handles secrets without no_log: true` |
| Deprecated include syntax | Use of bare `include:` | `[tasks/main.yml:line <N>] Deprecated 'include:' — use ansible.builtin.include_tasks or ansible.builtin.import_tasks` |
| Missing tasks/main.yml | The file does not exist | `CRITICAL: tasks/main.yml is missing — role has no entry point` |
| Meta/main.yml missing required fields | galaxy_info is absent or missing author/description/min_ansible_version | `[meta/main.yml] Missing required galaxy_info field: <field>` |

### WARNING

| Check | Condition | Message |
|-------|-----------|---------|
| Untagged tasks | Any task without `tags:` | `[tasks/main.yml:line <N>] Task "<name>" has no tags — add component name + action category` |
| vars/ used for overridable values | Variable in vars/main.yml that clearly should be in defaults/ (e.g., port, version) | `[vars/main.yml] Variable '<var>' looks like an operator-overridable default — consider moving to defaults/main.yml` |
| defaults/ used for internal constants | Variable in defaults/main.yml with underscore prefix or clearly internal | `[defaults/main.yml] Variable '<var>' looks like an internal constant — consider moving to vars/main.yml` |
| Missing directory | Standard dir (files/, templates/, handlers/) absent | `Directory '<dir>/' is missing from role structure (not required but recommended)` |
| Handler not referenced | Handler defined in handlers/main.yml but no task calls `notify:` for it | `[handlers/main.yml] Handler '<name>' is defined but never notified by any task` |
| Orphaned notify | Task notifies a handler name that doesn't exist in handlers/main.yml | `[tasks/main.yml:line <N>] Task notifies '<name>' but no handler with that name/listen exists` |
| Shell/command without idempotency | `ansible.builtin.shell` or `ansible.builtin.command` without `creates:`, `removes:`, or `changed_when:` | `[tasks/main.yml:line <N>] Task "<name>" uses shell/command without idempotency guard` |
| meta/main.yml: min_ansible_version not set | `min_ansible_version` absent | `[meta/main.yml] min_ansible_version not set — recommend setting to "2.15"` |

### INFO

| Check | Condition | Message |
|-------|-----------|---------|
| No tests/ directory | tests/ absent | `No tests/ directory found — consider adding tests/test.yml for smoke testing` |
| No validation guidance | role has example content but no clear smoke-test path | `Add tests/test.yml or README validation guidance aligned with references/testing.md` |
| No README.md | Role has no README | `Role is missing a README.md — document variables, dependencies, and usage` |
| tasks/main.yml lacks assertions | No `ansible.builtin.assert` in tasks/main.yml | `Consider adding an assert to validate minimum Ansible version or required variables` |
| Templates not validated | `ansible.builtin.template` task without `validate:` parameter | `[tasks/main.yml:line <N>] Template task for <dest> could use 'validate:' to verify syntax before deployment` |

---

## Constraints

- **Never modify files.** This command is read-only.
- Do not generate a "fixed" version of any file.
- Do not suggest sed/awk commands.
- Conclude with: "Use `/ansible-designer:update-role` to apply fixes."
