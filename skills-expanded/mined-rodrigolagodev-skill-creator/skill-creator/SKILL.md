---
name: skill-creator
description: Expert guidance for creating, structuring, and refining Agent Skills following the open standard. Use when working with skill files, authoring new skills, improving existing skills, or understanding skill architecture and best practices. Use PROACTIVELY when user mentions creating skills, structuring documentation, or building reusable agent capabilities.
license: MIT
compatibility: agent-skills-standard
metadata:
  category: skill-development
  version: "1.2.0"
  author: "Rodrigo Lago"
  standard: "https://agentskills.io"
---

# Creating Agent Skills

Expert system for creating high-quality Agent Skills following the open standard, with comprehensive templates, validation checklists, and best practices.

## What Are Agent Skills?

**Agent Skills** are folders of instructions, scripts, and resources that AI agents can discover and use dynamically to improve their capabilities. Think of them as **plugins for AI agents**.

### Key Benefits

- **Reusable**: Write once, use across multiple agent platforms
- **Discoverable**: Agents can find and activate skills on demand
- **Portable**: Compatible with Claude, OpenCode, Cursor, VS Code, and 20+ platforms
- **Version-controlled**: Skills are just folders → perfect for Git

### The Agent Skills Standard

This skill follows the **[Agent Skills open standard](https://agentskills.io)**, originally developed by Anthropic and adopted by the community.

**Supported platforms:**

- Claude, Claude Code
- OpenCode, Crush
- Cursor, VS Code
- GitHub Copilot
- Gemini CLI, Roo Code, Goose
- And 15+ more...

## Core Principles

### 1. Skills Are Structured Documentation

Skills are **pure markdown documentation** that agents load as context. No executable code required.

```
skill-name/
├── SKILL.md          # Entry point (YAML + Markdown)
├── references/       # Detailed documentation
├── templates/        # Reusable templates
└── workflows/        # Step-by-step guides
```

### 2. YAML Frontmatter + Markdown Body

```yaml
---
name: skill-identifier
description: What it does, when to use, examples
---
# Skill Name

Your instructions here...
```

### 3. Progressive Disclosure

- **SKILL.md**: < 650 lines (quick reference + essential patterns)
- **references/**: Deep dives when needed
- **templates/**: Copy-paste starting points
- **workflows/**: Guided processes

### 4. English-First for LLM Efficiency

Write skills in **English** for optimal LLM performance:

- Faster inference
- Lower token costs
- Better comprehension
- Consistent behavior

### 5. Verification Loop (Post-Creation Validation)

**CRITICAL:** Every skill MUST be verified after creation.

Include verification as the final step in any skill creation workflow:

```markdown
## Verification Loop

After creating any skill:

1. **Syntax Check** - Validate YAML frontmatter parses correctly
2. **Structure Check** - Verify all required files exist
3. **Link Check** - Confirm all internal references work
4. **Size Check** - SKILL.md < 650 lines

IF any check fails:
→ Fix the issue
→ Re-run verification
→ Do NOT report completion until all pass
```

**Why?** Professional systems (Claude Code, Codex, Gemini CLI) all require verification loops. Benefits:

- Catches errors before user discovers them
- Builds trust through reliability
- Reduces back-and-forth corrections
- Ensures consistent quality

## Quick Start

**What would you like to do?**

### Creating a New Skill

Choose your preferred mode:

| Mode               | Workflow                                                     | Best For                                              |
| ------------------ | ------------------------------------------------------------ | ----------------------------------------------------- |
| **🧙 Interactive** | [interactive-creation.md](workflows/interactive-creation.md) | First-time creators, complex skills, when unsure      |
| **⚡ Automatic**   | [create-new-skill.md](workflows/create-new-skill.md)         | Experienced users, quick creation, clear requirements |

**Interactive Mode** (Recommended for new users):

```
User: "Quiero crear un skill"
Agent: "¡Vamos paso a paso! ¿Qué problema quieres resolver?"
User: "Analizar código Python"
Agent: "Perfecto. ¿Cómo se llamará? Sugiero: python-analyzer..."
... (continues with guided questions)
```

**Automatic Mode** (For experienced users):

```
User: "Create a skill for analyzing Python code for errors"
Agent: [Creates skill immediately based on description]
```

### Other Actions

- **Validate existing skill** → Use checklist: [validation-checklist.md](references/validation-checklist.md)
- **Understand structure** → Read: [skill-anatomy.md](references/skill-anatomy.md)
- **Copy template** → Start with: [templates/minimal-skill.md](templates/minimal-skill.md)

> **Tip:** When user says "crear skill" or "create a skill" without details,
> prefer **Interactive Mode** to gather requirements step by step.

**Example - Interactive Flow:**

```
User: "Quiero crear un skill"
    ↓
1. Agent loads skill-creator
2. Agent follows workflows/interactive-creation.md
3. Agent asks: "¿Qué problema resuelve?"
4. User responds, agent confirms
5. Agent asks: "¿Cómo se llamará?"
... (8 phases of guided creation)
4. Agent uses Write tool to create ~/.config/opencode/skills/api-analyzer/SKILL.md
5. Done! Skill is ready to use
```

## Skill Structure

### Required Files

| File        | Required       | Purpose                                     |
| ----------- | -------------- | ------------------------------------------- |
| `SKILL.md`  | ✅ Yes         | Entry point with frontmatter + instructions |
| `README.md` | ⚠️ Recommended | GitHub documentation                        |
| `LICENSE`   | ⚠️ Recommended | Open source license (MIT suggested)         |

### Optional Directories

| Directory     | Purpose                  | When to Use                           |
| ------------- | ------------------------ | ------------------------------------- |
| `references/` | Detailed documentation   | Complex skills with multiple concepts |
| `templates/`  | Reusable starting points | Skills that generate content/code     |
| `workflows/`  | Step-by-step guides      | Multi-step processes                  |
| `examples/`   | Complete examples        | Show real usage patterns              |

### Minimal Skill Example

See [templates/minimal-skill.md](templates/minimal-skill.md) for a complete starting template.

**Quick structure:**

```yaml
---
name: your-skill-name
description: >-
  What it does. When to use it.
  <example>User: "..." Assistant: "..."</example>
---
# Your Skill

Instructions here...
```

## Frontmatter Specification

See [references/frontmatter-spec.md](references/frontmatter-spec.md) for complete details.

### Required Fields

| Field         | Format     | Description                                    |
| ------------- | ---------- | ---------------------------------------------- |
| `name`        | kebab-case | Unique identifier, < 64 chars                  |
| `description` | multi-line | What + When + `<example>` blocks, < 1024 chars |

### Optional Fields

| Field               | Example               | Purpose             |
| ------------------- | --------------------- | ------------------- |
| `license`           | MIT                   | SPDX identifier     |
| `compatibility`     | agent-skills-standard | Platform support    |
| `metadata.category` | development           | Organization        |
| `metadata.version`  | "1.0.0"               | Semantic versioning |
| `metadata.author`   | "Your Name"           | Attribution         |
| `metadata.tags`     | [python, testing]     | Discoverability     |

### Description Best Practices

**Rules:**

- Include **WHAT** it does (1 sentence)
- Include **WHEN** to use (triggers)
- Include at least 1 `<example>` block
- Keep under 1024 characters
- Write in third person

## Naming Conventions

### Skill Names (frontmatter `name`)

Use **kebab-case** with descriptive nouns or verb phrases:

✅ **Good:**

- `code-reviewer`
- `api-documentation`
- `database-migration`
- `security-audit`
- `prompt-engineering`

❌ **Avoid:**

- `helper`, `utils`, `tool` (too vague)
- `my-skill`, `skill1` (not descriptive)
- `CodeReviewer` (wrong case)

### Folder Names

Match your skill's `name` field:

```bash
~/.config/opencode/skills/
├── code-reviewer/           # name: code-reviewer
├── api-documentation/       # name: api-documentation
└── security-audit/          # name: security-audit
```

## File Organization

See [references/skill-anatomy.md](references/skill-anatomy.md) for complete structure breakdown.

### Quick Reference

| Directory     | Purpose                    | Files per Directory  |
| ------------- | -------------------------- | -------------------- |
| `references/` | Deep dive documentation    | One topic per file   |
| `templates/`  | Copy-paste starting points | Use `{{VAR}}` syntax |
| `workflows/`  | Step-by-step processes     | Numbered steps       |
| `examples/`   | Concrete usage examples    | README per example   |

### SKILL.md Sections

```
# Skill Name          → Brief intro
## Core Principles    → High-level concepts
## Quick Start        → How to use
## Main Instructions  → Detailed guidance
## When to Use        → Triggers and cases
## References         → Links to refs/
```

**Rule:** SKILL.md is the entry point. Keep it < 650 lines. Details go in references/.

## Skill Complexity Scale

Choose the right size for your skill:

| Complexity      | SKILL.md Lines | Directories | When to Use                                        |
| --------------- | -------------- | ----------- | -------------------------------------------------- |
| **🟢 Micro**    | 50-150         | None        | Single concept (code style, naming conventions)    |
| **🟡 Simple**   | 150-300        | templates/  | Focused domain (doc writer, linter config)         |
| **🟠 Standard** | 300-500        | refs + tmpl | Full workflow (component creator, API designer)    |
| **🔴 Complex**  | 500-650        | All dirs    | Multi-domain system (agent-creator, skill-creator) |

**Decision Logic:**

```
IF single concept, no templates needed → Micro
ELSE IF one domain with templates → Simple
ELSE IF full workflow with references → Standard
ELSE IF multi-domain with all directories → Complex

DEFAULT: Start with Micro/Simple. Upgrade only when proven necessary.
```

**Why Smaller is Better:**

- Faster to load (less context)
- Cheaper to run (fewer tokens)
- Easier to maintain
- More focused behavior
- Better discoverability

**Upgrade Signals:**

| Signal                      | Action                            |
| --------------------------- | --------------------------------- |
| SKILL.md > 300 lines        | Consider splitting to references/ |
| Repeated patterns           | Create templates/                 |
| Multi-step processes        | Add workflows/                    |
| Multiple unrelated concepts | Split into separate skills        |

## Token Optimization Guide

Optimize skills for performance and cost:

### File Size Guidelines

| File Type | Recommended   | Maximum   | Notes                        |
| --------- | ------------- | --------- | ---------------------------- |
| SKILL.md  | 200-400 lines | 650 lines | Entry point, quick reference |
| Reference | 100-300 lines | 600 lines | Single topic focus           |
| Template  | 50-200 lines  | 400 lines | Copy-paste ready             |
| Workflow  | 100-400 lines | 800 lines | Step-by-step process         |

### Token-Saving Patterns

1. **Progressive Loading** - Core in SKILL.md, details in references/
2. **Links Over Inline** - Reference files instead of embedding content
3. **Tables Over Prose** - Structured data is more token-efficient
4. **Decision Trees** - Clear IF/ELSE logic over long explanations
5. **Examples as Proof** - Show don't tell (1 example > 10 paragraphs)

### Content Density Targets

| Section Type    | Target                | Anti-Pattern                |
| --------------- | --------------------- | --------------------------- |
| Core Principles | 5-7 items max         | 15+ principles nobody reads |
| Quick Start     | 3-5 steps             | Essay-length introduction   |
| Tables          | 5-10 rows             | 50-row reference tables     |
| Examples        | 2-3 concrete examples | Abstract descriptions       |

**Rule:** If a section exceeds its target, split it into references/.

## Validation Checklist

Before publishing a skill, verify:

- [ ] `SKILL.md` exists with valid YAML frontmatter
- [ ] `name` field is kebab-case and descriptive
- [ ] `description` includes what/when/examples
- [ ] Description has at least one `<example>` block
- [ ] **Appropriate complexity level** chosen (🟢🟡🟠🔴)
- [ ] Instructions are clear and actionable
- [ ] Examples demonstrate real usage
- [ ] English language throughout
- [ ] **SKILL.md < 650 lines** (split to references/ if longer)
- [ ] README.md exists (for GitHub)
- [ ] LICENSE file present
- [ ] No executable scripts (pure markdown)
- [ ] **Verification loop completed** (syntax, structure, activation)

See [references/validation-checklist.md](references/validation-checklist.md) for complete rubric.

## Best Practices

### Do's ✅

1. **Write in English** - Optimal for LLM processing
2. **Use clear descriptions** - What + when + examples
3. **Include examples** - Show real usage with `<example>` blocks
4. **Organize content** - Use references/ for deep dives
5. **Provide templates** - Make it easy to get started
6. **Document limitations** - Be explicit about what skill cannot do
7. **Version your skill** - Use semantic versioning (1.0.0)

### Don'ts ❌

| Anti-Pattern                  | Problem                           | Solution                             |
| ----------------------------- | --------------------------------- | ------------------------------------ |
| No examples                   | Users don't know when to use      | Add `<example>` blocks               |
| Vague description             | Agent won't activate skill        | Specific triggers + use cases        |
| Monolithic SKILL.md           | Overwhelming (>650 lines)         | Split into references/               |
| Executable scripts            | Breaks portability                | Pure markdown documentation          |
| Missing README                | Hard to discover on GitHub        | Add README.md                        |
| No versioning                 | Breaking changes unclear          | Use CHANGELOG.md                     |
| **Skipping Verification**     | Errors found by users, not author | Always run verification loop         |
| **Wrong Complexity**          | Complex skill for simple concept  | Start Micro, upgrade when needed     |
| **No Token Optimization**     | Bloated, slow loading             | Tables over prose, links over inline |
| **Missing Limitations**       | Users try unsupported features    | Document what skill cannot do        |
| **Non-English Content**       | LLM inefficiency, higher costs    | Always write in English              |
| **No Progressive Disclosure** | Everything inline, too long       | Core in SKILL.md, details in refs/   |

## Skill Creation Process

### Method: Direct File Creation

When creating a skill, use the `Write` tool:

```markdown
1. Understand purpose (ask questions if needed)
2. Read template: templates/minimal-skill.md
3. Customize for specific use case
4. Use Write tool to create: ~/.config/opencode/skills/<name>/SKILL.md
5. (Optional) Add references/, templates/, workflows/ as needed
```

### Guided Workflow

**Two modes available:**

**🧙 Interactive Mode** - [workflows/interactive-creation.md](workflows/interactive-creation.md)

- Ask questions one at a time
- Wait for user responses
- Confirm understanding at each step
- Best for: first-time creators, complex skills

**⚡ Automatic Mode** - [workflows/create-new-skill.md](workflows/create-new-skill.md)

- Create skill from initial description
- No back-and-forth questions
- Best for: experienced users, clear requirements

**Decision Guide:**

```
User says: "Quiero crear un skill" (no details)
→ Use Interactive Mode

User says: "Create a skill for X that does Y and Z"
→ Use Automatic Mode
```

## Post-Creation Verification Loop

**CRITICAL:** After creating any skill, verify it works correctly.

### Verification Steps

```bash
# 1. Syntax Check - Validate YAML frontmatter
head -30 ~/.config/opencode/skills/<name>/SKILL.md | yq .
# Should parse without errors

# 2. Structure Check - Verify files exist
ls -la ~/.config/opencode/skills/<name>/

# 3. Size Check - Verify SKILL.md length
wc -l ~/.config/opencode/skills/<name>/SKILL.md
# Should be < 650 lines
```

### Functional Tests

| Test              | How                           | Expected                          |
| ----------------- | ----------------------------- | --------------------------------- |
| **Discovery**     | Search for skill in OpenCode  | Skill appears in available skills |
| **Activation**    | Reference skill in context    | Agent loads skill successfully    |
| **Core Function** | Use primary feature           | Works as documented               |
| **Edge Case**     | Empty/ambiguous input         | Handles gracefully                |
| **Links**         | Click all internal references | All links resolve                 |

### Verification Decision Tree

```
1. Create skill files
   ↓
2. YAML syntax valid?
   NO → Fix YAML errors → retry
   YES ↓
3. All required files present?
   NO → Create missing files → retry from step 2
   YES ↓
4. SKILL.md < 650 lines?
   NO → Split to references/ → retry from step 2
   YES ↓
5. Test skill activation
   ↓
6. Skill works as expected?
   NO → Edit content → retry from step 5
   YES ↓
7. ✅ Skill ready for use
```

### Report Template

After verification, report:

```markdown
## Skill Created: {name}

### Configuration

- Complexity: {🟢 Micro | 🟡 Simple | 🟠 Standard | 🔴 Complex}
- Lines: {count}
- Directories: {list}

### Verification

- [x] YAML syntax valid
- [x] Structure complete
- [x] Size within limits
- [x] Activation works
- [x] Links verified

### Usage

- Location: `~/.config/opencode/skills/{name}/`
- Load: Reference in context or skill tool
- Purpose: {brief description}
```

## Success Criteria

A well-structured skill:

- ✅ Has valid YAML frontmatter with `name` and `description`
- ✅ Description includes **WHAT**, **WHEN**, and `<example>` blocks
- ✅ Written entirely in English (LLM efficiency)
- ✅ **Appropriate complexity level** (start with 🟢 Micro, upgrade only when needed)
- ✅ **SKILL.md < 650 lines** (uses references/ for deep dives)
- ✅ **Token-optimized** (tables over prose, links over inline)
- ✅ Includes at least 1 concrete usage example
- ✅ Documents what it **can** and **cannot** do
- ✅ Has README.md for GitHub discoverability
- ✅ Follows Agent Skills standard structure
- ✅ **Has been verified** post-creation (syntax, structure, activation)
- ✅ **Progressive disclosure** (core in SKILL.md, details in references/)
- ✅ No executable scripts (pure markdown)

## Reference Documentation

| Document                                                      | Description                  |
| ------------------------------------------------------------- | ---------------------------- |
| [skill-anatomy.md](references/skill-anatomy.md)               | Complete structure breakdown |
| [frontmatter-spec.md](references/frontmatter-spec.md)         | YAML specification           |
| [validation-checklist.md](references/validation-checklist.md) | Quality verification         |

## Templates

| Template                                       | Use Case               |
| ---------------------------------------------- | ---------------------- |
| [minimal-skill.md](templates/minimal-skill.md) | Basic skill with TODOs |

## Workflows

| Workflow                                                                   | Purpose                                     | When to Use                             |
| -------------------------------------------------------------------------- | ------------------------------------------- | --------------------------------------- |
| [interactive-creation.md](workflows/interactive-creation.md)               | 🧙 Guided wizard with prompts               | User says "crear skill" without details |
| [create-new-skill.md](workflows/create-new-skill.md)                       | ⚡ Quick-start guide (index)                | User provides full description upfront  |
| [skill-discovery-planning.md](workflows/skill-discovery-planning.md)       | Phases 1-2: Discovery and Planning          | Define purpose and structure            |
| [skill-implementation.md](workflows/skill-implementation.md)               | Phase 3: Implementation                     | Create files and content                |
| [skill-validation-publishing.md](workflows/skill-validation-publishing.md) | Phases 4-6: Validation, Testing, Publishing | Verify and share                        |

## Philosophy

> "A great skill is like a well-written manual:
>
> - **Clear** about its purpose (description with examples)
> - **Focused** on one domain (single responsibility)
> - **Organized** for easy reference (SKILL.md + references)
> - **Portable** across platforms (Agent Skills standard)
> - **Documented** for contributors (README + LICENSE)"

Create skills that are **focused**, **clear**, and **reusable**.

## Additional Resources

- **Agent Skills Standard**: https://agentskills.io
- **Anthropic Skills Repo**: https://github.com/anthropics/skills
- **Agent Skills Spec**: https://github.com/agentskills/agentskills
- **OpenCode Docs**: https://opencode.ai/docs/

## Contributing

This skill is open source (MIT). Contributions welcome:

- Report issues
- Suggest improvements
- Share your skills

---

**Version:** 1.2.0  
**Author:** Rodrigo Lago  
**License:** MIT  
**Standard:** Agent Skills (https://agentskills.io)
