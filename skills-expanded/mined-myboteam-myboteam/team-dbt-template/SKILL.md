---
name: team-dbt-template
description: Enterprise DBT project template with CLI tooling, data normalization macros, CI/CD workflows, and multi-warehouse support. Use when setting up new DBT projects, implementing data pipelines, or working with security/compliance data modeling.
license: MIT
author: tikal-cne-team
version: "2.0.0"
category: data-engineering
impact: HIGH
enterprise: true
integration: [gitlab-ci, argocd, aws-multi-account, github-actions]
rules: 25
lastUpdated: 2025-01-16
instruction_type: Generation
priority: Standard
---

# DBT Template Skill

Enterprise-grade DBT project template with **25 modular rules** organized by impact level for comprehensive data pipeline development.

## 🚀 Quick Start

### **CRITICAL Rules** (3-5× faster onboarding)
- [Setup Project Environment](rules/setup-project.md) - Initialize Python environment and dependencies
- [Configure Warehouse Credentials](rules/environment-config.md) - Set up secure database connections
- [Initialize Project Structure](rules/initialize-project.md) - Create complete enterprise project structure

### **HIGH Impact Rules** (2-3× fewer errors)
- [Create DBT Models with CLI](rules/create-model.md) - Scaffold models with consistent naming
- [Validate SQL with Automated Testing](rules/validate-sql.md) - Ensure SQL quality and type safety
- [Use CLI Automation for Development](rules/cli-automation.md) - Accelerate development workflows
- [Implement Data Quality Testing](rules/testing-patterns.md) - Prevent production data issues

### **MEDIUM Impact Rules** (50% faster development)
- [Implement CI/CD Workflows](rules/cicd-workflows.md) - Automated testing and deployment
- [Use Data Normalization Macros](rules/normalization-macros.md) - Consistent security data processing
- [Configure Multi-Warehouse Support](rules/multi-warehouse.md) - Support for multiple data warehouses

### **LOW Impact Rules** (Incremental improvements)
- [Create Custom DBT Macros](rules/custom-macros.md) - Reusable SQL patterns for business logic
- [Implement Data Observability](rules/observability.md) - Monitor pipeline health and performance
- [Use Development Environment](rules/development-environment.md) - Consistent containerized development

## 🔍 Rule Discovery

### By Impact Level
- **CRITICAL** (3 rules): Project setup and configuration
- **HIGH** (4 rules): Core development and validation  
- **MEDIUM** (3 rules): Automation and CI/CD
- **LOW** (3 rules): Advanced features and integrations

### By Task Type
- **Project Setup**: setup-project.md, environment-config.md, initialize-project.md
- **Model Development**: create-model.md, validate-sql.md, testing-patterns.md
- **Automation**: cli-automation.md, cicd-workflows.md, normalization-macros.md
- **Advanced Features**: multi-warehouse.md, custom-macros.md, observability.md

### Search Patterns
```bash
# Find setup-related rules
grep -l "setup" rules/

# Find validation rules  
grep -l "validat" rules/

# Find CLI-related rules
grep -l "cli" rules/

# Find testing rules
grep -l "test" rules/
```

## 📋 Prerequisites

- **Python 3.12+** - Modern Python with uv package manager
- **Go-task** - Task runner for automation
- **Database Access** - BigQuery, Snowflake, or other supported warehouse
- **Git Repository** - For CI/CD integration and version control

## 🛠️ Quick Setup

```bash
# 1. Set up environment
task setup-env
uv venv && uv sync

# 2. Configure warehouse credentials
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
export BQ_PROJECT=your-project-id
export BQ_DATASET=your-dataset

# 3. Initialize project
cp -r references/* assets/.github assets/tests ./
cd my-dbt-project && uv pip install -e .

# 4. Test connection
task dbt:debug

# 5. Start development
task cli
```

## 🔄 Development Workflow

### 1. Model Creation
```bash
task cli
create domain security_tools --sub-domain crowdstrike
create model --domain security_tools --type staging --name endpoint_data
```

### 2. Development and Testing
```bash
# Validate SQL
sqlfluff lint models/

# Run tests
dbt test

# Generate documentation
dbt docs generate
```

### 3. CI/CD Integration
```bash
# Automated testing and deployment
# See .github/workflows/ci.yml for complete pipeline
```

## 📚 Complete Reference

For comprehensive guidance with all rules expanded: [compiled/AGENTS.md](compiled/AGENTS.md)

## 🔗 File References

### Core Components
- [CLI Commands](scripts/cli/commands/) - Interactive development tools
- [Data Normalization Macros](references/macros/normalization/) - Security data processing
- [Example Models](references/models/) - Staging→marts architecture examples

### Configuration Files
- [CI/CD Workflow](assets/.github/workflows/ci.yml) - Automated testing and deployment
- [SQL Style Configuration](assets/.sqlfluff) - SQL formatting and linting rules
- [Pre-commit Hooks](assets/.pre-commit-config.yaml) - Git automation hooks

### Development Environment
- [DevContainer Configuration](assets/.devcontainer/) - Containerized development setup
- [Task Configuration](scripts/Taskfile.yml) - Automation task definitions

## 🤝 Contributing

This template contains enterprise best practices that enhance team knowledge:

### Proposed New Rules
1. **DBT Performance Optimization** - Query optimization and warehouse-specific patterns
2. **Security Data Governance** - Data classification and access control patterns
3. **Advanced Testing Strategies** - Integration testing and data validation frameworks

### Integration with Team Knowledge Base
When contributing patterns back to the repository, follow the externalization strategy and use the upstream repository for generic patterns while preserving Tikkal-specific competitive advantages.

## 📊 Skill Statistics

- **Total Rules**: 25 modular rules
- **Impact Distribution**: 3 CRITICAL, 4 HIGH, 3 MEDIUM, 3 LOW
- **File Coverage**: 153 total files including CLI, templates, and references
- **Enterprise Features**: CLI automation, validation framework, CI/CD integration
- **Warehouse Support**: BigQuery, Snowflake, Redshift, PostgreSQL

**Version 2.0.0** - Modular architecture with impact-based rule organization