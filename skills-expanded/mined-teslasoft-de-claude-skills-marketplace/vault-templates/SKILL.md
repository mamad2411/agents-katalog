---
name: vault-templates
description: |
  All 12 Obsidian vault template specifications with key fields, sections, and usage guidelines.
  Covers Goals, Projects, Areas, Resources, Collab, Science, Skills, Inbox, Archive, CV-Schema,
  Policy, and Prompt templates. Includes Templater syntax and best practices.
  Keywords: template, Templater, apply template, use template, template for goal, project template,
  area template, resource template, create from template
triggers:
  - use template
  - apply template
  - template for goal
  - template for project
  - template for area
  - create from template
  - Templater syntax
  - template best practices
  - available templates
negative_triggers:
  - create note without template
  - PARA structure
  - dataview query
  - frontmatter schema reference
version: 3.7.0
author: Christian Kusmanow / Claude
last_updated: 2026-06-17
---

# Vault Templates

All 12 Obsidian template specifications for the Teslasoft vault. Templates are in `.obsidian/templates/` and use Templater syntax.

## When to Use

- Creating new notes from templates
- Checking which template to use for a note type
- Understanding template key fields and sections
- Reviewing Templater variable syntax

## When NOT to Use

- Understanding PARA folder structure or note types (use `vault-notes`)
- Writing Dataview queries or checking metadata values (use `vault-metadata`)

---

## Available Templates (12 types)

### 1. Goals.md
**Purpose:** Quarterly OKR-style objectives

**Key Fields:**
- `type: goal`
- `status: planning | active | reviewing | completed | partial`
- `horizon: "[[YYYY-Qn]]"` (auto-generated from current date)
- `created: YYYY-MM-DD` (auto-generated)

**Sections:**
- Objective (why it matters)
- Key Results (KR1-KR3)
- Related Projects (links)
- Success Metrics
- Timeline

**Usage:** Create new quarterly goal with `G-YYYY-Qn [Name]` naming

### 2. Projects.md
**Purpose:** Execution projects with task tracking

**Key Fields:**
- `type: project`
- `status: active | planning | completed | on-hold`
- `goal: "[[Goal Name]]"` (required link to parent)
- `repoPath:` (optional external repository)
- `created: YYYY-MM-DD` (auto-generated)

**Sections:**
- Overview
- Goal (contribution to parent)
- Next Actions (checkboxes)
- Dependencies
- Resources
- Repository info
- Status Updates (date-stamped)

**Usage:** Create new project with `P#-[Name]` naming, always link to goal

### 3. Areas.md
**Purpose:** Long-term responsibility domains

**Key Fields:**
- `type: area`
- `projects: []` (links to active projects)
- `resources: []` (links to resources)
- `created: YYYY-MM-DD` (auto-generated)

**Sections:**
- Purpose & Scope
- Active Projects
- Key Resources
- Responsibilities
- Skills Required
- Stakeholders
- Metrics
- Review Cycle

**Usage:** Define ongoing areas of responsibility, link to projects/resources

### 4. Resources.md
**Purpose:** Reference materials, tools, frameworks

**Key Fields:**
- `type: resource`
- `category:` (AI, IoT, Hosting, etc.)
- `repoPath:` (optional)
- `created: YYYY-MM-DD` (auto-generated)

**Sections:**
- Overview & Purpose
- Key Features
- Related Areas/Projects
- Repository/Source
- Quick Start
- Examples
- Pros & Cons
- Alternatives

**Usage:** Keep lightweight (1-5 lines) unless deep-dive, organize in category subdirectories

### 5. Collab.md
**Purpose:** Partnership and collaboration tracking

**Key Fields:**
- `type: collaboration`
- `partner:` (partner name)
- `status: active | planning | paused | completed`
- `patreonURL:` (optional)
- `contactEmail:` (optional)
- `created: YYYY-MM-DD` (auto-generated)

**Sections:**
- Partner Overview
- Collaboration Purpose
- Key Contacts
- Links (Patreon, website, GitHub)
- Scope & Deliverables
- Timeline & Communication
- Agreement/Terms

**Usage:** Track partnerships, sponsorships, joint ventures

### 6. Science.md
**Purpose:** Research and architectural exploration

**Key Fields:**
- `type: research`
- `status: exploring | active | blocked | parked | concluded | integrated`
- `created: YYYY-MM-DD` (auto-generated)

**Sections:**
- Research Question
- Hypothesis
- Approach & Key Concepts
- Findings (date-stamped)
- Architectures/Patterns
- Code Examples
- References
- Related Areas/Projects
- Conclusions

**Usage:** Document investigations, novel patterns, design decisions

### 7. Skills.md
**Purpose:** Professional competency tracking

**Key Fields:**
- `type: skill`
- `level: novice | developing | proficient | expert | master`
- `created: YYYY-MM-DD` (auto-generated)

**Sections:**
- Skill Level & Overview
- Core Competencies
- Learning Path (novice to master)
- Current Level Assessment
- Experience (projects, professional)
- Learning Resources
- Related Skills/Areas/Goals
- Progress Log (date-stamped)

**Usage:** Track professional development, competency growth

### 8. Inbox.md
**Purpose:** Quick capture for processing later

**Key Fields:**
- `captured: YYYY-MM-DD HH:mm` (auto-generated)
- `processed: false`
- `tags: [inbox]`

**Sections:**
- Quick Capture (unstructured)
- Context
- Next Action
- Category (checkboxes for destination)
- Processing Notes

**Usage:** Fast capture without structure, process regularly to proper locations

### 9. Archive.md
**Purpose:** Preserve completed/inactive notes

**Key Fields:**
- `type: archive`
- `originalType:` (goal, project, etc.)
- `archivedDate: YYYY-MM-DD` (auto-generated)
- `originalLocation:` (original folder path)
- `tags: [archived]`

**Sections:**
- Archive Information
- Original Content (preserved below)

**Usage:** Move completed items to 90_Archive/ with context preserved

### 10. CV-Schema.md
**Purpose:** Schema definition for structured CV data (TypeScript interfaces)

**Sections:**
- Schema Version
- Data Structure (root-level type definition)
- Type Definitions (CVMetadata, PersonalInfo, Language, Profile, TechnicalSkills, Education, ProfessionalExperience)
- File Naming Convention (cv-de.json, cv-en.json)
- Usage Guidelines
- Integration Points

**Usage:** Define or update the CV data schema; used by sync-cv and P4/P10

### 11. Policy.md
**Purpose:** Governance policy definition with enforcement rules

**Key Fields:**
- `type: policy`
- `policy_id:` (e.g., NDP-001, VOP-001)
- `version:` (semver)
- `status: active`
- `enforcement: BLOCK | WARN | ADVISORY`
- `scope: []`
- `created: YYYY-MM-DD` (auto-generated)

**Sections:**
- Overview & Scope
- Policy Rules (with enforcement level, rationale, examples)
- Enforcement (hooks, telemetry, audits)
- Incident History
- Exceptions
- Version History

**Usage:** Create governance policies in `coordination/policies/`

### 12. Prompt.md
**Purpose:** Structured prompt files for agent automation

**Key Fields:**
- `purpose:` (category)
- `description:` (brief summary)
- `skills: []` (required skills)
- `tools: []` (required tools)
- `agent:` (target agent)
- `created: YYYY-MM-DD` (auto-generated)

**Sections:**
- Context
- Task
- Inputs
- Expected Output
- Constraints
- Success Criteria

**Usage:** Create reusable prompts in `.prompts/` directories

---

## Template Best Practices

1. **Use Templater variables:**
   - `{{date:YYYY-MM-DD}}` - Current date
   - `{{date:YYYY-[Q]Q}}` - Current quarter
   - `{{title}}` - File title
   - `{{date:YYYY-MM-DD HH:mm}}` - Date with time

2. **Preserve template structure:**
   - Keep section headers consistent
   - Maintain frontmatter field names
   - Use comments for guidance

3. **Customize for workflow:**
   - Add sections as needed
   - Remove unused sections after creation
   - Adapt to specific use cases

4. **Link early and often:**
   - Use `[[]]` syntax for internal links
   - Connect to parent notes (goals, areas)
   - Create bidirectional relationships

---

## Cross-References

- **Note types and PARA structure**: Invoke `vault-notes` for naming conventions and category guidance
- **Metadata values and Dataview**: Invoke `vault-metadata` for status/type/horizon values and query patterns

---

## Metadata

```yaml
author: Christian Kusmanow / Claude
version: 1.2.0
last_updated: "2026-03-21"
source: Extracted from CLAUDE.md (Template Reference section, lines 244-505)
change_surface: Template specifications, best practices
extension_points: Add new template types
changelog:
  - "1.0.0: Initial extraction from CLAUDE.md"
```
