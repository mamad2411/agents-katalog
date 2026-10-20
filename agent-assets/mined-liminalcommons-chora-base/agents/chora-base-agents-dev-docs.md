# Developer Documentation - Agent Awareness

**Domain**: Developer Documentation (dev-docs)
**Audience**: Developers working ON chora-base, contributors, AI agents
**Last Updated**: 2025-11-04

---

## Quick Reference

### What's in dev-docs?

This domain contains **development process documentation** for working on chora-base itself:

- **workflows/**: Complete development lifecycle processes
- **research/**: Technical investigations and learnings
- **patterns/**: Code patterns and best practices
- **examples/**: Code walkthroughs (future)
- **vision/**: Long-term capability roadmap (future)
- **explanation/**: Conceptual deep-dives (future)

### When to Use This Domain

**Use dev-docs when**:
- Contributing to chora-base codebase
- Understanding chora-base architecture
- Following development processes (TDD, BDD, DDD)
- Researching technical decisions

**Don't use dev-docs for**:
- Using chora-base as a template → See [../user-docs/](../user-docs/)
- Adopting SAPs → See [../skilled-awareness/](../skilled-awareness/)
- Project management → See [../project-docs/](../project-docs/)

---

## Common Workflows

### Workflow 1: Contributing to Chora-Base

**Steps**:
1. Read [workflows/DOCUMENTATION_MIGRATION_WORKFLOW.md](workflows/DOCUMENTATION_MIGRATION_WORKFLOW.md) for documentation standards
2. Check [patterns/](patterns/) for code patterns to follow
3. Read [research/](research/) for technical context
4. Implement feature following TDD/BDD/DDD workflows
5. Document learnings in research/ or patterns/

**Example**:
```bash
# 1. Read documentation workflow
cat docs/dev-docs/workflows/DOCUMENTATION_MIGRATION_WORKFLOW.md

# 2. Check patterns
ls docs/dev-docs/patterns/

# 3. Implement feature (TDD example)
# - Write failing test
# - Implement minimal code to pass
# - Refactor
# - Repeat

# 4. Document learnings
vim docs/dev-docs/research/new-learning.md
```

---

### Workflow 2: Understanding Chora-Base Architecture

**Steps**:
1. Read root [ARCHITECTURE.md](../../ARCHITECTURE.md) for 4-domain model
2. Read [research/CLAUDE_Complete.md](research/CLAUDE_Complete.md) for Claude-specific insights
3. Explore [patterns/](patterns/) for code organization
4. Review [workflows/](workflows/) for development processes

**Example**:
```bash
# 1. Read architecture
cat docs/ARCHITECTURE.md

# 2. Read Claude learnings
cat docs/dev-docs/research/CLAUDE_Complete.md

# 3. Check patterns
ls docs/dev-docs/patterns/

# 4. Review workflows
ls docs/dev-docs/workflows/
```

---

### Workflow 3: Setting Up Development Environment

**Steps**:
1. Clone repository
2. Install dependencies (Python, Node.js, Docker as needed)
3. Set up pre-commit hooks (SAP-006: quality-gates)
4. Run tests to verify setup
5. Read [workflows/](workflows/) for development process

**Example**:
```bash
# 1. Clone
git clone https://github.com/liminalcommons/chora-base.git
cd chora-base

# 2. Install Python dependencies (if needed)
pip install -e ".[dev]"

# 3. Set up pre-commit hooks
pre-commit install

# 4. Run tests
pytest

# 5. Read development workflow
cat docs/dev-docs/workflows/DOCUMENTATION_MIGRATION_WORKFLOW.md
```

---

### Workflow 4: Track Development Tasks with Beads (SAP-015)

**Steps**:
1. Check for unblocked tasks: `bd ready --json`
2. Claim task: `bd update {id} --status in_progress --assignee {your-name}`
3. Work on task using TDD/BDD/DDD workflows (from static-template)
4. Add progress comments: `bd comment {id} "Completed X, working on Y"`
5. Run quality gates before commit: `just pre-merge`
6. Close task: `bd close {id} --reason "Implemented and tested"`

**Example**:
```bash
# 1. Find work
bd ready --json
# Output: [{"id": "chora-base-abc", "title": "Add SAP-033", "priority": 0}]

# 2. Claim task
bd update chora-base-abc --status in_progress --assignee alice

# 3. Work on task (TDD workflow)
# - Write failing test
# - Implement feature
# - Run tests: pytest
# - Refactor

# 4. Add progress
bd comment chora-base-abc "Implemented authentication flow, adding tests"

# 5. Quality gates
just pre-merge  # Runs test + lint + format + type-check

# 6. Close task
bd close chora-base-abc --reason "Implemented SAP-033 authentication with 90% test coverage"
```

**Why Use Beads**: Persistent task memory across sessions eliminates context re-establishment. Perfect for multi-day features or bug fixes.

**Integration with Pre-Commit Hooks (SAP-006)**:
```bash
# Before commit, always run quality gates
just pre-merge

# If hooks fail, fix issues then re-run
ruff check --fix src/
mypy src/
just pre-merge

# Then commit
git add .
git commit -m "feat(sap-033): Add authentication capability"
```

---

### Workflow 5: Researching Technical Decisions

**Steps**:
1. Check [research/](research/) directory for existing investigations
2. Read relevant research documents
3. If no existing research, conduct investigation
4. Document findings in new research document

**Example**:
```bash
# 1. Search research directory
ls docs/dev-docs/research/

# 2. Read relevant research
cat docs/dev-docs/research/adopter-learnings-executable-docs.md

# 3. If conducting new research, create document
vim docs/dev-docs/research/new-investigation.md

# 4. Follow research template (explanation, findings, recommendations)
```

---

## Directory Structure

```
docs/dev-docs/
├── AGENTS.md                                  ← You are here
├── CLAUDE.md                                  ← Claude-specific patterns
├── README.md                                  ← Domain overview
│
├── workflows/                                 ← Development processes
│   └── DOCUMENTATION_MIGRATION_WORKFLOW.md    ← Documentation standards
│
├── patterns/                                  ← Code patterns
│   └── ... (patterns to be documented)
│
├── research/                                  ← Technical investigations
│   ├── CLAUDE_Complete.md                     ← Claude learnings
│   └── adopter-learnings-executable-docs.md   ← Executable docs insights
│
├── examples/                                  ← Code walkthroughs (future)
├── vision/                                    ← Roadmap (future)
└── explanation/                               ← Conceptual deep-dives (future)
```

---

## Key Files

### Workflows

**[workflows/DOCUMENTATION_MIGRATION_WORKFLOW.md](workflows/DOCUMENTATION_MIGRATION_WORKFLOW.md)**
- How to migrate docs to 4-domain structure (user-docs, dev-docs, project-docs, skilled-awareness)
- Diataxis framework application
- Frontmatter schema requirements

**Related**: See [static-template/dev-docs/workflows/](../../static-template/dev-docs/workflows/) for TDD, BDD, DDD workflows

---

### Research

**[research/CLAUDE_Complete.md](research/CLAUDE_Complete.md)**
- Claude-specific learnings from development
- Best practices for working with Claude Code
- Common pitfalls and solutions

**[research/adopter-learnings-executable-docs.md](research/adopter-learnings-executable-docs.md)**
- Insights from executable documentation approach
- Test extraction patterns
- How-To guide testing strategies

---

### Patterns

**[patterns/](patterns/)**
- Code organization patterns
- Best practices for chora-base development
- Reusable patterns across SAPs

---

## Development Processes

### TDD (Test-Driven Development)

**Process** (from static-template):
1. Write failing test
2. Implement minimal code to pass
3. Refactor
4. Repeat

**Reference**: [static-template/dev-docs/workflows/](../../static-template/dev-docs/workflows/)

---

### BDD (Behavior-Driven Development)

**Process** (from static-template):
1. Define behavior (Given-When-Then)
2. Write feature file
3. Implement step definitions
4. Run and verify

**Reference**: [static-template/dev-docs/workflows/](../../static-template/dev-docs/workflows/)

---

### DDD (Domain-Driven Design)

**Process** (from static-template):
1. Identify domain
2. Model domain entities
3. Define bounded contexts
4. Implement domain logic

**Reference**: [static-template/dev-docs/workflows/](../../static-template/dev-docs/workflows/)

---

## Diataxis Structure

This domain uses **Diataxis for development processes**:

| Type | Purpose | Location | Example |
|------|---------|----------|---------|
| **Tutorials** | Learning-oriented lessons | tutorials/ (future) | "Your first feature using DDD→BDD→TDD" |
| **How-To Guides** | Task-oriented instructions | workflows/ | "How to migrate documentation" |
| **Reference** | Information-oriented specs | reference/ (future) | "Workflow definitions" |
| **Explanation** | Understanding-oriented concepts | explanation/ (future) | "Why test-first development?" |

**Current Focus**: How-To guides (workflows/) and research documents

---

## Navigation Map

### By Task

**"I want to contribute code"**
→ Read [workflows/DOCUMENTATION_MIGRATION_WORKFLOW.md](workflows/DOCUMENTATION_MIGRATION_WORKFLOW.md)
→ Check [patterns/](patterns/) for code patterns
→ Follow TDD/BDD/DDD workflows from static-template

**"I want to understand architecture"**
→ Read [../../ARCHITECTURE.md](../../ARCHITECTURE.md)
→ Read [research/CLAUDE_Complete.md](research/CLAUDE_Complete.md)
→ Explore [patterns/](patterns/)

**"I want to document learnings"**
→ Add to [research/](research/) for investigations
→ Add to [patterns/](patterns/) for reusable patterns
→ Add to [examples/](examples/) for walkthroughs (future)

**"I want to understand technical decisions"**
→ Check [research/](research/) directory
→ Read relevant research documents
→ Conduct new investigation if needed

---

### By Subdomain

**Processes & Workflows**:
- [workflows/](workflows/) - Development lifecycle processes
- Static-template workflows: [../../static-template/dev-docs/workflows/](../../static-template/dev-docs/workflows/)

**Learnings & Insights**:
- [research/](research/) - Technical investigations
- [patterns/](patterns/) - Reusable code patterns

**Future Subdomain**:
- [examples/](examples/) - Code walkthroughs
- [vision/](vision/) - Long-term roadmap
- [explanation/](explanation/) - Conceptual deep-dives

---

## Integration with Other Domains

### With user-docs/

**Relationship**: dev-docs is about building chora-base, user-docs is about using it

**Example**:
- dev-docs: "How to implement a new SAP" (contributor guide)
- user-docs: "How to adopt SAP-015" (end-user guide)

---

### With project-docs/

**Relationship**: dev-docs provides processes, project-docs tracks execution

**Example**:
- dev-docs: "TDD workflow process"
- project-docs: "Sprint 3 plan: Implement SAP-015 using TDD"

---

### With skilled-awareness/

**Relationship**: dev-docs explains how to build SAPs, skilled-awareness contains the SAPs

**Example**:
- dev-docs: "SAP artifact requirements (5 artifacts, Diataxis)"
- skilled-awareness: "SAP-015 task-tracking (5 complete artifacts)"

---

## Troubleshooting

### Issue: Can't find development process

**Solution**:
```bash
# Check workflows directory
ls docs/dev-docs/workflows/

# Check static-template for TDD/BDD/DDD workflows
ls static-template/dev-docs/workflows/

# Search research for insights
grep -r "{keyword}" docs/dev-docs/research/
```

---

### Issue: Don't understand technical decision

**Solution**:
```bash
# Check research directory
ls docs/dev-docs/research/

# Read relevant research document
cat docs/dev-docs/research/{document}.md

# If not documented, check git history
git log --all --grep="{keyword}"
```

---

### Issue: Code pattern unclear

**Solution**:
```bash
# Check patterns directory
ls docs/dev-docs/patterns/

# Search existing code for examples
grep -r "{pattern}" .

# Check static-template for reference implementation
ls static-template/
```

---

## Key Commands

```bash
# Development setup
pip install -e ".[dev]"
pre-commit install
pytest

# Documentation
cat docs/dev-docs/workflows/DOCUMENTATION_MIGRATION_WORKFLOW.md
ls docs/dev-docs/research/

# Code patterns
ls docs/dev-docs/patterns/
grep -r "{pattern}" static-template/

# Architecture
cat docs/ARCHITECTURE.md
cat docs/dev-docs/research/CLAUDE_Complete.md
```

---

## Support & Resources

**Development Workflows**:
- [workflows/](workflows/) - Chora-base specific processes
- [static-template/dev-docs/workflows/](../../static-template/dev-docs/workflows/) - TDD, BDD, DDD

**Technical Context**:
- [research/](research/) - Investigations and learnings
- [patterns/](patterns/) - Reusable code patterns

**Architecture**:
- [../../ARCHITECTURE.md](../../ARCHITECTURE.md) - 4-domain model
- [../../README.md](../../README.md) - Project overview

**Related Domains**:
- [../user-docs/](../user-docs/) - End-user documentation
- [../project-docs/](../project-docs/) - Project management
- [../skilled-awareness/](../skilled-awareness/) - SAP capabilities

**Claude-Specific**:
- [CLAUDE.md](CLAUDE.md) - Claude patterns for development
- [research/CLAUDE_Complete.md](research/CLAUDE_Complete.md) - Claude learnings

---

## Version History

- **1.0.0** (2025-11-04): Initial domain AGENTS.md for dev-docs
  - Development workflow navigation
  - Research and patterns discovery
  - Integration with other domains
  - Diataxis structure for development processes
  - Troubleshooting guide

---

**Next Steps**:
1. Read [workflows/](workflows/) for development processes
2. Check [research/](research/) for technical context
3. Explore [patterns/](patterns/) for code patterns
4. Read [CLAUDE.md](CLAUDE.md) for Claude-specific development patterns
5. Contribute learnings back to research/ or patterns/
