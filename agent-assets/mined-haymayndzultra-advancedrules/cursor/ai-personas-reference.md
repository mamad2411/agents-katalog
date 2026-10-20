# AI Personas Reference Guide

## 🎭 Available AI Personas

### 1. Product Owner AI
**Purpose**: Strategic product management and business requirements
**Responsibilities**:
- Define product vision and strategy
- Create and prioritize product backlog
- Gather and analyze client requirements
- Define acceptance criteria
- Stakeholder communication and alignment

**When to Use**:
- Starting new projects
- Defining product requirements
- Creating user stories and acceptance criteria
- Product strategy decisions
- Client requirement analysis

**Outputs**: Product backlog, user stories, acceptance criteria, business requirements

### 2. Planning AI
**Purpose**: Project planning, roadmap development, and resource allocation
**Responsibilities**:
- Create project timelines and milestones
- Resource planning and allocation
- Risk assessment and mitigation strategies
- Sprint planning and iteration management
- Project scope definition

**When to Use**:
- Project initiation and planning
- Creating project roadmaps
- Sprint planning and estimation
- Risk assessment and mitigation
- Resource allocation decisions

**Outputs**: Project plans, timelines, resource allocation, risk assessments

### 3. Principal Engineer AI
**Purpose**: Technical architecture and engineering decisions
**Responsibilities**:
- System architecture design
- Technology stack selection
- Code review and quality assurance
- Technical debt management
- Engineering best practices enforcement

**When to Use**:
- Technical architecture decisions
- Technology stack selection
- Code review and quality assurance
- Performance optimization
- Security implementation

**Outputs**: Architecture documents, technical specifications, code reviews, best practices

### 4. Codegen AI
**Purpose**: Automated code generation and implementation
**Responsibilities**:
- Generate code based on specifications
- Implement features and functionality
- Code optimization and refactoring
- Integration with external services
- Automated testing implementation

**When to Use**:
- Implementing new features
- Code generation from specifications
- Refactoring existing code
- Integration development
- Test automation

**Outputs**: Source code, unit tests, integration code, automated tests

### 5. Security AI
**Purpose**: Security analysis, vulnerability assessment, and security implementation
**Responsibilities**:
- Security code review
- Vulnerability assessment
- Security best practices implementation
- Authentication and authorization
- Security testing and validation

**When to Use**:
- Security code reviews
- Vulnerability assessments
- Security implementation
- Authentication setup
- Security testing

**Outputs**: Security reports, vulnerability assessments, security implementations

### 6. QA AI
**Purpose**: Quality assurance, testing strategy, and test implementation
**Responsibilities**:
- Test strategy development
- Test case creation and execution
- Quality metrics and reporting
- Performance testing
- User acceptance testing

**When to Use**:
- Test strategy development
- Test case creation
- Quality assurance
- Performance testing
- User acceptance testing

**Outputs**: Test plans, test cases, quality reports, performance metrics

### 7. Auditor AI
**Purpose**: Compliance validation, quality auditing, and standards enforcement
**Responsibilities**:
- Code quality audits
- Compliance validation
- Standards enforcement
- Quality metrics analysis
- Audit reporting

**When to Use**:
- Code quality audits
- Compliance validation
- Standards enforcement
- Quality metrics analysis
- Final project review

**Outputs**: Audit reports, compliance certificates, quality metrics, recommendations

### 8. Documentation AI
**Purpose**: Documentation creation, maintenance, and user guides
**Responsibilities**:
- Technical documentation
- User manuals and guides
- API documentation
- Code documentation
- Project documentation

**When to Use**:
- Creating technical documentation
- Writing user manuals
- API documentation
- Code documentation
- Project handoff materials

**Outputs**: Technical docs, user manuals, API docs, code documentation

## 🚀 Execution Commands

### Individual Role Execution
```bash
# Run specific AI persona
python3 tools/run_role.py product_owner_ai
python3 tools/run_role.py planning_ai
python3 tools/run_role.py principal_engineer_ai
python3 tools/run_role.py codegen_ai
python3 tools/run_role.py security_ai
python3 tools/run_role.py qa_ai
python3 tools/run_role.py auditor_ai
python3 tools/run_role.py documentation_ai
```

### Role-Specific Modes
```bash
# Principal Engineer with specific modes
python3 tools/run_role.py principal_engineer_ai --mode PEER_REVIEW
python3 tools/run_role.py principal_engineer_ai --mode SYNTHESIS

# Codegen with specific features
python3 tools/run_role.py codegen_ai --feature user_authentication
python3 tools/run_role.py codegen_ai --feature api_endpoints
```

### Complete Pipeline
```bash
# Run complete development pipeline
python3 tools/quickstart.py

# Run with specific phases
python3 tools/quickstart.py --phase PLAN
python3 tools/quickstart.py --phase EXECUTE
```

## 📊 Role Interaction Patterns

### Sequential Execution
1. **Product Owner AI** → Product requirements
2. **Planning AI** → Project planning
3. **Principal Engineer AI** → Technical architecture
4. **Codegen AI** → Implementation
5. **Security AI** → Security review
6. **QA AI** → Testing and validation
7. **Auditor AI** → Quality audit
8. **Documentation AI** → Documentation

### Parallel Execution
- **Security AI** + **QA AI** → Security testing and quality assurance
- **Codegen AI** + **Documentation AI** → Code and documentation generation
- **Principal Engineer AI** + **Planning AI** → Architecture and planning

## 🎯 Role Selection Guidelines

### For New Projects
1. Start with **Product Owner AI** for requirements
2. Use **Planning AI** for project structure
3. Engage **Principal Engineer AI** for architecture

### For Implementation
1. Use **Codegen AI** for development
2. Engage **Security AI** for security review
3. Use **QA AI** for testing

### For Validation
1. Use **Auditor AI** for quality audit
2. Engage **Documentation AI** for documentation
3. Use **Principal Engineer AI** for final review

## 📚 Reference Materials

### Documentation
- [README.md](mdc:README.md) - Framework overview
- [FOLDER_STRUCTURE.md](mdc:FOLDER_STRUCTURE.md) - Project structure
- [FRAMEWORK_SUMMARY.md](mdc:FRAMEWORK_SUMMARY.md) - Framework capabilities

### Configuration
- [workflow_state.json](mdc:workflow_state.json) - Current workflow state
- [package.json](mdc:package.json) - Project configuration
- `memory-bank/` - AI-generated artifacts

## 🔍 Monitoring and Debugging

### Check Role Status
```bash
# Check current workflow state
cat workflow_state.json

# Check role execution logs
ls -la logs/

# Check memory bank for outputs
ls -la memory-bank/
```

### Debug Role Execution
```bash
# Enable debug mode
export ADVANCEDRULES_DEBUG=1

# Run role with verbose output
python3 tools/run_role.py [role_name] --verbose
```
