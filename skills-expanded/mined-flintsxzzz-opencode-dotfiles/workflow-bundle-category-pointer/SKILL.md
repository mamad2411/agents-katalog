---
name: workflow-bundle-category-pointer
description: "Pointer to a library of 9 specialized Workflow Bundle skills. Use when working on workflow-bundle-related tasks."
risk: none
---

# Workflow Bundle Capability Library 🎯

This is a **pointer skill**. The 9 specialized Workflow Bundle skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **ai-ml** — AI and machine learning workflow covering LLM application development, RAG implementation, agent architecture, ML pipelines, and AI-powered features.
- **cloud-devops** — Cloud infrastructure and DevOps workflow covering AWS, Azure, GCP, Kubernetes, Terraform, CI/CD, monitoring, and cloud-native development.
- **database** — Database development and operations workflow covering SQL, NoSQL, database design, migrations, optimization, and data engineering.
- **development** — Comprehensive web, mobile, and backend development workflow bundling frontend, backend, full-stack, and mobile development skills for end-to-end application delivery.
- **documentation** — Documentation generation workflow covering API docs, architecture docs, README files, code comments, and technical writing.
- **os-scripting** — Operating system and shell scripting troubleshooting workflow for Linux, macOS, and Windows. Covers bash scripting, system administration, debugging, and automation.
- **security-audit** — Comprehensive security auditing workflow covering web application testing, API security, penetration testing, vulnerability scanning, and security hardening.
- **testing-qa** — Comprehensive testing and QA workflow covering unit testing, integration testing, E2E testing, browser automation, and quality assurance.
- **wordpress** — Complete WordPress development workflow covering theme development, plugin creation, WooCommerce integration, performance optimization, and security hardening. Includes WordPress 7.0 features: Real-Time Collaboration, AI Connectors, Abilities API, DataViews, and PHP-only blocks.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/workflow-bundle/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/workflow-bundle`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
