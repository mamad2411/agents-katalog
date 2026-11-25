---
name: code-generation
version: 1.0.0
description: Write code given specs — the implementation skill
uses:
  - development/architecture
  - development/testing
requires:
  tools: []
  env: []
security:
  risk_level: write
  capabilities:
    - file:write
  requires_approval: false
---

# Code Generation

Write code given specifications. This is the core implementation skill — translating requirements, designs, and specifications into working code that follows project conventions and best practices.

## Execution Model

This is an **agent-handled skill** (`handler: type: agent`). When `generate_code` is invoked, you (the agent) apply the methodology below using your reasoning capabilities. There is no backing code — you follow these instructions directly. The tool schema in tool.yaml defines the external contract; this document guides how you fulfill it.

## When to Use

- Implementing a feature from a specification or issue
- Writing a new module, class, or function
- Generating boilerplate or scaffolding
- Translating a design into working code
- Creating implementations that match an existing API contract

## Methodology

### 1. Understand the Specification

Before writing any code:
- **What**: What should the code do? (functional requirements)
- **How**: Are there specific patterns, frameworks, or APIs to use?
- **Where**: Where does this code go in the project structure?
- **Conventions**: What are the project's coding standards?
- **Constraints**: Performance, security, compatibility requirements

### 2. Study Existing Patterns

Before writing new code, read existing code in the project:
- How are similar things implemented?
- What naming conventions are used?
- What error handling patterns are used?
- What testing patterns are used?
- What import/dependency patterns are used?

**Match the project's style**, not your own preference. Consistency within a codebase is more important than personal preference.

### 3. Design Before Coding

Plan the implementation:
- What functions/classes/modules are needed?
- What are the inputs and outputs of each?
- What data structures are appropriate?
- What error cases need handling?
- How will this be tested?

### 4. Implement Incrementally

Write code in small, verifiable increments:
1. Start with the core logic (happy path)
2. Add error handling
3. Add edge case handling
4. Add input validation (at boundaries)
5. Add logging/observability (if appropriate)

### 5. Follow Code Quality Standards

Every piece of generated code should:
- **Be readable**: Clear variable names, consistent formatting
- **Be correct**: Handle all expected inputs and error cases
- **Be secure**: No injection vulnerabilities, proper input validation
- **Be testable**: Dependencies injectable, side effects isolated
- **Be minimal**: No speculative features, no unnecessary abstractions
- **Match conventions**: Follow the project's existing patterns

### 6. Write Accompanying Tests

Code generation is not complete without tests:
- Unit tests for the new code
- Edge case tests
- Error case tests
- Integration tests for interactions with existing code

### 7. Verify

After writing:
- Code compiles/parses without errors
- Tests pass
- Linter passes (if project uses one)
- Code integrates with existing modules

## Output Format

```
## Code Generation: [Feature/Module]

### Specification
- Purpose: [what the code does]
- Location: [where in the project]
- Convention: [patterns followed]

### Files Created/Modified
| File | Action | Description |
|------|--------|-------------|
| [path] | [created/modified] | [what it does] |

### Implementation Summary
- Core logic: [brief description]
- Error handling: [approach]
- Edge cases: [handled cases]

### Tests Written
| Test | What It Verifies |
|------|-----------------|
| [name] | [description] |

### Verification
- Compiles: [yes/no]
- Tests pass: [yes/no]
- Linter: [pass/fail/not-applicable]
```

## Quality Criteria

- Code matches the specification (does what was asked)
- Code follows project conventions (not personal style)
- Code is minimal (no speculative features or unnecessary abstractions)
- Code handles errors and edge cases
- Code is secure (input validation at boundaries, no injection)
- Accompanying tests are written
- Code compiles and tests pass

## Common Mistakes

- **Writing code before understanding the spec**: Starting to code before fully understanding what's needed leads to rework. Read the spec twice.
- **Ignoring project conventions**: Writing code in your preferred style instead of matching the project's existing patterns. Consistency matters more than preference.
- **Over-engineering**: Adding layers of abstraction, configuration, and extensibility for a simple feature. Write the minimum code that works correctly.
- **No tests**: Generating implementation code without tests. Tests are not optional — they're part of the implementation.
- **Ignoring error cases**: Only implementing the happy path. Real-world code encounters errors — handle them.
- **Not reading existing code first**: Writing a utility function when one already exists in the project. Search before creating.
- **Speculative generality**: Adding parameters, interfaces, or factory patterns "in case we need them later." YAGNI — You Aren't Gonna Need It.

## Completion

Code generation is complete when:
- Implementation matches the specification
- Code follows project conventions
- Error cases and edge cases are handled
- Tests are written and passing
- Code compiles/parses without errors
- Code integrates with the existing codebase
