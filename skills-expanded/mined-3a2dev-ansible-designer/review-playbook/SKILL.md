---
name: review-playbook
description: Review an existing Ansible playbook and produce a structured severity report grouped by CRITICAL, WARNING, and INFO. Triggered by /review-playbook. Checks FQCN usage, idempotency patterns, no_log on secret tasks, tag coverage, deprecated syntax, become usage, and style consistency. NEVER modifies files.
---

# review-playbook

Review an Ansible playbook and produce a structured severity report. This command never modifies files.

---

## Required Inputs

1. **path + filename** — Path to the playbook to review (resolved from discovery if not provided)

---

## Behavior

### Step 1 — Discovery
Run discovery per `references/discovery.md`. Use context to:
- Locate the playbook if only a filename is given (search in `./`, `./playbooks/`)
- Identify available roles/collections for FQCN verification

### Step 2 — Load and Analyze
Read the playbook file. Analyze every task, handler reference, role include, and play-level attribute.

### Step 3 — Generate Severity Report

Produce a structured report in this exact format:

```
## Playbook Review: <filename>
Reviewed: <timestamp>
Plays: <count>  Tasks: <count>  Roles: <count>

---

### CRITICAL
[List of critical issues — must fix before use in production]

### WARNING
[List of warnings — should fix; may cause problems under certain conditions]

### INFO
[Informational suggestions — best practices, performance hints]

---
Summary: <X> critical, <Y> warnings, <Z> info
```

If there are no issues in a severity level, show: `No issues found.`

---

## Checks to Perform

### CRITICAL checks

| Check | What to look for | Message format |
|-------|-----------------|----------------|
| Bare module names | Any task using a module without FQCN prefix | `[tasks:<line>] Task "<name>" uses bare module name '<module>' — must use FQCN '<ansible.builtin.module>'` |
| Missing no_log on secrets | Tasks with `password:`, `secret:`, `token:`, `key:` arguments, or tasks referencing `vault_*` variables, without `no_log: true` | `[tasks:<line>] Task "<name>" handles secret data (parameter: <param>) but is missing no_log: true` |
| Deprecated `include:` | Use of bare `include:` (removed in ansible-core 2.12) | `[tasks:<line>] Deprecated: 'include:' has been removed. Use 'ansible.builtin.include_tasks:' or 'ansible.builtin.import_tasks:'` |

### WARNING checks

| Check | What to look for | Message format |
|-------|-----------------|----------------|
| Untagged tasks | Any task without a `tags:` block | `[tasks:<line>] Task "<name>" has no tags — add at minimum component name + action category` |
| Shell/command without idempotency | `ansible.builtin.shell` or `ansible.builtin.command` without `creates:`, `removes:`, or `changed_when:` | `[tasks:<line>] Task "<name>" uses shell/command without idempotency guard (creates/removes/changed_when)` |
| Both play-level and task-level become | `become: true` set at play level AND again on individual tasks | `[play:<name>] 'become: true' is set at play level; remove redundant task-level become declarations` |
| Missing gather_facts declaration | Play with no explicit `gather_facts:` | `[play:<name>] gather_facts not explicitly set — add 'gather_facts: true' or 'gather_facts: false'` |
| Deprecated `include_role` without `name:` | `ansible.builtin.include_role` without explicit `name:` key | `[tasks:<line>] include_role missing explicit 'name:' key` |
| `ignore_errors: true` without justification | `ignore_errors: true` without adjacent comment explaining why | `[tasks:<line>] Task "<name>" uses ignore_errors: true without explanation — add a comment justifying this` |

### INFO checks

| Check | What to look for | Message format |
|-------|-----------------|----------------|
| Missing playbook header | No YAML comment header with author/version | `Playbook is missing a documentation header (author, version, description)` |
| No pre_tasks assertion | First play has no version/OS assertion | `Consider adding an ansible.builtin.assert in pre_tasks to verify minimum Ansible version or OS compatibility` |
| No post_tasks validation | Play has roles but no validation post_task | `Consider adding a validation post_task (wait_for, uri) to confirm deployment success` |
| No documented validation path | Example-style playbook has no clear validation task or surrounding test guidance | `Consider adding validation tasks or README guidance aligned with references/testing.md` |
| Long play without serial | Play targeting more than one group without `serial:` | `Play '<name>' targets multiple host groups without serial — consider serial: 1 for rolling updates` |
| Hard-coded IP addresses | Any IP address literal in the playbook | `[tasks:<line>] Hard-coded IP address '{{ ip }}' — use inventory variables or DNS names instead` |

---

## Example Output

```
## Playbook Review: deploy-app.yml
Reviewed: 2026-03-31T10:00:00
Plays: 2  Tasks: 8  Roles: 2

---

### CRITICAL
- [play:Deploy application, tasks:line 15] Task "Restart app service" uses bare module name 'service' — must use FQCN 'ansible.builtin.service'
- [play:Deploy application, tasks:line 22] Task "Set admin password" handles secret data (parameter: password) but is missing no_log: true

### WARNING
- [play:Deploy application, tasks:line 18] Task "Run migration script" uses ansible.builtin.shell without idempotency guard (creates/removes/changed_when)
- [play:Deploy application, tasks:line 31] Task "Copy config file" has no tags — add at minimum component name + action category

### INFO
- Playbook is missing a documentation header (author, version, description)
- Consider adding a validation post_task (wait_for, uri) to confirm deployment success

---
Summary: 2 critical, 2 warnings, 2 info
```

---

## Constraints

- **Never modify files.** This command is read-only.
- Do not suggest `sed` or `awk` commands to fix issues.
- Do not generate "fixed" versions of the playbook.
- Conclude with: "Use `/ansible-designer:update-playbook` to apply fixes."
