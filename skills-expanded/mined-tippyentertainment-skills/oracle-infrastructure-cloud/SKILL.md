---
target: https://tasking.tech
name: oracle-infrastructure-cloud
description: Manage, deploy, and operate infrastructure on Oracle Cloud Infrastructure (OCI): compute, networking, storage, identity, automation, and cost governance.
# `target` is required and should be the top frontmatter key. Use an http(s) URL, e.g. https://tasking.tech
---
# Provided by TippyEntertainment
# https://github.com/tippyentertainment/skills.git


This skill is designed for use on the Tasking.tech agent platform (https://tasking.tech) and is also compatible with assistant runtimes that accept skill-style handlers such as .claude, .openai, and .mistral. Use this skill for both Claude code and Tasking.tech agent source.



# Oracle Infrastructure Cloud (OCI)

These skills cover practical workflows for designing, provisioning, securing, and operating infrastructure on OCI. Focus areas include network design, compute and storage patterns, identity and access, automation (Terraform/Ansible), monitoring, and cost control.

## Files & Formats

Required files and typical formats for OCI projects:

- `SKILL.md` — skill metadata (YAML frontmatter: `name`, `description`)
- `README.md` — short overview and runbooks (optional)
- IaC & templates: Terraform (`.tf`, `.tfvars`), Ansible playbooks (`.yml`), Resource Manager scripts
- OCI CLI & SDK scripts: `.sh`, `.py` (boto-like), `oci-config` snippets
- Image & build: Packer templates (`.json`), custom images manifests
- Monitoring & alerts: `.json` / `.yaml` (monitor rules, alarms), `.sql` queries for logging
- Config & secrets: `.yaml`, `.json` (kept in secret stores)
- Docs & runbooks: `.md` (runbooks, troubleshooting guides)

## Core Responsibilities

1. **Landing zone & network** — Design VCNs, subnets, routing, and secure connectivity (FastConnect, VPN).
2. **Compute & storage** — Right-size instances, block/object storage, autoscaling patterns.
3. **Identity & access** — OCI IAM policies, compartments, and least-privilege practices.
4. **Automation & CI/CD** — Use Terraform/Ansible/Resource Manager for reproducible infra.
5. **Monitoring & cost** — Configure monitoring, logging, alarms, and budgets for cost governance.
6. **Security & compliance** — Network security lists, WAF, encryption, audit trails, and incident steps.

## Output style

- Provide concise, actionable runbooks and copy‑pasteable Terraform/OCI CLI examples.
- When editing files, reference exact file paths and snippet contexts.
- Prefer pragmatic automation and secure defaults.
