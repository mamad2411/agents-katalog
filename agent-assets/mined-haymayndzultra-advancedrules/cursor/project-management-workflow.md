# Project Management & Workflow

## 📋 Project Lifecycle Management

### 1. PRE-START Phase
**Purpose**: Validate project readiness and business requirements
**Key Activities**:
- Client screening and scoring
- Capacity planning and availability assessment
- Pricing strategy and rate card setup
- Risk assessment and mitigation planning
- Proposal development and client approval

**AI Personas**: Client Screener, Capacity Planner, Pricing Policy, Risk Catalog
**Outputs**: `memory-bank/business/*`, `memory-bank/plan/proposal.md`
**Success Criteria**: All business artifacts complete, client approval received

### 2. PLAN Phase
**Purpose**: Strategic planning and technical architecture
**Key Activities**:
- Product requirements and backlog creation
- Technical architecture design and validation
- Project roadmap and milestone planning
- Resource allocation and timeline development
- Technology stack selection and justification

**AI Personas**: Product Owner AI, Planning AI, Principal Engineer AI
**Outputs**: `memory-bank/plan/*`, technical specifications, architecture docs
**Success Criteria**: Complete project plan, approved architecture, defined timeline

### 3. EXECUTE Phase
**Purpose**: Code generation and implementation
**Key Activities**:
- Automated code generation based on specifications
- Security review and vulnerability assessment
- Quality assurance testing and validation
- Performance optimization and monitoring
- Integration testing and deployment preparation

**AI Personas**: Codegen AI, Security AI, QA AI
**Outputs**: Source code, test results, security reports, deployment packages
**Success Criteria**: All features implemented, tests passing, security validated

### 4. AUDIT Phase
**Purpose**: Quality assurance and compliance validation
**Key Activities**:
- Code quality audit and review
- Security vulnerability assessment
- Compliance validation against standards
- Performance benchmarking and optimization
- Documentation completeness validation

**AI Personas**: Auditor AI, Security AI, QA AI
**Outputs**: Audit reports, compliance certificates, quality metrics, recommendations
**Success Criteria**: Quality gates passed, compliance validated, performance targets met

### 5. DELIVER Phase
**Purpose**: Project handoff and documentation
**Key Activities**:
- Comprehensive documentation creation
- Deployment preparation and execution
- Client handoff materials preparation
- Training and knowledge transfer
- Project closure and lessons learned

**AI Personas**: Documentation AI, Principal Engineer AI
**Outputs**: User manuals, deployment guides, handoff documents, project closure report
**Success Criteria**: Successful deployment, client acceptance, project closure

## 🚀 Workflow Execution

### Automated Pipeline Execution
```bash
# Complete development pipeline
python3 tools/quickstart.py

# Phase-specific execution
python3 tools/quickstart.py --phase PLAN
python3 tools/quickstart.py --phase EXECUTE
python3 tools/quickstart.py --phase AUDIT
```

### Manual Role Execution
```bash
# Individual AI persona execution
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

## 📊 Project Monitoring & Tracking

### Workflow State Management
- **Current State**: Tracked in [workflow_state.json](mdc:workflow_state.json)
- **Phase Transitions**: Automatic state updates based on completion criteria
- **Progress Tracking**: Monitor completion of each phase and deliverables
- **Gate Validation**: Ensure all requirements are met before phase transitions

### Memory Bank Monitoring
```bash
# Check current project state
cat workflow_state.json

# Monitor memory bank contents
ls -la memory-bank/
ls -la memory-bank/plan/
ls -la memory-bank/business/
ls -la memory-bank/reports/
```

### Progress Indicators
- **Phase Completion**: Track completion percentage for each phase
- **Deliverable Status**: Monitor status of key deliverables
- **Quality Metrics**: Track code quality, test coverage, security scores
- **Timeline Adherence**: Monitor progress against planned timeline

## 🎯 Decision Making & Orchestration

### Decision Scoring System
```bash
# Score decision candidates
python3 tools/decision_scoring/advanced_score.py

# Check decision results
cat decision_candidates.json
```

### Decision Gates
- **PRE-START Gate**: All business artifacts complete
- **PLAN Gate**: Project plan approved, architecture validated
- **EXECUTE Gate**: Implementation complete, tests passing
- **AUDIT Gate**: Quality gates passed, compliance validated
- **DELIVER Gate**: Client acceptance, deployment successful

### Orchestration Logic
- **Sequential Execution**: Phases execute in order with gate validation
- **Parallel Execution**: Independent tasks execute simultaneously
- **Adaptive Execution**: Adjust execution based on feedback and results
- **Error Handling**: Graceful failure handling and recovery

## 📈 Project Metrics & KPIs

### Development Metrics
- **Velocity**: Features completed per sprint/iteration
- **Quality**: Bug count, test coverage, security score
- **Performance**: Response time, throughput, resource usage
- **Timeline**: On-time delivery, milestone achievement

### Business Metrics
- **Client Satisfaction**: Feedback scores, acceptance rates
- **Cost Efficiency**: Budget adherence, resource utilization
- **Risk Management**: Risk mitigation success, issue resolution time
- **Stakeholder Communication**: Communication frequency, clarity

### Technical Metrics
- **Code Quality**: Complexity, maintainability, technical debt
- **Security**: Vulnerability count, security score, compliance status
- **Performance**: Response time, scalability, resource efficiency
- **Reliability**: Uptime, error rates, recovery time

## 🔄 Iterative Improvement

### Sprint Planning
- **Sprint Duration**: 1-2 weeks for rapid feedback
- **Sprint Goals**: Clear objectives and success criteria
- **Sprint Review**: Evaluate progress and gather feedback
- **Sprint Retrospective**: Identify improvements and lessons learned

### Continuous Improvement
- **Process Optimization**: Refine workflows based on experience
- **Tool Enhancement**: Improve tools and automation
- **Knowledge Sharing**: Document lessons learned and best practices
- **Skill Development**: Enhance team capabilities and expertise

### Feedback Loops
- **Client Feedback**: Regular client communication and feedback
- **Team Feedback**: Internal team feedback and improvement suggestions
- **Process Feedback**: Workflow effectiveness and efficiency feedback
- **Quality Feedback**: Quality metrics and improvement opportunities

## 🛠️ Project Management Tools

### Framework Tools
- **Runner**: `tools/run_role.py` - Execute AI personas
- **Orchestrator**: `tools/quickstart.py` - Complete pipeline execution
- **Decision Scoring**: `tools/decision_scoring/advanced_score.py` - Score decisions
- **State Management**: `tools/orchestrator/state.py` - Workflow state management

### Monitoring Tools
- **Observability**: `tools/observability/aggregate.py` - Metrics aggregation
- **Artifact Tracking**: `tools/artifacts/hash_index.py` - Artifact management
- **Rule Attachment**: `tools/rule_attach/detect.py` - Rule application tracking
- **Logging**: `logs/` directory - Comprehensive execution logs

### External Tools Integration
- **Version Control**: Git for source code management
- **Issue Tracking**: GitHub Issues or similar for task management
- **CI/CD**: GitHub Actions or similar for automation
- **Documentation**: Markdown for documentation management

## 📚 Reference Materials

### Documentation
- [README.md](mdc:README.md) - Framework overview and setup
- [FOLDER_STRUCTURE.md](mdc:FOLDER_STRUCTURE.md) - Project structure
- [FRAMEWORK_SUMMARY.md](mdc:FRAMEWORK_SUMMARY.md) - Framework capabilities
- [UPWORK_IMPLEMENTATION_GUIDE.md](mdc:UPWORK_IMPLEMENTATION_GUIDE.md) - Upwork integration

### Configuration Files
- [workflow_state.json](mdc:workflow_state.json) - Current workflow state
- [package.json](mdc:package.json) - Project configuration
- [action_envelope.json](mdc:action_envelope.json) - Action execution context
- [decision_candidates.json](mdc:decision_candidates.json) - Decision candidates

### Memory Bank Structure
- `memory-bank/plan/` - Project plans and specifications
- `memory-bank/business/` - Business artifacts and requirements
- `memory-bank/reports/` - Generated reports and findings
- `memory-bank/upwork/` - Upwork-specific data and status

## 🎯 When to Use Project Management

- Starting new software development projects
- Managing project lifecycle and phases
- Coordinating multiple AI personas and tasks
- Monitoring project progress and quality
- Making project decisions and trade-offs
- Planning and executing project deliverables
- Managing client relationships and expectations
- Implementing continuous improvement processes
description:
globs:
alwaysApply: true
---
