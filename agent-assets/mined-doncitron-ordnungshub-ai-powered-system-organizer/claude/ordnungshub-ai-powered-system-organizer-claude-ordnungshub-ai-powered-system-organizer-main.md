# Claude Code Configuration - SPARC Development Environment

## Project Overview
This project uses the SPARC (Specification, Pseudocode, Architecture, Refinement, Completion) methodology for systematic Test-Driven Development with AI assistance through Claude-Flow orchestration.

## SPARC Development Commands

### Core SPARC Commands
- `npx claude-flow sparc modes`: List all available SPARC development modes
- `npx claude-flow sparc run <mode> "<task>"`: Execute specific SPARC mode for a task
- `npx claude-flow sparc tdd "<feature>"`: Run complete TDD workflow using SPARC methodology
- `npx claude-flow sparc info <mode>`: Get detailed information about a specific mode

### Standard Build Commands
- `npm run build`: Build the project
- `npm run test`: Run the test suite
- `npm run lint`: Run linter and format checks
- `npm run typecheck`: Run TypeScript type checking

## Test Automation Commands
### Batch Test Execution
- `test-all-functions.bat`: Run all tests
- `test-all-functions.bat generate`: Generate tests only
- `test-all-functions.bat execute`: Execute tests only
- `test-all-functions.bat target src/backend/services`: Test a specific directory

## SPARC Methodology Workflow

### 1. Specification Phase
Define clear functional requirements, edge cases, and acceptance criteria.

### 2. Pseudocode Phase
Break down complex logic into steps and plan data structures.

### 3. Architecture Phase
Design system architecture and component relationships.

### 4. Refinement Phase (TDD Implementation)
Execute Test-Driven Development cycle:
- **Red**: Write failing tests first
- **Green**: Implement minimal code to pass tests
- **Refactor**: Optimize and clean up code
- **Repeat**: Continue until feature is complete

### 5. Completion Phase
Integration testing, documentation, and validation.

## Important Notes
- Always run tests before committing (`npm run test`)
- Use SPARC memory system to maintain context across sessions
- Follow the Red-Green-Refactor cycle during TDD phases
- Document architectural decisions in memory for future reference
- Regular security reviews for any authentication or data handling code

For more information about SPARC methodology, see: https://github.com/ruvnet/claude-code-flow/docs/sparc.md