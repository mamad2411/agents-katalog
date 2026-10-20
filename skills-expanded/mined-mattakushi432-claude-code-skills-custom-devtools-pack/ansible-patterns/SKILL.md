---
name: ansible-patterns
description: "When to activate: Ansible, playbook, inventory, role, handler, template, vault, task, module, idempotent"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: devops
  language: devops
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# Ansible Patterns

## Directory Structure (roles)

```
site.yml
inventory/
  production/
    hosts
    group_vars/
      all.yml
      webservers.yml
  staging/
    hosts
roles/
  webserver/
    tasks/
      main.yml
    handlers/
      main.yml
    templates/
      nginx.conf.j2
    vars/
      main.yml
    defaults/
      main.yml
    meta/
      main.yml
```

## Inventory (ini)

```ini
[webservers]
web1.example.com ansible_user=ubuntu
web2.example.com ansible_user=ubuntu

[databases]
db1.example.com ansible_user=ubuntu

[all:vars]
ansible_python_interpreter=/usr/bin/python3
```

## Playbook

```yaml
---
- name: Configure web servers
  hosts: webservers
  become: true
  vars_files:
    - vars/secrets.yml
  roles:
    - common
    - webserver
  tasks:
    - name: Ensure nginx is latest
      ansible.builtin.package:
        name: nginx
        state: latest
      notify: Restart nginx
```

## Handlers

```yaml
# roles/webserver/handlers/main.yml
---
- name: Restart nginx
  ansible.builtin.service:
    name: nginx
    state: restarted

- name: Reload nginx
  ansible.builtin.service:
    name: nginx
    state: reloaded
```

## Jinja2 Template (nginx.conf.j2)

```nginx
server {
    listen 80;
    server_name {{ server_name }};
    root {{ document_root }};

    location / {
        proxy_pass http://{{ upstream_host }}:{{ upstream_port }};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    {% if enable_ssl %}
    listen 443 ssl;
    ssl_certificate {{ ssl_cert_path }};
    ssl_certificate_key {{ ssl_key_path }};
    {% endif %}
}
```

## Task: Deploy Template

```yaml
- name: Deploy nginx config
  ansible.builtin.template:
    src: nginx.conf.j2
    dest: /etc/nginx/sites-available/myapp
    owner: root
    group: root
    mode: '0644'
    validate: nginx -t -c %s
  notify: Reload nginx
```

## Loops and Conditions

```yaml
- name: Create directories
  ansible.builtin.file:
    path: "{{ item }}"
    state: directory
    mode: '0755'
  loop:
    - /var/www/html
    - /var/log/myapp
    - /etc/myapp

- name: Install packages (Debian only)
  ansible.builtin.apt:
    name: "{{ item }}"
    state: present
  loop:
    - nginx
    - certbot
    - python3-certbot-nginx
  when: ansible_os_family == "Debian"
```

## Ansible Vault

```bash
# Encrypt a file
ansible-vault encrypt vars/secrets.yml

# Edit in place
ansible-vault edit vars/secrets.yml

# Run playbook with vault password
ansible-playbook site.yml --vault-password-file ~/.vault_pass
# or
ansible-playbook site.yml --ask-vault-pass
```

```yaml
# vars/secrets.yml (encrypted)
db_password: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  ...
```

## Register and Use Output

```yaml
- name: Check if service is running
  ansible.builtin.command: systemctl is-active myapp
  register: service_status
  ignore_errors: true
  changed_when: false

- name: Start service if not running
  ansible.builtin.service:
    name: myapp
    state: started
  when: service_status.rc != 0
```

## Key Rules
- All tasks should be idempotent — running twice must not cause changes the second time
- Use `changed_when: false` for read-only commands
- Use `ansible.builtin.` FQCN for all built-in modules
- Tag tasks (`tags: [config, nginx]`) for selective runs: `--tags config`
- Test roles with Molecule before using in production
