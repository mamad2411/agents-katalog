---
name: review-conf
description: Review an ansible.cfg and produce a structured severity report grouped by CRITICAL, WARNING, and INFO. Triggered by /review-conf. Checks for deprecated settings, insecure values, missing critical sections, and vault misconfiguration. NEVER modifies files.
---

# review-conf

Review an ansible.cfg and produce a structured severity report. This command never modifies files.

---

## Required Inputs

1. **path to ansible.cfg** — Resolved from discovery if not provided (checks ANSIBLE_CONFIG env, ./ansible.cfg, ~/.ansible.cfg, /etc/ansible/ansible.cfg in that order)

---

## Behavior

### Step 1 — Discovery
Run discovery per `references/discovery.md`. Locate the ansible.cfg. Report which file will be reviewed.

### Step 2 — Load and Parse
Read and parse the ansible.cfg as an INI file. Identify all sections and key-value pairs.

### Step 3 — Generate Severity Report

```
## ansible.cfg Review: <path>
Reviewed: <timestamp>
Sections found: <list>

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
| vault_password_file world-readable | `vault_password_file` path exists and is readable by others (check permissions) | `[defaults] vault_password_file '<path>' may be world-readable — run: chmod 600 <path>` |
| Inline vault password | `vault_identity_list` contains an inline password (not a file path) | `[defaults] vault_identity_list contains what appears to be an inline password — use a file path instead` |
| Deprecated accelerate | `[accelerate]` section present (removed in ansible-core 2.12) | `[accelerate] Section removed in ansible-core 2.12 — remove this section entirely` |
| forks extremely high | `forks` > 200 | `[defaults] forks=<N> is dangerously high — each fork uses ~100MB RAM, risking OOM on controller` |
| log_path world-writable | `log_path` is set to a world-writable directory (e.g., /tmp/ansible.log without restriction) | `[defaults] log_path '<path>' is in a world-writable directory — logs may contain sensitive data` |

### WARNING

| Check | Condition | Message |
|-------|-----------|---------|
| host_key_checking=False without comment | `host_key_checking = False` with no inline comment justifying it | `[defaults] host_key_checking=False without justification comment — add a comment explaining the context (dev/CI/ephemeral runners)` |
| Missing [privilege_escalation] | `become = True` set in [defaults] but no [privilege_escalation] section | `[defaults] become=True is set but [privilege_escalation] section is absent — add the section for explicit configuration` |
| Callbacks include awx_display manually | `callbacks_enabled` contains `awx_display` | `[defaults] Do not add awx_display to callbacks_enabled — AWX injects it automatically and adding it causes duplicate output` |
| fact_caching_connection has credentials | `fact_caching_connection` contains a password in the URL (redis://:password@...) | `[defaults] fact_caching_connection contains credentials in plaintext — use an environment variable or vault-encrypted value` |
| stdout_callback=debug | `stdout_callback = debug` | `[defaults] stdout_callback=debug produces very verbose output — use yaml or minimal for normal operation` |
| retry_files_enabled=True | `retry_files_enabled = True` (the default) | `[defaults] retry_files_enabled is True (default) — consider setting to False to reduce filesystem noise` |
| Deprecated squash_actions | `squash_actions` key present | `[defaults] squash_actions was removed in ansible-core 2.8 — remove this setting` |
| Deprecated any_errors_fatal at cfg level | `any_errors_fatal` in ansible.cfg (not a valid ansible.cfg setting) | `[defaults] any_errors_fatal belongs in playbooks, not ansible.cfg` |
| Missing collections_path | local collections exist but no collection path is configured | `[defaults] ./collections/ directory exists but collections_path is not configured — add collections_path = ./collections` |
| pipelining disabled | `pipelining = False` or not set | `[ssh_connection] pipelining is disabled — enable it for significant performance improvement (requires Defaults:!requiretty in /etc/sudoers)` |

### INFO

| Check | Condition | Message |
|-------|-----------|---------|
| gathering=implicit | `gathering = implicit` (not smart) | `[defaults] gathering=implicit re-gathers facts on every play — consider smart to use cached facts` |
| forks at default | `forks` not set or = 5 | `[defaults] forks defaults to 5 — increase for large inventories (e.g., forks=20)` |
| No fact caching configured | `fact_caching` not set | `[defaults] Fact caching not configured — consider jsonfile or redis for faster reruns` |
| log_path not set | `log_path` absent | `[defaults] log_path not set — consider enabling for audit trail (rotate with logrotate)` |
| No vault config | Neither `vault_password_file` nor `vault_identity_list` is set | `[defaults] No vault configuration — add vault_password_file or vault_identity_list if using ansible-vault` |
| control_persist not set | `control_persist` absent | `[ssh_connection] control_persist not set — add control_persist=60s for connection reuse` |

---

## Constraints

- **Never modify files.** This command is read-only.
- Parse ansible.cfg as an INI file — do not attempt YAML parsing.
- Report the section and key name for every finding.
- Conclude with: "Use `/ansible-designer:update-conf` to apply fixes."
