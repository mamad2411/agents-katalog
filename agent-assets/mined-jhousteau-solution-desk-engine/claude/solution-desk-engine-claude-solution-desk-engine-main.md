# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Essential Commands
- `make setup` - Install dependencies and set up development environment (includes pre-commit hooks)
- `make test` - Run tests
- `make test-cov` - Run tests with coverage reporting
- `make quality` - Run all quality checks (format, lint, typecheck)
- `make run-dev` - Run the CLI in development mode

### Quality Assurance
- `make format` - Format code with black and isort
- `make typecheck` - Type check with mypy
- `poetry run ruff check src/ tests/ --fix` - Lint and auto-fix with ruff

### Testing
- `poetry run pytest` - Run all tests
- `poetry run pytest tests/specific_test.py` - Run a single test file
- `poetry run pytest -k test_name` - Run specific test by name
- `poetry run pytest --cov --cov-fail-under=75` - Coverage enforcement (75% minimum per pyproject.toml)

## Project Architecture

This is a **technical sales solutioning framework** built as a Python CLI application with Genesis integration. The framework implements a comprehensive 11-phase methodology for cloud consulting engagements.

### Core Architecture Components

**Framework Core** (`src/solution_desk_engine/framework/`):
- Framework infrastructure ready for 11-phase methodology implementation
- Progress tracking and document management architecture in place

**Document Management** (`src/solution_desk_engine/`):
- `export/document_exporter.py` - Multi-format export (PDF, DOCX, HTML, Markdown) with Pandoc integration
- `quality/validator.py` - Document validation with citation enforcement and quality scoring
- `config/project_config.py` - YAML-based project configuration and settings

**CLI Interface** (`src/solution_desk_engine/cli.py`):
- Click-based commands with Rich terminal styling
- Entry point: `solution-desk-engine` command via poetry.scripts

### Technical Sales Methodology

The framework is designed around an **11-phase comprehensive methodology** for technical sales solutioning:
- **Foundation Phase**: Initial project setup and requirements gathering
- **Analysis Phase**: Deep dive into technical and business requirements
- **Design Phase**: Solution architecture and technical design
- **Validation Phase**: Proof of concept and technical validation
- **Costing Phase**: Financial modeling and pricing analysis
- **Proposal Phase**: Comprehensive proposal development
- **Presentation Phase**: Executive and technical presentations
- **Negotiation Phase**: Contract and commercial discussions
- **Implementation Phase**: Solution deployment planning
- **Delivery Phase**: Project execution and delivery
- **Closure Phase**: Project wrap-up and lessons learned

The methodology is currently in development with document templates and validation rules being implemented.

## Code Quality Standards

The project enforces strict code quality through pre-commit hooks:
- **MyPy**: 100% strict type checking compliance (all methods require type annotations)
- **Black** (line-length=88) for code formatting
- **Ruff** for linting with auto-fix
- **isort** for import sorting
- **Bandit** for security scanning
- **detect-secrets** for credential scanning with baseline file
- **Test Coverage**: 75% minimum enforced (configured in pyproject.toml)

## Development Environment

- Python 3.11+ required
- Uses Poetry for virtual environment and dependency management
- Pre-commit hooks automatically run quality checks
- File organization is enforced via Genesis standards (scripts/check-file-organization.sh)

## Framework-Specific Development Notes

### Key Implementation Patterns
- **Dataclass + Enums**: All framework entities use `@dataclass` with typed enum properties
- **Progress Persistence**: JSON-based progress tracking in `.solution-desk-engine/progress.json`
- **Multi-Format Export**: Primary export via Pandoc with fallback strategies (weasyprint for PDF, python-docx for DOCX)
- **Validation Pipeline**: Citation enforcement for financial data, professional tone checking, structure validation

### Working with the Framework
- Framework implements comprehensive 11-phase methodology for technical sales
- Configuration system supports YAML-based project settings via `ProjectConfiguration`
- Quality validation and export infrastructure ready for full implementation
- Agent orchestration system with 26 specialized agents for dynamic team formation

## Containerization

The project includes Docker containerization for consistent development and deployment:

### Docker Commands
- `docker build -t solution-desk-engine .` - Build Docker image
- `docker-compose up` - Start containerized environment
- `docker-compose down` - Stop and remove containers

### Container Architecture
- Multi-stage Dockerfile with Python 3.11 Alpine base
- Poetry-based dependency management in containers
- Development and production configurations via docker-compose
- Volume mounts for local development workflow

## Agent Orchestration System

This project implements a sophisticated **Dynamic Team Formation** pattern for agent management:

### Core Architecture
- **26 Specialized Agents**: Complete library of domain experts across all 11 phases
- **Dynamic Selection**: Orchestrator forms optimal 5-6 agent teams for specific tasks
- **Context Efficiency**: Small active teams preserve context window and prevent decision paralysis
- **Agent Library**: Located in `/docs/guides/agents/` with professional system prompts

### Key Agent Categories
- **Core Agents**: business-analyst, project-manager (always available)
- **Discovery Specialists**: solution-architect-gcp, vertex-ai-specialist, domain-expert
- **Business Case Team**: financial-analyst, gcp-pricing-specialist
- **Architecture Team**: vertex-ai-architect, security-architect, data-architect
- **Implementation Team**: devops-engineer-gcp, ml-engineer, qa-lead
- **Commercial Team**: proposal-writer, legal-counsel, commercial-manager

### Architecture Reference
See `/docs/guides/agent-orchestration-architecture.md` for comprehensive documentation on:
- Team formation algorithms and selection criteria
- Context management and handoff protocols
- Agent design principles and best practices
- Phase-based and task-specific team compositions

## Opportunity Management

### Project Structure
Projects follow the pattern: `/opportunities/{client}/{project-name}/`

Example: `/opportunities/penske/franchise-lease-management/`
- `0-source/` - Source materials and document inventory
- `research-documents-config.yaml` - YAML configuration for document generation
- `research-documents-status.yaml` - Progress tracking for document creation

### Working with Opportunities
- Use YAML configuration files to define which documents to create per phase
- Progress tracking automatically maintains status across all 11 phases
- Document templates support comprehensive technical sales methodology

## Genesis Integration

This project uses Genesis CLI features:
- `make genesis-commit` - Smart commit with quality gates
- `make worktree-create NAME=feature-name` - Create AI-safe worktrees
- Genesis file organization checking is enforced via hooks

# important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.
