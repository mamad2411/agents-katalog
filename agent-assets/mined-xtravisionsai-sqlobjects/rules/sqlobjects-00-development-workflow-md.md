# Development Workflow and Methodology

## Design-First Principle

**CRITICAL**: Any code modification must begin with text-based design analysis.

### New Feature Implementation Process

1. **Requirements Analysis**
   - Define the problem clearly and completely
   - Identify user needs and use cases
   - Determine success criteria and constraints

2. **Design Phase**
   - List multiple solution approaches with pros/cons
   - Detail key technical implementation points
   - Specify API design and integration points
   - Assess impact on existing code and users

3. **Implementation Planning**
   - Break down work into logical steps
   - Identify dependencies and prerequisites
   - Plan testing strategy and validation approach

4. **Code Implementation**
   - Follow the planned approach
   - Implement with tests and documentation
   - Validate against design requirements

### Architecture Iteration Process

1. **Current State Analysis**
   - Document existing architecture and limitations
   - Identify specific problems and pain points
   - Analyze performance and maintainability issues

2. **Problem Identification**
   - Root cause analysis of architectural issues
   - Impact assessment on users and development
   - Priority ranking of problems to solve

3. **Solution Design**
   - Multiple architectural approaches with trade-offs
   - Migration strategy and backward compatibility plan
   - Risk assessment and mitigation strategies

4. **Migration Planning**
   - Step-by-step migration approach
   - Rollback strategies and safety measures
   - Timeline and resource requirements

### Bug Fix Process

1. **Problem Reproduction**
   - Create minimal reproduction case
   - Document expected vs actual behavior
   - Identify affected components and versions

2. **Root Cause Analysis**
   - Trace the issue to its source
   - Understand why the problem occurred
   - Assess scope and potential side effects

3. **Fix Strategy Design**
   - Design the minimal fix approach
   - Consider alternative solutions
   - Plan for regression prevention

4. **Testing Plan**
   - Unit tests for the specific issue
   - Integration tests for affected workflows
   - Regression tests to prevent recurrence

## Design Documentation Requirements

### Problem Description
- Clear statement of what needs to be solved
- Context and background information
- Constraints and requirements

### Solution Analysis
- Multiple approaches considered
- Pros and cons of each approach
- Recommended solution with justification

### Implementation Details
- Key technical decisions and rationale
- API design and interface specifications
- Integration points and dependencies

### Impact Assessment
- Changes to existing APIs or behavior
- Migration requirements for users
- Performance and compatibility implications

### Validation Strategy
- How to verify the solution works
- Test cases and scenarios
- Success metrics and acceptance criteria

## Code Modification Workflow

### Phase 1: Text Design
- **Analysis**: Problem understanding and solution exploration
- **Design**: Detailed technical approach and specifications
- **Review**: Design validation and feedback incorporation

### Phase 2: Implementation Preparation
- **Planning**: Task breakdown and dependency mapping
- **Environment**: Development setup and tool preparation
- **Dependencies**: Required libraries and infrastructure

### Phase 3: Code Implementation
- **Coding**: Following the designed approach
- **Testing**: Unit and integration test implementation
- **Documentation**: Code comments and user documentation

### Phase 4: Validation and Release
- **Integration**: Merge with existing codebase
- **Verification**: End-to-end testing and validation
- **Deployment**: Release preparation and rollout

## Quality Gates

### Design Review Checklist
- [ ] Problem clearly defined and understood
- [ ] Multiple solutions considered
- [ ] Implementation approach detailed
- [ ] Impact assessment completed
- [ ] Testing strategy defined

### Implementation Review Checklist
- [ ] Code follows design specifications
- [ ] Tests cover all scenarios
- [ ] Documentation updated
- [ ] Backward compatibility maintained
- [ ] Performance impact assessed

### Release Readiness Checklist
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Migration guide provided (if needed)
- [ ] Rollback plan available
- [ ] Monitoring and alerting configured