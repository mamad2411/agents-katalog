# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

This project uses Poetry for dependency management. All Python commands should be run with Poetry:

```bash
# Install dependencies
poetry install

# Run tests with coverage
poetry run pytest

# Run specific test file
poetry run pytest tests/unit/test_domain_models.py -v

# Run single test
poetry run pytest tests/unit/test_domain_models.py::TestWorkflow::test_workflow_creation -v

# Code formatting
poetry run black src tests

# Type checking
poetry run mypy src

# Linting
poetry run flake8 src tests

# Run the workflow engine CLI
poetry run workflow-engine run <workflow.yaml> --param_name=value --other_param=value

# Build the package
poetry build
```

## Architecture Overview

This is a **Generic Agentic Workflow Engine** built with **Clean Architecture** and **Domain-Driven Design (DDD)** principles. The system executes multi-step AI agent workflows defined in YAML files.

### Core Architecture Layers

1. **Domain Layer** (`src/workflow_engine/domain/`):
   - **Models**: Core business entities (`Workflow`, `Step`, `WorkflowExecutionContext`)
   - **Services**: Domain logic (`VariableSubstitutionService`, `IterationManagementService`, etc.)
   - **Events**: Rich domain event system for observability and auditing
   - **Exceptions**: Structured error hierarchy with context

2. **Application Layer** (`src/workflow_engine/application/`):
   - **Use Cases**: Orchestrates domain services (`ExecuteWorkflowUseCase`)
   - **DTOs**: Data transfer objects for external interfaces
   - **Services**: Application-level coordination

3. **Infrastructure Layer** (`src/workflow_engine/infrastructure/`):
   - **Agents**: AI agent implementations (Anthropic Claude integration)
   - **File System**: File operations and persistence
   - **Parsers**: YAML workflow definition parsing
   - **Persistence**: Data storage abstractions

### Key Domain Concepts

- **Workflow**: A collection of steps with execution settings (loop/single mode, timeouts, iterations)
- **Step**: Individual units of work executed by AI agents with variable substitution
- **WorkflowExecutionContext**: Aggregate root managing execution state across iterations
- **ExecutionMode**: `LOOP` (multi-iteration) or `SINGLE` (one-time execution)
- **Agent Types**: Different AI agents with fallback support and health checks

### Domain Events System

The system implements a comprehensive domain events architecture for observability:

- **Lifecycle Events**: `WorkflowStarted`, `WorkflowCompleted`, `WorkflowFailed`
- **Iteration Events**: `IterationStarted`, `IterationCompleted`, `IterationFailed`
- **Step Events**: `StepStarted`, `StepCompleted`, `StepFailed`
- **System Events**: `ExecutionTimedOut`, `ContextVariableUpdated`

Events support structured logging, metrics collection, audit trails, and notifications.

### Variable Substitution

Steps support dynamic variable substitution using:
- Workflow inputs: `${input_name}`
- Previous step outputs: `${step_id.output}`
- Cross-iteration context: Variables persist across iterations in LOOP mode

### File Processing

The engine supports file discovery and processing:
- Pattern-based file discovery (`file_patterns`)
- Iteration-based file processing chains
- Archiving and backup mechanisms
- File output validation

### Error Handling

Structured exception hierarchy with rich context:
- `WorkflowExecutionError`: Top-level workflow failures
- `AgentExecutionError`: AI agent-specific errors
- `IterationTimeoutError`: Timeout violations
- `FileOutputValidationError`: File validation failures

All exceptions include `ExecutionErrorContext` with workflow state for debugging.

## Configuration

### Environment Variables (.env)

Required environment variables:
```bash
ANTHROPIC_API_KEY=your_api_key_here
LOG_LEVEL=INFO
GENERATE_CONVERSATION_MARKDOWN=true
DEBUG_MODE=false
```

### Workflow Definition

Workflows are defined in YAML files with this structure:
```yaml
name: "workflow-name"
inputs:
  - name: "input_var"
    value: "default_value"
settings:
  execution_mode: "loop"  # or "single"
  max_iterations: 5
  max_duration: 3600
  max_duration_type: "seconds"
steps:
  - id: "step1"
    agent: "claude_sonnet"
    prompt: "Process ${input_var} and generate output"
    file_patterns: ["*.txt", "*.md"]
```

### Parameter Input Format

The workflow engine supports dynamic parameters that are automatically discovered from the workflow definition:

**Current Format (Recommended):**
```bash
# Parameters are specified directly as CLI options
poetry run workflow-engine run workflow.yaml --product_name="myproduct" --problem="example problem"

# Parameters correspond to the 'name' field in the workflow inputs section
```

**Legacy Format (NO LONGER SUPPORTED):**
```bash
# This format has been removed and will show an error
poetry run workflow-engine run workflow.yaml --input product_name=myproduct --input problem="example problem"
```

If you encounter the legacy format error, migrate to the new format by:
1. Remove `--input` and `-i` flags
2. Use parameter names directly as CLI options with `--parameter_name=value`
3. Ensure workflow inputs use the new format with `name` and `value` fields

## Dependency Injection

The system uses a custom DI container (`Container` class) that automatically resolves dependencies based on constructor type hints. Services are registered as singletons by default.

## Testing Strategy

- **Unit Tests**: Comprehensive coverage for domain models, services, and use cases
- **Test Structure**: Follows the same Clean Architecture layers as the source code
- **Mocking**: Uses `pytest-mock` for external dependencies
- **Coverage**: Configured for HTML and terminal reporting

The domain events system has particularly high test coverage (67-100% across components) demonstrating its critical importance to the system.

## Key Files to Understand

- `src/workflow_engine/main.py`: CLI entry point with workflow execution
- `src/workflow_engine/application/use_cases/execute_workflow.py`: Core workflow orchestration logic
- `src/workflow_engine/domain/models/execution_context.py`: Central state management aggregate
- `src/workflow_engine/domain/events/`: Complete domain events system
- `src/workflow_engine/container.py`: Dependency injection configuration
- use python-backend-engineer when writing any python code
- after every *.md file is created or modified, run a git commit and push with an appropriate message
- after every *.md file is created or modified, run a git add ., commit and push with an appropriate message. bypass permissions