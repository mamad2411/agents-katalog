---
name: dev-environment-setup
description: "Group skill: Set up a new development environment — project init, toolchain, package manager, dev container, editor config, git hooks, database, env vars, documentation, and CI/CD."
risk: low
source: self
---

# 🛠️ Dev Environment Setup

> **Group Skill** — Orchestrates sub-skills for onboarding a new project or team member.
> Activate by saying: "Set up dev environment" or "new project setup"

## When to Use

- Starting a new project from scratch
- Onboarding a new team member
- Standardizing development environments

## Step-by-Step Workflow

### Step 1: Project Init
**Skill**: `env-setup-guide`
- Initialize project structure
- Set up package.json / pyproject.toml
- Configure directory layout

### Step 2: Toolchain
**Skill**: `mise-configurator`
- Standardize Node/Python/Go versions
- Create `.mise.toml` or `.tool-versions`
- Ensure version consistency across team

### Step 3: Package Manager
**Skill**: `uv-package-manager`
- Configure dependency management
- Set up lock files
- Define scripts and tasks

### Step 4: Dev Container
**Skill**: `devcontainer-setup`
- Create `.devcontainer` config
- Define reproducible environment
- Include required tools and extensions

### Step 5: Editor Config
**Skill**: `devcontainer-setup`
- Set up `.editorconfig`
- Configure linters and formatters
- Define coding style rules

### Step 6: Git Hooks
**Skill**: `git-hooks-automation`
- Pre-commit: lint, format, type-check
- Commit-msg: enforce conventional commits
- Pre-push: run tests

### Step 7: Database
**Skill**: `database`
- Set up local database
- Run initial migrations
- Seed development data

### Step 8: Environment Vars
**Skill**: `secrets-management`
- Create `.env.example`
- Set up vault integration
- Document required variables

### Step 9: Documentation
**Skill**: `wiki-architect`
- Write README with setup instructions
- Create CONTRIBUTING guide
- Document architecture decisions

### Step 10: CI/CD
**Skill**: `github-actions-templates`
- Create first CI pipeline
- Configure build and test steps
- Set up deployment pipeline

## Completion

Dev environment is fully configured and reproducible. 🛠️

## Sub-Skills Referenced

1. `env-setup-guide`
2. `mise-configurator`
3. `uv-package-manager`
4. `devcontainer-setup`
5. `git-hooks-automation`
6. `database`
7. `secrets-management`
8. `wiki-architect`
9. `github-actions-templates`
