---
name: bmad-skill
description: This skill should be used when working with BMAD (BMad-CORE) v6-alpha projects. BMAD is a universal human-AI collaboration platform with specialized modules for software development (BMM), agent building (BMB), creative intelligence (CIS), and project management (BMD). Use this skill to understand agent workflows, command patterns, scale-adaptive methodology, and effective utilization of the four-phase development system.
---

# BMAD v6-Alpha Skill

## What is BMAD-CORE?

BMAD-CORE (Collaboration Optimized Reflection Engine) is a revolutionary framework that amplifies human potential through specialized AI agents. Unlike traditional AI tools that replace human thinking, BMAD-CORE guides through reflective workflows that bring out the best ideas in both human and AI.

**Core Philosophy:**
- **Collaboration**: Human-AI partnership where both contribute unique strengths
- **Optimized**: Refined processes for maximum effectiveness
- **Reflection**: Guided thinking that unlocks better solutions
- **Engine**: Powerful framework orchestrating specialized agents and workflows

## BMAD v6-Alpha Architecture

### Module System

BMAD organizes capabilities into four main modules:

#### 1. **Core Module** (Always Installed)
Foundation powering all modules:
- **BMad Master Agent** - Universal orchestrator and task executor
- **Party Mode** - Multi-agent collaborative sessions
- **Brainstorming Workflow** - Core ideation capabilities
- **Configuration System** - User preferences and settings

**Location**: `bmad/core/`

#### 2. **BMM Module** - BMad Method (Software Development)
Revolutionary agile software development with **Scale Adaptive Workflow Engine™**:
- **10 Specialized Agents**: Analyst, PM, Architect, SM, Dev, Game Designer, Game Architect, Game Dev, UX Designer, TEA (Test Architect)
- **Four-Phase Methodology**: Analysis → Planning → Solutioning → Implementation
- **Scale Levels 0-4**: From single changes to enterprise projects
- **Just-In-Time Design**: Create specs one epic at a time
- **Story State Machine**: Automated story progression (BACKLOG → TODO → IN PROGRESS → DONE)

**Location**: `bmad/bmm/` (if installed)

#### 3. **BMB Module** - BMad Builder (Custom Development)
Tools for creating custom agents, workflows, and modules:
- **Builder Agent** - Guides creation of custom components
- **7 Builder Workflows**: create-agent, create-workflow, create-module, audit-workflow, edit-workflow, module-brief, redoc
- **Three Agent Types**: Full module agents, hybrid agents, standalone agents

**Location**: `bmad/bmb/` (if installed)

#### 4. **CIS Module** - Creative Intelligence Suite
Innovation and creative problem-solving:
- **5 Specialized Agents**: Brainstorming Coach (Carson), Design Thinking Coach (Maya), Problem Solver (Dr. Quinn), Innovation Strategist (Victor), Storyteller (Sophia)
- **150+ Creative Techniques**: Across brainstorming, design thinking, problem-solving, innovation strategy, storytelling
- **Energy-Aware Sessions**: Adapts to user engagement

**Location**: `bmad/cis/` (shared resources appear even if not explicitly selected)

#### 5. **BMD Module** - BMad Development (Project Management)
Internal tools for BMAD development itself:
- **CLI Chief** - Command-line management
- **Doc Keeper** - Documentation management
- **Release Chief** - Release management

**Location**: `bmd/` (development only)

### Installation Structure

All modules install to a single unified `bmad/` folder:

```
your-project/
└── bmad/
    ├── core/           # Core framework (always present)
    ├── bmm/            # BMad Method (if selected)
    ├── bmb/            # BMad Builder (if selected)
    ├── cis/            # Creative Intelligence (shared resources)
    ├── _cfg/           # Your customizations
    │   ├── agents/     # Agent sidecar files
    │   └── manifest.yaml
    └── [module]/config.yaml  # Per-module configuration
```

## Working with BMAD Agents

### Agent Activation Methods

**Method 1: Claude Code Slash Commands** (Recommended)

When BMAD is installed locally in `.claude/commands/bmad/`, use these slash commands:

```bash
# Core Module
/bmad:bmad:core:agents:bmad-master
/bmad:bmad:core:workflows:brainstorming
/bmad:bmad:core:workflows:party-mode

# BMM Module Agents
/bmad:bmad:bmm:agents:analyst      # Business Analyst - Phase 1
/bmad:bmad:bmm:agents:pm           # Product Manager - Phase 2
/bmad:bmad:bmm:agents:architect    # Architect - Phase 3
/bmad:bmad:bmm:agents:sm           # Scrum Master - Phase 4
/bmad:bmad:bmm:agents:dev          # Developer - Phase 4
/bmad:bmad:bmm:agents:game-designer    # Game projects
/bmad:bmad:bmm:agents:game-architect   # Game architecture
/bmad:bmad:bmm:agents:game-dev         # Game development
/bmad:bmad:bmm:agents:ux-designer      # UX design
/bmad:bmad:bmm:agents:tea              # Test Architect

# BMB Module
/bmad:bmad:bmb:agents:bmad-builder     # Builder agent

# BMB Workflows (Direct Access)
/bmad:bmad:bmb:workflows:create-agent
/bmad:bmad:bmb:workflows:create-workflow
/bmad:bmad:bmb:workflows:create-module
/bmad:bmad:bmb:workflows:audit-workflow
/bmad:bmad:bmb:workflows:edit-workflow
/bmad:bmad:bmb:workflows:module-brief
/bmad:bmad:bmb:workflows:redoc
/bmad:bmad:bmb:workflows:convert-legacy

# BMD Module (Development/Management)
/bmad:bmad:bmd:agents:cli-chief
/bmad:bmad:bmd:agents:doc-keeper
/bmad:bmad:bmd:agents:release-chief
```

**Local Installation Location**: `/Users/mikhail/.claude/commands/bmad/`

**Method 2: Direct File Loading**
- Drag and drop agent file from `.claude/commands/bmad/`
- Use `@` mention with agent file path
- Navigate to agent file in your IDE's file browser

**Method 3: BMad Master Orchestrator**
Load BMad Master first, then use menu to access specific agents or workflows.

### Agent Structure

All BMAD agents follow a consistent YAML structure:

```yaml
agent:
  metadata:
    id: bmad/[module]/agents/[name].md
    name: AgentName
    title: Agent Title
    icon: 🎯
    module: [bmm|bmb|cis|core]

  persona:
    role: Primary Role + Secondary Expertise
    identity: Background and experience description
    communication_style: How the agent communicates
    principles:
      - Guiding principle 1
      - Guiding principle 2

  menu:
    - trigger: command-name
      workflow: "{project-root}/bmad/[module]/workflows/[workflow]/workflow.yaml"
      description: What this command does
```

### Common Agent Commands

**Every agent has these built-in commands:**
- `*help` - Show agent's menu
- `*exit` - Exit agent with confirmation

**Module-specific commands use asterisk prefix:**
- Analyst: `*workflow-status`, `*brainstorm-project`, `*research`, `*product-brief`
- PM: `*workflow-status`, `*prd`, `*tech-spec`, `*gdd` (games)
- Architect: `*architecture`, `*tech-spec`
- SM: `*create-story`, `*story-ready`, `*story-context`, `*story-done`, `*retrospective`
- Dev: `*dev-story`, `*review-story`, `*story-done`

## BMM: The Four-Phase Software Development Methodology

### Universal Entry Point: workflow-status

**ALWAYS START HERE!** Before beginning any workflow:

```bash
# Load Analyst or PM agent, then:
*workflow-status
```

**What it does:**
- ✅ Checks for existing workflow status file
- ✅ Displays current phase, progress, and next action
- ✅ Guides new projects to appropriate workflows
- ✅ Routes brownfield projects to documentation first
- ✅ Provides clear recommendations for next steps

### Phase 1: Analysis (Optional)

**Purpose**: Project discovery and requirements gathering

**Agents**: Analyst, Game Designer

**Workflows**:
- `brainstorm-project` - Software solution exploration
- `brainstorm-game` - Game concept ideation (5 methodologies)
- `research` - Multi-mode research (market/technical/deep)
- `product-brief` - Strategic product planning
- `game-brief` - Structured game design foundation

**When to use**: New projects needing concept development

### Phase 2: Planning (Required)

**Purpose**: Scale-adaptive planning with appropriate documentation

**Agents**: PM, Game Designer

**Scale Levels**:

| Level | Scope | Stories | Outputs | Next Phase |
|-------|-------|---------|---------|------------|
| **0** | Single atomic change | 1 | tech-spec.md + story | Implementation |
| **1** | Simple feature | 2-10 | tech-spec.md + epic + stories | Implementation |
| **2** | Focused project | 5-15 (1-2 epics) | PRD.md + epics.md | Tech-spec → Implementation |
| **3** | Complex project | 12-40 (2-5 epics) | PRD.md + epics.md | Solutioning → Implementation |
| **4** | Enterprise scale | 40+ (5+ epics) | PRD.md + epics.md | Solutioning → Implementation |

**Software Projects**:
- Level 0-1: `*tech-spec` (Architect) → Implementation
- Level 2: `*prd` (PM) → `*tech-spec` → Implementation
- Level 3-4: `*prd` (PM) → Solutioning → Implementation

**Game Projects**:
- All Levels: `*gdd` (Game Designer) → Optional narrative → Solutioning or Implementation

**Key Outputs**:
- `bmm-workflow-status.md` - Versioned workflow state with story backlog
- `PRD.md` - Product Requirements (L2-4)
- `epics.md` - Epic breakdown (L2-4)
- `tech-spec.md` - Technical specification (L0-2)
- `story-*.md` - User story files

### Phase 3: Solutioning (Levels 3-4 Only)

**Purpose**: Architecture and technical design for complex projects

**Agents**: Architect, Game Architect

**Workflows**:
- `architecture` - Create overall architecture.md with ADRs
- `tech-spec` - Create epic-specific tech specs (JIT - Just-In-Time)

**Just-In-Time Approach**:
```
FOR each epic in sequence:
    WHEN ready to implement epic:
        Architect: Run *tech-spec for THIS epic only
        → Creates tech-spec-epic-N.md
    IMPLEMENT epic completely
    THEN move to next epic
```

**Critical**: Tech specs created ONE AT A TIME, not all upfront. This prevents over-engineering and incorporates learning.

### Phase 4: Implementation (Iterative)

**Purpose**: Transform requirements into working software

**Agents**: SM (Scrum Master), Dev (Developer)

**The Story State Machine**:

```
BACKLOG → TODO → IN PROGRESS → DONE
```

**State Definitions**:
- **BACKLOG**: Ordered list of stories awaiting drafting (populated at phase transition)
- **TODO**: Single story needing drafting or awaiting approval
- **IN PROGRESS**: Single story approved for development
- **DONE**: Completed stories with dates and points

**Implementation Loop**:

```
1. SM: *create-story (drafts story from TODO)
   → Story file created with Status="Draft"

2. USER REVIEWS STORY

3. SM: *story-ready (approves story)
   → TODO → IN PROGRESS
   → BACKLOG → TODO (next story)
   → Story Status = "Ready"

4. SM: *story-context (optional but recommended)
   → Generates expertise injection XML

5. DEV: *dev-story (implements story)
   → Reads IN PROGRESS section
   → Implements with context guidance

6. USER REVIEWS IMPLEMENTATION

7. DEV: *story-done (marks complete)
   → IN PROGRESS → DONE
   → TODO → IN PROGRESS (if exists)
   → BACKLOG → TODO (if exists)
   → Story Status = "Done"

8. REPEAT until all stories complete

9. SM: *retrospective (after epic complete)
   → Captures learnings for next epic
```

**Key Workflows**:
- `create-story` - SM drafts story from TODO
- `story-ready` - SM approves story for dev (after user review)
- `story-context` - SM generates contextual expertise
- `dev-story` - DEV implements story
- `story-done` - DEV marks story complete (after user confirms DoD)
- `review-story` - Quality validation (optional)
- `correct-course` - Handle issues/changes
- `retrospective` - Capture epic learnings

**Critical Rule**: Agents NEVER search for "next story" - they ALWAYS read from status file.

## Working with Workflows

### Workflow Execution

Workflows are executed through agent menus:

1. Load agent (Analyst, PM, Architect, SM, Dev, etc.)
2. Agent shows menu with available commands
3. Enter command (e.g., `*prd`, `*create-story`)
4. Agent loads and executes workflow.yaml
5. Workflow guides through structured steps

### Workflow Structure

All workflows are YAML-based with consistent structure:

```yaml
workflow:
  metadata:
    id: workflow-unique-id
    name: Workflow Name
    version: 1.0.0

  config:
    output_folder: "{output_folder}"

  steps:
    - name: Step Name
      prompt: |
        Detailed instructions for this step
```

### Key Workflow Patterns

**Validation Workflows**: Use `validate-workflow` handler
```yaml
- trigger: validate-tech-spec
  validate-workflow: "{project-root}/bmad/bmm/workflows/2-plan-workflows/tech-spec/workflow.yaml"
  checklist: "{project-root}/bmad/bmm/workflows/2-plan-workflows/tech-spec/checklist.md"
  document: "{output_folder}/tech-spec.md"
```

**Data-Driven Workflows**: Use `data` parameter
```yaml
- trigger: command-name
  workflow: "{project-root}/bmad/[module]/workflows/[name]/workflow.yaml"
  data: "{output_folder}/context.md"
```

## BMB: Building Custom Components

### Creating Custom Agents

Load BMad Builder agent, then use:
- `*create-agent` - Design and implement custom agents
- `*create-workflow` - Build new workflow definitions
- `*create-module` - Design custom modules

### Agent Types

**1. Full Module Agents**: Complete agents embedded in modules
- Location: `src/modules/[module]/agents/`
- Example: PM, Analyst, Architect

**2. Hybrid Agents**: Shared across modules
- Location: Shared agent directories
- Example: Brainstorming agents used by multiple modules

**3. Standalone Agents**: Tiny, specialized agents
- Location: Independent of modules
- Example: Single-purpose utility agents

### Builder Workflows

- `audit-workflow` - Review and validate workflows
- `edit-workflow` - Modify existing workflows
- `module-brief` - Document module specifications
- `redoc` - Regenerate documentation
- `convert-legacy` - Migrate legacy formats

## CIS: Creative Intelligence

### CIS Agents and Workflows

**5 Specialized Agents** with unique personas:
- **Carson** - Brainstorming Coach (energetic facilitator)
- **Maya** - Design Thinking Maestro (jazz-like improviser)
- **Dr. Quinn** - Problem Solver (detective-scientist)
- **Victor** - Innovation Strategist (strategic precision)
- **Sophia** - Storyteller (whimsical narrator)

**5 Interactive Workflows**:
- `brainstorming` - 36 creative techniques across 7 categories
- `design-thinking` - 5-phase human-centered design
- `problem-solving` - Root cause analysis and solution generation
- `innovation-strategy` - Business model innovation
- `storytelling` - 25 story frameworks

### Using CIS

CIS workflows can be:
1. Invoked directly via CIS agents
2. Embedded in other modules (BMM uses brainstorming)
3. Used standalone for creative sessions

## Best Practices

### DO's

✅ **Always start with `*workflow-status`** - Universal entry point
✅ **Respect the scale levels** - Don't over-document small projects
✅ **Use Just-In-Time design** - Create tech specs one epic at a time
✅ **Follow the story state machine** - Never skip state transitions
✅ **Run retrospectives** - After each epic for continuous learning
✅ **Generate story-context** - Provides targeted expertise
✅ **Validate before advancing** - User reviews stories and implementations
✅ **Document brownfield first** - Never plan without understanding existing code

### DON'Ts

❌ **Don't skip workflow-status check** - It guides your entire journey
❌ **Don't create all tech specs upfront** - Use JIT approach
❌ **Don't batch story creation** - One at a time through state machine
❌ **Don't manually track stories** - Let state machine manage progression
❌ **Don't plan brownfield without docs** - Run analysis first
❌ **Don't over-document Level 0-1** - Simple projects need minimal docs
❌ **Don't skip Phase 3 for Level 3-4** - Architecture is critical

## Configuration and Customization

### Module Configuration

Each module has `config.yaml` with:
```yaml
project_name: "Your Project"
output_folder: "./docs/bmad"
user_name: "Your Name"
communication_language: "English"
technical_level: "intermediate"  # BMM specific
```

**Location**: `bmad/[module]/config.yaml`

### Agent Customization (Sidecar Files)

Customize any agent via sidecar files in `bmad/_cfg/agents/`:

```yaml
# bmad/_cfg/agents/core-bmad-master.customize.yaml
customizations:
  persona:
    name: "CustomName"
    communication_style: "Your preferred style"

  menu:
    - trigger: custom-command
      workflow: "{project-root}/path/to/custom/workflow.yaml"
      description: "Custom functionality"
```

**Update-Safe**: Customizations persist through BMAD updates

### Multi-Language Support

Agents communicate in configured language:
- Set in module `config.yaml`: `communication_language: "Spanish"`
- Agents automatically adapt communication
- Documentation output can use different language

## Troubleshooting Common Issues

### "Workflow status file not found"
→ Run `*workflow-status` first to initialize

### "Story not in expected state"
→ Check `bmm-workflow-status.md` - verify story is in correct section

### "Can't find next story"
→ Agents don't search - they read from status file sections

### "Brownfield planning fails"
→ Run documentation workflow first (coming soon: brownfield-analysis)

### "Over-documented small project"
→ Check scale level - Level 0-1 should skip PRD and architecture

### "Tech specs created all at once"
→ Use JIT approach - one epic at a time during implementation

## Quick Reference

### Essential Commands by Agent

**Analyst**:
- `*workflow-status` - Check status
- `*brainstorm-project` - Ideation
- `*research` - Market/technical research
- `*product-brief` - Product strategy

**PM**:
- `*workflow-status` - Check status
- `*prd` - Create PRD (L2-4)
- `*tech-spec` - Create tech spec (L0-2)
- `*gdd` - Game design document

**Architect**:
- `*architecture` - Overall architecture (L3-4)
- `*tech-spec` - Epic-specific specs (JIT)

**SM**:
- `*create-story` - Draft story
- `*story-ready` - Approve story
- `*story-context` - Generate expertise
- `*retrospective` - Capture learnings

**Dev**:
- `*dev-story` - Implement story
- `*review-story` - Quality check
- `*story-done` - Mark complete

**BMad Builder**:
- `*create-agent` - Build custom agent
- `*create-workflow` - Build workflow
- `*create-module` - Build module

### File Locations

**Config**: `bmad/[module]/config.yaml`
**Agents**: `bmad/[module]/agents/`
**Workflows**: `bmad/[module]/workflows/`
**Tasks**: `bmad/core/tasks/`
**Customizations**: `bmad/_cfg/agents/`
**Status Tracking**: `{output_folder}/bmm-workflow-status.md`

### Support Resources

- 💬 [Discord Community](https://discord.gg/gk8jAdXWmj)
- 🐛 [Issue Tracker](https://github.com/bmad-code-org/BMAD-METHOD/issues)
- 🎥 [YouTube Tutorials](https://www.youtube.com/@BMadCode)
- 📚 [Full Documentation](https://github.com/bmad-code-org/BMAD-METHOD)

---

**Framework**: BMAD-CORE v6-alpha | **Version**: Alpha | **Branch**: v6-alpha
