---
name: update-playbook
description: Update an existing Ansible playbook. Triggered by /update-playbook. Reads the target file, applies the requested change following all global rules (FQCN, tags, no_log), shows a unified diff, waits for explicit user confirmation, then writes. Never overwrites silently.
---

# update-playbook

Update an existing Ansible playbook with a specific change. Always shows a diff and waits for confirmation before writing.

---

## Required Inputs

1. **path + filename** — Path to the playbook to modify (resolved from discovery if not provided)
2. **change_description** — What to change (e.g., "add a post_task to validate nginx", "replace the service module calls with FQCN", "add tags to all tasks")

---

## Behavior

### Step 1 — Discovery
Run discovery per `references/discovery.md` to locate the target file if only a filename is given.

### Step 2 — Load Existing File
Read the full content of the target playbook.

### Step 2a — Secret Scan (before any output)
Before displaying any content or diff, scan the loaded file for credential-like values:
- Match lines or YAML values where the key contains `password`, `secret`, `token`, `api_key`, `private_key`, `pass`, or `credential`
- **Skip** lines where the value is already a vault reference (`{{ vault_* }}`), a task option (`no_log`, `register`, `when`), empty, or `None`
- For any remaining matches, **redact the value** in all output: `password: "***REDACTED***"`
- Emit a warning at the top of the diff block:
  ```
  ⚠ Warning: N line(s) with credential-like values were redacted from this display.
    Review the file directly before applying changes.
  ```
- Never output actual credential values in diffs, summaries, or confirmations.

### Step 3 — Apply Change
Apply the requested change following all global rules:
- All modules use FQCN
- All tasks have tags (component + action category)
- `no_log: true` on any task handling secrets per `references/security_vault.md`
- Preserve existing structure, indentation style, and header
- Preserve all existing functionality — only change what was requested
- Use templates from `references/playbook.md` for any new blocks added
- Keep validation changes aligned with `references/testing.md`

### Step 4 — Show Unified Diff
Display the diff in unified format:

```
--- deploy-nginx.yml (original)
+++ deploy-nginx.yml (proposed)
@@ -15,7 +15,10 @@
   roles:
     - role: myorg.infra.nginx

+  post_tasks:
+    - name: Confirm nginx is listening
+      ansible.builtin.wait_for:
+        host: "{{ ansible_host }}"
+        port: "{{ nginx_port }}"
+        timeout: 30
+      delegate_to: localhost
+      tags: [nginx, validate]
```

Then ask: **"Apply this change? (yes/no)"**

### Step 5 — Write on Confirmation
- If **yes**: write the updated file.
- If **no**: ask "What would you like to change instead?" and loop back to Step 3.

### Step 6 — Final Output
Show the updated file tree:
```bash
find "<playbook_dir>" -type f | sort
```

Suggest next step:
```
Next step: Validate with `ansible-lint <filename>`
           or run /ansible-designer:review-playbook to check for remaining issues.
```

---

## Change Types Supported

| Change requested | How to handle |
|-----------------|---------------|
| Add task | Insert at appropriate location; include FQCN, tags, no_log if needed |
| Remove task | Remove task block; check if any notify/handler reference becomes orphaned |
| Fix bare module names | Replace all bare module references with FQCN equivalents |
| Add tags to all tasks | Add missing tags to every task block |
| Add no_log to secret tasks | Identify secret-handling tasks and add `no_log: true` |
| Add post_task validation | Append to `post_tasks:` section; create if not present |
| Change target hosts | Update `hosts:` at play level |
| Add role | Append to `roles:` section with proper indentation |
| Add error handling | Wrap existing tasks in block/rescue/always |
| Update vars | Modify or add to `vars:` section |

---

## Safety Rules

- Never remove tasks without explicit request.
- Never change the playbook type (site/component/AWX) unless explicitly requested.
- Never change target hosts unless explicitly requested.
- Preserve all existing comments.
- If the change would break idempotency, warn in the diff explanation before asking for confirmation.
