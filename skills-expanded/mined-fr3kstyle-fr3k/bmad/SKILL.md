---
name: BMAD
description: Breakthrough Method of Agile AI-Driven Development. USE WHEN bmad, BMAD, agile development, spec-driven development, structured workflows. Universal AI agent framework with structured workflows, specialized agents, and spec-driven development.
---

# BMAD-METHOD Integration

BMAD (Breakthrough Method of Agile AI-Driven Development) is a universal AI agent framework providing structured workflows and specialized agents for AI-assisted development.

## Core Philosophy

BMAD transforms LLM capabilities through:
- **Structured Governance**: Agent-as-code architecture with defined roles
- **Spec-Driven Development (SDD)**: PRD-first approach with human-in-the-loop
- **Closed-Loop Workflow**: Analysis → Planning → Solutioning → Deployment
- **21 Specialized Agents**: Domain expert AI agents with clear responsibilities

## When to Use BMAD

Use BMAD when:
- User mentions "BMAD", "bmad", or "bmad method"
- Complex multi-agent collaboration is needed
- Structured development workflow is required
- PRD/spec-driven development approach fits the task
- Team-based AI development patterns would help
- Task requires architecture → development → QA flow

## BMAD Workflows

### Planning Workflow
**Triggers**: "plan", "architecture", "design system", "PRD"

Agents:
1. **Business Analyst** - Requirements gathering, stakeholder analysis
2. **Product Manager** - PRD creation, feature prioritization
3. **Architecture Specialist** - System design, tech stack decisions
4. **SME Agents** - Domain-specific expertise as needed

**Output**: One-page PRD, architecture document, implementation plan

### Development Workflow
**Triggers**: "implement", "build", "develop", "code"

Agents:
1. **Scrum Master (SM)** - Sprint planning, task breakdown
2. **Developer Agents** - Implementation by domain/stack
3. **QA Agent** - Testing strategy, test generation
4. **Review Agent** - Code review, quality checks

**Output**: Working code, tests, documentation

### Deployment Workflow
**Triggers**: "deploy", "release", "production"

Agents:
1. **DevOps Agent** - Deployment strategy, CI/CD
2. **Security Agent** - Security review, compliance
3. **Monitoring Agent** - Observability, alerts

**Output**: Deployed system, monitoring setup

## BMAD + FR3K Integration

BMAD workflows extend FR3K's Algorithm:
- **FR3K** provides the meta-framework (OBSERVE→LEARN)
- **BMAD** provides specialized agents and workflows for development tasks
- Use FR3K's ISC criteria to verify BMAD workflow outputs
- Apply FR3K's thinking tools (Council, FirstPrinciples) to BMAD agent decisions

## Hybrid Usage Pattern

When BMAD is invoked:
1. FR3K runs OBSERVE phase (reverse engineer intent)
2. Select appropriate BMAD workflow (Planning/Development/Deployment)
3. Invoke BMAD agents as specialized capabilities
4. FR3K runs VERIFY phase on BMAD outputs
5. FR3K runs LEARN phase to capture improvements

## Agent Invocation Syntax

```bash
# Planning workflow
/bmad plan [project description]

# Development workflow
/bmad develop [PRD or architecture spec]

# Full workflow (plan + develop)
/bmad full [idea or requirement]

# Direct agent invocation
/bmad agent [agent-name] [task]
```

## BMAD Agents Reference

**Planning Agents:**
- Business Analyst (BA) - Requirements, stakeholders
- Product Manager (PM) - PRD, features, roadmap
- Architecture Architect (AA) - System design, patterns
- UX Designer - User experience, interfaces
- Data Architect - Data modeling, databases

**Development Agents:**
- Scrum Master (SM) - Planning, coordination
- Frontend Dev - UI implementation
- Backend Dev - Server-side logic
- Fullstack Dev - End-to-end features
- DevOps Engineer - Infrastructure, CI/CD

**Quality Agents:**
- QA Engineer - Testing strategy, test plans
- Security Engineer - Security review, pentesting
- Code Reviewer - Code quality, best practices

**Specialist Agents:**
- Database Specialist - Query optimization, schema design
- API Specialist - API design, documentation
- Performance Engineer - Optimization, profiling
- Documentation Specialist - Docs, guides

## Examples

**User**: "Plan a real-time chat app"

**FR3K Response**:
```
🤖 FR3K ALGORITHM (with BMAD Planning)

🗒️ TASK: Design real-time chat application architecture

━━━ BMAD PLANNING WORKFLOW ━━━

Invoking: Business Analyst → Product Manager → Architecture Architect

[BA analyzes requirements: real-time messaging, users, scale]
[PM creates one-page PRD with features and priorities]
[AA designs WebSocket architecture, chooses tech stack]

✅ BMAD Output: PRD + Architecture Document
✅ FR3K Verify: ISC criteria met (scalability, real-time, testable)

🗣️ FR3K: Planning complete. Ready for development workflow.
```

## Learning Sources

- [BMAD-METHOD GitHub](https://github.com/bmad-code-org/BMAD-METHOD)
- [BMAD From Zero to Hero](https://medium.com/@visrow/bmad-method-from-zero-to-hero-1bf5203f2ecd)
- [GMO Engineer Blog](https://recruit.group.gmo/engineer/jisedai/blog/the-bmad-method-a-framework-for-spec-oriented-ai-driven-development/)

## Version

BMAD Integration v1.0 - Based on BMAD-METHOD v6.0.0-Beta.7 (Feb 2026)
