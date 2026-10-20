# User Documentation - Agent Awareness

**Domain**: User Documentation (user-docs)
**Audience**: End-users consuming chora-base, adopters, operators
**Last Updated**: 2025-11-04

---

## Quick Reference

### What's in user-docs?

This domain contains **end-user product documentation** using Diataxis framework:

- **how-to/**: Task-oriented guides (problem-solving)
- **tutorials/**: Learning-oriented lessons (skill acquisition)
- **reference/**: Information-oriented specs (fact lookup)
- **explanation/**: Understanding-oriented concepts (conceptual clarity)
- **guides/**: End-user getting started guides
- **troubleshooting/**: Problem diagnosis and resolution

### When to Use This Domain

**Use user-docs when**:
- Adopting chora-base as a template
- Learning how to use chora-base features
- Looking up technical specifications
- Understanding chora-base concepts

**Don't use user-docs for**:
- Contributing to chora-base codebase → See [../dev-docs/](../dev-docs/)
- Adopting specific SAPs → See [../skilled-awareness/](../skilled-awareness/)
- Project management → See [../project-docs/](../project-docs/)

---

## Common Workflows

### Workflow 1: New Adopter Onboarding

**Steps**:
1. Read [explanation/benefits-of-chora-base.md](explanation/benefits-of-chora-base.md) to understand value
2. Read [../../ARCHITECTURE.md](../../ARCHITECTURE.md) for 4-domain model
3. Follow tutorials/ for hands-on learning (when available)
4. Use how-to/ guides for specific tasks

**Example**:
```bash
# 1. Understand benefits
cat docs/user-docs/explanation/benefits-of-chora-base.md

# 2. Understand architecture
cat docs/ARCHITECTURE.md

# 3. Check available tutorials
ls docs/user-docs/tutorials/

# 4. Find relevant how-to guide
ls docs/user-docs/how-to/
cat docs/user-docs/how-to/{relevant-guide}.md
```

---

### Workflow 2: Adopting Chora-Base for a Project

**Steps**:
1. Read [explanation/benefits-of-chora-base.md](explanation/benefits-of-chora-base.md)
2. Check [../../README.md](../../README.md) for installation
3. Follow project bootstrap guide (SAP-003)
4. Customize templates to fit project needs
5. Deploy using Docker (SAP-011) if needed

**Example**:
```bash
# 1. Understand benefits
cat docs/user-docs/explanation/benefits-of-chora-base.md

# 2. Read installation
cat README.md

# 3. Bootstrap project (see SAP-003)
cd docs/skilled-awareness/project-bootstrap/
cat adoption-blueprint.md

# 4. Customize templates
cp -r static-template/ ../my-project/
vim ../my-project/PROJECT_CONFIG.yaml

# 5. Deploy (if needed)
cd docs/skilled-awareness/docker-operations/
cat adoption-blueprint.md
```

---

### Workflow 3: Using Specific Features

**Steps**:
1. Navigate to how-to/ directory
2. Find relevant task guide
3. Follow step-by-step instructions
4. Check reference/ for technical details if needed
5. Read explanation/ for conceptual understanding

**Example (Setup MCP Ecosystem)**:
```bash
# 1. Navigate to how-to
cd docs/user-docs/how-to/

# 2. Find MCP setup guide
ls | grep mcp

# 3. Follow guide
cat setup-mcp-ecosystem.md

# 4. Check reference (if needed)
ls docs/user-docs/reference/

# 5. Understand concepts
cat docs/user-docs/explanation/multi-repo-capability-evolution.md
```

---

### Workflow 4: Troubleshooting Issues

**Steps**:
1. Check [troubleshooting/](troubleshooting/) directory
2. Read relevant troubleshooting guide
3. If not found, check SAP-specific troubleshooting in [../skilled-awareness/](../skilled-awareness/)
4. Search documentation for error messages
5. Consult explanation/ for conceptual clarity

**Example**:
```bash
# 1. Check troubleshooting
ls docs/user-docs/troubleshooting/

# 2. Read relevant guide
cat docs/user-docs/troubleshooting/{issue}.md

# 3. Check SAP troubleshooting (if SAP-related)
cd docs/skilled-awareness/{sap-name}/
cat adoption-blueprint.md  # Look for "Troubleshooting" section

# 4. Search for error
grep -r "{error_message}" docs/

# 5. Understand concept
cat docs/user-docs/explanation/{concept}.md
```

---

## Directory Structure

```
docs/user-docs/
├── AGENTS.md                                  ← You are here
├── CLAUDE.md                                  ← Claude-specific patterns
├── README.md                                  ← Domain overview
│
├── how-to/                                    ← Task-oriented guides
│   ├── write-executable-documentation.md      ← Executable how-tos
│   ├── setup-mcp-ecosystem.md                 ← MCP setup
│   └── ... (11 how-to guides)
│
├── tutorials/                                 ← Learning-oriented lessons
│   └── ... (to be populated)
│
├── reference/                                 ← Technical specifications
│   └── ... (8 reference docs)
│
├── explanation/                               ← Conceptual understanding
│   ├── benefits-of-chora-base.md              ← Value proposition
│   ├── architecture-clarification.md          ← Architecture concepts
│   ├── multi-repo-capability-evolution.md     ← Multi-repo patterns
│   └── ... (5 explanation docs)
│
├── guides/                                    ← Getting started guides
│   └── ... (10 guides)
│
└── troubleshooting/                           ← Problem resolution
    └── ... (troubleshooting guides)
```

---

## Key Files

### Getting Started

**[explanation/benefits-of-chora-base.md](explanation/benefits-of-chora-base.md)**
- Why use chora-base?
- Value proposition for adopters
- Comparison with alternatives

**[../../README.md](../../README.md)**
- Project overview
- Installation instructions
- Quick start guide

**[../../ARCHITECTURE.md](../../ARCHITECTURE.md)**
- 4-domain model (user-docs, dev-docs, project-docs, skilled-awareness)
- Architectural principles
- Diataxis framework application

---

### How-To Guides (Task-Oriented)

**[how-to/write-executable-documentation.md](how-to/write-executable-documentation.md)**
- How to write executable how-to guides
- Test extraction patterns
- Frontmatter schema

**[how-to/setup-mcp-ecosystem.md](how-to/setup-mcp-ecosystem.md)**
- How to set up MCP (Model Context Protocol) ecosystem
- Claude Desktop integration
- MCP server configuration

**Other How-Tos**: See [how-to/](how-to/) directory (11 guides)

---

### Explanation (Conceptual)

**[explanation/architecture-clarification.md](explanation/architecture-clarification.md)**
- Architectural concepts clarified
- Design principles explained
- Rationale for 4-domain model

**[explanation/multi-repo-capability-evolution.md](explanation/multi-repo-capability-evolution.md)**
- Multi-repo patterns
- Capability evolution strategies
- Cross-repo coordination (SAP-001)

---

### Reference (Technical Specs)

**[reference/](reference/)**
- Technical specifications
- Configuration schemas
- API documentation

**Note**: Many reference docs are in static-template/user-docs/reference/ as examples

---

### Tutorials (Learning-Oriented)

**[tutorials/](tutorials/)**
- Structured learning lessons
- "Your First..." style guides
- Hands-on skill acquisition

**Note**: To be populated in future waves

---

## Diataxis Structure

| Type | Purpose | Audience | Example |
|------|---------|----------|---------|
| **Tutorials** | Learning skills | Newcomers | "Your First Chora-Base Project" |
| **How-To** | Solving problems | Practitioners | "How to Install SAP-004" |
| **Reference** | Looking up facts | Implementers | "SAP Protocol Specification" |
| **Explanation** | Understanding | Learners | "4-Domain Architecture Explained" |

**Guides**: Hybrid category for getting started guides (combines tutorial + how-to)

**Troubleshooting**: Problem-specific resolution guides (combines how-to + reference)

---

## Navigation Map

### By Task

**"I'm new to chora-base"**
→ Read [explanation/benefits-of-chora-base.md](explanation/benefits-of-chora-base.md)
→ Read [../../ARCHITECTURE.md](../../ARCHITECTURE.md)
→ Follow tutorials/ (when available)

**"I want to bootstrap a project"**
→ Read [../../README.md](../../README.md)
→ Follow [../skilled-awareness/project-bootstrap/adoption-blueprint.md](../skilled-awareness/project-bootstrap/adoption-blueprint.md)

**"I want to set up MCP"**
→ Follow [how-to/setup-mcp-ecosystem.md](how-to/setup-mcp-ecosystem.md)

**"I want to write executable docs"**
→ Follow [how-to/write-executable-documentation.md](how-to/write-executable-documentation.md)

**"I want to understand architecture"**
→ Read [explanation/architecture-clarification.md](explanation/architecture-clarification.md)
→ Read [../../ARCHITECTURE.md](../../ARCHITECTURE.md)

**"I have an issue"**
→ Check [troubleshooting/](troubleshooting/)
→ Check SAP-specific troubleshooting in [../skilled-awareness/](../skilled-awareness/)

---

### By Diataxis Type

**Learning** (Tutorials):
- [tutorials/](tutorials/) - Structured learning lessons

**Problem-Solving** (How-To):
- [how-to/](how-to/) - Task-oriented guides (11 guides)

**Information** (Reference):
- [reference/](reference/) - Technical specifications (8 docs)

**Understanding** (Explanation):
- [explanation/](explanation/) - Conceptual clarity (5 docs)

**Hybrid**:
- [guides/](guides/) - Getting started guides (10 guides)
- [troubleshooting/](troubleshooting/) - Problem resolution

---

## Integration with Other Domains

### With skilled-awareness/

**Relationship**: user-docs is for using chora-base, skilled-awareness is for adopting SAPs

**Example**:
- user-docs: "How to use chora-base templates" (general)
- skilled-awareness: "How to adopt SAP-015 task-tracking" (specific capability)

**Navigation**: For SAP-specific tasks, navigate to [../skilled-awareness/{sap-name}/adoption-blueprint.md](../skilled-awareness/)

---

### With dev-docs/

**Relationship**: user-docs is for using chora-base, dev-docs is for building it

**Example**:
- user-docs: "How to bootstrap a project with chora-base"
- dev-docs: "How to contribute to chora-base codebase"

---

### With project-docs/

**Relationship**: user-docs provides capabilities, project-docs tracks how they're used in project

**Example**:
- user-docs: "Benefits of chora-base"
- project-docs: "Sprint 3: Adopt chora-base for new service"

---

## Troubleshooting

### Issue: Can't find relevant guide

**Solution**:
```bash
# Search by keyword
grep -r "{keyword}" docs/user-docs/

# List all how-to guides
ls docs/user-docs/how-to/

# Check SAP-specific guides
ls docs/skilled-awareness/
cd docs/skilled-awareness/{sap-name}/
cat adoption-blueprint.md
```

---

### Issue: Guide doesn't match my use case

**Solution**:
1. Check [explanation/](explanation/) for conceptual understanding
2. Adapt how-to guide to your specific context
3. Check [reference/](reference/) for technical specifications
4. Search for similar examples in static-template/

---

### Issue: Need SAP-specific help

**Solution**:
```bash
# Navigate to SAP directory
cd docs/skilled-awareness/{sap-name}/

# Read SAP awareness guide
cat AGENTS.md  # or awareness-guide.md

# Read adoption blueprint
cat adoption-blueprint.md

# Check troubleshooting section in blueprint
```

---

## Key Commands

```bash
# Getting started
cat docs/user-docs/explanation/benefits-of-chora-base.md
cat README.md
cat docs/ARCHITECTURE.md

# Task-oriented
ls docs/user-docs/how-to/
cat docs/user-docs/how-to/{task}.md

# Learning
ls docs/user-docs/tutorials/

# Reference
ls docs/user-docs/reference/

# Troubleshooting
ls docs/user-docs/troubleshooting/
grep -r "{error}" docs/user-docs/
```

---

## Support & Resources

**End-User Documentation**:
- [how-to/](how-to/) - Task-oriented guides (11 guides)
- [explanation/](explanation/) - Conceptual understanding (5 docs)
- [reference/](reference/) - Technical specifications (8 docs)
- [guides/](guides/) - Getting started guides (10 guides)
- [tutorials/](tutorials/) - Learning lessons (future)
- [troubleshooting/](troubleshooting/) - Problem resolution

**Root Documentation**:
- [../../README.md](../../README.md) - Project overview
- [../../ARCHITECTURE.md](../../ARCHITECTURE.md) - 4-domain model
- [../../ROADMAP.md](../../ROADMAP.md) - Product roadmap

**SAP-Specific**:
- [../skilled-awareness/](../skilled-awareness/) - All 45 SAP capabilities
- Each SAP has adoption-blueprint.md for installation

**Related Domains**:
- [../dev-docs/](../dev-docs/) - Development processes
- [../project-docs/](../project-docs/) - Project management
- [../skilled-awareness/](../skilled-awareness/) - SAP capabilities

**Claude-Specific**:
- [CLAUDE.md](CLAUDE.md) - Claude patterns for user documentation
- [/CLAUDE.md](../../CLAUDE.md) - Root navigation

---

## Version History

- **1.0.0** (2025-11-04): Initial domain AGENTS.md for user-docs
  - End-user navigation patterns
  - Diataxis framework application (tutorials, how-to, reference, explanation)
  - Integration with other domains
  - Troubleshooting guide
  - Key files and navigation map

---

**Next Steps**:
1. Read [explanation/benefits-of-chora-base.md](explanation/benefits-of-chora-base.md) to understand value
2. Browse [how-to/](how-to/) for task-oriented guides
3. Check [explanation/](explanation/) for conceptual clarity
4. Read [CLAUDE.md](CLAUDE.md) for Claude-specific user doc patterns
5. For SAP adoption, navigate to [../skilled-awareness/](../skilled-awareness/)
