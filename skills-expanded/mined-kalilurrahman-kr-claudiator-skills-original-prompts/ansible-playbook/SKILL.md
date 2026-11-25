---
name: ansible-playbook
description: Write Ansible playbooks for server provisioning, configuration management, and application deployment. Outputs idempotent plays with roles, handlers, vault-encrypted secrets, and inventory management.
argument-hint: [target environment, OS type, services to configure, deployment target]
allowed-tools: Read, Write, Bash
---

# Ansible Playbook

Ansible automates server configuration, application deployment, and operational tasks without agents. Write idempotent playbooks — running them multiple times produces the same result as running once.

## Process

1. **Define inventory** — static file or dynamic inventory from cloud provider.
2. **Structure with roles** — one role per concern (nginx, postgres, app deployment).
3. **Use variables hierarchy** — group_vars → host_vars → role defaults → play vars.
4. **Encrypt secrets with Vault** — never store plaintext credentials in playbooks.
5. **Write idempotent tasks** — use `state:` parameters, not shell commands that repeat.
6. **Add handlers** — restart services only when configuration actually changes.
7. **Test with `--check`** — dry run before applying to production.
8. **Tag tasks** — enable selective execution (`--tags deploy`, `--tags config`).

## Output Format

### Directory Structure

```
ansible/
├── inventories/
│   ├── production/
│   │   ├── hosts.yml
│   │   └── group_vars/
│   │       ├── all.yml
│   │       ├── webservers.yml
│   │       └── databases.yml
│   └── staging/
│       └── hosts.yml
├── roles/
│   ├── common/
│   │   ├── tasks/main.yml
│   │   ├── handlers/main.yml
│   │   ├── templates/
│   │   ├── files/
│   │   └── defaults/main.yml
│   ├── nginx/
│   ├── postgres/
│   └── app/
├── site.yml          # Master playbook
├── deploy.yml        # Deployment-only playbook
└── ansible.cfg
```

### Inventory

```yaml
# inventories/production/hosts.yml
all:
  children:
    webservers:
      hosts:
        web-01:
          ansible_host: 10.0.1.10
        web-02:
          ansible_host: 10.0.1.11
      vars:
        nginx_workers: 4
    
    databases:
      hosts:
        db-primary:
          ansible_host: 10.0.2.10
          postgres_role: primary
        db-replica:
          ansible_host: 10.0.2.11
          postgres_role: replica
    
    loadbalancers:
      hosts:
        lb-01:
          ansible_host: 10.0.0.10
  
  vars:
    ansible_user: deploy
    ansible_ssh_private_key_file: ~/.ssh/deploy_key
    ansible_python_interpreter: /usr/bin/python3
```

```yaml
# inventories/production/group_vars/all.yml
app_name: myapp
app_user: myapp
app_dir: /opt/myapp
app_port: 8080
environment: production

# Vault-encrypted values (ansible-vault encrypt_string)
db_password: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  62373362646463353933616266323739...

# Non-sensitive
log_level: info
max_connections: 100
```

### Main Playbook

```yaml
# site.yml
---
- name: Apply common configuration to all hosts
  hosts: all
  become: true
  roles:
    - common
  tags: [common]

- name: Configure web servers
  hosts: webservers
  become: true
  roles:
    - nginx
    - app
  tags: [web]

- name: Configure database servers
  hosts: databases
  become: true
  roles:
    - postgres
  tags: [db]
```

### Common Role

```yaml
# roles/common/tasks/main.yml
---
- name: Update apt cache
  ansible.builtin.apt:
    update_cache: true
    cache_valid_time: 3600   # Don't update if cache < 1 hour old
  tags: [packages]

- name: Install common packages
  ansible.builtin.apt:
    name:
      - curl
      - wget
      - vim
      - htop
      - fail2ban
      - ufw
      - ntp
    state: present
  tags: [packages]

- name: Create application user
  ansible.builtin.user:
    name: "{{ app_user }}"
    system: true
    shell: /bin/false
    home: "{{ app_dir }}"
    create_home: true
  tags: [users]

- name: Configure UFW — deny all inbound by default
  community.general.ufw:
    state: enabled
    policy: deny
    direction: incoming
  tags: [firewall]

- name: Allow SSH
  community.general.ufw:
    rule: allow
    port: "22"
    proto: tcp
  tags: [firewall]

- name: Set timezone
  community.general.timezone:
    name: "{{ timezone | default('UTC') }}"
  tags: [system]

- name: Configure NTP
  ansible.builtin.template:
    src: ntp.conf.j2
    dest: /etc/ntp.conf
    owner: root
    group: root
    mode: '0644'
  notify: restart ntp
  tags: [system]
```

```yaml
# roles/common/handlers/main.yml
---
- name: restart ntp
  ansible.builtin.service:
    name: ntp
    state: restarted

- name: reload nginx
  ansible.builtin.service:
    name: nginx
    state: reloaded

- name: restart app
  ansible.builtin.service:
    name: "{{ app_name }}"
    state: restarted
```

### Nginx Role

```yaml
# roles/nginx/tasks/main.yml
---
- name: Install nginx
  ansible.builtin.apt:
    name: nginx
    state: present
  tags: [nginx]

- name: Allow HTTP/HTTPS through firewall
  community.general.ufw:
    rule: allow
    port: "{{ item }}"
    proto: tcp
  loop:
    - "80"
    - "443"
  tags: [nginx, firewall]

- name: Deploy nginx config
  ansible.builtin.template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    owner: root
    group: root
    mode: '0644'
    validate: nginx -t -c %s   # Validate before replacing
  notify: reload nginx
  tags: [nginx, config]

- name: Deploy site config
  ansible.builtin.template:
    src: site.conf.j2
    dest: /etc/nginx/sites-available/{{ app_name }}
    owner: root
    group: root
    mode: '0644'
  notify: reload nginx
  tags: [nginx, config]

- name: Enable site
  ansible.builtin.file:
    src: /etc/nginx/sites-available/{{ app_name }}
    dest: /etc/nginx/sites-enabled/{{ app_name }}
    state: link
  notify: reload nginx
  tags: [nginx]

- name: Remove default site
  ansible.builtin.file:
    path: /etc/nginx/sites-enabled/default
    state: absent
  notify: reload nginx
  tags: [nginx]

- name: Ensure nginx is started and enabled
  ansible.builtin.service:
    name: nginx
    state: started
    enabled: true
  tags: [nginx]
```

```nginx
# roles/nginx/templates/site.conf.j2
upstream {{ app_name }}_backend {
    {% for port in range(app_port, app_port + app_workers | default(1)) %}
    server 127.0.0.1:{{ port }};
    {% endfor %}
    keepalive 32;
}

server {
    listen 80;
    server_name {{ server_name | default(inventory_hostname) }};
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name {{ server_name | default(inventory_hostname) }};

    ssl_certificate     /etc/ssl/certs/{{ app_name }}.crt;
    ssl_certificate_key /etc/ssl/private/{{ app_name }}.key;

    location / {
        proxy_pass http://{{ app_name }}_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout {{ nginx_read_timeout | default(30) }}s;
    }

    location /health {
        access_log off;
        proxy_pass http://{{ app_name }}_backend;
    }
}
```

### App Deployment Role

```yaml
# roles/app/tasks/main.yml
---
- name: Create app directories
  ansible.builtin.file:
    path: "{{ item }}"
    state: directory
    owner: "{{ app_user }}"
    group: "{{ app_user }}"
    mode: '0755'
  loop:
    - "{{ app_dir }}"
    - "{{ app_dir }}/releases"
    - "{{ app_dir }}/shared"
    - "{{ app_dir }}/shared/config"
    - "{{ app_dir }}/shared/logs"
  tags: [app]

- name: Deploy application archive
  ansible.builtin.unarchive:
    src: "{{ app_archive_url }}"
    dest: "{{ app_dir }}/releases/"
    remote_src: true
    creates: "{{ app_dir }}/releases/{{ app_version }}"
    owner: "{{ app_user }}"
    group: "{{ app_user }}"
  tags: [app, deploy]

- name: Deploy environment config
  ansible.builtin.template:
    src: app.env.j2
    dest: "{{ app_dir }}/shared/config/.env"
    owner: "{{ app_user }}"
    group: "{{ app_user }}"
    mode: '0600'   # Secrets file — owner only
  tags: [app, config]

- name: Link shared config
  ansible.builtin.file:
    src: "{{ app_dir }}/shared/config/.env"
    dest: "{{ app_dir }}/releases/{{ app_version }}/.env"
    state: link
    owner: "{{ app_user }}"
    group: "{{ app_user }}"
  tags: [app, deploy]

- name: Update current symlink (atomic deploy)
  ansible.builtin.file:
    src: "{{ app_dir }}/releases/{{ app_version }}"
    dest: "{{ app_dir }}/current"
    state: link
    owner: "{{ app_user }}"
    group: "{{ app_user }}"
  notify: restart app
  tags: [app, deploy]

- name: Deploy systemd service
  ansible.builtin.template:
    src: app.service.j2
    dest: /etc/systemd/system/{{ app_name }}.service
    owner: root
    group: root
    mode: '0644'
  notify:
    - reload systemd
    - restart app
  tags: [app, service]

- name: Ensure app service is started and enabled
  ansible.builtin.systemd:
    name: "{{ app_name }}"
    state: started
    enabled: true
    daemon_reload: true
  tags: [app]

- name: Clean up old releases (keep last 5)
  ansible.builtin.shell: |
    cd {{ app_dir }}/releases && \
    ls -t | tail -n +6 | xargs rm -rf
  changed_when: false
  tags: [app, cleanup]
```

### Deployment Playbook

```yaml
# deploy.yml — rolling deploy with zero downtime
---
- name: Deploy application
  hosts: webservers
  become: true
  serial: 1            # Deploy one server at a time
  max_fail_percentage: 0

  pre_tasks:
    - name: Remove from load balancer
      community.general.haproxy:
        state: disabled
        host: "{{ inventory_hostname }}"
        socket: /run/haproxy/admin.sock
      delegate_to: lb-01
      tags: [deploy]

  roles:
    - role: app
      tags: [deploy]

  post_tasks:
    - name: Wait for app to be healthy
      ansible.builtin.uri:
        url: "http://localhost:{{ app_port }}/health"
        status_code: 200
      retries: 10
      delay: 3
      tags: [deploy]

    - name: Add back to load balancer
      community.general.haproxy:
        state: enabled
        host: "{{ inventory_hostname }}"
        socket: /run/haproxy/admin.sock
      delegate_to: lb-01
      tags: [deploy]
```

### ansible.cfg

```ini
[defaults]
inventory          = inventories/production
roles_path         = roles
remote_user        = deploy
host_key_checking  = True
stdout_callback    = yaml
callback_whitelist = profile_tasks
retry_files_enabled = False
vault_password_file = ~/.ansible_vault_pass

[ssh_connection]
pipelining         = True
control_path       = /tmp/ansible-ssh-%%h-%%p-%%r
ssh_args           = -o ControlMaster=auto -o ControlPersist=60s

[privilege_escalation]
become             = True
become_method      = sudo
become_user        = root
become_ask_pass    = False
```

## Rules

- **Idempotency is non-negotiable** — every task must be safe to run multiple times.
- **Use modules over shell** — `ansible.builtin.apt` not `shell: apt install`; modules are idempotent.
- **Encrypt all secrets with Vault** — never commit plaintext passwords or keys.
- **Validate templates before applying** — use the `validate:` parameter for config files.
- **Rolling deploys with `serial:`** — prevents simultaneous downtime across all servers.
- **Tag everything** — `--tags` enables surgical re-runs without full playbook execution.
- **Test with `--check --diff`** — dry run shows what would change before it changes it.
- **Use handlers for restarts** — restart services only when something actually changed.
- **Pin role versions in requirements.yml** — `ansible-galaxy install -r requirements.yml`.
- **Separate deploy from provision** — provisioning (install) and deployment (update app) are different playbooks.
