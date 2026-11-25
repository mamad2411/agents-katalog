---
name: tpl-devops-ansible-server-setup
description: Template do pack (devops/05-ansible-server-setup.md). Orienta o agente em infra, deploy, CI/CD e operacao alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: devops/05-ansible-server-setup.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: Ansible Server Setup (Ubuntu 24.04 LTS)

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `devops/05-ansible-server-setup.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Automation:** Ansible 9+ (ansible-core 2.16+)
- **Target OS:** Ubuntu 24.04 LTS
- **Services:** Nginx, Certbot (Let's Encrypt), UFW, Fail2ban, Node.js
- **Secret Management:** Ansible Vault
- **Inventory:** Static YAML inventory (or dynamic from AWS/GCP)
- **Python:** 3.12 (ansible controller), Python 3.12 (managed nodes)

---

## DIRECTORY STRUCTURE
```
ansible/
├── ansible.cfg
├── inventory/
│   ├── production.yml
│   └── staging.yml
├── group_vars/
│   ├── all.yml                  # Shared vars
│   ├── all/
│   │   └── vault.yml            # Encrypted secrets (ansible-vault)
│   ├── webservers.yml
│   └── appservers.yml
├── host_vars/
│   └── web01.example.com.yml
├── playbooks/
│   ├── site.yml                 # Master playbook
│   ├── setup-server.yml
│   └── deploy-app.yml
└── roles/
    ├── common/
    │   ├── tasks/main.yml
    │   ├── handlers/main.yml
    │   └── vars/main.yml
    ├── nginx/
    │   ├── tasks/main.yml
    │   ├── handlers/main.yml
    │   ├── templates/
    │   │   └── vhost.conf.j2
    │   └── vars/main.yml
    ├── certbot/
    ├── ufw/
    ├── fail2ban/
    └── nodejs/
```

---

## ARCHITECTURE RULES
1. **Everything is idempotent** — run the playbook 10 times; result is the same. Use `state: present/absent`, never bare shell commands that can double-execute.
2. **Vault for all secrets** — no passwords, keys, or tokens in plaintext YAML. Use `ansible-vault encrypt_string` for inline secrets.
3. **Handlers for service restarts** — restart Nginx via `notify: restart nginx`, not a task. Handlers run only once per play, at the end.
4. **Tags on every task** — enables `--tags nginx,certbot` partial runs.
5. **`become: true` only when needed** — task-level, not play-level wherever possible.
6. **Check mode safe** — tasks must support `--check --diff` without side effects.
7. **Roles are reusable units** — no playbook-specific logic inside roles; parameterize via `vars/`.
8. **Use `validate:` on config templates** — `validate: nginx -t -c %s` before overwriting live config.

---

## ANSIBLE.CFG

```ini
# ansible/ansible.cfg
[defaults]
inventory          = inventory/production.yml
remote_user        = ubuntu
private_key_file   = ~/.ssh/deploy_key
host_key_checking  = True
retry_files_enabled = False
stdout_callback    = yaml
callbacks_enabled  = profile_tasks
gathering          = smart    # Cache facts

[privilege_escalation]
become       = True
become_method = sudo
become_user  = root

[ssh_connection]
pipelining           = True    # Speeds up execution significantly
control_path_dir     = ~/.ansible/cp
ssh_args             = -C -o ControlMaster=auto -o ControlPersist=60s
```

---

## INVENTORY

```yaml
# inventory/production.yml
all:
  vars:
    ansible_python_interpreter: /usr/bin/python3

  children:
    webservers:
      hosts:
        web01.example.com:
          ansible_host: 203.0.113.10
        web02.example.com:
          ansible_host: 203.0.113.11
    appservers:
      hosts:
        app01.example.com:
          ansible_host: 203.0.113.20
          node_port: 3000
```

---

## MASTER PLAYBOOK

```yaml
# playbooks/site.yml
---
- name: Apply common configuration
  hosts: all
  roles:
    - common
    - ufw
    - fail2ban

- name: Setup web servers
  hosts: webservers
  roles:
    - nginx
    - certbot

- name: Setup app servers
  hosts: appservers
  roles:
    - nodejs
```

---

## ROLE: COMMON (tasks/main.yml)

```yaml
---
- name: Update apt cache and upgrade packages
  ansible.builtin.apt:
    update_cache: true
    upgrade: dist
    cache_valid_time: 3600
  tags: [common, packages]

- name: Install required packages
  ansible.builtin.apt:
    name:
      - curl
      - git
      - unzip
      - htop
      - vim
      - logrotate
      - python3-pip
    state: present
  tags: [common, packages]

- name: Set timezone to UTC
  community.general.timezone:
    name: UTC
  tags: [common, timezone]

- name: Ensure deploy user exists
  ansible.builtin.user:
    name: deploy
    groups: sudo
    shell: /bin/bash
    create_home: true
    state: present
  tags: [common, users]

- name: Add SSH authorized key for deploy user
  ansible.posix.authorized_key:
    user: deploy
    key: "{{ vault_deploy_pubkey }}"
    state: present
  tags: [common, users]

- name: Disable root SSH login
  ansible.builtin.lineinfile:
    dest: /etc/ssh/sshd_config
    regexp: "^PermitRootLogin"
    line: "PermitRootLogin no"
    state: present
  notify: restart sshd
  tags: [common, security]

- name: Disable password authentication
  ansible.builtin.lineinfile:
    dest: /etc/ssh/sshd_config
    regexp: "^PasswordAuthentication"
    line: "PasswordAuthentication no"
    state: present
  notify: restart sshd
  tags: [common, security]
```

---

## ROLE: NGINX (tasks/main.yml)

```yaml
---
- name: Install Nginx
  ansible.builtin.apt:
    name: nginx
    state: present
  tags: [nginx]

- name: Ensure Nginx is enabled and started
  ansible.builtin.systemd:
    name: nginx
    enabled: true
    state: started
  tags: [nginx]

- name: Remove default Nginx site
  ansible.builtin.file:
    path: /etc/nginx/sites-enabled/default
    state: absent
  notify: reload nginx
  tags: [nginx]

- name: Deploy vhost configuration
  ansible.builtin.template:
    src: vhost.conf.j2
    dest: "/etc/nginx/sites-available/{{ nginx_vhost_name }}.conf"
    owner: root
    group: root
    mode: "0644"
    validate: "nginx -t -c %s"
  notify: reload nginx
  tags: [nginx, vhost]

- name: Enable vhost
  ansible.builtin.file:
    src: "/etc/nginx/sites-available/{{ nginx_vhost_name }}.conf"
    dest: "/etc/nginx/sites-enabled/{{ nginx_vhost_name }}.conf"
    state: link
  notify: reload nginx
  tags: [nginx, vhost]
```

---

## ROLE: NGINX (handlers/main.yml)

```yaml
---
- name: reload nginx
  ansible.builtin.systemd:
    name: nginx
    state: reloaded

- name: restart nginx
  ansible.builtin.systemd:
    name: nginx
    state: restarted

- name: restart sshd
  ansible.builtin.systemd:
    name: sshd
    state: restarted
```

---

## ROLE: UFW (tasks/main.yml)

```yaml
---
- name: Install UFW
  ansible.builtin.apt:
    name: ufw
    state: present
  tags: [ufw]

- name: Set UFW default policies
  community.general.ufw:
    direction: "{{ item.direction }}"
    policy: "{{ item.policy }}"
  loop:
    - { direction: incoming, policy: deny }
    - { direction: outgoing, policy: allow }
  tags: [ufw]

- name: Allow SSH
  community.general.ufw:
    rule: allow
    port: "22"
    proto: tcp
  tags: [ufw]

- name: Allow HTTP and HTTPS
  community.general.ufw:
    rule: allow
    port: "{{ item }}"
    proto: tcp
  loop: ["80", "443"]
  tags: [ufw]

- name: Enable UFW
  community.general.ufw:
    state: enabled
  tags: [ufw]
```

---

## ROLE: CERTBOT (tasks/main.yml)

```yaml
---
- name: Install Certbot and Nginx plugin
  ansible.builtin.apt:
    name:
      - certbot
      - python3-certbot-nginx
    state: present
  tags: [certbot]

- name: Request SSL certificate
  ansible.builtin.command:
    cmd: >
      certbot --nginx
      -d {{ certbot_domain }}
      --non-interactive
      --agree-tos
      --email {{ certbot_email }}
      --redirect
    creates: "/etc/letsencrypt/live/{{ certbot_domain }}/fullchain.pem"
  tags: [certbot]

- name: Ensure renewal timer is enabled
  ansible.builtin.systemd:
    name: certbot.timer
    enabled: true
    state: started
  tags: [certbot]
```

---

## ROLE: NODE.JS (tasks/main.yml)

```yaml
---
- name: Download NodeSource setup script
  ansible.builtin.get_url:
    url: https://deb.nodesource.com/setup_20.x
    dest: /tmp/nodesource_setup.sh
    mode: "0755"
  tags: [nodejs]

- name: Run NodeSource setup
  ansible.builtin.command:
    cmd: bash /tmp/nodesource_setup.sh
    creates: /etc/apt/sources.list.d/nodesource.list
  tags: [nodejs]

- name: Install Node.js
  ansible.builtin.apt:
    name: nodejs
    state: present
    update_cache: true
  tags: [nodejs]

- name: Install PM2 globally
  community.general.npm:
    name: pm2
    global: true
    state: present
  tags: [nodejs, pm2]

- name: Configure PM2 startup
  ansible.builtin.command:
    cmd: pm2 startup systemd -u deploy --hp /home/deploy
  changed_when: false
  tags: [nodejs, pm2]
```

---

## VAULT USAGE

```bash
# Create vault-encrypted file
ansible-vault create group_vars/all/vault.yml

# Encrypt an inline value
ansible-vault encrypt_string 'supersecret' --name 'vault_deploy_pubkey'

# Run playbook with vault password file (CI)
echo "$ANSIBLE_VAULT_PASS" > /tmp/vault_pass
ansible-playbook playbooks/site.yml --vault-password-file /tmp/vault_pass
rm /tmp/vault_pass
```

```yaml
# group_vars/all/vault.yml (encrypted)
vault_deploy_pubkey: "ssh-ed25519 AAAA..."
vault_db_password: "$(uuidgen)"
vault_jwt_secret: "$(openssl rand -hex 32)"
```

---

## RUN COMMANDS

```bash
# Check syntax
ansible-playbook playbooks/site.yml --syntax-check

# Dry run with diff
ansible-playbook playbooks/site.yml --check --diff

# Run specific tags
ansible-playbook playbooks/site.yml --tags "nginx,certbot"

# Limit to one host
ansible-playbook playbooks/site.yml --limit web01.example.com

# Production run
ansible-playbook playbooks/site.yml --ask-vault-pass
```
