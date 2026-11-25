---
name: update-role
description: Update an existing Ansible role. Triggered by /update-role. Reads specific role files, applies the requested change following all global rules (FQCN, tags, no_log), shows a unified diff per file, waits for explicit user confirmation, then writes. Never overwrites silently.
---

# update-role

Update one or more files in an existing Ansible role. Always shows a diff and waits for confirmation before writing.

---

## Required Inputs

1. **role_name or FQCN** — The role to update (resolved from discovery)
2. **change_description** — What to change (e.g., "add Windows support", "fix bare module names in tasks/main.yml", "add SELinux task to RedHat.yml")

---

## Behavior

### Step 1 — Discovery
Locate the role via discovery (`references/discovery.md`).

### Step 2 — Load Target Files
Read only the files relevant to the requested change. If the change affects multiple files (e.g., "add multi-OS support"), read all affected files.

### Step 2a — Secret Scan (before any output)
Before displaying any content or diff — especially for `defaults/main.yml`, `vars/*.yml`, and `group_vars/` files — scan every loaded file for credential-like values:
- Match lines or YAML values where the key contains `password`, `secret`, `token`, `api_key`, `private_key`, `pass`, or `credential`
- **Skip** lines where the value is already a vault reference (`{{ vault_* }}`), a task option (`no_log`, `register`, `when`), empty, or `None`
- For any remaining matches, **redact the value** in all output: `db_password: "***REDACTED***"`
- Emit a warning at the top of each affected file's diff block:
  ```
  ⚠ Warning: N line(s) with credential-like values were redacted from this display.
    Review the file directly before applying changes.
  ```
- Never output actual credential values in diffs, summaries, or confirmations.

### Step 3 — Apply Change
Apply the requested change to the relevant files:
- Preserve existing structure, indentation style, and comments
- All modules use FQCN
- All new tasks have tags (role_name + action category)
- `no_log: true` on any new task handling secrets per `references/security_vault.md`
- Use templates from `references/role.md` for any new blocks
- Keep tests and smoke-playbook updates aligned with `references/testing.md`

### Step 4 — Show Unified Diff (per file)
For each modified file, show the diff:

```
--- roles/nginx/tasks/main.yml (original)
+++ roles/nginx/tasks/main.yml (proposed)
@@ -12,6 +12,12 @@
   tags:
     - nginx
     - configure
+
+- name: Open firewall port for nginx
+  ansible.posix.firewalld:
+    port: "{{ nginx_port }}/tcp"
+    permanent: true
+    state: enabled
+    immediate: true
+  tags:
+    - nginx
+    - security
```

Then ask: **"Apply these changes? (yes/no)"**

### Step 5 — Write on Confirmation
- If **yes**: write all modified files.
- If **no**: ask what to change and loop back to Step 3.

### Step 6 — Final Output
Show file tree of the updated role:
```bash
find "roles/<role_name>" -type f | sort
```

Suggest next step:
```
Next step: Run `ansible-lint roles/<role_name>/` to validate
           or use /ansible-designer:review-role to re-check for remaining issues.
```

---

## Change Types Supported

| Change requested | Files to modify | How to handle |
|-----------------|-----------------|---------------|
| Add task | tasks/main.yml (or OS-specific task file) | Insert task with FQCN, tags, no_log if needed |
| Remove task | tasks/main.yml | Remove task block; check for orphaned handlers |
| Add multi-OS support | tasks/main.yml, tasks/RedHat.yml, tasks/Solaris.yml, tasks/Windows.yml, vars/RedHat.yml, vars/Solaris.yml, vars/Windows.yml | Add OS detection block + generate OS task/var files |
| Fix bare module names | tasks/main.yml, handlers/main.yml | Replace all bare module names with FQCN |
| Add tags | tasks/main.yml | Add missing tags to untagged tasks |
| Add handler | handlers/main.yml | Append handler with FQCN, add notify to triggering task |
| Update defaults | defaults/main.yml | Add/modify default variable |
| Update meta | meta/main.yml | Modify galaxy_info fields (platforms, version, etc.) |
| Add Windows support | tasks/Windows.yml (create), vars/Windows.yml (create), tasks/main.yml (update) | Generate Windows task file; add OS detection to main.yml |
| Add Solaris support | tasks/Solaris.yml (create), vars/Solaris.yml (create), tasks/main.yml (update) | Generate Solaris SMF task file; add OS detection to main.yml |

---

## Safety Rules

- Never remove tasks unless explicitly requested.
- Never change the role name or its meta role_name field without explicit request.
- Preserve all existing comments.
- If adding OS support to an existing role that already has tasks in main.yml: do NOT remove those tasks. Wrap existing platform-independent tasks to remain in main.yml and move platform-specific tasks to the OS files.
- If the change would break backward compatibility (e.g., removing a defaults variable), warn before asking for confirmation.
