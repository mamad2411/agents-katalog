# User Documentation - Claude-Specific Awareness

**Domain**: User Documentation (user-docs)
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-04

---

## Quick Start for Claude

This file provides **Claude-specific patterns** for helping users adopt and use chora-base.

### First-Time User Assistance

1. Read [AGENTS.md](AGENTS.md) for generic user patterns
2. Use this file for Claude Code integration shortcuts
3. Guide users through Diataxis-structured documentation

### Session Resumption

- Check [explanation/](explanation/) for conceptual clarity
- Use [how-to/](how-to/) for task-oriented guidance
- Reference [reference/](reference/) for technical specs

---

## Progressive Context Loading for User Assistance

### Phase 1: Onboarding (0-10k tokens)

**Goal**: Help user understand chora-base value

**Read**:
1. [explanation/benefits-of-chora-base.md](explanation/benefits-of-chora-base.md)
2. [../../README.md](../../README.md)

**Example**:
```markdown
User: "What is chora-base?"

Claude (Phase 1):
1. Read docs/user-docs/explanation/benefits-of-chora-base.md
2. Summarize value proposition
3. Guide to README.md for installation

Result: User understands "why" and "how to get started"
```

---

### Phase 2: Task Execution (10-50k tokens)

**Goal**: Help user accomplish specific task

**Read**:
1. Relevant how-to guide
2. Related reference documentation if needed

**Example**:
```markdown
User: "How do I set up MCP ecosystem?"

Claude (Phase 2):
1. Read docs/user-docs/how-to/setup-mcp-ecosystem.md
2. Guide user through step-by-step instructions
3. Check reference/ for configuration details if needed

Result: User completes MCP setup successfully
```

---

### Phase 3: Deep Understanding (50-200k tokens)

**Goal**: Help user understand concepts deeply

**Read**:
1. Explanation documents
2. Architecture documentation
3. Multiple related docs for comprehensive view

**Example**:
```markdown
User: "Why does chora-base use 4-domain structure?"

Claude (Phase 3):
1. Read docs/user-docs/explanation/architecture-clarification.md
2. Read docs/ARCHITECTURE.md
3. Read docs/user-docs/explanation/benefits-of-chora-base.md
4. Synthesize comprehensive answer

Result: User understands architectural rationale
```

---

## Claude Code Tool Usage for User Assistance

### Using Read Tool

**Pattern**: Navigate Diataxis structure for user

```bash
# Onboarding
Read docs/user-docs/explanation/benefits-of-chora-base.md
Read README.md

# Task-oriented
Read docs/user-docs/how-to/{task}.md

# Learning (when available)
Read docs/user-docs/tutorials/{tutorial}.md

# Reference lookup
Read docs/user-docs/reference/{spec}.md

# Conceptual understanding
Read docs/user-docs/explanation/{concept}.md
```

**Why**: Diataxis provides clear structure for finding right content

---

### Using Bash Tool

**Pattern**: Help user execute commands from how-to guides

```bash
# From how-to guides, execute commands on user's behalf
npm install -g @beads/bd
bd init
bd version

# Validate setup
pytest tests/
docker ps

# Check environment
which python
python --version
```

**Why**: Users may not know exact commands, Claude executes from guides

---

### Using Write/Edit Tool

**Pattern**: Help user create configuration files

```bash
# From reference docs, create config files
Write config.yaml
# Content from reference/configuration-spec.md

# Edit user's project files
Edit README.md
# Add chora-base capabilities section
```

**Why**: Users may need help with file creation from specs

---

## Claude-Specific User Assistance Tips

### Tip 1: Start with Explanation, Not How-To

**Pattern**:
```markdown
User: "I want to use chora-base"

Claude:
1. Read explanation/benefits-of-chora-base.md
2. Explain "why" first
3. Then guide to how-to/ for "how"
```

**Why**: Users need motivation before instructions

---

### Tip 2: Use Diataxis Categories Explicitly

**Pattern**:
```markdown
User: "I need help with chora-base"

Claude:
"I can help you with:
- **Learning** (tutorials): Structured lessons for newcomers
- **Tasks** (how-to): Step-by-step guides for specific problems
- **Reference**: Technical specifications and configs
- **Understanding** (explanation): Conceptual clarity

What are you trying to do?"
```

**Why**: Users may not know how to ask, categories help clarify

---

### Tip 3: Check if User Needs SAP-Specific Help

**Pattern**:
```markdown
User: "How do I add task tracking?"

Claude (thinking):
- "task tracking" → Likely SAP-015
- user-docs has general guides
- skilled-awareness has SAP-specific guides

Claude:
1. Check if SAP-015 adopted
2. If yes: Read docs/skilled-awareness/task-tracking/AGENTS.md
3. If no: Read docs/skilled-awareness/task-tracking/adoption-blueprint.md
```

**Why**: SAP-specific help is in skilled-awareness/, not user-docs/

---

### Tip 4: Guide Users to Appropriate Domain

**Pattern**:
```markdown
User: "How do I contribute to chora-base?"

Claude (thinking):
- "contribute" → dev-docs domain, not user-docs

Claude:
"Contributing to chora-base is covered in developer documentation:
See docs/dev-docs/AGENTS.md for contribution workflows."
```

**Why**: user-docs is for using chora-base, not building it

---

### Tip 5: Combine Explanation + How-To for Complex Tasks

**Pattern**:
```markdown
User: "How do I bootstrap a project?"

Claude:
1. Read explanation/benefits-of-chora-base.md (why bootstrap)
2. Read how-to/bootstrap-project.md (how to bootstrap)
3. Read reference/configuration-spec.md (config details)
4. Guide user through complete workflow

Result: User understands "why" and completes "how"
```

**Why**: Complex tasks benefit from conceptual understanding + instructions

---

## Common Pitfalls for Claude Assisting Users

### Pitfall 1: Jumping to How-To Without Explanation

**Problem**: User asks "how do I X?" and Claude immediately provides steps without context

**Fix**:
```markdown
Claude:
"Let me first explain why chora-base uses X approach...
(read explanation/)

Now, here's how to do X step-by-step:
(read how-to/)"
```

---

### Pitfall 2: Confusing User Docs with Dev Docs

**Problem**: User wants to use chora-base, Claude provides contribution guide

**Fix**:
```markdown
# User wants to USE chora-base
→ docs/user-docs/

# User wants to BUILD chora-base
→ docs/dev-docs/
```

---

### Pitfall 3: Not Checking SAP Adoption Status

**Problem**: User asks about SAP feature, Claude assumes not adopted

**Fix**:
```bash
# Check if SAP adopted
ls .beads/  # SAP-015
ls inbox/  # SAP-001
ls .chora/memory/  # SAP-010
```

---

### Pitfall 4: Overwhelming User with All Diataxis Types

**Problem**: Reading tutorials + how-to + reference + explanation for simple question

**Fix**: Use progressive loading
- Simple question: explanation only
- Task question: how-to + reference
- Learning: tutorials (when available)

---

### Pitfall 5: Not Adapting to User's Skill Level

**Problem**: Providing advanced reference docs to beginner

**Fix**:
- Beginner: tutorials + explanation
- Intermediate: how-to + reference
- Advanced: reference + explanation

---

## Example Claude Code Session (User Assistance)

```markdown
User: "I want to use chora-base for my new project"

Claude (thinking):
- User wants to USE chora-base (user-docs domain)
- Likely needs onboarding (Phase 1)
- Then project bootstrap (Phase 2)

Claude (Phase 1: Onboarding - 0-10k tokens):
1. Read docs/user-docs/explanation/benefits-of-chora-base.md
2. Read README.md
3. Explain value proposition to user

Claude (response):
"Chora-base provides a comprehensive template for AI-assisted development with 30+ capabilities (SAPs). It includes:

- Project bootstrap templates
- Testing and CI/CD automation
- Agent awareness patterns
- Task tracking and coordination

Would you like to bootstrap a new project with chora-base?"

User: "Yes, let's bootstrap a project"

Claude (Phase 2: Task Execution - 10-50k tokens):
4. Read docs/skilled-awareness/project-bootstrap/adoption-blueprint.md
5. Guide user through steps:
   - Clone chora-base
   - Use static-template
   - Configure project
   - Initialize SAPs

Claude (executes via Bash):
git clone https://github.com/liminalcommons/chora-base.git
cp -r chora-base/static-template/ new-project/
cd new-project/
# Configure project...

Claude (response):
"I've bootstrapped your new project with chora-base template:

- ✅ Project structure created
- ✅ Testing framework configured
- ✅ CI/CD workflows added
- ✅ Documentation structure ready

Next steps:
1. Review PROJECT_CONFIG.yaml
2. Run: pytest tests/
3. Commit initial structure

Would you like help with any of these?"

Result: User has working project, understands next steps
Time: 20-30 minutes (onboarding + bootstrap)
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
- [../skilled-awareness/](../skilled-awareness/) - All 30+ SAP capabilities
- Each SAP has adoption-blueprint.md for installation

**Related Domains**:
- [../dev-docs/](../dev-docs/) - Development processes
- [../project-docs/](../project-docs/) - Project management
- [../skilled-awareness/](../skilled-awareness/) - SAP capabilities

**Navigation**:
- [AGENTS.md](AGENTS.md) - Generic user patterns
- [/CLAUDE.md](../../CLAUDE.md) - Root navigation

---

## Version History

- **1.0.0** (2025-11-04): Initial domain CLAUDE.md for user-docs
  - Progressive context loading for user assistance
  - Diataxis navigation patterns
  - Tool usage for user help (Read, Bash, Write/Edit)
  - Common pitfalls and tips
  - Example user assistance session

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic user patterns
2. Use Diataxis structure (tutorials, how-to, reference, explanation)
3. Start with explanation/ for conceptual clarity
4. Use how-to/ for task-oriented guidance
5. Check skilled-awareness/ for SAP-specific help
