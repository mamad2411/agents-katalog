---
name: new-playbook
description: Create a new Ansible playbook. Triggered by /new-playbook. Runs discovery to find existing roles and collections, then collects path, filename, target hosts/groups, and roles to include. Generates a complete playbook with header, vars block, pre/post tasks, roles section, error handling, and tags. Shows summary before writing. Never overwrites existing files without confirmation.
---

# new-playbook

Create a new Ansible playbook following production conventions.

---

## Required Inputs

Collect these parameters (one question at a time, using discovery context for defaults):

1. **path** — Directory where the playbook will be created (default: `./` or `./playbooks/` if that directory exists)
2. **filename** — Playbook filename (e.g., `site.yml`, `deploy-nginx.yml`)
3. **target_hosts** — Inventory group(s) or host pattern (e.g., `webservers`, `all`, `databases:webservers`)
4. **roles** — List of roles to include (suggest roles found in discovery; accept FQCN or short names)
5. **playbook_type** — Site playbook / Component playbook / AWX-ready playbook (suggest based on filename and roles)

If the user provides all of these inline, skip parameter collection.

---

## Behavior

### Step 1 — Discovery
Run discovery per `references/discovery.md`. Report:
- Roles found (in roles_path)
- Collections found (in collections_path)
- Existing playbooks
- Inventory location

Use discovered roles as suggestions during parameter collection.

### Step 2 — Parameter Collection
Ask one question at a time. Suggest smart defaults:
- If `site.yml` is the filename → suggest site playbook type
- If single role → suggest component playbook type
- If AWX is mentioned or `tower_job_id` is referenced → suggest AWX-ready type
- Roles list: show numbered list of discovered roles, let user pick by number or type FQCN

### Step 3 — Pre-Write Confirmation
Show a summary:
```
Will create: ./playbooks/deploy-nginx.yml

Play: "Deploy nginx web server"
  Hosts: webservers
  Roles: myorg.infra.nginx
  Type: Component playbook
  Tags: nginx, validate

Proceed? (yes/no)
```

Check if the file already exists. If it does, warn and require explicit confirmation.

### Step 4 — Generate Playbook
Use `references/playbook.md` as the base template. Select the appropriate template:
- Site playbook → Template 1
- Component playbook → Template 2
- AWX-ready → Template 3

Apply these rules to the generated content:
- All modules use FQCN
- All tasks have tags (component + action category)
- `no_log: true` on any task handling secrets per `references/security_vault.md`
- `pre_tasks` includes OS version assertion using `ansible.builtin.assert`
- Include a `post_tasks` validation block using `ansible.builtin.wait_for` or `ansible.builtin.uri`
- Keep inventory and variable references aligned with `references/inventory.md`
- End with validation guidance aligned with `references/testing.md`
- Include block/rescue pattern for the main execution block if multiple steps
- Proper YAML comment header (author, version, description, usage)

Write using bash:
```bash
cat > /path/to/playbook.yml << 'EOF'
[playbook content]
EOF
```

### Step 5 — Final Output
Show file tree:
```bash
find ./playbooks -type f | sort
```

Suggest next step:
```
Next step: Validate with `ansible-lint playbooks/deploy-nginx.yml`
           or use /ansible-designer:review-playbook to get a structured review.
```

---

## Example Generated Output

```yaml
---
# =============================================================================
# Playbook: deploy-nginx.yml
# Author:   Platform Team
# Version:  1.0.0
# Description: Deploy and configure nginx on webservers group.
# Usage:
#   ansible-playbook -i inventory/ deploy-nginx.yml
#   ansible-playbook -i inventory/ deploy-nginx.yml --check --diff
# =============================================================================

- name: Deploy nginx web server
  hosts: webservers
  become: true
  gather_facts: true
  vars:
    nginx_port: "{{ deploy_nginx_port | default(80) }}"
    nginx_enable_ssl: "{{ deploy_nginx_ssl | default(false) }}"

  pre_tasks:
    - name: Verify target OS is supported
      ansible.builtin.assert:
        that:
          - ansible_os_family in ['RedHat', 'Debian']
        fail_msg: "Unsupported OS family: {{ ansible_os_family }}"
      tags: [always]

  roles:
    - role: myorg.infra.nginx
      vars:
        nginx_port: "{{ nginx_port }}"
        nginx_enable_ssl: "{{ nginx_enable_ssl }}"

  post_tasks:
    - name: Confirm nginx is listening
      ansible.builtin.wait_for:
        host: "{{ ansible_host }}"
        port: "{{ nginx_port }}"
        timeout: 30
      delegate_to: localhost
      tags: [nginx, validate]

    - name: Print deployment summary
      ansible.builtin.debug:
        msg: "nginx deployed on {{ inventory_hostname }} — port {{ nginx_port }}"
      tags: [nginx, validate]
```
