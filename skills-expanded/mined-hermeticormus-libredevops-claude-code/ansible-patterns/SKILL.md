---
name: ansible-patterns
description: "Ansible reference patterns: playbook and role layout, Jinja2 templates, Vault usage, idempotency and handlers, dynamic AWS EC2 inventory, block/rescue error handling, Molecule tests, ansible.cfg settings, and anti-patterns. Use when writing or reviewing Ansible code."
---

# Ansible Patterns

Production-tested Ansible patterns with real YAML, Jinja2, and configuration examples.

## Playbook Structure

```yaml
# site.yml - Top-level orchestration playbook
---
- name: Configure base OS
  hosts: all
  become: true
  gather_facts: true
  roles:
    - common
    - security-hardening

- name: Deploy web tier
  hosts: webservers
  become: true
  serial: "25%"
  max_fail_percentage: 10
  pre_tasks:
    - name: Remove host from load balancer
      community.general.haproxy:
        state: disabled
        host: "{{ inventory_hostname }}"
        backend: webservers
      delegate_to: lb01
  roles:
    - nginx
    - webapp
  post_tasks:
    - name: Wait for app healthcheck
      uri:
        url: "http://{{ ansible_host }}:8080/health"
        status_code: 200
      retries: 10
      delay: 5
    - name: Re-enable in load balancer
      community.general.haproxy:
        state: enabled
        host: "{{ inventory_hostname }}"
        backend: webservers
      delegate_to: lb01
```

## Role Directory Layout

```
roles/postgresql/
├── tasks/
│   ├── main.yml          # import_tasks for sub-task files
│   ├── install.yml       # Package installation
│   ├── configure.yml     # postgresql.conf, pg_hba.conf
│   └── replication.yml   # Streaming replication setup
├── handlers/
│   └── main.yml          # restart postgresql, reload postgresql
├── defaults/
│   └── main.yml          # Safe defaults (port: 5432, max_connections: 100)
├── vars/
│   └── main.yml          # Internal role vars (version-specific paths)
├── templates/
│   ├── postgresql.conf.j2
│   └── pg_hba.conf.j2
├── files/
│   └── pg_hba.conf.base  # Static base config if needed
├── meta/
│   └── main.yml          # Dependencies: [common]
└── molecule/
    └── default/
        ├── molecule.yml
        ├── converge.yml
        └── verify.yml
```

## Jinja2 Template Patterns

```jinja2
{# postgresql.conf.j2 #}
# Managed by Ansible - do not edit manually
# Generated: {{ ansible_date_time.iso8601 }}

listen_addresses = '{{ postgresql_listen_addresses | join(",") }}'
port = {{ postgresql_port | default(5432) }}
max_connections = {{ postgresql_max_connections | default(100) }}

# Memory settings (tune to 25% of total RAM for dedicated DB server)
shared_buffers = {{ (ansible_memtotal_mb * 0.25) | int }}MB
effective_cache_size = {{ (ansible_memtotal_mb * 0.75) | int }}MB
work_mem = {{ postgresql_work_mem | default('4MB') }}

{% if postgresql_ssl_enabled %}
ssl = on
ssl_cert_file = '{{ postgresql_ssl_cert_file }}'
ssl_key_file = '{{ postgresql_ssl_key_file }}'
{% else %}
ssl = off
{% endif %}

{% for replica in groups['pg_replicas'] | default([]) %}
# Replica: {{ replica }}
{% endfor %}
```

## Ansible Vault Usage

```bash
# Encrypt a single variable value inline
ansible-vault encrypt_string 'MyS3cretP@ss' --name 'db_password'
# Produces vault-encrypted value for pasting into vars file

# Encrypt a whole vars file
ansible-vault encrypt group_vars/prod/vault.yml

# Decrypt for inspection
ansible-vault decrypt group_vars/prod/vault.yml

# Edit encrypted file in place
ansible-vault edit group_vars/prod/vault.yml

# Run playbook with vault password
ansible-playbook site.yml --vault-password-file ~/.vault_pass

# Multi-vault with vault IDs (different passwords per environment)
ansible-playbook site.yml \
  --vault-id dev@~/.vault_pass_dev \
  --vault-id prod@prompt
```

```yaml
# group_vars/prod/vars.yml - References vault vars
db_host: db.prod.example.com
db_port: 5432
db_name: myapp
db_user: myapp_user
db_password: "{{ vault_db_password }}"  # Defined in vault.yml

# group_vars/prod/vault.yml - Encrypted file
vault_db_password: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  66386439...
```

## Idempotency Patterns

```yaml
# Pattern: changed_when for command module
- name: Check if service is initialized
  command: systemctl is-active myapp
  register: myapp_status
  changed_when: false
  failed_when: false

# Pattern: creates for one-time init tasks
- name: Initialize application database
  command: /opt/myapp/bin/db-init
  args:
    creates: /var/lib/myapp/.initialized

# Pattern: failed_when for custom error detection
- name: Run database migration
  command: /opt/myapp/bin/migrate up
  register: migration_result
  failed_when:
    - migration_result.rc != 0
    - '"already at latest" not in migration_result.stdout'

# Pattern: when with registered vars
- name: Get current app version
  command: /opt/myapp/bin/version
  register: current_version
  changed_when: false

- name: Deploy new version
  # ... deploy tasks
  when: current_version.stdout != desired_version
```

## Handler Patterns

```yaml
# handlers/main.yml
---
- name: restart nginx
  service:
    name: nginx
    state: restarted
  listen: "restart web services"  # Can listen to group notifications

- name: reload nginx
  service:
    name: nginx
    state: reloaded

- name: restart postgresql
  service:
    name: postgresql
    state: restarted

# In tasks:
- name: Update nginx configuration
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    validate: nginx -t -c %s  # Validate before deploy
  notify: reload nginx         # Use reload (not restart) for zero-downtime
```

## Dynamic AWS EC2 Inventory

```yaml
# inventory/aws_ec2.yml
plugin: amazon.aws.aws_ec2
regions:
  - us-east-1
  - us-west-2
keyed_groups:
  - key: tags.Environment
    prefix: env
    separator: "_"
  - key: tags.Role
    prefix: role
    separator: "_"
  - key: placement.region
    prefix: region
compose:
  ansible_host: public_ip_address
  ansible_user: "'ubuntu'"
filters:
  instance-state-name: running
  "tag:ManagedBy": ansible
hostnames:
  - tag:Name
  - private-dns-name
```

## Block/Rescue Error Handling

```yaml
- name: Deploy application with rollback
  block:
    - name: Stop current application
      service:
        name: myapp
        state: stopped

    - name: Deploy new release
      unarchive:
        src: "{{ release_url }}"
        dest: /opt/myapp
        remote_src: true

    - name: Run database migrations
      command: /opt/myapp/bin/migrate up
      register: migration_result

    - name: Start application
      service:
        name: myapp
        state: started

    - name: Verify application health
      uri:
        url: http://localhost:8080/health
        status_code: 200
      retries: 10
      delay: 3

  rescue:
    - name: Rollback to previous release
      file:
        src: /opt/myapp/releases/previous
        dest: /opt/myapp/current
        state: link

    - name: Start application from rollback
      service:
        name: myapp
        state: started

    - name: Fail with informative message
      fail:
        msg: "Deployment failed. Rolled back to previous release. Migration output: {{ migration_result.stdout | default('N/A') }}"

  always:
    - name: Record deployment attempt
      uri:
        url: "{{ deployment_webhook }}"
        method: POST
        body_format: json
        body:
          host: "{{ inventory_hostname }}"
          status: "{{ 'success' if not ansible_failed_task else 'failed' }}"
          timestamp: "{{ ansible_date_time.iso8601 }}"
```

## Molecule Test Structure

```yaml
# molecule/default/molecule.yml
---
dependency:
  name: galaxy
driver:
  name: docker
platforms:
  - name: ubuntu-22
    image: geerlingguy/docker-ubuntu2204-ansible:latest
    pre_build_image: true
  - name: centos-9
    image: geerlingguy/docker-rockylinux9-ansible:latest
    pre_build_image: true
provisioner:
  name: ansible
verifier:
  name: ansible
lint: |
  set -e
  ansible-lint

# molecule/default/verify.yml
---
- name: Verify nginx role
  hosts: all
  tasks:
    - name: Check nginx is running
      service:
        name: nginx
        state: started
      check_mode: true

    - name: Verify nginx responds on port 80
      uri:
        url: http://localhost:80
        status_code: [200, 301, 302]

    - name: Check nginx config is valid
      command: nginx -t
      changed_when: false
```

## ansible.cfg Best Practices

```ini
[defaults]
inventory          = inventory/
roles_path         = roles/:~/.ansible/roles
collections_paths  = collections/:~/.ansible/collections
host_key_checking  = False
retry_files_enabled = False
stdout_callback    = yaml
forks              = 20
gathering          = smart
fact_caching       = jsonfile
fact_caching_connection = /tmp/ansible_facts
fact_caching_timeout = 3600

[ssh_connection]
pipelining         = True
control_path       = %(directory)s/%%h-%%r
ssh_args           = -C -o ControlMaster=auto -o ControlPersist=60s
```

## Anti-Patterns to Avoid

- `command: apt-get install nginx` -- use `apt: name=nginx state=present`
- `shell: service nginx restart` in tasks -- use a handler with `notify:`
- Hardcoded IPs in playbooks -- use inventory variables
- `ignore_errors: true` broadly -- use `failed_when:` for specific conditions
- `vars_files: [secrets.yml]` with plaintext -- always vault-encrypt secrets
- `gather_facts: true` when you only need to copy a file -- adds 2-3s per host
