---
name: update-conf
description: Update an existing ansible.cfg. Triggered by /update-conf. Reads the current config, applies the requested section or key changes, shows a unified diff, waits for explicit user confirmation, then writes. Never overwrites silently. Adds justification comments for security-sensitive settings.
---

# update-conf

Update an existing ansible.cfg with targeted changes. Always shows a diff and waits for confirmation before writing.

---

## Required Inputs

1. **path to ansible.cfg** — Resolved from discovery if not provided
2. **change_description** — What to change (e.g., "enable fact caching with redis", "set forks to 20", "add vault_identity_list for dev and prod")

---

## Behavior

### Step 1 — Discovery
Locate the ansible.cfg via discovery (`references/discovery.md`).

### Step 2 — Load Existing Config
Read the full ansible.cfg content.

### Step 2a — Secret Scan (before any output)
Before displaying any content or diff, scan every line for credential-like values:
- Match lines where the key contains `password`, `secret`, `token`, `key`, `pass`, `credential`, or `vault_password_file`
- **Skip** lines where the value is already a vault reference (`{{ vault_* }}`), empty, or `None`
- For any remaining matches, **redact the value** in all output: `password = ***REDACTED***`
- Emit a warning at the top of the diff block:
  ```
  ⚠ Warning: N line(s) with credential-like values were redacted from this display.
    Review the file directly before applying changes.
  ```
- Never output actual credential values in diffs, summaries, or confirmations.

### Step 3 — Apply Change
Apply the requested change:
- Preserve all existing sections, keys, and comments
- Add inline justification comments for security-sensitive settings:
  - `host_key_checking = False` → must have a comment explaining why
  - `vault_password_file` → add chmod reminder comment
- Use correct INI format: `key = value` with spaces around `=`
- If a requested section doesn't exist, create it at the appropriate location
- If removing a key: remove only that line (and its comment block if it's clearly paired)
- Prefer `collections_path` in newly generated examples while preserving existing intent in older files

### Step 4 — Show Unified Diff

```
--- ansible.cfg (original)
+++ ansible.cfg (proposed)
@@ -8,6 +8,9 @@
 forks                 = 10
 timeout               = 30
+
+# Fact caching: redis (shared across controller nodes; configure auth via REDIS_URL or vault)
+fact_caching          = redis
+fact_caching_connection = redis://:{{ vault_redis_password }}@cache.internal:6379/0
+fact_caching_timeout  = 86400
```

Then ask: **"Apply this change? (yes/no)"**

### Step 5 — Write on Confirmation
- If **yes**: write the updated ansible.cfg.
- If **no**: ask what to change and loop back.

### Step 6 — Final Output
```bash
echo "Updated: $(realpath ansible.cfg)"
```

Suggest next step:
```
Next step: Validate with `ansible --version` to confirm the config is loaded
           or run /ansible-designer:review-conf to check for remaining issues.
```

---

## Change Types Supported

| Change requested | How to handle |
|-----------------|---------------|
| Set a key in an existing section | Find the section, update the key value; add if not present |
| Add a new section | Append section at end of file with appropriate keys |
| Enable fact caching | Set `fact_caching`, `fact_caching_connection`, `fact_caching_timeout` in [defaults] |
| Add vault_identity_list | Add/update `vault_identity_list` in [defaults]; show example format |
| Change callback plugins | Update `callbacks_enabled` in [defaults]; warn if awx_display is being added |
| Enable pipelining | Add `pipelining = True` to [ssh_connection]; add sudoers note comment |
| Change stdout_callback | Update `stdout_callback` in [defaults] |
| Set forks | Update `forks` in [defaults]; add RAM note if value > 50 |
| Remove a setting | Remove the line (and its comment if inline or immediately preceding) |
| Comment out a setting | Prefix line with `#` and add a note explaining why it's disabled |

---

## Safety Rules

- Never remove entire sections unless explicitly requested.
- Never change `host_key_checking = True` to `False` without adding a justification comment.
- If adding `vault_password_file`, add a comment reminding about `chmod 600`.
- If the user requests `forks > 100`, warn: "Each fork uses ~100MB RAM — ensure the controller has sufficient memory."
- Preserve the existing indentation/alignment style (spaces around `=`).
- **Never display actual credential values** — apply the Step 2a secret scan before any output. Redact before showing.
- When modifying security-sensitive settings (`host_key_checking`, `become`, `transport`, `vault_password_file`, callback or stdout plugins), always add an inline comment explaining the security implication of the change.
