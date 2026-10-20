---
name: configuration-management-sysadmin
description: Configuration management, Infrastructure as Code, and automation with Ansible, Puppet, Chef
license: MIT
compatibility: opencode
metadata:
  audience: devops
  category: systems-administration
---

## What I do
- Manage server configurations at scale
- Automate infrastructure setup
- Use configuration management tools
- Implement idempotent manifests
- Define desired state
- Ensure configuration compliance

## When to use me
When managing infrastructure at scale, automating deployments, or ensuring consistent configurations.

## Tools Overview

### Ansible
- Agentless
- YAML playbooks
- SSH-based
- Declarative
- Best for: Ad-hoc automation, configuration

```yaml
- name: Install nginx
  hosts: webservers
  become: yes
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
```

### Puppet
- Agent-based (master/agent)
- Declarative DSL
- Resource types
- Report drift
- Best for: Long-running infrastructure

```puppet
package { 'nginx':
  ensure => installed,
}
service { 'nginx':
  ensure => running,
  require => Package['nginx'],
}
```

### Chef
- Agent-based
- Ruby DSL
- Cookbooks and recipes
- Chef Infra, Chef Inspec
- Best for: Complex configurations

```ruby
package 'nginx' do
  action :install
end

service 'nginx' do
  action [:start, :enable]
end
```

### Terraform
- Infrastructure provisioning
- HCL language
- Plan and apply
- State management
- Best for: Cloud resources

```hcl
resource "aws_instance" "web" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  tags = {
    Name = "WebServer"
  }
}
```

## Key Concepts

### Idempotency
- Same result regardless of runs
- Check current state first
- Make minimal changes

### Desired State
- Define what, not how
- System reconciles to desired
- Drift detection

### Modules/Recipes/Cookbooks
- Reusable components
- Dependency management
- Version control

### Testing
- Testinfra
- Serverspec
- Kitchen/CI integration

## Best Practices
- Use version control
- Peer review changes
- Test in staging first
- Use secrets management
- Modularize configurations
- Document modules
- Monitor drift
- Backup state files
