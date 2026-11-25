---
name: ansible-configure
description: Configuration management and automation with Ansible
version: 1.0.0
tags: [devops, automation, configuration, deployment]
---

# Ansible – Configuration Management

Ansible automates server configuration, application deployment,
and orchestration using human-readable YAML playbooks.

- **GitHub**: github.com/ansible/ansible (65 000+ ⭐)
- **License**: GPL-3.0
- **Security**: Red Hat-backed. Enterprise-grade. No malware.

## Usage Examples

### Run a playbook

```bash
ansible-playbook -i inventory.ini site.yml
```

### Ping all hosts

```bash
ansible all -i inventory.ini -m ping
```

### Run an ad-hoc command

```bash
ansible webservers -i inventory.ini -m shell -a "uptime"
```

## AI Agent Tips

- Agentless — connects via SSH, no agent installation on targets.
- Playbooks are idempotent — safe to run multiple times.
- Galaxy provides 1000+ community roles and collections.
- Integrates with Jenkins, GitLab CI, and GitHub Actions for CI/CD.
